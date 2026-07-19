#!/usr/bin/env python3
"""lint.py - render the baked template against scenarios/*.json under
strict jinja2 and assert lane invariants. Passing here does NOT prove
minja/LM Studio pass (engines differ); it catches logic and typo bugs
before any server is touched.

scenario file: {"name":..., "messages":[...], "tools":[...] or null,
               "expect": {"contains":[...], "not_contains":[...]}}
"""
import json, glob, sys
import jinja2

def render(tpl, sc):
    # scenario "lenient": true renders with default Undefined instead of
    # StrictUndefined - needed for families whose SOURCE template relies
    # on lenient undefined handling (gemma-4 truth-tests missing keys
    # like message['tool_calls'] / value['enum']; minja tolerates that).
    und = jinja2.Undefined if sc.get("lenient") else jinja2.StrictUndefined
    env = jinja2.Environment(undefined=und)
    return env.from_string(tpl).render(
        messages=sc["messages"], tools=sc.get("tools"),
        add_generation_prompt=True, bos_token="")

def main(tpl_path="baked_index_v6.jinja", pattern="scenarios_pydata/*.json"):
    # scenarios_pydata = the SHIPPED pythondata model (p8 = numpy dead name).
    # scenarios_gemma4 = the 1,027-fact NICHE model (g8 = BQN) - use it with
    # baked_gemma4_1k.jinja, or g8 fails against a bank that has no BQN facts.
    tpl = open(tpl_path, encoding="utf-8").read()
    fails = 0
    for path in sorted(glob.glob(pattern)):
        sc = json.load(open(path, encoding="utf-8"))
        try:
            out = render(tpl, sc)
        except Exception as e:
            print(f"FAIL {sc['name']}: render error: {e}")
            fails += 1
            continue
        probs = []
        for s in sc["expect"].get("contains", []):
            if s not in out:
                probs.append(f"missing {s!r}")
        for s in sc["expect"].get("not_contains", []):
            if s in out:
                probs.append(f"present {s!r}")
        for a, b in sc["expect"].get("ordered", []):
            if not (a in out and b in out and out.index(a) < out.index(b)):
                probs.append(f"order violated: {a!r} before {b!r}")
        fbp = sc["expect"].get("first_block_pure")
        if fbp:
            lo, hi = fbp["between"]
            if lo in out and hi in out:
                block = out[out.index(lo):out.index(hi)]
                for s in fbp.get("not_contains", []):
                    if s in block:
                        probs.append(f"history rewrite: {s!r} inside first block (point 14)")
            else:
                probs.append("first_block_pure markers missing")
        if probs:
            fails += 1
            print(f"FAIL {sc['name']}: " + "; ".join(probs))
            print("---- rendered ----\n" + out + "\n------------------")
        else:
            print(f"PASS {sc['name']}")
    sys.exit(1 if fails else 0)

if __name__ == "__main__":
    main(*sys.argv[1:])
