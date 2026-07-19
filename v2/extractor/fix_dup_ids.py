#!/usr/bin/env python3
"""fix_dup_ids.py - repair duplicate fact ids in the shipped expert banks.

The historical id hashed only `type|subject|old|new` (extract.py:cid, now fixed),
so DISTINCT facts with null subject/old/new collided: 19 groups / 38 rows, incl. a
cross-library flask/hf-datasets clash. This re-ids ONLY the colliding rows with a
content-complete hash (lib|version|type|subject|old|new|truth[:80]), keeping every
non-colliding id stable. Idempotent; verifies global uniqueness at the end.

  python fix_dup_ids.py [--dry-run]
"""
import json, glob, hashlib, collections, os, sys, argparse

HERE = os.path.dirname(os.path.abspath(__file__))
GLOB = os.path.join(HERE, "experts", "*", "facts", "*.jsonl")

def rich_id(r):
    key = (f"{r.get('lib')}|{r.get('version')}|{r.get('type')}|{r.get('subject')}|"
           f"{r.get('old')}|{r.get('new')}|{(r.get('truth') or '')[:80]}")
    return "sx-" + hashlib.sha256(key.encode()).hexdigest()[:10]

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    files = sorted(glob.glob(GLOB))
    # pass 1: find colliding ids
    by_id = collections.defaultdict(list)
    for f in files:
        for i, l in enumerate(open(f, encoding="utf-8")):
            l = l.strip()
            if not l: continue
            by_id[json.loads(l)["id"]].append((f, i))
    dup_ids = {k for k, v in by_id.items() if len(v) > 1}
    print(f"{len(dup_ids)} colliding ids across {sum(len(by_id[k]) for k in dup_ids)} rows")
    existing = set(by_id)                       # all ids currently in use
    changes = 0
    for f in files:
        lines = [l for l in open(f, encoding="utf-8")]
        out, touched = [], False
        for l in lines:
            s = l.strip()
            if not s:
                out.append(l); continue
            r = json.loads(s)
            if r["id"] in dup_ids:
                nid = rich_id(r)
                # guard against a (vanishingly unlikely) new clash
                while nid in existing and nid != r["id"]:
                    nid = "sx-" + hashlib.sha256((nid + "x").encode()).hexdigest()[:10]
                if nid != r["id"]:
                    existing.add(nid); r["id"] = nid; touched = True; changes += 1
                    out.append(json.dumps(r, ensure_ascii=False) + "\n")
                    continue
            out.append(l if l.endswith("\n") else l + "\n")
        if touched and not a.dry_run:
            open(f, "w", encoding="utf-8").writelines(out)
            print(f"  rewrote {os.path.relpath(f, HERE)}")
    print(f"{'[dry-run] would re-id' if a.dry_run else 're-id'} {changes} rows")
    # verify
    seen = collections.Counter()
    for f in files:
        for l in open(f, encoding="utf-8"):
            l = l.strip()
            if l: seen[json.loads(l)["id"]] += 1
    remaining = {k: c for k, c in seen.items() if c > 1}
    print(f"remaining duplicate ids: {len(remaining)}")
    if remaining and not a.dry_run:
        sys.exit("FAILED: duplicates remain " + str(list(remaining)[:5]))

if __name__ == "__main__":
    main()
