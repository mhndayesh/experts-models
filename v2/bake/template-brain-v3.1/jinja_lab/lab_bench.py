#!/usr/bin/env python3
"""bench.py - score every retrieval design on the gold set, with NO baking.

Metrics (all offline, deterministic, free):
  hit@5     - did the gold fact win one of the 5 slots?  (the metric that matters)
  rank      - where the gold fact landed (lower is better; '-' = not eligible)
  ctl_fires - controls that retrieved ANY fact (must be 0: fact-slavery guard)
  bytes     - the size the design's data would add to the template (the 1 MiB
              ceiling is the real budget, F-048)

usage: python bench.py [--full]
"""
import argparse, json, sys, collections
sys.path.insert(0, ".")
from designs import DESIGNS, build_index, run_index, norm, words


def load_bank():
    """the shipped 2,560-fact pydata bank, with provenance and trigger lists"""
    rows = [json.loads(l) for l in
            open("../bank_pythondata_v3.jsonl", encoding="utf-8").read().splitlines()[1:]
            if l.strip()]
    raw = {json.loads(l)["id"]: json.loads(l) for l in
           open("../facts_pythondata_v3.jsonl", encoding="utf-8")}
    sys.path.insert(0, "..")
    from bake_template_v3 import build_gate
    gate, groups, _ = build_gate(rows, 48)
    trig = {g["lib"]: g["trig"] for g in gate}
    bank = []
    for r in rows:
        lib = " " + r["library"] + " "
        rid = r["id"]
        bank.append({
            "id": rid, "lib": lib, "trig": trig.get(lib, []),
            "s": r["s"], "c": r.get("c", []), "w": r["w"], "d": r.get("d", []),
            "txt": r["txt"],
            # PROVENANCE, not kind: a curated research fact can be labelled
            # kind="signature" (polars-001) and must still be treated as
            # curated - that mislabel evicted it from the shipped bank.
            "curated": not rid.endswith(tuple("0123456789")) or
                       not rid.split("-")[0].endswith("api"),
        })
    return bank


def data_bytes(name, model):
    """bytes this design's DATA adds to the template (the 1 MiB ceiling is the
    real budget). Scan: every fact carries its own keyword lists. Index: keys
    are stored once, globally, but every posting repeats a fact id."""
    if name == "D1_scan_today":
        return sum(len(json.dumps({k: f[k] for k in ("s", "c", "w", "d", "txt")},
                                  ensure_ascii=False)) for f in model["facts"])
    post_b = sum(len(t) + 4 + sum(len(sid) + 4 for sid, _ in pl)
                 for t, pl in model["post"].items())
    txt_b = sum(len(f["txt"]) + 10 for f in model["bank"])   # id->txt map
    return post_b + txt_b


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--full", action="store_true")
    a = ap.parse_args()
    bank = load_bank()
    gold = json.load(open("gold.json", encoding="utf-8"))
    cases, controls = gold["cases"], gold["controls"]

    built = {name: (b(bank), r) for name, (b, r) in DESIGNS.items()}
    print(f"bank: {len(bank)} facts | {sum(1 for f in bank if f['curated'])} curated\n")

    hdr = f"{'case':52} " + " ".join(f"{n.split('_',1)[1][:11]:>12}" for n in DESIGNS)
    print(hdr)
    print("-" * len(hdr))
    tally = collections.Counter()
    for c in cases:
        cells = []
        for name, (model, run) in built.items():
            got = run(model, c["q"])
            hit = c["gold"] in got
            rank = got.index(c["gold"]) + 1 if hit else None
            tally[name] += hit
            cells.append(f"{'HIT@'+str(rank) if hit else 'miss':>12}")
        print(f"{c['q'][:52]:52} " + " ".join(cells))
    print("-" * len(hdr))
    print(f"{'HIT@5 (gold fact retrieved)':52} " +
          " ".join(f"{str(tally[n])+'/'+str(len(cases)):>12}" for n in DESIGNS))

    # controls: must retrieve NOTHING
    cfires = {}
    for name, (model, run) in built.items():
        cfires[name] = sum(1 for q in controls if run(model, q))
    print(f"{'control false-fires (want 0)':52} " +
          " ".join(f"{str(cfires[n])+'/'+str(len(controls)):>12}" for n in DESIGNS))

    # bytes
    print(f"{'data bytes in template':52} " +
          " ".join(f"{data_bytes(n, built[n][0])/1024:>11.0f}K" for n in DESIGNS))
    print(f"{'facts that fit under 0.9MB budget':52} " +
          " ".join(f"{int(len(bank) * 900_000 / max(1,data_bytes(n, built[n][0]))):>12}"
                   for n in DESIGNS))

    if a.full:
        print("\n--- what the winner retrieves (D4) ---")
        model, run = built["D4_index_class"]
        for c in cases[:4]:
            got = run(model, c["q"])
            print(f"\nQ: {c['q'][:60]}")
            for fid in got:
                mark = " <<< GOLD" if fid == c["gold"] else ""
                print(f"   {fid:16} {model['meta'][fid]['txt'][:60]}{mark}")


if __name__ == "__main__":
    main()
