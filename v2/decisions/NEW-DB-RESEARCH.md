# New DB / Store Research — do we need a real database for the bank?

**Date:** 2026-07-15. **Status:** investigated, no code shipped. Conclusion:
**no new store is needed.** Both pieces a "proper store" would add already exist
in the repo, and the existing versions already carry the fixes.

This file records the investigation so it isn't re-run. It answers three
questions that came up: (1) should the bank become an append-only log with a
real DB discipline? (2) do we need an embedding cache? (3) would any of it work
inside the GGUF?

---

## 1. The proposal that started it

A design was floated: turn the bank into an **append-only JSONL log** with DB
discipline — `id`/`op`/`ts`/`hash`/`data` records, sha256 dedup, tombstone
deletes, fsync + atomic swap, single-writer lockfile, replay-on-startup,
compaction at ~30% garbage, embedding sidecar keyed by hash, TOML manifest.
Roughly 150–200 lines, zero new deps.

It is **good general engineering.** It is also **aimed at conditions this repo
does not have.**

## 2. The two facts that collapse the case for it

**Q: More than one writer?** No. The runtime bank is **read-only at runtime**
(CLAUDE.md architecture). Writes happen offline through one `factbank watch` →
propose → apply run, which **already does snapshot + atomic swap + health-check +
rollback**. → lockfile unnecessary.

**Q: Thousands or millions?** **Thousands.** Shipped bank 1,911 facts;
experiments 2.3k–24k; largest raw mine ~46k *before* gating. Never millions. →
startup replay, compaction-ratio tuning, and replay-scaling are all insurance
against a scale that never occurs.

Frozen bank + existing snapshot/rollback + thousands-of-records ⇒ the log,
lockfile, and compaction are **dead weight**.

## 3. The one claim that was WRONG — and it was the selling point

> *"sha256 of normalized text … directly fixes your BM25 IDF poisoning (F-064)."*

**It does not.** F-064's poison was **not exact duplicates** — it was facts that
**share a docstring but have different text**:

```
sklearn.LogisticRegression.get_params(self, deep=True) - Get parameters for this estimator.
sklearn.SVC.get_params(self, deep=True)                - Get parameters for this estimator.
sklearn.KMeans.get_params(self, deep=True)             - Get parameters for this estimator.
```

Same docstring flattens IDF on `get_params`/`estimator`/`parameters`. **But the
`text` differs** (different class in the symbol) → **different sha256** → hash
dedup lets all 144 clones through. It fixes ~0% of the 11,700-fact
inherited-duplicate bucket.

What actually caught F-064 was `dedupe_mine.py` grouping on the **semantic key**
`(source, leaf_name, docstring, signature)` — deliberately ignoring the class
prefix. **Exact-hash dedup is strictly weaker than the tool already in the repo.**
Nothing about dedup should be replaced.

## 4. The embedding cache already exists — and is better

The proposal's one genuinely useful component was an embedding sidecar. **It is
already built:** [`bankio.py`](../package/factbank/bankio.py), the **F-034 cache**,
wired into `HybridBank.from_jsonl_cached`.

| | proposed `EmbedCache` | existing `bankio.py` (F-034) |
|---|---|---|
| Misses cleanly on model change | keyed on `embedder_id` | keyed on **`model` + `dims` + `version`** ✅ |
| Atomic write | temp + `os.replace` | temp + `os.replace` ✅ |
| Never serves a bad cache | — | rebuilds on any mismatch, **never raises** ✅ |
| Size per fact | float32 = **3,072 B** | int8 Matryoshka-768 = **260 B** (**11.8× smaller**, retrieves identically, hit@5 0.972) |
| Bank-change detection | per-text hash | sha256 of the **whole file** |

The "stale-vector phantom" the critique worried about is **already handled** by
the `model`/`dims`/`version` stamp in `load_cache`.

**The one real difference:** invalidation granularity. `bankio.py` keys on the
whole-file hash, so editing one fact re-embeds all ~2,000; a per-text key would
re-embed one. **But** a full rebuild is a single batched call to a *local* nomic
embedder for 2k short strings — a few seconds, offline, during `watch apply`.
Per-text invalidation saves seconds on a rare unattended op. Not worth a second
cache. *If* the bank ever exceeds ~50k facts AND single-fact edits become
frequent, patch `bankio.py`'s key — do **not** add a parallel cache.

## 5. `watch.apply()` is already crash-safe

[`watch.py:176-192`](../package/factbank/watch.py#L176-L192): snapshot (timestamped
`.bak`) → copy to `.tmp` → append → `os.replace()` (atomic) → `health_check()`
(bank parses, ids unique, new facts retrievable) → **rollback to snapshot on
failure**. More careful than a bare `atomic_write_text()`. The only thing a
helper would add is an `fsync` before the swap — durability against a power cut
in a sub-second window, not corruption safety (`os.replace` already gives that).
Not worth a line for an offline, re-runnable op.

## 6. None of it works inside the GGUF

The whole append-log / cache / atomic-write discussion lives **only on the Python
side** (Retriever A). Inside the GGUF (Retriever B, the template-brain) there is
**no Python, no numpy, no HTTP, no embedder, no float matrix math, and no runtime
write** — the retriever is **Jinja**, run by llama.cpp's C++ engine at render
time, and the bank is **baked into the chat template, frozen**.

- Embedding cache → irrelevant (no numpy, no sidecar).
- Embedding *retrieval* → impossible (can't embed the query at render time; no
  vector math in the template engine).
- Append log / atomic writes → moot (no runtime write; "edit" = re-bake the GGUF).

Semantic-like recall inside the GGUF is achieved **at bake time** via **Doc2Token
expansions** (`expansions_v2.json`, F-052): user-phrasings are pre-generated
offline and indexed into the lexical inverted index, so runtime only ever matches
tokens. See the companion report / [`LANGUAGES.md`](LANGUAGES.md) §4.

## 7. Verdict

**Build nothing.** The bank does not need a database. It needs:
- durable writes → **have them** (`watch.apply`, `bankio.write_cache`)
- an embedding cache → **have it** (`bankio.py`, and 4× smaller than proposed)
- clean dedup → **have it**, semantic and stronger than hash (`dedupe_mine.py`)

The open problems in this repo are **not** storage problems, and they are **not
size problems** — the ~1 MB wall is dead (F-059); the shipping `model.yaml` route
has no ceiling (proven at 1.5–2.0 MB), and bytes were never the constraint
(F-055/F-056: 21k facts render a matched query in 218 ms). The only size-adjacent
thing that still bites is a *stale metadata cache* during dev — verify baked bytes
after every bake (see [`LANGUAGES.md`](LANGUAGES.md) §7).

What's actually open is **recall at scale** (F-055/F-056) and **obedience**
(F-065) — neither of which a better store or a bigger byte budget touches. Effort
belongs there, not on infrastructure the repo already closed.
