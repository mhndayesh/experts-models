"""Live test of gemma-4-12b-qat-factbank-1027-native-v4 in LM Studio.
Same questions as the NATIVE-v2 live test (2026-07-13). Plain chat calls:
one user message, no tools, no tags. Checks per answer:
  - ECHO: does message.content contain forged-block text
    ("<|tool_call>", "call:factbank_search", the notes header)?
  - facts reaching the answer (manual read; we print full content).
"""
import json, urllib.request, time, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

URL = "http://127.0.0.1:1234/api/v0/chat/completions"
MODEL = "gemma-4-12b-qat-factbank-1027-native-v4"

QUESTIONS = [
    ("hello", "hello there"),
    ("haiku", "write a haiku about the sea"),
    ("closure", "Explain what a closure is in Python, briefly."),
    ("bqn_sum", "in bqn how do I sum a list of numbers?"),
    ("zig_float", "in zig how do I convert an integer to a float?"),
    ("polars_wide", "quick polars question: how do i reshape wide format into long format"),
    ("whenever_tz", "quick whenever question: how do i get the current time in a specific timezone"),
    ("polars_melt", "my polars melt code stopped working after upgrading, fix it"),
    ("mixed", "what is the weather in paris and fix my polars melt code"),
]

ECHO_MARKERS = ["<|tool_call>", "call:factbank_search", "<tool_call|>",
                "verified documentation lookup results", "<|turn>", "<turn|>"]

out = []
for tag, q in QUESTIONS:
    body = json.dumps({
        "model": MODEL,
        "messages": [{"role": "user", "content": q}],
        "temperature": 0.2,
        "max_tokens": 2048,
    }).encode()
    t0 = time.time()
    req = urllib.request.Request(URL, data=body,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=600) as r:
        resp = json.loads(r.read())
    dt = time.time() - t0
    msg = resp["choices"][0]["message"]
    content = msg.get("content") or ""
    reasoning = msg.get("reasoning_content") or ""
    echo = [m for m in ECHO_MARKERS if m in content]
    stats = resp.get("stats", {})
    usage = resp.get("usage", {})
    rec = {"tag": tag, "q": q, "content": content, "reasoning_len": len(reasoning),
           "echo_markers": echo, "finish": resp["choices"][0].get("finish_reason"),
           "usage": usage, "stats": stats, "wall_s": round(dt, 1)}
    out.append(rec)
    print(f"=== {tag} | echo={'YES:' + ','.join(echo) if echo else 'clean'} | "
          f"prompt={usage.get('prompt_tokens')} completion={usage.get('completion_tokens')} "
          f"| {rec['finish']} | {rec['wall_s']}s")
    print(content[:1500])
    print()

with open("live_v3_results.jsonl", "w", encoding="utf-8") as f:
    for r in out:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
print("saved live_v3_results.jsonl")
