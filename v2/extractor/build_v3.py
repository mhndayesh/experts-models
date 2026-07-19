#!/usr/bin/env python3
"""build_v3.py - rebuild the bank as faceted CONCEPT -> VARIANT (schema v3, see decisions/SCHEMA-V3.md).
Reuses the verified content of the current bank as raw material; restructures freely (owner: ok to waste it).

PASS 1 (this file, DETERMINISTIC, no LLM): concept backbone from CWE + code-derived facets/anchors.
PASS 2 (build_v3_llm.py): sub_pattern / framework / aliases / query_phrases + concept labels for non-CWE facts.
"""
import json, os, re
from collections import defaultdict, Counter
import retriever2 as R2   # norm_lang, terms_from, is_symbol

HERE = os.path.dirname(os.path.abspath(__file__))
SRC  = os.path.join(HERE, "experts", "appsec", "facts", "FINAL.jsonl")
FACTS = [json.loads(l) for l in open(SRC, encoding="utf-8")]

CWE_RE = re.compile(r"cwe[-\s]?0*(\d+)", re.I)
def extract_cwe(f):
    """concept backbone = CWE. From lib (cwe-089), else scanned from subject/truth/why."""
    for src in (f.get("lib",""), f.get("subject",""), f.get("truth",""), f.get("why_it_bites","")):
        m = CWE_RE.search(src or "")
        if m: return f"CWE-{int(m.group(1))}"
    return None

IDENT = re.compile(r"[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)+|[A-Za-z_][A-Za-z0-9_]{2,}")
def idents(text):
    """API-ish identifiers: dotted (torch.load) or snake/camel words. Skip bare short/common words."""
    out = []
    for m in IDENT.findall(text or ""):
        if "." in m or "_" in m or any(c.isupper() for c in m[1:]) or len(m) > 6:
            out.append(m)
    return out

IMPORT_RE = re.compile(r"^\s*(?:import|from)\s+([A-Za-z0-9_.]+)", re.M)
def code_package(code):
    m = IMPORT_RE.findall(code or "")
    return m[0].split(".")[0] if m else None

def derive(f):
    kw = f.get("keywords", {})
    ff = kw.get("from_fact", [])
    cb, cg = f.get("code_bad") or "", f.get("code_good") or ""
    # exact symbols (secure/aware side) vs bad-pattern symbols
    exact = []
    for s in ff + idents(cg):
        s = s.strip()
        if s and s not in exact and ("." in s or "_" in s or any(c.isupper() for c in s[1:])):
            exact.append(s)
    bad = [s for s in idents(cb) if s not in exact]
    # namespace = the primary dotted API; package = its root or the import
    dotted = [s for s in exact if "." in s]
    namespace = dotted[0] if dotted else (exact[0] if exact else None)
    pkg = code_package(cb) or code_package(cg) or (namespace.split(".")[0] if namespace and "." in namespace else None)
    prov = "code_derived" if (cb or cg) else ("keyword_derived" if ff else "none")
    return {
        "language": R2.norm_lang(f.get("lang","")),
        "package": pkg,
        "namespace": namespace,
        "exact_symbols": exact[:12],
        "bad_pattern_symbols": bad[:8],
        "anchor_provenance": prov,
    }

def main():
    variants, concepts = [], {}
    for f in FACTS:
        cwe = extract_cwe(f)
        door = f.get("door", "?")
        cid = cwe or f"door:{door}"          # fallback concept for facts with no CWE
        concepts.setdefault(cid, {"kind":"concept","concept_id":cid,"cwe":[cwe] if cwe else [],
                                  "door":door,"labels":Counter(),"n":0})
        concepts[cid]["n"] += 1
        concepts[cid]["labels"][f.get("subject","")[:40]] += 1
        d = derive(f)
        variants.append({
            "kind":"variant","id":f["id"],"concept_id":cid,
            "facets":{k:d[k] for k in ("language","package","namespace")},
            "retrieval":{"exact_symbols":d["exact_symbols"],"bad_pattern_symbols":d["bad_pattern_symbols"],
                         "aliases":[],"query_phrases":[],"anchor_provenance":d["anchor_provenance"]},
            "claim":{"type":f.get("type"),"truth":f.get("truth","")},
            "examples":[e for e in [
                {"role":"bad","language":d["language"],"code":f.get("code_bad")} if f.get("code_bad") else None,
                {"role":"good","language":d["language"],"code":f.get("code_good")} if f.get("code_good") else None] if e],
            "evidence":{"source":f.get("source"),"source_edition":f.get("version"),"quote":f.get("quote"),"lib":f.get("lib")},
            "verification":{"audit_fix":bool(f.get("_audit_fix"))},
        })
    # report concept distribution
    print(f"variants: {len(variants)}  |  concepts: {len(concepts)}  (CWE: {sum(1 for c in concepts if not c.startswith('door:'))}, door-fallback: {sum(1 for c in concepts if c.startswith('door:'))})")
    sizes = sorted((c["n"] for c in concepts.values()), reverse=True)
    print(f"concept sizes: max {sizes[0]}, median {sizes[len(sizes)//2]}, singletons {sum(1 for s in sizes if s==1)}")
    print("biggest concepts (look-alike groups collapsed):")
    for cid, c in sorted(concepts.items(), key=lambda kv:-kv[1]['n'])[:12]:
        top = c["labels"].most_common(1)[0][0]
        print(f"   {c['n']:4d}  {cid:14s} {c['door']:20s} e.g. {top}")
    # anchor coverage
    wexact = sum(1 for v in variants if v["retrieval"]["exact_symbols"])
    print(f"\nvariants with >=1 code/keyword-derived exact_symbol: {wexact}/{len(variants)} "
          f"({100*wexact//len(variants)}%)  -- LLM pass fills the rest + aliases/phrases/sub_pattern")
    out = os.path.join(HERE, "experts", "appsec", "facts", "v3_pass1.jsonl")
    with open(out, "w", encoding="utf-8") as fh:
        for c in concepts.values():
            c = dict(c); c["labels"] = None; fh.write(json.dumps(c, ensure_ascii=False)+"\n")
        for v in variants: fh.write(json.dumps(v, ensure_ascii=False)+"\n")
    print("wrote", out)

if __name__ == "__main__":
    main()
