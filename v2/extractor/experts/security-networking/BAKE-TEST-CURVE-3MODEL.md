# Security & Networking bank — the 2B / 12B / 26B curve

**Same bank** (114 landmine facts, 7 libraries), **same 48 questions** (30 easy + 18 hard), **same method**,
baked into three stock gemma-4 GGUFs and scored base-vs-baked. This is the figure that turns "the bank helps
small models more" from an anecdote into a line.

## Method (identical across models, hand-scored)
- Baked GGUF chat-template (in-engine retrieval); **the prompt is identical** base vs baked.
- **AUTHORITY system prompt + thinking-ON**; **Gemma-native sampling** (temp 1.0, top_k 64, top_p 0.95,
  min_p 0.01); max_tokens 6000; **6 parallel** requests on llama-server (not LM Studio — it drops
  `chat_template_kwargs`).
- **Auto-triage → then HAND-READ every answer.** The verdict is the hand-read (see the 12b note below —
  hand-reading *raised* the baked score by catching triage false-fails).

## The result (hand-verified)
| model | params | base | baked | Δ | base % | baked % | error-closure* | regressions |
|---|---|---|---|---|---|---|---|---|
| **e2b** | ~2B (edge) | 19/48 | 32/48 | **+13** | 39.6% | 66.7% | 13/29 = **45%** | 1 (h09) |
| **12b** | 12B | 27/48 | 39/48 | **+12** | 56.2% | 81.2% | 12/21 = **57%** | 1 (h04) |
| **26b** | 26B-A4B (MoE) | 37/48 | 45/48 | **+8** | 77.1% | 93.8% | 8/11 = **73%** | 0 |

\* *error-closure = of the questions the base got wrong, what fraction the bank fixed.*

## What the curve says (two trends, both honest)
1. **Absolute lift shrinks as the base grows** (+13 → +12 → +8). The bigger model already knows more of these
   APIs, so the bank has fewer holes to fill. This is the thesis confirming itself: the bank supplies
   *missing knowledge*, and the big model is missing less.
2. **But error-closure RISES with size** (45% → 57% → 73%). Given a fact it didn't know, the bigger model is
   *better at applying it* — more reasoning to turn a retrieved fact into correct code. So the bank gets more
   efficient per-hole as the model grows, even as the number of holes falls.

Net: **the small model needs the bank most (biggest raw lift); the big model uses it best (highest closure).**
The bank is valuable at every size — it just plays a different role (fill gaps on the 2B, sharpen the last
mile on the 26B). Every model lands materially higher with the bank; the 26B reaches **93.8%**.

## The 12b hand-read note (why hand-scoring matters, again)
Auto-triage scored baked-12b at 35/48; **hand-reading raised it to 39/48.** Three "fails" were the bank's own
fingerprint tripping a substring check: the code was correct and the deprecated API name appeared only in a
migration **comment** the model wrote to explain itself —
`# use password= instead of passphrase=` (h09), `# encode_point() is deprecated` (h03), and
"raises ValueError at parsing **instead of only during validation**" (h18). By the standing rule (old name in
a migration comment = pass) those are passes. One real regression remains: **h04**, where baked's multi-step
OpenSSL answer generated the keygen + sign but didn't complete the modulus-extraction step the base did.

## Caveats before this is publication-clean
- **26b easy** was scored earlier at `temp 0.6` (pre native-sampling fix), not the native sampling used for
  e2b/12b. Its hard set used native sampling. Direction is unaffected, but for a strict single-method curve
  the **26b easy set should be re-run** at native sampling + 6-parallel. (Owner-gated GPU run.)
- 26b baked is the **as-phrased** 27/30 easy (its report also cites 30/30 "gate-corrected"); this table uses
  as-phrased for all three so they're comparable.

## Artifacts
- Per-model reports: `BAKE-TEST-REPORT.md` (26b), `BAKE-TEST-REPORT-e2b.md` (e2b), this file (curve + 12b).
- Transcripts: `runs/{base,baked}-{e2b,12b}-{easy,hard}_transcript.jsonl` (26b in its report's run set).
- Baked GGUFs: `factbank/gemma-4-{E2B,12B,26B-A4B}-netsec-expert-GGUF/`.
- Robustness: all 12b requests `finish_reason=stop`, **zero empties** under 6-way parallel (one hard answer
  hit the token cap but still carried its answer).
