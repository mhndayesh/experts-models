#!/usr/bin/env python3
"""retriever_f.py - FLOAT/SORT retriever (llama.cpp >=2.24.0 engine, floats+sort confirmed). Proper BM25F
with real float weights + door-concentration discriminativeness + typed fields (symbols/anchors weighted
above prose) + abstention (float floor + top-margin + language filter) + sort-based top-k. Replaces the
integer max-scan design now that the engine supports floats and sort. Bakes to a float-postings template.

Reuses retriever2's bake-faithful tokenizer/anchors; scoring machinery is new (BM25F, not integer TF-IDF)."""
import json, os, math
from collections import defaultdict, Counter
import retriever2 as R2   # terms_from, is_symbol, norm_lang, LANG_ALIAS

BANK = os.path.join(os.path.dirname(os.path.abspath(__file__)), "experts", "appsec", "facts", "FINAL_anchored.jsonl")
FACTS = [json.loads(l) for l in open(BANK, encoding="utf-8")]
DOOR = [f.get("door","?") for f in FACTS]
LANG = [R2.norm_lang(f.get("lang","")) for f in FACTS]

# --- typed fields per fact: symbols/anchors (high value) vs prose (low) ---
def field_terms(f):
    kw = f.get("keywords", {})
    sym_src  = " ".join(kw.get("from_fact", []) + (f.get("anchors") or []))
    prose_src= " ".join([f.get("truth",""), f.get("subject",""), " ".join(kw.get("associative", []))])
    return {"sym": R2.terms_from(sym_src, keep_bigrams=True),
            "prose": R2.terms_from(prose_src, keep_bigrams=True)}

FIELD_BOOST = {"sym": 3.0, "prose": 1.0}     # BM25F per-field weight
K1, B = 1.4, 0.55                            # BM25 saturation / length-norm
N = len(FACTS)

# --- build index: per-field tf, df, door-concentration, field lengths ---
FTF   = [field_terms(f) for f in FACTS]                       # fid -> {field: [terms]}
TFC   = [{fl: Counter(ts) for fl, ts in ff.items()} for ff in FTF]
df    = defaultdict(int); ddf = defaultdict(lambda: defaultdict(int))
post  = defaultdict(set)                                      # term -> {fid}  (candidate generation)
for fid, ff in enumerate(FTF):
    allt = set(t for ts in ff.values() for t in ts)
    for t in allt:
        df[t] += 1; ddf[t][DOOR[fid]] += 1; post[t].add(fid)
avgdl = {fl: (sum(len(FTF[i][fl]) for i in range(N)) / N) or 1.0 for fl in FIELD_BOOST}
def idf(t):   # BM25 idf (float)
    return math.log(1 + (N - df[t] + 0.5) / (df[t] + 0.5))
def conc(t):  # door-concentration in [0,1]: 1 = topic-specific, ~1/10 = cross-door boilerplate
    return max(ddf[t].values()) / df[t] if df[t] else 0.0
CONC_MIN, GENERIC_DF = 0.30, 0.14 * N

def _qterms(prompt, draft):
    q = defaultdict(float)
    for t in R2.terms_from(draft):  q[t] = max(q[t], 0.6)     # draft (baked=empty) secondary
    for t in R2.terms_from(prompt): q[t] = max(q[t], 1.0)
    return q

def score_all(prompt, draft=""):
    q = _qterms(prompt, draft)
    cands = set()
    for t in q:
        if t in post and df[t] < GENERIC_DF and conc(t) >= CONC_MIN:
            cands |= post[t]
    scores = {}
    for fid in cands:
        s = 0.0
        for t, qw in q.items():
            if t not in post or fid not in post[t]: continue
            if df[t] >= GENERIC_DF or conc(t) < CONC_MIN: continue
            # BM25F: combine per-field normalized tf, then saturate
            comb = 0.0
            for fl, boost in FIELD_BOOST.items():
                tf = TFC[fid][fl].get(t, 0)
                if not tf: continue
                dl = len(FTF[fid][fl]) or 1
                comb += boost * (tf / (1 - B + B * dl / avgdl[fl]))
            if comb > 0:
                s += qw * idf(t) * conc(t) * (comb * (K1 + 1)) / (comb + K1)
        if s > 0: scores[fid] = s
    return scores

def retrieve(prompt, draft="", k=5, floor=2.5, margin=0.45, lang=""):
    """Float BM25F + abstention. floor = absolute; margin = keep facts >= margin*top; lang filter. sort top-k."""
    scores = score_all(prompt, draft)
    ql = R2.norm_lang(lang)
    if ql:
        scores = {fid: s for fid, s in scores.items() if LANG[fid] == "" or LANG[fid] == ql}
    if not scores: return []
    top = max(scores.values())
    cut = max(floor, margin * top)
    ranked = sorted(scores.items(), key=lambda kv: -kv[1])           # SORT (engine supports it now)
    return [(fid, round(s, 3)) for fid, s in ranked if s >= cut][:k]

if __name__ == "__main__":
    print(f"BM25F float index: {len(post)} terms, {N} facts, avgdl={ {k:round(v,1) for k,v in avgdl.items()} }")
