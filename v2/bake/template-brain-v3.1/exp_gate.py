#!/usr/bin/env python3
"""exp_gate.py - can we keep the +10 recall AND claw the precision back?

The expansion-gate lifted curated reachability 64.4% -> 74.5%, but precision fell
90.4% -> 87.4%: a generic word ("replacement"), unique to pandas only by accident,
opened the PANDAS tab on the numpy question "is there a replacement for np.fix?".

So a trigger must be SPECIFIC. Two knobs:
  --gate-exp-minlen   how long a word must be
  --gate-exp-max-df   how FEW facts may use it (a word many facts use is phrasing,
                      not a topic)

Reported together, because optimising recall alone is how the leak got in.
"""
import json, subprocess, sys

import reach
from baseline import compile_tpl, facts_injected, load_bank
from bake_index import build, is_curated

FACTS = "facts_pythondata_v4.jsonl"
PE = "_expansions_probe.json"

GRID = [
    ("shipped (no expGate)", ["--gate-n", "48"]),
    ("expGate len5  df999",  ["--gate-n", "150", "--idf", "smooth", "--gate-expansions"]),
    ("expGate len6  df8",    ["--gate-n", "150", "--idf", "smooth", "--gate-expansions",
                              "--gate-exp-minlen", "6", "--gate-exp-max-df", "8"]),
    ("expGate len6  df4",    ["--gate-n", "150", "--idf", "smooth", "--gate-expansions",
                              "--gate-exp-minlen", "6", "--gate-exp-max-df", "4"]),
    ("expGate len7  df3",    ["--gate-n", "150", "--idf", "smooth", "--gate-expansions",
                              "--gate-exp-minlen", "7", "--gate-exp-max-df", "3"]),
    ("expGate len6  df2",    ["--gate-n", "150", "--idf", "smooth", "--gate-expansions",
                              "--gate-exp-minlen", "6", "--gate-exp-max-df", "2"]),
]


def main():
    held = reach.build_probe_expansions()
    d = build(FACTS, "controls_pydata.txt", "taskwords_pydata.json", 48, PE)
    rows = [json.loads(l) for l in open(FACTS, encoding="utf-8") if l.strip()]
    rows.sort(key=lambda r: (not is_curated(r["id"]),))
    lib_of = {r["id"]: d["lib"][i] for i, r in enumerate(rows)}
    by_id, by_text = load_bank()
    gold = json.load(open("jinja_lab/gold.json", encoding="utf-8"))

    print(f"{'variant':22} {'gold':>6} {'ctl':>5} {'RECALL':>8} {'PRECISION':>10} "
          f"{'empty':>6} {'KB':>5}")
    print("-" * 74)
    for name, flags in GRID:
        tpl_path = "_gx_" + name.split("(")[0].strip().replace(" ", "_") + ".jinja"
        r = subprocess.run([sys.executable, "bake_index.py", "--facts", FACTS,
                            "--expansions", PE, "--out", tpl_path] + flags,
                           capture_output=True, text=True)
        if r.returncode:
            print(f"{name:22} SIZE GUARD: {r.stderr.strip().splitlines()[-1][:34]}")
            continue
        kb = int(r.stdout.rsplit("(", 1)[1].split(" KB")[0])
        tpl = compile_tpl(open(tpl_path, encoding="utf-8").read())

        def inject(q):
            return facts_injected(
                tpl.render(messages=[{"role": "user", "content": q}],
                           add_generation_prompt=True), by_text)

        hit = tot = inj = same = empty = 0
        for fid, qs in sorted(held.items()):
            tot += 1
            ok = False
            for q in qs:
                got = inject(q)
                if not got:
                    empty += 1
                if fid in got:
                    ok = True
                for g in got:
                    inj += 1
                    same += (lib_of.get(g) == lib_of[fid])
            hit += ok
        g_hit = sum(1 for c in gold["cases"] if c["gold"] in inject(c["q"]))
        ctl = sum(1 for q in gold["controls"] if inject(q))
        print(f"{name:22} {g_hit:>3}/12 {ctl:>2}/10 {100*hit/tot:>7.1f}% "
              f"{100*same/max(1,inj):>9.1f}% {empty:>6} {kb:>5}"
              + ("" if ctl == 0 else "  <-- CONTROL FIRED"))


if __name__ == "__main__":
    main()
