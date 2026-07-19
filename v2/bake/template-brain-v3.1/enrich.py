#!/usr/bin/env python3
"""enrich.py v3 - facts_v2.jsonl (id,text,source,version,kind,meta)
                  -> bank_enriched.jsonl for the template-brain bake.

usage: python enrich.py RAW.jsonl OUT.jsonl [--controls FILE] [--taskwords FILE]

Keyword policy (audit points 5, 9):
  strong  = tokens with code signal (has _ . ( ) digits-mixed) OR exact
            library names. min length 3. One strong hit injects.
  weak    = task phrases from --taskwords (LLM-mined offline). min length
            5. Two weak hits inject.
  STOP    = common-word stoplist; plain English single words are never
            keywords at all.
Culling (point 7): any keyword that substring-matches any control line
is deleted, with a report.
Library (point 6): meta.library first, then HOSTMAP on the source URL,
else UNREVIEWED:<hint>; bake refuses UNREVIEWED.
Text (point 11): text + [version] + [src] + fact id carried through.
Header (point 19): first output line records sha256 of the raw file.
"""
import json, re, sys, hashlib

HOSTMAP = {
    "pola.rs": "polars", "pola-rs.github.io": "polars",
    "requests.readthedocs.io": "requests", "docs.python-requests.org": "requests",
    "docs.pydantic.dev": "pydantic", "pydantic.dev": "pydantic",
    "docs.python.org": "python", "peps.python.org": "python", "python.org": "python",
    "fastapi.tiangolo.com": "fastapi", "python-httpx.org": "httpx",
    "litestar.dev": "litestar", "numpy.org": "numpy",
    "pandas.pydata.org": "pandas", "docs.pytest.org": "pytest",
}
STOP = set("""the a an and or of in on for with to from is are was be has have
does do not no use used using new old this that these those it its api apis
call calls function functions method methods argument arguments version
removed renamed deprecated instead now longer error must should can will
default value values string int list dict none true false
script scripts file files folder name names main print write read run test
start stop line lines text code word words item items index count output
input time data type types key keys get set add app apps project projects
strings json command commands node module modules package packages
import imports config open close next first last new
struct structs convert converts concatenate concat float floats integer
integers array arrays hash tuple tuples vector vectors bool boolean char
chars double sort sorted split join replace trim strip find insert remove
append push pop slice map filter reduce fold range random sleep parse
format length size empty contains delete create copy clone update send
receive spawn wait yield match compare equal number numbers object objects
field fields element elements date dates datetime""".split())
COMMON_DF = 8      # strong keys in more than this many facts are "common" (weight 1)
MAX_RARE = 8       # per-fact keyword caps: the template is byte-rationed (F-048)
MAX_COMMON = 3
CODE_SIG = re.compile(r"[._()]|\d")
TOKEN = re.compile(r"[A-Za-z_][A-Za-z0-9_.]*(?:\(\))?")

def host_of(url):
    m = re.match(r"https?://([^/]+)/?", url or "")
    return m.group(1).lower().removeprefix("www.") if m else ""

def derive_library(r):
    meta = r.get("meta") or {}
    if isinstance(meta, dict) and meta.get("library"):
        return str(meta["library"]).lower()
    src = r.get("source", "")
    if src and not src.startswith(("http://", "https://")):
        # repo schema (facts_v2.jsonl): source IS the curated module/package
        # name; the URL lives in meta.url. Per-module tabs beat one giant
        # "python" tab for gate recall.
        return src.lower()
    h = host_of(src) or host_of(meta.get("url", "") if isinstance(meta, dict) else "")
    if h in HOSTMAP:
        return HOSTMAP[h]
    return "UNREVIEWED:" + (h or "no-source")

CAMEL = re.compile(r"[a-z][A-Z]")

def strong_keywords(r, lib):
    out = set()
    if not lib.startswith("UNREVIEWED:"):
        out.add(lib)                      # padded with the rest at return
        # the name people SAY is not always the import name: without this,
        # a question saying "scikit-learn" opens the sklearn TAB (bake's
        # GATE_ALIASES) but matches no FACT - not even the floor pass, whose
        # lib-name hit is what makes it fire. Aliases must live in both.
        for al in GATE_ALIASES.get(lib, []):
            out.add(al.strip())
    for raw in TOKEN.findall(r["text"]):
        raw = raw.rstrip(".")
        t = raw.lower()
        if len(t) < 3 or t in STOP:
            continue
        if CODE_SIG.search(raw) or CAMEL.search(raw):
            core = t.rstrip("()")
            if "." in core:               # datetime.utcnow -> phrase + segments
                out.add(core.replace(".", " "))
                for seg in core.split("."):
                    # 3 chars, not 4: the discriminating token of "np.NaN" IS
                    # "nan" (also inf, pad, loc, iat...). At a 4-char floor the
                    # np.NaN question had NO specific term to match and lost to
                    # sibling facts that shared generic expansion phrases.
                    if len(seg) >= 3 and seg not in STOP:
                        out.add(seg)
            elif core not in STOP:        # "App()" -> "app" must not bypass STOP
                out.add(core)
    # both-side space padding = word boundaries after the templates
    # normalize punctuation to spaces (audit point 9)
    # the library name itself is exempt from the 3-char minimum: padding
    # already makes it word-boundary-exact (" uv " cannot false-fire)
    return sorted(" " + k + " " for k in out if len(k.strip()) >= 3 or k == lib)

from bake_template_v3 import GATE_ALIASES   # one source of truth for aliases

# --- auto task phrases for signature facts -----------------------------------
# A mined signature fact ("sklearn.model_selection.train_test_split(*arrays,
# test_size=None, ...) - Split arrays or matrices into random train and test
# subsets.") is only reachable by someone who ALREADY knows the function name.
# Real users ask "how do i split data into train and test sets". The docstring
# summary is the library's own description of exactly that intent, so we mine
# weak (task) phrases from it: content-word bigrams/trigrams. Weak phrases only
# score INSIDE an already-open library tab, which is what keeps this safe - and
# every phrase still passes the control cull.
PHRASE_STOP = set("""the a an and or of in on for with to from is are was be as at by
this that these those it its into onto over under between each per if then else
return returns returned given using use used based only also new all any not no
same other another which whose when where while will can may must should would
you your we our they their he she his her i me my mine ours yours theirs
object objects value values result results type types list lists dict dicts
none true false self cls args kwargs default defaults optional required
parameter parameters argument arguments function functions method methods
class classes module modules attribute attributes instance instances
one two three first second last next previous above below following""".split())
WORD = re.compile(r"[a-z][a-z0-9_]+")


def auto_phrases(text, limit=3):
    """content-word bi/trigrams from a signature fact's description half."""
    desc = text.split(" - ", 1)[1] if " - " in text else ""
    if not desc:
        return []
    words = [w for w in WORD.findall(desc.lower())]
    keep, out = [], []
    for w in words:
        if w in PHRASE_STOP or len(w) < 3:
            keep.append(None)              # break the n-gram window on stopwords
        else:
            keep.append(w)
    run = []
    for w in keep + [None]:
        if w is None:
            for n in (3, 2):
                for i in range(0, max(0, len(run) - n + 1)):
                    p = " ".join(run[i:i + n])
                    if len(p) >= 8:
                        out.append(p)
            run = []
        else:
            run.append(w)
    seen, uniq = set(), []
    for p in out:
        if p not in seen:
            seen.add(p)
            uniq.append(p)
    return uniq[:limit]


CTL_PUNCT = ".,()?!:;'-\n"

def norm_control(c):
    """Controls must be normalized EXACTLY like the template normalizes a user
    question (lowercase, punctuation -> spaces, padded both sides) or the cull
    silently misses: keywords are padded (" tell "), so an unpadded control
    line ("tell me about...") never matched a keyword at position 0. That let
    English-word API names (pyarrow.tell, xarray.depth) through the cull and
    into the gate, where they fired on plain-English questions (F-046)."""
    s = " " + c.lower() + " "
    for ch in CTL_PUNCT:
        s = s.replace(ch, " ")
    return s

def cull(kws, controls, report, fid):
    kept = []
    for k in kws:
        hit = next((c for c in controls if k in c), None)
        if hit is not None:
            report.append(f"CULLED  {fid}  '{k}'  (matches control: {hit[:50]!r})")
        else:
            kept.append(k)
    return kept

def main(argv):
    raw_path, out_path = argv[0], argv[1]
    controls, taskwords = [], {}
    if "--controls" in argv:
        p = argv[argv.index("--controls") + 1]
        controls = [norm_control(l.strip()) for l in open(p, encoding="utf-8") if l.strip()]
    if "--taskwords" in argv:
        p = argv[argv.index("--taskwords") + 1]
        taskwords = json.load(open(p, encoding="utf-8"))

    raw_bytes = open(raw_path, "rb").read()
    raw_sha = hashlib.sha256(raw_bytes).hexdigest()
    rows = [json.loads(l) for l in raw_bytes.decode("utf-8").splitlines() if l.strip()]

    # document frequency of strong keys across the whole bank: dead-name
    # candidates must be RARE (df <= 3) - a real dead name (melt, applymap,
    # float_) names one API; a generic token (dataframe, series) appears in
    # dozens of facts and would put weight 10 on all of them at once,
    # exploding the uncapped tie band (measured: 28 facts tied at 18).
    from collections import Counter
    df_count = Counter()
    pre = {}
    for r in rows:
        lib = derive_library(r)
        ks = set(strong_keywords(r, lib))
        pre[r["id"]] = (lib, ks)
        df_count.update(ks)

    report, out, unreviewed = [], [], 0
    for r in rows:
        lib = derive_library(r)
        if lib.startswith("UNREVIEWED:"):
            unreviewed += 1
        s = cull(strong_keywords(r, lib), controls, report, r["id"])
        # hand-written task phrases win; mined signature facts fall back to
        # phrases auto-derived from their own docstring summary (see above)
        phrases = taskwords.get(r["id"]) or auto_phrases(r["text"])
        w = cull(sorted({" " + p.lower() + " " for p in phrases if len(p) >= 5}),
                 controls, report, r["id"])
        ver = r.get("version") or "unversioned"
        txt = f'{r["text"]} [version: {ver}] [src: {r.get("source","?")}]'
        # d = dead-name keyword class (rank weight 10 in the template):
        # rename/removal facts' strong keys, MINUS the bare library name -
        # the lib name is in every fact's s, and letting it into d would
        # top-rank every such fact whenever the library is merely named.
        # Detection: kind=="mistake" (authored niche facts) OR dead-marker
        # words in the text (the research bank labels its rename facts
        # 'concept'/'signature', e.g. polars-003 melt->unpivot). The new
        # name rides along with the dead one (both are in s and we cannot
        # tell them apart) - acceptable: a hit on either should top-rank
        # the migration fact over a plain signature fact.
        deadish = r.get("kind") == "mistake" or any(
            m in r["text"].lower() for m in
            (" renamed", " removed", " deprecated", " no longer", " replaced"))
        d = [k for k in s if k.strip() != lib and df_count[k] <= 3] if deadish else []
        # RARITY TIERS (F-047). A strong key's weight must reflect how much it
        # narrows the bank. The library name is in EVERY fact of its tab, and
        # tokens like "stats"/"dataframe" are in hundreds - scoring them +4 made
        # 280 scipy facts tie at the top of an UNCAPPED tie band on "t-test with
        # scipy stats". Split: s = rare keys (df <= COMMON_DF, real evidence,
        # +4); c = common keys (+1). Both still count toward sc, so eligibility
        # and the lib-name floor pass are unchanged.
        # byte budget (F-048): keep the most DISCRIMINATIVE keys - rarest
        # first, then longest (a longer token is a more specific match).
        s_rare = sorted([k for k in s if df_count[k] <= COMMON_DF],
                        key=lambda k: (df_count[k], -len(k)))[:MAX_RARE]
        s_common = sorted([k for k in s if df_count[k] > COMMON_DF],
                          key=lambda k: (df_count[k], -len(k)))[:MAX_COMMON]
        out.append({"id": r["id"], "kind": r.get("kind", ""), "library": lib,
                    "s": s_rare, "c": s_common, "w": w, "d": d, "txt": txt})
        if not s and len(w) < 2:
            report.append(f"UNREACHABLE  {r['id']}  (no strong kw, <2 weak)")

    out.sort(key=lambda x: 0 if x["kind"] == "mistake" else 1)   # best facts win the cap slots
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(json.dumps({"_raw_sha": raw_sha, "_count": len(out)}) + "\n")
        for r in out:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    libs = sorted({r["library"] for r in out})
    print(f"{len(out)} facts | libraries: {', '.join(libs)}")
    print(f"unreviewed libraries: {unreviewed} (bake will refuse if >0)")
    for line in report:
        print(line)
    print("REVIEW the lines above, then bake.")

if __name__ == "__main__":
    main(sys.argv[1:])
