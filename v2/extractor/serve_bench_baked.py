"""Send the 30 benign benchmark prompts to a served llama-server and save outputs.
Baked GGUF (--jinja) => the bank fires IN-ENGINE from the template (the real shipped artifact).
Base GGUF => no bank. Run once per arm; hand-score the saved outputs (SCORE MANUALLY).

usage: LMS_URL=http://localhost:8080/v1 python serve_bench_baked.py <out.jsonl> [--n N]
"""
import json, os, sys, urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

HERE = os.path.dirname(os.path.abspath(__file__))
BENCH = os.path.join(HERE, "experts", "appsec", "benchmark", "appsec_bench.jsonl")
BASE_URL = os.environ.get("LMS_URL", "http://localhost:8080/v1")
OUT = sys.argv[1]
N = int(sys.argv[sys.argv.index("--n") + 1]) if "--n" in sys.argv else 999

# gemma-native sampling; thinking OFF (baked expert ships thinking-off)
THINK = os.environ.get("THINK", "1") == "1"
MAXTOK = int(os.environ.get("MAXTOK", "2600"))
def call(prompt):
    payload = {"model": "local", "temperature": 1.0, "top_k": 64, "top_p": 0.95, "min_p": 0.01,
               "max_tokens": MAXTOK, "stream": False,
               "chat_template_kwargs": {"enable_thinking": THINK},
               "messages": [{"role": "user", "content": prompt}]}
    req = urllib.request.Request(f"{BASE_URL}/chat/completions",
        data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"})
    d = json.loads(urllib.request.urlopen(req, timeout=600).read())
    ch = d["choices"][0]
    return ch["message"]["content"] or "", ch.get("finish_reason", "")

tasks = [json.loads(l) for l in open(BENCH, encoding="utf-8")][:N]
results = {}
def run_one(t):
    txt, fin = call(t["task"])
    return {"id": t["id"], "task": t["task"], "rubric": t.get("rubric", ""),
            "landmines": [l.get("cwe") for l in t.get("landmines", [])],
            "out": txt, "finish": fin}
with ThreadPoolExecutor(max_workers=8) as ex:
    futs = {ex.submit(run_one, t): t for t in tasks}
    for fut in as_completed(futs):
        r = fut.result(); results[r["id"]] = r
        print(f"[{r['id']:8s}] {len(r['out']):5d}c/{r['finish']:<7} {r['landmines']}")
order = {t["id"]: i for i, t in enumerate(tasks)}
with open(OUT, "w", encoding="utf-8") as fh:
    for r in sorted(results.values(), key=lambda x: order[x["id"]]):
        fh.write(json.dumps(r, ensure_ascii=False) + "\n")
print(f"\nwrote {len(results)} -> {OUT}")
