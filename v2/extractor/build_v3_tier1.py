#!/usr/bin/env python3
"""build_v3_tier1.py - Tier-1 RICHNESS pass (DeepSeek, max parallel). Per fact add the fields that fix the
failure classes: feature_phrases (the CODING TASK, not the vuln - fixes Class A), disambiguator (distinguishes
a variant from its concept-siblings), library_trigger (package/API whose presence should inject this - Class D),
canonical_cwe (one authoritative CWE - fixes Class B fragmentation). Merged into FINAL_v3 by build_v3_assemble2.

usage: DEEPSEEK_API_KEY=$(cat /c/projects/api/deepseek.txt) python build_v3_tier1.py [--n N] [--workers W]
"""
import json, os, re, sys, urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

HERE = os.path.dirname(os.path.abspath(__file__))
SRC  = os.path.join(HERE, "experts", "appsec", "facts", "FINAL.jsonl")
KEY  = os.environ.get("DEEPSEEK_API_KEY") or open(r"C:\projects\api\deepseek.txt").read().strip()
BASE, MODEL = "https://api.deepseek.com/v1", "deepseek-v4-flash"

SYS = ("You enrich insecure-coding facts for retrieval by a BENIGN prompt (the developer describes the FEATURE "
       "they are building, NOT the vulnerability). For each numbered fact return STRICT JSON on ONE line: "
       "{\"n\":N,\"canonical_cwe\":\"CWE-89\","
       "\"feature_phrases\":[...],\"disambiguator\":\"...\",\"library_trigger\":[...]}. "
       "feature_phrases = 3-6 SHORT task descriptions a dev would actually write/ask when building code that hits "
       "this landmine - describe the FEATURE/GOAL, not the fix. e.g. for a SQL-injection fact: 'filter a table by "
       "optional query parameters','search users by name from a request','build a dynamic WHERE clause'. NOT "
       "'prevent SQL injection'. disambiguator = one short clause distinguishing THIS variant from sibling facts "
       "under the same CWE (the specific API/sub-case). library_trigger = the package/module/API tokens whose mere "
       "presence in code should surface this fact (e.g. 'paramiko.SSHClient','torch.load'). canonical_cwe = the "
       "single best-fitting CWE id. NO prose outside the JSON.")

def desc(i, f):
    d = f"{i+1}. [{f.get('door')}/{f.get('lang')}] {f.get('subject','')} :: {f.get('truth','')}"
    cb = f.get("code_bad") or ""
    if cb: d += " |code: " + cb[:130].replace("\n"," ")
    return d[:400]

def call(batch):
    lines = "\n".join(desc(i, f) for i, f in enumerate(batch))
    payload = {"model":MODEL,"temperature":0.2,"stream":False,"max_tokens":3200,"thinking":{"type":"disabled"},
               "messages":[{"role":"system","content":SYS},{"role":"user","content":lines}]}
    r = urllib.request.urlopen(urllib.request.Request(f"{BASE}/chat/completions",
        data=json.dumps(payload).encode(),
        headers={"Content-Type":"application/json","Authorization":f"Bearer {KEY}"}), timeout=180)
    txt = json.loads(r.read())["choices"][0]["message"]["content"]
    out = {}
    for m in re.finditer(r"\{[^{}]*\"n\"\s*:\s*(\d+)[^{}]*\}", txt):   # flat objects (arrays have no braces)
        try: o = json.loads(m.group(0)); out[int(o["n"]) - 1] = o
        except Exception: pass
    return out

def main():
    facts = [json.loads(l) for l in open(SRC, encoding="utf-8")]
    if "--n" in sys.argv: facts = facts[:int(sys.argv[sys.argv.index("--n")+1])]
    workers = int(sys.argv[sys.argv.index("--workers")+1]) if "--workers" in sys.argv else 48
    out_path = os.path.join(HERE, "experts", "appsec", "facts", "v3_tier1.jsonl")
    B = 4
    batches = [(bi, facts[i:i+B]) for bi, i in enumerate(range(0, len(facts), B))]
    enr = {}; done = 0
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futs = {ex.submit(call, b): (bi, b) for bi, b in batches}
        for fut in as_completed(futs):
            bi, b = futs[fut]
            try: res = fut.result()
            except Exception as e: res = {}
            for j, f in enumerate(b): enr[f["id"]] = res.get(j, {})
            done += 1
            if done % 30 == 0: print(f"  {done}/{len(batches)}")
    got = sum(1 for v in enr.values() if v.get("feature_phrases"))
    with open(out_path, "w", encoding="utf-8") as fh:
        for fid, e in enr.items(): fh.write(json.dumps({"id":fid, **e}, ensure_ascii=False)+"\n")
    print(f"tier1: {got}/{len(enr)} with feature_phrases -> {out_path}")

if __name__ == "__main__":
    main()
