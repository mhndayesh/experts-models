#!/usr/bin/env python3
"""adapt_expert.py - generic version of adapt_secnet.py / adapt_gc.py.

Maps ANY expert's facts/*.jsonl into the bake_index.py schema, so we don't need a
per-expert adapter copy. Same transform as adapt_secnet.py, parameterized.

usage:
  python adapt_expert.py <facts_dir> <out_prefix>
  e.g. python adapt_expert.py "c:/projects/LLM BANK/v2/extractor/experts/offensive-security-re/facts" offsec
       -> offsec_bank.jsonl + offsec_taskwords.json
"""
import json, glob, os, re, sys

if len(sys.argv) < 3:
    sys.exit("usage: python adapt_expert.py <facts_dir> <out_prefix>")
FD = sys.argv[1].rstrip("/")
PREFIX = sys.argv[2]
OUT_BANK = f"{PREFIX}_bank.jsonl"
OUT_TASK = f"{PREFIX}_taskwords.json"

def primary_symbol(ff):
    syms = [k for k in ff if re.search(r"[.(]", k)]
    return (syms or sorted(ff, key=len, reverse=True) or [""])[0]

# --- release selection (audit #4/#5): NEVER infer production facts from a bare glob ---
# 1) explicit manifest.json wins; 2) else the merged FINAL.jsonl if present; 3) else glob MINUS
#    rejects/removed/anchored/review intermediates. A glob that swept in reject/removed/source-bank
#    files baked ~92 rejected facts into the GGUF (unique ids escape the `seen` de-dup).
EXCLUDE = (".review.jsonl", ".rejects.jsonl", ".removed.jsonl", "_anchored.jsonl")
manifest = os.path.join(FD, "manifest.json")
if os.path.exists(manifest):
    files = [os.path.join(FD, f) for f in json.load(open(manifest, encoding="utf-8"))["release"]]
elif os.path.exists(os.path.join(FD, "FINAL.jsonl")):
    files = [os.path.join(FD, "FINAL.jsonl")]                     # merged canonical bank only
else:
    files = [f for f in sorted(glob.glob(FD + "/*.jsonl")) if not f.endswith(EXCLUDE)]
print(f"baking from: {[os.path.basename(f) for f in files]}")

bank, task, seen = [], {}, set()
for fn in files:
    for l in open(fn, encoding="utf-8"):
        l = l.strip()
        if not l: continue
        r = json.loads(l)
        if r["id"] in seen:            # cross-file id safety
            continue
        seen.add(r["id"])
        lib = r["lib"]; kw = r.get("keywords", {})
        ff = kw.get("from_fact", []); asso = kw.get("associative", [])
        truth = r.get("truth", "").strip()
        sym = primary_symbol(ff)
        text = truth if (not sym or sym.split(".")[-1].lower() in truth.lower()) else f"{sym}: {truth}"
        # preserve the RICH fields (audit #1/#5): code pairs, retrieval anchors, door, language.
        bank.append({
            "id": r["id"],
            "text": text,
            "source": lib,
            "version": r.get("version") or "multi",
            "kind": "landmine",
            "door": r.get("door"),
            "lang": r.get("lang"),
            "anchors": r.get("anchors") or [],
            "meta": {"library": lib, "symbol": sym, "type": r.get("type"),
                     "why_it_bites": r.get("why_it_bites"),
                     "code_good": r.get("code_good"), "code_bad": r.get("code_bad")},
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
print(f"{len(libs)} libraries:", ", ".join(libs))
