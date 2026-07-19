#!/usr/bin/env python3
"""appsec_merge.py - merge the 7 per-source appsec fact files into ONE bank and CROSS-SOURCE dedupe.

Per-source dedupe already ran (each adapter's C.run). This pass removes the SAME landmine restated by a
DIFFERENT source (e.g. SQL-injection in CWE + CodeQL + OWASP). Design:
  - CONSERVATIVE: the bank must stay RICH (serve all model sizes). Only collapse NEAR-IDENTICAL facts, not
    thematic siblings. Cross-source threshold 0.72 (stricter than the 0.60 within-source pass).
  - Two facts are duplicates if: same verbatim code_bad (gnorm), OR Jaccard(subject+truth tokens) >= 0.72.
  - Keep the BEST representative per cluster: has-code first (verbatim bad/good pair wins over a text
    restatement), then longer truth, then a stable source priority (codeql/sast carry the code).
  - Writes FINAL.jsonl (merged bank) + FINAL.removed.jsonl (every cut, with the id it duplicates) for audit.

usage:  python appsec_merge.py [--thresh 0.72]
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
FACTS = os.path.join(HERE, "experts", "appsec", "facts")
SOURCES = ["cwe", "codeql", "sast", "mastg", "rustsec", "crypto_net", "owasp_cs"]
# source priority when quality ties (code-bearing sources first)
PRIO = {"codeql": 0, "sast": 1, "cwe": 2, "mastg": 3, "owasp_cs": 4, "crypto_net": 5, "rustsec": 6}

def gnorm(s): return re.sub(r"\s+", " ", s or "").strip()
def toks(f): return set(re.findall(r"[a-z0-9]+", ((f.get("subject") or "") + " " + (f.get("truth") or "")).lower()))
def jac(a, b): return len(a & b) / max(1, len(a | b))

def quality(f):
    # higher is better: code-bearing, then longer truth, then source priority (lower PRIO = better)
    return (1 if f.get("code_bad") else 0, len(f.get("truth") or ""), -PRIO.get(f.get("_src"), 9))

def main():
    thresh = float(sys.argv[sys.argv.index("--thresh") + 1]) if "--thresh" in sys.argv else 0.72
    allf = []
    for s in SOURCES:
        p = os.path.join(FACTS, s + ".jsonl")
        for l in open(p, encoding="utf-8"):
            f = json.loads(l); f["_src"] = s; allf.append(f)
    print(f"loaded {len(allf)} facts from {len(SOURCES)} sources")

    # PROSE-ONLY dedupe. A shared code_bad is NOT a duplicate signal: sibling CodeQL queries legitimately
    # reuse one boilerplate sample to teach DIFFERENT lessons (servlet-throws vs password-in-GET on the same
    # doGet; block-__proto__ vs check-own-property on the same merge()). Only collapse when the LESSON
    # (subject+truth) is near-identical.
    if "--sweep" in sys.argv:
        order0 = sorted(range(len(allf)), key=lambda i: quality(allf[i]), reverse=True)
        for th in (0.80, 0.75, 0.72, 0.68, 0.65, 0.60):
            k, sig = 0, []
            for i in order0:
                ft = toks(allf[i])
                if any(jac(ft, kt) >= th for kt in sig):
                    continue
                sig.append(ft); k += 1
            print(f"  thresh {th:.2f} -> keep {k}, remove {len(allf)-k}")
        return

    # sort best-first so the representative we keep is the highest quality in its cluster
    order = sorted(range(len(allf)), key=lambda i: quality(allf[i]), reverse=True)
    kept, removed = [], []
    kept_sig = []   # (token_set, id) for each kept fact
    for i in order:
        f = allf[i]
        ft = toks(f)
        dup_of = None
        for (kt, kid) in kept_sig:
            if jac(ft, kt) >= thresh:             # near-identical LESSON (prose)
                dup_of = kid; break
        if dup_of:
            f["_dup_of"] = dup_of; removed.append(f)
        else:
            kept.append(f); kept_sig.append((ft, f["id"]))

    out = os.path.join(FACTS, "FINAL")
    with open(out + ".jsonl", "w", encoding="utf-8") as fh:
        for f in kept:
            f.pop("_src", None)
            fh.write(json.dumps(f, ensure_ascii=False) + "\n")
    with open(out + ".removed.jsonl", "w", encoding="utf-8") as fh:
        for f in removed:
            fh.write(json.dumps(f, ensure_ascii=False) + "\n")

    wc = sum(1 for f in kept if f.get("code_bad"))
    print(f"kept {len(kept)} ({wc} w/code) | removed {len(removed)} cross-source dups -> FINAL.jsonl")
    # per-source removal tally
    from collections import Counter
    print("removed by source:", dict(Counter(f["_src"] for f in removed)))

if __name__ == "__main__":
    main()
