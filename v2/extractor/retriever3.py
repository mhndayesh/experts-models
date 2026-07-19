#!/usr/bin/env python3
"""retriever3.py - CRIR: Concept-Routed Integer Retrieval. Draft-symbol EXACT-MATCH primary +
concept-routing backstop + fail-open floor. Concepts are built OFFLINE by pure-Python co-occurrence
clustering (union-find over facts sharing a rare discriminative symbol) -> integer concept_id per fact.
Runtime mirrors the minja integer instruction set (dict lookup, int add/compare, max-scan; no float/sort).

Reuses retriever2's bake-faithful tokenizer + symbol-anchored inverted index; adds the concept layer.
"""
import json, os, math
from collections import defaultdict
import retriever2 as R2   # terms_from, is_symbol, fact_tokens, FACTS, POST, DOOR, build_index

FACTS = R2.FACTS
POST  = R2.POST          # term -> {fid: int weight}  (IDF x door-concentration + symbol bonus)
DOOR  = R2.DOOR

# ---- OFFLINE: concept clustering by shared RARE discriminative symbols (union-find) ----
def build_concepts(df_lo=2, df_hi=22, w_min=7):
    N = len(FACTS)
    # discriminative symbols = index terms that are structured identifiers, rare, high-weight
    parent = list(range(N))
    def find(x):
        while parent[x] != x: parent[x] = parent[parent[x]]; x = parent[x]
        return x
    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb: parent[max(ra,rb)] = min(ra,rb)
    for term, posting in POST.items():
        if not R2.is_symbol(term):                 # only underscore/identifier symbols bridge a concept
            continue
        if not (df_lo <= len(posting) <= df_hi):   # rare enough to be specific, shared enough to link
            continue
        if max(posting.values()) < w_min:          # must be a high-weight (discriminative) symbol
            continue
        fids = list(posting.keys())
        for f in fids[1:]:
            union(fids[0], f)
    concept = [find(i) for i in range(N)]
    # renumber concepts to small ints
    remap = {}
    cid = [remap.setdefault(c, len(remap)) for c in concept]
    # routing table: term -> {concept_id: integer votes} (sum of the term's posting weights per concept)
    route = defaultdict(lambda: defaultdict(int))
    for term, posting in POST.items():
        for fid, w in posting.items():
            route[term][cid[fid]] += w
    return cid, route

CID, ROUTE = build_concepts()
NCONCEPT = len(set(CID))

def retrieve(prompt, draft="", k=5, floor=6, concept_boost=12, sym_primary=4):
    # query terms: draft is the primary key (names the insecure API); prompt secondary
    qterms = {}
    for t in R2.terms_from(draft):  qterms[t] = max(qterms.get(t,0), 3)
    for t in R2.terms_from(prompt): qterms[t] = max(qterms.get(t,0), 4)
    # STEP 1 - route: accumulate integer concept votes, pick dominant concept(s) [max-scan]
    votes = defaultdict(int)
    for t, qw in qterms.items():
        if t in ROUTE:
            for c, v in ROUTE[t].items(): votes[c] += v * qw
    top_concepts = set()
    if votes:
        top = max(votes.values())
        top_concepts = {c for c, v in votes.items() if v * 2 >= top}   # concepts within 50% of the peak
    # STEP 2 - score facts: symbol-anchored exact match (primary) + concept membership boost
    score = defaultdict(int)
    for t, qw in qterms.items():
        if t in POST:
            prim = sym_primary if R2.is_symbol(t) else 1     # draft's API symbols carry the signal
            for fid, w in POST[t].items():
                score[fid] += w * qw * prim
    if not score: return []
    for fid in score:
        if CID[fid] in top_concepts: score[fid] += concept_boost
    # STEP 3 - select: max-scan top-k with FLOOR (fail open)
    picked = []; taken = set()
    for _ in range(k):
        best, bs = None, floor - 1
        for fid, s in score.items():
            if fid in taken: continue
            if s > bs: best, bs = fid, s
        if best is None: break
        picked.append((best, bs)); taken.add(best)
    return picked

def score_all(prompt, draft="", concept_boost=12, sym_primary=4):
    """full score dict (for ranking/measurement) mirroring retrieve()'s scoring, no top-k truncation."""
    qterms = {}
    for t in R2.terms_from(draft):  qterms[t] = max(qterms.get(t,0), 3)
    for t in R2.terms_from(prompt): qterms[t] = max(qterms.get(t,0), 4)
    votes = defaultdict(int)
    for t, qw in qterms.items():
        if t in ROUTE:
            for c, v in ROUTE[t].items(): votes[c] += v * qw
    top_concepts = set()
    if votes:
        top = max(votes.values()); top_concepts = {c for c,v in votes.items() if v*2 >= top}
    score = defaultdict(int)
    for t, qw in qterms.items():
        if t in POST:
            prim = sym_primary if R2.is_symbol(t) else 1
            for fid, w in POST[t].items(): score[fid] += w * qw * prim
    for fid in score:
        if CID[fid] in top_concepts: score[fid] += concept_boost
    return score

if __name__ == "__main__":
    print(f"concepts: {NCONCEPT} over {len(FACTS)} facts (avg {len(FACTS)//max(1,NCONCEPT)}/concept)")
