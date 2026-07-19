#!/usr/bin/env python3
"""gen_expansions.py - Doc2Token expansion for the CURATED facts.

The last recall gap is vocabulary mismatch: a user asks "how do I turn columns
into rows", the fact says "melt() was renamed to unpivot()". Zero shared words,
so no keyword engine can bridge it. The literature's answer (doc2query /
SPLADE-doc / Walmart's Doc2Token - PRIOR-ART-RETRIEVAL.md) does the work OFFLINE:
predict the words a user would use, and index those. The runtime stays dumb.

Only CURATED facts get expansions: they answer "what changed", they are 388 of
2,345, and template bytes are rationed (F-048).

Uses the model already loaded in LM Studio (repo rule: each model extracts with
itself; never load/unload). Writes ONLY expansions.json - the bank is untouched.

ONE fact per call, run CONCURRENTLY. Batching 6 facts into one call failed: the
model's reasoning ate the token budget before it reached the answer
(finish_reason=length, nothing parseable) - the F-009/F-035 trap, again.

usage: python gen_expansions.py --model <loaded id> [--workers 4]
"""
import argparse, json, re, time, urllib.request
from concurrent.futures import ThreadPoolExecutor

# LM Studio SILENTLY DROPS chat_template_kwargs (F-018), and a model reload
# resets its thinking toggle back ON (F-035) - with thinking on, the model burns
# the whole token budget reasoning and returns EMPTY content (measured: 3 of 4
# calls came back with 900 tokens of nothing). llama-server honors the kwarg, so
# generation runs there with thinking OFF.
URL = "http://127.0.0.1:1234/v1/chat/completions"

PROMPT = """FACT: {fact}

Write 6 short questions a developer would type when they need this fact.
Use THEIR everyday words, not the API names. Imagine someone who does not know
the function name yet, and someone whose code just broke after an upgrade.
One question per line. No numbering, no preamble, nothing else."""


def ask(url, model, prompt, max_tokens=400):
    body = json.dumps({"model": model,
                       "messages": [{"role": "user", "content": prompt}],
                       "temperature": 0.7, "max_tokens": max_tokens,
                       "chat_template_kwargs": {"enable_thinking": False}}).encode()
    req = urllib.request.Request(url, data=body,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=900) as r:
        return json.loads(r.read())["choices"][0]["message"].get("content") or ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--facts", default="facts_pythondata_v4.jsonl")
    ap.add_argument("--out", required=True,   # NO default: a stale background job
                help="VERSION the filename. A shared default output path is what "
                     "clobbered 388 good expansions into 90 garbage ones.")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--url", default=URL)
    a = ap.parse_args()

    facts = [json.loads(l) for l in open(a.facts, encoding="utf-8") if l.strip()]
    curated = [f for f in facts if "api-" not in f["id"]]
    if a.limit:
        curated = curated[:a.limit]
    print(f"{len(curated)} curated facts | {a.workers} concurrent workers", flush=True)

    out, t0, done = {}, time.time(), [0]

    def one(f):
        try:
            resp = ask(a.url, a.model, PROMPT.format(fact=f["text"][:240]))
        except Exception:
            resp = ""
        qs = [re.sub(r"^[-*\d.)\s]+", "", l).strip().lower()
              for l in resp.strip().splitlines() if l.strip()]
        qs = [q for q in qs if 8 <= len(q) <= 90][:6]
        done[0] += 1
        if done[0] % 20 == 0:
            rate = (time.time() - t0) / done[0]
            print(f"  {done[0]}/{len(curated)} | eta "
                  f"{rate*(len(curated)-done[0])/60:.1f} min", flush=True)
        return f["id"], qs

    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        for fid, qs in ex.map(one, curated):
            if qs:
                out[fid] = qs

    json.dump(out, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    n = sum(len(v) for v in out.values())
    print(f"\n{len(out)}/{len(curated)} facts expanded, {n} questions -> {a.out} "
          f"({(time.time()-t0)/60:.1f} min)", flush=True)


if __name__ == "__main__":
    main()
