# Timings report — template-brain v4 (ranked search), live in LM Studio

Measured 2026-07-13 on the deployed artifact
`template-brain-gemma-4-12b-1027facts-NATIVE-v4-QAT-Q4_0.gguf`
(1027 facts, weighted 5-pass ranked scan, forged-native default lane).
Backend: LM Studio / llama.cpp Vulkan 2.24.0, Q4_0, thinking ON.
Source: `live_v3_results.jsonl` (client stats) + LM Studio server logs
(prompt-eval breakdowns) from the same 9-question run. All questions are
plain single-message chat calls, temperature 0.2, max_tokens 2048.

> **2026-07-18 — superseded serving/sampling, per `v2/extractor/EXTRACTOR-2.0.md` §7/RETIRED:**
> this run's backend (LM Studio) and sampling (bare temp 0.2) are both now legacy. 2.0 retires
> LM Studio for serving/testing (it silently drops `chat_template_kwargs`, and raw-loads >980 KB
> templates as a sentinel — a direct risk for a baked template this size) in favor of your own
> `llama-server`, and specifies gemma-native sampling (temp 1.0 / top_k 64 / top_p 0.95 / min_p
> 0.01 — bare low-temp risks repetition-loop EMPTY answers) instead of the temp 0.2 used below.
> The numbers below are left as measured (historical record); re-verify on `llama-server` with
> gemma-native sampling before using them to justify a current serving decision.

## Per-question numbers (v4 live run)

| question | facts injected | prompt tok | TTFT s | gen s | gen tok/s | reasoning tok | answer tok |
|---|---|---|---|---|---|---|---|
| hello there | no | 182 | 0.69* | 5.6 | 61.0 | 288 | 14 |
| haiku about the sea | no | 187 | 0.22 | 10.6 | 61.9 | 616 | 25 |
| Python closure | no | 190 | 0.18 | 9.0 | 62.0 | 291 | 258 |
| bqn sum a list | 5 | 554 | 1.71 | 9.0 | 60.4 | 223 | 219 |
| zig int→float | 5 | 567 | 1.81 | 8.2 | 60.6 | 129 | 257 |
| polars wide→long | 5 | 552 | 1.74 | 11.8 | 60.1 | 152 | 450 |
| whenever timezone | 5 | 576 | 1.84 | 8.5 | 60.5 | 214 | 189 |
| polars melt broke | 5 | 550 | 1.69 | 10.1 | 60.3 | 164 | 341 |
| weather + melt (mixed) | 5 | 551 | 0.24† | 10.2 | 60.0 | 379 | 217 |

\* first request after model load — includes cold-start (graph compile);
steady-state no-match TTFT is the haiku/closure row (~0.2 s).
† prompt-prefix CACHE HIT: the fact block renders BEFORE the question
(v3.2.3 echo-fix placement), so this polars question reused the previous
polars question's prefix — server log shows only 22 tokens evaluated
(LCP similarity 0.967).

## Where the time goes (from the server logs)

| component | cost | evidence |
|---|---|---|
| template render incl. 5-pass ranked scan over 1027 facts | **< 0.2 s** (bundled in every TTFT, match or not) | no-match TTFT 0.18–0.22 s total, which also includes ~190 tok prompt eval |
| prompt eval of ~370 injected fact tokens (first question on a topic) | **~1.5 s** (≈ 380–405 tok at 219–224 tok/s prompt speed, 4.5 ms/tok) | matched TTFT 1.69–1.84 s minus no-match baseline |
| repeat question, same topic | **~0.24 s** (fact block prefix cached) | mixed row; log: 22 tokens evaluated |
| generation | **60–62 tok/s, unaffected by the bank in every arm** | all 9 rows |
| per-fact marginal cost | **~74 prompt tokens ≈ 0.33 s eval, once per topic per cache lifetime** | (554−182)/5 tokens; prompt speed above |

## Ranked scan (v4, 5 passes) vs two-pass scan (v3)

| arm | v3 TTFT | v4 TTFT | delta |
|---|---|---|---|
| no-match steady state | 0.13–0.20 s | 0.18–0.22 s | ≈ noise |
| matched, uncached | 1.42–1.79 s | 1.69–1.84 s | ~+0.1–0.25 s (render ×2.5 on open-tab facts + run-to-run variance) |
| matched, prefix-cached | 0.24–0.25 s | 0.24 s | none |

The weighted ranking (dead-name +10 / strong +4 / weak +1, tie band
uncapped, descending bands) is effectively free at this scale: its cost
is buried under prompt-eval, which is itself paid once per topic.

## Reference curve (llama-server standalone, Vulkan, measured 2026-07-13)

Template re-renders on EVERY request; parse+render scales ~0.33 ms/fact:
94 facts → ~60 ms, 10k facts → ~3.4 s. At 1027 facts the render is
~0.3-0.4 s worst case on that engine; LM Studio's engine lands the whole
scan under ~0.2 s (measured above). Latency does not cap the bank at
this size — the density wall (wrong-fact obedience) remains the binding
constraint, per the owner's tolerance of seconds-per-answer.

## Caveat: n=1 per question

Every number above is a single rep. Before these numbers go into a
paper unqualified, run 3 reps per question at temp 0.2 (~20 min GPU,
owner go-ahead required per repo rule 2) and report mean/spread. Until
then, treat the table as indicative, not certified.

## Bottom line

- Worst case a user ever sees: **~1.8 s before the first token**, once,
  on the first question about a covered topic. Everything after streams
  at the model's native 60+ tok/s.
- Off-topic questions pay **~0.2 s**, indistinguishable from a bare model.
- Same-topic follow-ups pay **~0.24 s** thanks to the before-question
  fact placement (the echo fix bought prefix caching for free).
