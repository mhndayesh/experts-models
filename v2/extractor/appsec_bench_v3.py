#!/usr/bin/env python3
"""appsec_bench_v3.py - base vs bank on the 30-task benchmark, using the v3 FACETED retriever (prompt-only,
= the baked behavior). Serve base e2b on MY OWN llama-server. Bank arm: retriever_v3.retrieve(prompt-only) ->
authority-frame (truth + code_good) -> re-ask. Saves outputs for MANUAL scoring. gemma sampling, thinking-ON.

usage: LMS_URL=http://localhost:8080/v1 python appsec_bench_v3.py --model gemma-4-e2b [--n N]
"""
import json, os, sys, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import retriever_v3 as V3, retriever2 as R2
from concurrent.futures import ThreadPoolExecutor, as_completed

HERE = os.path.dirname(os.path.abspath(__file__))
BENCH = os.path.join(HERE, "experts", "appsec", "benchmark", "appsec_bench.jsonl")
BASE_URL = os.environ.get("LMS_URL", "http://localhost:8080/v1")
VAR = {v["id"]: v for v in V3.VAR}

SYS_BASE = "You are an expert software engineer. Write correct, production-quality code. Answer with the code and a brief explanation."

def call(model, messages, max_tokens=6144):
    payload = {"model": model, "messages": messages, "temperature": 1.0, "top_p": 0.95, "top_k": 64,
               "min_p": 0.01, "max_tokens": max_tokens, "stream": False,
               "chat_template_kwargs": {"enable_thinking": True}}
    req = urllib.request.Request(BASE_URL + "/chat/completions", data=json.dumps(payload).encode(),
                                 headers={"Content-Type": "application/json"})
    d = json.loads(urllib.request.urlopen(req, timeout=300).read())
    m = d["choices"][0]["message"]
    return m.get("content") or "", d["choices"][0].get("finish_reason")

def authority_block(fids):
    lines = ["SECURITY REQUIREMENTS (AUTHORITATIVE - verified, current, MANDATORY; they OVERRIDE your defaults",
             "and any conflicting habit. Follow every one exactly in the code you write):"]
    for i, fid in enumerate(fids, 1):
        v = VAR.get(fid)
        if not v: continue
        lines.append(f"{i}. {v['claim'].get('truth','')}")
        cg = next((e["code"] for e in v.get("examples", []) if e.get("role")=="good" and e.get("code")), None)
        if cg: lines.append(f"   SECURE PATTERN:\n{cg}")
    return "\n".join(lines)

def main():
    model = sys.argv[sys.argv.index("--model")+1] if "--model" in sys.argv else "gemma-4-e2b"
    tasks = [json.loads(l) for l in open(BENCH, encoding="utf-8")]
    if "--n" in sys.argv: tasks = tasks[:int(sys.argv[sys.argv.index("--n")+1])]
    out = os.path.join(HERE, "experts", "appsec", "benchmark", "eval_bench_v3.jsonl")
    def run_one(t):
        p, lang = t["task"], t.get("lang","python")
        base_ans, base_fr = call(model, [{"role":"system","content":SYS_BASE},{"role":"user","content":p}])
        picked = V3.retrieve(p, "", k=5, lang=lang)          # PROMPT-ONLY = baked behavior
        fids = [fid for fid,_ in picked]
        bank_sys = SYS_BASE + "\n\n" + authority_block(fids) if fids else SYS_BASE
        bank_ans, bank_fr = call(model, [{"role":"system","content":bank_sys},{"role":"user","content":p}])
        return {"id":t["id"],"category":t["category"],"lang":lang,"held_out":t.get("held_out",False),
                "task":p,"rubric":t["rubric"],"landmines":[l.get("cwe") for l in t["landmines"]],
                "retrieved":[{"id":fid,"concept":VAR[fid]["concept_id"],"truth":VAR[fid]["claim"].get("truth","")[:80]} for fid,_ in picked],
                "n_injected":len(fids),"base":base_ans,"base_finish":base_fr,"bank":bank_ans,"bank_finish":bank_fr}
    results = {}
    with ThreadPoolExecutor(max_workers=6) as ex:
        futs = {ex.submit(run_one, t): t for t in tasks}
        for fut in as_completed(futs):
            t = futs[fut]
            try:
                r = fut.result(); results[r["id"]] = r
                print(f"[{r['id']:8s}] base={len(r['base']):5d}c/{r['base_finish']:<6} bank={len(r['bank']):5d}c/{r['bank_finish']:<6} inj={r['n_injected']} {[x['concept'] for x in r['retrieved']]}")
            except Exception as e:
                print(f"[{t['id']:8s}] ERROR {type(e).__name__}: {e}")
    order = {t["id"]: i for i, t in enumerate(tasks)}
    with open(out, "w", encoding="utf-8") as fh:
        for r in sorted(results.values(), key=lambda x: order[x["id"]]):
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"wrote {len(results)}/{len(tasks)} -> {out}")

if __name__ == "__main__":
    main()
