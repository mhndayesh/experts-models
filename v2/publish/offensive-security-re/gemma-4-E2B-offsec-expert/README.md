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
  - pentesting
  - reverse-engineering
  - retrieval
---
> **⚙️ Recommended runtime settings** — gemma-native sampling `temperature 1.0, top_k 64, top_p 0.95, min_p 0.01` (the **`min_p 0.01`** floor prevents the reasoning-loop *empty-answer* issue), context length **≥ 16k (32k recommended)**, and a generous `max_tokens` when running with thinking on. The Gemma-4 thinking path needs `--jinja`.


# gemma-4-E2B-offsec-expert (GGUF)

**Base `gemma-4-E2B-it` with an *Offensive Security & Reverse Engineering* FactBank baked into its chat-template.** The model answers
correctly about post-cutoff / breaking-change APIs in **17 offensive-security / RE libraries** — not by fine-tuning,
but by carrying a searchable bank of **489 landmine facts** that fires **inside llama.cpp** at inference
time. **Weights are untouched** (only the GGUF chat-template was rewritten); no external RAG service.

> The model supplies the reasoning; the bank supplies the knowledge it was never trained on.

> 🔗 **Full project — all experts, methodology, per-question transcripts, and benchmarks:**
> **[github.com/mhndayesh/experts-models](https://github.com/mhndayesh/experts-models)**

## What this expert is about
Red-team tooling and binary analysis move fast and break APIs constantly — a v2→v3 rewrite (volatility3), a Rust rewrite (yara-x), a tool renamed outright (CrackMapExec → **netexec**). A stock model answers about these from stale training and is confidently wrong. This bank carries the exact breaking-change facts so the model gets them right.

Everything here is a **landmine fact**: post-cutoff, reverses-a-trained-habit, or a silent failure the model
wouldn't otherwise catch. Every fact is quote-grounded to a real migration guide / changelog line. Examples
the base gets wrong and this model gets right: the CrackMapExec→`netexec` (`nxc`) rename, the volatility3 v3 plugin shape (`PluginInterface`+`TreeGrid`+`run`), yara-x's Rust rule/API differences, capstone v6, frida 17.

## Libraries in the bank (17) — 489 facts total
| library | facts | what it is / the churn |
|---|---:|---|
| `angr` | 103 | binary analysis / symbolic execution — API migration |
| `ldap3` | 63 | LDAP client (AD tooling) — async module rename, constant renames |
| `capstone` | 58 | disassembly framework — the v6 API break |
| `netexec` | 52 | network execution toolkit — **the CrackMapExec successor** (`nxc`) |
| `pwntools` | 45 | CTF / exploit-dev toolkit — v5 changes |
| `nuclei` | 27 | template-based vulnerability scanner — v3 flags/schema |
| `responder` | 27 | LLMNR/NBT-NS/mDNS poisoner — option changes |
| `impacket` | 18 | network-protocol toolkit — example/API changes |
| `volatility3` | 18 | memory forensics — **the v2→v3 rewrite** (PluginInterface/TreeGrid/run) |
| `frida` | 16 | dynamic instrumentation — the v17 split |
| `unicorn` | 15 | CPU emulator — the v2 API |
| `plaso` | 12 | timeline forensics — tool/flag changes |
| `certipy` | 10 | AD CS abuse — v5 command surface |
| `yara-x` | 10 | **YARA rewritten in Rust** — rule/API differences |
| `dnfile` | 6 | .NET PE parsing — API changes |
| `bloodhound-py` | 5 | BloodHound Python ingestor — CE changes |
| `pefile` | 4 | PE-file parsing — API changes |

## Where the facts come from (mined sources)
Each library's facts were extracted from its **migration guide / changelog** (source targeting is the whole
game — a migration guide, not release-note noise), then quote-verified against the source line:
- angr migration guide
- ldap3 changelog
- capstone v6 changelog
- netexec migration notes
- pwntools 5 changelog
- nuclei 3 changelog
- responder changelog
- impacket changelog
- volatility3 migration guide
- frida 17 notes
- unicorn 2 changelog
- plaso changelog
- certipy v5 notes
- yara-x differences doc
- dnfile changelog
- bloodhound-py docs
- pefile changelog

Full provenance (the mined source docs themselves) lives in the repo under
[`v2/extractor/experts/offensive-security-re/sources/`](https://github.com/mhndayesh/experts-models/tree/main/v2/extractor/experts/offensive-security-re/sources).

## Results (this model — hand-verified)
Same 44 adversarial landmine questions, base vs. this baked model, identical prompts (the bank injects
in-engine). Config: **thinking-on + authority framing**, Gemma-native sampling.

| | base E2B | **this model** | Δ | error-closure* |
|---|---|---|---|---|
| /44 landmine questions | 12/44 (27.3%) | **37/44 (84.1%)** | **+25** | 78% |

\* of the answers the base got wrong, the fraction the bank fixed. Every answer was **hand-scored** — an
automated substring check miscounts in both directions (it fails a correct answer that names the old API as a
contrast, and passes a semantically wrong one).

## How to run
The bank lives in the chat-template, so retrieval needs the template applied — run on **llama.cpp**:
```bash
llama-server -m gemma-4-E2B-offsec-expert-Q4_K_M.gguf --jinja --port 8080 --ctx-size 8192
```
Then query normally — the same prompt you'd send the base model; the bank fires automatically for covered
topics. **Sampling — use Gemma-native**, not a bare low temperature:
`temperature 1.0, top_k 64, top_p 0.95, min_p 0.01` (the `min_p` floor prevents reasoning-loop empty answers).

**Best accuracy (authority + thinking) — this is how the numbers above were measured.** Send
`chat_template_kwargs={"enable_thinking": true}` and a system prompt telling the model the looked-up facts
are verified and supersede its training. A reasoning model otherwise tends to "correct" an injected fact back
to its trained prior; authority framing holds the fact.

## Limitations
- **Scoped to the 17 covered libraries.** Outside them it's the base model.
- **Supplies knowledge, not reasoning.** A multi-step transform can still fail even with the right fact retrieved.
- **Retrieval gate is token-based, with aliases.** This bake includes the **gate-alias fix** — a rename's OLD
  name (e.g. "CrackMapExec") also opens the tab — but a wholly unrelated phrasing may still miss.
- Numbers are **hand-scored** landmine tests, not a general coding benchmark.

## Papers
The write-ups behind this project (PDFs, rendered on GitHub): [Research Report](https://github.com/mhndayesh/experts-models/blob/main/v2/papers/FactBank-Research-Report.pdf) · [Idea](https://github.com/mhndayesh/experts-models/blob/main/v2/papers/FactBank-1-Idea-Paper.pdf) · [Technical](https://github.com/mhndayesh/experts-models/blob/main/v2/papers/FactBank-2-Technical-Paper.pdf) · [Verdict](https://github.com/mhndayesh/experts-models/blob/main/v2/papers/FactBank-3-Verdict-Paper.pdf) · [Evidence Ledger](https://github.com/mhndayesh/experts-models/blob/main/v2/papers/FactBank-Evidence-Ledger.pdf)

## Provenance & license
- **Base:** `lmstudio-community/gemma-4-E2B-it-GGUF` (Q4_K_M). This model = that GGUF with `tokenizer.chat_template` rewritten to embed an
  inverted-index retriever + the bank (`factbank.version 0.4.0`, gate-alias fix applied).
- **License:** Google **Gemma Terms of Use** (`license: gemma`) — a gemma-4 derivative. The fact bank is from
  the FactBank project (see the repo `LICENSE`); mined sources keep their own licenses.
- **Source & method:** [github.com/mhndayesh/experts-models](https://github.com/mhndayesh/experts-models).
