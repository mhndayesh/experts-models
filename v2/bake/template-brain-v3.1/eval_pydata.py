#!/usr/bin/env python3
"""eval_pydata.py - scored A/B for the pythondatafactbank model.

Repo discipline (CLAUDE.md):
  * PROBE FIRST: the baseline arm IS the probe. A case only proves something
    if the bare model cannot already answer it. KNOWS = passed CODE on ANY rep.
  * TWO METRICS, ALWAYS BOTH: USES (did the information reach the answer at
    all - the architecture question) and CODE (does the code actually obey it
    - the product question). The gap between them is the finding.
  * CONTROLS ARE A SEPARATE METRIC, never averaged into ALL (F-027).
  * SCORE WHAT THE CODE DOES: markers are matched by codecheck.py's AST index
    (calls, kwargs, identifier chains). Comments and string literals count for
    nothing (F-029). We do not re-implement the scorer - we import it.
  * BOTH VIEWS: diagnostic (truncations excluded) and product (truncation =
    failure). The baseline never truncates, so exclusion alone flatters the
    bank arm.

Cases target the POST-CUTOFF dead-name seam (pandas 3.0 = Jan 2026, polars
1.x, numpy 2.x). Every "right" answer requires a fact that is in the bank.
NB: codecheck lowercases identifiers, so np.NaN vs np.nan is NOT scoreable by
CODE - such cases are deliberately excluded rather than faked.

usage:
  python eval_pydata.py --arm bank     --model gemma-4-12b-pythondatafactbank
  python eval_pydata.py --arm baseline --model google/gemma-4-12b-qat
  python eval_pydata.py --score
"""
import argparse, json, os, sys, time, urllib.request

sys.path.insert(0, os.path.abspath(os.path.join(
    "..", "..", "NEW BANK", "factbank", "factbank")))
import codecheck  # the repo's AST scorer - do NOT reimplement (F-007/F-029)

URL = "http://127.0.0.1:1234/api/v0/chat/completions"
REPS = 3

CASES = [
    # ---- pandas 3.0 (released 2026-01, a year past the Jan-2025 cutoff) ----
    dict(id="pd-h1", level="hard", lib="pandas",
         prompt="My pandas code does df.applymap(lambda x: x * 2) and now raises "
                "AttributeError on pandas 3.0. Fix it - show the corrected code.",
         uses=["map", "applymap", "removed"], call=[".map("], wrong=[".applymap("]),
    dict(id="pd-n1", level="normal", lib="pandas",
         prompt="In pandas 3.0, apply a function to every element of a DataFrame. "
                "Show the code.",
         uses=["map"], call=[".map("], wrong=[".applymap("]),
    dict(id="pd-m1", level="medium", lib="pandas",
         prompt="In pandas 3.0, forward-fill missing values in a DataFrame. "
                "Show the code.",
         uses=["ffill"], call=[".ffill("], wrong=["fillna(method="]),
    dict(id="pd-h2", level="hard", lib="pandas",
         prompt="This pandas code raises ChainedAssignmentError on 3.0: "
                'df["price"][df["qty"] > 5] = 0 . Fix it - show the corrected code.',
         uses=["loc", "copy-on-write"], call=[".loc"], wrong=[]),
    dict(id="pd-m2", level="medium", lib="pandas",
         prompt="In pandas 3.0, interpolate a Series forward. I used "
                'interpolate(method="pad") and it fails. Show working code.',
         uses=["ffill"], call=[".ffill("], wrong=["interpolate(method="]),

    # ---- polars 1.x ----
    dict(id="pl-h1", level="hard", lib="polars",
         prompt="My polars code calls df.melt(id_vars=['name'], value_vars=['a','b']) "
                "and it no longer works after upgrading. Fix it - show the code.",
         uses=["unpivot", "index", "on"], call=["unpivot(index="], wrong=[".melt("]),
    dict(id="pl-n1", level="normal", lib="polars",
         prompt="Using polars 1.x, reshape a wide DataFrame into long format. "
                "Show the code.",
         uses=["unpivot"], call=[".unpivot("], wrong=[".melt("]),
    dict(id="pl-h2", level="hard", lib="polars",
         prompt="In polars, pl.count() with no arguments to get the row count is "
                "deprecated. What replaces it? Show the code.",
         uses=["len"], call=["pl.len("], wrong=["pl.count("]),
    dict(id="pl-m1", level="medium", lib="polars",
         prompt="In polars 1.x, apply a Python function elementwise to a column. "
                "Show the code.",
         uses=["map_elements"], call=[".map_elements("], wrong=[".apply("]),
    dict(id="pl-m2", level="medium", lib="polars",
         prompt="In polars 1.x, group a DataFrame by a column and aggregate. "
                "Show the code.",
         uses=["group_by"], call=[".group_by("], wrong=[".groupby("]),
    dict(id="pl-h3", level="hard", lib="polars",
         prompt="My polars code calls lf.collect(streaming=True) and errors on 1.x. "
                "Fix it - show the corrected code.",
         uses=["engine", "streaming"], call=["collect(engine="],
         wrong=["collect(streaming="]),

    # ---- numpy 2.x (scoreable ones only: codecheck is case-insensitive, so
    #      np.NaN -> np.nan and np.Inf -> np.inf CANNOT be scored by CODE) ----
    dict(id="np-h1", level="hard", lib="numpy",
         prompt="My numpy code uses np.float_ and raises AttributeError on numpy 2. "
                "Fix it - show the corrected code.",
         uses=["float64", "removed"], call=["np.float64"], wrong=["np.float_"]),
    dict(id="np-h2", level="hard", lib="numpy",
         prompt="numpy 2 broke my call to np.product(arr). Fix it - show the code.",
         uses=["prod"], call=["np.prod("], wrong=["np.product("]),
    dict(id="np-m1", level="medium", lib="numpy",
         prompt="In numpy 2, test which elements of array a are present in array b. "
                "Show the code.",
         uses=["isin"], call=["np.isin("], wrong=["np.in1d("]),
    dict(id="np-m2", level="medium", lib="numpy",
         prompt="In numpy 2, make a fixed-width byte-string dtype array. Show the code.",
         uses=["bytes_"], call=["np.bytes_"], wrong=["np.string_"]),

    # ---- controls: bank must NOT drag facts in (fact-slavery check) ----
    dict(id="ctl-1", level="control", lib="-",
         prompt="Write a haiku about the sea.", uses=[], call=[], wrong=[]),
    dict(id="ctl-2", level="control", lib="-",
         prompt="Explain what a closure is in Python, briefly.",
         uses=[], call=[], wrong=[]),
    dict(id="ctl-3", level="control", lib="-",
         prompt="Write a python function that returns the nth Fibonacci number.",
         uses=[], call=[], wrong=[]),
    dict(id="ctl-4", level="control", lib="-",
         prompt="Explain the difference between processes and threads in a short "
                "paragraph.", uses=[], call=[], wrong=[]),
]

FACT_MARKERS = ["[src:", "[version:", "documentation lookup results",
                "factbank_search"]


def ask(model, prompt, max_tokens=1536):
    body = json.dumps({"model": model,
                       "messages": [{"role": "user", "content": prompt}],
                       "temperature": 0.2, "max_tokens": max_tokens}).encode()
    req = urllib.request.Request(URL, data=body,
                                 headers={"Content-Type": "application/json"})
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=900) as r:
        resp = json.loads(r.read())
    ch = resp["choices"][0]
    return {"content": ch["message"].get("content") or "",
            "finish": ch.get("finish_reason"),
            "usage": resp.get("usage", {}), "stats": resp.get("stats", {}),
            "wall": round(time.time() - t0, 1)}


def run(arm, model):
    out = []
    for c in CASES:
        for rep in range(REPS):
            a = ask(model, c["prompt"])
            rec = dict(arm=arm, model=model, rep=rep, **{k: c[k] for k in
                       ("id", "level", "lib", "prompt", "uses", "call", "wrong")},
                       **a)
            out.append(rec)
            print(f"  {arm:8} {c['id']:6} rep{rep} "
                  f"{a['finish']:6} {a['usage'].get('completion_tokens',0):5}tok "
                  f"{a['wall']:5}s")
    path = f"eval_{arm}.jsonl"
    with open(path, "w", encoding="utf-8") as f:
        for r in out:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"saved {path} ({len(out)} rows)")


def score_row(r):
    """USES = information reached the answer (prose ok). CODE = the code obeys.
    code_ok is None when the case has nothing to call (controls) - callers MUST
    exclude None (F-026)."""
    text = r["content"]
    fences = codecheck.fences_of(text)
    idx = codecheck.index_fences(fences)
    uses = all(m.lower() in text.lower() for m in r["uses"]) if r["uses"] else None
    code = (codecheck.all_markers_in_code(r["call"], idx) if r["call"] else None)
    wrong = any(codecheck.marker_in_index(m, idx, penalty_ok=True)
                for m in r["wrong"]) if r["wrong"] else False
    noise = any(m in text for m in FACT_MARKERS)      # controls: fact leakage
    trunc = r["finish"] == "length"
    return uses, code, wrong, noise, trunc


def score():
    rows = []
    for arm in ("baseline", "bank"):
        p = f"eval_{arm}.jsonl"
        if os.path.exists(p):
            rows += [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]
    if not rows:
        sys.exit("no eval_*.jsonl found - run the arms first")

    per = {}
    for r in rows:
        u, c, w, n, t = score_row(r)
        per.setdefault((r["arm"], r["id"]), []).append(
            dict(level=r["level"], uses=u, code=c, wrong=w, noise=n, trunc=t))

    # PROBE: a case is "known" if the BASELINE passed CODE on ANY rep
    known = {cid for (arm, cid), reps in per.items()
             if arm == "baseline" and any(x["code"] for x in reps)}

    print("\n=== PROBE (baseline = the probe; KNOWS = passed CODE on any rep) ===")
    for c in CASES:
        if c["level"] == "control":
            continue
        reps = per.get(("baseline", c["id"]))
        if not reps:
            continue
        print(f"  {c['id']:6} {c['level']:7} {'KNOWS (excluded)' if c['id'] in known else 'unknown -> measurable'}")

    def agg(arm, levels, view):
        u_n = u_d = c_n = c_d = w_n = w_d = 0
        for c in CASES:
            if c["level"] not in levels or c["id"] in known:
                continue
            for x in per.get((arm, c["id"]), []):
                if view == "diagnostic" and x["trunc"]:
                    continue
                if x["uses"] is not None:
                    u_d += 1
                    u_n += bool(x["uses"]) and not (view == "product" and x["trunc"])
                if x["code"] is not None:
                    c_d += 1
                    c_n += bool(x["code"]) and not (view == "product" and x["trunc"])
                if c["wrong"]:
                    w_d += 1
                    w_n += bool(x["wrong"])
        return (u_n / u_d if u_d else 0, c_n / c_d if c_d else 0,
                w_n / w_d if w_d else 0, c_d)

    for view in ("diagnostic", "product"):
        print(f"\n=== SCORE ({view} view; truncations "
              f"{'excluded' if view=='diagnostic' else 'count as failure'}) ===")
        print(f"{'tier':10} {'arm':9} {'USES':>6} {'CODE':>6} {'wrong-API':>10} {'n':>4}")
        for levels, label in ((("hard",), "hard"), (("medium",), "medium"),
                              (("normal",), "normal"),
                              (("hard", "medium", "normal"), "ALL")):
            for arm in ("baseline", "bank"):
                u, c, w, n = agg(arm, levels, view)
                print(f"{label:10} {arm:9} {u:6.2f} {c:6.2f} {w:10.2f} {n:4}")

    print("\n=== CONTROLS (separate metric, never averaged in - F-027) ===")
    for arm in ("baseline", "bank"):
        reps = [x for c in CASES if c["level"] == "control"
                for x in per.get((arm, c["id"]), [])]
        if not reps:
            continue
        leaked = sum(1 for x in reps if x["noise"])
        print(f"  {arm:9} fact-leakage into control answers: {leaked}/{len(reps)}")

    trunc = [(r['arm'], r['id']) for r in rows if r['finish'] == 'length']
    print(f"\ntruncations: {len(trunc)} {sorted(set(trunc))[:6]}")
    print(f"cases: {len([c for c in CASES if c['level']!='control'])} measurable "
          f"({len(known)} excluded as KNOWN), {len([c for c in CASES if c['level']=='control'])} controls, {REPS} reps")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--arm", choices=["baseline", "bank"])
    ap.add_argument("--model")
    ap.add_argument("--score", action="store_true")
    a = ap.parse_args()
    if a.score:
        score()
    else:
        if not (a.arm and a.model):
            sys.exit("need --arm and --model (or --score)")
        run(a.arm, a.model)
