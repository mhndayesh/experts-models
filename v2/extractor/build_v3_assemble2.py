#!/usr/bin/env python3
"""build_v3_assemble2.py - the FULL faceted merge (the step build_v3_tier1.py refers to as
"build_v3_assemble2"). Folds ALL enrichment into the shipped concept->variant store
experts/appsec/facts/FINAL_v3.jsonl:
  - build_v3        (derive: package/namespace/typed anchors) + FINAL.jsonl base facts
  - build_v3_llm    (v3_llm.jsonl:   cwe, framework, sub_pattern, symbols, aliases, query_phrases)
  - build_v3_tier1  (v3_tier1.jsonl: feature_phrases, library_trigger, disambiguator, canonical_cwe)
  - build_v3_usecases (v3_usecases.jsonl: use_cases -> folded into feature_phrases, use_cases first)

build_v3_assemble.py is the earlier PARTIAL version (v3_llm only; no feature_phrases/library_trigger/
disambiguator) - superseded by this file. Concept records are the minimal {kind, concept_id, n} stubs.

usage: python build_v3_assemble2.py [out_path]   (default: experts/appsec/facts/FINAL_v3.jsonl)
"""
import json, os, sys
import build_v3 as B   # derive(), extract_cwe(), FACTS, R2

HERE = os.path.dirname(os.path.abspath(__file__))
def P(name): return os.path.join(HERE, "experts", "appsec", "facts", name)
OUT = sys.argv[1] if len(sys.argv) > 1 else P("FINAL_v3.jsonl")

def load(name):
    d = {}
    if os.path.exists(P(name)):
        for l in open(P(name), encoding="utf-8"):
            if l.strip():
                o = json.loads(l); d[o["id"]] = o
    return d

def uniq(*lists):
    seen, out = set(), []
    for L in lists:
        for x in (L or []):
            x = str(x).strip()
            if x and x.lower() not in seen: seen.add(x.lower()); out.append(x)
    return out

def uniq_cs(*lists):   # case-SENSITIVE dedup (feature_phrases keep near-dup casing, verified vs FINAL_v3)
    seen, out = set(), []
    for L in lists:
        for x in (L or []):
            x = str(x).strip()
            if x and x not in seen: seen.add(x); out.append(x)
    return out

def cwe_ok(x): return bool(x) and str(x).upper().startswith("CWE-")

def concept_id(f, e, a):
    # precedence: canonical CWE (tier1) > llm cwe > extracted cwe > door fallback.
    # (usecases.canonical_cwe is intentionally NOT consulted - it disagrees with the shipped
    #  bank on the door-fallback facts; verified against FINAL_v3.jsonl.)
    for c in ((a.get("canonical_cwe") or "").strip(),
              (e.get("cwe") or "").strip(),
              (B.extract_cwe(f) or "").strip()):
        if cwe_ok(c): return c
    return f"door:{f.get('door')}"

def main():
    llm = load("v3_llm.jsonl"); t1 = load("v3_tier1.jsonl"); uc = load("v3_usecases.jsonl")
    variants, concepts = [], {}
    for f in B.FACTS:
        fid = f["id"]
        e = llm.get(fid, {}); a = t1.get(fid, {}); u = uc.get(fid, {})
        d = B.derive(f)
        cid = concept_id(f, e, a)
        lang = B.R2.norm_lang(e.get("language") or f.get("lang", ""))
        concepts.setdefault(cid, {"kind": "concept", "concept_id": cid, "n": 0})["n"] += 1
        facets = {"language": lang, "package": d["package"], "namespace": d["namespace"],
                  "framework": (e.get("framework") or None), "sub_pattern": e.get("sub_pattern")}
        if a.get("disambiguator"): facets["disambiguator"] = a["disambiguator"]
        retrieval = {
            "exact_symbols": uniq(d["exact_symbols"], e.get("exact_symbols")),
            "bad_pattern_symbols": uniq(d["bad_pattern_symbols"], e.get("bad_symbols")),
            "aliases": uniq(e.get("aliases")),
            "query_phrases": uniq(e.get("query_phrases")),
            "anchor_provenance": d["anchor_provenance"] if d["exact_symbols"] else ("llm_generated" if e.get("exact_symbols") else "none")}
        fp = uniq_cs(u.get("use_cases"), a.get("feature_phrases"))   # use_cases first, then tier1's new ones
        if fp: retrieval["feature_phrases"] = fp
        lt = a.get("library_trigger") or []                          # tier1's list raw (no dedup, verified)
        if lt: retrieval["library_trigger"] = lt
        variants.append({
            "kind": "variant", "id": fid, "concept_id": cid,
            "facets": facets, "retrieval": retrieval,
            "claim": {"type": f.get("type"), "truth": f.get("truth", "")},
            "examples": [x for x in [
                {"role": "bad", "language": lang, "code": f.get("code_bad")} if f.get("code_bad") else None,
                {"role": "good", "language": lang, "code": f.get("code_good")} if f.get("code_good") else None] if x],
            "evidence": {"source": f.get("source"), "source_edition": f.get("version"), "quote": f.get("quote"), "lib": f.get("lib")},
            "verification": {"audit_fix": bool(f.get("_audit_fix"))},
        })
    with open(OUT, "w", encoding="utf-8") as fh:
        for c in concepts.values(): fh.write(json.dumps(c, ensure_ascii=False) + "\n")
        for v in variants: fh.write(json.dumps(v, ensure_ascii=False) + "\n")
    cwe_c = sum(1 for cid in concepts if cid.startswith("CWE-"))
    print(f"wrote {len(concepts)} concepts ({cwe_c} CWE, {len(concepts)-cwe_c} door) + {len(variants)} variants -> {OUT}")

if __name__ == "__main__":
    main()
