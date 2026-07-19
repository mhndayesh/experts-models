#!/usr/bin/env python3
"""anchor_facts.py - add an `anchors` field to every fact: the exact code identifiers a developer would
TYPE in vulnerable code that the fact is about (cross-language API/method/class/config names). Anchors are
derived from the FACT's own content (subject+truth+code_bad) via DeepSeek - NEVER from any test draft (fair).
This is the T-02 data change: it gives generic-prose facts the code-symbol surface retrieval needs to match.

usage: DEEPSEEK_API_KEY=$(cat /c/projects/api/deepseek.txt) python anchor_facts.py [--n N] [--workers W] [--out FILE]
"""
import json, os, re, sys, urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

HERE = os.path.dirname(os.path.abspath(__file__))
BANK = os.path.join(HERE, "experts", "appsec", "facts", "FINAL.jsonl")
KEY  = os.environ.get("DEEPSEEK_API_KEY") or open(r"C:\projects\api\deepseek.txt").read().strip()
BASE = "https://api.deepseek.com/v1"; MODEL = "deepseek-v4-flash"

SYS = ("You label security rules with the concrete CODE IDENTIFIERS that appear in code the rule is about. "
       "For each numbered rule, output the exact API/function/method/class/config/attribute names a developer "
       "would literally TYPE in code that has (or fixes) this weakness, across ALL relevant languages. "
       "Include the vulnerable call AND the secure one. Identifiers ONLY - real tokens like torch.load, "
       "weights_only, aws_access_key_id, dangerouslySetInnerHTML, AutoAddPolicy, resolve_entities, "
       "compare_digest, O_EXCL, DocumentBuilderFactory, secure_filename. NO prose, NO explanations, NO CWE ids. "
       "5-14 identifiers per rule. Output EXACTLY one line per rule: 'N| id1, id2, id3, ...'")

def fact_desc(f):
    d = f.get("subject","") + " :: " + f.get("truth","")
    cb = f.get("code_bad") or ""
    if cb: d += " [code: " + cb[:180].replace("\n"," ") + "]"
    return d[:400]

def call(batch):
    lines = "\n".join(f"{i+1}. {fact_desc(f)}" for i,f in enumerate(batch))
    payload = {"model":MODEL,"temperature":0.2,"stream":False,"max_tokens":1400,
               "thinking":{"type":"disabled"},
               "messages":[{"role":"system","content":SYS},{"role":"user","content":lines}]}
    r = urllib.request.urlopen(urllib.request.Request(f"{BASE}/chat/completions",
        data=json.dumps(payload).encode(),
        headers={"Content-Type":"application/json","Authorization":f"Bearer {KEY}"}), timeout=180)
    txt = json.loads(r.read())["choices"][0]["message"]["content"]
    out = {}
    for ln in txt.splitlines():
        m = re.match(r"\s*(\d+)\s*[|.:)]\s*(.+)", ln)
        if not m: continue
        idx = int(m.group(1)) - 1
        syms = [s.strip() for s in re.split(r"[,;]", m.group(2)) if s.strip() and len(s.strip()) > 1]
        out[idx] = syms[:14]
    return out

def main():
    facts = [json.loads(l) for l in open(BANK, encoding="utf-8")]
    if "--n" in sys.argv: facts = facts[:int(sys.argv[sys.argv.index("--n")+1])]
    workers = int(sys.argv[sys.argv.index("--workers")+1]) if "--workers" in sys.argv else 12
    out_path = sys.argv[sys.argv.index("--out")+1] if "--out" in sys.argv else \
               os.path.join(HERE, "experts", "appsec", "facts", "FINAL_anchored.jsonl")
    B = 8
    batches = [(bi, facts[i:i+B]) for bi,i in enumerate(range(0, len(facts), B))]
    done = 0
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futs = {ex.submit(call, b): (bi, b) for bi, b in batches}
        for fut in as_completed(futs):
            bi, b = futs[fut]
            try: res = fut.result()
            except Exception as e: res = {}; print(f"  batch {bi} ERR {type(e).__name__}: {e}")
            for j, f in enumerate(b):
                f["anchors"] = res.get(j, [])
            done += 1
            if done % 20 == 0: print(f"  {done}/{len(batches)} batches")
    with_anchor = sum(1 for f in facts if f.get("anchors"))
    with open(out_path, "w", encoding="utf-8") as fh:
        for f in facts: fh.write(json.dumps(f, ensure_ascii=False) + "\n")
    print(f"anchored {with_anchor}/{len(facts)} facts -> {out_path}")

if __name__ == "__main__":
    main()
