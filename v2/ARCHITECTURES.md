# The three FactBank "bake" architectures — don't conflate them

Three distinct retrieval systems in this repo are all loosely called "the FactBank bake." They are
**not** the same design, and — critically — **the one that produced the headline Gemma pass@1 numbers is
NOT the one described by the soft-door / pointer / MMR / HyDE recipe** in `extractor/BLUEPRINT.md` and
`README.md`. That recipe is a *different* system (the Python served-loop prototype). This page names all
three so a reader never attributes one system's behaviour to another.

Everything below is verified against the code paths named in each row.

> **Pointer (2026-07-18):** `extractor/EXTRACTOR-2.0.md` §6-7 is the newest proof point for the
> Served-Loop family below — a HyDE double-key + authority-framing + thinking-ON retrieval, proven
> **served** (own `llama-server`, no bake) against `gemma-4-12b-qat` for the appsec expert (3,984
> facts, 1,075 w/code, audited). **SHIPPED 2026-07-19:** the security expert is now baked ×3 sizes
> (e2b/12b/26b) × both thinking editions and published (LM Studio Hub + HF). NOTE: the SHIPPED baked
> GGUFs do **prompt-only** retrieval (in-template) and score **weaker** than these served/HyDE draft-key
> numbers — treat the served result as the retrieval-method ceiling, not the shipped GGUF. See the
> System 2 note below; that result does not change the Baked-Index or Static-Bake rows.

## The three systems

### 1. Baked-Index — the one that was benchmarked
- **Code:** `bake/template-brain-v3.1/inserts/gemma4_idx/fb_gen.jinja` (baked via
  `bake/template-brain-v3.1/bake_index.py`; adapters `adapt_gc.py`, `adapt_secnet.py`).
- **Runs where:** *inside* the GGUF chat-template, executed by llama.cpp at render time (no Python).
- **What it does:** reads **ONLY the final user message**; applies a **HARD library gate** — facts whose
  library/tab is not selected are **excluded** from scoring; scores the surviving facts with an
  **inverted-index term match**; injects the **top-N**.
- **Does NOT have:** no draft/HyDE second key, no pointer chains, no MMR, no soft doors.
- **Produced:** the GitChameleon **12b (37.8%→44.2%)** and **26b (43.4%→46.2%)** execution pass@1, and
  the Security & Networking **26b** results (easy 21/30→27/30, hard 16/18→18/18). This is the shipped baker.

### 2. Served-Loop — the full Python recipe (prototype)
- **Code:** the Python `lookup.retrieve` prototype (`extractor/lookup.py`); the recipe documented in
  `extractor/BLUEPRINT.md` §WHAT WORKS #8 and `extractor/PROGRESS.md` §2.
- **Runs where:** a Python served loop (draft → search bank → re-derive), **not** inside the GGUF.
- **What it does:** **soft doors** (multiply the matching door's score, never exclude — fail open) +
  **classic pointer chains** (bucket by lib+namespace) + **richer associative keywords** + **MMR**
  (dedup near-duplicates) + **double-key (HyDE)**: search with the user prompt AND the model's draft
  (prompt hits outrank draft hits; draft key capped).
- **Produced:** the Python-only retrieval results (7/8 hand-read hits at 508 facts / 4 doors) and the
  **Qwen authority probes**. Proven in Python; **NOT yet Jinja/engine-verified** for the baked path.
- **2026-07-18 update (same family, sibling code path):** `appsec_servetest.py::retrieve` reproves this
  HyDE double-key recipe (prompt + model's draft) for the appsec expert, with **authority-framing +
  thinking-ON** now the default injection posture, served against `gemma-4-12b-qat` on the repo owner's
  **own `llama-server`** (`--jinja`, NOT LM Studio — LM Studio drops `chat_template_kwargs`), Gemma-native
  sampling (temp 1.0/top_k 64/top_p 0.95/min_p 0.01). Result: **SECURE@1 base 14/15 → bank 15/15, zero
  regressions.** This is a **served** (HyDE draft-key) result — the **retrieval-method ceiling**, NOT the
  shipped GGUF: the security expert baked+shipped 2026-07-19 (×3 sizes × both editions) does prompt-only
  in-template retrieval and scores lower (it does not close F-050). Full writeup:
  `extractor/EXTRACTOR-2.0.md` §6-7.

### 3. Static-Bake — no retrieval at all
- **Code:** `package/factbank/bake.py`.
- **Runs where:** bakes ALL facts into one **static system prompt**; the model sees the whole bank.
- **What it does:** no retrieval, no draft, no gate, no ranking — every fact is always present.
- **Produced:** the package's simple whole-bank delivery route (bounded only by context/size).

## Capability matrix

| system | reads draft key (HyDE)? | library gate | MMR? | pointer chains? | soft doors? | which results |
|---|---|---|---|---|---|---|
| **Baked-Index** (`inserts/gemma4_idx/fb_gen.jinja`) | ❌ (final user msg only) | **HARD** (excludes) | ❌ | ❌ | ❌ | **the Gemma 12b/26b + Security pass@1 numbers** |
| **Served-Loop** (`extractor/lookup.py`) | ✅ prompt + draft | **soft** (nudge, fail open) | ✅ | ✅ | ✅ | Python 7/8 hand-read; **Qwen authority probes** |
| **Static-Bake** (`package/factbank/bake.py`) | ❌ (no retrieval) | none (all facts) | ❌ | ❌ | ❌ | whole-bank static-prompt route |

## The one thing to remember
When a doc states the **soft-door + pointer + MMR + HyDE** recipe next to a **baked benchmark result**,
the recipe describes **Served-Loop (system 2)**, while the result came from **Baked-Index (system 1)** —
a simpler hard-gated, single-query inverted index. Closing that gap (porting the full recipe into the
baked Jinja path and re-verifying in-engine, F-050) is open work, not a done fact.
