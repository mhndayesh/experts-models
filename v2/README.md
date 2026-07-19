# FactBank — v2 (standalone, latest-only)

A clean, self-contained snapshot of the project: **only the current version of each part**, no
superseded generations, no giant binaries, no archive. Built 2026-07-15.

## What FactBank is
A stock LLM answers correctly about fast-moving libraries it was never trained on, by carrying a
searchable bank of **landmine facts** (post-cutoff / reverses-a-habit / silent-failure) — either
inside its GGUF chat-template or via a served loop. The model supplies reasoning; the bank supplies
knowledge. Works untrained, across model sizes (3b/12b/30b).

> **Building an expert end-to-end?** Start at **[`BUILD-AN-EXPERT.md`](BUILD-AN-EXPERT.md)** — the A-to-Z
> playbook (base GGUF → running expert): every step, rule, and trap, with the exact commands.

## The map
| folder | what it is | start here |
|---|---|---|
| **`extractor/`** | **The current fact-making engine** (LLM-first, structured; **2.0 rebuild, 2026-07-18** — shared `appsec_core.run` pipeline + thin per-source adapters, code lives IN the fact as verbatim `code_bad`/`code_good`). Builds fact banks from docs. Includes the first built expert (**AI-ML, 817 facts, 11 doors**) and the **security/appsec** expert (**258 concepts (254 CWE) → 3,984 variants**, `FINAL_v3.jsonl`, **BAKED + PUBLISHED** ×3 sizes × both thinking editions). | **`extractor/EXTRACTOR-2.0.md`** (canonical — supersedes the mining/repair/dedupe/retrieval sections below) → `extractor/BLUEPRINT.md` → `extractor/EXTRACTOR-SPEC.md` |
| `extractor/experts/ai-ml/` | The AI-ML expert bank + its coverage spec | `COVERAGE.md` |
| `extractor/sources_harvested/` · `sources_ext/` | the source docs the extractor mined (self-contained) | — |
| **`serving/`** | How a bank ships **inside a GGUF** and is delivered (retrieval + native tool lane) | `serving/README.md` → `serving/LIMITS.md` |
| **`bake/`** | The code that bakes a bank into a GGUF's chat-template (inverted index). Code + docs only; the 7 GB model artifacts are archived in `archive/pre-v2-2026-07-15/template-brain-v3.1/`. | `bake/…/bake_index.py` |
| **`package/`** | The installable `factbank` package (serve/watch/bake CLI) | `package/…` |
| **`decisions/`** | The live decision blueprints — shipping, packaging, languages, DB research, card-mining record | `decisions/*.md` |
| **`papers/`** | Final papers only | `papers/` |

## Current state (headline)
- **Fact-making is solved and blueprinted.** Pipeline: **FIND (migration guides) → extract → repair
  → check**. Proven: k8s 96.5%, messy pydantic 97.8% clean, all hand-read. See `extractor/BLUEPRINT.md`
  (what works / what doesn't) and `PROGRESS.md`. **Superseded 2026-07-18** by the **2.0 rebuild**
  (`extractor/EXTRACTOR-2.0.md`, canonical): "check" is now a **mandatory** two-pass verification
  (currency-verify + an adversarial correctness audit) — grounding proves a quote is REAL, not CORRECT
  or CURRENT; ~3.8% of the appsec bank's facts were wrong/stale before that audit caught them.
- **First expert built: AI-ML** — 817 facts, 11 doors (openai/langchain/llamaindex/google/transformers/
  vllm/pydantic/llama-cpp/hf-datasets/langgraph/anthropic). Rich, not model-gated.
- **GitChameleon expert built + baked + BENCHMARKED** — 4,167 facts / 23 doors, baked into gemma-4
  **12b + 26b** GGUFs; parity **CLOSED** (bank fires in llama.cpp). **Execution pass@1 (249/328 buildable,
  hand-verified): 12b 37.8%→44.2% (+6.4), 26b 43.4%→46.2% (+2.8)**, thinking-OFF. Full write-up:
  `eval/gitchameleon/BAKE-REPORT.md`.
- **The reasoning finding.** Chain-of-thought *reverts* landmine facts to the model's trained prior
  (12b thinking-ON drops to 36.9%) — proven by convergence to the no-bank answer. Cure: ship thinking-OFF,
  or for thinking-native models use **authority framing** (Qwen3-4B-Thinking: 18/18 framed authority
  trials — 3 conditions × 6; a 0/6 unframed control is reported but was not retained as a log). **Two-pass**
  (authority+thinking on the failures) lifts the 12b **44.2%→54.2% (+10)** — frontier-greedy territory
  from a Q4 12B local model. See `eval/gitchameleon/QWEN-THINKING-AUTHORITY.md`.
- **Web expert department built** (2026-07-16) — 9 banks / 279 facts (tailwind v4, pydantic v2, react 19,
  svelte 5, vue 3, sqlalchemy 2.0, django, express, nextjs), DeepSeek-extracted, 100% quote-grounded. See
  `extractor/experts/web/COVERAGE.md` and the department catalog `extractor/experts/DEPARTMENTS.md`.
- **Security & Networking department built + baked + tested on THREE model sizes** (2026-07-16/17) — 114
  landmine facts, 7 libraries, baked into stock **e2b (~2B) / 12b / 26b** GGUFs and hand-verified in-engine
  (48 questions each, authority + thinking-ON, Gemma-native sampling, 6-parallel):
  **e2b 19→32/48 (+13), 12b 27→39/48 (+12), 26b 37→45/48 (+8).** The curve: raw lift shrinks with model size
  but error-closure rises (45%→57%→73%) — small models need the bank most, big models use it best. e2b needed
  its own template re-anchoring (different revision); 12b/26b share one. See
  `extractor/experts/security-networking/` (`BAKE-TEST-CURVE-3MODEL.md`, per-model reports) and
  `bake/template-brain-v3.1/E2B-BAKE-NOTES.md`.
- **Two more security experts built, baked ×3, tested, and PUBLISHED** (2026-07-17) —
  **offsec** (offensive security + RE: 17 libs / 489 facts) and **dataplane** (eBPF + kernel/userspace net:
  7 libs / 318 facts). Hand-scored base→baked (thinking-ON + authority): offsec e2b 12→37, 12b 12→43, 26b
  17→43 (/44); dataplane e2b 5→32, 12b 16→41, 26b 20→43 (/47). See `extractor/experts/{offensive-security-re,
  ebpf-dataplane}/`.
- **All three security experts published to HF + GitHub with the gate-alias fix** (2026-07-17) — a rename's
  OLD/natural name now opens the retrieval tab (`gen_gate_aliases.py` → `bake_index.py --extra-aliases`).
  netsec was re-baked in place (old bake tagged `v1-pre-gate-fix`). 9 HF repos, one collection. Local baked
  GGUFs were then deleted to save disk (~89 GB) — HF is the canonical store; re-bake from base + bank anytime.
- **Security / appsec expert — SHIPPED (2026-07-18/19), all 3 sizes × BOTH thinking editions.** The 2.0
  mine (single shared `appsec_core.run` pipeline + thin per-source adapters; code lives IN the fact) was
  **rebuilt as the v3 faceted concept→variant bank** (`experts/appsec/facts/FINAL_v3.jsonl` — **258 CWE
  concepts → 3,984 variants**, `SCHEMA-V3.md`) after a MANDATORY adversarial correctness audit (~3.8%
  wrong/stale removed), then **baked and published**: **LM Studio Hub** (6 virtual models
  `gemma-4-{e2b,12b,26b-a4b}-security-expert` [+`-thinking`], 4.18 MB bank via model.yaml) + **Hugging Face**
  (3 GGUF repos, both editions each; "Information Security EXPERTS" collection). **Thinking-ON was made to
  work** (Gemma-4 gen-prompt thought-channel fix + strong authority framing + forced `enable_thinking`; see
  `decisions/TICKET-thinking-on-enablement.md`); ~10% hard-reasoning residual → both editions ship. Cross-model
  SecurityEval (shipped baked, thinking-off, 21-task subset): e2b 13 · 12b 17 · **26b 19** vs DeepSeek-V4 14 —
  12B/26B+bank beat the cloud model (`experts/appsec/benchmark/SCORECARD-crossmodel.md`). **Note:** the shipped
  in-template retrieval is **prompt-only** and weaker than the served-loop + HyDE draft-key ceiling (which hit
  base 14→25 served). Canonical: **`extractor/EXTRACTOR-2.0.md`** + `decisions/SCHEMA-V3.md`.
- **Draft paper:** `papers/FACTBANK-DRAFT.md` (work in progress — kept as a draft).
- **Retrieval recipe** (the **Served-Loop** Python prototype, proven in Python): soft doors + classic
  pointers + richer keywords + MMR + double-key (HyDE). NOTE: the **baked GGUF** that produced the Gemma
  12b/26b and Security pass@1 numbers used a simpler **hard-gated, single-query inverted-index** retriever,
  NOT this full recipe. The three distinct "bake" systems are laid out in [`ARCHITECTURES.md`](ARCHITECTURES.md).
- **Baking + serving (proven):** `bake/…/bake_index.py` → run via `llama-server` (NOT LM Studio raw-load,
  F-053; size wall OVERCOME). Launcher `bake/serve_factbank.ps1`.
- **Still open:** Web / AI-ML departments not yet baked/scored; a Linux/Docker harness to score the 79
  Windows-unbuildable GitChameleon problems. (e2b bake DONE; netsec/offsec/dataplane **and security/appsec**
  shipped ×3 sizes.)
- **`archive/`** holds all run outputs (solutions/transcripts/results/logs), superseded docs, and one-off
  scripts — the evidence trail, kept out of the clean front. See `archive/README.md`.

## Deliberately EXCLUDED from v2 (and where it lives)
- **`archive/`** (1.5 GB historical evidence, F-001…F-065) — stays at repo root; it's the proof trail.
- **Superseded generations:** the rules-based `card-mining/` extractor (replaced by `extractor/`),
  `NEW BANK/` research code, old template-brain generations.
- **Binaries:** GGUFs, model weights, template inserts — archived in `archive/pre-v2-2026-07-15/template-brain-v3.1/`.
- v2 carries the **latest code, docs, papers, and blueprints** — the intellectual content, standalone.

## The one law (from the blueprint)
**Source targeting decides everything.** A perfect extractor on the wrong document yields a bank of
the wrong facts. Find the migration guide first; extract second.
