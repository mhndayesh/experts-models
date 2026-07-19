#!/usr/bin/env python3
"""refine.py - the SECOND DeepSeek pass: rewrite VAGUE facts into CONCRETE, output-explicit
ones, GROUNDED IN THE ACTUAL SOURCE TEXT the fact came from (owner requirement: pass the real
doc part, not just the fact). Ecto finding: a vague-but-true fact loses; the same fact reworded
concretely WINS (map/2: "behaviour changed" -> "you now get %{id: nil}, not nil").

Safety: the verbatim `quote` anchor is NOT touched (still grounds the fact). Only `truth` is
refined, using ONLY the passed source part. Manual reading is the verdict (F-065) - writes a
before/after diff to READ.

usage: DEEPSEEK_API_KEY=... python refine.py <facts.jsonl> <source.md>
out:   <facts>.concrete.jsonl  +  <facts>.concrete.diff.md  (READ this)
"""
import json, os, re, sys, urllib.request
# OpenAI-compatible endpoint (see extract.py). Defaults to DeepSeek; override with
# LLM_BASE_URL / LLM_MODEL + an API key to use OpenAI or any compatible server.
KEY = (os.environ.get("LLM_API_KEY") or os.environ.get("OPENAI_API_KEY")
       or os.environ.get("DEEPSEEK_API_KEY")
       or sys.exit("set an API key: LLM_API_KEY (or OPENAI_API_KEY / DEEPSEEK_API_KEY)"))
BASE = (os.environ.get("LLM_BASE_URL") or os.environ.get("OPENAI_BASE_URL")
        or "https://api.deepseek.com/v1").rstrip("/")
MODEL = os.environ.get("LLM_MODEL") or "deepseek-v4-flash"
IS_DEEPSEEK = "deepseek" in BASE.lower()
FACTS, SRC = sys.argv[1], sys.argv[2]
src = open(SRC, encoding="utf-8").read()

def canon(s):
    s = re.sub(r"`([^`]+)`", r"\1", s); s = re.sub(r"\*\*([^*]+)\*\*", r"\1", s)
    return re.sub(r"\s+", " ", s).strip().lower()

def chunks(text, size=3500):
    out, cur = [], ""
    for p in re.split(r"\n\s*\n", text):
        if len(cur) + len(p) > size and cur: out.append(cur); cur = p
        else: cur = (cur + "\n\n" + p) if cur else p
    if cur.strip(): out.append(cur)
    return out
CHUNKS = [(c, canon(c)) for c in chunks(src)]
def find_part(quote):                                  # the ACTUAL doc part the fact came from
    q = canon(quote)
    for raw, cc in CHUNKS:
        if q and q in cc: return raw
    return None

VAGUE = ("behaviour changed", "behavior changed", "has changed", "was updated", "is different",
         "changed the", "been changed", "now behaves", "different behavior", "different behaviour",
         "was modified", "is now handled differently")
def is_vague(f):
    t = (f.get("truth") or "").lower()
    if any(v in t for v in VAGUE): return True
    if f.get("type") == "CHANGED" and not f.get("new") and not re.search(r"[`(]|->|::| to ", f.get("truth", "")):
        return True
    return False

SYS = ("You refine ONE extracted fact into a CONCRETE, output-explicit sentence a developer can ACT "
 "on, using ONLY the SOURCE TEXT provided. Say exactly what to STOP using and what to USE instead, "
 "or what the new behaviour concretely IS (e.g. 'you now get an empty list, not None'). NEVER vague "
 "('behaviour changed'). Do NOT invent anything not supported by the source text. If the fact is "
 'already concrete, return it unchanged.\nOutput ONLY JSON: {"truth":"..."}')

def ask(part, truth):
    payload = {"model": MODEL, "temperature": 0.2, "stream": False,
        "response_format": {"type": "json_object"}, "max_tokens": 300,
        "messages": [{"role": "system", "content": SYS},
                     {"role": "user", "content": f"SOURCE TEXT:\n{part}\n\nFACT: {truth}"}]}
    if IS_DEEPSEEK:
        payload["thinking"] = {"type": "disabled"}   # DeepSeek-only; OpenAI-compatible servers 400 on it
    b = json.dumps(payload).encode()
    d = json.loads(urllib.request.urlopen(urllib.request.Request(f"{BASE}/chat/completions", data=b,
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {KEY}"}), timeout=120).read())
    return json.loads(d["choices"][0]["message"]["content"]).get("truth", "").strip()

facts = [json.loads(l) for l in open(FACTS, encoding="utf-8")]
diffs, rewritten, no_part = [], 0, 0
for f in facts:
    if not is_vague(f): continue
    part = find_part(f.get("quote", ""))
    if not part: no_part += 1; continue                # can't ground -> leave untouched
    old = f["truth"]
    try:
        nt = ask(part, old)
    except Exception:
        continue
    if nt and nt != old and 8 <= len(nt) <= 220:
        f["truth"] = nt; f["_concrete"] = True; rewritten += 1
        diffs.append((f.get("subject"), old, nt))
with open(FACTS.replace(".jsonl", ".concrete.jsonl"), "w", encoding="utf-8") as fh:
    for f in facts: fh.write(json.dumps(f, ensure_ascii=False) + "\n")
with open(FACTS.replace(".jsonl", ".concrete.diff.md"), "w", encoding="utf-8") as fh:
    fh.write(f"# Concrete-rewrite diff: {rewritten} rewritten / {len(facts)} facts "
             f"({no_part} vague but source-part not found, left as-is)\n\n")
    for subj, a, b in diffs:
        fh.write(f"### {subj}\n- BEFORE: {a}\n- AFTER:  {b}\n\n")
print(f"rewritten {rewritten}/{len(facts)} vague facts (grounded in source) | {no_part} ungroundable")
print(f"READ: {FACTS.replace('.jsonl', '.concrete.diff.md')}")
