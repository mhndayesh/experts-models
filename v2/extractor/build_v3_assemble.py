#!/usr/bin/env python3
"""build_v3_assemble.py - merge deterministic (build_v3) + LLM (build_v3_llm) into the final faceted
concept->variant store: experts/appsec/facts/FINAL_v3.jsonl. Reuses verified content; restructures freely."""
import json, os
from collections import defaultdict, Counter
import build_v3 as B   # derive(), extract_cwe(), FACTS

HERE = os.path.dirname(os.path.abspath(__file__))
LLM = os.path.join(HERE, "experts", "appsec", "facts", "v3_llm.jsonl")
OUT = os.path.join(HERE, "experts", "appsec", "facts", "FINAL_v3.jsonl")

def uniq(*lists):
    seen, out = set(), []
    for L in lists:
        for x in (L or []):
            x = str(x).strip()
            if x and x.lower() not in seen: seen.add(x.lower()); out.append(x)
    return out

def main():
    enr = {}
    if os.path.exists(LLM):
        for l in open(LLM, encoding="utf-8"):
            o = json.loads(l); enr[o["id"]] = o
    variants, concepts = [], {}
    for f in B.FACTS:
        e = enr.get(f["id"], {})
        d = B.derive(f)
        cwe = (e.get("cwe") or "").strip() or B.extract_cwe(f)
        cid = cwe if (cwe and cwe.upper().startswith("CWE-")) else f"door:{f.get('door')}"
        lang = B.R2.norm_lang(e.get("language") or f.get("lang",""))
        concepts.setdefault(cid, {"kind":"concept","concept_id":cid,"cwe":[cwe] if cwe and cwe.startswith("CWE-") else [],
                                  "door":f.get("door"),"_truths":Counter(),"_subp":Counter(),"n":0})
        c = concepts[cid]; c["n"]+=1; c["_truths"][f.get("truth","")]+=1
        if e.get("sub_pattern"): c["_subp"][e["sub_pattern"]]+=1
        variants.append({
            "kind":"variant","id":f["id"],"concept_id":cid,
            "facets":{"language":lang,"package":d["package"],"namespace":d["namespace"],
                      "framework":(e.get("framework") or None),"sub_pattern":e.get("sub_pattern")},
            "retrieval":{
                "exact_symbols":uniq(d["exact_symbols"], e.get("exact_symbols")),
                "bad_pattern_symbols":uniq(d["bad_pattern_symbols"], e.get("bad_symbols")),
                "aliases":uniq(e.get("aliases")),
                "query_phrases":uniq(e.get("query_phrases")),
                "anchor_provenance":d["anchor_provenance"] if d["exact_symbols"] else ("llm_generated" if e.get("exact_symbols") else "none")},
            "claim":{"type":f.get("type"),"truth":f.get("truth","")},
            "examples":[x for x in [
                {"role":"bad","language":lang,"code":f.get("code_bad")} if f.get("code_bad") else None,
                {"role":"good","language":lang,"code":f.get("code_good")} if f.get("code_good") else None] if x],
            "evidence":{"source":f.get("source"),"source_edition":f.get("version"),"quote":f.get("quote"),"lib":f.get("lib")},
            "verification":{"audit_fix":bool(f.get("_audit_fix"))},
        })
    # finalize concept records (representative lesson + sub_patterns)
    for c in concepts.values():
        c["lesson"] = c["_truths"].most_common(1)[0][0] if c["_truths"] else ""
        c["sub_patterns"] = [s for s,_ in c["_subp"].most_common(12)]
        del c["_truths"]; del c["_subp"]
    with open(OUT, "w", encoding="utf-8") as fh:
        for c in concepts.values(): fh.write(json.dumps(c, ensure_ascii=False)+"\n")
        for v in variants: fh.write(json.dumps(v, ensure_ascii=False)+"\n")
    cwe_c = sum(1 for cid in concepts if cid.startswith("CWE-"))
    wexact = sum(1 for v in variants if v["retrieval"]["exact_symbols"])
    wphr = sum(1 for v in variants if v["retrieval"]["query_phrases"])
    print(f"wrote {len(variants)} variants + {len(concepts)} concepts ({cwe_c} CWE, {len(concepts)-cwe_c} door) -> {OUT}")
    print(f"  exact_symbols: {wexact}/{len(variants)} ({100*wexact//len(variants)}%) | query_phrases: {wphr}/{len(variants)} ({100*wphr//len(variants)}%)")
    sizes=sorted((c["n"] for c in concepts.values()),reverse=True)
    print(f"  concept sizes: max {sizes[0]}, median {sizes[len(sizes)//2]}, singletons {sum(1 for s in sizes if s==1)}")

if __name__ == "__main__":
    main()
