#!/usr/bin/env python3
"""retriever2.py - Option A: symbol-anchored, door-routed, fail-open retrieval, written to MIRROR the
baked-GGUF engine limits (integer weights, '.'-splitting tokenizer, underscore-preserving, adjacent
bigrams, no-sort max-select). What works here bakes into fb_gen.jinja + a bake_index.py reweight.

Faithful to fb_gen.jinja:
  - normalize: lower, split on . , ( ) ? ! : ; ' and whitespace  (so 'torch.load' -> 'torch','load')
  - query terms: content words (len>2, not stopword) + identifier parts (split '_'/'-') + adjacent
    bigrams 'a_b'  (so 'torch load' -> 'torch_load' is recovered)
  - INTEGER posting weights; score = sum of weights of hitting terms (+ curated bonus)
  - DOOR gate: a fact only scores if its door is 'open' (a door opens when a discriminative query term
    indexes into it)  -> soft routing, no polars-for-pydantic
  - select: max-scan top-FB_MAX, with FLOOR (fail open) and <=MAXPERDOOR (aspect diversification)
"""
import json, os, re, math
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
BANK = os.path.join(HERE, "experts", "appsec", "facts", "FINAL.jsonl")
FACTS = [json.loads(l) for l in open(BANK, encoding="utf-8")]

# Only true English function words are hand-listed (standard IR, bank-agnostic). Everything else
# (incl. code boilerplate like __main__/app.route) is suppressed by a DATA-DERIVED signal, not a list.
STOP = set("the a an and or of to in on for with is are be as at by from that this it its use used using your you we our not no if do does can will would should must may new current over all any into via each other same than then them they he she his her which who what when where how why than".split())
PUNCT = str.maketrans({c: " " for c in ".,()?!:;'\"[]{}<>=+*/\\|@#$%^&~`\n\t"})

def norm(s):
    return (" " + (s or "").lower() + " ").translate(PUNCT)

def is_symbol(tok):
    """discriminative identifier: had an underscore, or is a camelCase/dotted API name."""
    return "_" in tok

def terms_from(text, keep_bigrams=True):
    """mirror fb_gen query-term expansion (operates on already-normalized, .-split text)."""
    raw = [w for w in norm(text).split() if w]
    words = [w for w in raw if len(w) > 2 and w not in STOP]
    out = []
    for w in words:
        out.append(w)
        for part in w.replace("-", "_").split("_"):     # identifier parts
            if len(part) > 3 and part != w and part not in STOP:
                out.append(part)
    if keep_bigrams:                                     # adjacent bigrams a_b (recovers dotted APIs)
        for i in range(len(words) - 1):
            out.append(words[i] + "_" + words[i+1])
    return out

# ---- per-fact token set: EVERY discriminative token from truth+subject+keywords+code (bake-tokenized) ----
def fact_tokens(f):
    kw = f.get("keywords", {})
    # curated 'from_fact' symbols + prose; NOT raw code_bad (full of boilerplate: __main__, app.route, ...)
    blob = " ".join([f.get("truth",""), f.get("subject",""),
                     " ".join(kw.get("associative", [])), " ".join(kw.get("from_fact", []))])
    return set(terms_from(blob, keep_bigrams=True))

# ---- build inverted index with INTEGER weights (what bake_index.py would emit) ----
# METHOD (bank-agnostic, no hand lists): a term's value = RARITY x DOOR-CONCENTRATION.
#   rarity        = IDF (a term in few facts is more informative)
#   concentration = fraction of the term's facts that sit in its single most common door.
#                   ~1.0 => topic-specific symbol (argon2, weights_only) -> keep/boost.
#                   ~1/#doors => cross-door boilerplate (__main__, app, flask, import) -> ~0 weight.
# This suppresses boilerplate and rewards true symbols automatically, computed only from the bank.
def build_index(idf_scale=4, sym_boost=4, conc_min=0.35, generic_df_frac=0.14):
    N = len(FACTS)
    tsets = [fact_tokens(f) for f in FACTS]
    door = [f.get("door","?") for f in FACTS]
    df = defaultdict(int); door_df = defaultdict(lambda: defaultdict(int))
    for fid, ts in enumerate(tsets):
        for t in ts:
            df[t] += 1; door_df[t][door[fid]] += 1
    generic_df = generic_df_frac * N
    post = defaultdict(dict)     # term -> {fid: int weight}
    for fid, ts in enumerate(tsets):
        for t in ts:
            if df[t] >= generic_df: continue               # too common anywhere -> drop
            conc = max(door_df[t].values()) / df[t]        # DOOR-CONCENTRATION (the boilerplate killer)
            if conc < conc_min: continue                   # spread across doors -> boilerplate -> drop
            idf = math.log(1 + N / (1 + df[t]))
            w = 1 + int(round(idf * idf_scale * conc))     # rarity x concentration
            if is_symbol(t): w += sym_boost                # structured identifier -> extra anchor
            post[t][fid] = w
    return post, door

POST, DOOR = build_index()

# fact language (for the abstention language filter). Normalized to a canonical enum.
LANG_ALIAS = {"py":"python","python":"python","js":"javascript","javascript":"javascript","ts":"typescript",
    "typescript":"typescript","rb":"ruby","ruby":"ruby","rs":"rust","rust":"rust","cs":"csharp","c#":"csharp",
    "csharp":"csharp","cpp":"cpp","c++":"cpp","c":"c","go":"go","golang":"go","java":"java","kotlin":"kotlin",
    "kt":"kotlin","swift":"swift","php":"php","xml":"xml"}
def norm_lang(s): return LANG_ALIAS.get((s or "").strip().lower(), (s or "").strip().lower())
LANG = [norm_lang(f.get("lang","")) for f in FACTS]

def retrieve(prompt, draft="", k=5, floor=6, door_boost=10, maxperdoor=5, lang="", margin_pct=0):
    """Abstaining retriever (audit #3). ABSTAIN = precision before recall (authority-framing makes a wrong
    inject worse). Gates, all bakeable (integer compares + string eq):
      floor      - absolute score floor (fail-CLOSED: withhold weak facts; system falls open to base)
      margin_pct - inject fact i only if score_i >= margin_pct% of the top score (drops the weak tail)
      lang       - drop facts whose language is incompatible (blank fact-lang = language-agnostic, kept)
    Returns [] (abstain) when nothing clears the gates. draft='' = the baked single-pass reality."""
    ql = norm_lang(lang)
    qterms = {}
    for t in terms_from(draft):  qterms[t] = max(qterms.get(t,0), 3)
    for t in terms_from(prompt): qterms[t] = max(qterms.get(t,0), 4)
    score = defaultdict(int)
    for t, qw in qterms.items():
        if t in POST:
            for fid, w in POST[t].items():
                score[fid] += w * qw
    if ql:                                    # LANGUAGE FILTER: keep agnostic facts + matching-language facts
        score = {fid: s for fid, s in score.items() if LANG[fid] == "" or LANG[fid] == ql}
    if not score: return []
    if door_boost:
        mass = defaultdict(int)
        for fid, s in score.items(): mass[DOOR[fid]] += s
        top_mass = max(mass.values())
        strong = {d for d, m in mass.items() if m * 2 >= top_mass}
        for fid in score:
            if DOOR[fid] in strong: score[fid] += door_boost
    top_score = max(score.values())
    eff_floor = max(floor, (top_score * margin_pct) // 100)   # MARGIN: relative to the strongest evidence
    picked = []; per = defaultdict(int); taken = set()
    for _ in range(k):
        best, bs = None, eff_floor - 1
        for fid, s in score.items():
            if fid in taken or per[DOOR[fid]] >= maxperdoor: continue
            if s > bs: best, bs = fid, s
        if best is None: break
        picked.append((best, bs)); per[DOOR[best]] += 1; taken.add(best)
    return picked

def score_all(prompt, draft="", door_boost=10):
    """full score dict (for ranking/measurement) mirroring retrieve()'s scoring, no top-k truncation."""
    qterms = {}
    for t in terms_from(draft):  qterms[t] = max(qterms.get(t,0), 3)
    for t in terms_from(prompt): qterms[t] = max(qterms.get(t,0), 4)
    score = defaultdict(int)
    for t, qw in qterms.items():
        if t in POST:
            for fid, w in POST[t].items(): score[fid] += w * qw
    if door_boost and score:
        mass = defaultdict(int)
        for fid, s in score.items(): mass[DOOR[fid]] += s
        top = max(mass.values()); strong = {d for d,m in mass.items() if m*2 >= top}
        for fid in score:
            if DOOR[fid] in strong: score[fid] += door_boost
    return score

if __name__ == "__main__":
    print(f"index: {len(POST)} terms over {len(FACTS)} facts")
