---
license: gemma
base_model: lmstudio-community/gemma-4-12B-it-QAT-GGUF
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
  - networking
  - retrieval
---
> **⚙️ Recommended runtime settings** — gemma-native sampling `temperature 1.0, top_k 64, top_p 0.95, min_p 0.01` (the **`min_p 0.01`** floor prevents the reasoning-loop *empty-answer* issue), context length **≥ 16k (32k recommended)**, and a generous `max_tokens` when running with thinking on. The Gemma-4 thinking path needs `--jinja`.


# gemma-4-12B-netsec-expert (GGUF)

**Base `gemma-4-12B-it-QAT` with a Security & Networking *FactBank* baked into its chat-template.** The model
answers correctly about post-cutoff / breaking-change APIs in 7 security & networking libraries — not by
fine-tuning, but by carrying a searchable bank of **landmine facts** that fires **inside llama.cpp** at
inference time. **Weights are untouched** (only the GGUF chat-template was rewritten); no external RAG service.

> The model supplies the reasoning; the bank supplies the knowledge it was never trained on.

> 🔗 **Full project — all experts, methodology, per-question transcripts, and benchmarks:**
> **[github.com/mhndayesh/experts-models](https://github.com/mhndayesh/experts-models)**

## What it fixes
114 curated **landmine facts** (post-cutoff · reverses-a-trained-habit · silent-failure) across:
**cryptography · OpenSSL 3 · paramiko 3 · urllib3 2 · volatility3 · yara-x · eBPF (BCC→libbpf)**.
Examples the base gets wrong and this model gets right: `RSA_new→EVP_PKEY_new`, `BN_is_prime_ex→BN_check_prime`,
`FIPS_mode→EVP_default_properties_is_fips_enabled`, `SSL_CTX_new→SSL_CTX_new_ex`, TripleDES→`hazmat.decrepit`,
the volatility3 v3 plugin (`PluginInterface`+`TreeGrid`+`run`), yara-x base64/wildcard rule changes.

## Libraries in the bank (7) — 114 facts total
| library | facts | what it is / the churn |
|---|---:|---|
| `openssl` (3) | 31 | OpenSSL 3 — the `RSA_new`→`EVP_PKEY_new` provider-API rewrite, `FIPS_mode`→`EVP_default_properties_is_fips_enabled` |
| `cryptography` | 20 | Python crypto — hazmat API moves, TripleDES→`hazmat.decrepit` |
| `ebpf` | 16 | eBPF from Python — the **BCC→libbpf** shift |
| `paramiko` (3) | 16 | SSH library — v3 key/algorithm removals |
| `urllib3` (2) | 14 | HTTP client — the v2 breaking changes |
| `yara-x` | 9 | **YARA rewritten in Rust** — rule/API differences (base64, wildcards) |
| `volatility3` | 8 | memory forensics — **the v2→v3 rewrite** (`PluginInterface`+`TreeGrid`+`run`) |

## Where the facts come from (mined sources)
Each library's facts were extracted from its **migration guide / changelog** (source targeting is the whole
game — a migration guide, not release-note noise), then quote-verified against the source line:
- cryptography changelog
- OpenSSL 3 migration guide
- eBPF BCC→libbpf migration guide
- paramiko changelog
- urllib3 v2 migration guide
- volatility3 migration guide
- yara-x differences doc

Full provenance (the mined source docs themselves) lives in the repo under
[`v2/extractor/experts/security-networking/sources/`](https://github.com/mhndayesh/experts-models/tree/main/v2/extractor/experts/security-networking/sources).

## Results (this model — hand-verified)
Same 48 landmine questions, base vs. this baked model, identical prompts (the bank injects in-engine):

| set | base 12B | **this model** | Δ |
|---|---|---|---|
| Easy (30 single-API) | 17/30 | **24/30** | **+7** |
| Hard (18 multi-fact / silent-failure) | 10/18 | **15/18** | **+5** |
| **Total (48)** | **27/48 (56.2%)** | **39/48 (81.2%)** | **+12**, 1 regression |

Part of a **2B/12B/26B curve** (e2b 39.6→66.7% · 12B 56.2→81.2% · 26B 77.1→93.8%): raw lift shrinks with
size, error-closure rises. Full methodology, per-question transcripts, and caveats:
[github.com/mhndayesh/experts-models](https://github.com/mhndayesh/experts-models) →
`v2/extractor/experts/security-networking/`.

## How to run
The bank lives in the chat-template, so retrieval needs the template applied — run on **llama.cpp**:
```bash
llama-server -m gemma-4-12B-netsec-expert-Q4_0.gguf --jinja --port 8080 --ctx-size 8192
```
Then query normally (the same prompt you'd send the base model — the bank fires automatically for covered
topics). **Sampling — use Gemma-native**, not a bare low temperature:
`temperature 1.0, top_k 64, top_p 0.95, min_p 0.01` (the `min_p` floor prevents reasoning-loop empty answers).

**Best accuracy (authority + thinking):** send `chat_template_kwargs={"enable_thinking": true}` and a system
prompt that tells the model the looked-up facts are verified and supersede its training. A reasoning model
otherwise tends to "correct" an injected fact back to its trained prior — authority framing holds the fact.
(The 118 KB template is under the LM Studio raw-load size wall, so LM Studio also works — but it ignores
`chat_template_kwargs`, so use llama-server for the thinking-on mode.)

## Limitations
- **Scoped to the 7 covered libraries.** Outside them it's the base model.
- **Supplies knowledge, not reasoning.** Multi-step transforms (e.g. some eBPF CO-RE conversions) can still
  fail even with the right fact retrieved.
- **Retrieval gate is token-based, with aliases.** This bake includes the **gate-alias fix** — a natural or old name (e.g. "Volatility 3", `RSA_new`) also opens the tab; a wholly unrelated phrasing may still miss.
- Numbers are **hand-scored** landmine tests, not a general coding benchmark.

## Also in this project — GitChameleon 2.0 vs. the frontier
The same FactBank approach on a different, code-**execution** benchmark: a local 12B + bank next to the
published GitChameleon 2.0 leaderboard.

| model | pass@1 (greedy) | + RAG |
|---|---|---|
| o1 / Gemini 2.5 Pro / GPT-4o / Claude 3.7 / **GPT-4.1** | 51.2 / 50.0 / 49.1 / 48.8 / **48.5** | — / 56.7 / — / 56.1 / 58.5 |
| Claude 4 Sonnet (best RAG) | — | **59.4** |
| **gemma-4-12B + FactBank** (thinking-off → two-pass) | **44.2 → 54.2** | — |
| gemma-4-12B base | 37.8 | — |

> ⚠️ **Not apples-to-apples — the container harness was NOT run.** Frontier = the official 328-problem run in
> pinned Docker containers ([arXiv 2507.12367](https://arxiv.org/abs/2507.12367)). FactBank rows = a local,
> non-Docker run over the **249 problems that built** (hand-verified, some 3.7→3.9 remapped, no RAG).
> Base-vs-baked is internally fair; the frontier column is a *different measurement* — "what neighborhood,"
> not a ranking. Details:
> [LEADERBOARD-COMPARISON.md](https://github.com/mhndayesh/experts-models/blob/main/v2/eval/gitchameleon/LEADERBOARD-COMPARISON.md).

## Papers
The write-ups behind this project (PDFs, rendered on GitHub): [Research Report](https://github.com/mhndayesh/experts-models/blob/main/v2/papers/FactBank-Research-Report.pdf) · [Idea](https://github.com/mhndayesh/experts-models/blob/main/v2/papers/FactBank-1-Idea-Paper.pdf) · [Technical](https://github.com/mhndayesh/experts-models/blob/main/v2/papers/FactBank-2-Technical-Paper.pdf) · [Verdict](https://github.com/mhndayesh/experts-models/blob/main/v2/papers/FactBank-3-Verdict-Paper.pdf) · [Evidence Ledger](https://github.com/mhndayesh/experts-models/blob/main/v2/papers/FactBank-Evidence-Ledger.pdf)

## Provenance & license
- **Base:** `lmstudio-community/gemma-4-12B-it-QAT-GGUF` (Q4_0). This model = that GGUF with
  `tokenizer.chat_template` rewritten to embed an inverted-index retriever + the bank (`factbank.version 0.4.0`).
- **License:** Google **Gemma Terms of Use** (`license: gemma`) — this is a gemma-4 derivative. The fact bank
  is from the FactBank project (see the repo `LICENSE`); mined sources keep their own licenses.
- **Source & method:** [github.com/mhndayesh/experts-models](https://github.com/mhndayesh/experts-models).
