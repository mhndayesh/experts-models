#!/usr/bin/env python3
"""build_v3_llm.py - PASS 2: DeepSeek enrichment for schema v3. Per fact, assign the structural fields the
deterministic pass couldn't: concept CWE (the backbone), sub_pattern, framework, aliases, query_phrases, and
extra exact/bad symbols for the ~61% of facts with no code-derived anchor. Batched + parallel. Cheap/no-GPU.

usage: python build_v3_llm.py [--n N] [--workers W] [--out FILE]
"""
import json, os, re, sys, urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

HERE = os.path.dirname(os.path.abspath(__file__))
SRC  = os.path.join(HERE, "experts", "appsec", "facts", "FINAL.jsonl")
KEY  = os.environ.get("DEEPSEEK_API_KEY") or open(r"C:\projects\api\deepseek.txt").read().strip()
BASE, MODEL = "https://api.deepseek.com/v1", "deepseek-v4-flash"

SYS = ("You classify insecure-coding facts into a faceted schema for retrieval. For each numbered fact return a "
       "STRICT JSON object on ONE line: {\"n\":N,\"cwe\":\"CWE-89\",\"sub_pattern\":\"dynamic-order-by\","
       "\"framework\":\"flask\"|null,\"language\":\"python\","
       "\"exact_symbols\":[...],\"bad_symbols\":[...],\"aliases\":[...],\"query_phrases\":[...]}. "
       "cwe = the single best-fitting CWE id (the reusable concept). sub_pattern = a short kebab-case tag for the "
       "SPECIFIC variant within that CWE. exact_symbols = the exact API a dev types in SECURE/aware code; "
       "bad_symbols = the vulnerable call; aliases = natural names; query_phrases = the coding task a dev asks "
       "(e.g. 'load an uploaded model checkpoint'). Identifiers must be real tokens (torch.load, weights_only, "
       "PreparedStatement, dangerouslySetInnerHTML). 3-10 items per list, [] if none. NO prose outside the JSON.")

def desc(i, f):
    d = f"{i+1}. [{f.get('door')}] {f.get('subject','')} :: {f.get('truth','')}"
    cb = f.get("code_bad") or ""
    if cb: d += " |bad_code: " + cb[:160].replace("\n"," ")
    return d[:420]

def call(batch, base):
    lines = "\n".join(desc(i, f) for i, f in enumerate(batch))
    payload = {"model":MODEL,"temperature":0.2,"stream":False,"max_tokens":2200,"thinking":{"type":"disabled"},
               "messages":[{"role":"system","content":SYS},{"role":"user","content":lines}]}
    r = urllib.request.urlopen(urllib.request.Request(f"{base}/chat/completions",
        data=json.dumps(payload).encode(),
        headers={"Content-Type":"application/json","Authorization":f"Bearer {KEY}"}), timeout=180)
    txt = json.loads(r.read())["choices"][0]["message"]["content"]
    out = {}
    for m in re.finditer(r"\{[^{}]*\"n\"\s*:\s*(\d+)[^{}]*\}", txt):
        try:
            o = json.loads(m.group(0)); out[int(o["n"]) - 1] = o
        except Exception: pass
    return out

def main():
    facts = [json.loads(l) for l in open(SRC, encoding="utf-8")]
    if "--n" in sys.argv: facts = facts[:int(sys.argv[sys.argv.index("--n")+1])]
    workers = int(sys.argv[sys.argv.index("--workers")+1]) if "--workers" in sys.argv else 14
    out_path = sys.argv[sys.argv.index("--out")+1] if "--out" in sys.argv else \
               os.path.join(HERE, "experts", "appsec", "facts", "v3_llm.jsonl")
    B = 6
    batches = [(bi, facts[i:i+B]) for bi, i in enumerate(range(0, len(facts), B))]
    enriched = {}
    done = 0
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futs = {ex.submit(call, b, BASE): (bi, b) for bi, b in batches}
        for fut in as_completed(futs):
            bi, b = futs[fut]
            try: res = fut.result()
            except Exception as e: res = {}; print(f"  batch {bi} ERR {type(e).__name__}")
            for j, f in enumerate(b): enriched[f["id"]] = res.get(j, {})
            done += 1
            if done % 30 == 0: print(f"  {done}/{len(batches)}")
    got = sum(1 for v in enriched.values() if v.get("cwe"))
    with open(out_path, "w", encoding="utf-8") as fh:
        for fid, e in enriched.items(): fh.write(json.dumps({"id":fid, **e}, ensure_ascii=False)+"\n")
    print(f"enriched {got}/{len(enriched)} with a CWE concept -> {out_path}")

if __name__ == "__main__":
    main()
