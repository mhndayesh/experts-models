#!/usr/bin/env python3
"""live_obey.py - the question every offline number cannot answer:
the fact now REACHES the model. Does the model OBEY it?

Reachability measures delivery. This measures use. The gap between them is where
this project has historically hidden its failures (the USES/CODE gap).

METHOD - no extra VRAM, no second model load:
  The chat template's only job is to build a prompt. So we render it in Python
  (jinja2) and POST the resulting prompt to /v1/completions on the model the OWNER
  already loaded. The model sees the exact bytes the baked GGUF would give it.

  arm "bare"   : the STOCK gemma template - no bank. The control.
  arm "rescue" : our candidate - bank + index + rescue gate.

Same question, same model, same decoding. The only variable is the template.

SCORING is structural, never prose: we look only inside ``` fences, and we ask
what the code CALLS. A fact "mentioned" in a sentence is not obedience (F-029).
"""
import json, re, sys, urllib.request

import jinja2

URL = "http://127.0.0.1:1234/v1/completions"
MODEL = "google/gemma-4-12b-qat"          # EXACTLY the id the owner loaded. Never another.

CASES = [
    # question, correct API (must appear in code), dead API (must NOT appear in code)
    ("Using polars 1.x, reshape a wide DataFrame into long format. Show the code.",
     ["unpivot"], ["melt"]),
    ("In pandas 3.0, resample a DataFrame monthly. Show the code.",
     ['"ME"', "'ME'"], ['"M"', "'M'"]),
    ("In NumPy 2.0, convert an array to a specific dtype using np.cast. Show the code.",
     ["asarray", "astype"], ["np.cast", "cast("]),
    ("I need to safely evaluate a string literal with numpy. Show the code.",
     ["literal_eval"], ["safe_eval"]),
    ("In NumPy 2.x, stack arrays as rows using np.row_stack. Show the code.",
     ["vstack"], ["row_stack"]),
    ("In pandas 3.0, get the first 3 days of a time series with DataFrame.first(). Show the code.",
     ["loc", "head", "iloc"], [".first("]),
    ("In pandas 3.0, set values on a filtered column: df['foo'][df['bar'] > 5] = 100. Fix it.",
     [".loc["], None),      # dead pattern checked separately
    ("In NumPy 2.4, round an array in place with np.round and reuse the view. Show the code.",
     ["round"], ["np.round_"]),
]
CONTROLS = ["write a haiku about the sea", "what is the capital of France?"]


def render(tpl_path, q):
    src = open(tpl_path, encoding="utf-8").read()
    env = jinja2.Environment(undefined=jinja2.Undefined)
    return env.from_string(src).render(
        messages=[{"role": "user", "content": q}], add_generation_prompt=True)


def ask(prompt, n=520):
    body = json.dumps({"model": MODEL, "prompt": prompt, "max_tokens": n,
                       "temperature": 0.2, "stop": ["<turn|>", "<|endoftext|>"]}).encode()
    req = urllib.request.Request(URL, body, {"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as r:
        d = json.load(r)
    return d["choices"][0]["text"]


def code_of(answer):
    """only what is INSIDE fences. Prose and comments are not obedience (F-029)."""
    fences = re.findall(r"```[a-zA-Z]*\n(.*?)```", answer, re.S)
    if not fences:
        return ""
    body = "\n".join(fences)
    body = re.sub(r"#.*", "", body)                  # strip comments
    return body


def judge(answer, good, bad):
    code = code_of(answer)
    if not code:
        return "NO CODE"
    used_bad = bad and any(b in code for b in bad)
    used_good = good and any(g in code for g in good)
    if used_bad:
        return "DEAD API"
    return "OK" if used_good else "MISS"


def main():
    arms = [("bare  ", "family_bases/gemma4.source.jinja"),
            ("rescue", "_rescue.jinja")]
    score = {a: 0 for a, _ in arms}
    print(f"model: {MODEL}   (stock weights - any correct post-cutoff answer MUST come "
          f"from the bank)\n")
    for q, good, bad in CASES:
        print("=" * 78)
        print("Q:", q[:72])
        for name, tpl in arms:
            try:
                ans = ask(render(tpl, q))
            except Exception as e:
                print(f"   {name}  ERROR {e}")
                continue
            v = judge(ans, good, bad)
            score[name] += (v == "OK")
            snip = " ".join(code_of(ans).split())[:64] or " ".join(ans.split())[:64]
            print(f"   {name}  {v:8}  {snip}")
    print("=" * 78)
    for name, _ in arms:
        print(f"  {name}  {score[name]}/{len(CASES)} obeyed")
    print()
    for q in CONTROLS:
        ans = ask(render("_rescue.jinja", q))
        leaked = any(w in ans.lower() for w in ("pandas", "polars", "numpy", "dtype"))
        print(f"  CONTROL {'LEAKED FACTS' if leaked else 'clean'}: {q[:34]!r} -> "
              f"{' '.join(ans.split())[:52]}")


if __name__ == "__main__":
    main()
