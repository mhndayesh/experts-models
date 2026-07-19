#!/usr/bin/env python3
"""build_pool.py - assemble a fact pool for select_facts.py.

A pool = the CURATED facts (the ones that beat a wrong prior - never cut) plus
the mined signature facts for one domain (api_facts/<domain>__*.jsonl, 46,834
facts across 4 domains). The old monolithic pool files (facts_pydata_deep.jsonl
and friends) were archived on 2026-07-14; this rebuilds an equivalent in seconds.

Domains available in api_facts/: data, web, ai, stdlib.

usage:
  python build_pool.py --domain data --out _pool.jsonl
  python select_facts.py --pool _pool.jsonl --out bank.jsonl --default-quota 200
  python bake_index.py --facts bank.jsonl --out tpl.jinja
"""
import argparse, glob, json, os


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--domain", required=True,
                    help="api_facts/<domain>__*.jsonl  (data | web | ai | stdlib)")
    ap.add_argument("--curated", default="facts_pythondata_v4.jsonl",
                    help="bank to take the CURATED facts from (ids without 'api-')")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    curated = [l for l in open(a.curated, encoding="utf-8")
               if l.strip() and "api-" not in json.loads(l)["id"]]
    mined = [l for f in sorted(glob.glob(os.path.join("api_facts", f"{a.domain}__*.jsonl")))
             for l in open(f, encoding="utf-8") if l.strip()]
    if not mined:
        raise SystemExit(f"no mined facts for domain '{a.domain}' in api_facts/")

    with open(a.out, "w", encoding="utf-8") as w:
        w.writelines(curated)
        w.writelines(l if l.endswith("\n") else l + "\n" for l in mined)
    print(f"{len(curated)} curated + {len(mined)} mined ({a.domain}) "
          f"= {len(curated)+len(mined)} facts -> {a.out}")


if __name__ == "__main__":
    main()
