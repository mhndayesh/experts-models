# Landmine Facts: Teaching Untrained Language Models Post-Cutoff Library APIs with a Baked Fact Bank — and Why Reasoning Fights the Fix

**DRAFT — 2026-07-16. Incomplete references; numbers provisional pending a faithful (Docker) benchmark
re-run.** Working paper. All GitChameleon pass@1 figures below come from a **local, non-Docker harness**
(maps Python 3.7/3.8→3.9 and does not key its venv cache on dependencies — see §6), so they are internally
fair (base and baked scored on the same 249-problem buildable set) but **not** directly comparable to the
official Docker leaderboard. Numbers are hand-verified. Not yet peer-reviewed.

---

## Abstract

Large language models write plausible but wrong code for library versions released after their
training cutoff: they reach for the API they learned, which the new version renamed, removed, or
silently changed. We show that a stock, **untrained** model can be made version-correct by giving it a
small, curated **fact bank** — post-cutoff "landmine" facts (each version-tagged and grounded to a
source quote) delivered at inference time, either inside the model's own GGUF chat-template or via a
retrieval loop. The model supplies reasoning; the bank supplies knowledge. On GitChameleon 2.0, an
execution-scored benchmark of 328 version-conditioned Python problems, baking a 4,167-fact bank into
two quantized Gemma GGUFs raises execution pass@1 without touching a single weight: **+6.4 points on a
12B model (37.8%→44.2%, 94→110/249)** and **+2.8 on a 26B MoE (43.4%→46.2%, 108→115/249)**, measured on
the 249 problems whose pinned environments build on our machine. These are **local-harness provisional**
figures — base and baked are scored on the identical 249-problem set (internally fair) but on a non-Docker
harness, so they are not directly comparable to the official Docker leaderboard.

We then report a counterintuitive and, to our knowledge, unremarked finding: **enabling chain-of-thought
reasoning makes the bank *worse***. On the same 12B model, thinking-on drops pass@1 to **36.9% (−7.3)**.
The cause is mechanistic, not incidental: a landmine fact is by construction a *habit reversal*, and
extended reasoning re-weights the decision toward the model's trained prior — so the prior argues the
injected fact away. We prove this by convergence — the reasoning model's committed answer matches the
answer of the *base model with no bank at all*. Reasoning also spirals into its own priors and truncates
to an empty answer on ~30% of problems. Finally, we show a cure for **thinking-native** models that cannot
disable reasoning: framing the fact as **authoritative** ("verified, absolutely correct for this version,
supersedes your training") holds fact-adherence at **18/18 across framed authority trials** (3 conditions
× 6 trials, all pass; an unframed 0/6 control is reported but was not retained as a log — treat it as
illustrative) on the hardest landmine, and lets a
**4-billion-parameter** thinking model solve an easy→hard difficulty ladder (3/4), failing only a problem
no fact bank could fix (a numerical-stability implementation, not an API fact).

---

## 1. Introduction

The knowledge in a language model's weights is frozen at its training cutoff, but the libraries people
code against are not. Between cutoff and deployment, a fast-moving library ships releases that rename
attributes (`falcon`: `Response.body` → `Response.text`), remove functions, flip default arguments, or
change a return type with no error at the call site. A model that "knows" the library from training will
confidently emit the *old* API. The failure is quiet: the code looks right, imports resolve, and it
breaks only at runtime or, worse, silently computes the wrong thing.

The usual answer is retrieval-augmented generation (RAG): attach a document store and fetch relevant docs
per query. RAG works, but it externalizes the knowledge — it needs a live retrieval service alongside the
model, and it retrieves *prose* the model must still read and interpret. We ask a narrower, more portable
question: **can the correction ride inside the model artifact itself**, so that a stock GGUF, loaded
anywhere with no companion server, answers version-correctly?

Our thesis — **FactBank** — is that it can, if three things hold:

1. **The knowledge is distilled to landmines, not documents.** We do not carry the library's docs. We
   carry only facts that *bite*: post-cutoff changes, habit reversals, and silent-failure traps. Each is
   one sentence, version-tagged, and grounded to a verbatim source quote.
2. **The model is asked to reason, never to memorize.** The weights remain the "fuzzy core" — good at
   synthesis and code structure. The bank is a "frozen core" — read-only exact knowledge. The two are
   kept separate.
3. **Delivery is code-driven, not tool-choice.** Retrieval is not a decision the model makes; it happens
   deterministically, and the retrieved facts are placed in context before the model answers.

This paper makes four contributions:

- **A method** for building and delivering fact banks: an LLM-first structured extractor with
  code-verified fields and quote-grounding, and a *baking* procedure that rewrites a GGUF's chat-template
  to carry an inverted-index retriever plus the bank, so the correction is in the file (§4–5).
- **An evaluation** on GitChameleon 2.0 showing untrained, in-artifact banks lift execution pass@1 on two
  model sizes, closing the gap toward far larger cloud models (§6–7).
- **The reasoning paradox**: enabling chain-of-thought *reduces* the bank's benefit, and a mechanistic
  explanation (habit-reversal facts vs. prior re-weighting) supported by base-model convergence (§8).
- **Authority framing**: a delivery change that makes fact banks work on thinking-native models, validated
  from a controlled probe up to a difficulty ladder on a 4B model (§9).

---

## 2. Related work

**Version-conditioned code generation.** GitChameleon [Islah et al., 2025] introduced execution-scored,
version-pinned Python completion; enterprise models cluster at 48–51% greedy pass@1 (o1 51.2%, GPT-4.1
48.5%), and document-RAG lifts the best to **59.4% (Claude 4 Sonnet + RAG)** — the current best RAG figure
(the older **58.5% is GPT-4.1 + RAG**, historical, not the current frontier). We adopt GitChameleon as our
benchmark and situate our small, in-artifact banks against those numbers (§7).

**Retrieval-augmented generation.** RAG attaches an external store queried at inference. FactBank differs
in three ways: the payload is curated landmine facts rather than raw documents; retrieval is deterministic
(code-driven, no tool-choice step); and the payload can be *baked into the model file*, removing the
runtime store. Our "double-key" retrieval (searching with both the user prompt and the model's own draft)
is a HyDE-style [Gao et al.] variant specialized to name libraries the question left implicit.

**Knowledge editing / model surgery.** Weight-editing methods insert facts by modifying parameters.
FactBank deliberately does not touch weights: the same base GGUF serves with or without the bank, banks
are swappable, and there is no retraining. The trade-off is that our knowledge lives in context, not in
the weights — which, as §8 shows, has consequences under reasoning.

---

## 3. The FactBank architecture

Three components, deliberately separated:

- **Fuzzy core** — the model's weights. Holds reasoning and code structure. Never asked to recall an exact
  post-cutoff fact.
- **Frozen bank** — curated JSONL landmine facts, each version-tagged with a source. Read-only at
  inference.
- **Code-driven loop** — plain code decides to retrieve (no tool-choice), searches the bank, and places
  results in context. Draft → search → re-derive.

Two design rules proved load-bearing:

- **Double-key retrieval (HyDE).** Search with the user prompt *and* the model's draft answer; the draft
  names libraries the prompt did not. Prompt hits outrank draft hits, and the draft key is capped so it
  cannot dominate.
- **Retrieve first, filter second, fail open.** A version/door filter never decides *which* library comes
  back — only ranks within an already-relevant pool. If a filter empties the pool, we fall back to the
  unfiltered ranking. Inverting this once returned Polars facts for a Pydantic question; getting it right
  makes the filter a nudge, not a wall.

We report **two metrics** whenever possible: **USES** (did a retrieved fact reach the answer?) and **CODE**
(does the emitted code obey the fact?). The gap between them is diagnostic.

---

## 4. Building a fact bank

Facts are made by an LLM-first structured extractor in which the model does the *meaning* and dumb code
verifies every field. The pipeline is **FIND → extract → repair → check**:

- **FIND (the one law).** Source targeting decides everything: a perfect extractor on the wrong document
  yields a bank of the wrong facts. We target **migration guides and changelogs**, not release-note blogs.
- **Extract.** The extractor (DeepSeek v4-flash, thinking off, function-calling — no strict JSON-schema
  needed) emits structured facts: `{type ∈ {REMOVED, REPLACED, CHANGED}, subject, old, new, truth,
  why_it_bites, quote, keywords, lib, version}`. Deriving `type`/provenance in code rather than trusting
  the model's enum alone moved one source from 35% to 96.5% clean.
- **Repair.** A verbatim `quote` anchor is the anti-hallucination gate; `repair.py` re-grounds any
  paraphrased quote back to a real source line.
- **Check.** Field/enum validation and quote-grounding. On the GitChameleon source, fixing three checker
  bugs (an enum leak, an over-aggressive markup-normalizer, and too-narrow repair anchors) *recovered 901
  facts* that were being falsely rejected — a reminder that the checker triages, but a human reading the
  facts is the verdict.

*Method note (2026-07-18, added post-draft).* The FIND→extract→repair→check pipeline and the `{old, new,
...}` fact schema above are the **v1** method used to build this paper's bank. They have since been
superseded by **Extractor/Facts/Retrieval 2.0** (`v2/extractor/EXTRACTOR-2.0.md`, 2026-07-18): a shared
`appsec_core.run()` pipeline with thin per-source adapters (retires the parallel-agent-per-source mining
described above), sentence-boundary verbatim repair (retires the v1 ellipsis-only/≥3-word-guard/0.6-threshold
`repair_quote`), a superset Facts 2.0 schema (code now lives *in* the fact as verbatim `code_bad`/`code_good`;
the `old`/`new` keys used here are v1-only), and — the most consequential change — a **mandatory** adversarial
correctness + currency audit run after grounding (verbatim grounding proves a quote is *real*, not that it is
*true today*; auditing one comparably-built, verbatim-grounded ~4,000-fact bank still found ~3.8% of facts
wrong or stale). This paper's GitChameleon bank and the §7 results were built and scored **before** that
mandatory audit stage existed and have not been re-audited by the 2.0 standard; the numbers below stand as
reported (unchanged by this note), but should be read as not yet currency/correctness-audited.

The **GitChameleon expert bank** has **4,167 facts across 23 libraries** (torch, pandas, pytest, gradio,
pillow, scikit-learn, scipy, django, flask, sympy, networkx, numpy, and others), 100% quote-grounded,
all ids unique. Three of the benchmark's 26 libraries (`kymatio`, `lightgbm`, `tqdm`) have no prose
changelog to mine and are left uncovered — an honest ceiling.

**Retrieval recipe** (proven in Python): soft doors (a *nudge* toward the inferred library, never a wall)
+ classic pointer chains (facts bucketed by library+namespace and linked so a seed pulls its cluster) +
richer associative keywords + MMR de-duplication. Rejected alternatives: hard doors, rare-token² weighting,
a concrete-rewrite second pass, and alias tables.

---

## 5. Delivery: baking a bank into a GGUF

To put the correction *in the file*, we rewrite the GGUF's `tokenizer.chat_template` to carry an
**inverted index** over the bank plus a retriever that runs in-template at inference. The bank facts are
adapted to an index schema, an inverted index (58,877 terms) is built, and the template — 2.73 MB — is
written back into the GGUF with all weight tensors copied byte-for-byte; only metadata changes. At
inference the template forges a `factbank_search` call and injects the top-k facts as a verified
tool-response *before* the model answers — retrieval with no tool-choice step and no external service.

**Serving traps (each cost real time; all now encoded in a launcher):**
- LM Studio's raw GGUF loader silently truncates chat-templates larger than ~980 KB to a 48-char
  sentinel, so the bank never fires. We serve with **llama.cpp `llama-server`**, which honors the full
  template.
- The ROCm `llama-server` needs its HIP/BLAS vendor DLLs on `PATH`; launched from the wrong shell it
  fails to find the Windows CRT. A single launcher script fixes both.

We verify parity by rendering the baked template with `/apply-template`: for sampled problems across
libraries, the retriever fires and the *library-correct* landmine fact is present in context — the first
in-engine (not merely Python-prototype) confirmation that the baked bank retrieves.

---

## 6. Experimental setup

**Benchmark.** GitChameleon 2.0: 328 Python problems over 26 libraries, each pinned to a specific version
and scored by hidden `pytest` tests. The **official** benchmark builds each environment in **Docker with
real Python 3.7/3.9/3.10**. Our harness is a **provisional local (non-Docker) approximation, NOT the
official pinned environment**: `run_tests.py` builds venvs with `uv` but (a) **remaps Python 3.7/3.8 → 3.9**
(there is no real 3.7 interpreter on the box) and (b) keys its venv cache on `library@version@python`,
**omitting dependencies** (unlike upstream). So the environment is only an approximation of the pinned one.
**79 of 328 problems did not build on our local Windows harness**; the cause was **not isolated** — build
errors were not retained, and **53 of the 79 are Python-3.7 problems forced into 3.9** (where 3.7-era pins
often have no 3.9 wheel), so "no Windows wheels" is unproven and confounded with the 3.7→3.9 remap. We
score on the **249 that build**, excluding the same 79 from every condition for fairness, and also report
the pessimistic all-328 number (unbuildable = fail). Because base and baked run on this same local harness
and the same 249-problem set, the base-vs-baked **delta is internally fair**, but the absolute numbers are
**local-harness provisional** and not comparable to the official Docker leaderboard.

**Models.** `gemma-4-12b-qat` (Q4_0, 6.98 GB) and `gemma-4-26b-a4b-qat` (Q4_0 MoE, 14.4 GB), served via
ROCm `llama-server`; and `Qwen3-4B-Thinking-2507` (Q8_0), a thinking-native model whose chat-template
forces a `<think>` block with no disable switch. Base vs. baked use identical prompts; the only difference
is whether the template injects facts.

**Scoring.** Execution pass@1 (single greedy/low-temperature sample, pass = tests green). We additionally
**score manually**: automated counts triage what to read, but the verdict is a human reading the model
outputs against ground truth. This caught issues in both directions repeatedly.

---

## 7. Results: untrained in-artifact banks lift pass@1

| model (Q4, `llama-server`) | base | **+ baked bank** | Δ |
|---|---|---|---|
| **12B** gemma-4-12b-qat | 94/249 = 37.8% | **110/249 = 44.2%** | **+6.4** (fixed 30 / broke 14) |
| **26B-A4B** gemma-4-26b-a4b-qat | 108/249 = 43.4% | **115/249 = 46.2%** | **+2.8** (fixed 21 / broke 14) |

*Local-harness provisional (see §6): base and baked scored on the same 249-problem buildable set on our
non-Docker harness — internally fair, but not directly comparable to the official Docker leaderboard.*

Both sizes improve, and the lift **shrinks as the base grows stronger** — the 26B already knows more of
the post-cutoff surface. Hand-reading all 14 breaks and a sample of fixes confirmed the verdicts are real
(e.g., `sklearn` `make_sparse_coded_signal` return; `torch.stft` `return_complex`; `falcon` `.body`→`.text`).
There were zero empty answers on either side (no artifact inflating the gap).

**In context.** GitChameleon's enterprise baselines are **48–51% greedy** on all 328 (o1 51.2%, GPT-4.1
48.5%) — but those are 100B–400B-parameter *cloud* models, and document-RAG lifts the current best to
**59.4% (Claude 4 Sonnet + RAG)** (the older 58.5% is GPT-4.1 + RAG, historical). Our 12B+bank at 33.5% over all 328
(the pessimistic basis) lands in **Llama-3.3-70B territory (36.3%)** — a model roughly 6× its size — and
the bank's lift is the same *kind* of gain RAG gives the large models (+8–11 points), delivered in-artifact
with no retrieval server. We do not beat o1; the claim is that a *bank turns a small local model into
something that scores like a much larger one*. (No published GitChameleon numbers exist for the current
frontier — GPT-5.5, Claude Opus 4.x — so we cannot compare against those.)

---

## 8. The reasoning paradox: chain-of-thought makes the bank worse

The natural next step — let the model *think* before answering — backfires. On the baked 12B with
thinking enabled (temperature 0.6, 8k token budget, 16k context):

| baked 12B | pass@1 (249 buildable) |
|---|---|
| thinking **OFF** | **44.2%** |
| thinking **ON** | **36.9%** (−7.3) |

Two mechanisms account for the entire loss.

**(a) Reasoning spirals into its own priors and truncates.** On 30.2% of problems the answer came back
empty: the model restated its reasoning without closing the `<think>` channel, consumed the token budget,
and produced no code (`finish_reason = length`). Raising the budget did not help — reasoning simply
spiraled longer (one problem grew from 14k to 28k characters without terminating). Pass rate is strongly
monotone in reasoning length: problems with under 4k characters of reasoning pass **73%**; those over 16k
pass **14%** (and 56% of those are empty).

**(b) Where it does commit, reasoning reverts to the trained habit.** A landmine fact is, by definition, a
*habit reversal* — the correct post-cutoff answer contradicts what the model learned. With thinking off,
the template injects the fact and the model commits it before its weights get a vote. With thinking on,
the model deliberates *from its parameters*, and the learned habit reasserts itself and argues the fact
away. We prove this by **convergence**: on the non-empty regressions, the baked+thinking answer is
**identical to the base model with no bank at all** —

| problem | base (no bank) = learned habit | baked, think-OFF = fact | baked, think-ON |
|---|---|---|---|
| falcon `custom_body` | `status.body` | `status.text` ✓ | **`status.body`** (reverts) |
| pandas groupby | `observed=False` | `observed=True, dropna=False` ✓ | **`observed=False`** (reverts) |

The fact is present in context (verified); thinking-off applies it; thinking-on makes the bank a no-op.
Critically, on the 185 problems where the reasoning model *did* commit an answer, its accuracy is a
statistical tie with thinking-off (49.2% vs 50.3%) — reasoning adds no accuracy, because the knowledge is
in the injected fact, not in the weights; it only adds variance and the reversion failure mode.

**Interpretation.** For *deriving* an answer, deliberation helps. For *applying a single injected fact that
contradicts training*, deliberation is counterproductive: it re-activates exactly the learned behavior the
bank exists to override. The empties and the reversions are one phenomenon — given room to think, the model
pulls back toward its training. **For habit-reversing facts, retrieve-and-commit beats retrieve-and-
deliberate**, and the practical prescription is to ship such banks **thinking-off**.

---

## 9. Authority framing: making banks work on thinking-native models

Some models cannot be run thinking-off. `Qwen3-4B-Thinking-2507`'s chat-template forces `<think>` with no
disable switch. On the hardest landmine (falcon `.body`→`.text`), the bare fact in context reverts to the
habit — an unframed control of **0/6** correct across repetitions (reported from a session read but **not
retained as a log — illustrative, not measured**) — reproducing §8's mechanism on a second, different model.

The cure is to change how the fact is *framed*. We prepend an **authority directive**:

> "The VERIFIED FACTS below are extracted from the official changelog and are **ABSOLUTELY CORRECT** for
> this exact version. They **SUPERSEDE your training**, which is older and may be wrong here. If a fact
> contradicts your instinct, your instinct is stale training and **the fact wins**."

**Result: 18/18 framed authority trials pass** (3 conditions × 6 trials each, all correct) — fact in the
system prompt (A), fact via a forged tool-response (B), or both (C). The retained log
(`probe_qwen_authority_log.jsonl`) is exactly these 18 framed rows; the unframed 0/6 control was **not
retained as a log** and is illustrative, not measured. Findings:

- **The active ingredient is the authority stance, not the channel.** Every framed channel passes
  (18/18); the illustrative unframed control reverts (0/6). This decouples *retrieval* (getting the fact into context, already solved)
  from *trust* (getting the model to obey it over its prior) — authority framing is the trust lever.
- **Combining channels is redundant, not additive** (C = A = B = 100%); ship one channel, the system
  prompt is cheapest.
- **Authority framing does not reliably shorten reasoning.** An early single-run read suggested it did; a
  controlled rerun showed that was noise — reasoning length is governed by intrinsic problem difficulty
  (an enum-mutation puzzle stays long regardless) and sampling temperature. Guaranteed-short reasoning
  needs a hard `</think>` cap, a separate mechanism.

**End-to-end validation.** We then ran the full pipeline — the same 4,167-fact bank retrieved per problem
(soft doors + pointers + MMR, k=5) and injected via the authority prompt — on the raw 4B thinking model,
and evaluated a difficulty ladder defined by how many of our four baked-Gemma configurations solved each
problem:

| tier | problem | result | bank contribution |
|---|---|---|---|
| Easy (4/4 configs pass) | torch boolean mask | **PASS** | none needed |
| Medium (bank-rescued) | networkx naive greedy modularity | **PASS** | applied "returns a list, not a generator" |
| Hard (1/4 configs pass) | torch STFT | **PASS** | applied "must pass `return_complex`" (reasoning cited it) |
| Impossible (0/4 pass) | torch 1.9.0 `log_ndtr` | **FAIL** | not bankable |

**3/4 on a 4-billion-parameter model** — including the hard `torch.stft` landmine that only one of our four
much-larger Gemma configurations solved, via the retrieved fact. The one failure is instructive: `log_ndtr`
requires a *numerically stable* log-CDF because `torch.special.log_ndtr` does not exist in torch 1.9.0, so
the naive `log(Normal.cdf(x))` underflows on large negatives. That is an algorithm/numerics problem, not a
documentable API change — **outside what any fact bank can supply.** It fails for the right reason.

---

## 10. Discussion and limitations

**What the bank is and isn't.** FactBank corrects *version-API knowledge* — renames, removals, default
flips, silent behavior changes that a changelog documents. It does not and cannot supply reasoning,
algorithms, or numerical methods (§9's impossible case). Its ceiling on GitChameleon is bounded by the ~12
un-mineable problems (no changelog) and the "absence" problems no document describes.

**Windows buildability + harness fidelity.** 79/328 problems did not build on our **local, non-Docker**
harness; our clean numbers are on the 249 that do. The cause is **not isolated**: the runner discarded
build errors, and 53 of the 79 are Python-3.7 problems forced into 3.9 by the harness's 3.7/3.8→3.9 remap
(where 3.7-era pins often lack 3.9 wheels), so this is confounded with the harness rather than proven to be
missing Windows wheels. The harness also omits dependencies from its venv cache key, so it only approximates
the official pinned (Docker, real 3.7/3.9/3.10) environment. The true all-328 score lies between our
pessimistic 33.5% and the buildable 44.2%; a faithful Linux/Docker re-run is needed before these numbers
are treated as final.

**Single-sample, focused probes.** The thinking-native results (§9) are a controlled probe (one landmine,
repeated) plus a four-problem ladder — a strong existence proof of the mechanism and its cure. The
**complete 328-problem pass@1 for the authority-framed 4B thinking model is done**: on the same local
harness it scores **31.3% (78/249 buildable; 23.8% over all 328), with zero empty answers and zero
truncations** — a 4B model reaching roughly Llama-3.1-70B territory. This is the bank+authority absolute
score, not a base-vs-bank delta (a base Qwen-4B run for the lift is still outstanding).

**Over-deference — the open risk.** Every authority-framing probe used a fact that genuinely applied.
Strong "the fact is absolute" wording could make a model *force in* a near-miss fact that does not apply.
Probing a mix of applicable and inapplicable facts under authority framing is the most important next
experiment before trusting the technique broadly.

**Non-determinism.** Thinking with temperature > 0 is non-deterministic; single-sample thinking numbers
should be read as noisy, and the thinking-off numbers as the clean, deterministic baseline.

---

## 11. Conclusion

A stock, untrained language model can be made version-correct about libraries released after its cutoff by
carrying a small bank of curated landmine facts, delivered either through a retrieval loop or baked into
its own GGUF chat-template. On GitChameleon 2.0 this lifts execution pass@1 by +6.4 (12B) and +2.8 (26B)
with no weight changes, moving a small local model into the neighborhood of models several times larger.

The sharper lesson is about *reasoning*. Chain-of-thought, usually a free win, is actively harmful for
applying habit-reversing facts: it re-weights the decision toward the model's trained prior and argues the
injected fact away, converging on the answer of a model with no bank at all. The remedy is not more
thinking but a different *stance*: frame the fact as authoritative and instruct the model to trust it over
its training. That single change holds fact-adherence on a thinking-native model at 18/18 across framed
authority trials (against an illustrative, unretained 0/6 unframed control) and
lets a 4B model solve an easy-through-hard ladder. In short: **the bank supplies knowledge, the model
supplies reasoning, and the two must be told which one wins when they disagree.**

---

### Reproducibility

Bank, extractor, retrieval prototype (`lookup.py`), baking code (`bake_index.py`), the standard serving
launcher (`serve_factbank.ps1`), execution scorer (`run_tests.py`), and the thinking/authority harnesses
(`test_baked.py`, `probe_qwen_authority.py`, `test_qwen_bank.py`) are in the project tree under
`v2/`. Detailed run logs and per-problem verdicts are in `v2/eval/gitchameleon/BAKE-REPORT.md` and
`v2/eval/gitchameleon/QWEN-THINKING-AUTHORITY.md`.

### References (to be completed)

- Islah et al. *GitChameleon 2.0: Evaluating AI Code Generation Against Python Library Version
  Incompatibilities.* arXiv:2507.12367, 2025.
- Gao et al. *Precise Zero-Shot Dense Retrieval without Relevance Labels (HyDE).*
- [knowledge-editing, RAG, and chain-of-thought references to be added]
