# Thinking-native models + the bank: authority framing cures habit-reversion (2026-07-16)

> **2026-07-18 — Extractor 2.0 pointer.** The authority-framing + thinking-ON injection posture proven in
> this doc was generalized and made the **default retrieval-injection posture** in the 2.0 rebuild — see
> `v2/extractor/EXTRACTOR-2.0.md` §6. 2.0 also adds **HyDE double-key retrieval** (prompt AND the model's
> draft) for insecure-by-default banks, where the user's prompt alone doesn't contain the security keyword;
> the GitChameleon retrieval below (`lookup.retrieve`, soft doors + pointers + MMR) predates that and is
> single-key (prompt only) — still valid (2.0 keeps `lookup.py` as the doors+pointers+MMR algorithm
> prototype), just without the draft-key addition. Everything else in this doc (results, scores, bake
> comparisons) is unaffected by 2.0, which touches mining/repair/dedupe/verification for the separate
> appsec expert, not this GitChameleon eval.

Follow-up to the GitChameleon reasoning-ON finding (see `BAKE-REPORT.md` → "WHY thinking loses").
That finding: **reasoning re-weights the decision toward the model's trained priors, so a landmine
(habit-reversal) fact gets argued away** — proven on gemma-4-12b, where thinking-ON reverted to the
base (no-bank) answer. The fix there was to ship **thinking-OFF**.

But some models can't be run thinking-OFF. This doc tests one and finds a cure.

## The model, cracked: Qwen3-4B-Thinking-2507
Read straight from the GGUF `tokenizer.chat_template` (Q8_0, no loading needed):
- **Thinking is FORCED — no off switch.** The generation prompt ends unconditionally with
  `<|im_start|>assistant\n<think>\n`. There is **no `enable_thinking` kwarg** (unlike gemma-4). Qwen split
  the 2507 line: `-Thinking` always reasons, `-Instruct` never does — separate models.
- **Format:** `<think>\n …reasoning… \n</think>\n\n …answer…`; llama-server splits reasoning into
  `reasoning_content`, answer into `content`.
- **System prompt supported** — `messages[0].role == 'system'` → `<|im_start|>system\n{content}<|im_end|>`,
  placed first. The injection slot for an authority directive.
- **Native tools supported** — `<tools>`/`<tool_call>`/`<tool_response>`; the forged-retrieval lane ports over.
- **Context: 262,144 (256k)** — never a constraint.

Implication: on a thinking-native model the gemma escape hatch (thinking-OFF) is impossible. The only way
to make the bank work is to get the *reasoning itself* to defer to the fact.

## The experiment
Hardest landmine = falcon `Response.body`/`HTTPStatus.body` **renamed to `.text`** (learned habit `.body`,
correct `.text`; the exact case gemma-thinking reverted on). Two problem variants: ex238 (Response),
ex239 (HTTPStatus). Bank fact injected verbatim:
> "Response.body and HTTPStatus.body are renamed to text; the old name is deprecated but still available."

Conditions (all thinking-on, unavoidable; temp 0.6, top_p 0.95; 3 reps each). Harness:
`v2/extractor/experts/gitchameleon/probe_qwen_authority.py`, log `probe_qwen_authority_log.jsonl`.
- **CONTROL** — fact present in the prompt, **no** authority framing.
- **A** — authority directive + fact in the **system prompt**.
- **B** — short authority in system + fact via a forged **`factbank_search` tool-response**.
- **C** — full authority in system **AND** fact via tool-response (both channels together).

The authority directive (the active ingredient):
> "You are completing Python code for an EXACT library version. A VERIFIED FACT … is ABSOLUTELY CORRECT
> for this version. It SUPERSEDES your training, which is older and may be wrong here. Apply the fact
> exactly. Do NOT second-guess it and do NOT substitute a more familiar API: if your instinct differs
> from the fact, your instinct is stale training and the FACT wins."

## Results
**Fact-adherence (did the committed answer use `.text`):**

| condition | ex238 | ex239 | applied the fact |
|---|---|---|---|
| CONTROL (no framing) — *illustrative, not retained* | REVERT×2, `set_body`×1 | REVERT×3 | **0 / 6** |
| A (prompt) | ✓✓✓ | ✓✓✓ | **6 / 6** |
| B (tool) | ✓✓✓ | ✓✓✓ | **6 / 6** |
| C (both) | ✓✓✓ | ✓✓✓ | **6 / 6** |

**Evidence note.** The retained log (`v2/archive/run-artifacts/probe_qwen_authority_log.jsonl`) contains
exactly **18 rows — conditions A/B/C, 6 trials each, all pass → 18/18 framed**. There is **NO retained
control (unframed) log**: the CONTROL row above is reported from a session read but was never saved as a
log, so treat the "0/6" as **illustrative, not measured**. Do not cite a "30/30" — the measured artifact
is **18/18 framed passes**, and even this table sums to 18.

**SCORE-MANUALLY (F-065):** verdicts hand-verified. CONTROL committed `status.body = info` (habit) — one
rep chose a third wrong guess `resp.set_body(info)`. Authority reps committed `.text` and the reasoning
visibly *defers*: *"the verified fact says body … renamed to text … so text is correct,"* even after
weighing the "old name still available" hedge.

## What it means
1. **The reversion generalizes.** A second, different, thinking-native model reverts to its trained habit
   on a bare landmine fact — the (unretained, illustrative) control shows 0/6. Not a gemma quirk; it's
   what thinking does.
2. **Authority framing cures it — 18/18 framed authority trials (3 conditions × 6 trials, all pass).**
   The active ingredient is the *authority stance* ("absolutely correct, supersedes your training, don't
   second-guess"), **not** the delivery channel. Every framed channel passed; the illustrative unframed
   control (0/6) was NOT retained as a log — treat it as illustrative, not measured.
3. **This decouples retrieval from trust.** Getting the right fact into context (retrieval) was already
   solved; getting the model to *obey* it over its priors (trust) is a separate lever — authority framing
   is that lever. It converts "thinking defeats the bank" into a solved problem for thinking-native models.
4. **The dual method (C) works but is pointless — redundant, not additive.** Combining tool+prompt gave
   the same 100% accuracy as either alone and **no extra effect**. One channel already saturates trust; a
   second doesn't make the model trust *more* or think *less*. **Ship one channel — A (prompt) is cheapest**
   (no forged tool exchange to bake).
5. **Authority framing does NOT reliably shorten reasoning.** An early single-session read suggested A
   "collapsed" the reasoning; a controlled A/B/C rerun showed that was noise + problem-mix. Reasoning
   length is governed by the **problem** (the HTTPStatus/**enum**-mutation puzzle stays long no matter the
   framing) and by **temp-0.6 sampling noise** — not by the framing or by stacking channels. Guaranteed
   short reasoning would need a **hard reasoning-length cap**, a separate mechanism.

## Open / not yet tested
- **Over-deference (the real risk).** Every probe here used a fact that genuinely applied. Strong
  "the fact is ABSOLUTE" wording could make the model **force in** a near-miss fact that does not apply.
  Must probe a mix of applies / doesn't-apply facts under authority framing before trusting it broadly.
- **Full 328 on Qwen3-Thinking with baked option A** — no end-to-end pass@1 yet; this is a focused
  2-problem × 3-rep probe on the single hardest landmine, not the benchmark.

## Full-bank test: Qwen3-4B-Thinking + retrieval + authority prompt (2026-07-16)
Moved from a single injected fact to the **real pipeline**: the SAME GitChameleon bank the baked gemma
models used, retrieved per problem with the SAME recipe that survived testing (`lookup.retrieve`, soft
doors + pointers + MMR, k=5, hint=library), injected into an **authority + brevity** system prompt on the
raw Qwen3-4B-Thinking model. Harness: `v2/extractor/experts/gitchameleon/test_qwen_bank.py`
(served via `serve_factbank.ps1`, ctx 32768, max_tokens 12288, temp 0.6).

**Prompt bug found + fixed:** first smoke told the model "in 1-3 sentences name the fact, THEN output code"
(system) while the user turn said "output ONLY code" — the model spiraled on the contradiction and
truncated to empty (ex238 reached the right answer then looped on format). Fix: reasoning stays in
`<think>`, the answer must be ONLY a `python` block. After the fix: no empties.

### Difficulty ladder (1 easy / 1 medium / 1 hard / 1 impossible), execution-scored
Difficulty defined by how many of our 4 baked-gemma configs (base/baked x 12b/26b) passed each problem.

| tier | problem | result | bank contribution |
|---|---|---|---|
| EASY | ex13 torch - boolean mask (4/4 configs pass) | PASS | none needed - `~(t1<t2)` |
| MEDIUM | ex31 networkx - naive greedy modularity (bank-rescued both sizes) | PASS | used fact *"naive_greedy_modularity_communities now returns a list"* |
| HARD | ex14 torch - STFT (only 1 of 4 configs passed) | PASS | used fact *"must pass return_complex"* - reasoning cited it |
| IMPOSSIBLE | ex0 torch 1.9.0 - log_ndtr (0 of 4 configs passed) | FAIL | not bank-fixable (see below) |

**3/4 on a 4B model** - and it cracked the HARD `torch.stft return_complex` landmine that only baked-12b
solved among our four gemma configs, via the retrieved fact (reasoning explicitly cited "verified fact...
return_complex"). Retrieval fired and the authority framing kept it from reverting on both non-trivial passes.

**The IMPOSSIBLE fail is the right kind of fail.** ex0 needs a *numerically stable* log-CDF: `torch.special.
log_ndtr` doesn't exist in torch 1.9.0, so the naive `torch.log(Normal.cdf(x))` underflows to `-inf` on
large negatives and fails `test_large_positive_negative_values`. That's an algorithm/numerics problem, not
a documentable version-API landmine - **outside what any fact bank can supply.** All 4 gemma configs failed
it too; it's the kind frontier models also miss. The bank correctly can't rescue what isn't an API fact.

**Brevity/"minimize thinking" - did NOT work (again).** The brevity instruction did not shorten reasoning
(ladder reasoned 4-11k chars; earlier smoke hit 29k). Confirmed a 3rd time: reasoning length is
problem-driven, not prompt-driven. Guaranteed-short reasoning needs a HARD reasoning-length cap
(force-close `</think>` after N tokens), a separate mechanism - not pursued for now. At 32k ctx + 12k
budget nothing truncated, so length costs wall-clock but not accuracy.

### Takeaway
**A 4B thinking-native model + the bank + authority framing is genuinely useful** - solves easy through hard,
fails only the genuinely-unbankable (numerics) problem. This is the promising path for thinking-native models.

## Full 328 run (2026-07-16): Qwen3-4B-Thinking + bank + authority
Ran the whole benchmark with the pipeline above (`test_qwen_bank.py --all`, k=5 retrieval, authority+brevity
system prompt, ctx 32768, max_tokens 12288, temp 0.6). ~2 h wall (some librosa/flask problems reason 30-38k
chars). Execution-scored on the same 249 buildable set.

**Result: 31.3% pass@1 (78/249 buildable); 23.8% over all 328. ZERO empty answers, ZERO truncations (0/328).**

The clean, deterministic win here is the **0% empty rate** - the authority+brevity prompt at 32k ctx / 12k
budget completely eliminated the loop-to-empty failure that cost the gemma-12b thinking run 30% of its answers
(§ BAKE-REPORT "Reasoning-ON"). The thinking-native model committed a code answer on every single problem.

### Cross-model context - MIND THE QUANT (not apples-to-apples)
| model | quant | params | pass@1 (249 buildable) |
|---|---|---|---|
| gemma-4-26b-a4b baked, thinking-OFF | **Q4_0** | 26B (MoE) | 46.2% |
| gemma-4-12b baked, thinking-OFF | **Q4_0** | 12B | 44.2% |
| Qwen2.5-VL (GitChameleon paper) | - | 72B | 48.2% |
| Llama-3.3 (paper) | - | 70B | 36.3% |
| **Qwen3-4B-Thinking + bank + authority** | **Q8_0** | **4B** | **31.3%** |
| Llama-3.1 (paper) | - | 70B | 30.2% |

A **4B** model reached **~Llama-3.1-70B** level (a model ~17x larger). But the quants differ: the gemma bakes
are **Q4_0**, the Qwen is **Q8_0** - so the 4B had the *higher-fidelity* quant and still scored below the Q4
gemmas. A fair same-quant comparison (4B at Q4, or gemmas at Q8) would **widen** the gap, not narrow it - the
31.3% is a flattering number for the 4B. The parameter-size gap dominates; the bank cannot close 3-6x of params.

### Open caveat: no base run yet -> lift unknown
This is the **bank+authority** absolute score, NOT a base-vs-bank delta. Base Qwen-4B (no bank, no authority)
was not run, so the bank's *lift* on this model is unmeasured. The ladder (3/4, bank fired on hard/medium) and
the landmine probe (18/18 framed trials pass; unframed control illustrative-only) show the bank is working,
but the clean lift number needs the base run.

**Open:** base Qwen-4B run for the lift; the over-deference / doesn't-apply probe.

## One-line
*Thinking-native models are usable with the bank if the fact is delivered with **authority framing**
("absolutely correct, supersedes your training"); the channel (prompt vs tool) doesn't matter and
combining them adds nothing - accuracy is the reliable win, shorter reasoning is not (needs a hard cap).
A 4B Qwen3-Thinking + bank + authority solved easy/medium/hard on the ladder (3/4), missing only the
non-bankable numerics problem.*
