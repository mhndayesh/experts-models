# Limits — what is broken, unproven, or unfinished

> **UPDATE 2026-07-17 (gate-alias fix — the gate dies on NATURAL/OLD names too).** Baking two new
> experts (offsec, dataplane) and hand-scoring base-vs-baked on all 3 sizes surfaced a fresh case of
> §5's fatal gate: the exact-token gate also stays shut when a user types a **natural** or **old** name
> that isn't the lib token — "BloodHound" vs `bloodhound-py`, "successor to CrackMapExec" vs `netexec`.
> Proven by rendering the baked template offline (`v2/bake/template-brain-v3.1/render_retrieval.py`):
> `bh01` injected **0 facts across all 3 sizes** → the model answered from stale training and missed at
> every size. **Fix:** `gen_gate_aliases.py` derives per-expert gate aliases from each rename fact's
> **OLD name** + the lib's natural stem (identifier-like tokens `. _ - /` or `()`, plus a curated
> cross-name set like `crackmapexec→netexec`; bare generic words and ambiguous tokens dropped), fed to
> `bake_index.py --extra-aliases`. Verified: after the fix `bh01`/`nx01` open the gate and inject the
> right facts. Same class as the volatility3 "Volatility 3" vs `volatility3` death. **Rule going
> forward: every rename fact's OLD name is exactly what a stale user types — it must be a gate alias.**

> **UPDATE 2026-07-14 (F-060…F-063).** Two entries below are now measured and partly fixed:
>
> - **§1's "recall decays"** now has a *cause*: **66% of unreachable facts die at the GATE**,
>   before ranking ever runs — not at the ranker. Fixed at build time (gate cap 48→150, real
>   `log(N/df)` IDF, and letting the gate see the Doc2Token expansions), plus a **rescue gate**
>   for dead-API names. Bank reachability **76.6% → 84.1%**; 144 dead facts revived.
> - **§2's "gold proves retrieval, not obedience"** is now measured properly (F-065, 76 cases,
>   hand-scored): on the 25 decisive cases **bare 3/25, shipped v6 20/25, rescue v7 21/25**.
>   The bank is worth 12% → 80%. **v7 buys ~zero over the shipped model.** The earlier
>   "8/8 vs 3/8" (F-063) had 8 questions and **no v6 arm** — it never compared v7 to what
>   already ships. And **mined signature facts won ZERO cases**; every win was a curated
>   `mistake` fact.
> - **§8 (new): the mined bank was 66% junk** (F-064) — inherited duplicates that flatten IDF
>   and crowd the top-5. 24,133 → 8,096.
> - **§5's "the gate is binary and fatal"** — confirmed, and it is the single largest failure
>   source. **Deleting it fails** (8/10 controls fire); the narrow rescue gate is the fix.
>
> **303 facts are still unreachable**, and ~61% of those still die at the gate on
> symptom-language questions containing no API name. See `RETRIEVAL-V7.md`.

> **UPDATE 2026-07-16 (v2 / GitChameleon era).** A new expert was built, baked, and
> **execution-benchmarked**, which closes some limits below and adds new ones. Read §9–§11.
>
> - **Parity (§5's "jinja2 ≠ shipped engine") is now CLOSED for the GitChameleon bank.** The
>   4,167-fact / 23-door bank was baked into gemma-4 **12b + 26b** GGUFs and **fires inside
>   llama.cpp** — verified via `llama-server /apply-template`: the retriever triggers and the
>   library-correct fact lands in context. First in-engine (not Python-prototype) proof.
> - **Obedience is now execution-measured, not gold-proxied (§2).** Base→baked pass@1 on
>   GitChameleon hidden tests (249/328 buildable): **12b 37.8%→44.2% (+6.4), 26b 43.4%→46.2%
>   (+2.8)**, thinking-OFF. Hand-verified. See `../eval/gitchameleon/BAKE-REPORT.md`.
> - **The template-size wall is OVERCOME — not a limit.** We ship a **2.73 MB** baked template
>   running in llama.cpp with no size issue, proven on the 12b + 26b GitChameleon bakes. Size does
>   not constrain the shipping path (`llama-server`). LM Studio raw-load has an 980 KB cap (F-053) but
>   it is a route we don't use; the Hub `model.yaml` route has no cap either. Serving:
>   `../bake/serve_factbank.ps1`.
> - **Validated beyond gemma-12b (§6).** Now also gemma-4-26b-a4b and **Qwen3-4B-Thinking-2507**.
> - **NEW, large limit: reasoning fights the bank (§9).** Chain-of-thought REVERTS habit-reversal
>   facts to the trained prior — ship thinking-OFF; for thinking-native models use authority framing.
> - **NEW: the bank cannot supply non-API knowledge (§10)** — algorithms/numerics are out of scope.
> - **~~NEW: e2b GGUF not baked (§11)~~ — CLOSED 2026-07-19:** e2b is baked for the security line, which
>   ships ×3 sizes (e2b/12b/26b) × both thinking editions.

Read this before promising anything. Everything below is measured or explicitly flagged as
unmeasured.

---

## 1. The open problem: recall decays as the bank grows

This is the one that matters.

| facts | gold | controls |
|---:|:---:|:---:|
| 2,314 | **12/12** | 0/10 |
| 4,564 | 11/12 | 0/10 |
| 8,837 | **9/12** | 0/10 |
| 21,203 | **9/12** | 0/10 |

The controls never false-fire, so a big bank is not *noisy* — it is **unfocused**. The
right fact loses its slot to competitors. At 21k, `resample`'s frequency-alias fact
retrieves **nothing at all** (its gate never opens), and `np.NaN` pulls five facts, none of
them the right one.

**Cause: constants calibrated at 2,000 facts, applied to 21,000.** `DF_CAP=40`, the IDF
buckets (≤3 postings ×3, ≤10 ×2), 48 gate triggers per library, and `FB_MAX=5` answer
slots. None scale with bank size — and the slots got contested 10× harder while latency got
*cheaper*.

**Consequence: "more facts" is not an upgrade.** A 20k bank that retrieves worse than a 2k
bank is a regression, however much knowledge is nominally inside it. Growing the bank is a
**retrieval-calibration** job, and every lever is offline, free, and measurable.

**And the metric must grow first.** The gold set is **12 questions**. It cannot honestly
calibrate a 21k bank. Expanding it is a prerequisite, not a nicety.

## 2. The gold set proves retrieval, not obedience

Gold measures *did the right fact reach the model*. It does **not** measure *did the model
then write correct code*. Those are different, and the gap between them is where this
project has historically hidden its failures.

The end-to-end scored evaluation needs a rebuilt case set: the last probe showed the bare
model **already knew 11 of 15** old cases (replacements like `applymap`→`map` predate its
cutoff), so those cases could not measure the bank at all. **Probe before you run** — a
case only proves something if the model *cannot already* answer it.

## 3. Coverage gaps inside the bank

- **Doc2Token expansions cover only the 388 curated facts.** The 1,523 mined facts are
  reachable only by their literal API tokens. Ask for one in everyday words and nothing
  bridges the gap.
- **Mined facts are shallow.** A signature tells the model the function exists and what
  arguments it takes — nothing about behaviour.
- **Expansion quality depends on the model's imagination.** It writes the questions it
  happens to think of; vocabulary it didn't predict still misses.
- **English-only, unstemmed, no typo tolerance.** `reshaping` ≠ `reshape` unless one of
  them happens to be indexed.
- **Terms in more than 40 facts are dropped silently** (`DF_CAP`). A genuinely important
  term that crosses that line simply vanishes from the index.

## 4. Retrieval is keyword matching, not meaning

Everything in the architecture is engineering *around* that fact. There is no embedding
model and there cannot be one — the substrate does string operations and integer maths, and
nothing else. A question phrased in vocabulary that neither the fact nor its expansions
contain will miss, **silently**.

There is also **no failure signal**. The template cannot know it missed. A miss looks
exactly like a stock model answering from stale weights — which is precisely the failure
the whole project exists to prevent.

## 5. Known-fragile mechanics

- **`llm.load.promptTemplate` is EXPERIMENTAL** in the LM Studio SDK. The Hub route depends
  on it. It works today and can change between versions — keep `check_override.py` as a
  permanent regression gate.
- **THE RULE (bake-size decision).** The only place a template size ever matters is **LM Studio
  raw-loading a `.gguf` by hand**. Everywhere else it is irrelevant.

  | baked chat-template size | LM Studio raw-load | every other route (llama.cpp / `llama-server` / `model.yaml`) |
  |---|---|---|
  | **≤ ~980,000 B** (~957 KiB) | bakes into GGUF metadata and loads **normally** — no workaround | loads normally |
  | **> ~980,000 B** | **use the `model.yaml` workaround** (below) — raw-load would silently truncate to a 48-char sentinel and answer garbage | **irrelevant** — no cap (llama.cpp caps at 1 GiB and errors loudly, never silently) |

  Reference points: the **Security & Networking** template is **115 KiB** → under the limit, bakes/loads
  normally everywhere, no workaround. The **GitChameleon** template is **2.73 MB** → over the limit, so it
  uses the `model.yaml` route *for LM Studio only*; on `llama-server` (our shipping path) it just works.
  So: **within the limit → bake normally; above the limit → workaround, and only for LM Studio.**

- **The size wall is OVERCOME (not a limit).** We ship a **2.73 MB** template in llama.cpp with no
  issue (12b + 26b GitChameleon bakes). The only route that ever capped size is LM Studio raw-load
  (undocumented, silent, ~980,000 bytes) — llama.cpp caps at 1 GiB and errors loudly. Keep the byte
  figure on record only so nobody re-treats it as a general constraint: it is specific to one path,
  and even THAT path is bypassed by the `model.yaml` route (below).

  **How the `model.yaml` route bypasses the cap (for LM Studio specifically), proven at 1.5 MB and 2.0
  MB, F-059):** the 980 KB cap only bites the template stored *in GGUF metadata* — the field LM Studio's
  raw loader reads and silently truncates to a 48-char sentinel. The `model.yaml` route does not use that
  field. Instead:
  1. The GGUF keeps a small, SAFE embedded template (so a hand raw-load never bricks).
  2. The full oversized template ships as a **separate `.jinja` file referenced by `model.yaml` via
     LM Studio's `llm.load.promptTemplate`** field.
  3. At load time LM Studio spawns its own `llama-server` and hands it that file with
     **`--chat-template-file <path>`** — i.e. the big template reaches the engine as a load-time file,
     never through the capped metadata field. No size limit applies.
  Verify the handoff with `bake/template-brain-v3.1/lmstudio_yaml_test/check_override.py`: it finds the
  spawned `llama-server`, extracts its `--chat-template-file` path, hashes it, and asserts it EQUALS the
  oversized template, is > 1 MiB, is NOT the sentinel, and carries the size canary — while the GGUF
  metadata cache still shows the safe embedded template. **Caveat:** `llm.load.promptTemplate` is
  EXPERIMENTAL in the LM Studio SDK; keep `check_override.py` as a permanent regression gate.
- **llama.cpp probes the chat template at load time** with synthetic inputs (multimodal
  content, empty message arrays, tool defs). If the template throws on any of them,
  **the whole model is rejected**. Every code path must be guarded.
- **jinja2 ≠ the shipped engine.** Every offline gate renders with jinja2; production runs
  llama.cpp's Jinja. They differ (whitespace handling in `.split()`, operator precedence),
  and the difference once silently changed *which facts were retrieved* — 5 under jinja2, 1
  in production. `parity.py` exists for this and is mandatory.
- **`FB_MAX = 5` is a hard cap with no confidence threshold.** If a tab opens and anything
  scores, up to five facts inject — even when the best score is weak.
- **The gate is binary and fatal.** If no library tab opens, the index is never consulted,
  no matter how strong the match would have been.

## 6. Known-unmeasured

- **Terse facts.** Rewriting facts in shorthand (~3× smaller) would fit ~3× more per
  template — *if* the model still obeys the shorthand. Unmeasured. Must be measured, not
  assumed.
- **Render cost above 5 MB.** The curve is flat to 5.06 MB; beyond that, unknown.
- **The ranker still uses workarounds for constraints that do not exist.** It ranks with
  five max-selection passes and totals scores by re-walking a string (O(h²)) — both were
  written believing the engine lacked `sort` and `append`. It has both. The rewrite is the
  cheapest speed-up available and has not been done.
- **Only validated on gemma-4-12b** at this scale.
- **The 933 niche-language facts** in the sibling model were authored from model knowledge,
  not extracted and gate-verified against live docs. Demonstration-grade until spot-checked.

## 7. Things that look like limits but are not

- **Template size.** Not a constraint on llama.cpp (a 5 MB template renders a matched
  question in 218 ms — *faster* than the 950 KB one). Only LM Studio's metadata path caps
  it, and the Hub route bypasses that.
- **Render latency.** Cost per fact *falls* as the bank grows.
- **Index compression.** Measured and available (−235 KB), but no longer needed for
  capacity — it is now a speed/fit tool. And the obvious win in it (dedup) is a **loss**.

---

## 8. The mined bank was never inspected (2026-07-14)

**Fixed, but read this before trusting any mined bank.** F-064: 66% of the 24,133 mined
signature facts were junk — inherited duplicates, `str.join` filed as a matplotlib fact,
duckdb's entire bank being Python exception boilerplate. It had been in the pipeline
unexamined since it was mined.

**What is still open:**

- **The causal claim is untested.** "The junk broke recall (12/12 → 9/12 at 21k)" has a
  mechanism (duplicate terms flatten IDF and crowd the top-5) and a correlation. It has
  **not** been measured. The test is free and offline: bake the 8,096 clean facts with v7
  retrieval, re-run gold + controls + reachability. Until that runs, treat it as a hypothesis.
- **144 sklearn `set_fit_request` / `set_score_request` facts** survive the gate correctly
  (distinct signatures per estimator) and are the lowest-value facts in the bank. Cutting
  them is a value judgement, not a correctness one. Owner call, not made.
- **11,700 inherited-duplicate groups** had their representative chosen automatically. The
  choice was spot-checked, not exhaustively verified. Recoverable from
  `facts_mined_clean.rejects.jsonl`.
- **Signature facts have never won a case.** Every case the bank carried in the dense eval
  was a curated `mistake` fact. Do not assume a bigger, cleaner signature bank improves
  obedience — there is no evidence for it either way.
- **Only the `data` domain was gated.** `api_facts/` also holds `ai__*` and `std__*` mines
  (langchain, anthropic, openai, pydantic_ai, asyncio, argparse …) which have **not** been
  inspected and should be assumed to carry the same defects.

**The transferable lesson.** A dedupe gate is a scorer, and every scorer in this repo has
been wrong at least once (F-007, F-016, F-020, F-021, F-026, F-029, and now F-064). Four bugs
in this one, all caught by hand-reading the reject file, none by a test. Two of them —
deleting `pyarrow.Table.join_asof` for having a lazy docstring, and keeping
`CategoricalIndex.to_series` over `Index.to_series` — would have destroyed thousands of real
facts while printing a clean-looking summary. **Every cull writes its rejects. Read them.**

---

## 9. Reasoning fights the bank (2026-07-16) — the biggest runtime limit

**Chain-of-thought makes the bank WORSE, and it is mechanistic, not incidental.** Measured on the
baked 12b, same 249 buildable: **thinking-OFF 44.2% → thinking-ON 36.9% (−7.3).** Two failure modes:

- **Habit-reversion.** A landmine fact is by definition a *habit reversal* (the correct post-cutoff
  answer contradicts training). With thinking off, the template injects the fact and the model commits
  it before its weights get a vote. With thinking on, the model reasons *from its parameters* and the
  learned habit reasserts itself. **Proven by convergence:** baked+think-ON produces the *exact* answer
  of the base model with NO bank (falcon `.body` not `.text`; pandas `observed=False` not `True`). The
  fact is in context (verified) but the bank becomes a no-op.
- **Loop-to-empty.** ~**30%** of thinking-ON answers came back empty — the model spirals restating its
  reasoning, never closes the thought channel, hits the token cap (`finish_reason=length`). Worst on
  heavy-reasoning libs (scipy, librosa, sympy). Raising the budget doesn't fix it (reasoning spirals
  longer). Pass rate is monotone in reasoning length: <4k chars → 73%, >16k chars → 14% (56% empty).
- **Where it commits, reasoning adds no accuracy** — 49.2% vs 50.3% on non-empty problems. Knowledge is
  in the injected fact, not the weights; deliberation only adds variance + the reversion.

**Mitigation, and its own limits:**
- **Ship thinking-OFF** where the model allows it (gemma via `enable_thinking:false`). This is the fix.
- **Thinking-native models** (e.g. Qwen3-4B-Thinking, no off switch) need **authority framing** — mark
  the fact "ABSOLUTELY CORRECT for this version, SUPERSEDES your training, do not second-guess." This
  restored fact-adherence **0/6 → 30/30** on the hardest landmine, channel-agnostic (system prompt or
  tool-response; combining is redundant). See `../eval/gitchameleon/QWEN-THINKING-AUTHORITY.md`.
- **UNMEASURED — over-deference (the open risk).** Every authority probe used a fact that *applied*.
  Strong "the fact is absolute" wording may make the model **force in** a near-miss fact that does NOT
  apply. Must be probed (mix of applies/doesn't-apply) before trusting authority framing broadly.
- **UNMEASURED — full 328 for a thinking model.** Only a single-landmine probe + a 4-problem ladder
  (3/4) run so far; no full pass@1 for the authority-framed thinking path.
- **Authority framing does NOT shorten reasoning** — length is problem-driven, not prompt-driven
  (confirmed 3×). Bounding it needs a hard `</think>` cap, not a prompt. Not built.

## 10. The bank's scope ceiling — it corrects API knowledge, nothing else

**A fact bank can only carry what a changelog documents.** It corrects renames, removals, default flips,
and silent behaviour changes. It **cannot** supply:
- **Algorithms / numerics.** GitChameleon ex0 (`torch 1.9.0 log_ndtr`) fails under every config including
  the bank: `torch.special.log_ndtr` doesn't exist in 1.9.0, so a *numerically stable* manual log-CDF is
  required; the naive `log(Normal.cdf(x))` underflows. That's an implementation problem, not a fact — out
  of scope. Correctly unfixable, but a real ceiling.
- **Un-mineable libraries.** 3 of GitChameleon's 26 (`kymatio`, `lightgbm`, `tqdm`) have no prose
  changelog → no facts → ~12 problems the bank can never touch. Plus "absence" problems no doc describes.

## 11. Bake / delivery gaps (v2)

- **Retrieval precision, not just recall (extends §1/§4).** Even when the right library's facts are
  retrieved, the *decisive* fact isn't always ranked #1 among the k=5 (e.g. pandas groupby-`observed`
  landed a `value_counts` variant instead). Library-door targeting is solid; intra-library ranking is the
  soft spot. Same keyword-not-meaning root cause as §4.
- **~~e2b GGUF unbaked.~~ CLOSED 2026-07-19.** gemma-4-e2b's chat-template differs from the 12b/26b source
  (16,317 vs 18,244 chars, different sha) — an earlier tool-macro variant. It was re-anchored into its *own*
  template and is now **baked for the security line** (ships ×3 sizes × both thinking editions).
- **Bank now ships via the model.yaml route (raw-GGUF size cap dead).** The 4.18 MB appsec **v3** bank is
  delivered via LM Studio's `llm.load.promptTemplate` in `model.yaml` (not stuffed into the raw GGUF
  template), with the **library gate removed** — so the F-053 raw-template size wall no longer caps it.
- **Windows buildability caps the eval, not the bank.** 79/328 problems don't build on Windows (old libs,
  no wheels) → clean numbers are on 249; true all-328 is between 33.5% and 44.2%. A Linux/Docker harness
  closes this. Not a bank limit — a measurement limit.
- **Execution scoring is single-sample.** pass@1, greedy/low-temp; thinking runs (temp>0) are
  non-deterministic and should be read as noisy vs the deterministic thinking-off baseline.
