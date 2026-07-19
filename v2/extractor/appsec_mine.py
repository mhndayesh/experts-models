#!/usr/bin/env python3
"""appsec_mine.py - Extractor 2.0 (code-carrying). Mines MITRE CWE into insecure-by-default
landmine facts that carry VERBATIM bad/good code lifted from the source.

Design laws (do not violate):
  - The CODE and the security claims in the source are GROUND TRUTH (MITRE CWE). DeepSeek SELECTS and
    COPIES verbatim; it never rewrites, reformats, fixes, shortens, or invents code or facts.
  - code_bad / code_good must each be a VERBATIM substring of the source (modulo whitespace) or they are
    dropped. A fact with code_bad MUST also have code_good (never ship a vuln snippet without its fix).
  - The prose `quote` stays the anti-hallucination anchor (verbatim in source). Code is grounded separately,
    NEVER through canon() (case + punctuation are load-bearing in code).
  - LLM does meaning; code verifies every field. Read the output by hand; the count lies.

usage:  DEEPSEEK_API_KEY=$(cat /c/projects/api/deepseek.txt) python appsec_mine.py [--n N] [--critic] [--pairs-only]
out:    experts/appsec/facts/cwe.jsonl   (+ cwe.rejects.jsonl)
"""
import hashlib, json, os, re, sys, glob, urllib.request
import xml.etree.ElementTree as ET

KEY  = (os.environ.get("LLM_API_KEY") or os.environ.get("DEEPSEEK_API_KEY")
        or sys.exit("set DEEPSEEK_API_KEY"))
BASE = (os.environ.get("LLM_BASE_URL") or "https://api.deepseek.com/v1").rstrip("/")
MODEL = os.environ.get("LLM_MODEL") or "deepseek-v4-flash"
IS_DEEPSEEK = "deepseek" in BASE.lower()

HERE = os.path.dirname(os.path.abspath(__file__))
CWE_XML = glob.glob(os.path.join(HERE, "..", "..", "appsec-corpus", "cwe", "*.xml"))
CWE_XML = CWE_XML[0] if CWE_XML else sys.exit("CWE xml not found in appsec-corpus/cwe/")
OUTDIR = os.path.join(HERE, "experts", "appsec", "facts")
LICENSE_NOTE = "© The MITRE Corporation, reproduced with permission (CWE)"

DOORS = ["injection","web-appsec","crypto","auth-session","memory-safety",
         "deserialization-input","secrets-config","network-security","concurrency-race","api-supply-chain"]
TYPES = ["INSECURE_DEFAULT","HABIT_REVERSAL","SILENT_FAILURE","DEPRECATED_CRYPTO","MISSING_CONTROL"]
HW_LANGS = {"verilog","vhdl","systemverilog"}

# Curated SECURITY CWE set (source-targeting inside CWE): CWE Top 25 + OWASP-Top-10 mappings + the
# well-known exploitable injection/crypto/authz/memory weaknesses + a few good modern ones. Excludes the
# hardware (1194 view) and code-quality clusters that dilute bite.
SECURITY_CWES = set(map(str, [
 # --- injection ---
 89,78,77,79,80,83,87,88,94,95,96,90,91,643,611,917,943,1236,113,116,74,75,1427,
 # --- memory safety ---
 787,125,416,476,190,191,119,120,121,122,124,126,127,131,134,170,415,401,457,562,197,681,469,20,129,
 # --- auth / authz / session ---
 287,306,288,302,307,384,613,620,640,798,259,321,522,269,285,862,863,565,521,620,
 # --- crypto ---
 327,328,916,326,330,338,335,759,760,347,295,319,311,312,313,322,323,324,325,329,331,336,337,340,547,780,
 # --- web / appsec ---
 352,601,434,614,1004,732,276,200,209,532,538,548,22,23,36,73,98,918,444,1021,1275,
 # --- deserialization / input ---
 502,470,915,913,1284,
 # --- secrets / config ---
 489,1188,15,526,
 # --- resource / dos ---
 400,770,772,674,1333,834,405,
 # --- supply chain / integrity ---
 494,829,345,353,354,830,
 # --- concurrency ---
 362,367,364,366,
]))

# ---------------- CWE parsing ----------------
def lt(e): return e.tag.split('}')[-1]
def code_text(e):
    """Serialize an Example_Code element preserving line breaks (xhtml br/div/p -> newline)."""
    parts=[]
    def rec(el):
        if lt(el) in ('br','div','p','li','tr'): parts.append('\n')
        if el.text: parts.append(el.text)
        for ch in el:
            rec(ch)
            if ch.tail: parts.append(ch.tail)
    rec(e)
    return re.sub(r'\n{3,}', '\n\n', ''.join(parts)).strip()
def plain(e):
    return ' '.join(''.join(e.itertext()).split())

def parse_cwe():
    root = ET.fromstring(open(CWE_XML, encoding="utf-8").read())
    out=[]
    for w in root.iter():
        if lt(w)!='Weakness': continue
        rec={"id":w.get('ID'),"name":w.get('Name'),"desc":"","ext":"","examples":[],"mitigations":[]}
        for c in w:
            t=lt(c)
            if t=='Description': rec["desc"]=plain(c)
            elif t=='Extended_Description': rec["ext"]=plain(c)
            elif t=='Demonstrative_Examples':
                for ex in c.iter():
                    if lt(ex)=='Example_Code':
                        rec["examples"].append({"nature":ex.get('Nature'),"lang":ex.get('Language'),
                                                "code":code_text(ex)})
            elif t=='Potential_Mitigations':
                for m in c.iter():
                    if lt(m)=='Mitigation':
                        txt=plain(m)
                        if txt: rec["mitigations"].append(txt[:400])
        out.append(rec)
    return out

# ---------------- LLM ----------------
SYS = (
"You turn a MITRE CWE weakness into 'insecure-by-default' landmine facts for a code-generation model. "
"A landmine fact captures a pattern that a model tends to WRITE INSECURELY BY DEFAULT (the idiomatic/obvious "
"code is exploitable), and pairs the vulnerable code with its secure fix.\n"
"GROUND TRUTH RULE (absolute): the CWE text and its code examples are authoritative and CORRECT. You SELECT "
"and COPY; you do NOT rewrite, reformat, fix, shorten, translate, or 'improve' any code, and you do NOT "
"change the meaning of a fact. Never invent code.\n"
"For each fact:\n"
"- code_bad: copy VERBATIM, character-for-character, from a Bad/vulnerable Example_Code block. Do not edit it.\n"
"- code_good: copy VERBATIM from a Good/fixed Example_Code block if one exists. If there is NO verbatim good "
"example in the source, set BOTH code_bad and code_good to null and make it a text-only fact (still fill truth).\n"
"- Never output a fact with code_bad but no code_good.\n"
"- truth: ONE concrete, actionable sentence (stop doing X; do Y instead). Never vague.\n"
"- quote: a SHORT phrase copied VERBATIM from the weakness description or a mitigation (the anchor).\n"
"- lang: the Example_Code Language (lowercase) or the fix's language; 'text' if unknown.\n"
"- door: the single best of the given enum.\n"
"- type: INSECURE_DEFAULT (obvious code is exploitable) | HABIT_REVERSAL (trained default is wrong) | "
"SILENT_FAILURE (wrong-but-runs) | DEPRECATED_CRYPTO | MISSING_CONTROL.\n"
"- associative: 5-8 short phrases a dev would TYPE when about to write this insecure code, that are NOT in the "
"fact (e.g. 'run a sql query with a variable', 'hash a password', 'parse untrusted json').\n"
"Emit 1-4 facts per weakness (the most bite-y). Call emit_facts once.")

TOOL=[{"type":"function","function":{"name":"emit_facts",
 "description":"Emit insecure-by-default landmine facts (with verbatim code) for this weakness.",
 "parameters":{"type":"object","properties":{"facts":{"type":"array","items":{"type":"object","properties":{
   "type":{"type":"string","enum":TYPES},
   "subject":{"type":"string"},
   "truth":{"type":"string"},
   "why_it_bites":{"type":"string","enum":["insecure-default","habit-reversal","silent-failure","post-cutoff"]},
   "quote":{"type":"string"},
   "code_bad":{"type":["string","null"]},
   "code_good":{"type":["string","null"]},
   "lang":{"type":["string","null"]},
   "door":{"type":"string","enum":DOORS},
   "associative":{"type":"array","items":{"type":"string"}}},
   "required":["type","subject","truth","why_it_bites","quote","door","associative"]}}},
  "required":["facts"]}}}]

def call(messages, tool_name):
    payload={"model":MODEL,"temperature":0.1,"stream":False,"tools":TOOL,
             "tool_choice":{"type":"function","function":{"name":tool_name}},"max_tokens":8000,
             "messages":messages}
    if IS_DEEPSEEK: payload["thinking"]={"type":"disabled"}
    body=json.dumps(payload).encode()
    r=urllib.request.urlopen(urllib.request.Request(f"{BASE}/chat/completions",data=body,
        headers={"Content-Type":"application/json","Authorization":f"Bearer {KEY}"}),timeout=180)
    msg=json.loads(r.read())["choices"][0]["message"]
    out=[]
    for tc in (msg.get("tool_calls") or []):
        try: out+=json.loads(tc["function"]["arguments"]).get("facts",[])
        except json.JSONDecodeError as e:
            print(f"    !! JSON parse fail (len={len(tc['function']['arguments'])}): {e}")
    return out

def build_input(w):
    L=[f"CWE-{w['id']}: {w['name']}", "", "DESCRIPTION:", w['desc']]
    if w['ext']: L += ["", w['ext'][:600]]
    for i,ex in enumerate(w['examples']):
        if ex['code']:
            L += ["", f"EXAMPLE_CODE [{ex['nature']}] (language={ex['lang']}):", ex['code']]
    if w['mitigations']:
        L += ["", "MITIGATIONS:"] + [f"- {m}" for m in w['mitigations'][:4]]
    return "\n".join(L)

# ---------------- grounding (code-aware, never canon()) ----------------
def gnorm(s):  # collapse ALL whitespace to single space, KEEP case + punctuation
    return re.sub(r"\s+"," ", s or "").strip()
def grounded(snippet, corpus):
    n=gnorm(snippet)
    return len(n)>=12 and n in gnorm(corpus)
def py_ok(code, lang):
    if (lang or "").lower() not in ("python","py"): return True
    try: compile(code,"<good>","exec"); return True
    except SyntaxError: return False

def repair_quote(quote, corpus):
    """No-LLM re-grounding: if the quote isn't verbatim, snap it to the best-overlapping real source
    line/sentence. Recovers facts whose quote was paraphrased, abbreviated with '...', or was a short
    code symbol the model put in the quote field. The fact is already scoped to this weakness, so any
    real line here is a valid provenance anchor."""
    # first try grounding each ellipsis-separated fragment verbatim (model abbreviates with '...')
    for frag in re.split(r'\s*\.\.\.\s*', quote or ""):
        if grounded(frag, corpus): return frag.strip()
    q=set(re.findall(r'[a-z0-9]+', (quote or "").lower()))
    if not q: return None
    best,bs=None,0.0
    for p in re.split(r'(?<=[.;:])\s+|\n+', corpus):
        p=p.strip()
        if len(p)<12: continue
        pw=set(re.findall(r'[a-z0-9]+', p.lower()))
        ov=len(q & pw)/len(q)
        if ov>bs: bs,best=ov,p
    return best[:200] if bs>=0.5 else None

# CWE -> door (deterministic; overrides the LLM's guess for retrieval consistency)
DOOR_MAP={str(c):d for d,cs in {
  "injection":[89,78,77,88,94,95,96,90,91,643,611,917,943,1236,113,116,74,75,1427,79,80,83,87],
  "memory-safety":[787,125,416,476,190,191,119,120,121,122,124,126,127,131,134,170,415,401,457,562,197,681,469,129,20],
  "crypto":[327,328,916,326,330,338,335,759,760,347,319,311,312,313,322,323,324,325,329,331,336,337,340,547,780],
  "auth-session":[287,306,288,302,307,384,613,620,640,259,565,521,285,862,863,269],
  "web-appsec":[352,601,434,614,1004,732,276,538,548,22,23,36,73,98,444,1021,1275],
  "deserialization-input":[502,470,915,913,1284],
  "secrets-config":[798,522,321,489,1188,15,526,532,209,200],
  "network-security":[918,523,295],
  "concurrency-race":[362,367,364,366],
  "api-supply-chain":[494,829,345,353,354,830,400,770,772,674,1333,834,405],
}.items() for c in cs}

def dedupe(facts):
    """Collapse near-duplicate facts (token-set Jaccard >=0.6 on subject+truth); keep longest truth."""
    def tk(f): return set(re.findall(r'[a-z0-9]+', ((f.get('subject') or '')+' '+(f.get('truth') or '')).lower()))
    kept, sigs = [], []
    for f in sorted(facts, key=lambda x:-len(x.get('truth') or '')):
        s=tk(f)
        if any(len(s & o)/max(1,len(s | o))>=0.6 for o in sigs): continue
        sigs.append(s); kept.append(f)
    return kept

SYM=re.compile(r"[A-Za-z_][A-Za-z0-9_]*(?:[.\-/][A-Za-z0-9_]+)+|[A-Za-z_][A-Za-z0-9_]*\(|=[A-Za-z_]\w*|\b(?:md5|sha1|pickle|eval|exec|system|strcpy|gets|yaml\.load)\b")
def keywords(f):
    ks=[]
    for src in (f.get("code_bad"), f.get("subject"), f.get("truth")):
        for m in SYM.findall(src or ""): ks.append(m.lower().rstrip("("))
    out,seen=[],set()
    for k in ks:
        if k and len(k)>1 and k not in seen: seen.add(k); out.append(k)
    return out[:12]

def cid(f):
    key=f"{f.get('weakness')}|{f['type']}|{f.get('subject')}|{(f.get('truth') or '')[:80]}|{gnorm(f.get('code_bad') or '')[:60]}"
    return "ax-"+hashlib.sha256(key.encode()).hexdigest()[:10]

def main():
    n=int(sys.argv[sys.argv.index("--n")+1]) if "--n" in sys.argv else 12
    pairs_only = "--pairs-only" in sys.argv
    ws=parse_cwe()
    # SOFTWARE only: CWE's 1000+ range is hardware-heavy (Verilog/VHDL) and useless for a code-gen
    # appsec model. Require a Bad example in a software language.
    SOFTWARE_LANGS={'c','c++','java','javascript','python','php','c#','go','ruby','perl','sql','html',
                    'asp.net','shell','bash','typescript','xml','json'}
    curated = "--all" not in sys.argv   # default: only curated SECURITY CWEs (source-targeting)
    def natures(w): return {e['nature'] for e in w['examples'] if e['code']}
    def sw_bad(w): return any(e['nature']=='Bad' and (e['lang'] or '').lower() in SOFTWARE_LANGS
                              for e in w['examples'] if e['code'])
    def ok(w):
        if not sw_bad(w): return False
        if curated and w['id'] not in SECURITY_CWES: return False
        return ({'Bad','Good'} <= natures(w)) if pairs_only else ('Bad' in natures(w))
    cand=[w for w in ws if ok(w)][:n]
    print(f"CWE: {len(ws)} weaknesses; mining {len(cand)} (curated={curated}, pairs_only={pairs_only})")
    os.makedirs(OUTDIR, exist_ok=True)
    kept, rej = [], []
    for w in cand:
        corpus = build_input(w)   # grounding corpus = the exact text we showed the model (verbatim code incl.)
        msgs=[{"role":"system","content":SYS},{"role":"user","content":corpus}]
        try: facts=call(msgs,"emit_facts")
        except Exception as e: print(f"  CWE-{w['id']}: ERR {type(e).__name__}: {e}"); continue
        nk=0
        for f in facts:
            if (f.get("lang") or "").lower() in HW_LANGS: continue   # per-fact hardware drop (Verilog/VHDL)
            f["weakness"]=f"CWE-{w['id']}"; f["source"]=f"CWE-{w['id']}"; f["license_note"]=LICENSE_NOTE
            f["lib"]=f"cwe-{w['id']}"; f["version"]="cwe4.20"
            if f.get("type") not in TYPES: f["type"]="INSECURE_DEFAULT"   # coerce invented types
            if f.get("why_it_bites") not in ("insecure-default","habit-reversal","silent-failure","post-cutoff"):
                f["why_it_bites"]="insecure-default"
            cb, cg = f.get("code_bad"), f.get("code_good")
            # code-grounding: both must be verbatim-in-source; bad requires good
            reason=None
            if cb or cg:
                if not (cb and cg): reason="code_bad without code_good (or vice versa)"
                elif not grounded(cb, corpus): reason="code_bad not verbatim in source"
                elif not grounded(cg, corpus): reason="code_good not verbatim in source"
                elif not py_ok(cg, f.get("lang")): reason="code_good fails python syntax check"
            if reason:
                # demote to text-only rather than lose the fact (unless the claim itself is ungrounded)
                f["_code_dropped"]=reason; f["code_bad"]=None; f["code_good"]=None
            # prose quote anchor (verbatim in the weakness text); repair paraphrased quotes
            rq=repair_quote(f.get("quote",""), corpus)
            if rq: f["quote"]=rq
            else: f["_quote_ungrounded"]=True
            # deterministic door from the CWE map (overrides LLM guess), else the LLM's if valid
            f["door"]=DOOR_MAP.get(w['id']) or (f["door"] if f.get("door") in DOORS else "web-appsec")
            f["keywords"]={"from_fact":keywords(f),"associative":[a for a in f.get("associative",[]) if a][:8]}
            f.pop("associative",None)
            f["id"]=cid(f)
            # hard reject only if the CLAIM is ungrounded (quote not in source)
            if f.get("_quote_ungrounded"):
                rej.append(f); continue
            kept.append(f); nk+=1
        hascode=sum(1 for f in kept[-nk:] if f.get("code_bad"))
        print(f"  CWE-{w['id']:>5} {w['name'][:44]:44s} -> {nk} facts ({hascode} w/code)")
    # de-dup by id
    seen,uniq=set(),[]
    for f in kept:
        if f["id"] in seen: continue
        seen.add(f["id"]); uniq.append(f)
    before=len(uniq); uniq=dedupe(uniq)
    print(f"dedupe: {before} -> {len(uniq)}")
    with open(os.path.join(OUTDIR,"cwe.jsonl"),"w",encoding="utf-8") as fh:
        for f in uniq: fh.write(json.dumps(f,ensure_ascii=False)+"\n")
    with open(os.path.join(OUTDIR,"cwe.rejects.jsonl"),"w",encoding="utf-8") as fh:
        for f in rej: fh.write(json.dumps(f,ensure_ascii=False)+"\n")
    withcode=sum(1 for f in uniq if f.get("code_bad"))
    print(f"\n{len(uniq)} facts ({withcode} carry verbatim bad+good code) -> experts/appsec/facts/cwe.jsonl")
    print(f"{len(rej)} rejected (ungrounded quote) -> cwe.rejects.jsonl")

if __name__=="__main__":
    main()
