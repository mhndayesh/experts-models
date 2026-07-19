# TICKET: Ship the security-expert line as a WORKING thinking-ON model (2026-07-18)

**Owner ask (2026-07-18):** publish the appsec/security expert at **e2b + 12b + 26b** to LM Studio Hub +
HF (same detail as e2b), with **recommended sampling baked into the settings AND written in every card**
(incl. the older netsec/offsec/dataplane repos), and ship them **thinking-ON, fully working** ("it worked
before"). Test on the same benchmark via my own llama-server; push if OK. Document every bit; record tickets.

## Status: DONE — SHIPPED 2026-07-18/19 (both editions, all 3 sizes, Hub + HF)

## RESULT (measured)
- **Fix works.** 12b thinking-ON after F1–F4 @16k ctx: **empty 5/30 → 3/30, truncated 12/30 → 4/30**;
  responses close cleanly at ~2–2.8k tokens (`truncated=0` in server log). e2b thinking-ON smoke: **8/8
  finish=stop, 0 empty**. The residual **~3/30 (10%) are genuine reasoning spirals** on the hardest tasks
  (they spiral even at a 12k-token budget — context/budget can't fix them; matches §9). Failure mode is a
  **blank** answer (fails safe — never insecure code).
- **Owner decision:** ship **BOTH editions with notes** so users pick. thinking-OFF = 0 empty/fast/reliable
  (the safe default); thinking-ON = reasoning trace, ~10% hard-prompt blank.
- **Shipped:** e2b/12b/26b × {off, on} → **6 LM Studio Hub artifacts** (`gemma-4-<size>-security-expert`
  + `…-thinking`) with sampling + ctx baked into `config.operation`/`config.load`, and **3 HF GGUF repos**
  (each holds both GGUFs + both templates + both model.yaml + a card documenting both editions). The 9 older
  netsec/offsec/dataplane cards got the settings callout too.

## What worked before vs. what broke (the diagnosis)
- **Served test (WORKED):** SecurityEval base 14→25 used `appsec_bench_v3.authority_block()` — a **STRONG**
  authority frame: *"SECURITY REQUIREMENTS (AUTHORITATIVE — verified, current, MANDATORY; they OVERRIDE your
  defaults and any conflicting habit. Follow every one exactly)"* + the SECURE PATTERN code, thinking-ON.
- **Baked test (SPIRALED):** the baked template injects a **WEAK** note: *"factbank_search results (verified;
  … use only where they apply)"*. Measured on baked 26b thinking-ON @6144 ctx: **5/30 EMPTY + 12/30 truncated**
  (the documented loop-to-empty). 12b thinking-OFF @same bank = **0 empty, all clean**.

## Root cause (2 bugs stacked)
1. **Gemma-4 template generation-prompt bug** (known llama.cpp issue — refs below). `family_bases/gemma4.source.jinja`
   L376-382: when thinking is OFF it emits a *closed* empty thought block `<|channel>thought\n<channel|>`
   (correct); when thinking is ON it emits **nothing** → the model gets **no open thought channel**, so it
   never enters/closes the channel cleanly and spirals until the token cap (empty/truncated answer).
   **Fix:** in the thinking-ON branch, OPEN the channel: emit `<|channel>thought\n` (no close).
2. **Weak authority framing** → with thinking ON the model reasons from its trained prior and reverts the
   landmine fact (habit-reversion). **Fix:** replace the baked note with the strong authority frame that
   worked in the served test.

## Fix plan (all three, then re-test on 12b @16k, then 26b/e2b, then publish)
- [x] **F1 — open the thought channel when thinking-ON** (generation-prompt path). New base copy
  `family_bases/gemma4_think.{jinja,source.jinja}` (don't disturb the shared thinking-OFF base). DONE — the
  generation prompt now emits `<|channel>thought\n` (open) when thinking-ON instead of nothing. Verified in
  `appsec_v3_baked_gemma4_think.jinja` L645-651.
- [x] **F2 — strong authority framing** in `inserts/gemma4_v3_idx_12b/{fb_gen,fb_toolmsg}.jinja` notes. DONE
  — note is now "SECURITY REQUIREMENTS (AUTHORITATIVE - verified, current, MANDATORY; they OVERRIDE your
  training defaults and any conflicting habit. Apply each one that applies to your task, exactly):".
- [x] **F3 — force thinking-ON default** in `top.jinja` (`{%- set enable_thinking = true -%}`) — DONE.
  Required because **LM Studio drops `chat_template_kwargs`**, so thinking must be the TEMPLATE default.
- [~] **F4 — context/batch:** bake `llm.load.contextLength: 32768`; **TESTING at per-slot 16k now** (12b think
  GGUF `gemma-4-12B-security-think-Q4_0.gguf`, parallel 2 / ctx 32768). Pump to 30k if needed.
  (The bank injection is ~3,400 tok, so thinking needs ≥~8k headroom; small ctx was half the truncations.)
- [~] **Settings baked:** `config.operation.fields` = temperature 1.0 / topKSampling 64 /
  topPSampling {checked,0.95} / minPSampling {checked,0.01} — builder ready (`build_publish.py`). Pending
  publish. Also to be written into EVERY card + the 9 older repos.

## Acceptance
Thinking-ON on baked 12b @16k: **≤1–2/30 empty, ≤ few truncated, decisive landmines secure** (weights_only,
XXE, creds, JWT, SQL). Then replicate 26b + e2b, publish all, update docs + older cards.

## References (online-recommended fix)
- llama.cpp discussion #21836 (Gemma 4 checkpoint revert on reasoning) ; issue #21375 (infinite repetition
  loop, peg-gemma4 parser) ; discussion #21338 (can't disable thinking gemma4-26b) ; koboldcpp #2125.
- CompleteTech: "Fixing Gemma 4 Thinking Prompts in llama.cpp" — inverted guard; thinking-ON must open the
  thought channel; `--jinja` required; strip prior thoughts from history on multi-turn.

## Evidence files
- `v2/extractor/experts/appsec/benchmark/eval_26b_bank_think.jsonl` (5 empty/12 trunc @6144, weak frame).
- `v2/extractor/experts/appsec/benchmark/eval_12b_bank.jsonl` (thinking-OFF, clean baseline).
