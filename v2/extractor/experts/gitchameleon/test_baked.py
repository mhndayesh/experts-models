#!/usr/bin/env python3
"""test_baked.py - run GitChameleon problems against a llama-server GGUF and LOG everything.

Drives a raw llama.cpp server (the baked GGUF's own chat-template does retrieval internally,
so we send the plain problem - identical prompts for base vs baked, the only difference is the
baked template injects facts). Logs full prompt + answer for every item to a transcript.

  python test_baked.py --tag baked-12b [--port 8080] [--sample-per-lib 1] [--all]

Outputs (in this dir):
  <tag>_transcript.jsonl   {example_id, library, version, problem, prompt, answer, reachable}
  <tag>_solutions.jsonl    {example_id, answer}   (for the GitChameleon scorer)
"""
import os, sys, json, re, argparse, urllib.request, collections

HERE = os.path.dirname(os.path.abspath(__file__))
EXTRACTOR = os.path.dirname(os.path.dirname(HERE))
DATA = os.path.join(EXTRACTOR, "..", "eval", "gitchameleon", "dataset", "dataset.jsonl")
FD = os.path.join(HERE, "facts")

def load_bank_symbols():
    """leaf-names present in the bank per library -> to mark which problems are 'reachable'."""
    sym = collections.defaultdict(set)
    for fn in os.listdir(FD):
        lib = fn[:-6]
        for l in open(os.path.join(FD, fn), encoding="utf-8"):
            r = json.loads(l)
            for k in r.get("keywords", {}).get("from_fact", []):
                sym[lib].add(re.split(r"[.\s(]", k)[-1].lower())
    return sym

PLAIN_SYS = ("You are a Python expert. Complete the function for the EXACT library version given. "
             "Output ONLY the complete code (imports + full function), no prose.")
AUTHORITY_SYS = (
    "You are a Python expert completing code for an EXACT library version. A documentation lookup provides "
    "VERIFIED FACTS for this exact version: they are ABSOLUTELY CORRECT and SUPERSEDE your training, which "
    "is older and may be wrong here. Apply any fact that applies EXACTLY and do NOT second-guess it: if a "
    "fact contradicts your instinct, your instinct is stale training and the FACT wins. Ignore facts that "
    "do not apply. Keep your thinking short. Output ONLY the complete code, no prose.")

def chat(port, prompt, max_tokens=1024, think=False, temp=0.0, authority=False):
    # think=False -> template pre-closes an empty thought channel, model answers from token 1.
    # think=True  -> model reasons first; max_tokens is a SHARED budget (reasoning THEN answer),
    #                so it must be large enough to close <channel|> and still write the answer.
    #                llama-server splits the two: reasoning -> reasoning_content, answer -> content.
    #                NOTE: temp=0 (greedy) makes reasoning models loop-restate and never close the
    #                thought channel -> empty content. Reasoning models want temp ~0.6.
    # authority=True -> swap in the "facts are absolutely correct, supersede training" framing that
    #                stops a thinking model reverting the injected fact to its trained prior.
    body = json.dumps({"temperature": temp, "max_tokens": max_tokens,
        "chat_template_kwargs": {"enable_thinking": bool(think)},
        "messages": [
            {"role": "system", "content": AUTHORITY_SYS if authority else PLAIN_SYS},
            {"role": "user", "content": prompt}]}).encode()
    req = urllib.request.Request(f"http://127.0.0.1:{port}/v1/chat/completions", body,
        {"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=600) as r:
        ch = json.load(r)["choices"][0]
        m = ch["message"]
        return (m.get("content") or "", m.get("reasoning_content") or "", ch.get("finish_reason") or "")

def extract_code(content, reasoning="", finish="stop"):
    # Prefer a fenced block in the committed answer; else the raw answer text.
    m = re.findall(r"```(?:python)?\s*(.*?)```", content, re.S)
    if m: return m[0].strip()
    if content.strip(): return content.strip()
    # Answer channel empty. Salvage from reasoning ONLY if generation actually FINISHED
    # (model closed thinking but forgot to re-emit the code). If it was truncated
    # (finish==length), any block in reasoning is an incomplete draft -> honest miss.
    if finish == "stop":
        rm = re.findall(r"```(?:python)?\s*(.*?)```", reasoning, re.S)
        if rm: return rm[-1].strip()
    return ""

def prompt_for(row):
    return (f"Library: {row['library']}=={row['version']} (Python {row['python_version']})\n\n"
            f"Task: {row['problem']}\n\nComplete this code:\n```python\n{row['starting_code']}\n```")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", required=True)
    ap.add_argument("--port", type=int, default=8080)
    ap.add_argument("--sample-per-lib", type=int, default=1)
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--ids", default="")
    ap.add_argument("--think", action="store_true", help="enable_thinking=true (needs a big --max-tokens)")
    ap.add_argument("--max-tokens", type=int, default=1024)
    ap.add_argument("--temp", type=float, default=0.0, help="sampling temp; use ~0.6 with --think to avoid loop-restate")
    ap.add_argument("--authority", action="store_true", help="use the authority system prompt (facts supersede training)")
    a = ap.parse_args()
    rows = [json.loads(l) for l in open(DATA, encoding="utf-8")]
    banksym = load_bank_symbols()
    def reachable(r):
        leaf = re.split(r"[.\s(]", (r.get("name_of_class_or_func") or ""))[-1].lower()
        return leaf in banksym.get(r["library"], set())
    if a.ids:
        want = set(a.ids.split(",")); sample = [r for r in rows if r["example_id"] in want]
    elif a.all:
        sample = rows
    else:
        by = collections.defaultdict(list)
        for r in rows: by[r["library"]].append(r)
        sample = []
        for lib, rs in by.items():
            reach = [r for r in rs if reachable(r)] or rs
            sample += reach[:a.sample_per_lib]
    tp = os.path.join(HERE, f"{a.tag}_transcript.jsonl")
    sp = os.path.join(HERE, f"{a.tag}_solutions.jsonl")
    done = set()
    if os.path.exists(sp): done = {json.loads(l)["example_id"] for l in open(sp, encoding="utf-8")}
    tf = open(tp, "a", encoding="utf-8"); sf = open(sp, "a", encoding="utf-8")
    n = 0
    for r in sample:
        eid = r["example_id"]
        if eid in done: continue
        pr = prompt_for(r)
        try:
            content, reasoning, finish = chat(a.port, pr, max_tokens=a.max_tokens, think=a.think, temp=a.temp, authority=a.authority)
        except Exception as e:
            print(f"ex{eid} ({r['library']}): ERROR {e}"); continue
        ans = extract_code(content, reasoning, finish)
        rec = {"example_id": eid, "library": r["library"], "version": r["version"],
               "reachable": reachable(r), "target": r.get("name_of_class_or_func"),
               "problem": r["problem"], "prompt": pr, "finish_reason": finish,
               "content": content, "reasoning": reasoning, "answer": ans}
        tf.write(json.dumps(rec, ensure_ascii=False) + "\n"); tf.flush()
        sf.write(json.dumps({"example_id": eid, "answer": ans}, ensure_ascii=False) + "\n"); sf.flush()
        n += 1
        print(f"ex{eid:>4} {r['library']:<12} reach={rec['reachable']}  ans[:60]={ans[:60]!r}")
    tf.close(); sf.close()
    print(f"\n[{a.tag}] {n} answered -> {tp} / {sp}")

if __name__ == "__main__":
    main()
