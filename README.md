# FactBank — expert models from a bank of landmine facts

[![Hugging Face — Experts Models](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Experts%20Models%20Collection-ffce1c?style=for-the-badge)](https://huggingface.co/collections/mhndayesh/experts-models-6a595448703ca843051011a1)
[![Hugging Face — Information Security Experts](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Information%20Security%20Experts-ff6f61?style=for-the-badge)](https://huggingface.co/collections/mhndayesh/information-security-experts-6a5acc07beca2a1896a94af8)
[![License: Gemma](https://img.shields.io/badge/models-Gemma%20license-4285F4?style=for-the-badge)](https://ai.google.dev/gemma/terms)

Make a stock LLM answer correctly about fast-moving libraries it was **never trained on** — by baking a
searchable bank of **landmine facts** (post-cutoff / reverses-a-habit / silent-failure) into the model's own
GGUF chat-template. The model keeps doing the reasoning; the bank supplies the knowledge it's missing. No
fine-tuning, no retraining, no external RAG service — retrieval runs *inside* the model at inference time.

> **The thesis, proven:** knowledge and reasoning are separable. Hand a model the exact fact it's missing at
> the moment it needs it, and even a 2B edge model answers like it was trained yesterday — on libraries it
> never saw.

**🐛 Found a bug or a wrong/stale fact?** [Report a problem](https://github.com/mhndayesh/experts-models/issues) — please include the expert, size, edition (thinking on/off), and the exact prompt.

## Why even a small model works
The coding and reasoning come from the model itself, and that part is already strong, even in the small sizes.
What smaller models lack is not intelligence, it is up to date knowledge. They were simply never trained on the
newest library versions. The bank fills exactly that gap: it hands the model the current facts right when it
needs them, so the model can apply skills it already has. Because reasoning was never the missing piece, a small
model plus the bank closes much of the distance to a big model on covered libraries. Bigger models use a
retrieved fact a bit more reliably, but the small models are the ones that gain the most.

## Start here
- **[`v2/BUILD-AN-EXPERT.md`](v2/BUILD-AN-EXPERT.md)** — the A-to-Z playbook: pick a library → mine its
  migration guide → extract facts with an LLM → bake into a GGUF → serve → test. Your first expert in an
  afternoon, ~4¢ of API cost. Everything you need is on that one page.
- **[`v2/README.md`](v2/README.md)** — the full project map (extractor · bake · serving · package · docs).

## Ready-to-run models (Hugging Face)
Four experts, each baked into three sizes (2B / 12B / 26B) — run with llama.cpp, the bank fires in-engine.
Browse the churn-library experts on the **[🤗 Experts Models collection](https://huggingface.co/collections/mhndayesh/experts-models-6a595448703ca843051011a1)** and the security expert on the **[🤗 Information Security Experts collection](https://huggingface.co/collections/mhndayesh/information-security-experts-6a5acc07beca2a1896a94af8)**.

### `security` — Secure code by default (application security · 258 concepts (254 CWE) / 3,984 variants) 🆕
A bank of **insecure-by-default landmines** that makes the model write secure code without being asked —
`torch.load(weights_only=True)`, XXE `resolve_entities=False`, `yaml.safe_load`, `secrets` over `random`,
parameterized SQL, `os.environ` creds. Mined from **CWE · CodeQL · Bandit/gosec · MASTG · RustSec ·
NIST/RFC/Mozilla · OWASP**, across 10+ languages. **Two editions per size** — *thinking-OFF* (fast, reliable,
the default) and *thinking-ON* (shows a reasoning trace; ~10% of hard prompts may run long/blank, fails safe).

| size | thinking-OFF | thinking-ON | LM Studio Hub |
|---|---|---|---|
| **E2B** (~2B edge) | [🤗 GGUF](https://huggingface.co/mhndayesh/gemma-4-E2B-security-expert-GGUF) | same repo (`-thinking.gguf`) | [Hub](https://lmstudio.ai/mhndayesh/gemma-4-e2b-security-expert) · [+think](https://lmstudio.ai/mhndayesh/gemma-4-e2b-security-expert-thinking) |
| **12B** | [🤗 GGUF](https://huggingface.co/mhndayesh/gemma-4-12B-security-expert-GGUF) | same repo (`-thinking.gguf`) | [Hub](https://lmstudio.ai/mhndayesh/gemma-4-12b-security-expert) · [+think](https://lmstudio.ai/mhndayesh/gemma-4-12b-security-expert-thinking) |
| **26B-A4B** | [🤗 GGUF](https://huggingface.co/mhndayesh/gemma-4-26B-A4B-security-expert-GGUF) | same repo (`-thinking.gguf`) | [Hub](https://lmstudio.ai/mhndayesh/gemma-4-26b-security-expert) · [+think](https://lmstudio.ai/mhndayesh/gemma-4-26b-security-expert-thinking) |

On **SecurityEval** (thinking-off, 21-task common subset, identical scoring): e2b 13 · 12b 17 · **26b 19 (best)**
vs **DeepSeek-V4** (no-thinking) 14 — 12B+bank and 26B+bank beat the cloud model. *(In-template retrieval is
prompt-only; the served-loop + HyDE draft-key reaches higher — see the card's honest note.)*
Recommended runtime: `temperature 1.0, top_k 64, top_p 0.95, min_p 0.01`, context ≥ 16k (32k baked). Because
the bank template is 4.2 MB (over LM Studio's raw-GGUF cap), **LM Studio users use the Hub links above**.

### `netsec` — Security & Networking (114 facts, 7 libraries)
cryptography · OpenSSL 3 · paramiko 3 · urllib3 2 · volatility3 · yara-x · eBPF. *(Easy/hard landmine split.)*

| size | download | size | base→baked |
|---|---|---|---|
| **E2B** (~2B edge) | [🤗](https://huggingface.co/mhndayesh/gemma-4-E2B-netsec-expert-GGUF) | 3.2 GB | 39.6→**66.7%** |
| **12B** | [🤗](https://huggingface.co/mhndayesh/gemma-4-12B-netsec-expert-GGUF) | 6.5 GB | 56.2→**81.2%** |
| **26B-A4B** | [🤗](https://huggingface.co/mhndayesh/gemma-4-26B-A4B-netsec-expert-GGUF) | 13.5 GB | 77.1→**93.8%** |

### `offsec` — Offensive Security & Reverse Engineering (489 facts, 17 libraries)
angr · ldap3 · capstone · **netexec** (ex-CrackMapExec) · pwntools · nuclei · responder · impacket · volatility3 ·
frida · unicorn · plaso · certipy · yara-x · dnfile · bloodhound-py · pefile. *(44 adversarial landmine Qs,
thinking-on + authority.)*

| size | download | size | base→baked |
|---|---|---|---|
| **E2B** (~2B edge) | [🤗](https://huggingface.co/mhndayesh/gemma-4-E2B-offsec-expert-GGUF) | 3.2 GB | 27.3→**84.1%** |
| **12B** | [🤗](https://huggingface.co/mhndayesh/gemma-4-12B-offsec-expert-GGUF) | 6.5 GB | 27.3→**97.7%** |
| **26B-A4B** | [🤗](https://huggingface.co/mhndayesh/gemma-4-26B-A4B-offsec-expert-GGUF) | 13.5 GB | 38.6→**97.7%** |

### `dataplane` — eBPF & the Networking Data Plane (318 facts, 7 libraries)
libbpf · cilium · frr · eBPF (BCC→libbpf) · dpdk · xdp/libxdp · vpp. *(47 adversarial landmine Qs, thinking-on
+ authority.)*

| size | download | size | base→baked |
|---|---|---|---|
| **E2B** (~2B edge) | [🤗](https://huggingface.co/mhndayesh/gemma-4-E2B-dataplane-expert-GGUF) | 3.2 GB | 10.6→**68.1%** |
| **12B** | [🤗](https://huggingface.co/mhndayesh/gemma-4-12B-dataplane-expert-GGUF) | 6.5 GB | 34.0→**87.2%** |
| **26B-A4B** | [🤗](https://huggingface.co/mhndayesh/gemma-4-26B-A4B-dataplane-expert-GGUF) | 13.5 GB | 42.6→**91.5%** |

```bash
llama-server -m gemma-4-12B-offsec-expert-Q4_0.gguf --jinja --port 8080
```
Model cards (also the HF README for each): [`v2/publish/`](v2/publish/) — `security-networking/`,
`offensive-security-re/`, `ebpf-dataplane/`. Publishing kit: [`v2/publish/PUBLISH.md`](v2/publish/PUBLISH.md).

## Results (measured, hand-verified)

### 1 — Security & Networking expert: the 2B / 12B / 26B curve
Same 114-fact bank, same 48 landmine questions, base vs. baked (bank in-template, no RAG):

| model | base | + FactBank | Δ | error-closure* |
|---|---|---|---|---|
| gemma-4 e2b (~2B) | 19/48 (39.6%) | **32/48 (66.7%)** | **+13** | 45% |
| gemma-4 12B | 27/48 (56.2%) | **39/48 (81.2%)** | **+12** | 57% |
| gemma-4 26B-A4B | 37/48 (77.1%) | **45/48 (93.8%)** | **+8** | 73% |

\* of the base's wrong answers, the fraction the bank fixed. Raw lift shrinks with size but error-closure
rises — **small models need the bank most, big models use it best.**
Detail: [`…/security-networking/BAKE-TEST-CURVE-3MODEL.md`](v2/extractor/experts/security-networking/BAKE-TEST-CURVE-3MODEL.md).

### 2 — GitChameleon 2.0: a local 12B + FactBank vs. the frontier leaderboard

| model | pass@1 (greedy) | + RAG |
|---|---|---|
| o1 | 51.2% | — |
| Gemini 2.5 Pro | 50.0% | 56.7% |
| GPT-4o | 49.1% | — |
| Claude 3.7 Sonnet | 48.8% | 56.1% |
| **GPT-4.1** | **48.5%** | 58.5% |
| Claude 4 Sonnet | — | **59.4%** (best) |
| — | | |
| gemma-4-12B — base (no bank) | 37.8% | — |
| **gemma-4-12B + FactBank** — thinking-off | **44.2%** | — |
| **gemma-4-12B + FactBank** — two-pass (authority) | **54.2%** | — |
| gemma-4-26B-A4B + FactBank — thinking-off | 46.2% | — |

> ⚠️ **Not apples-to-apples — we did NOT run the container harness.** The frontier rows are the official run:
> **all 328 problems in pinned Docker containers** (arXiv [2507.12367](https://arxiv.org/abs/2507.12367)).
> The FactBank rows are a **local, non-Docker** harness over the **249 problems that built** on Windows
> (hand-verified, some 3.7→3.9 remapped, no RAG — the bank is baked into the template). **Base-vs-baked is
> internally fair; the frontier column is a different measurement** — read it as "what neighborhood," not a
> ranking or a claim of beating those models. Full table + caveats:
> [`v2/eval/gitchameleon/LEADERBOARD-COMPARISON.md`](v2/eval/gitchameleon/LEADERBOARD-COMPARISON.md).

Fact-making pipeline behind both: FIND (migration guide) → extract → repair → check; the verbatim quote is
the anti-hallucination gate. For the faceted (concept→variant) security bank the full build — three LLM
enrichment passes → assemble — is **scripted and reproducible**
([`REBUILD.md`](v2/extractor/experts/appsec/facts/REBUILD.md) + `build_v3_assemble2.py`; rebuilds 91% of the
shipped bank exactly from its committed inputs). The extractor speaks the **standard OpenAI API** (DeepSeek by
default, or point it at OpenAI / any compatible server).

## Papers
Five write-ups of the project (PDF, with editable `.docx` sources in [`v2/papers/`](v2/papers/)):
- **[Research Report](v2/papers/FactBank-Research-Report.pdf)** the full technical report and foundation for a future paper
- **[Idea Paper](v2/papers/FactBank-1-Idea-Paper.pdf)** the concept, motivation, and real-world use, in plain terms
- **[Technical Paper](v2/papers/FactBank-2-Technical-Paper.pdf)** architecture, retrieval, and where the gains come from
- **[Verdict Paper](v2/papers/FactBank-3-Verdict-Paper.pdf)** a critical assessment: strengths, weaknesses, novelty, risks
- **[Evidence Ledger](v2/papers/FactBank-Evidence-Ledger.pdf)** every claim mapped to a real file or number in the repo

## How it works (one glance)
```
pick a library → mine its migration guide → extract landmine facts (LLM, quote-grounded)
   → bake an inverted-index retriever + the facts into the GGUF chat-template
   → serve on llama-server (--jinja) → the bank fires in-engine, base prompt unchanged
   → test base vs expert on landmine questions, hand-scored
```

## Layout
> **Everything lives in [`v2/`](v2/) — that's the actual, canonical project** (the code, banks, experts, docs, and papers). The `v2` name is historical; there is no active `v1` to switch between.

| path | what |
|---|---|
| [`v2/extractor/`](v2/extractor/) | the fact-making engine + the built experts (`experts/<dept>/`) |
| [`v2/bake/`](v2/bake/) | bakes a bank into a GGUF chat-template (inverted index) + the serve launcher |
| [`v2/serving/`](v2/serving/) | how a bank ships inside a GGUF (retrieval + limits) |
| [`v2/package/`](v2/package/) | the installable `factbank` package |
| [`v2/eval/`](v2/eval/) | benchmarks (GitChameleon) |
| [`v2/decisions/`](v2/decisions/) · [`v2/papers/`](v2/papers/) | live blueprints and write-ups |

## Scope of this repo
This is the **active, latest-only tree** (`v2/`). The project's historical evidence trail (the F-001…F-065
archive) and the multi-GB source corpus are **intentionally not included** — they're large, partly under
third-party licenses, and not needed to build or run an expert. Model weights (`*.gguf`, `*.safetensors`)
are never committed. A few docs reference `archive/…` for provenance; that content lives in the project's
full archive, outside this repo.

## License
Code and docs: see [`LICENSE`](LICENSE). Third-party notices: [`THIRD-PARTY-NOTICES.md`](THIRD-PARTY-NOTICES.md).
Mined source documents retain their original licenses (each expert's `sources/` records provenance).
