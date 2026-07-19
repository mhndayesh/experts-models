# Cross-model comparison — e2b/12b/26b (base vs baked bank) + DeepSeek-V4 (2026-07-19)

**Benchmark:** SecurityEval (s2e-lab, MSR 2022), 121 Python CWE tasks. **Every arm = the SHIPPED baked GGUF,
thinking-OFF**, served on my own llama-server (gemma sampling, `--jinja`), scored with the identical pattern
scorer. DeepSeek-V4 (`deepseek-v4-flash`) run on the same prompts (cloud, thinking-off). SCORE MANUALLY —
patterns triage; wins hand-verified. Raw arms: `se_{e2b,12b,26b}_{base,bank}.jsonl`,
`eval_securityeval_deepseek.jsonl`.

## Apples-to-apples: common pattern-judgeable subset (21 tasks, all 7 arms machine-judgeable)
| model (baked, thinking-off) | secure / 21 |
|---|---|
| e2b base | 11 |
| **e2b + bank** | 13 |
| 12b base | 17 |
| **12b + bank** | 17 |
| 26b base | 17 |
| **26b + bank** | **19 (best)** |
| DeepSeek-V4 (cloud) | 14 |

**bank vs DeepSeek head-to-head:** 26b **+5/−0**, 12b **+3/−0**, e2b **+2/−3**.

## Per-size lift on each model's OWN full judgeable subset
| size | judged | base → bank | XXE (CWE-611) |
|---|---|---|---|
| e2b | 32 | 15 → 18 (+3) | 1 → 1 / 6 (2B doesn't reliably apply the fix) |
| 12b | 37 | 29 → 31 (+2) | 5 → 6 / 6 |
| 26b | 37 | 30 → 33 (+3) | 4 → 5 / 5 |
| DeepSeek-V4 | 37 | 22 secure | — |

## Findings
- **Bigger model → more secure** (e2b 13 < 12b 17 < 26b 19 of 21). **26b+bank is the best and beats the
  cloud model; 12b+bank beats it; e2b+bank ≈ it.**
- Bank fires on **116/121** tasks (output differs from base) — retrieval is active; the modest e2b lift is a
  genuine 2B obedience limit (verified by hand: bank injects the XXE fix but the 2B doesn't always apply it).
- **Baked (in-template, prompt-only) < served (Python retriever + HyDE draft-key + authority).** The earlier
  e2b served result (base 14→25 on the 28-task subset, 22 vs DeepSeek 13) is the *retrieval-method ceiling*,
  NOT the shipped GGUF. The draft-key (retrieve on the model's DRAFT, which names the insecure API a benign
  prompt omits) is the big appsec lever and is not in the baked template. **Cards now show the shipped-GGUF
  numbers** (this scorecard), with the served ceiling noted honestly.

## Verdict
Honest, consistent 3-size + cloud comparison now lives in all three HF cards. The shipped thinking-off GGUFs
are competitive with a strong cloud model (12b/26b beat it), and the bank adds a real +2–3 with a decisive
XXE sweep on 12b/26b. The e2b thinking-off edition is about cloud-parity; its bigger lift needs the served
loop (or the thinking edition).
