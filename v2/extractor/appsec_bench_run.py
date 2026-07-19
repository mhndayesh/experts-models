#!/usr/bin/env python3
"""appsec_bench_run.py - run the 30-task APPSEC-INTEGRATION benchmark base-vs-bank against a served base model.

Reuses the proven serve-loop machinery from appsec_servetest.py (HyDE double-key retrieval, authority-framed
injection, gemma-native sampling, thinking-ON). For each task:
  BASE : ask the task directly.
  BANK : HyDE-retrieve top-K facts from FINAL.jsonl using the task + the base draft, inject authority-framed, re-ask.
Writes both answers + the retrieved facts + the rubric to eval_bench.jsonl. SCORE MANUALLY against the rubric
(project rule) - the prose must/must_not are properties, not regex.

Talks ONLY to the server at $LMS_URL (default my own llama-server on :8080). Never loads/unloads a model.
usage:  LMS_URL=http://localhost:8080/v1 python appsec_bench_run.py --model gemma-4-e2b [--k 5] [--n N] [--smoke]
"""
import json, os, sys
from concurrent.futures import ThreadPoolExecutor, as_completed
import appsec_servetest as S   # retrieve(), call(), authority_block(), SYS_BASE, FACTS

HERE = os.path.dirname(os.path.abspath(__file__))
BENCH = os.path.join(HERE, "experts", "appsec", "benchmark", "appsec_bench.jsonl")

def load_tasks():
    return [json.loads(l) for l in open(BENCH, encoding="utf-8")]

def run_one(model, t, k):
    """Full base->retrieve(HyDE on base draft)->bank chain for one task. Sequential WITHIN a task
    (bank needs the base draft); tasks run concurrently across server slots."""
    prompt = t["task"]
    base_ans, base_fr = S.call(model, [{"role":"system","content":S.SYS_BASE},{"role":"user","content":prompt}])
    facts = S.retrieve(prompt, base_ans, k)
    bank_sys = S.SYS_BASE + "\n\n" + S.authority_block(facts)
    bank_ans, bank_fr = S.call(model, [{"role":"system","content":bank_sys},{"role":"user","content":prompt}])
    return {"id":t["id"], "category":t["category"], "lang":t["lang"], "held_out":t.get("held_out",False),
            "libraries":t["libraries"], "task":prompt, "rubric":t["rubric"],
            "landmines":[{"cwe":l.get("cwe"),"currency":l.get("currency")} for l in t["landmines"]],
            "retrieved":[{"id":f["id"],"lib":f.get("lib"),"truth":f["truth"]} for f in facts],
            "base":base_ans, "base_finish":base_fr, "bank":bank_ans, "bank_finish":bank_fr}

def main():
    model = sys.argv[sys.argv.index("--model")+1] if "--model" in sys.argv else "gemma-4-e2b"
    k = int(sys.argv[sys.argv.index("--k")+1]) if "--k" in sys.argv else 5
    jobs = int(sys.argv[sys.argv.index("--jobs")+1]) if "--jobs" in sys.argv else 1
    tasks = load_tasks()
    if "--smoke" in sys.argv: tasks = tasks[:1]
    elif "--n" in sys.argv: tasks = tasks[:int(sys.argv[sys.argv.index("--n")+1])]
    out = os.path.join(HERE, "experts", "appsec", "benchmark", "eval_bench.jsonl")
    order = {t["id"]: i for i, t in enumerate(tasks)}
    results = {}
    with ThreadPoolExecutor(max_workers=jobs) as ex:
        futs = {ex.submit(run_one, model, t, k): t for t in tasks}
        for fut in as_completed(futs):
            t = futs[fut]
            try:
                rec = fut.result()
            except Exception as e:
                print(f"[{t['id']:8s}] ERROR {type(e).__name__}: {e}"); continue
            results[rec["id"]] = rec
            libs = [f.get("lib") for f in rec["retrieved"]]
            print(f"[{rec['id']:8s}] base={len(rec['base']):5d}c/{rec['base_finish']:<6} "
                  f"bank={len(rec['bank']):5d}c/{rec['bank_finish']:<6} facts:{libs}")
    with open(out, "w", encoding="utf-8") as fh:
        for rec in sorted(results.values(), key=lambda r: order[r["id"]]):
            fh.write(json.dumps(rec, ensure_ascii=False)+"\n")
    print(f"wrote {len(results)}/{len(tasks)} -> {out}")

if __name__ == "__main__":
    main()
