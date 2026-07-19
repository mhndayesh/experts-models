#!/usr/bin/env python3
"""test_secnet.py - run the hand-authored Security & Networking landmine test against a llama-server GGUF.

The baked GGUF's own chat-template does retrieval internally, so we send the plain question - the same
prompt works for base (no bank) vs baked (bank fires). Uses the AUTHORITY system prompt + thinking-on
(the documented trick that stops a reasoning model reverting an injected fact to its trained prior).

  python test_secnet.py --tag baked-26b --port 8080 --think --temp 0.6 --authority --max-tokens 4096

Outputs (this dir):
  <tag>_transcript.jsonl   full prompt/reasoning/answer per question + auto-triage
  <tag>_score.txt          human-readable summary (auto-triage; the VERDICT is hand-read)
"""
import os, sys, json, re, argparse, urllib.request
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
QF = os.path.join(HERE, "test_questions.jsonl")

PLAIN_SYS = ("You are a senior security engineer. Answer the question for the EXACT library/version given. "
             "If the task is to write code, output the code; if it asks a yes/no or why question, answer briefly "
             "and concretely with the specific API or value.")
AUTHORITY_SYS = (
    "You are a senior security engineer answering for an EXACT library/version. A documentation lookup provides "
    "VERIFIED FACTS for this exact version: they are ABSOLUTELY CORRECT and SUPERSEDE your training, which is "
    "older and may be wrong here. Apply any fact that applies EXACTLY and do NOT second-guess it: if a fact "
    "contradicts your instinct, your instinct is stale training and the FACT wins. Ignore facts that do not "
    "apply. Keep your thinking short. Answer concretely: for a coding task output the code; for a yes/no or why "
    "question, name the specific API, import path, or value.")

def chat(port, prompt, max_tokens=4096, think=False, temp=1.0, authority=False,
         top_k=64, top_p=0.95, min_p=0.01):
    # Gemma-NATIVE sampling (official: temp 1.0, top_k 64, top_p 0.95, min_p 0.0-0.01,
    # rep_penalty 1.0). Sending bare temp=0.6 with no top_k/top_p/min_p is what let the
    # model collapse into a repetition loop on a hard token (reasoning ran to `length`
    # with an EMPTY answer) - it was a SAMPLING bug, not a budget/context limit (h04
    # looped even at 12288 tokens). min_p gives a probability floor that breaks the loop.
    body = json.dumps({"temperature": temp, "max_tokens": max_tokens,
        "top_k": top_k, "top_p": top_p, "min_p": min_p,
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

def triage(ans, q):
    """auto pre-check (TRIAGE ONLY - the verdict is hand-read). Case-insensitive.
    expect_new: list of groups; each group is any-of -> all groups must hit.
    avoid_old: none of these substrings may appear."""
    low = ans.lower()
    new_ok = all(any(alt.lower() in low for alt in group) for group in q.get("expect_new", []))
    old_hit = [t for t in q.get("avoid_old", []) if t.lower() in low]
    return bool(new_ok and not old_hit), new_ok, old_hit

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", required=True)
    ap.add_argument("--port", type=int, default=8080)
    ap.add_argument("--think", action="store_true")
    ap.add_argument("--temp", type=float, default=1.0, help="Gemma-native default 1.0")
    ap.add_argument("--top-k", type=int, default=64)
    ap.add_argument("--top-p", type=float, default=0.95)
    ap.add_argument("--min-p", type=float, default=0.01, help="probability floor; breaks repetition loops")
    ap.add_argument("--authority", action="store_true")
    ap.add_argument("--max-tokens", type=int, default=12288,
                    help="big by default (owner call): thinking-ON shares this budget with the answer, "
                         "and hard multi-step tasks need headroom so the answer isn't truncated to empty")
    ap.add_argument("--ids", default="")
    ap.add_argument("--qfile", default=QF, help="questions file (default test_questions.jsonl)")
    ap.add_argument("--workers", type=int, default=1,
                    help="concurrent requests (llama-server must be launched with --parallel >= this)")
    a = ap.parse_args()
    qfile = a.qfile if os.path.isabs(a.qfile) else os.path.join(HERE, a.qfile)
    qs = [json.loads(l) for l in open(qfile, encoding="utf-8") if l.strip()]
    if a.ids:
        want = set(a.ids.split(",")); qs = [q for q in qs if q["id"] in want]
    tp = os.path.join(HERE, f"{a.tag}_transcript.jsonl")

    def run_one(q):
        try:
            content, reasoning, finish = chat(a.port, q["q"], max_tokens=a.max_tokens,
                                              think=a.think, temp=a.temp, authority=a.authority,
                                              top_k=a.top_k, top_p=a.top_p, min_p=a.min_p)
        except Exception as e:
            return q, None, None, None, str(e)
        return q, content, reasoning, finish, None

    # Fan out over `workers` concurrent requests; the server batches them (continuous
    # batching), so 6 in flight is real throughput, not just queued. Order-preserving:
    # executor.map yields results in input order regardless of completion order.
    recs = []
    with ThreadPoolExecutor(max_workers=max(1, a.workers)) as ex:
        for q, content, reasoning, finish, err in ex.map(run_one, qs):
            if err is not None:
                print(f"{q['id']} ERROR {err}")
                recs.append({**q, "finish_reason": "error", "content": "", "reasoning": "",
                             "auto_pass": False, "new_ok": False, "old_hit": [], "error": err})
                continue
            judge_text = content if content.strip() else reasoning
            auto, new_ok, old_hit = triage(judge_text, q)
            recs.append({**q, "finish_reason": finish, "content": content, "reasoning": reasoning,
                         "auto_pass": auto, "new_ok": new_ok, "old_hit": old_hit})

    npass = 0
    lines = []
    tf = open(tp, "w", encoding="utf-8")
    for rec in recs:
        tf.write(json.dumps(rec, ensure_ascii=False) + "\n")
        npass += int(rec["auto_pass"])
        tag = "PASS" if rec["auto_pass"] else "FAIL"
        line = f"{rec['id']} {rec['lib']:<12} [{tag}] new_ok={rec['new_ok']} old_hit={rec['old_hit']}"
        lines.append(line); print(line)
    tf.close()
    sp = os.path.join(HERE, f"{a.tag}_score.txt")
    with open(sp, "w", encoding="utf-8") as sf:
        sf.write(f"[{a.tag}] AUTO-TRIAGE {npass}/{len(qs)} pass (HAND-VERIFY required)\n\n")
        sf.write("\n".join(lines) + "\n")
    print(f"\n[{a.tag}] auto-triage {npass}/{len(qs)}  ->  {tp}\n(hand-verify: read the transcript)")

if __name__ == "__main__":
    main()
