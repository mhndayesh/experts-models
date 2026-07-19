#!/usr/bin/env python3
"""repair_quotes.py - a SECOND pass that acts as a CHECKER, not an extractor. Facts dropped
for 'quote NOT verbatim' usually have a REAL grounding - the LLM just paraphrased/stitched the
quote. This finds the actual verbatim source line that supports the fact and snaps the quote to
it. No LLM, no new facts: it only re-grounds an existing fact to real source text.

SAFETY (keeps the anchor honest): it snaps ONLY to a source line that (a) contains one of the
fact's own symbols (old/new/subject) and (b) shares >=2 content tokens with the fact. If no such
line exists, the fact was genuinely ungrounded and STAYS dropped.

usage: python repair_quotes.py <lib>.llm2_facts.jsonl <source>
out:   <lib>.llm2_facts.repaired.jsonl   (all facts; bad quotes snapped where possible)
"""
import json, re, sys
FACTS = sys.argv[1]; SRC = sys.argv[2]
raw = open(SRC, encoding="utf-8").read()

def canon(s):
    # MUST match check.py.canon exactly: reduce to bare lowercase word-sequence so the
    # verbatim anchor is robust to rst/markdown markup (:meth:`X`, ``code``, **bold**).
    return re.sub(r"[^a-z0-9]+", " ", (s or "").lower()).strip()
SRC_C = canon(raw)

# candidate units = verbatim source spans (lines, then sentence-split long ones)
def units(text):
    out = []
    for line in text.splitlines():
        line = line.strip()
        if len(line) < 20: continue
        for part in re.split(r"(?<=[.:;])\s+", line):
            part = part.strip(" -*")
            if len(part) >= 20: out.append(part)
    return out
UNITS = [(u, canon(u), set(re.findall(r"[a-z0-9_]{3,}", canon(u)))) for u in units(raw)]

STOP = {"the","and","for","with","not","was","are","use","now","you","that","this","from","have","been","will","can"}
def toks(*ss):
    return {t for s in ss for t in re.findall(r"[a-z0-9_]{3,}", (s or "").lower()) if t not in STOP}
def anchors(f):
    core = []
    for v in (f.get("old"), f.get("new"), f.get("subject")):
        core += [t for t in re.findall(r"[a-z_][a-z0-9_]{2,}", (v or "").lower()) if t not in ("field","none","true","false","self","the")]
    # the real API symbol often lives ONLY in truth/quote when old/subject are prose
    # ("returned None"); the derived from_fact keywords carry those grounded symbols.
    # Include them so repair can find the right source line to snap to.
    for kw in f.get("keywords", {}).get("from_fact", []):
        core += [t for t in re.findall(r"[a-z_][a-z0-9_]{2,}", str(kw).lower()) if t not in ("field","none","true","false","self","the")]
    return set(core)

def verbatim(f): return canon(f.get("quote") or "") in SRC_C and len(canon(f.get("quote") or "")) >= 12

facts = [json.loads(l) for l in open(FACTS, encoding="utf-8")]
repaired = still_bad = already = 0
for f in facts:
    if verbatim(f): already += 1; continue
    a = anchors(f); want = toks(f.get("truth"), f.get("old"), f.get("new"))
    best, best_score = None, 0
    for u_raw, u_c, u_t in UNITS:
        if not (a & u_t): continue                      # must mention the fact's own symbol
        score = len(want & u_t)
        if score > best_score: best, best_score = u_raw, score
    if best and best_score >= 2:
        f["quote"] = best[:220]; f["_repaired"] = True; repaired += 1
    else:
        f["_unsalvageable"] = True; still_bad += 1

with open(FACTS.replace(".jsonl", ".repaired.jsonl"), "w", encoding="utf-8") as fh:
    for f in facts: fh.write(json.dumps(f, ensure_ascii=False) + "\n")
print(f"{len(facts)} facts | already verbatim {already} | SNAPPED {repaired} | unsalvageable {still_bad}")
print(f"-> {FACTS.replace('.jsonl','.repaired.jsonl')}")
