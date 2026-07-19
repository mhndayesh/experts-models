#!/usr/bin/env python3
"""llm_extract2.py - STRICTER schema test. Two changes from v1, both about NOT asking the
model to do code's job:
  1. function-calling (DeepSeek supports it; json_schema it does NOT) enforces SHAPE:
     required fields present, correct types, why_it_bites/type from an enum.
  2. code DERIVES what it can, so the model can't get it wrong:
       - type: reconciled against `new` (new present + said REMOVED -> REPLACED)
       - from_fact keywords: pulled from old/new/truth in CODE (always grounded)
     The model fills ONLY the meaning: subject, old, new?, truth, why, quote, associative.

The raw checker then only has REAL grounding left to catch (quote verbatim, old in source,
truth concrete) - the schema-adherence slop is gone by design.
usage: DEEPSEEK_API_KEY=... python llm_extract2.py <source> <lib> <version>
out:   <lib>.facts.jsonl
"""
import hashlib, json, os, re, sys, urllib.request
# LLM endpoint — OpenAI-compatible. Defaults to DeepSeek (the project's proven,
# ~4¢/lib extractor), but works with OpenAI or ANY OpenAI-compatible server: set
# LLM_BASE_URL + LLM_MODEL and an API key. Function-calling is standard OpenAI;
# the only DeepSeek-specific field (`thinking:{disabled}`) is sent ONLY when the
# endpoint is DeepSeek, because other servers 400 on an unknown field.
#   DeepSeek (default):  DEEPSEEK_API_KEY=sk-...  python run.py <src> <lib> <ver>
#   OpenAI:  OPENAI_API_KEY=sk-...  LLM_BASE_URL=https://api.openai.com/v1  LLM_MODEL=gpt-4.1  python ...
#   Local (llama-server/vLLM/Ollama-OpenAI):  LLM_BASE_URL=http://127.0.0.1:8080/v1  LLM_MODEL=... LLM_API_KEY=x
KEY = (os.environ.get("LLM_API_KEY") or os.environ.get("OPENAI_API_KEY")
       or os.environ.get("DEEPSEEK_API_KEY")
       or sys.exit("set an API key: LLM_API_KEY (or OPENAI_API_KEY / DEEPSEEK_API_KEY)"))
BASE = (os.environ.get("LLM_BASE_URL") or os.environ.get("OPENAI_BASE_URL")
        or "https://api.deepseek.com/v1").rstrip("/")
MODEL = os.environ.get("LLM_MODEL") or "deepseek-v4-flash"
IS_DEEPSEEK = "deepseek" in BASE.lower()
SRC = sys.argv[1]; LIB = sys.argv[2] if len(sys.argv) > 2 else "lib"
VER = sys.argv[3] if len(sys.argv) > 3 else "x"

SYS = ("You extract ONLY breaking changes (removals, renames/replacements, behaviour changes "
"that break or silently misbehave existing code) from software docs. IGNORE new features, bug "
"fixes, internal refactors, docs, tests. Call emit_facts once with every breaking change you find. "
"quote MUST be copied VERBATIM from the text. truth must be ONE concrete, actionable sentence "
"(what to stop using + what to use, or what the new behaviour concretely IS) - never vague. "
"associative = 5-8 short (2-6 word) phrases a dev would TYPE when they hit this but that are NOT "
"literally in the fact. COVER ALL THREE kinds: (1) the underlying TASK in plain words (e.g. "
"'validate string length', 'limit field size'), (2) a natural QUESTION ('how long can a field be'), "
"(3) the SYMPTOM/concept. Write as someone who does NOT know the API name (e.g. an API that connects "
"to a provider gets 'connect to provider', 'set up client').")

TOOL = [{"type": "function", "function": {"name": "emit_facts",
  "description": "Emit all breaking-change facts found in the text.",
  "parameters": {"type": "object", "properties": {"facts": {"type": "array", "items": {
    "type": "object", "properties": {
      "type": {"type": "string", "enum": ["REMOVED", "REPLACED", "CHANGED"]},
      "subject": {"type": "string"}, "old": {"type": "string"},
      "new": {"type": ["string", "null"]}, "truth": {"type": "string"},
      "why_it_bites": {"type": "string", "enum": ["post-cutoff", "reverses-habit", "silent-failure"]},
      "quote": {"type": "string"},
      "associative": {"type": "array", "items": {"type": "string"}}},
    "required": ["type", "subject", "old", "truth", "why_it_bites", "quote", "associative"]}}},
  "required": ["facts"]}}}]

def chunks(text, size=3500):
    out, cur = [], ""
    for para in re.split(r"\n\s*\n", text):
        if len(cur) + len(para) > size and cur: out.append(cur); cur = para
        else: cur = (cur + "\n\n" + para) if cur else para
    if cur.strip(): out.append(cur)
    return out

def ask(chunk):
    payload = {"model": MODEL, "temperature": 0.2, "stream": False, "tools": TOOL,
        "tool_choice": {"type": "function", "function": {"name": "emit_facts"}}, "max_tokens": 8000,
        "messages": [{"role": "system", "content": SYS},
                     {"role": "user", "content": f"library: {LIB} (version ~{VER})\n\nTEXT:\n{chunk}"}]}
    if IS_DEEPSEEK:
        payload["thinking"] = {"type": "disabled"}   # DeepSeek-only; OpenAI-compatible servers 400 on it
    body = json.dumps(payload).encode()
    r = urllib.request.urlopen(urllib.request.Request(f"{BASE}/chat/completions", data=body,
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {KEY}"}), timeout=180)
    msg = json.loads(r.read())["choices"][0]["message"]
    facts = []
    for tc in (msg.get("tool_calls") or []):
        try: facts += json.loads(tc["function"]["arguments"]).get("facts", [])
        except Exception: pass
    return facts

SYM = re.compile(r"[A-Za-z_][A-Za-z0-9_]*(?:[./][A-Za-z0-9_]+)+|[A-Za-z_][A-Za-z0-9_]*\(\)|:[a-z_]\w+")
def derive_from_fact(f):
    """from_fact = the symbols code can SEE in old/new/truth. Always grounded."""
    kws = []
    for v in (f.get("old"), f.get("new")):
        if v: kws.append(str(v).lower())
    for m in SYM.findall(f.get("truth") or ""):
        kws.append(m.lower())
    out, seen = [], set()
    for k in kws:
        if k and k not in seen: seen.add(k); out.append(k)
    return out[:8]

def cid(f):
    # Content-complete id: include lib + version + a truth prefix so two DISTINCT
    # facts can never collide just because type|subject|old|new match (the old key
    # hashed only those four, so any facts with null subject/old/new collided -
    # that produced 19 duplicate-id groups incl. a cross-library flask/hf-datasets
    # clash). Deterministic and stable per (lib, version, content).
    key = (f"{f.get('lib')}|{f.get('version')}|{f['type']}|{f.get('subject')}|"
           f"{f.get('old')}|{f.get('new')}|{(f.get('truth') or '')[:80]}")
    return "sx-" + hashlib.sha256(key.encode()).hexdigest()[:10]

def main():
    text = open(SRC, encoding="utf-8").read()
    cks = chunks(text)
    print(f"{SRC}: {len(text)} chars -> {len(cks)} chunks")
    facts = []
    for i, ck in enumerate(cks, 1):
        try: got = ask(ck)
        except Exception as e: print(f"  chunk {i}: ERR {type(e).__name__}: {e}"); got = []
        for f in got:
            # DERIVE in code: reconcile type vs new, build from_fact, stamp meta
            # coerce any out-of-enum type the LLM invents (e.g. DEPRECATED, ADDED)
            # from the `new`-presence signal: has replacement -> REPLACED, else REMOVED
            if f.get("type") not in ("REMOVED", "REPLACED", "CHANGED"):
                f["type"] = "REPLACED" if f.get("new") else "REMOVED"
            if f.get("new") and f.get("type") == "REMOVED": f["type"] = "REPLACED"
            if not f.get("new") and f.get("type") == "REPLACED": f["type"] = "REMOVED"
            # coerce why_it_bites the same way: the model sometimes invents a
            # near-synonym (e.g. 'behaviour-change') that check.py then rejects,
            # silently losing a valid fact. Anything outside the enum is a
            # behaviour change we couldn't bucket -> silent-failure.
            if f.get("why_it_bites") not in ("post-cutoff", "reverses-habit", "silent-failure"):
                f["why_it_bites"] = "silent-failure"
            ff = derive_from_fact(f); ffset = set(ff)
            asso = [a for a in f.pop("associative", []) if str(a).lower().strip() not in ffset]
            f["keywords"] = {"from_fact": ff, "associative": asso}
            f["lib"] = LIB; f["version"] = VER; f["id"] = cid(f)
            facts.append(f)
        print(f"  chunk {i}/{len(cks)}: {len(got)} facts")
    seen, uniq = set(), []
    for f in facts:
        if f["id"] in seen: continue
        seen.add(f["id"]); uniq.append(f)
    with open(f"{LIB}.facts.jsonl", "w", encoding="utf-8") as fh:
        for f in uniq: fh.write(json.dumps(f, ensure_ascii=False) + "\n")
    print(f"\n{len(uniq)} unique facts -> {LIB}.facts.jsonl")

if __name__ == "__main__":
    main()
