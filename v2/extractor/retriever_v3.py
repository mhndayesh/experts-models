#!/usr/bin/env python3
"""retriever_v3.py - float BM25F over the FACETED concept->variant store (schema v3). Fields: exact_symbols,
bad_pattern_symbols, query_phrases (the benign-prompt bridge), aliases, truth - each weighted. Concept routing
(shared lesson matched once) + language-facet filter + float floor/margin abstention + sort. Requires >=2.24.0
engine (floats/sort). Reads FINAL_v3.jsonl."""
import json, os, math
from collections import defaultdict, Counter
import retriever2 as R2

BANK = os.path.join(os.path.dirname(os.path.abspath(__file__)), "experts", "appsec", "facts", "FINAL_v3.jsonl")
_rows = [json.loads(l) for l in open(BANK, encoding="utf-8")]
VAR = [r for r in _rows if r.get("kind") == "variant"]
FID = {v["id"]: i for i, v in enumerate(VAR)}
CID = [v["concept_id"] for v in VAR]
LANG = [R2.norm_lang(v["facets"].get("language","")) for v in VAR]
N = len(VAR)

FIELD_BOOST = {"exact":4.0, "feature":3.5, "bad":3.0, "phrase":2.5, "alias":2.0, "truth":1.0}
K1, B = 1.4, 0.5

def _field_terms(v):
    r = v["retrieval"]
    return {
        "exact":   R2.terms_from(" ".join(r.get("exact_symbols") or []), keep_bigrams=True),
        "feature": R2.terms_from(" ".join(r.get("feature_phrases") or []), keep_bigrams=False),  # benign-prompt bridge
        "bad":     R2.terms_from(" ".join(r.get("bad_pattern_symbols") or []), keep_bigrams=True),
        "phrase":  R2.terms_from(" ".join(r.get("query_phrases") or []), keep_bigrams=False),
        "alias":   R2.terms_from(" ".join(r.get("aliases") or []), keep_bigrams=False),
        "truth":   R2.terms_from(v["claim"].get("truth",""), keep_bigrams=False),
    }
FT  = [_field_terms(v) for v in VAR]
TFC = [{fl: Counter(ts) for fl, ts in ff.items()} for ff in FT]
df  = defaultdict(int); ddf = defaultdict(lambda: defaultdict(int)); post = defaultdict(set)
for i, ff in enumerate(FT):
    allt = set(t for ts in ff.values() for t in ts)
    for t in allt: df[t]+=1; ddf[t][CID[i]]+=1; post[t].add(i)
# library-trigger index (net-02 Class-D fix): a fact whose library API appears in the prompt is surfaced
# regardless of vuln-match, so ALL of a library's landmines (e.g. paramiko host-key) come up when it's named.
LIBTRIG = defaultdict(set)
for i, v in enumerate(VAR):
    for t in (v["retrieval"].get("library_trigger") or []):
        for tok in R2.terms_from(t, keep_bigrams=True):
            if len(tok) > 3 and df.get(tok, 0) < 0.05*N:   # a SPECIFIC library token, not a common word
                LIBTRIG[tok].add(i)
avgdl = {fl:(sum(len(FT[i][fl]) for i in range(N))/N) or 1.0 for fl in FIELD_BOOST}
GENERIC_DF, CONC_MIN = 0.14*N, 0.25
def idf(t): return math.log(1 + (N - df[t] + 0.5)/(df[t] + 0.5))
def conc(t): return max(ddf[t].values())/df[t] if df[t] else 0.0

def score_all(prompt, draft=""):
    q = defaultdict(float)
    for t in R2.terms_from(draft):  q[t] = max(q[t], 0.6)
    for t in R2.terms_from(prompt): q[t] = max(q[t], 1.0)
    cands = set()
    for t in q:
        if t in post and df[t] < GENERIC_DF and conc(t) >= CONC_MIN: cands |= post[t]
    scores = {}
    for i in cands:
        s = 0.0
        for t, qw in q.items():
            if t not in post or i not in post[t] or df[t] >= GENERIC_DF or conc(t) < CONC_MIN: continue
            comb = 0.0
            for fl, boost in FIELD_BOOST.items():
                tf = TFC[i][fl].get(t, 0)
                if tf:
                    dl = len(FT[i][fl]) or 1
                    comb += boost * (tf / (1 - B + B*dl/avgdl[fl]))
            if comb > 0: s += qw * idf(t) * conc(t) * (comb*(K1+1))/(comb+K1)
        if s > 0: scores[i] = s
    # library-trigger surfacing: a named library's facts get a floor score so its OTHER landmines surface
    qtok = set(R2.terms_from(prompt))
    trig_hits = set()
    for tok in qtok:
        if tok in LIBTRIG: trig_hits |= LIBTRIG[tok]
    if trig_hits:
        base = (max(scores.values()) if scores else 4.0)
        # concept-DIVERSE surfacing: the BEST fact of EACH triggered concept gets a strong floor, so a
        # named library's OTHER landmines (host-key) get a slot instead of losing to its dominant one (cmd-inj).
        by_concept = defaultdict(list)
        for i in trig_hits: by_concept[CID[i]].append(i)
        for c, ids in by_concept.items():
            best = max(ids, key=lambda i: scores.get(i, 0.0))
            scores[best] = max(scores.get(best, 0.0), 0.75 * base)   # one representative per triggered concept
    # concept routing: reward variants in the dominant concept(s) (shared lesson matched once)
    if scores:
        mass = defaultdict(float)
        for i, s in scores.items(): mass[CID[i]] += s
        top = max(mass.values()); strong = {c for c, m in mass.items() if m >= 0.5*top}
        for i in scores:
            if CID[i] in strong: scores[i] *= 1.25
    return scores

def retrieve(prompt, draft="", k=5, floor=2.0, margin=0.4, lang=""):
    sc = score_all(prompt, draft); ql = R2.norm_lang(lang)
    if ql: sc = {i:s for i,s in sc.items() if LANG[i]=="" or LANG[i]==ql}
    if not sc: return []
    top = max(sc.values()); cut = max(floor, margin*top)
    return [(VAR[i]["id"], round(s,3)) for i,s in sorted(sc.items(), key=lambda kv:-kv[1]) if s>=cut][:k]

if __name__ == "__main__":
    print(f"v3 index: {N} variants, {len(set(CID))} concepts, {len(post)} terms")
