#!/usr/bin/env python3
"""eval_dense.py - COLLECT the answers. It does NOT score them.

  THIS SCRIPT PRODUCES NO VERDICTS, ON PURPOSE.

The repo's standing rule (owner, 2026-07-14, F-065): **score MANUALLY. Always.**
Read the question, the facts retrieved, and the model's full answer, and judge
each one yourself. Never report a number that came out of an automated scorer.

That rule was bought, not preferred. On THIS eval, three successive automated
scorers each produced a different, wrong answer from the same saved transcripts:

  1. Scanned EVERY code fence -> flagged the model's "# Old code (broken)"
     snippet as a dead-API failure. A CORRECT migration answer scored DEAD.
  2. Matched the ground truth as a literal substring -> `Series.value_counts`
     never appears in real code (`df["x"].value_counts()`), so correct answers
     scored MISS.
  3. Even "last fence only" (F-020's wrong_scope="last") failed, because the
     before/after snippet sits INSIDE ONE FENCE. Fixing that changed 33 of ~117
     verdicts and REVERSED the run's conclusion.

Reading the answers by hand then revealed what no scorer could have: two thirds
of the cases were unmeasurable (the bare model already knew them), several
questions had drifted off the fact they were built from, and one arm answered a
NumPy question in TypeScript. `rescore_dense.py` - the third scorer - has been
DELETED rather than fixed, because a fourth version would have been wrong too.

So this script's whole job is to produce a transcript you can READ:

    python eval_dense.py            # -> eval_dense_results.jsonl (full answers)
    python dump_for_review.py       # -> _manual.txt  (question / truth / 3 answers)
    # ...then read _manual.txt and score it yourself.

THREE ARMS, one variable (the template). Same model, same decoding, same question.

  bare     the STOCK gemma template. No bank. The control, and the PROBE.
  shipped  baked_index_v6.jinja   - what is live today
  rescue   rescue_v7.jinja        - the candidate

PROBE-CERTIFICATION (F-028). A case only measures the bank if the BARE model
cannot already answer it. "The baseline scores 0 on the measurable cases" is a
TAUTOLOGY if you pick the cases after seeing the baseline. Every case is run bare
too, so you can separate the decisive cases from the ones that prove nothing.
On the 2026-07-14 run that was 25 decisive out of 76 - two thirds of the set
could not measure the bank at all.

TRUNCATION is recorded, never hidden (F-009): a budget failure must not be read
as an architecture failure. `finish_reason == "length"` is saved per answer, and
on the 2026-07-14 run **bare truncated on 43 of 76** - any scorer that silently
folds those into "MISS" is lying about the baseline. It did.
"""
import json
import sys
import time
import urllib.request

import jinja2

URL = "http://127.0.0.1:1234/v1/completions"
MODEL = "google/gemma-4-12b-qat"       # EXACTLY the id the owner loaded. Never another.
CASES = "cases_dense.json"
OUT = "eval_dense_results.jsonl"

ARMS = [("bare", "family_bases/gemma4.source.jinja"),
        ("shipped", "baked_index_v6.jinja"),
        ("rescue", "rescue_v7.jinja")]

_C = {}


def render(path, q):
    if path not in _C:
        src = open(path, encoding="utf-8").read()
        _C[path] = jinja2.Environment(undefined=jinja2.Undefined).from_string(src)
    return _C[path].render(messages=[{"role": "user", "content": q}],
                           add_generation_prompt=True)


def ask(prompt, n=600):
    body = json.dumps({"model": MODEL, "prompt": prompt, "max_tokens": n,
                       "temperature": 0.2,
                       "stop": ["<turn|>", "<|endoftext|>"]}).encode()
    req = urllib.request.Request(URL, body, {"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=600) as r:
        d = json.load(r)
    ch = d["choices"][0]
    return ch["text"], ch.get("finish_reason", "")


def main():
    cases = json.load(open(CASES, encoding="utf-8"))
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else len(cases)
    cases = cases[:limit]
    print(f"{len(cases)} cases | model {MODEL} | arms: {[a for a, _ in ARMS]}")
    print("collecting answers. NOT scoring them - that is done by hand.\n")

    out = open(OUT, "w", encoding="utf-8")
    trunc = {a: 0 for a, _ in ARMS}
    t0 = time.time()

    for i, c in enumerate(cases):
        row = {"id": c["id"], "tier": c["tier"], "lib": c["lib"], "q": c["q"],
               "correct": c["correct"], "dead": c["dead"]}
        for arm, tpl in ARMS:
            try:
                ans, fin = ask(render(tpl, c["q"]))
            except Exception as e:
                row[arm + "_answer"] = None
                row[arm + "_err"] = str(e)[:160]
                continue
            # THE FULL ANSWER, always. A run writes every answer so it can be
            # re-read for free, forever, without spending GPU again. The first
            # version of this eval saved only a 180-char code snippet - so when
            # the scorer turned out to be wrong, the entire run was worthless.
            row[arm + "_answer"] = ans
            row[arm + "_finish"] = fin
            trunc[arm] += (fin == "length")
        out.write(json.dumps(row) + "\n")
        out.flush()
        if (i + 1) % 10 == 0:
            el = time.time() - t0
            print(f"  {i+1}/{len(cases)}  ({el:.0f}s, {el/(i+1):.1f}s/case)", flush=True)
    out.close()

    print("\n" + "=" * 72)
    print(f"{len(cases)} cases collected -> {OUT}")
    print("\ntruncated (finish_reason == 'length') - a BUDGET failure, not a bank "
          "failure (F-009):")
    for a, _ in ARMS:
        print(f"  {a:9} {trunc[a]:>3}/{len(cases)}")
    print("\n" + "=" * 72)
    print("NO SCORES PRINTED. That is deliberate - see this file's docstring.")
    print("Next:  python dump_for_review.py    then READ _manual.txt and judge it.")


if __name__ == "__main__":
    main()
