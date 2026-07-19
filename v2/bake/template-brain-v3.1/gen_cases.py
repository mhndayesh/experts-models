#!/usr/bin/env python3
"""gen_cases.py - a dense eval set with EXACT ground truth and REALISTIC questions.

Two halves, and they must not be confused:

  GROUND TRUTH is extracted from the fact, never invented:
      "np.row_stack was deprecated in NumPy 2.0 - use np.vstack instead."
         dead    = np.row_stack   (must NOT appear in the answer's code)
         correct = np.vstack      (must appear)

  THE QUESTION is written by the model, in a real developer's voice - because a
  templated "show me code that uses np.row_stack" tests a strawman. Real people paste
  broken code, or describe a task and never name an API at all. The generator is
  FORBIDDEN from naming the replacement: that would leak the answer into the question.

A case only counts if the BARE model gets it wrong (F-028). eval_dense.py certifies that.
"""
import json, re, sys, urllib.request

FACTS = "facts_pythondata_v4.jsonl"
OUT = "cases_dense.json"
URL = "http://127.0.0.1:1234/v1/chat/completions"
MODEL = "google/gemma-4-12b-qat"          # EXACTLY the id the owner loaded

# "X was REMOVED in NumPy 2.0 - use Y instead."   "X is deprecated ... - use Y"
# NOTE: an earlier version used [^.]* here, which was a BUG - every fact contains
# "NumPy 2.0", so the dot ended the match and only 16/177 facts extracted.
TOK = r"[`\"]?([A-Za-z_][\w.]*)(?:\(\))?[`\"]?"

# Three explicit patterns beat one clever one. An earlier single regex consumed the word
# "renamed" and then needed it again, so every polars rename (melt -> unpivot) was missed.
P_RENAME = re.compile(TOK + r"\s+(?:was|were)\s+renamed\s+to\s+" + TOK, re.S)
P_REPLACED = re.compile(TOK + r"\s+(?:was|were)\s+replaced\s+by\s+" + TOK, re.S)
P_USE = re.compile(
    TOK + r"\s+(?:was|were|is|are)\s+(?:REMOVED|removed|deprecated|renamed|no longer)"
    r".{0,110}?[-–]\s+use\s+(.{0,70}?)(?:\s+instead|,|\.\s|$)", re.S)
# quoted aliases: 'The frequency alias `"M"` was REMOVED in pandas 3.0 - use `"ME"`'
QPAT = re.compile(
    r"`?\"([A-Za-z]{1,4})\"`?\s+(?:was|were|is|are)\s+(?:REMOVED|removed|deprecated|renamed)"
    r".{0,110}?[-–]\s+use\s+`?\"([A-Za-z]{1,4})\"`?", re.S)

FILLER = {"the", "a", "an", "plain", "lowercase", "literals", "literal", "and", "its",
          "explicit", "new", "modern", "your", "own", "it", "them", "either", "both",
          "function", "argument", "parameter", "keyword", "method", "attribute", "module"}


LIB = {"numpy": "NumPy", "pandas": "pandas", "polars": "polars", "scipy": "SciPy",
       "sklearn": "scikit-learn", "matplotlib": "matplotlib", "pyarrow": "PyArrow",
       "duckdb": "DuckDB", "xarray": "xarray", "statsmodels": "statsmodels"}


def clean(t):
    return t.strip("`\"()").split("(")[0]


def first_api(blob):
    """first real identifier after 'use' - skip filler ('use the lowercase np.nan')"""
    for tok in re.findall(r"[`\"]?([A-Za-z_][\w.]*)[`\"]?", blob or ""):
        if tok.lower() in FILLER:
            continue
        return tok
    return None


def is_apiish(tok):
    """a replacement must look like an API, not an English word ('use your own print')"""
    return "." in tok or "_" in tok or any(c.isupper() for c in tok[1:]) or len(tok) >= 6


def ask(prompt, n=260):
    body = json.dumps({"model": MODEL, "max_tokens": n, "temperature": 0.7,
                       "messages": [{"role": "user", "content": prompt}]}).encode()
    req = urllib.request.Request(URL, body, {"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=180) as r:
        return json.load(r)["choices"][0]["message"]["content"]


GEN = """You are helping build a test set. Here is a documentation fact:

  {fact}

Write TWO questions a real developer would actually type, about this situation.

Rules:
- Question 1 (BROKEN CODE): they hit this in real life. They paste a snippet or an error
  and ask what to do. Casual, lowercase is fine, may be slightly messy.
- Question 2 (TASK): they describe what they are TRYING TO DO, in plain words, and ask
  for code. This one must NOT name any API at all - no function names.
- NEVER mention "{good}" in either question. That is the answer; naming it leaks it.
- No preamble. Output exactly two lines:
1. <question>
2. <question>"""


def main():
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else 60
    rows = [json.loads(l) for l in open(FACTS, encoding="utf-8") if l.strip()]
    curated = [r for r in rows if "api-" not in r["id"]]

    seeds = []
    for r in curated:
        qm = QPAT.search(r["text"])
        if qm and qm.group(1) != qm.group(2):
            seeds.append((r, '"%s"' % qm.group(1), '"%s"' % qm.group(2)))
            continue
        dead = good = None
        for P in (P_RENAME, P_REPLACED):
            m = P.search(r["text"])
            if m:
                dead, good = clean(m.group(1)), clean(m.group(2))
                break
        if not dead:
            m = P_USE.search(r["text"])
            if not m:
                continue
            dead, good = clean(m.group(1)), first_api(m.group(2))
            good = clean(good) if good else None
        if not dead or not good:
            continue
        # BOTH sides must look like an API. Without this, "the `axis` argument was REMOVED
        # - use ..." yields dead="argument", and the case is nonsense.
        if (dead.lower() in FILLER or good.lower() in FILLER
                or not is_apiish(dead) or not is_apiish(good)):
            continue
        if dead == good or len(dead) < 3 or len(good) < 3:
            continue
        if good in dead or dead in good:      # np.round_ -> np.round: substring scoring lies
            continue
        # REJECT multi-name facts. "np.NINF and np.PINF were REMOVED - use -np.inf and
        # np.inf" yields dead=np.PINF while the question asks about np.NINF: ground truth
        # would be wrong and the case would score nonsense.
        head = r["text"].split(" was ")[0].split(" were ")[0]
        if " and " in head or "," in head:
            continue
        seeds.append((r, dead, good))

    # STRATIFY: seeds arrive in file order, which is numpy-first. Taking the first N gave
    # 80 numpy cases and 10 pandas. Round-robin across libraries instead.
    by_lib = {}
    for s_ in seeds:
        by_lib.setdefault(s_[0].get("source", "?"), []).append(s_)
    mixed = []
    while any(by_lib.values()):
        for lib in sorted(by_lib):
            if by_lib[lib]:
                mixed.append(by_lib[lib].pop(0))
    seeds = mixed
    print(f"{len(seeds)} facts have a clean, SINGLE-name dead->replacement mapping")
    print("  by library:", {k: sum(1 for x in seeds if x[0].get("source") == k)
                            for k in sorted({x[0].get("source") for x in seeds})})

    cases = []
    for i, (r, dead, good) in enumerate(seeds[:limit]):
        lib = LIB.get(r.get("source", ""), r.get("source", ""))
        try:
            out = ask(GEN.format(fact=r["text"], good=good))
        except Exception as e:
            print(f"  [{i}] generation failed: {e}")
            continue
        qs = [re.sub(r"^\s*\d[.)]\s*", "", l).strip()
              for l in out.strip().splitlines() if re.match(r"^\s*\d[.)]", l)]
        if len(qs) < 2:
            continue
        for tier, q in (("broken", qs[0]), ("task", qs[1])):
            if good.lower() in q.lower():          # the generator leaked the answer
                continue
            cases.append({"id": f"{r['id']}-{tier}", "fact": r["id"], "tier": tier,
                          "lib": lib, "version": r.get("version", ""),
                          "q": q, "correct": [good], "dead": [dead],
                          "fact_text": r["text"][:120]})
        if (i + 1) % 10 == 0:
            print(f"  {i+1}/{min(limit, len(seeds))} facts -> {len(cases)} questions")

    json.dump(cases, open(OUT, "w", encoding="utf-8"), indent=1)
    print(f"\nwrote {len(cases)} cases -> {OUT}")
    for c in cases[:6]:
        print(f"\n  [{c['tier']:6}] {c['q'][:96]}")
        print(f"           must use {c['correct']}  must NOT use {c['dead']}")


if __name__ == "__main__":
    main()
