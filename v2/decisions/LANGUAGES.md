# Languages & Technologies — the bank, its code, and the retriever

A reference map of **every language and format** this project is built on: what
each one is, where the fact bank / the code / the retriever use it, the official
sources and docs, and — the part that keeps biting — the **limitations of each
language**.

Compiled 2026-07-15. Facts marked *(repo-verified)* were checked against the
code in this session; the rest is general/official knowledge about the tool.

---

## 0. The big picture — three layers, four "languages"

This project has **two very different retrievers**, and they are written in
**different languages**. Confusing them is the single most common mistake.

| layer | what it is | language it's written in | who runs it |
|---|---|---|---|
| **The facts (the bank)** | the knowledge itself | **JSONL** (data, not code) | read by Python or by a template |
| **Research / package code** | loop, gates, extractors, server | **Python** ≥3.11 | CPython |
| **Retriever A — "loop" bank** | search runs in *plain code* next to the model | **Python** (BM25 / embeddings) | `serve.py`, `factbank serve` |
| **Retriever B — "template-brain"** | search compiled *inside* the model's chat template | **Jinja** (a templating language) | llama.cpp's C++ Jinja engine |
| **Guardrails** | structured extraction output | **JSON Schema / GBNF grammar** | LM Studio / llama.cpp sampler |
| **Config** | deployment settings | **TOML** | Python `tomllib` |
| **Model container** | the shipped model + baked bank | **GGUF** (binary format) | llama.cpp / LM Studio |

> **The one-sentence version:** the bank is **JSONL**, the code is **Python**,
> and the retriever is **either Python (BM25) or Jinja (in-GGUF)** depending on
> which chapter you're in.

---

## 1. Python — the code layer

**What it is:** the general-purpose language everything in the repo is written
in — the retrieval loop, the entry gates, both extractors, the mock/real
servers, the tests, the bake tools.

**Where used**
- `package/factbank/` — the installable package (`factbank` v0.1.0)
- `NEW BANK/factbank/factbank/` — all research code
- `template-brain-v3.1/` — the bake tools, miners, parity gates

**Version** *(repo-verified)*
- Package: `requires-python = ">=3.11"` (`package/pyproject.toml`)
- Research code: header says `Python >= 3.10` (`| ` union types, `ast` features
  used in `codecheck.py`)
- **Effective floor: 3.11+** for the package.

**Runtime dependencies** *(repo-verified — deliberately tiny)*
- `numpy>=1.26` — embedding-matrix math (research env pins `2.4.6`)
- `rank-bm25==0.2.2` — the BM25 retriever (see §4)
- The nomic embedder must be reachable over HTTP (see §5); it is **not** a pip
  dependency.

**Sources & docs**
- Language: https://docs.python.org/3/
- What's new (version behaviour): https://docs.python.org/3/whatsnew/
- `ast` module (used by the scorer): https://docs.python.org/3/library/ast.html
- `inspect` (used by the miner): https://docs.python.org/3/library/inspect.html

**Limitations that actually bit this project**
- **`ast` parses structure, not behaviour.** `codecheck.py` uses `ast` to see
  what code *calls*, but it **cannot execute** it — wrong argument *values*,
  missing imports, and runtime errors are invisible. Several eval cases need
  Python 3.13/3.14 runtimes that don't exist on this machine, so "does it run?"
  is still unanswerable by static analysis alone. *(repo-verified: CLAUDE.md
  scorer section)*
- **`inspect.signature` walks the inheritance chain.** The miner (`mine_api.py`)
  used it to read every public callable — and got every inherited method too, so
  `str.join` entered the bank as a matplotlib fact. 66% of the mine was junk.
  This is a *language behaviour* (inheritance is transparent to `inspect`), not a
  bug in the idea. *(repo-verified: F-064)*
- **No sandbox in the standard library.** There is no safe way to *execute*
  candidate code to verify it; the project relies on structural checks instead.

---

## 2. JSONL — the bank storage format

**What it is:** **JSON Lines** — one independent JSON object per line, newline-
separated. Not a language; a data format. This is what a "fact" physically *is*.

**Where used** *(repo-verified)*
- `facts_v2.jsonl`, `facts_pythondata_v4.jsonl`, `facts_mined_clean.jsonl`, every
  `*.rejects.jsonl`, every saved run transcript (`*.jsonl`).

A fact looks like:
```json
{"id": "numpy2-001", "text": "np.float_ was REMOVED in NumPy 2.0 - use np.float64 instead.",
 "source": "numpy", "version": "2.0", "kind": "mistake",
 "meta": {"url": "https://numpy.org/doc/stable/numpy_2_0_migration_guide.html"}}
```

**Why JSONL and not one big JSON array:** each line parses on its own, so a
half-written file still yields every complete line, files append cheaply, and
`rescore.py` can re-judge a run line-by-line without loading it whole.

**Sources & docs**
- JSON: https://www.json.org/ · spec: https://datatracker.ietf.org/doc/html/rfc8259
- JSON Lines convention: https://jsonlines.org/

**Limitations**
- **No comments, no trailing commas, no schema.** Nothing in the *format*
  enforces that a fact has a `version` tag or a real `source` — that's the entry
  gates' job (`gates.py`), in Python. The format will happily store a lie.
- **No cross-line structure.** Deduplication, ordering, "which copy is
  canonical" — none of it lives in JSONL; it's all imposed by code.
- **Text encoding.** Files are UTF-8; a stray BOM or smart-quote can break a
  verbatim quote match, which is why `gates._canon()` normalises curly quotes and
  backticks before comparing. *(repo-verified)*

---

## 3. Retriever A — the "loop" bank (Python: BM25 + embeddings)

This is the retriever that runs as **plain Python code beside the model** —
`serve.py` / `factbank serve`. It has two interchangeable engines.

### 3a. BM25 — `rank_bm25`

**What it is:** a classic **lexical** ranking function (Okapi BM25). It scores a
document by how many of the query's *rare* words it contains, with saturation
(a term repeated 10× isn't 10× the evidence) and length normalisation. No neural
network, no training, deterministic.

**Where used** *(repo-verified)*
- `bank.py`'s `Bank` (BM25) — the default for `test_pipeline.py`,
  `serve.py --mock`, and `serve.py --bm25-only`.
- Library: `rank-bm25==0.2.2`, pinned. Pure Python. (Its Feb-2022 release *is*
  the current one — it's not abandonware, it's finished.)

**Sources & docs**
- Library: https://github.com/dorianbrown/rank_bm25 · https://pypi.org/project/rank-bm25/
- The algorithm (Robertson & Zaragoza, *BM25 and Beyond*):
  https://www.nowpublishers.com/article/Details/INR-019

**Limitations**
- **Lexical only — no synonyms.** BM25 matches *words*. "split my data" will not
  find a fact that only says `train_test_split` unless the words overlap. This
  is exactly why the project bolts on **aliases** (`scikit-learn`→`sklearn`) and
  **Doc2Token expansions** (generating the user-phrasings a fact should match).
  *(repo-verified: PROGRESS.md steps 12–15)*
- **IDF is corruptible by duplicates.** 205 copies of a fact containing `fit`
  flatten that term's inverse-document-frequency, so BM25 stops treating it as
  discriminating — the mechanism behind gold retrieval falling 12/12 → 9/12 at
  scale. *(repo-verified: F-064)*
- **Pure Python = O(corpus) per query** unless indexed; fine at a few thousand
  facts, not a search engine.

### 3b. Embeddings — `HybridBank` + nomic

**What it is:** **semantic** search. Facts and queries are turned into vectors by
an embedding model; similarity is cosine distance. Catches meaning where BM25
catches only words. "Hybrid" = combined with BM25.

**Where used** *(repo-verified)*
- `HybridBank` in `lmstudio_embed.py` — the current retrieval path and
  `serve.py` v2's default.
- Embedder: `text-embedding-nomic-embed-text-v1.5`, served over LM Studio's HTTP
  API (must be loaded alongside the chat model).

**Sources & docs**
- Model: https://huggingface.co/nomic-ai/nomic-embed-text-v1.5
- Math is `numpy`: https://numpy.org/doc/

**Limitations**
- **Needs a live embedder.** Kills the "zero-dependency, offline" property — the
  nomic model must be running. If it's evicted, hybrid search is dead until
  reload.
- **`search_document:` / `search_query:` prefixes are mandatory** for nomic; get
  them wrong and similarity silently degrades. *(repo-verified: `gate_collision`
  encodes `search_document: ...`)*
- **Opaque failures.** A bad semantic hit gives no reason; BM25 at least points
  at the matched term.

---

## 4. Retriever B — the "template-brain" (Jinja, run inside the GGUF)

**This is the important one for limitations.** Here the retriever is not Python —
it is **compiled into the model's chat template** and runs every time the model
is prompted. The template language is **Jinja**.

**What it is:** Jinja is a text-templating language (loops, filters, conditionals
inside `{{ }}` / `{% %}`). Every chat model already has a `chat_template` written
in it — the project **rewrites that template** so it also contains the fact bank
(as an inverted index) and the search logic. Two GGUF metadata keys change; all
667 tensors stay byte-identical. *(repo-verified: CLAUDE.md layout notes)*

**Where used** *(repo-verified)*
- `baked_index_v6.jinja` (live), `bake_index.py`, `inserts/gemma4_idx/`
- The data layout is chosen *for the engine's quirks*: facts live in a **list**
  addressed by integer id (`fb_txt`), not a dict — because "minja builds lists
  fast and dicts slowly — moving the facts out of a dict cut per-request cost
  from 1318 ms to 291 ms." *(repo-verified: file header)*

### Which Jinja engine, exactly? — this changed, and the repo's names lag

There are **three** Jinja implementations in play, and they are **not identical**:

| engine | language | who uses it | role here |
|---|---|---|---|
| **Jinja2** | Python | offline gates (`parity.py`, `lab_bench.py`) | where templates are *developed & tested* |
| **minja** | C++ | *old* llama.cpp | the historical serving engine |
| **llama.cpp C++ Jinja engine** | C++ | *current* llama.cpp | what actually serves today |

> **Naming trap** *(repo-verified: F-054):* LM Studio renders by spawning
> `llama-server --jinja --chat-template-file`, and **minja is gone** — PR #18462
> replaced it. **Where the repo says "minja", read "llama.cpp's C++ Jinja
> engine".**

**Sources & docs**
- Jinja2 (the Python reference): https://jinja.palletsprojects.com/
- Template designer docs: https://jinja.palletsprojects.com/en/stable/templates/
- minja: https://github.com/google/minja
- llama.cpp: https://github.com/ggml-org/llama.cpp
- The engine swap: llama.cpp PR #18462

### Limitations of Jinja-as-a-retriever — every one measured here

This is a language never meant to run a search engine, so its limits are sharp:

- **Jinja2 ≠ the C++ engine. Same template, different results.** This is the
  headline limitation and the reason `parity.py` is a **mandatory gate**
  (22/22 or do not ship). Concretely *(repo-verified: PROGRESS.md #10, F-050)*:
  - the C++ engine's **`.split()` does NOT collapse whitespace**, Python's does;
  - operator **precedence differs**: `d[x | int]` parses differently;
  - a template that retrieves 5 facts in jinja2 retrieved 1 in the real engine.
  **Every offline gate renders with jinja2 — so an un-parity-checked template is
  measuring a language you don't ship.**
- **No mutable dict item assignment.** `probe_minja.py` tested 31 features:
  **29 work** — including the surprises `sort`, `.append()`, `selectattr` — but
  **dict item assignment fails**. The whole index layout is designed around this
  (build lists, never mutate dicts). *(repo-verified: probe result 29/31)*
- **Re-parsed on every request.** The engine re-renders the template for each
  prompt, so template *bytes* used to be a latency tax (~0.15–0.33 ms/fact on the
  linear scanner). The inverted index made cost scale with the *query* not the
  bank — but the property is a landmine: naive layouts are O(bank) per token.
  *(repo-verified: F-045 retired by F-055)*
- **Dicts are slow to build.** See the 1318 ms → 291 ms fix above. A "language
  limitation" that dictates the entire data structure.
- **No debugger, no stack trace worth reading.** A logic bug surfaces as *wrong
  facts retrieved*, not an error — which is why retrieval is gated against a
  hand-built `gold.json` (12 cases) offline.

---

## 5. Structured-output guardrails — JSON Schema & GBNF grammar

**What it is:** when the LLM *extracts* facts, its output shape is forced by a
grammar at the sampler level, so invalid JSON / invalid `kind` labels become
literally unsamplable.

**Where used** *(repo-verified)*
- `extract.py::CANDIDATES_SCHEMA` — a JSON-Schema `response_format`, verified
  live on LM Studio + llama-server (2026-07-13). Locks the `kind` enum, kills the
  invented-label and parse-failure classes.

**Sources & docs**
- JSON Schema: https://json-schema.org/
- OpenAI-compatible structured output (the `response_format` field the servers
  accept): https://platform.openai.com/docs/guides/structured-outputs
- llama.cpp GBNF grammars (what the constraint compiles to):
  https://github.com/ggml-org/llama.cpp/blob/master/grammars/README.md

**Limitations**
- **Shape ≠ truth.** *"Structured output guarantees shape, never content — same
  boundary as the quote gate: valid JSON ≠ valid facts."* A grammar cannot stop a
  fabricated quote or a wrong library attribution; that's the gates' job.
  *(repo-verified: F-037)*
- **Backend support varies.** `extract.py` falls back to a plain prompt on HTTP
  400 — not every endpoint honours `response_format`.

---

## 6. Config — TOML

**What it is:** a minimal, human-readable config format (`key = value`, sections
in `[brackets]`). Python reads it natively via `tomllib` (3.11+).

**Where used** *(repo-verified)*
- Deployment config `factbank.toml` (in `C:\Users\mhnda\factbank\`),
  `sources.toml` (watch overrides), `pyproject.toml` (package metadata).

**Sources & docs**
- Spec: https://toml.io/ · `tomllib`: https://docs.python.org/3/library/tomllib.html

**Limitations**
- **Read-only in the stdlib.** `tomllib` *parses* but cannot *write* TOML — you
  need a third-party writer to emit it. Fine here (config is hand-edited).
- No schema; a typo'd key is silent until code looks for it.

---

## 7. Model container — GGUF (and its metadata trap)

**What it is:** the single-file binary format that holds a quantised model
(weights + metadata, including the `chat_template`). Not a language; the box the
template-brain ships in.

**Where used** *(repo-verified)*
- Every shipped model; `factbank bake` writes one; `bake_index.py` embeds the
  bank into the template inside it.

**Sources & docs**
- Spec: https://github.com/ggml-org/ggml/blob/master/docs/gguf.md
- llama.cpp (reads/writes GGUF): https://github.com/ggml-org/llama.cpp
- Python tooling: https://pypi.org/project/gguf/

**The ~1 MB "wall" is DEAD — size is NOT a limit** *(repo-verified: F-053 → F-059,
and `bake_index.py` which enforces exactly this)*
- **Bytes were never a limit on the format, the engine, or the bank.** The cap
  lived in **one place only** — LM Studio's *raw-GGUF metadata reader* — and it is
  **beaten and proven beaten.** `bake_index.py` sets **no default cap**; the guard
  is opt-in via `--route rawgguf`.
- **The shipping route has no ceiling.** A Hub `model.yaml`
  `llm.load.promptTemplate` delivers multi-MB templates — **proven live at 1.5 MB
  and 2.0 MB**, manifest accepted intact. This is the plan of record
  (`FACTBANK-SHIPPING-BLUEPRINT.md`). llama.cpp likewise has no practical limit
  (cap 1 GiB) and errors *loudly*, never silently.
- **The real constraint is recall, not bytes** (F-055/F-056): 21,203 facts /
  5.06 MB renders a matched query in 218 ms; what runs out is the ranker's focus,
  not the byte budget.
- *History (F-053, kept only so nobody re-derives it the hard way):* the cap once
  looked like a hard wall because LM Studio's raw-GGUF **metadata reader** swapped
  any over-long template for a 48-char sentinel
  (`[LM Studio Patch - String too long; didn't read]`) — model loads "fine,"
  answers garbage. F-059 proved this was a *reader* bug on one route, not a limit.
- **The one gotcha that still bites during dev:** the metadata cache is **stale
  by default**. An edited template can reload as the *old* one from
  `~/.lmstudio/.internal/gguf-metadata-cache.json`. After any bake, **verify the
  cached `chatTemplate` length equals what you baked** before trusting a run — on
  the raw route via that JSON, on the `model.yaml` route via
  `lmstudio_yaml_test/check_override.py` (reads the real process cmdline). This is
  a *cache-invalidation* gotcha, not a size limit.
- `model.yaml`-route traps (not limits): **LOAD-only** — also setting
  `llm.prediction.promptTemplate` → HTTP 500; `metadataOverrides` is mandatory.

---

## 8. The HTTP interface (not a language, but the glue)

Everything talks to the model over the **OpenAI-compatible chat-completions
API** (`POST /v1/chat/completions`), served by **LM Studio** on
`127.0.0.1:1234` or a spawned **llama-server**.

**Sources & docs**
- API shape: https://platform.openai.com/docs/api-reference/chat
- LM Studio: https://lmstudio.ai/docs · llama.cpp server:
  https://github.com/ggml-org/llama.cpp/tree/master/tools/server

**Limitations that cost real time here** *(repo-verified: F-018, F-009, F-008)*
- **LM Studio silently drops `chat_template_kwargs`.** `enable_thinking` has *no
  effect* per-request — thinking is a **global UI toggle**, a between-run
  variable. llama-server honours it; LM Studio eats it.
- **`max_tokens` is one shared budget** for reasoning *then* answer. Blow it and
  the backend returns `content=""`, `finish_reason="length"`, **no error** — a
  budget failure disguised as an architecture failure. `loop.py` / `extract.py`
  raise `Truncated`; never swallow it.
- **Never quantise the KV cache on sub-1B models** (Q4 KV → word salad).

---

## 9. Summary table

| language / format | layer | source of truth | headline limitation |
|---|---|---|---|
| **Python ≥3.11** | all code | docs.python.org | `ast` sees structure, not runtime; `inspect` walks inheritance |
| **JSONL** | the bank | jsonlines.org | no schema — stores lies as happily as facts |
| **BM25 (`rank_bm25`)** | retriever A | github.com/dorianbrown/rank_bm25 | lexical only; duplicates poison IDF |
| **Embeddings (nomic)** | retriever A | huggingface nomic-embed-text-v1.5 | needs a live embedder; opaque hits |
| **Jinja (C++ engine)** | retriever B | jinja.palletsprojects.com + llama.cpp | jinja2 ≠ serving engine (parity gate); no dict-item assign; re-parsed per request |
| **JSON Schema / GBNF** | extraction guard | json-schema.org / llama.cpp grammars | guarantees shape, never truth |
| **TOML** | config | toml.io | stdlib parses but can't write |
| **GGUF** | model container | ggml gguf.md | none on the shipping route — the ~1 MB wall is dead (F-059); only the legacy raw-GGUF-by-hand route caps, and it degrades not bricks |
| **OpenAI chat API** | transport | platform.openai.com/docs | LM Studio drops `chat_template_kwargs`; shared token budget fails silently |

---

## 10. The rule underneath all of it

The whole architecture is a **separation of languages by trust**:

- **Python code decides what is true** (it reads the real library; it can verify
  a quote) — never the model.
- **JSONL holds the facts** as inert text — no logic, no trust.
- **Jinja/BM25 decide what is *relevant*** — retrieval, not truth.
- **The model only proposes and reasons** — it never gets the truth seat.

Every limitation above is survivable because no single language is asked to do a
job it can't: the format doesn't validate, the template doesn't judge truth, the
grammar doesn't check facts, and the model doesn't decide what's real. The gates,
in Python, are where those responsibilities meet.
