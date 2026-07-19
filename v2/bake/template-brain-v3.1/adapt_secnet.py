#!/usr/bin/env python3
"""adapt_secnet.py - map the Security & Networking expert bank into the bake_index.py schema.

Same transform as adapt_gc.py, pointed at the security-networking facts. Produces:
  secnet_bank.jsonl        {id, text, source, version, kind, meta{library,symbol,...}}
  secnet_taskwords.json    {id: [search phrases]}  <- from_fact + associative keywords
"""
import json, glob, re

FD = "c:/projects/LLM BANK/v2/extractor/experts/security-networking/facts"
OUT_BANK = "secnet_bank.jsonl"
OUT_TASK = "secnet_taskwords.json"

def primary_symbol(ff):
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
        phrases = []
        for p in ff + asso:
            p = str(p).strip()
            if p and p not in phrases: phrases.append(p)
        if phrases: task[r["id"]] = phrases

with open(OUT_BANK, "w", encoding="utf-8") as fh:
    for b in bank: fh.write(json.dumps(b, ensure_ascii=False) + "\n")
json.dump(task, open(OUT_TASK, "w", encoding="utf-8"), ensure_ascii=False)
print(f"wrote {len(bank)} facts -> {OUT_BANK}; taskwords for {len(task)} -> {OUT_TASK}")
libs = sorted({b['source'] for b in bank})
print("libraries:", ", ".join(libs))
