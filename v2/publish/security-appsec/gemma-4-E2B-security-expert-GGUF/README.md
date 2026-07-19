---
license: gemma
base_model: lmstudio-community/gemma-4-E2B-it-GGUF
pipeline_tag: text-generation
library_name: llama.cpp
language:
  - en
tags:
  - gguf
  - llama.cpp
  - gemma
  - factbank
  - security
  - secure-coding
  - appsec
  - cwe
  - reasoning
---

# gemma-4-E2B-security-expert (GGUF)

**A ~2B (E2B) model that writes *secure code by default* — an application-security *FactBank* is baked into
its chat-template and fires **inside the inference engine** to steer the model off insecure-by-default
patterns.** Weights untouched; no external RAG. This repo ships **two editions** (see below).

> 🔗 **Full project:** [github.com/mhndayesh/experts-models](https://github.com/mhndayesh/experts-models)

## Two editions — pick one (files in this repo)
| edition | file | when to use | notes |
|---|---|---|---|
| **thinking-OFF** (default) | `gemma-4-E2B-security-expert-Q4_K_M.gguf` | production, speed, reliability | 0 empty answers, fast, secure. No reasoning trace. **The safe default.** |
| **thinking-ON** | `gemma-4-E2B-security-expert-thinking-Q4_K_M.gguf` | you want a visible reasoning trace | Shows its work and is strong on most tasks, **but ~10% of the hardest-reasoning prompts can run long and return a *blank* answer** (fails safe — it does not emit insecure code; just retry). Needs a large context + generous output budget. |

Both editions carry the **same** bank. They differ only in whether chain-of-thought is on. We ship both so
you know exactly what you're getting — a landmine fact *reverses a trained habit*, and with thinking on the
model sometimes over-reasons back toward its prior, so the thinking edition trades some reliability for a
reasoning trace. Thinking-ON has a **known llama.cpp Gemma-4 fix applied** (the generation prompt opens the
thought channel) + **strong authority framing** so facts hold; the residual ~10% is inherent to reasoning-on.

## Settings that work (baked into the Hub editions; set these yourself on llama.cpp)
- **Sampling (gemma-native):** `temperature 1.0, top_k 64, top_p 0.95, min_p 0.01`. The **`min_p 0.01`** floor
  is important — it stops the low-temperature repetition loop that otherwise yields empty answers.
- **Context length:** **≥ 16k, 32k recommended** (`contextLength 32768` is baked). The bank injects ~3,400
  tokens per query, so a small context truncates the answer — especially with thinking on.
- **Output budget (thinking-ON):** allow **generous `max_tokens`** (reasoning traces run ~2–3k tokens); too
  small a cap truncates before the answer.

## What it does
Given a normal coding request it silently corrects insecure defaults, e.g. `torch.load(weights_only=True)`
(post-cutoff), XXE `resolve_entities=False`, `yaml.safe_load`, `secrets` over `random`, `os.environ` creds,
parameterized SQL, `ast.literal_eval` over `eval`, constant-time HMAC compare. You **don't name the
vulnerability** — the bank is indexed by the coding task, so it fires on benign prompts.

## Coverage — what's in the bank
- **258 concepts (254 CWE + 4 door groups) → 3,984 language/framework variants** (organized by weakness, not a short lib list).
- **10+ languages:** Python, Java, JavaScript, C/C++, Swift, Go, C#, Rust, Ruby, and more.
- **Frameworks:** Android, iOS/SwiftUI/WKWebView, Flask, Django, Express, Node.js, ASP.NET/.NET, Spring,
  Java EE, Rails, Laravel.
- **7 mined sources:** MITRE **CWE**, GitHub **CodeQL**, SAST (**Bandit**+**gosec**), OWASP **MASTG**,
  **RustSec**, **NIST/RFC/Mozilla** crypto-net, **OWASP** — each fact quote-grounded then adversarially
  correctness-audited (~3.8% wrong/stale removed).

## How the three sizes compare — and vs a cloud model (hand-scored)
**External SecurityEval** (s2e-lab, MSR 2022, 121 Python CWE tasks). Every arm below is the **shipped baked
GGUF, thinking-OFF**, served on my own llama-server with identical scoring; **DeepSeek-V4**
(`deepseek-v4-flash`) run on the same prompts **in no-thinking mode (thinking disabled)** — to match the
thinking-off editions here (its reasoning mode could score higher; this is an apples-to-apples, thinking-off
comparison). Table is the **common pattern-checkable subset (21 tasks)** where every arm is machine-judgeable.

| model (baked, thinking-off) | secure / 21 |
|---|---|
| e2b base | 11 |
| **e2b + bank** | 13 |
| 12b base | 17 |
| **12b + bank** | 17 |
| 26b base | 17 |
| **26b + bank** | **19 — best** |
| **DeepSeek-V4** (cloud) | 14 |

**Reading it:** bigger model → more secure. The bank lifts each model and helps most where the base is weak
+ on specific weaknesses — **XXE (CWE-611): 12b 5→6/6, 26b 4→5/5**, plus deserialization, weak-random,
hardcoded-creds. **12b+bank and 26b+bank beat the cloud model; e2b+bank is about even with it.** On each
model's *own* full judgeable set the bank adds **+2–3** (e2b 15→18, 12b 29→31, 26b 30→33).

> **Honest note:** these are the *in-template (prompt-only)* baked editions. The FactBank *retrieval method*
> reaches higher when run as a served loop with a HyDE draft-key + authority framing (e2b 14→25 on the
> 28-task subset) — that draft-key is the big lever for benign security prompts and is not in the baked
> template. The numbers above are what the **shipped GGUFs** actually do.

## How to run

### LM Studio (Hub editions — the full bank is delivered via model.yaml)
The bank template is 4.2 MB — over LM Studio's ~980 KB raw-GGUF cap, so for LM Studio use the **Hub virtual
models** (they hand the full template to the engine, no cap), which also carry the settings above:
- **thinking-OFF:** https://lmstudio.ai/mhndayesh/gemma-4-e2b-security-expert
- **thinking-ON:** https://lmstudio.ai/mhndayesh/gemma-4-e2b-security-expert-thinking

### llama.cpp / any OpenAI-compatible server (this GGUF, full bank embedded)
```bash
# thinking-OFF (recommended)
llama-server -m gemma-4-E2B-security-expert-Q4_K_M.gguf --jinja --ctx-size 32768 --port 8080
# thinking-ON
llama-server -m gemma-4-E2B-security-expert-thinking-Q4_K_M.gguf --jinja --ctx-size 32768 --port 8080
```
Sampling: `temperature 1.0, top_k 64, top_p 0.95, min_p 0.01`. Don't quantize the KV cache on small models.
Exposes an OpenAI-compatible API at `/v1`.

## Limitations
- **Scoped to secure coding.** Outside it, base model.
- **Supplies knowledge, not reasoning** — still misses some multi-step fixes.
- **thinking-ON:** ~10% of hard prompts run long / blank (fails safe). Use thinking-OFF for reliability.
- **Keyword + faceted retrieval, not embeddings** — an unusual phrasing can miss. Research-grade; review output.

## Provenance & license
- **Base:** `lmstudio-community/gemma-4-E2B-it-GGUF` (weights untouched). Only `tokenizer.chat_template` is rewritten to embed an
  inverted-index retriever + the bank (`factbank.version 0.4.0`).
- **License:** Google **Gemma Terms of Use** (`license: gemma`). Fact bank = FactBank-project content; mined
  sources keep their own licenses.
- **Source & method:** [github.com/mhndayesh/experts-models](https://github.com/mhndayesh/experts-models).
