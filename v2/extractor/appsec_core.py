#!/usr/bin/env python3
"""appsec_core.py - shared Extractor-2.0 pipeline for the appsec bank. Every source is a thin ADAPTER
that produces `items` (structured text + grounding corpus); this module runs the same proven drill:
  extract (LLM, verbatim code) -> code-ground -> repair quote -> door -> dedupe -> write + rejects.

Design laws (see ../decisions/REAL-SECURITY-EXPERT-PLAN.md):
  - Code + facts are GROUND TRUTH: the LLM SELECTS and COPIES verbatim; never rewrites/invents code.
  - code_bad/code_good must be verbatim-in-source (modulo whitespace), NEVER via canon(); bad requires good.
  - prose `quote` is the anti-hallucination anchor (verbatim, else repair-snap to the nearest source line).
  - LLM does meaning; code verifies every field. SCORE MANUALLY afterwards.

An adapter calls:  run(items, out_prefix, extra_sys="")   where each item is:
  {"llm_input": <text shown to the model>, "corpus": <verbatim text to ground against>,
   "source": <"CWE-89"|"CodeQL js/...">, "license_note": <attribution>, "lib": <id>, "version": <str>,
   "door": <optional forced door>}
"""
import hashlib, json, os, re, sys, urllib.request

KEY  = (os.environ.get("LLM_API_KEY") or os.environ.get("DEEPSEEK_API_KEY") or "")
BASE = (os.environ.get("LLM_BASE_URL") or "https://api.deepseek.com/v1").rstrip("/")
MODEL = os.environ.get("LLM_MODEL") or "deepseek-v4-flash"
IS_DEEPSEEK = "deepseek" in BASE.lower()

DOORS = ["injection","web-appsec","crypto","auth-session","memory-safety",
         "deserialization-input","secrets-config","network-security","concurrency-race","api-supply-chain"]
TYPES = ["INSECURE_DEFAULT","HABIT_REVERSAL","SILENT_FAILURE","DEPRECATED_CRYPTO","MISSING_CONTROL"]
WHYS  = ["insecure-default","habit-reversal","silent-failure","post-cutoff"]
HW_LANGS = {"verilog","vhdl","systemverilog"}

SYS = (
"You turn a software-security source into 'insecure-by-default' landmine facts for a code-generation model. "
"A landmine fact captures a pattern a model tends to WRITE INSECURELY BY DEFAULT (the idiomatic/obvious code "
"is exploitable), and pairs the vulnerable code with its secure fix.\n"
"GROUND TRUTH RULE (absolute): the source text and its code examples are authoritative and CORRECT. You "
"SELECT and COPY; you do NOT rewrite, reformat, fix, shorten, translate, or 'improve' any code, and you do "
"NOT change the meaning of a fact. Never invent code.\n"
"- code_bad: copy VERBATIM from a vulnerable/bad/noncompliant code block. code_good: copy VERBATIM from a "
"fixed/good/compliant code block if one exists. If there is NO verbatim good example, set BOTH to null and "
"make it a text-only fact. Never output code_bad without code_good.\n"
"- truth: ONE concrete actionable sentence (stop X; do Y). quote: a SHORT phrase copied VERBATIM from the "
"prose (the anchor). lang: the code language lowercased, or 'text'. door: the single best of the enum.\n"
"- associative: 5-8 short phrases a dev would TYPE when about to write this insecure code, not in the fact.\n"
"Emit 1-4 of the most bite-y facts. Call emit_facts once.")

def tool(): return [{"type":"function","function":{"name":"emit_facts",
 "description":"Emit insecure-by-default landmine facts (with verbatim code) for this item.",
 "parameters":{"type":"object","properties":{"facts":{"type":"array","items":{"type":"object","properties":{
   "type":{"type":"string","enum":TYPES},"subject":{"type":"string"},"truth":{"type":"string"},
   "why_it_bites":{"type":"string","enum":WHYS},"quote":{"type":"string"},
   "code_bad":{"type":["string","null"]},"code_good":{"type":["string","null"]},
   "lang":{"type":["string","null"]},"door":{"type":"string","enum":DOORS},
   "associative":{"type":"array","items":{"type":"string"}}},
   "required":["type","subject","truth","why_it_bites","quote","door","associative"]}}},"required":["facts"]}}}]

def call(llm_input, extra_sys=""):
    payload={"model":MODEL,"temperature":0.1,"stream":False,"tools":tool(),
             "tool_choice":{"type":"function","function":{"name":"emit_facts"}},"max_tokens":8000,
             "messages":[{"role":"system","content":SYS+("\n"+extra_sys if extra_sys else "")},
                         {"role":"user","content":llm_input}]}
    if IS_DEEPSEEK: payload["thinking"]={"type":"disabled"}
    r=urllib.request.urlopen(urllib.request.Request(f"{BASE}/chat/completions",
        data=json.dumps(payload).encode(),
        headers={"Content-Type":"application/json","Authorization":f"Bearer {KEY}"}),timeout=180)
    msg=json.loads(r.read())["choices"][0]["message"]; out=[]
    for tc in (msg.get("tool_calls") or []):
        try: out+=json.loads(tc["function"]["arguments"]).get("facts",[])
        except json.JSONDecodeError as e: print(f"    !! JSON parse fail (len={len(tc['function']['arguments'])}): {e}")
    return out

# --- grounding (code-aware, never canon()) ---
def gnorm(s): return re.sub(r"\s+"," ", s or "").strip()
def grounded(snippet, corpus):
    n=gnorm(snippet); return len(n)>=12 and n in gnorm(corpus)
def py_ok(code, lang):
    if (lang or "").lower() not in ("python","py"): return True
    try: compile(code,"<good>","exec"); return True
    except SyntaxError: return False
def repair_quote(quote, corpus):
    q=quote or ""
    gc=gnorm(corpus)
    # 1) verbatim grounding of the quote or a natural sub-span. Split on ellipses AND sentence
    #    boundaries so a multi-sentence quote whose FIRST sentence is verbatim (but whose full span
    #    isn't, e.g. a punctuation artifact or a mid-sentence newline) still grounds. Longest wins.
    best_g=None
    for frag in re.split(r'\s*\.\.\.\s*', q) + re.split(r'(?<=[.;:])\s+', q) + [q]:
        n=gnorm(frag)
        if len(n)>=12 and n in gc and (best_g is None or len(n)>len(gnorm(best_g))):
            best_g=frag.strip()
    if best_g: return best_g
    # 2) fallback: best token-overlap source line (paraphrased quote snaps to the nearest real line)
    qw=set(re.findall(r'[a-z0-9]+', q.lower()))
    if not qw: return None
    best,bs=None,0.0
    for p in re.split(r'(?<=[.;:])\s+|\n+', corpus):
        p=p.strip()
        if len(p)<12: continue
        pw=set(re.findall(r'[a-z0-9]+', p.lower()))
        ov=len(qw & pw)/len(qw)
        if ov>bs: bs,best=ov,p
    return best[:200] if bs>=0.5 else None

SYM=re.compile(r"[A-Za-z_][A-Za-z0-9_]*(?:[.\-/][A-Za-z0-9_]+)+|[A-Za-z_][A-Za-z0-9_]*\(|=[A-Za-z_]\w*")
def keywords(f):
    ks=[]
    for src in (f.get("code_bad"), f.get("subject"), f.get("truth")):
        for m in SYM.findall(src or ""): ks.append(m.lower().rstrip("("))
    out,seen=[],set()
    for k in ks:
        if k and len(k)>1 and k not in seen: seen.add(k); out.append(k)
    return out[:12]
def cid(f, prefix="ax"):
    key=f"{f.get('source')}|{f['type']}|{f.get('subject')}|{(f.get('truth') or '')[:80]}|{gnorm(f.get('code_bad') or '')[:60]}"
    return f"{prefix}-"+hashlib.sha256(key.encode()).hexdigest()[:10]
def dedupe(facts):
    def tk(f): return set(re.findall(r'[a-z0-9]+', ((f.get('subject') or '')+' '+(f.get('truth') or '')).lower()))
    kept,sigs=[],[]
    for f in sorted(facts, key=lambda x:-len(x.get('truth') or '')):
        s=tk(f)
        if any(len(s & o)/max(1,len(s | o))>=0.6 for o in sigs): continue
        sigs.append(s); kept.append(f)
    return kept

def run(items, out_prefix, extra_sys="", id_prefix="ax", verbose=True):
    """Mine a list of adapter items to <out_prefix>.jsonl (+ .rejects.jsonl). Returns (kept, rejects)."""
    if not KEY: sys.exit("set DEEPSEEK_API_KEY")
    kept, rej = [], []
    for it in items:
        corpus=it["corpus"]
        try: facts=call(it["llm_input"], extra_sys)
        except Exception as e:
            if verbose: print(f"  {it.get('source')}: ERR {type(e).__name__}: {e}")
            continue
        nk=0
        for f in facts:
            if (f.get("lang") or "").lower() in HW_LANGS: continue
            f["source"]=it["source"]; f["license_note"]=it["license_note"]
            f["lib"]=it["lib"]; f["version"]=it["version"]
            if f.get("type") not in TYPES: f["type"]="INSECURE_DEFAULT"
            if f.get("why_it_bites") not in WHYS: f["why_it_bites"]="insecure-default"
            cb,cg=f.get("code_bad"),f.get("code_good")
            if cb or cg:
                if not (cb and cg): f["_code_dropped"]="bad xor good"; f["code_bad"]=f["code_good"]=None
                elif not grounded(cb, corpus): f["_code_dropped"]="bad not verbatim"; f["code_bad"]=f["code_good"]=None
                elif not grounded(cg, corpus): f["_code_dropped"]="good not verbatim"; f["code_bad"]=f["code_good"]=None
                elif not py_ok(cg, f.get("lang")): f["_code_dropped"]="good bad-syntax"; f["code_bad"]=f["code_good"]=None
            rq=repair_quote(f.get("quote",""), corpus)
            if rq: f["quote"]=rq
            else: f["_quote_ungrounded"]=True
            f["door"]=it.get("door") or (f["door"] if f.get("door") in DOORS else "web-appsec")
            f["keywords"]={"from_fact":keywords(f),"associative":[a for a in f.get("associative",[]) if a][:8]}
            f.pop("associative",None)
            f["id"]=cid(f, id_prefix)
            if f.get("_quote_ungrounded"): rej.append(f); continue
            kept.append(f); nk+=1
        if verbose and nk:
            hc=sum(1 for x in kept[-nk:] if x.get("code_bad"))
            print(f"  {it.get('source'):>22} -> {nk} facts ({hc} w/code)")
    seen,uniq=set(),[]
    for f in kept:
        if f["id"] in seen: continue
        seen.add(f["id"]); uniq.append(f)
    before=len(uniq); uniq=dedupe(uniq)
    outdir=os.path.dirname(out_prefix); os.makedirs(outdir, exist_ok=True) if outdir else None
    with open(out_prefix+".jsonl","w",encoding="utf-8") as fh:
        for f in uniq: fh.write(json.dumps(f,ensure_ascii=False)+"\n")
    with open(out_prefix+".rejects.jsonl","w",encoding="utf-8") as fh:
        for f in rej: fh.write(json.dumps(f,ensure_ascii=False)+"\n")
    wc=sum(1 for f in uniq if f.get("code_bad"))
    if verbose: print(f"\ndedupe {before}->{len(uniq)} | {len(uniq)} facts ({wc} w/code) -> {out_prefix}.jsonl | {len(rej)} rejects")
    return uniq, rej
