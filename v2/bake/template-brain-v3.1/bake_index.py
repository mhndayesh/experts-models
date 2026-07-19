#!/usr/bin/env python3
"""bake_index.py - bake the D7 INVERTED-INDEX retriever into a real gemma-4 GGUF.

This replaces the v3.4 linear scanner with the design proven in jinja_lab:
  * inverted index: term -> "factid:weight" postings, keys stored ONCE globally
  * facts in a LIST (integer ids) - minja builds lists fast and dicts slowly
    (measured: dict facts 1318 ms/request vs list facts 291 ms)
  * curated facts sorted FIRST, so provenance is `id < FB_NCUR` and costs no bytes
  * gate: a NAMED library wins; inferred tabs only when nothing is named
  * delivery unchanged: the forged native tool exchange, rendered BEFORE the
    user's question (the F-042 echo fix) via the source's own macro

Measured against the shipped scanner on the same 2,560-fact bank:
  retrieval 9/12 vs 6/12 gold | 809 KB vs 949 KB | 545 ms vs 2,629 ms per matched request

HARD REQUIREMENT (learned the expensive way): llama.cpp PROBES the chat template
at load time with synthetic inputs (multimodal content lists, empty message
arrays, tool defs) to auto-detect the tool-call format. A template that throws on
any of them makes llama.cpp reject the ENTIRE model. Every code path here is
guarded by `fbok`.

usage:
  python bake_index.py --facts facts_pythondata_v4.jsonl --out baked_index.jinja \
      [--src-gguf ... --dst-gguf ...]
"""
import argparse, collections, json, math, os, re, sys

sys.path.insert(0, "jinja_lab")
from designs import STOPW, INTENT, norm            # one source of truth
from enrich import strong_keywords, auto_phrases, derive_library, norm_control, COMMON_DF
from bake_template_v3 import (ANCHORS, OPT_ANCHORS, INSERT_FILES, MACRO_PATCH,
                              check_base_is_source_plus_anchors, write_baked,
                              GATE_ALIASES, pad)

FB_MAX = 5
DF_CAP = 40

# The ONLY route that still has a size wall: LM Studio loading a raw .gguf by
# hand. Its GGUF-metadata reader silently swaps an over-long template for a
# 48-char sentinel (F-053), so the model loads "fine" and answers garbage.
# 980,000 bytes == 957 KiB. The docs used to quote both numbers plus a loose
# "950 KB" and it read as three different limits; it is ONE limit.
#
# This is NOT a default. llama.cpp caps at 1 GiB and errors loudly; the LM
# Studio Hub `model.yaml` route (llm.load.promptTemplate) has no size limit at
# all — proven live at 1.5 MB and 2.0 MB (F-059). The wall is one application's
# undocumented bug on one route, and it is opt-in via --route rawgguf.
RAWGGUF_CAP = 980_000

# DETERMINISM: every set/dict iteration below is sorted, and every JSON blob is
# emitted with sort_keys=True. Python randomizes string hashing PER PROCESS, so
# without this two runs of the same command produced templates with identical
# content but different key ORDER - byte-different, semantically equal. That
# breaks the repo's rule that a shipped artifact must be regenerable from source.


def is_curated(fid):
    return "api-" not in fid


_SENTINEL = re.compile(r" at 0x[0-9A-Fa-f]+>")


def sanitize(text):
    """Strip repr() memory addresses captured by the miner.

    13 shipped facts carry them, e.g.
        pandas.Timedelta(value=<object object at 0x000001A8A4C73BD0>, unit=None, ...)
    The miner introspected a live sentinel default and wrote its repr(). The address
    changes every process, so those facts also made the BANK NON-REPRODUCIBLE - the
    exact property F-058 exists to protect. They tell the model nothing either.
    """
    return _SENTINEL.sub(">", text)


def cluster_facts(pre):
    """Near-duplicate clusters, by term overlap WITHIN a library (Jaccard >= 0.5).

    The measured failure (reach.py, 2026-07-14): four pandas facts all describe the
    pandas 3.0 `str` dtype. They share their words, so they (a) match anything
    pandas-shaped and steal 247 slots across the library, and (b) split the vote
    among themselves - all four are UNREACHABLE by their own questions.

    Global IDF cannot see this: `dtype` is rare across the whole bank, but within
    this cluster it is what the facts have in COMMON, so it carries zero
    information. The terms that matter are the ones that SEPARATE siblings
    (`assign`, `values`, `prod`). That is what --discriminative uses this for.
    """
    parent = list(range(len(pre)))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[max(ra, rb)] = min(ra, rb)

    by_lib = collections.defaultdict(list)
    for i, (r, lib, keys) in enumerate(pre):
        by_lib[lib].append(i)
    for lib in sorted(by_lib):
        idx = by_lib[lib]
        for a in range(len(idx)):
            ka = pre[idx[a]][2]
            if not ka:
                continue
            for b in range(a + 1, len(idx)):
                kb = pre[idx[b]][2]
                if not kb:
                    continue
                inter = len(ka & kb)
                if inter and inter / len(ka | kb) >= 0.5:
                    union(idx[a], idx[b])
    groups = collections.defaultdict(list)
    for i in range(len(pre)):
        groups[find(i)].append(i)
    return {i: groups[find(i)] for i in range(len(pre))}


def build(facts_path, controls_path, taskwords_path, gate_n=48, expansions_path=None,
          idf="bucket", discriminative=False, len_norm=False, gate_expansions=False,
          gate_exp_minlen=5, gate_exp_max_df=999, rescue_gate=False, extra_aliases_path=None):
    rows = [json.loads(l) for l in open(facts_path, encoding="utf-8") if l.strip()]
    controls = [norm_control(l.strip()) for l in open(controls_path, encoding="utf-8") if l.strip()]
    taskwords = json.load(open(taskwords_path, encoding="utf-8"))
    # Doc2Token expansions: the model's own predictions of how a USER would ask
    # for each curated fact. Indexed at a LOWER weight than real terms (the
    # literature is explicit: expansions that outrank real evidence hurt - and
    # Doc2Query-- showed FILTERING them improves quality AND shrinks the index).
    expansions = {}
    if expansions_path and os.path.exists(expansions_path):
        expansions = json.load(open(expansions_path, encoding="utf-8"))

    # curated first -> provenance is a number comparison in the template
    rows.sort(key=lambda r: (not is_curated(r["id"]),))
    ncur = sum(1 for r in rows if is_curated(r["id"]))

    # ---- per-fact keys (same rules as enrich.py) ----
    df = collections.Counter()
    pre = []
    for r in rows:
        lib = derive_library(r)
        keys = set(strong_keywords(r, lib))
        pre.append((r, lib, keys))
        df.update(keys)

    txt, libs_of, post = [], [], collections.defaultdict(list)
    all_terms = []
    culled = 0
    for i, (r, lib, keys) in enumerate(pre):
        ver = r.get("version") or "unversioned"
        txt.append(f'{sanitize(r["text"])} [version: {ver}] [src: {r.get("source","?")}]')
        libs_of.append(lib)
        curated = is_curated(r["id"])
        terms = collections.Counter()
        deadish = r.get("kind") == "mistake" or any(
            m in r["text"].lower() for m in
            (" renamed", " removed", " deprecated", " no longer", " replaced"))
        for k in sorted(keys):
            kk = k.strip()
            if not kk or " " in kk:
                continue
            if any(k in c for c in controls):      # control cull (F-046)
                culled += 1
                continue
            w = 4 if df[k] <= COMMON_DF else 1
            if deadish and kk != lib and df[k] <= 3:
                w = 10                              # dead name: strongest evidence
            terms[kk] += w
        phrases = taskwords.get(r["id"]) or auto_phrases(txt[-1])
        for p in phrases:
            ws = [w for w in p.lower().split() if len(w) > 2 and w not in STOPW]
            for w in ws:
                terms[w] += 2
            for a, b in zip(ws, ws[1:]):
                terms[a + "_" + b] += 3
        # Doc2Query-- : expansions must be FILTERED, not dumped in whole. Bytes
        # are the budget (F-048), so we keep what discriminates: the PHRASES
        # (bigrams - "turn_columns" is the signal) and only the longer unigrams.
        # Dumping all 6 phrases' words blew the template to 1,077 KB.
        for p in expansions.get(r["id"], [])[:5]:
            ws = [w for w in norm(p).split() if len(w) > 2 and w not in STOPW]
            for w in ws:
                if len(w) >= 5:
                    terms[w] += 1                       # below real terms, on purpose
            for a, b in zip(ws, ws[1:]):
                terms[a + "_" + b] += 2                 # the phrase IS the signal
        desc = txt[-1].split(" - ", 1)[1] if " - " in txt[-1] else txt[-1]
        dw = 3 if curated else 1
        for w in [w for w in norm(desc).split() if len(w) > 3 and w not in STOPW][:24]:
            terms[w] += dw
        # SQUASH-NORMALISATION + identifier splitting (PRIOR-ART-ALIASES steal #1).
        # "ttest_ind" is also findable as "ttest"/"ind"/"ttestind"; "scikit-learn"
        # as "scikitlearn". Costs no extra facts - only extra postings - and it is
        # what makes a user's "t-test" reach scipy.stats.ttest_ind.
        extra = collections.Counter()
        for t, w in sorted(terms.items()):
            if w < 4:
                continue          # only API-name tokens (weight >= 4) earn variants:
                                  # squashing every description word blew the index
                                  # from 11k to 18k terms and tripped the size guard.
            sq = t.replace("-", "").replace("_", "").replace(".", "")
            if sq != t and len(sq) >= 4:
                extra[sq] = max(extra[sq], w)        # a squashed API name IS the API name
            for part in t.replace(".", "_").replace("-", "_").split("_"):
                if len(part) >= 4 and part not in STOPW and part != t:
                    # "ttest" out of "ttest_ind" is the user's word for that API -
                    # weighting it at half made it lose to generic description words
                    extra[part] = max(extra[part], w if len(part) >= 5 else max(2, w // 2))
        for t, w in sorted(extra.items()):
            terms[t] = max(terms.get(t, 0), w)
        all_terms.append(terms)

    # ---- DISCRIMINATIVE re-weighting (off by default) ----
    # A term's value is not "how rare in the bank" but "how well does it SEPARATE
    # this fact from its nearest neighbours". A term every sibling in the cluster
    # shares cannot discriminate between them, however rare it is globally.
    if discriminative:
        clusters = cluster_facts(pre)
        for i, terms in enumerate(all_terms):
            sibs = clusters[i]
            if len(sibs) < 2:
                continue
            for t in sorted(terms):
                shared = sum(1 for j in sibs if t in all_terms[j])
                frac = shared / len(sibs)
                if frac >= 0.5 and shared >= 2:
                    terms[t] = max(1, terms[t] // 3)     # common to the cluster: mute it
                elif shared == 1 and terms[t] >= 3:
                    terms[t] += 3                         # unique to THIS sibling: the signal

    # ---- LENGTH NORMALISATION (off by default) ----
    # BM25's other half, which we never had: a long fact matches more terms and wins
    # by accident. Damp each fact's weights by how many terms it carries.
    if len_norm:
        avg = sum(len(t) for t in all_terms) / max(1, len(all_terms))
        for terms in all_terms:
            f = avg / max(1.0, len(terms))
            damp = min(1.3, max(0.7, f))
            for t in sorted(terms):
                terms[t] = max(1, int(round(terms[t] * damp)))

    for i, terms in enumerate(all_terms):
        for t, w in sorted(terms.items()):
            if t and ":" not in t and " " not in t:
                post[t].append(f"{i}:{w}")

    # IDF: a term that points at 3 facts is EVIDENCE; a term that points at 34 is
    # noise. Without this, "test" (34 postings, from every scipy docstring) outvoted
    # "ttest" (3 postings) and a t-test question returned scipy.stats.dunnett.
    # Multiplied at BUILD time - the runtime stays integer addition.
    #   bucket : the shipped 3-step guess (x3 / x2 / x1)
    #   smooth : real IDF, log(N/df), rounded to an integer multiplier
    scaled = {}
    N = len(rows)
    for t, v in post.items():
        if len(v) > DF_CAP:
            continue
        if idf == "smooth":
            mult = max(1, min(8, int(round(math.log(N / len(v))))))
        else:
            mult = 3 if len(v) <= 3 else (2 if len(v) <= 10 else 1)
        scaled[t] = " ".join(f"{p.split(':')[0]}:{int(p.split(':')[1]) * mult}" for p in v)
    post = scaled

    # ---- gate ----
    libnames = sorted({l for l in libs_of})
    by_lib = collections.defaultdict(list)
    for (r, lib, keys) in pre:
        by_lib[lib].append((r, keys))

    # how many LIBRARIES does each expansion word appear in? A gate trigger must be
    # unique to one library, or "error"/"column" would open every tab at once.
    xdf = collections.Counter()
    if gate_expansions:
        seen = collections.defaultdict(set)
        for (r, lib, keys) in pre:
            for p in expansions.get(r["id"], [])[:5]:
                for w in norm(p).split():
                    if len(w) >= 5 and w not in STOPW:
                        seen[w].add(lib)
        for w, libs in seen.items():
            xdf[w] = len(libs)                          # a trigger must live in exactly 1
    trig = {}
    for lib in libnames:
        facts = by_lib[lib]
        cnt = collections.Counter(k for _, keys in facts for k in keys)
        # a trigger must be UNIQUE to this library, and we want the words a USER
        # would type ("resample", "dataframe"), not internal plumbing
        # ("create_block_manager_from_blocks"). Curated facts' keywords first,
        # then SHORT keys - sorting by -len picked the plumbing and lost the
        # "FutureWarning about frequency alias M" question (no library named).
        cur_keys = {k for r, keys in facts if is_curated(r["id"]) for k in keys}
        uniq = [k.strip() for k, c in sorted(cnt.items())
                if df[k] == c and k.strip() and " " not in k.strip()
                # a gate trigger must never be a word a CONTROL question uses:
                # short curated keys are the words users type, but some of them
                # are also plain English ("sort", "value") and opened tabs on a
                # haiku. The cull already protects the index; the gate needs it
                # too (F-046, second bite).
                and not any(pad(k) in c for c in controls)
                and len(k.strip()) >= 4]
        uniq.sort(key=lambda k: (pad(k) not in cur_keys, len(k)))
        gate_words = uniq[:gate_n]

        # GATE FROM EXPANSIONS (off by default).
        # Measured 2026-07-14: 66% of unreachable curated facts die AT THE GATE - no
        # tab opens, so the index is never consulted and ranking never runs. The
        # questions that kill them are pure symptom language ("chained assignment
        # error after upgrade") - no library name, no API token, so no trigger.
        # But the Doc2Token expansions ARE that language: the model already wrote it.
        # We index those words and never told the GATE about them. This does.
        # Control words are already culled from the index (F-046) and are culled here
        # too, so a haiku still opens nothing.
        if gate_expansions:
            cnt_x = collections.Counter()
            for r, _keys in facts:
                for p in expansions.get(r["id"], [])[:5]:
                    for w in norm(p).split():
                        if len(w) >= gate_exp_minlen and w not in STOPW:
                            cnt_x[w] += 1
            for w in sorted(cnt_x):
                # A trigger must be SPECIFIC, or it opens the wrong tab. Three tests,
                # and the third is the one that matters: a word used by many facts is
                # generic phrasing ("replacement", "instead"), not a topic. It was
                # such a word - unique to pandas only by accident - that opened the
                # PANDAS tab on the numpy question "is there a replacement for np.fix?"
                if (xdf[w] == 1                                      # only one library
                        and cnt_x[w] <= gate_exp_max_df              # used by few facts = specific
                        and not any(pad(w) in c for c in controls)):
                    gate_words.append(w)

        trig[lib] = "|".join([lib] + gate_words
                             + [a.strip() for a in GATE_ALIASES.get(lib, [])])

    alias = {k: v for k, v in json.load(open("aliases.json", encoding="utf-8")).items()
             if not k.startswith("_") and v in libnames}
    # per-expert gate aliases (2026-07-17 fix): natural names + OLD rename names must open
    # a library's tab, or a stale user's wording ("BloodHound", "CrackMapExec") shuts the
    # gate and ZERO facts reach the model. Same class as the volatility3 gate-vocab death.
    if extra_aliases_path and os.path.exists(extra_aliases_path):
        for k, v in json.load(open(extra_aliases_path, encoding="utf-8")).items():
            if not k.startswith("_") and v in libnames:
                alias[k] = v
    for a, canon in alias.items():                 # the gate is a FILTER: aliases
        trig[canon] += "|" + a                     # must open the tab too, or it
                                                   # rejects the facts the query
                                                   # would have found (PRIOR-ART #10)
    # ---- RESCUE MAP: dead API name -> its library ----
    # The narrowest possible escape from a fatal gate. A term qualifies ONLY if it is
    # a weight-10 dead API name (renamed/removed - the strongest evidence the index
    # has), points at exactly one library, and appears in no control question.
    # Deleting the gate outright fired 8/10 controls; this cannot, because a haiku
    # contains no `safe_eval`.
    rescue = {}
    if rescue_gate:
        owner = {}
        for i, terms in enumerate(all_terms):
            for t, w in terms.items():
                if w >= 10:
                    owner.setdefault(t, set()).add(libs_of[i])
        for t in sorted(owner):
            if (len(owner[t]) == 1 and len(t) >= 4
                    and t not in STOPW
                    and not any(pad(t) in c for c in controls)):
                rescue[t] = sorted(owner[t])[0]

    return dict(post=post, txt=txt, lib=libs_of, ncur=ncur, names=libnames,
                trig=trig, culled=culled, nfacts=len(rows), alias=alias, rescue=rescue)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--facts", required=True)
    ap.add_argument("--controls", default="controls_pydata.txt")
    ap.add_argument("--taskwords", default="taskwords_pydata.json")
    ap.add_argument("--expansions", default="expansions_v2.json",
                    help="Doc2Token predicted user wording per curated fact. "
                         "v2 is the GOOD file: a stale background job once clobbered "
                         "expansions.json (388 good facts -> 90 garbage), so the "
                         "original name is retired. Never let two jobs share an "
                         "output path; version the filename.")
    ap.add_argument("--base", default="family_bases/gemma4.jinja")
    ap.add_argument("--source-template", default="family_bases/gemma4.source.jinja")
    ap.add_argument("--family", default="gemma4_idx")
    ap.add_argument("--out", required=True)
    ap.add_argument("--gate-n", type=int, default=48)
    # --- retrieval experiments. Defaults reproduce the SHIPPED template byte-for-byte. ---
    ap.add_argument("--idf", choices=["bucket", "smooth"], default="bucket",
                    help="bucket = the shipped 3-step guess; smooth = real log(N/df) IDF")
    ap.add_argument("--discriminative", action="store_true",
                    help="weight a term by how well it SEPARATES a fact from its "
                         "near-duplicate siblings, not just by global rarity")
    ap.add_argument("--len-norm", action="store_true",
                    help="BM25 length normalisation: damp facts that carry many terms")
    ap.add_argument("--gate-exp-minlen", type=int, default=5,
                    help="minimum length of an expansion-derived gate trigger")
    ap.add_argument("--gate-exp-max-df", type=int, default=999,
                    help="max facts an expansion word may appear in and still be a "
                         "trigger. Low = only SPECIFIC words open a tab.")
    ap.add_argument("--rescue-gate", action="store_true",
                    help="when NO library tab opens, let a weight-10 dead API name open "
                         "its own library. Requires --family gemma4_rescue.")
    ap.add_argument("--gate-expansions", action="store_true",
                    help="let the GATE see the Doc2Token expansion words, not just API "
                         "keys. 66%% of unreachable curated facts die at the gate on "
                         "symptom-language questions that name no library and no API.")
    ap.add_argument("--extra-aliases", default=None,
                    help="per-expert gate aliases {token: lib} from gen_gate_aliases.py; "
                         "makes natural/old names open the library tab (2026-07-17 gate fix)")
    ap.add_argument("--src-gguf"); ap.add_argument("--dst-gguf")
    # THE ~1 MB WALL IS DEAD (F-059). It was never a GGUF limit or an engine
    # limit - it lives ONLY in LM Studio's GGUF-metadata READER, which silently
    # swaps an over-long template for a 48-char sentinel. llama.cpp caps at
    # 1 GiB and errors LOUDLY; LM Studio's Hub `model.yaml` load-config path has
    # no size limit at all (proven live at 1.5 MB and 2.0 MB).
    #
    # So there is NO DEFAULT CAP. Capping by default made the wall look like a
    # property of the format instead of one application's undocumented bug, and
    # it silently blocked the big-bank work.
    #
    # The guard survives as an OPT-IN for the one route that still has the wall:
    #   --route rawgguf   -> hard-fail above RAWGGUF_CAP (a brick can never ship)
    #   --route llamacpp  -> no cap (default)
    #   --route hub       -> no cap
    # Over-size bakes still print a LOUD warning, because F-053's failure mode is
    # SILENT: the model loads "fine" and answers garbage.
    ap.add_argument("--route", choices=("llamacpp", "hub", "rawgguf"),
                    default="llamacpp",
                    help="delivery route. Only 'rawgguf' (LM Studio loading the "
                         ".gguf by hand) has a size wall; it is enforced as a "
                         "hard fail. llamacpp/hub have NO size limit (F-059).")
    ap.add_argument("--max-bytes", type=int, default=None,
                    help="explicit size ceiling in bytes. Default: NONE. "
                         f"--route rawgguf implies {RAWGGUF_CAP:,}.")
    a = ap.parse_args()

    d = build(a.facts, a.controls, a.taskwords, a.gate_n, a.expansions,
              idf=a.idf, discriminative=a.discriminative, len_norm=a.len_norm,
              gate_expansions=a.gate_expansions, gate_exp_minlen=a.gate_exp_minlen,
              gate_exp_max_df=a.gate_exp_max_df, rescue_gate=a.rescue_gate,
              extra_aliases_path=a.extra_aliases)
    print(f"{d['nfacts']} facts ({d['ncur']} curated) | {len(d['post'])} index terms "
          f"| {len(d['names'])} libraries | {d['culled']} keys culled by controls")

    base = open(a.base, encoding="utf-8").read()
    source_tpl = open(a.source_template, encoding="utf-8").read()
    check_base_is_source_plus_anchors(base, source_tpl)

    ins_dir = os.path.join("inserts", a.family)
    inserts = {a_: open(os.path.join(ins_dir, INSERT_FILES[a_]), encoding="utf-8").read()
               for a_ in ANCHORS + OPT_ANCHORS}
    top = open(os.path.join(ins_dir, "top.jinja"), encoding="utf-8").read()

    preloop = (inserts["{#FB_PRELOOP#}"]
               .replace("__POST__", json.dumps(d["post"], ensure_ascii=False, sort_keys=True))
               .replace("__TXT__", json.dumps(d["txt"], ensure_ascii=False))
               .replace("__LIB__", json.dumps(d["lib"], ensure_ascii=False))
               .replace("__NAMES__", json.dumps(d["names"], ensure_ascii=False))
               .replace("__TRIG__", json.dumps(d["trig"], ensure_ascii=False, sort_keys=True))
               .replace("__STOPW__", json.dumps(sorted(STOPW), ensure_ascii=False))
               .replace("__INTENT__", json.dumps(sorted(INTENT), ensure_ascii=False))
               .replace("__ALIAS__", json.dumps(d["alias"], ensure_ascii=False, sort_keys=True))
               .replace("__NCUR__", str(d["ncur"]))
               .replace("__FBMAX__", str(FB_MAX))
               .replace("__RESCUE__", json.dumps(d["rescue"], ensure_ascii=False, sort_keys=True)))
    menu = ", ".join(d["names"])
    out = base.replace("{#FB_PRELOOP#}", preloop)
    out = out.replace("{#FB_SYS#}", inserts["{#FB_SYS#}"].replace("__MENU__", menu))
    for anc in ("{#FB_USER#}", "{#FB_HOOK#}", "{#FB_TOOLMSG#}", "{#FB_GEN#}"):
        out = out.replace(anc, inserts[anc])
    for anc in ANCHORS + OPT_ANCHORS:
        assert anc not in out, f"anchor {anc} not consumed"
    patch = "" if "macro format_type_argument" in source_tpl else MACRO_PATCH
    tpl = patch + top + out

    nbytes = len(tpl.encode())
    cap = a.max_bytes if a.max_bytes is not None else (
        RAWGGUF_CAP if a.route == "rawgguf" else None)

    if cap is not None and nbytes > cap:
        sys.exit(f"[rawgguf guard] template is {nbytes:,} B > {cap:,} B. "
                 f"LM Studio's GGUF-metadata reader would SILENTLY swap it for a "
                 f"48-char sentinel (F-053): the model loads 'fine' and answers "
                 f"garbage. Cut facts (select_facts.py), or ship via --route "
                 f"llamacpp / hub, which have no size limit (F-059).")

    open(a.out, "w", encoding="utf-8").write(tpl)
    print(f"template: {a.out} ({nbytes:,} B = {nbytes/1024:.0f} KiB)  route={a.route}")

    # F-053's failure mode is SILENT. Never let an over-size template out the
    # door quietly, even on a route that permits it - the same file may later be
    # loaded by hand as a raw GGUF.
    if nbytes > RAWGGUF_CAP:
        print(f"\n  !! {nbytes:,} B is OVER the raw-GGUF ceiling ({RAWGGUF_CAP:,} B).")
        print("  !! This template is fine for llama.cpp and for the LM Studio Hub")
        print("  !! model.yaml route (llm.load.promptTemplate - no size limit, proven")
        print("  !! at 1.5 MB and 2.0 MB, F-059). It will NOT work if someone loads")
        print("  !! the raw .gguf by hand in LM Studio: it degrades SILENTLY to a")
        print("  !! 48-char sentinel and the model answers garbage (F-053).")
        print("  !! Verify the applied bytes with lmstudio_yaml_test/check_override.py.\n")

    if a.src_gguf and a.dst_gguf:
        write_baked(a.src_gguf, a.dst_gguf, tpl,
                    open(a.facts, encoding="utf-8").read(), version="0.4.0")
        print("baked:", a.dst_gguf)


if __name__ == "__main__":
    main()
