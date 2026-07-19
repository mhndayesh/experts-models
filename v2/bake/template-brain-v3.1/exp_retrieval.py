#!/usr/bin/env python3
"""exp_retrieval.py - do the textbook IR fixes actually help? Measure, don't assume.

Every variant is scored on the SAME three numbers, all offline, no GPU:
  gold      12 known questions must still find their fact   (must not regress)
  controls  10 off-topic questions must retrieve NOTHING    (must stay 0)
  reach     of ALL 1,911 facts, how many can any realistic question pull?

Reachability is the metric under test. The gold set is the guard rail: a variant
that lifts reachability but breaks gold or fires a control is a regression, not a
win.

HONESTY: each variant is baked with 2 expansions per curated fact HELD OUT of the
index, and probed with exactly those held-out questions. A fact never sees the
words it is asked with. (Without this, facts retrieve themselves and every design
scores ~100%.)
"""
import json, subprocess, sys, time

FACTS = "facts_pythondata_v4.jsonl"
PROBE_EXP = "_expansions_probe.json"       # written by reach.py: the held-out split

VARIANTS = [
    ("baseline",        []),
    ("smooth-idf",      ["--idf", "smooth"]),
    ("discriminative",  ["--discriminative"]),
    ("len-norm",        ["--len-norm"]),
    ("disc+smooth",     ["--discriminative", "--idf", "smooth"]),
    ("all three",       ["--discriminative", "--idf", "smooth", "--len-norm"]),
]


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    return r.returncode, r.stdout, r.stderr


def main():
    # the held-out split must exist and must be the SAME for every variant
    import reach
    held = reach.build_probe_expansions()
    print(f"held out {sum(len(v) for v in held.values()):,} questions "
          f"across {len(held):,} curated facts\n")

    rows = []
    for name, flags in VARIANTS:
        t0 = time.time()
        tpl = f"_exp_{name.replace(' ', '_').replace('+', '_')}.jinja"

        # 1. bake with the held-out expansions (honest index)
        rc, out, err = run([sys.executable, "bake_index.py", "--facts", FACTS,
                            "--expansions", PROBE_EXP, "--out", tpl] + flags)
        if rc:
            print(f"{name:15} BAKE FAILED: {(err or out)[-160:]}")
            continue
        nterms = int(out.split("|")[1].strip().split()[0]) if "|" in out else 0
        kb = int(out.rsplit("(", 1)[1].split(" KB")[0])

        # 2. gold + controls, through the REAL template
        rc, out, err = run([sys.executable, "baseline.py", tpl, "--json"])
        c = json.loads(out)

        # 3. reachability, probed with the held-out questions
        rc, out, err = run([sys.executable, "reach.py", "--skip-bake",
                            "--template", tpl, "--json"])
        try:
            r = json.loads(out)
        except json.JSONDecodeError:
            print(f"{name:15} REACH FAILED: {(err or out)[-160:]}")
            continue

        rows.append(dict(name=name, gold=c["gold"], gold_ok=c["gold_ok"],
                         ctl=c["controls_fired"], ctl_ok=c["controls_ok"],
                         cur=r["curated_pct"], mined=r["mined_pct"], bank=r["bank_pct"],
                         dead=r["dead"], kb=kb, terms=nterms, secs=round(time.time() - t0)))
        print(f"  {name:15} done in {rows[-1]['secs']}s")

    print()
    print("=" * 92)
    print(f"{'variant':16} {'gold':>7} {'ctl':>6} {'curated':>9} {'mined':>8} "
          f"{'BANK':>8} {'dead':>6} {'KB':>5} {'terms':>7}")
    print("-" * 92)
    base = rows[0] if rows else None
    for r in rows:
        d = ""
        if base and r is not base:
            delta = r["cur"] - base["cur"]
            d = f"  ({delta:+.1f} curated)"
        flag = "" if (r["gold_ok"] and r["ctl_ok"]) else "  <-- REGRESSION"
        print(f"{r['name']:16} {r['gold']:>7} {r['ctl']:>6} {r['cur']:>8.1f}% "
              f"{r['mined']:>7.1f}% {r['bank']:>7.1f}% {r['dead']:>6} {r['kb']:>5} "
              f"{r['terms']:>7}{d}{flag}")
    print("=" * 92)
    json.dump(rows, open("_exp_retrieval.json", "w", encoding="utf-8"), indent=1)
    print("\n-> _exp_retrieval.json")


if __name__ == "__main__":
    main()
