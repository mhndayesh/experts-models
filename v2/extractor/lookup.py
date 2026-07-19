#!/usr/bin/env python3
"""lookup.py - PROTOTYPE of the doors + classic-pointer retrieval, pure Python (algorithm
first; Jinja/GGUF port is a later parity concern). Loads the structured facts and compares:

  A flat        IDF-weighted keyword overlap (today's approach, no structure)
  B +doors      infer the door (lib) from the top hit, filter to it, FAIL OPEN if empty
  C +doors+ptrs B, then follow the classic linked-list `next` from each seed to pull the
                related cluster (the SET_L "combine 3-5 facts" case)

Doors  = lib (top) + subject-namespace (sub-doors).
Ptrs   = facts bucketed by (lib, primary-namespace) and linked into a ring; `next` walks
         the bucket. Edges are DERIVED from structure - no LLM.
"""
import json, math, os, re, glob
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
BANK = os.environ.get("BANK_DIR") or os.path.join(HERE, "facts")
if not os.path.isabs(BANK): BANK = os.path.join(HERE, BANK)
FACTS = []
for p in sorted(glob.glob(os.path.join(BANK, "*.jsonl"))):
    FACTS += [json.loads(l) for l in open(p, encoding="utf-8")]

def words(s): return [w for w in re.split(r"[^a-z0-9_]+", (s or "").lower()) if len(w) > 1]
def ns_tokens(subject):                      # sub-doors: split a symbol into its namespace path
    return [w for w in re.split(r"[.:/()=,\s]+", (subject or "").lower()) if len(w) > 1]

# ---- index each fact: door tokens + namespace + keywords + truth ----
def fact_tokens(f):
    t = set(words(f.get("lib")))                    # the door
    t |= set(ns_tokens(f.get("subject")))           # sub-doors
    for k in ("old", "new", "truth"): t |= set(words(f.get(k)))
    kw = f.get("keywords", {})
    for phrase in kw.get("from_fact", []) + kw.get("associative", []): t |= set(words(phrase))
    return t
TOKENS = [fact_tokens(f) for f in FACTS]
N = len(FACTS)
df = defaultdict(int)
for ts in TOKENS:
    for w in ts: df[w] += 1
IDF = {w: math.log(1 + N / (1 + d)) for w, d in df.items()}

# ---- classic pointer chains: bucket by (lib, primary namespace), link into a ring ----
def bucket_key(f):
    ns = ns_tokens(f.get("subject"))
    prim = next((x for x in ns if x != f.get("lib", "").lower()), ns[0] if ns else "misc")
    return (f.get("lib"), prim)
buckets = defaultdict(list)
for i, f in enumerate(FACTS): buckets[bucket_key(f)].append(i)
NEXT = {}                                             # fact-id -> next fact-id (the linked list)
for key, idxs in buckets.items():
    for j, i in enumerate(idxs):
        NEXT[FACTS[i]["id"]] = FACTS[idxs[(j + 1) % len(idxs)]]["id"]
ID2I = {f["id"]: i for i, f in enumerate(FACTS)}

W = 0.8   # soft-door weight: matching door * (1+W). A NUDGE, not a wall - nothing excluded.

# illustrative alias stub (fix 2C) - task words -> the symbol tokens facts actually carry
ALIASES = {
    "length": ["min_length", "max_length", "min_items", "max_items"],
    "size":   ["min_length", "max_length", "min_items", "max_items"],
    "mutation": ["frozen", "allow_mutation"],
    "immutable": ["frozen"],
    "validate": ["validator", "constraint"],
}

def score(qtokens, i, spec=1.0):
    s = sum(IDF.get(w, 0) ** spec for w in qtokens if w in TOKENS[i])   # spec>1 = rare tokens dominate
    return s / (1 + 0.15 * math.log(1 + len(TOKENS[i])))

def sim(i, j):                                    # fact-fact Jaccard, for MMR de-dup
    u = len(TOKENS[i] | TOKENS[j]); return len(TOKENS[i] & TOKENS[j]) / u if u else 0

def door_target(base, hint):
    if hint: return hint                          # draft/context names the lib (HyDE)
    agg = defaultdict(float)
    for s, i in sorted(base, reverse=True)[:8]: agg[FACTS[i]["lib"]] += s
    return max(agg, key=agg.get) if agg else None

def retrieve(query, hint=None, spec=1.0, mmr=False, alias=False, ptr=True, k=5, depth=4):
    q = set(words(query))
    if alias:
        for w in list(q): q |= set(ALIASES.get(w, []))
    base = [(score(q, i, spec), i) for i in range(N)]
    target = door_target(base, hint)
    ranked = sorted(((s * (1 + W) if FACTS[i]["lib"] == target else s, i) for s, i in base), reverse=True)
    got = {i: s for s, i in ranked[:max(k * 3, 15)]}
    if ptr:
        for _, seed in ranked[:3]:
            cur = FACTS[seed]["id"]
            for _ in range(depth):
                cur = NEXT.get(cur)
                if cur is None: break
                ci = ID2I[cur]
                got.setdefault(ci, score(q, ci, spec) * (1 + W if FACTS[ci]["lib"] == target else 0) + 0.5)
    pool = sorted(((s, i) for i, s in got.items()), reverse=True)
    if not mmr:
        return pool[:k]
    sel, cand = [], pool[:]                         # MMR: penalise near-duplicates already picked
    while cand and len(sel) < k:
        best, bestv = None, -1e9
        for s, i in cand:
            pen = max((sim(i, j) for _, j in sel), default=0)
            v = s - 1.2 * pen * s
            if v > bestv: bestv, best = v, (s, i)
        sel.append(best); cand.remove(best)
    return sel

TESTS = [   # (query, context-hint-lib, intent)
    ("validate string length in a field", "pydantic", "pydantic Field min_items->min_length"),
    ("how to access model fields", "pydantic", "pydantic __fields__ -> model_fields"),
    ("make a field frozen instead of allow mutation", "pydantic", "pydantic allow_mutation -> frozen"),
    ("custom root model", "pydantic", "pydantic __root__ -> RootModel"),
    ("flowschema api version no longer served", "kubernetes", "k8s flowcontrol/FlowSchema"),
    ("csistoragecapacity storage api removed", "kubernetes", "k8s storage.k8s.io CSIStorageCapacity"),
    ("aws eip vpc attribute removed", "terraform-aws", "tf-aws vpc -> domain"),
    ("pass a huggingface auth token when loading a model", "transformers", "transformers use_auth_token -> token"),
]

CONFIGS = {                                    # baseline vs the recipe that survived testing
    "baseline (soft+ptr)":            dict(),
    "FINAL (soft+ptr+mmr)":           dict(mmr=True),
}

import sys
if __name__ == "__main__":
    only = sys.argv[1] if len(sys.argv) > 1 else None
    print(f"bank: {N} facts, doors {sorted(set(f['lib'] for f in FACTS))} (W={W})")
    for name, flags in CONFIGS.items():
        if only and only not in name: continue
        print("\n" + "=" * 74 + f"\nCONFIG: {name}   flags={flags or 'none'}\n" + "=" * 74)
        for q, hint, intent in TESTS:
            res = retrieve(q, hint=hint, **flags)
            print(f"\nQ: {q!r}   want: {intent}")
            for s, i in res:
                f = FACTS[i]
                print(f"     {s:5.1f} {f['lib'][:4]}:{(f.get('old') or f['subject'])[:44]:44} -> {f.get('new') or ''}")
