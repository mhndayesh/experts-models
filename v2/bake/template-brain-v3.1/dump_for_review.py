#!/usr/bin/env python3
"""dump_for_review.py - lay a saved run out so a human can SCORE IT BY HAND.

This is the other half of the repo's scoring rule (F-065): eval_dense.py collects
answers and refuses to judge them; this prints them in the one shape that makes
judging them cheap - question, ground truth, then each arm's FULL answer, side by
side, in reading order.

    python eval_dense.py           # -> eval_dense_results.jsonl
    python dump_for_review.py      # -> _manual.txt
    # now READ _manual.txt.

Costs nothing and touches no GPU: it reads the saved transcript. You can re-read a
run from six months ago for free, which is exactly why every run saves full answers.

WHAT TO ASK OF EACH ANSWER (this is the checklist that produced F-065):

  * Judge it against THE QUESTION THAT WAS ASKED, not against `correct`. The
    ground-truth token is a hint, not the answer key. A flawed question can still
    have a right answer - and several of these questions had drifted off the fact
    they were generated from. On one case the ground truth was
    `np.char.compare_chararrays` and the BEST answer was plain `arr1 == arr2`.

  * Does the CODE obey, or only the prose? A model can name the right API in a
    sentence and then write the dead one in the fence. Both matter; they are
    different questions (USES vs CODE), and the gap between them IS the finding.

  * On a migration answer the model shows the BROKEN code first and the fix
    second, often inside ONE fence. Score what it RECOMMENDS - the last usage.
    Three automated scorers died on exactly this.

  * finish=length means TRUNCATED. That is a budget failure, not an architecture
    failure (F-009). Do not score it as a miss - note it and move on.

  * If every arm gets it right, the case is UNMEASURABLE - the bare model already
    knew it, so it says nothing about the bank (F-028). Count those separately.
    On the 2026-07-14 run that was 51 of 76 cases.
"""
import json
import sys

IN = sys.argv[1] if len(sys.argv) > 1 else "eval_dense_results.jsonl"
OUT = sys.argv[2] if len(sys.argv) > 2 else "_manual.txt"
ARMS = ("bare", "shipped", "rescue")


def main():
    rows = [json.loads(l) for l in open(IN, encoding="utf-8")]
    with open(OUT, "w", encoding="utf-8") as f:
        for i, r in enumerate(rows, 1):
            f.write("=" * 100 + "\n")
            f.write(f"CASE {i}/{len(rows)}  [{r['tier']}/{r['lib']}]  {r['id']}\n")
            f.write(f"Q: {r['q']}\n")
            f.write(f"GROUND TRUTH (a hint, not the answer key)  "
                    f"correct={r['correct']}  dead={r['dead']}\n")
            for a in ARMS:
                ans = r.get(a + "_answer")
                fin = r.get(a + "_finish", "")
                flag = "  << TRUNCATED (budget failure, not a bank failure)" \
                       if fin == "length" else ""
                f.write(f"\n--- {a.upper()} (finish={fin}){flag} ---\n")
                f.write((ans or "(no answer / error)").strip() + "\n")
            f.write("\n")
    print(f"{len(rows)} cases -> {OUT}")
    print("\nNow READ it. Do not write a scorer. Nine of them have been wrong in this repo\n"
          "(F-007, F-016, F-020, F-021, F-026, F-029, F-064, and three in a row on this\n"
          "very eval - F-065).")


if __name__ == "__main__":
    main()
