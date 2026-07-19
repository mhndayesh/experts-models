#!/usr/bin/env python3
"""experts_to_package.py - the ONE generic adapter: expert banks -> package schema.

Reads every `experts/*/facts/*.jsonl` (the canonical rich lab schema) and writes a
single package-schema JSONL (`{id,text,source,version,kind,meta}`) that the
`factbank` package loads directly. This replaces the ad-hoc, bake-only adapters
(adapt_gc.py / adapt_secnet.py) as the documented expert->package path.

  python experts_to_package.py [--out ../package/factbank/facts_v2.jsonl] [--expert web]

The mapping is Fact.from_row() in the package, so there is exactly ONE source of
truth for the schema translation (see v2/extractor/SCHEMA.md).
"""
import json, glob, os, sys, argparse
from dataclasses import asdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "package"))
from factbank.bank import Fact   # single source of truth for the mapping

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(HERE, "..", "package", "factbank", "facts_v2.jsonl"))
    ap.add_argument("--expert", default="*", help="one expert folder name, or * for all")
    a = ap.parse_args()
    files = sorted(glob.glob(os.path.join(HERE, "experts", a.expert, "facts", "*.jsonl")))
    seen, rows = set(), []
    for f in files:
        for l in open(f, encoding="utf-8"):
            l = l.strip()
            if not l: continue
            fact = Fact.from_row(json.loads(l))
            if fact.id in seen:            # cross-department bank duplication guard
                continue
            seen.add(fact.id)
            rows.append({"id": fact.id, "text": fact.text, "source": fact.source,
                         "version": fact.version, "kind": fact.kind, "meta": fact.meta})
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    with open(a.out, "w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"wrote {len(rows)} package-schema facts from {len(files)} banks -> {a.out}")

if __name__ == "__main__":
    main()
