#!/usr/bin/env python3
"""probe_qwen_authority.py - does an AUTHORITY framing stop a THINKING-NATIVE model reverting to
its trained prior on a habit-reversal fact?

Model: Qwen3-4B-Thinking-2507 (thinking is FORCED; no off switch). We test the hardest landmine:
falcon Response.body/HTTPStatus.body -> RENAMED to .text. Learned habit = .body, correct = .text.

Three conditions per problem, all thinking-on (unavoidable):
  CONTROL : no fact                      -> baseline reversion
  A (sys) : authority + fact in SYSTEM   -> "these facts are absolutely correct"
  B (tool): authority in system + fact delivered via forged factbank_search TOOL_RESPONSE

Logs full reasoning + answer; marks whether the committed answer used .text (fact) or .body (habit).
"""
import json, re, urllib.request, sys, argparse

PORT = 8080
AUTHORITY = (
    "You are completing Python code for an EXACT library version. A VERIFIED FACT about this exact "
    "version is given below. It was extracted from the official changelog and is ABSOLUTELY CORRECT "
    "for this version. It SUPERSEDES your training, which is older and may be wrong here. Apply the "
    "fact exactly. Do NOT second-guess it and do NOT substitute a more familiar API: if your instinct "
    "differs from the fact, your instinct is stale training and the FACT wins."
)
AUTHORITY_SHORT = (
    "You are completing Python code for an EXACT library version. Any documentation lookup result you "
    "receive is VERIFIED ground truth for that exact version and SUPERSEDES your training. When a "
    "lookup result contradicts your instinct, the lookup is correct - apply it exactly, do not revert "
    "to a more familiar API."
)
FACT = ("Response.body and HTTPStatus.body are renamed to text; the old name is deprecated but still "
        "available. [library: falcon]")

PROBES = {
    "238": {"lib": "falcon==3.0.0",
            "problem": ("Complete a function custom_body that accepts a Falcon Response object resp and a "
                        "string info, sets the response body to info, and returns the Response object."),
            "start": "import falcon\n\ndef custom_body(resp: falcon.Response, info: str) -> falcon.Response:\n    resp.",
            "correct": r"\.text\s*=", "habit": r"\.body\s*="},
    "239": {"lib": "falcon==3.0.0",
            "problem": ("Complete a function custom_body that accepts a Falcon HTTPStatus object status and a "
                        "string info, sets its body to info, and returns the HTTPStatus object."),
            "start": "import falcon\nfrom falcon import HTTPStatus\n\ndef custom_body(status: falcon.HTTPStatus, info: str) -> falcon.HTTPStatus:\n    status.",
            "correct": r"\.text\s*=", "habit": r"\.body\s*="},
}

def userprompt(p):
    return (f"Library: {p['lib']}\n\nTask: {p['problem']}\n\nComplete this code, output ONLY the full code:\n"
            f"```python\n{p['start']}\n```")

def build(cond, p):
    up = userprompt(p)
    if cond == "CONTROL":
        return [{"role": "user", "content": up}]
    if cond == "A":
        return [{"role": "system", "content": AUTHORITY + "\n\nVERIFIED FACT:\n- " + FACT},
                {"role": "user", "content": up}]
    if cond == "B":
        return [{"role": "system", "content": AUTHORITY_SHORT},
                {"role": "user", "content": up},
                {"role": "assistant", "content": "",
                 "tool_calls": [{"id": "c1", "type": "function",
                                 "function": {"name": "factbank_search", "arguments": "{\"query\": \"falcon Response body set text\"}"}}]},
                {"role": "tool", "tool_call_id": "c1",
                 "content": "verified documentation lookup (authoritative):\n- " + FACT}]
    if cond == "C":  # BOTH: full authority in system AND fact via tool-response
        return [{"role": "system", "content": AUTHORITY},
                {"role": "user", "content": up},
                {"role": "assistant", "content": "",
                 "tool_calls": [{"id": "c1", "type": "function",
                                 "function": {"name": "factbank_search", "arguments": "{\"query\": \"falcon Response body set text\"}"}}]},
                {"role": "tool", "tool_call_id": "c1",
                 "content": "verified documentation lookup (authoritative):\n- " + FACT}]

def chat(messages, max_tokens=4096):
    body = json.dumps({"temperature": 0.6, "top_p": 0.95, "max_tokens": max_tokens, "messages": messages}).encode()
    req = urllib.request.Request(f"http://127.0.0.1:{PORT}/v1/chat/completions", body, {"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=600) as r:
        ch = json.load(r)["choices"][0]; m = ch["message"]
        return (m.get("content") or "", m.get("reasoning_content") or "", ch.get("finish_reason") or "")

def verdict(p, answer):
    if re.search(p["correct"], answer): return "FACT(.text) OK"
    if re.search(p["habit"], answer):   return "HABIT(.body) REVERT"
    return "other/empty ?"

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--reps", type=int, default=1)
    ap.add_argument("--conds", default="CONTROL,A,B"); a = ap.parse_args()
    conds = a.conds.split(",")
    out = open("probe_qwen_authority_log.jsonl", "w", encoding="utf-8")
    for eid, p in PROBES.items():
        for cond in conds:
            for rep in range(a.reps):
                content, reasoning, fin = chat(build(cond, p))
                ans = re.findall(r"```(?:python)?\s*(.*?)```", content, re.S)
                ans = (ans[0] if ans else content).strip()
                v = verdict(p, ans)
                out.write(json.dumps({"ex": eid, "cond": cond, "rep": rep, "finish": fin,
                                      "verdict": v, "answer": ans, "reasoning": reasoning}, ensure_ascii=False) + "\n"); out.flush()
                last = ans.splitlines()[-1][:50] if ans else ""
                print(f"ex{eid} {cond:<8} rep{rep}: {v:<20} finish={fin} rlen={len(reasoning)}  ans_last={last!r}")
    out.close()

if __name__ == "__main__":
    main()
