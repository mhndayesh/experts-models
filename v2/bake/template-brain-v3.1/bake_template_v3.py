#!/usr/bin/env python3
"""bake_template_v3.py - splice the factbank inserts into a family base
template and (optionally) write the baked GGUF via the project's writer.

Runnable TODAY without the repo:
  python bake_template_v3.py --base test_family/base.jinja \
      --enriched bank_enriched.jsonl --raw smoke_facts.jsonl \
      --family reference --out baked_template.jinja
GGUF write (--src-gguf/--dst-gguf) stays a wired step: see write_baked().
"""
import json, hashlib, argparse, os, sys

ANCHORS = ["{#FB_PRELOOP#}", "{#FB_SYS#}", "{#FB_USER#}", "{#FB_HOOK#}", "{#FB_TOOLMSG#}"]
# v3.2: FB_GEN is OPTIONAL (per family) - placed in the generation-prompt
# block, it delivers matched facts as a FORGED native tool exchange on
# plain no-tools requests (default-native lane). Bases without it bake
# exactly as before.
OPT_ANCHORS = ["{#FB_GEN#}"]
INSERT_FILES = {"{#FB_PRELOOP#}": "fb_preloop.jinja", "{#FB_SYS#}": "fb_sys.jinja",
                "{#FB_USER#}": "fb_user.jinja", "{#FB_HOOK#}": "fb_hook.jinja",
                "{#FB_TOOLMSG#}": "fb_toolmsg.jinja", "{#FB_GEN#}": "fb_gen.jinja"}
MAX_TEMPLATE_FACTS = 500   # template-lane honesty cap (scope: pouch+loop owns 10k-100k)
MACRO_PATCH = ("{%- macro format_type_argument(type_arg) -%}"
               "{{- type_arg if type_arg is string else format_argument(type_arg) -}}"
               "{%- endmacro -%}\n")

def sha(s): return hashlib.sha256(s.encode("utf-8")).hexdigest()

def load_inserts(family, anchors):
    d = os.path.join("inserts", family)
    if not os.path.isdir(d):
        d = os.path.join("inserts", "reference")
    return {a: open(os.path.join(d, INSERT_FILES[a]), encoding="utf-8").read()
            for a in anchors}, open(os.path.join(d, "top.jinja"), encoding="utf-8").read()

def check_base_is_source_plus_anchors(base, source_tpl):
    """Point 20: base with the anchors stripped must equal the source
    template exactly. Family adaptation lives in inserts/<family>/,
    never in the base itself."""
    stripped = base
    for a in ANCHORS + OPT_ANCHORS:
        stripped = stripped.replace(a, "", 1)
    if sha(stripped) != sha(source_tpl):
        sys.exit("[base guard] family base != source template + anchors. "
                 "Re-anchor against the CURRENT source template; put any "
                 "variable-name adaptation into inserts/<family>/ instead.")

def splice(base, inserts, top, gate_jinja, bank_jinja, menu, source_tpl):
    for a in ANCHORS:
        n = base.count(a)
        assert n == 1, f"anchor {a} found {n} times (need exactly 1)"
    opt_present = [a for a in OPT_ANCHORS if a in base]
    for a in opt_present:
        assert base.count(a) == 1, f"optional anchor {a} found more than once"
    out = base
    out = out.replace("{#FB_PRELOOP#}", inserts["{#FB_PRELOOP#}"]
                      .replace("__GATE__", gate_jinja).replace("__BANK__", bank_jinja))
    out = out.replace("{#FB_SYS#}", inserts["{#FB_SYS#}"].replace("__MENU__", menu))
    for a in ("{#FB_USER#}", "{#FB_HOOK#}", "{#FB_TOOLMSG#}"):
        out = out.replace(a, inserts[a])
    for a in opt_present:
        out = out.replace(a, inserts[a])
    for a in ANCHORS + opt_present:
        assert a not in out, f"anchor {a} not consumed"
    patch = "" if "macro format_type_argument" in source_tpl else MACRO_PATCH
    return patch + top + out          # point 18: top.jinja actually loaded

def pad(k): return " " + k.strip() + " "

# extra gate triggers per library: the name people SAY vs the import name.
# k2 turns punctuation into spaces, so "scikit-learn" in a question arrives as
# "scikit learn" - aliases are written post-normalization.
GATE_ALIASES = {
    # NB: the template's k2 does NOT normalize hyphens (only . , ( ) ? ! : ; '
    # and newline), so a hyphenated alias must be written WITH the hyphen.
    "sklearn": ["scikit-learn", "scikit learn", "scikitlearn"],
    "matplotlib": ["pyplot", "plt "],
    "statsmodels": ["stats model"],
    "pyarrow": ["arrow table"],
}

def build_gate(rows, gate_n):
    """Group facts by library; per group pick gate triggers: the library
    name + up to gate_n strong keywords UNIQUE to that group, mistake-kind
    facts' keywords first. Returns (gate, flat bank, shadowed fact ids)."""
    from collections import Counter, defaultdict
    df = Counter(k for r in rows for k in set(r["s"]))
    groups = defaultdict(list)
    for r in rows:
        groups[r["library"]].append(r)
    gate, bank, shadowed = [], [], []
    for lib in sorted(groups):
        facts = groups[lib]
        cand = []
        for r in facts:                       # mistakes first, then rest
            for k in list(r["s"]) + list(r.get("c", [])):
                if df[k] == sum(1 for x in facts if k in x["s"]):  # unique to group
                    cand.append((0 if r["kind"] == "mistake" else 1, len(k), k))
        seen, trig = set(), [pad(lib)]
        for _, _, k in sorted(cand):
            if k not in seen and len(trig) < gate_n + 1:
                seen.add(k); trig.append(k)   # keywords are pre-padded by enrich
        for al in GATE_ALIASES.get(lib, []):
            trig.append(pad(al))
        gate.append({"lib": pad(lib), "trig": trig})
        # v3.4.0 GROUPED BANK: facts are nested under their library instead of
        # one flat list. The scan's outer loop then skips a whole unmatched
        # library with ONE check (`g.lib in fbns.libs`) instead of testing
        # every one of its facts. Cost per request goes from O(total bank) to
        # O(matched libraries' facts) - the change that makes 10k-50k banks
        # affordable (at 24k facts the flat scan walked 120k fact-slots per
        # request across the 5 ranked passes; grouped, a pandas question walks
        # ~1.6k).
        gf = []
        for r in facts:
            gf.append({"s": r["s"], "c": r.get("c", []), "w": r["w"],
                       "d": r.get("d", []), "txt": r["txt"]})
            if not ((set(r["s"]) | set(r.get("c", []))) & set(trig)):
                shadowed.append(r["id"] + f"(via '{lib}' only)")
        bank.append({"lib": pad(lib), "f": gf})
    return gate, bank, shadowed

def load_enriched(path, raw_path, cap=MAX_TEMPLATE_FACTS):
    lines = open(path, encoding="utf-8").read().splitlines()
    header = json.loads(lines[0])
    raw_sha = hashlib.sha256(open(raw_path, "rb").read()).hexdigest()
    if header.get("_raw_sha") != raw_sha:
        sys.exit("[19 guard] enriched bank was built from a DIFFERENT raw "
                 "bank than --raw. Re-run enrich.py on the current raw file.")
    rows = [json.loads(l) for l in lines[1:] if l.strip()]
    bad = [r["id"] for r in rows if r["library"].startswith("UNREVIEWED:")]
    if bad:
        sys.exit(f"[6 guard] unreviewed libraries on facts {bad}; fix meta/"
                 f"HOSTMAP and re-enrich before baking.")
    if len(rows) > cap:
        sys.exit(f"{len(rows)} facts > template-lane cap {cap}. "
                 f"This lane is the demo tier; 10k-100k belongs to pouch+loop.")
    return rows

def write_baked(src_gguf, dst_gguf, template, bank_text, version="0.3.0"):
    """A6: wired 2026-07-13 to the same proven write path as
    package/factbank/bake.py bake() (lines 94-126): GGUFReader -> GGUFWriter
    -> gguf.scripts.gguf_new_metadata.copy_with_new_metadata, tensors copied
    untouched, arch/endianess/alignment preserved. Deliberately NOT the
    repo's bake() itself: that function performs its own template surgery
    (think-off + all-facts block, the F-040 demo) which must not touch the
    already-spliced template written here. Adds the factbank pouch keys the
    repo writer lacks."""
    try:
        import gguf
        from gguf.scripts.gguf_new_metadata import (MetadataDetails,
                                                    copy_with_new_metadata)
    except ImportError:
        raise SystemExit("write_baked needs the gguf package: pip install gguf")
    reader = gguf.GGUFReader(src_gguf, "r")
    arch = reader.get_field(gguf.Keys.General.ARCHITECTURE).contents()
    writer = gguf.GGUFWriter(dst_gguf, arch=arch, endianess=reader.endianess)
    align = reader.get_field(gguf.Keys.General.ALIGNMENT)
    if align is not None:
        writer.data_alignment = align.contents()
    new_md = {
        gguf.Keys.Tokenizer.CHAT_TEMPLATE:
            MetadataDetails(gguf.GGUFValueType.STRING, template),
        "factbank.bank":
            MetadataDetails(gguf.GGUFValueType.STRING, bank_text),
        "factbank.version":
            MetadataDetails(gguf.GGUFValueType.STRING, version),
    }
    copy_with_new_metadata(reader, writer, new_md, [])
    return {"template_chars": len(template), "bank_chars": len(bank_text),
            "out_bytes": os.path.getsize(dst_gguf)}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True, help="family base (source template + 5 anchors)")
    ap.add_argument("--source-template", help="the unmodified source template for the base guard; "
                    "default: extracted from --src-gguf; test mode: --base with anchors stripped is trusted")
    ap.add_argument("--enriched", required=True)
    ap.add_argument("--raw", required=True)
    ap.add_argument("--family", default="reference")
    ap.add_argument("--out", default="baked_template.jinja")
    ap.add_argument("--src-gguf"); ap.add_argument("--dst-gguf")
    ap.add_argument("--cap", type=int, default=MAX_TEMPLATE_FACTS,
                    help="template-lane fact cap; raise ONLY per bench.py results")
    ap.add_argument("--gate-n", type=int, default=8,
                    help="gate triggers per library beyond the name")
    a = ap.parse_args()

    base = open(a.base, encoding="utf-8").read()
    if a.source_template:
        source_tpl = open(a.source_template, encoding="utf-8").read()
    elif a.src_gguf:
        from gguf import GGUFReader
        r = GGUFReader(a.src_gguf); f = r.fields["tokenizer.chat_template"]
        source_tpl = bytes(f.parts[f.data[0]]).decode("utf-8")
    else:
        source_tpl = base
        for an in ANCHORS: source_tpl = source_tpl.replace(an, "", 1)
        print("[warn] no --source-template/--src-gguf: base guard is self-referential (test mode)")
    check_base_is_source_plus_anchors(base, source_tpl)

    rows = load_enriched(a.enriched, a.raw, a.cap)
    gate, bank, shadowed = build_gate(rows, a.gate_n)
    gate_jinja = json.dumps(gate, ensure_ascii=False)
    bank_jinja = json.dumps(bank, ensure_ascii=False)
    menu = ", ".join(sorted({r["library"] for r in rows}))
    if shadowed:
        print(f"GATE-SHADOWED ({len(shadowed)}): reachable only when the "
              f"library is named: {', '.join(shadowed)}")
    needed = ANCHORS + [x for x in OPT_ANCHORS if x in base]
    inserts, top = load_inserts(a.family, needed)
    tpl = splice(base, inserts, top, gate_jinja, bank_jinja, menu, source_tpl)
    open(a.out, "w", encoding="utf-8").write(tpl)
    print(f"template written: {a.out} ({len(rows)} facts, menu: {menu})")

    if a.src_gguf and a.dst_gguf:
        write_baked(a.src_gguf, a.dst_gguf, tpl, open(a.raw, encoding="utf-8").read())
        print("baked:", a.dst_gguf)
    else:
        print("template-only mode (no GGUF written). Paste into LM Studio "
              "override for testing, or supply --src-gguf/--dst-gguf once "
              "write_baked() is wired.")

if __name__ == "__main__":
    main()
