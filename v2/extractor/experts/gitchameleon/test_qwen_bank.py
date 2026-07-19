#!/usr/bin/env python3
"""test_qwen_bank.py - Qwen3-4B-Thinking + the GitChameleon bank via RETRIEVAL + AUTHORITY-prompt.

Thinking is forced ON (Qwen3-Thinking has no off switch). We counter the two failure modes we found:
  - reversion to trained priors  -> AUTHORITY framing ("facts are absolutely correct, supersede training")
  - loop/empty (reasoning spiral) -> BREVITY instruction ("think briefly, then output code")
Facts are retrieved per problem with the SAME recipe that survived testing (soft doors + pointers + MMR,
lookup.retrieve) from the SAME bank the baked models used, and injected into the system prompt.

  python test_qwen_bank.py --tag qwen-bank --all            # full 328
  python test_qwen_bank.py --tag qwen-bank --sample-per-lib 1
  python test_qwen_bank.py --tag qwen-bank --ids 238,239,56 --k 5
Outputs: <tag>_transcript.jsonl, <tag>_solutions.jsonl
"""
import os, sys, json, re, argparse, urllib.request, collections

HERE = os.path.dirname(os.path.abspath(__file__))
EXTRACTOR = os.path.dirname(os.path.dirname(HERE))
DATA = os.path.join(EXTRACTOR, "..", "eval", "gitchameleon", "dataset", "dataset.jsonl")
os.environ["BANK_DIR"] = os.path.join(HERE, "facts")     # the GitChameleon bank (23 doors, 4167 facts)
sys.path.insert(0, EXTRACTOR)
import lookup                                             # retrieve() + FACTS

AUTHORITY = (
    "You are completing Python code for an EXACT library version. The VERIFIED FACTS below were extracted "
    "from the official changelog and are ABSOLUTELY CORRECT for this exact version. They SUPERSEDE your "
    "training, which is older and may be wrong here. Apply any fact that applies EXACTLY and do NOT "
    "second-guess it: if a fact contradicts your instinct, your instinct is stale training and the FACT "
    "wins. Ignore facts that do not apply.\n"
    "Keep your thinking SHORT: quickly identify which fact applies, then commit. Do NOT re-derive, do NOT "
    "argue with yourself, do NOT re-read the instructions. Your final answer must be ONLY the complete "
    "code in a single ```python code block, nothing else."
)

def fact_line(f):
    t = f.get("truth") or ""
    return f"- {t} [library: {f.get('lib')}, version: {f.get('version')}]"

def retrieve_facts(row, k):
    q = f"{row['problem']} {row.get('starting_code','')}"
    res = lookup.retrieve(q, hint=row["library"], mmr=True, k=k)
    return [lookup.FACTS[i] for _, i in res]

def sys_prompt(facts):
    return AUTHORITY + "\n\nVERIFIED FACTS (authoritative for this version):\n" + "\n".join(fact_line(f) for f in facts)

def prompt_for(row):
    return (f"Library: {row['library']}=={row['version']} (Python {row['python_version']})\n\n"
            f"Task: {row['problem']}\n\nComplete this code:\n"
            f"```python\n{row['starting_code']}\n```")

def chat(port, system, user, max_tokens=4096, temp=0.6):
    body = json.dumps({"temperature": temp, "top_p": 0.95, "max_tokens": max_tokens,
        "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}]}).encode()
    req = urllib.request.Request(f"http://127.0.0.1:{port}/v1/chat/completions", body, {"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=600) as r:
        ch = json.load(r)["choices"][0]; m = ch["message"]
        return (m.get("content") or "", m.get("reasoning_content") or "", ch.get("finish_reason") or "")

def extract_code(content, reasoning="", finish="stop"):
    m = re.findall(r"```(?:python)?\s*(.*?)```", content, re.S)
    if m: return m[0].strip()
    if content.strip(): return content.strip()
    if finish == "stop":
        rm = re.findall(r"```(?:python)?\s*(.*?)```", reasoning, re.S)
        if rm: return rm[-1].strip()
    return ""

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", required=True); ap.add_argument("--port", type=int, default=8080)
    ap.add_argument("--sample-per-lib", type=int, default=1); ap.add_argument("--all", action="store_true")
    ap.add_argument("--ids", default=""); ap.add_argument("--k", type=int, default=5)
    ap.add_argument("--max-tokens", type=int, default=8192); ap.add_argument("--temp", type=float, default=0.6)
    a = ap.parse_args()
    rows = [json.loads(l) for l in open(DATA, encoding="utf-8")]
    if a.ids:
        want = set(a.ids.split(",")); sample = [r for r in rows if r["example_id"] in want]
    elif a.all:
        sample = rows
    else:
        by = collections.defaultdict(list)
        for r in rows: by[r["library"]].append(r)
        sample = [rs[i] for rs in by.values() for i in range(min(a.sample_per_lib, len(rs)))]
    tp = os.path.join(HERE, f"{a.tag}_transcript.jsonl"); sp = os.path.join(HERE, f"{a.tag}_solutions.jsonl")
    done = set()
    if os.path.exists(sp): done = {json.loads(l)["example_id"] for l in open(sp, encoding="utf-8")}
    tf = open(tp, "a", encoding="utf-8"); sf = open(sp, "a", encoding="utf-8")
    n = 0
    for r in sample:
        eid = r["example_id"]
        if eid in done: continue
        facts = retrieve_facts(r, a.k)
        system = sys_prompt(facts); user = prompt_for(r)
        try:
            content, reasoning, finish = chat(a.port, system, user, a.max_tokens, a.temp)
        except Exception as e:
            print(f"ex{eid} ({r['library']}): ERROR {e}"); continue
        ans = extract_code(content, reasoning, finish)
        rec = {"example_id": eid, "library": r["library"], "version": r["version"], "finish_reason": finish,
               "retrieved": [f["id"] for f in facts], "retrieved_libs": [f["lib"] for f in facts],
               "problem": r["problem"], "system": system, "reasoning": reasoning, "content": content, "answer": ans}
        tf.write(json.dumps(rec, ensure_ascii=False) + "\n"); tf.flush()
        sf.write(json.dumps({"example_id": eid, "answer": ans}, ensure_ascii=False) + "\n"); sf.flush()
        n += 1
        rl = len(reasoning); hit = r["library"] in rec["retrieved_libs"]
        print(f"ex{eid:>4} {r['library']:<12} rlen={rl:>6} fin={finish:<6} libhit={hit}  ans1={ans.splitlines()[-1][:44] if ans else ''!r}")
    tf.close(); sf.close()
    print(f"\n[{a.tag}] {n} answered -> {tp}")

if __name__ == "__main__":
    main()
