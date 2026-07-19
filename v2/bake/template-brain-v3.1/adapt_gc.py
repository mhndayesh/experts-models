#!/usr/bin/env python3
"""adapt_gc.py - map the GitChameleon expert bank into the bake_index.py schema.

Produces:
  gitchameleon_bank.jsonl   {id, text, source, version, kind, meta{library,symbol,...}}
  gitchameleon_taskwords.json  {id: [search phrases]}  <- from_fact + associative keywords

`text` is the clean injected fact the model sees; the searchable phrases go to taskwords
(the designed index slot) so they don't pollute what the model reads.
"""
import json, os, glob, re

FD = "c:/projects/LLM BANK/v2/extractor/experts/gitchameleon/facts"
OUT_BANK = "gitchameleon_bank.jsonl"
OUT_TASK = "gitchameleon_taskwords.json"

def primary_symbol(ff):
    # the most specific from_fact symbol (dotted / call-like), else the longest
    syms = [k for k in ff if re.search(r"[.(]", k)]
    return (syms or sorted(ff, key=len, reverse=True) or [""])[0]

bank, task = [], {}
for fn in sorted(glob.glob(FD + "/*.jsonl")):
    for l in open(fn, encoding="utf-8"):
        l = l.strip()
        if not l: continue
        r = json.loads(l)
        lib = r["lib"]; kw = r.get("keywords", {})
        ff = kw.get("from_fact", []); asso = kw.get("associative", [])
        truth = r.get("truth", "").strip()
        sym = primary_symbol(ff)
        # self-contained injected text: ensure the API symbol is present
        text = truth if (not sym or sym.split(".")[-1].lower() in truth.lower()) else f"{sym}: {truth}"
        bank.append({
            "id": r["id"],
            "text": text,
            "source": lib,
            "version": r.get("version") or "multi",
            "kind": "landmine",
            "meta": {"library": lib, "symbol": sym, "type": r.get("type"),
                     "why_it_bites": r.get("why_it_bites")},
        })
        # searchable phrases: symbols + associative task phrases (dedup, non-empty)
        phrases = []
        for p in ff + asso:
            p = str(p).strip()
            if p and p not in phrases: phrases.append(p)
        if phrases: task[r["id"]] = phrases

with open(OUT_BANK, "w", encoding="utf-8") as fh:
    for b in bank: fh.write(json.dumps(b, ensure_ascii=False) + "\n")
json.dump(task, open(OUT_TASK, "w", encoding="utf-8"), ensure_ascii=False)
print(f"wrote {len(bank)} facts -> {OUT_BANK}; taskwords for {len(task)} -> {OUT_TASK}")
