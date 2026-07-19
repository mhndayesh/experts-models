#!/usr/bin/env python3
"""reach.py - REACHABILITY: what fraction of the bank can any question actually pull?

gold.json asks "do 12 known questions find their facts". That cannot scale: nobody
will write 21,000 gold questions. This asks the inverse, per fact, for free:

    can ANY realistic question retrieve this fact into the top 5?

A fact that no question can reach is DEAD WEIGHT - it costs bytes, contests slots,
and helps nobody. Reachability is the number that keeps meaning something at 2k,
21k or 200k facts.

THE CIRCULARITY TRAP: a fact's Doc2Token expansions are INDEXED. Probing with an
indexed question means the fact retrieves itself trivially - a meaningless 100%.
So we HOLD OUT 2 expansions per fact, re-bake the index without them, and probe
with the held-out ones. The fact has never seen the words we ask it with.

Retrieval runs through the REAL baked template (jinja2 render), not a Python
re-implementation - so what we measure is what ships.

  curated facts (388)  probed with held-out everyday-language questions
  mined facts (1,523)  have no expansions; probed with their own API name, which
                       is the ONLY way anyone could reach them. That is the point:
                       it measures the ceiling of a literal-token-only fact.

usage:
    python reach.py                    # full run (bakes a probe template first)
    python reach.py --skip-bake        # reuse _tpl_probe.jinja
"""
import argparse, collections, json, os, re, subprocess, sys

from baseline import compile_tpl, facts_injected, load_bank, render

FACTS = "facts_pythondata_v4.jsonl"

EXPANSIONS = "expansions_v2.json"
PROBE_EXP = "_expansions_probe.json"
PROBE_TPL = "_tpl_probe.jinja"
HOLDOUT = 2


def build_probe_expansions():
    """hold out the LAST 2 questions of each fact - deterministic, no randomness"""
    exp = json.load(open(EXPANSIONS, encoding="utf-8"))
    train, held = {}, {}
    for fid, qs in sorted(exp.items()):
        if len(qs) <= HOLDOUT:
            train[fid] = qs                       # too few to hold out; keep, don't probe
            continue
        train[fid] = qs[:-HOLDOUT]
        held[fid] = qs[-HOLDOUT:]
    with open(PROBE_EXP, "w", encoding="utf-8") as f:
        json.dump(train, f, indent=1, sort_keys=True)
    return held


def api_name(fact):
    """the literal call a user would type for a mined signature fact"""
    m = re.match(r"([A-Za-z_][\w.]*)\s*\(", fact["text"])
    return m.group(1) if m else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--skip-bake", action="store_true")
    ap.add_argument("--template", default=PROBE_TPL)
    ap.add_argument("--json", action="store_true", help="machine-readable, for exp_retrieval.py")
    a = ap.parse_args()

    held = build_probe_expansions()
    if not a.json:
        print(f"held out {sum(len(v) for v in held.values()):,} questions "
              f"across {len(held):,} curated facts\n")

    if not a.skip_bake:
        print("baking probe template (index WITHOUT the held-out questions)...")
        r = subprocess.run([sys.executable, "bake_index.py", "--facts", FACTS,
                            "--expansions", PROBE_EXP, "--out", PROBE_TPL],
                           capture_output=True, text=True)
        if r.returncode != 0:
            print("BAKE FAILED:\n" + (r.stderr or r.stdout)[-800:])
            return 1
        print("  " + (r.stdout.strip().splitlines() or [""])[-1] + "\n")

    tpl = open(a.template, encoding="utf-8").read()
    by_id, by_text = load_bank()
    facts = {json.loads(l)["id"]: json.loads(l)
             for l in open(FACTS, encoding="utf-8") if l.strip()}

    curated = [f for f in facts.values() if "api-" not in f["id"]]
    mined = [f for f in facts.values() if "api-" in f["id"]]

    # Build the full probe list, then render SINGLE-PROCESS with the template
    # compiled ONCE. The parse of the ~1 MB template is the whole cost (~0.75 s);
    # each render is ~1.3 ms, so ~2,300 probes finish in ~4 s. The old ProcessPool
    # re-parsed the megabyte in EVERY worker on Windows spawn - that, not the
    # per-render work, was the minutes-long slowness. Parse once, render many.
    jobs = []                       # (fact_id, kind, question)
    for f in curated:
        for q in held.get(f["id"], []):
            jobs.append((f["id"], "curated", q))
    for f in mined:
        name = api_name(f)
        if name:
            jobs.append((f["id"], "mined", f"how do I use {name} in {f['source']}?"))

    compiled = compile_tpl(tpl)
    got_lists = [
        facts_injected(
            compiled.render(messages=[{"role": "user", "content": q}],
                            add_generation_prompt=True),
            by_text)
        for _, _, q in jobs
    ]

    stealers = collections.Counter()
    hits = collections.defaultdict(bool)
    asked = {}
    for (fid, kind, q), got in zip(jobs, got_lists):
        asked.setdefault(fid, (kind, q))
        if fid in got:
            hits[fid] = True
        else:
            stealers.update(g for g in got if g != fid)

    results = {"curated": {"reach": 0, "total": 0, "dead": []},
               "mined": {"reach": 0, "total": 0, "dead": []}}
    for fid, (kind, q) in sorted(asked.items()):
        results[kind]["total"] += 1
        if hits[fid]:
            results[kind]["reach"] += 1
        else:
            results[kind]["dead"].append((fid, q[:58]))

    if a.json:
        cur, mi = results["curated"], results["mined"]
        tot_r = cur["reach"] + mi["reach"]
        tot_t = cur["total"] + mi["total"]
        print(json.dumps({
            "template": a.template,
            "curated_pct": round(100 * cur["reach"] / cur["total"], 1) if cur["total"] else 0,
            "mined_pct": round(100 * mi["reach"] / mi["total"], 1) if mi["total"] else 0,
            "bank_pct": round(100 * tot_r / tot_t, 1) if tot_t else 0,
            "dead": tot_t - tot_r,
            "stealers": stealers.most_common(10),
        }))
        return 0

    print("=" * 66)
    print("REACHABILITY - can any realistic question pull this fact into the top 5?")
    print("=" * 66)
    for k in ("curated", "mined"):
        r = results[k]
        pct = 100 * r["reach"] / r["total"] if r["total"] else 0
        probe = "held-out everyday questions" if k == "curated" else "its own API name"
        print(f"  {k:8} {r['reach']:5,}/{r['total']:<5,} = {pct:5.1f}%   (probed with {probe})")
    tot_r = results["curated"]["reach"] + results["mined"]["reach"]
    tot_t = results["curated"]["total"] + results["mined"]["total"]
    print(f"  {'BANK':8} {tot_r:5,}/{tot_t:<5,} = {100*tot_r/tot_t:5.1f}%")
    print()
    print(f"  DEAD WEIGHT: {tot_t - tot_r:,} facts no question could retrieve")
    print()
    print("  top seat-stealers (facts that won slots the probed fact wanted):")
    for fid, n in stealers.most_common(10):
        t = facts.get(fid, {}).get("text", "")[:52]
        print(f"    {n:4}x  {fid:<20} {t}")

    json.dump({"curated": {k: v for k, v in results["curated"].items()},
               "mined": {k: v for k, v in results["mined"].items()},
               "stealers": stealers.most_common(40)},
              open("_reach.json", "w", encoding="utf-8"), indent=1)
    print("\n  full detail -> _reach.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
