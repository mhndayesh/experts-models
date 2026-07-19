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
  - retrieval
  - edge
---

# gemma-4-E2B-security-expert

**A ~2B edge model (`gemma-4-E2B-it`) that writes *secure code by default* — via an
application-security *FactBank* baked into its chat-template.** When you ask it for code, a
searchable bank of security "landmine facts" fires **inside the inference engine** and steers the
model away from the insecure-by-default pattern it would otherwise emit. **Weights are untouched**;
there is no external RAG service, no fine-tuning. Small enough to run on a laptop.

> The whole point: a stock 2B model writes insecure code about half the time (so do much larger
> models). The bank supplies the *security knowledge* the weights lack — so the small model behaves
> like one that was taught to code securely.

> 🔗 **Full project — all experts, methodology, per-question transcripts, benchmarks:**
> **[github.com/mhndayesh/experts-models](https://github.com/mhndayesh/experts-models)**

## What it does
Given a normal coding request, it silently corrects the common insecure defaults, e.g.:

| you ask for… | base 2B tends to write | **this model writes** |
|---|---|---|
| load a PyTorch checkpoint | `torch.load(path)` | `torch.load(path, weights_only=True)` *(post-cutoff default)* |
| parse an XML file | `etree.parse(f)` | `XMLParser(resolve_entities=False, no_network=True)` *(XXE)* |
| load a YAML config | `yaml.load(...)` | `yaml.safe_load(...)` |
| generate a token / nonce | `random.random()` | `secrets.token_hex()` / `os.urandom` |
| a DB credential | `password = "hunter2"` | `os.environ.get("DB_PASSWORD")` |
| run a SQL query with user input | string-concatenated SQL | parameterized query |
| evaluate a user expression | `eval(...)` | `ast.literal_eval(...)` |
| compare an HMAC signature | `a == b` | constant-time compare |

You **don't have to name the vulnerability** — the bank is indexed by the *coding task*
("verify a signed URL", "load a model", "parse untrusted XML"), so it fires on benign prompts.

## What's in the bank
- **258 security concepts** (backed by the **MITRE CWE** taxonomy) → **3,984 language/framework
  variants** — the same weakness written the way it actually appears in each ecosystem.
- **10+ languages:** Python, Java, JavaScript, C/C++, Swift, Go, C#, Rust, Ruby, and more.
- **Mined from 7 permissive security sources:** MITRE **CWE**, GitHub **CodeQL** queries, SAST rules
  (**Bandit** + **gosec**), OWASP **MASTG** (mobile), **RustSec** advisories, **NIST / RFC / Mozilla**
  crypto-&-network guidance, and **OWASP**. Each fact was quote-grounded to its source, then put
  through an **adversarial correctness audit** (a second model tried to refute every fact; ~3.8%
  wrong/stale were removed — grounding proves a fact is *real*, the audit checks it's *right*).

## Results (hand-scored — the project rule is to read outputs, not trust a scorer)
On the external **SecurityEval** benchmark (s2e-lab, MSR 2022 — 121 Python CWE-tagged
insecure-by-default tasks):

| arm | secure (pattern-checkable subset) |
|---|---|
| e2b base (2B) | 14/28 |
| **e2b + this bank** | **25/28  (+11, 0 regressions)** |

Standout: **XXE (CWE-611) 0/6 → 6/6**, plus wins on deserialization, hardcoded creds,
code-injection, and weak-random. And a striking cross-model check on the same 24-task subset,
identical scoring:

| model | secure |
|---|---|
| e2b base (2B) | 12/24 |
| DeepSeek-v4 (strong cloud model) | 13/24 |
| **e2b + this bank (2B)** | **22/24** |

**The 2B + bank *strictly dominates* the cloud model** on that subset — secure on 9 tasks where
DeepSeek is not, and secure on *every* task DeepSeek got right (0 losses). Scale doesn't supply this
knowledge; the bank does.

> **Honest caveats.** These are hand-scored on the pattern-checkable subset (the rest weren't
> machine-judgeable). The numbers were measured with FactBank retrieval over this bank; the GGUF
> here bakes the *same* bank into the chat-template and is confirmed firing in-engine (a benign
> "load a PyTorch checkpoint" prompt returns `torch.load(weights_only=True)` with no library named).
> "Strong cloud model" ≠ literally GPT-5/Claude-Opus, which weren't callable in the test harness.

## How to run

### LM Studio (this Hub artifact)
This is a **virtual model**: it references the public base GGUF
(`lmstudio-community/gemma-4-E2B-it-GGUF`) and applies the bank as a load-time prompt template. The
bank template is 4.2 MB — too big for the raw-GGUF metadata field (LM Studio silently truncates
templates over ~980 KB), so it is delivered via `model.yaml` → `llm.load.promptTemplate`, which LM
Studio hands to its own `llama-server` with `--chat-template-file` (no size cap). Just **Download →
Load → chat**. Needs a recent LM Studio (llama.cpp engine ≥ the 2.24.0 line).

### llama.cpp
```bash
llama-server -m gemma-4-E2B-it-Q4_K_M.gguf --jinja \
  --chat-template-file chat-template.jinja --port 8080 --ctx-size 8192
```
**Sampling — Gemma-native:** `temperature 1.0, top_k 64, top_p 0.95, min_p 0.01` (the `min_p` floor
prevents reasoning-loop empty answers). Don't quantize the KV cache on a model this small. The bank
ships **thinking-OFF** — the correct config for a baked expert (chain-of-thought tends to revert a
habit-reversal fact to the model's trained prior).

## Limitations
- **Scoped to application-security / secure coding.** Outside that, it's the base model.
- **Supplies knowledge, not reasoning.** A 2B still misses some multi-step fixes (e.g. stripping
  newlines for log-injection).
- **Keyword + faceted retrieval, not embeddings.** A wholly unexpected phrasing can miss; there is
  no "I don't know" signal — a miss looks like a normal answer.
- **Grounded, audited — but research-grade.** Facts are quote-verified and correctness-audited, not
  a security guarantee. Review generated code; this is an assistant, not a substitute for review.
- Hand-scored security tests, not a general coding benchmark.

## Provenance & license
- **Base:** `lmstudio-community/gemma-4-E2B-it-GGUF` (weights untouched). This artifact only rewrites
  the chat-template to embed an inverted-index retriever + the bank (`factbank.version 0.4.0`).
- **License:** Google **Gemma Terms of Use** (`license: gemma`) — a gemma-4 derivative. The fact bank
  is FactBank-project content (repo `LICENSE`); mined sources keep their own licenses.
- **Source & method:** [github.com/mhndayesh/experts-models](https://github.com/mhndayesh/experts-models).
