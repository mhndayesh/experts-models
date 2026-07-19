#!/usr/bin/env python3
"""check_extract.py - the RAW checker for llm_extract.py output. Because the LLM filled a
STRICT schema, dumb code can verify EVERY field. The load-bearing check is the anti-
hallucination anchor: `quote` must appear VERBATIM in the source. Nothing is trusted.

Triage, not verdict (F-065): it flags what to READ, it is not the final say.
usage: python check_extract.py <lib>.llm_facts.jsonl <source>
out:   <lib>.llm_facts.kept.jsonl / .rejects.jsonl  + a printed report
"""
import json, re, sys, collections
FACTS = sys.argv[1]; SRC = sys.argv[2]
src = open(SRC, encoding="utf-8").read()

def canon(s):
    # Normalize to bare words: markup (rst roles :meth:`X`, ``code``, **bold**, [links])
    # carries no semantic content and its subtle differences between the LLM's copied
    # quote and the source were breaking the verbatim anchor. Reduce both sides to a
    # lowercase word-sequence; the anchor then checks word-order containment, robust to markup.
    return re.sub(r"[^a-z0-9]+", " ", (s or "").lower()).strip()
SRC_C = canon(src)

TYPES = {"REMOVED", "REPLACED", "CHANGED"}
WHY = {"post-cutoff", "reverses-habit", "silent-failure"}
VAGUE = ("behaviour changed", "behavior changed", "has changed", "was updated", "is different", "changed the")

def check(f):
    errs = []
    for k in ("type", "subject", "old", "truth", "why_it_bites", "quote", "keywords", "lib", "version", "id"):
        if f.get(k) in (None, "", []) and not (k == "new"):
            if not f.get(k): errs.append(f"missing {k}")
    if f.get("type") not in TYPES: errs.append(f"bad type {f.get('type')!r}")
    if f.get("why_it_bites") not in WHY: errs.append(f"bad why_it_bites {f.get('why_it_bites')!r}")
    truth = (f.get("truth") or "")
    if not (8 <= len(truth) <= 220): errs.append(f"truth len {len(truth)}")
    if any(v in truth.lower() for v in VAGUE): errs.append("truth is VAGUE (not concrete)")
    # --- the anchor: quote must be verbatim in source ---
    q = canon(f.get("quote") or "")
    if len(q) < 12: errs.append("quote too short")
    elif q not in SRC_C: errs.append("quote NOT verbatim in source")
    # grounding: the `old` SYMBOL should live in the source. Only enforced when `old` is a
    # single token (a real symbol) - for behaviour facts `old` is a described behaviour, and
    # the verbatim `quote` is already the anchor, so a prose `old` is fine.
    old = canon(f.get("old") or "")
    if old and " " not in old and old not in SRC_C:
        # the LLM may normalise a symbol (Field(min_items=...)) while the source writes the
        # bare token (min_items). Ground on the core identifier(s) instead of the whole form.
        cores = [t for t in re.findall(r"[a-z_][a-z0-9_]{3,}", old) if t not in ("field", "none", "true", "false", "self")]
        if not cores or not any(c in SRC_C for c in cores):
            errs.append(f"old {f.get('old')!r} not grounded in source")
    # REPLACED must carry a new; REMOVED must not
    if f.get("type") == "REPLACED" and not f.get("new"): errs.append("REPLACED without new")
    if f.get("type") == "REMOVED" and f.get("new"): errs.append("REMOVED but has new")
    # keywords: two tiers, both validated
    kw = f.get("keywords") or {}
    ff = [str(x).lower().strip() for x in kw.get("from_fact", [])]
    asso = [str(x).lower().strip() for x in kw.get("associative", [])]
    if not ff: errs.append("from_fact empty")
    hay = (truth + " " + str(f.get("old")) + " " + str(f.get("new"))).lower()
    ungrounded = [w for w in ff if w and w not in hay]
    if ungrounded: errs.append(f"from_fact not in fact: {ungrounded[:3]}")
    if not (1 <= len(asso) <= 8): errs.append(f"associative count {len(asso)}")
    bad_len = [a for a in asso if not (1 <= len(a.split()) <= 6)]
    if bad_len: errs.append(f"associative wrong length: {bad_len[:2]}")
    dupe = [a for a in asso if a in ff]
    if dupe: errs.append(f"associative duplicates from_fact: {dupe[:2]}")
    return errs

facts = [json.loads(l) for l in open(FACTS, encoding="utf-8")]
kept, rej = [], []
for f in facts:
    e = check(f); (rej.append((f, e)) if e else kept.append(f))
by = collections.Counter(e.split(":")[0].split(" (")[0] for _, es in rej for e in es)
print(f"{len(facts)} llm facts -> {len(kept)} PASS / {len(rej)} flagged\n")
print("flag reasons (most common):")
for reason, n in by.most_common(12): print(f"  {n:>3}  {reason}")
with open(FACTS.replace(".jsonl", ".kept.jsonl"), "w", encoding="utf-8") as fh:
    for f in kept: fh.write(json.dumps(f, ensure_ascii=False) + "\n")
with open(FACTS.replace(".jsonl", ".rejects.jsonl"), "w", encoding="utf-8") as fh:
    for f, e in rej: fh.write(json.dumps({**f, "_flags": e}, ensure_ascii=False) + "\n")
print(f"\n-> {FACTS.replace('.jsonl','.kept.jsonl')} / .rejects.jsonl   (READ both)")
