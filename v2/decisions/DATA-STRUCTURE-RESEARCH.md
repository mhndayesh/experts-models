# Data-structure research — what to store, cross-checked against minja limits

> ✅ **PROBE RESULT (2026-07-18) — the integer-only premise is STALE.** Fail-fast probe of the shipping
> **llama.cpp 2.24.0** engine (avx2 build, `/apply-template`, no inference):
> `{{ 7 / 2 }}` → **`3.5` (FLOATS supported)**; `{{ [3,1,2]|sort }}` → **`1-2-3` (SORT supported)**; baseline
> integer math passes. So the "1970s integer-only machine" framing below is **WRONG for 2.24.0** — the engine
> modernized. Float BM25/TF-IDF, `sort`-based top-k, WAND, and quantized-vector cosine are all now expressible
> in-template. The rejections of float-scoring/WAND below are LIFTED for 2.24.0+.
>
> **DECISION (owner, 2026-07-18): (A) USE FLOATS/SORT.** Modern in-GGUF IR scoring; the GGUF requires
> llama.cpp ≥ 2.24.0.
>
> **LM Studio confirmed upstream (2026-07-18).** `.lmstudio/.internal/backend-preferences-v1.json` → selected
> runtime = **`llama.cpp-win-x86_64-vulkan-avx2` 2.24.0** (the newest installed; no 2.25+ exists). Probed that
> EXACT runtime: `{{ 7/2 }}` → `3.5`, `{{ [3,1,2]|sort }}` → `1-2-3`. Floats + sort work on the runtime LM Studio
> actually loads. No update needed — already on the latest.
>
> **Ship requirement:** the model card must state **"requires llama.cpp ≥ 2.24.0 (LM Studio runtime ≥ 2.24.0)"** —
> a template using float/sort fails to LOAD on older engines (the load-time validator rejects it). (`dictsort`
> was inconclusive in the probe — an unrelated message-format quirk, not a filter rejection — but it isn't needed.)


Supports **T-02 (bank & data structure)**. Question: of all IR data structures, which give the best retrieval
AND fit the minja runtime (integer math, dict-lookup, `.split()`, `namespace` string accumulators; **no float,
no sort, no bitwise, no mutation**)? Researched the classic IR literature + modern vector-IR, then filtered.

## The candidates, scored against our machine
| structure | what it is | fits minja? | verdict |
|---|---|---|---|
| **Inverted index** (term → postings) | dict {term → "fid:weight …"} | ✓ dict lookup + integer accumulate | **CORE** |
| **Cluster/IVF routing** (integer) | partition facts; route query to top clusters | ✓ integer vote table + max-scan | **ROUTING LAYER** |
| **Term-at-a-time (TAAT) accumulation** | scoring model, per-term accumulators | ✓ forced by "no dict mutation" — string accumulators | **SCORING MODEL** |
| Forward index (fact → text) | reconstruct the injected sentence | ✓ list index | keep as `fb_txt` |
| Signature files / Bloom filters | bit signatures, match by AND | ✗ no bitwise; **+ false positives** | **reject** |
| Bitmap index | bit-per-doc per term | ✗ no bitwise | reject |
| Trie / suffix array / FM-index | prefix / substring search | ✗ dict is already O(1); bigrams cover substrings | not needed |
| Vector ANN (HNSW, IVF-PQ) | float nearest-neighbour | ✗ float dot-product at query time | reject (query-time) |
| WAND / impact-ordered / tiered | sorted postings + skip + threshold | ✗ needs **sort / heap / float** threshold | reject |
| Learned sparse (SPLADE) | neural term weights | weights ✓ (bake-time), but query encoder ✗ | reject (query-time) |

## What the literature says (grounding)
- **Zobel & Moffat, *Inverted files vs signature files* (ACM TODS 1998):** inverted indexes **beat signature files
  and bitmaps on both index size and query speed.** Signature files only win under scarce memory — *and they trade
  it for false positives.* For us false positives are disqualifying: a wrong injected fact breaks the small model
  (the whole reason for the fail-open FLOOR). → **inverted index, not signatures.**
- **Cluster pruning / IVF** (Chierichetti et al., *Finding near neighbors through cluster pruning*, SIGMOD 2007;
  and modern IVF vector DBs): partition the corpus into clusters, keep an inverted list per cluster, and at query
  time route to the top-`nprobe` clusters, searching only inside them. This is exactly our **door/concept routing**
  — except IVF picks clusters by a **float** centroid dot-product, which we replace with an **integer term→cluster
  vote table**. So CRIR = IVF with the centroid step integerised. `nprobe` = "concepts within 50% of the peak vote."

## The cross-check verdict
Every structure that outperforms a plain inverted index in modern IR — WAND, block-max, learned-sparse, vector
ANN — needs **sort, float, or a neural query encoder**, none of which exist in minja. So we are not settling for a
weaker option: for an **integer-only, no-sort, no-float** machine, the best-available structure *is*:

> **Inverted index (integer weights) + integer cluster/door routing (IVF-style) + term-at-a-time accumulation +
> max-scan top-K with a fail-open floor.**

That is literally the state-of-the-art shape for this class of hardware — it's what pre-2000 IR shipped, and what
IVF does minus the floating-point centroids.

## The concrete baked structure (all integer, all minja-verified ops)
```
fb_post  {term → "fid:w fid:w …"}     # inverted index; w = IDF × door-concentration + symbol bonus (int)
fb_cid   [fid → cluster_id]           # IVF partition (door now; data-derived concepts later — T-02 D2)
fb_route {term → "cid:votes …"}       # integer routing table (replaces float centroids)
fb_txt   [fid → sentence]             # forward index for injection
FB_NCUR                               # curated-first boundary (id < FB_NCUR ⇒ curated bonus)
FB_FLOOR                              # fail-open threshold (NEW — one integer compare)
```
Runtime (`fb_gen.jinja`): tokenize → route (accumulate cluster votes, max-scan top clusters) → score facts in
those clusters (TAAT accumulate) → **max-scan top-K where score ≥ FB_FLOOR**. No op leaves the verified subset.

## Size is OUT OF SCOPE (owner, 2026-07-18)
Owner ruling: **do not consider index size.** This removes Zobel's one caveat against inverted files and, more
importantly, **inverts the design emphasis** — the binding constraints are now only (1) the minja instruction set
and (2) retrieval **precision**. What size-freedom unlocks (all pure upside, no cost):
- **Lavish bake-time anchoring.** The strict test proved the ceiling is *anchoring* (facts must carry the API a
  vulnerable draft types). With size free, anchor every fact generously — all cross-language API equivalents,
  synonyms, and symbol variants that should route to it. This is the single highest-leverage use of the freedom.
- **Baked query expansion / association thesaurus** — bake a full `{term → related terms}` table so a query term
  drags in its co-occurring symbols (`argon2 → kdf, salt, rehash`). No size penalty.
- **Redundant routing** — store BOTH coarse `door` and fine data-derived `concept` routing; keep both.
- **Wide postings** — do not truncate postings length; index every discriminative term of every fact.
- Note: door-concentration still **drops generic/boilerplate terms — for PRECISION, not size** (that stays).
(F-053 / the 980 KB LM Studio truncation is moot for us — we serve via `llama-server`.)

## Decisions this settles / leaves open
- **Settled:** inverted index + integer IVF routing + TAAT + max-scan + floor. Reject signatures/bitmaps/ANN/WAND.
- **Open (T-02):** D2 cluster granularity (doors only vs data-derived concepts — CRIR gave no lift *yet* because
  facts lack anchors, so concepts wait on anchors); D3 baked size; D1 anchor generation.

**Sources:** [Zobel & Moffat, Inverted files vs signature files (ACM TODS 1998)](https://dl.acm.org/doi/10.1145/296854.277632)
· [Zobel, RMIT PDF](https://www.cs.columbia.edu/~gravano/Qual/Papers/19%20-%20Inverted%20files%20versus%20signature%20files%20for%20text%20indexing.pdf)
· [Survey of Data Structures for Large-Scale IR](https://gatiaher.github.io/projects/survey-of-data-structures-for-large-scale-information-retrieval/)
· [Chierichetti et al., Finding near neighbors through cluster pruning (SIGMOD 2007)](https://dl.acm.org/doi/10.1145/1265530.1265545)
· [Survey on Vector Databases (IVF/centroid routing)](https://arxiv.org/html/2310.11703v2)
