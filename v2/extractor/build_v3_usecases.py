#!/usr/bin/env python3
"""build_v3_usecases.py - SAMPLE re-enrichment for the locked lexical method. Improves the single biggest
lever: USE_CASES = the CONTAINING coding task a dev is building when they hit this landmine (what a benign
prompt actually says). For subtle facts (timing compare, TOCTOU) this is the broader feature, not the vuln.
Operates on a --sample id list; merges improved use_cases into FINAL_v3 for a fair failure-set re-measure.

usage: python build_v3_usecases.py --sample <ids.json> [--workers W]
"""
import json, os, re, sys, urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

HERE = os.path.dirname(os.path.abspath(__file__))
SRC  = os.path.join(HERE, "experts", "appsec", "facts", "FINAL.jsonl")
KEY  = os.environ.get("DEEPSEEK_API_KEY") or open(r"C:\projects\api\deepseek.txt").read().strip()
BASE, MODEL = "https://api.deepseek.com/v1", "deepseek-v4-flash"

SYS = ("You label a security fact with the CONTAINING CODING TASKS a developer is building when their code "
       "would hit this landmine - i.e. what a benign feature request actually SAYS (never the vulnerability). "
       "Think about the broader FEATURE, not the bug. Examples: a constant-time-comparison fact -> tasks like "
       "'verify an HMAC-signed URL','check a webhook signature','validate a password-reset token','authenticate "
       "an API request'. A TOCTOU file fact -> 'create a file only if it does not exist','write a lock file'. "
       "A SQL-injection fact -> 'filter a table by optional query params','search users by name','sort results "
       "by a column'. For each numbered fact return STRICT JSON on ONE line: "
       "{\"n\":N,\"use_cases\":[6-10 short containing-task phrases],\"canonical_cwe\":\"CWE-NN\"}. "
       "use_cases must be things a dev types when REQUESTING the feature - concrete, varied, NO fix/vuln words. "
       "NO prose outside the JSON.")

def desc(i, f):
    d = f"{i+1}. [{f.get('door')}/{f.get('lang')}] {f.get('subject','')} :: {f.get('truth','')}"
    cb = f.get("code_bad") or ""
    if cb: d += " |code: " + cb[:120].replace("\n"," ")
    return d[:380]

def call(batch):
    lines = "\n".join(desc(i, f) for i, f in enumerate(batch))
    payload = {"model":MODEL,"temperature":0.3,"stream":False,"max_tokens":2600,"thinking":{"type":"disabled"},
               "messages":[{"role":"system","content":SYS},{"role":"user","content":lines}]}
    r = urllib.request.urlopen(urllib.request.Request(f"{BASE}/chat/completions",
        data=json.dumps(payload).encode(),
        headers={"Content-Type":"application/json","Authorization":f"Bearer {KEY}"}), timeout=180)
    txt = json.loads(r.read())["choices"][0]["message"]["content"]
    out = {}
    for m in re.finditer(r"\{[^{}]*\"n\"\s*:\s*(\d+)[^{}]*\}", txt):
        try: o = json.loads(m.group(0)); out[int(o["n"]) - 1] = o
        except Exception: pass
    return out

def main():
    facts = [json.loads(l) for l in open(SRC, encoding="utf-8")]
    sample = json.load(open(sys.argv[sys.argv.index("--sample")+1])) if "--sample" in sys.argv else list(range(len(facts)))
    sel = [facts[i] for i in sample]
    workers = int(sys.argv[sys.argv.index("--workers")+1]) if "--workers" in sys.argv else 48
    out_path = os.path.join(HERE, "experts", "appsec", "facts", "v3_usecases.jsonl")
    B = 4
    batches = [sel[i:i+B] for i in range(0, len(sel), B)]
    enr = {}; done = 0
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futs = {ex.submit(call, b): b for b in batches}
        for fut in as_completed(futs):
            b = futs[fut]
            try: res = fut.result()
            except Exception: res = {}
            for j, f in enumerate(b): enr[f["id"]] = res.get(j, {})
            done += 1
    got = sum(1 for v in enr.values() if v.get("use_cases"))
    with open(out_path, "w", encoding="utf-8") as fh:
        for fid, e in enr.items(): fh.write(json.dumps({"id":fid, **e}, ensure_ascii=False)+"\n")
    print(f"use_cases: {got}/{len(enr)} -> {out_path}")

if __name__ == "__main__":
    main()
