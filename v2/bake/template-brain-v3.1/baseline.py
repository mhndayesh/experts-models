#!/usr/bin/env python3
"""baseline.py - the regression contract. Run this BEFORE and AFTER every change.

The shipped model is good (gold 12/12, controls 0/10). This locks that in as a
contract: nothing merges that regresses any line below.

Everything here is OFFLINE and FREE - jinja2 render only, no GPU, no models, no
llama-server. (The engine-parity gate is separate: `parity.py`, which spawns
llama-server and therefore costs VRAM.)

usage:
    python baseline.py                       # score the shipped template
    python baseline.py other.jinja           # score a candidate
    python baseline.py other.jinja --json    # machine-readable, for CI
"""
import argparse, hashlib, json, os, sys

import jinja2

SHIPPED = "baked_index_v6.jinja"
BANK = "facts_pythondata_v4.jsonl"
GOLD = "jinja_lab/gold.json"
SIZE_CAP = 980_000                      # bake_index.py --max-bytes default; the LM Studio
                                        # metadata ceiling (F-053). Docs quote it as "957 KB"
                                        # — that is 980_000 bytes in KiB, not 957_000.
FORGE = "<|tool_call>call:factbank_search"


def load_bank():
    """id -> fact text, so a rendered line can be mapped back to a fact id."""
    by_id, by_text = {}, {}
    with open(BANK, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            if "id" not in r or "text" not in r:
                continue
            by_id[r["id"]] = r["text"]
            by_text[r["text"][:80].strip()] = r["id"]
    return by_id, by_text


_COMPILED = {}


def compile_tpl(tpl):
    """Parse the template ONCE.

    jinja2 re-parses the whole ~1 MB source on every from_string() call, and the
    parse - not the render - is the entire cost. reach.py renders ~2,300 times per
    variant; compiling per render made that 2,300 full parses of a megabyte.
    """
    key = hash(tpl)
    if key not in _COMPILED:
        env = jinja2.Environment(undefined=jinja2.Undefined)
        _COMPILED[key] = env.from_string(tpl)
    return _COMPILED[key]


def render(tpl, question):
    return compile_tpl(tpl).render(
        messages=[{"role": "user", "content": question}],
        add_generation_prompt=True,
    )


def facts_injected(prompt, by_text):
    """the fact ids the template actually put in front of the model"""
    if FORGE not in prompt:
        return []
    block = prompt.split(FORGE, 1)[1]
    ids = []
    for line in block.splitlines():
        s = line.strip()
        if not s.startswith("- "):
            continue
        text = s[2:].strip()
        hit = by_text.get(text[:80].strip())
        if hit is None:                          # fall back to prefix match
            for t, i in by_text.items():
                if text.startswith(t[:50]) or t.startswith(text[:50]):
                    hit = i
                    break
        ids.append(hit or f"?{text[:40]}")
    return ids


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("template", nargs="?", default=SHIPPED)
    ap.add_argument("--json", action="store_true")
    # The size ceiling is a property of the SHIPPING ROUTE, not of the template
    # (F-059). Only LM Studio's GGUF-metadata reader caps it - and it does so
    # SILENTLY, swapping the template for a 48-char sentinel. llama.cpp caps at
    # 1 GiB and errors loudly; LM Studio's Hub `model.yaml` load path has no cap
    # at all (proven live at 1.5 MB and 2.0 MB).
    ap.add_argument("--route", choices=["rawgguf", "llamacpp", "hub"], default="rawgguf",
                    help="rawgguf = LM Studio loading the .gguf by hand (957 KB cap); "
                         "llamacpp / hub = no practical cap")
    a = ap.parse_args()

    tpl = open(a.template, encoding="utf-8").read()
    by_id, by_text = load_bank()
    gold = json.load(open(GOLD, encoding="utf-8"))

    # --- gold: did the right fact win a slot? ---
    hits, misses = 0, []
    for c in gold["cases"]:
        got = facts_injected(render(tpl, c["q"]), by_text)
        if c["gold"] in got:
            hits += 1
        else:
            misses.append({"q": c["q"][:60], "want": c["gold"],
                           "got": got[:5], "why": c.get("why", "")})

    # --- controls: the loop must drag NOTHING in ---
    fires = []
    for q in gold["controls"]:
        got = facts_injected(render(tpl, q), by_text)
        if got:
            fires.append({"q": q, "got": got})

    size = len(tpl.encode("utf-8"))
    sha = hashlib.sha256(tpl.encode("utf-8")).hexdigest()[:16]
    cap = SIZE_CAP if a.route == "rawgguf" else 1_000_000_000

    contract = {
        "template": a.template,
        "sha256_16": sha,
        "bytes": size,
        "gold": f"{hits}/{len(gold['cases'])}",
        "gold_ok": hits == len(gold["cases"]),
        "controls_fired": f"{len(fires)}/{len(gold['controls'])}",
        "controls_ok": len(fires) == 0,
        "size_ok": size < cap,
        "route": a.route,
        "facts_in_bank": len(by_id),
    }
    contract["PASS"] = all([contract["gold_ok"], contract["controls_ok"], contract["size_ok"]])

    if a.json:
        print(json.dumps(contract, indent=1))
        return 0 if contract["PASS"] else 1

    print(f"template   {a.template}  ({size:,} bytes, sha {sha})")
    print(f"bank       {len(by_id):,} facts")
    print()
    print(f"  gold           {contract['gold']}        {'OK' if contract['gold_ok'] else 'REGRESSED'}")
    print(f"  controls fired {contract['controls_fired']}        {'OK' if contract['controls_ok'] else 'FACT-SLAVERY'}")
    limit = f"< {cap:,}" if a.route == "rawgguf" else "no practical cap"
    print(f"  size {limit:16} {size:,}   "
          f"{'OK' if contract['size_ok'] else 'OVER THE LM STUDIO RAW-GGUF CEILING'}  [route: {a.route}]")
    print()
    if misses:
        print("  MISSED:")
        for m in misses:
            print(f"    want {m['want']:<14} got {m['got']}")
            print(f"      q: {m['q']}")
            if m["why"]:
                print(f"      why it matters: {m['why'][:80]}")
    if fires:
        print("  CONTROL FIRES (must be zero):")
        for f in fires:
            print(f"    {f['q'][:50]!r} -> {f['got']}")
    print()
    print("  RESULT:", "PASS" if contract["PASS"] else "FAIL")
    print()
    print("  not covered here (needs llama-server, costs VRAM): parity.py, lint.py")
    return 0 if contract["PASS"] else 1


if __name__ == "__main__":
    sys.exit(main())
