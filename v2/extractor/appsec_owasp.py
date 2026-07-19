#!/usr/bin/env python3
"""appsec_owasp.py - OWASP Cheat Sheet Series adapter for the shared appsec pipeline (appsec_core).

Mines each cheatsheet into 'insecure-by-default' landmine facts carrying VERBATIM bad/good code.

Chunking: each cheatsheet is markdown with ## sections; a vulnerable example and its safe fix often
live in DIFFERENT sections (e.g. "Anatomy" vs "Defense Option 1"). So we pack CONSECUTIVE whole ##
sections into ~TARGET-char chunks (never splitting a code fence) so the bad/good pair lands in one
item's corpus and the model can pair them. The corpus is the exact chunk text (fences + prose) so
code grounds verbatim.

usage:
  DEEPSEEK_API_KEY=$(cat /c/projects/api/deepseek.txt) python appsec_owasp.py [--files A,B] [--limit N] [--dry]
out: experts/appsec/facts/owasp_cs.jsonl (+ .rejects.jsonl)
"""
import os, re, sys, glob
import appsec_core as C

HERE = os.path.dirname(os.path.abspath(__file__))
CS_DIR = os.path.join(HERE, "..", "..", "appsec-corpus", "owasp-cheatsheets", "cheatsheets")
LICENSE = "OWASP Cheat Sheet Series, CC BY-SA"
TARGET = 7000   # target chars per chunk (input side; never splits a fence)

# Cheatsheets that are pure process/policy/testing with little/no exploitable code — skip to keep bite.
SKIP = {
 "Abuse_Case", "Attack_Surface_Analysis", "Authorization_Testing_Automation",
 "Authorization_Regression_Testing", "Bot_Management_and_Anti-Automation", "Business_Logic_Security",
 "Choosing_and_Using_Security_Questions", "Threat_Modeling", "Vulnerability_Disclosure",
 "Vulnerable_Dependency_Management", "Secure_Product_Design", "Secure_Cloud_Architecture",
 "Third_Party_Javascript_Management", "AML_Sanctions_AI_Agent_Payments", "Security_Champions_Guide",
 "Web_Application_Security_Testing_and_Assessment", "Legacy_Application_Management",
}

def title_of(fname, text):
    m = re.search(r'(?m)^#\s+(.+)$', text)
    return m.group(1).strip() if m else os.path.basename(fname)

def lib_id(fname):
    base = re.sub(r'_Cheat_Sheet\.md$', '', os.path.basename(fname))
    return base.lower().replace('_', '-')

def split_h2(text):
    """Split into blocks at ## headings; keep each heading with its body. Preamble kept as block 0."""
    parts = re.split(r'(?m)^(##\s+.*)$', text)
    blocks = []
    if parts and parts[0].strip():
        blocks.append(parts[0].strip())
    for i in range(1, len(parts), 2):
        head = parts[i]
        body = parts[i + 1] if i + 1 < len(parts) else ""
        blocks.append((head + body).strip())
    return [b for b in blocks if b]

def pack(blocks, target=TARGET):
    """Greedily pack consecutive whole sections into ~target-char chunks (never splits a fence,
    because we only ever join whole sections)."""
    chunks, cur = [], ""
    for b in blocks:
        if cur and len(cur) + len(b) + 1 > target:
            chunks.append(cur); cur = b
        else:
            cur = (cur + "\n\n" + b) if cur else b
    if cur.strip():
        chunks.append(cur)
    return chunks

def substantive(chunk):
    """Keep chunks with a code fence, or long prose sections that carry a bad/good security pattern."""
    if "```" in chunk:
        return True
    low = chunk.lower()
    if len(chunk) < 500:
        return False
    # text-only but bite-y: do/don't security guidance
    hints = ("must ", "never ", "do not ", "don't ", "avoid ", "instead of", "insecure",
             "vulnerab", "attacker", "should not", "by default")
    return sum(h in low for h in hints) >= 2

EXTRA_SYS = (
"OWASP CHEAT SHEET RULES (this source):\n"
"- Set code_bad ONLY when the source EXPLICITLY presents that snippet as vulnerable/insecure/unsafe/"
"noncompliant/'don't do this' (prose or an inline comment like 'unsafe', 'BAD', 'not OK', 'vulnerable'). "
"A snippet shown as the correct/parameterized/safe way is NEVER code_bad. Many cheatsheet fences are safe "
"examples only — for those, emit a text-only fact (code_bad=code_good=null) stating the required pattern.\n"
"- code_bad and code_good MUST be the SAME operation shown two ways (the vulnerable version vs its fix). "
"If the nearest good fence is a DIFFERENT operation, do NOT pair them — set both to null and keep the fact "
"text-only. Never fabricate a pairing.\n"
"- Prefer the tightest snippet: one or two lines that show the insecure call and its secure replacement.")

def build_items(files):
    items = []
    for f in files:
        text = open(f, encoding="utf-8").read()
        title = title_of(f, text)
        lib = lib_id(f)
        chunks = [c for c in pack(split_h2(text)) if substantive(c)]
        for c in chunks:
            llm_input = f"OWASP Cheat Sheet: {title}\n\n{c}"
            items.append({
                "llm_input": llm_input,
                "corpus": c,                       # ground against the exact chunk (fences + prose)
                "source": f"OWASP CS: {title}",
                "license_note": LICENSE,
                "lib": lib,
                "version": "owasp-cs",
            })
    return items

def main():
    all_files = sorted(glob.glob(os.path.join(CS_DIR, "*.md")))
    all_files = [f for f in all_files
                 if not any(s in os.path.basename(f) for s in SKIP)]
    if "--files" in sys.argv:
        want = sys.argv[sys.argv.index("--files") + 1].split(",")
        all_files = [f for f in all_files if any(w.lower() in os.path.basename(f).lower() for w in want)]
    if "--limit" in sys.argv:
        all_files = all_files[:int(sys.argv[sys.argv.index("--limit") + 1])]

    items = build_items(all_files)
    print(f"files: {len(all_files)}  chunks/items: {len(items)}  "
          f"(w/fence: {sum('```' in it['corpus'] for it in items)})")
    if "--dry" in sys.argv:
        from collections import Counter
        per = Counter(it["lib"] for it in items)
        for lib, n in per.most_common(12):
            print(f"    {n:>3}  {lib}")
        return
    C.run(items, "experts/appsec/facts/owasp_cs", extra_sys=EXTRA_SYS, id_prefix="ow")

if __name__ == "__main__":
    main()
