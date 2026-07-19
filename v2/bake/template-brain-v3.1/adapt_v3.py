#!/usr/bin/env python3
"""adapt_v3.py - convert the FACETED v3 store (FINAL_v3.jsonl: concept->variant) into bake_index inputs.
The rich retrieval fields (exact_symbols, feature_phrases/use_cases, query_phrases, aliases, bad_symbols)
become the TASKWORDS - that is the retrieval surface the index is built over. Also emits per-fact language
and concept sidecars for the v3 template's language filter + concept routing (no library gate).

usage: python adapt_v3.py <FINAL_v3.jsonl> <out_prefix>
  -> <prefix>_bank.jsonl  <prefix>_taskwords.json  <prefix>_lang.json  <prefix>_concept.json
"""
import json, sys, os
from collections import Counter

if len(sys.argv) < 3: sys.exit("usage: adapt_v3.py <FINAL_v3.jsonl> <out_prefix>")
SRC, PREFIX = sys.argv[1], sys.argv[2]
rows = [json.loads(l) for l in open(SRC, encoding="utf-8") if l.strip()]
variants = [r for r in rows if r.get("kind") == "variant"]

bank, task, lang, concept = [], {}, {}, {}
for v in variants:
    r = v["retrieval"]; f = v["facets"]
    # the injected text = the truth (+ a leading symbol so the display carries the API)
    sym = (r.get("exact_symbols") or [""])[0]
    truth = v["claim"].get("truth", "").strip()
    text = truth if (not sym or sym.split(".")[-1].lower() in truth.lower()) else f"{sym}: {truth}"
    bank.append({
        "id": v["id"], "text": text,
        "source": f.get("package") or v["concept_id"],
        "version": v.get("evidence", {}).get("source_edition") or "multi",
        "kind": "landmine",
    })
    # RETRIEVAL SURFACE: everything a benign prompt might match (feature_phrases = the big lever)
    terms = []
    for fld in ("exact_symbols", "feature_phrases", "query_phrases", "aliases", "bad_pattern_symbols"):
        terms += [str(x) for x in (r.get(fld) or [])]
    if terms: task[v["id"]] = terms
    lang[v["id"]] = (f.get("language") or "")
    concept[v["id"]] = v["concept_id"]

json.dump(task, open(f"{PREFIX}_taskwords.json", "w", encoding="utf-8"), ensure_ascii=False)
json.dump(lang, open(f"{PREFIX}_lang.json", "w", encoding="utf-8"), ensure_ascii=False)
json.dump(concept, open(f"{PREFIX}_concept.json", "w", encoding="utf-8"), ensure_ascii=False)
with open(f"{PREFIX}_bank.jsonl", "w", encoding="utf-8") as fh:
    for b in bank: fh.write(json.dumps(b, ensure_ascii=False) + "\n")
print(f"wrote {len(bank)} variants -> {PREFIX}_bank.jsonl")
print(f"  taskwords for {len(task)} | langs {dict(Counter(lang.values()).most_common(6))} | concepts {len(set(concept.values()))}")
