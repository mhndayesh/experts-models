# Architecture — how FactBank actually works

Verified against the shipped artifact on 2026-07-14.

The whole system lives in two metadata keys of a GGUF file. Nothing else runs.

```
gemma-4-12B-it-QAT-Q4_0-pythondatafactbank-idx.gguf
├── 667 tensors ................ byte-identical to the base model. Untouched.
├── tokenizer.chat_template .... 973,652 bytes: the bank + the index + the retriever
└── factbank.bank .............. the raw JSONL, carried for auditability
```

---

## 1. Storage — where the facts live

**Master copy: plain JSONL**, one fact per line.

```json
{"id": "numpy2-001",
 "text": "np.float_ was REMOVED in NumPy 2.0 - use np.float64 instead.",
 "source": "numpy", "version": "2.0", "kind": "mistake",
 "meta": {"url": "https://numpy.org/doc/stable/numpy_2_0_migration_guide.html"}}
```

**1,911 facts**, of two provenances — and the distinction drives everything downstream:

| kind | count | where it comes from | what it's worth |
|---|---:|---|---|
| **curated** | **388** | hand/agent-extracted from real docs, gated on a verbatim quote | **high** — these are renames, removals, gotchas: the facts that beat a *wrong* prior |
| **mined** | **1,523** | `inspect.signature` on the installed library + the doc URL from its Sphinx `objects.inv` | **unproven. Mined facts have won ZERO eval cases (F-065)** — every case the bank carried was won by a curated `mistake` fact. They are shallow but hallucination-proof (the API exists, with these arguments); there is no evidence they move obedience at all |

Provenance is encoded in the id: mined ids contain `api-`. At bake time curated facts are
sorted **first**, so "is this curated?" becomes `id < 388` — a number comparison, costing
zero bytes at runtime.

The mined pool is far larger than what ships: **46,834 facts across 45 libraries** in four
domains (data, web, ai, stdlib). A model is a *quota over that pool*, not a separate mining
run.

> **The mined pool is ~66% JUNK, and the junk actively breaks retrieval (F-064).**
> `mine_api.py` walks the **inheritance chain**, so every sklearn estimator donated its own
> `get_params`, every duckdb exception its own `add_note`, and `str.join` entered the bank as
> a *matplotlib* fact. On the `data` domain: 24,133 → **8,096** after gating
> (`dedupe_mine.py`). Duplicate terms flatten IDF and crowd the top-5 — this is the likely
> cause of gold retrieval falling 12/12 at 2.3k facts → 9/12 at 21k.
>
> **A bigger mined pool is NOT an upgrade.** Only the `data` domain has been gated; `ai__*`
> and `std__*` have never been inspected and must be assumed equally bad.

### Why these facts are unfalsifiable evidence

Every fact targets a **post-training-cutoff API** (pandas 3.0, NumPy 2, Polars 1.x,
scikit-learn, SciPy…). With `requests` and old `pandas` you could never separate "the bank
told it" from "it already knew." Here, **any correct answer must have come from the bank** —
which is what makes the measurements mean anything.

## 2. Shaping — what the build does offline (`bake_index.py`)

Each fact becomes a set of **weighted index terms**. The weight is "how strongly does this
word prove this fact is the one you want?"

| term source | weight | example |
|---|---:|---|
| **dead API name** (renamed/removed, rare) | **10** | `melt` → the melt→unpivot fact |
| rare API token | 4 | `unpivot`, `ttest_ind` |
| description word (curated fact) | 3 | `removed`, `float64` |
| task-phrase bigram | 3 | `wide_long` |
| task-phrase word | 2 | `reshape` |
| **Doc2Token expansion bigram** | 2 | `columns_rows` |
| expansion word / common token | 1 | `dataframe` |

Then four transformations, each of which exists because its absence broke something:

**Squash-normalisation and identifier splitting.** `ttest_ind` also indexes as `ttest`,
`ind`, `ttestind`; `scikit-learn` as `scikitlearn`. This is what lets a user's *"t-test"*
reach `scipy.stats.ttest_ind`. Only strong (weight ≥ 4) tokens earn variants — squashing
every description word blew the index from 11k to 18k terms.

**Doc2Token expansions.** The model wrote **2,326 everyday questions** for its own **388
curated facts**, offline — *"how do I pivot longer in polars?"* — and their bigrams are
indexed at a weight strictly *below* real terms. This is the cure for the hardest failure
in keyword retrieval: a question that shares **zero words** with its fact. *"Turn columns
into rows"* now finds the melt→unpivot fact, and 35 terms point at it.

**IDF at build time.** A term pointing at ≤3 facts is evidence (×3); ≤10, weak (×2); more,
noise (×1). Above 40 postings it is dropped entirely. Runtime stays pure integer addition.
Without this, `test` (in every SciPy docstring) outvoted `ttest`, and a t-test question
returned `scipy.stats.dunnett`.

**Control culling.** Any key that appears in the control questions ("write me a haiku…") is
deleted — from the index **and** the gate. Both, because a version that culled only one let
English-word API names (`pyarrow.tell`) open library tabs on a haiku.

**Result:** 17,260 terms, 34,671 postings (2.0 per term), stored as one dict
`term → "factid:weight factid:weight …"`. Plus a **gate**: per library, its name + up to 48
unique trigger words + aliases (`np`→numpy, `scikit-learn`→sklearn, verified from real
package metadata).

The bake is **deterministic** — every iteration is sorted and every JSON blob uses
`sort_keys=True`. Without that, Python's per-process hash randomisation produced the same
index in a different key order, and a shipped artifact could not be reproduced from source.

## 3. Retrieval — what runs on every request

Executed by llama.cpp's Jinja engine, on the last user message, **before the question
renders**:

1. **Normalise** — lowercase, punctuation → spaces.
2. **Gate ("phone-book tabs")** — if the user *names* a library, only that tab opens;
   named always wins. If none is named, tabs open on trigger words. **No tab → nothing
   renders**, and the request is byte-identical to a stock model's.
3. **Build query terms** — content words, their squashed/split variants, alias canonicals,
   and adjacent bigrams. (`turn columns into rows` → `columns_rows` — the exact bridge to
   the melt fact.)
4. **Look up each term in the postings dict.** This is the point of an index: a fact is
   never visited unless a term points at it. Hits outside open tabs are discarded.
5. **Score** — integer adds. Curated facts get +6, or **+12** if the question shows
   breakage intent (*"broke"*, *"stopped working"*, *"after upgrading"*).
6. **Top 5** by max-selection.
7. **Deliver** (below).

### The delivery lane: a forged native tool exchange

Facts are *not* handed over as prose. The template renders a **completed
`factbank_search` call and response in the model's own tool syntax**, using the base
template's own macro — bit-identical to a real tool exchange. The model's experience is:
*a documentation lookup already ran; here are the results; now answer.*

This matters because prose delivery invites arbitration. Handed the same facts as prose,
the model deliberated — one glyph-heavy question burned **8,189 reasoning tokens and
produced no answer at all**. Through the tool channel: **390–757 tokens and a correct
answer**. A `tool_response` is not something the model argues with.

The forged block is rendered **before the user's question**. That placement kills an
LM Studio echo bug *and* buys prompt-prefix caching: repeat questions on the same topic
drop from ~1.8 s to ~0.24 s to first token.

## 4. Why this shape, and not RAG

There is no server, no embedding model, no vector store, no client code, and no
tool-choice step. **Code decides to retrieve — not the model.** The bank is frozen and
read-only. Everything that could drift at runtime was moved to build time: the expansions,
the IDF weights, the aliases, the gate.

What is left at runtime is string operations and integer addition — the only things the
substrate can do — and that is precisely why the whole system fits inside a file that
every serving stack already executes.
