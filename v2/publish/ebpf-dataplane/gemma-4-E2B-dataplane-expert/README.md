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
  - networking
  - ebpf
  - dpdk
  - retrieval
---
> **⚙️ Recommended runtime settings** — gemma-native sampling `temperature 1.0, top_k 64, top_p 0.95, min_p 0.01` (the **`min_p 0.01`** floor prevents the reasoning-loop *empty-answer* issue), context length **≥ 16k (32k recommended)**, and a generous `max_tokens` when running with thinking on. The Gemma-4 thinking path needs `--jinja`.


# gemma-4-E2B-dataplane-expert (GGUF)

**Base `gemma-4-E2B-it` with an *eBPF & the Networking Data Plane* FactBank baked into its chat-template.** The model answers
correctly about post-cutoff / breaking-change APIs in **7 networking data-plane libraries** — not by fine-tuning,
but by carrying a searchable bank of **318 landmine facts** that fires **inside llama.cpp** at inference
time. **Weights are untouched** (only the GGUF chat-template was rewritten); no external RAG service.

> The model supplies the reasoning; the bank supplies the knowledge it was never trained on.

> 🔗 **Full project — all experts, methodology, per-question transcripts, and benchmarks:**
> **[github.com/mhndayesh/experts-models](https://github.com/mhndayesh/experts-models)**

## What this expert is about
The Linux networking data plane — eBPF/XDP in the kernel, DPDK/VPP in userspace, and the controllers (Cilium, FRR) that program them — churns hard: the whole **BCC→libbpf (CO-RE)** shift, libxdp splitting out of the kernel tree, Cilium config keys renamed (`tunnel`→`routingMode`). This bank carries those breaking-change facts so the model stops answering from the old world.

Everything here is a **landmine fact**: post-cutoff, reverses-a-trained-habit, or a silent failure the model
wouldn't otherwise catch. Every fact is quote-grounded to a real migration guide / changelog line. Examples
the base gets wrong and this model gets right: the BCC→libbpf CO-RE conversion, libxdp's split from the kernel, Cilium's `tunnel`→`routingMode`, DPDK removed APIs, FRR operator changes.

## Libraries in the bank (7) — 318 facts total
| library | facts | what it is / the churn |
|---|---:|---|
| `libbpf` | 93 | the canonical eBPF loader — v1 API, **BCC→libbpf** migration |
| `cilium` | 74 | eBPF-based Kubernetes networking/CNI — config-key renames |
| `frr` | 65 | FRRouting (BGP/OSPF/… routing suite) — operator-facing changes |
| `ebpf` | 42 | eBPF programming model — the **BCC→libbpf CO-RE** shift |
| `dpdk` | 25 | userspace packet processing — deprecated/removed APIs |
| `xdp` | 12 | XDP / **libxdp** fast path — the split from the kernel tree |
| `vpp` | 7 | FD.io Vector Packet Processing — release changes |

## Where the facts come from (mined sources)
Each library's facts were extracted from its **migration guide / changelog** (source targeting is the whole
game — a migration guide, not release-note noise), then quote-verified against the source line:
- eBPF BCC→libbpf migration guide
- libbpf v1 notes
- xdp/libxdp split doc
- cilium upgrade guide
- DPDK deprecation notices
- VPP release notes
- FRR changelog

Full provenance (the mined source docs themselves) lives in the repo under
[`v2/extractor/experts/ebpf-dataplane/sources/`](https://github.com/mhndayesh/experts-models/tree/main/v2/extractor/experts/ebpf-dataplane/sources).

## Results (this model — hand-verified)
Same 47 adversarial landmine questions, base vs. this baked model, identical prompts (the bank injects
in-engine). Config: **thinking-on + authority framing**, Gemma-native sampling.

| | base E2B | **this model** | Δ | error-closure* |
|---|---|---|---|---|
| /47 landmine questions | 5/47 (10.6%) | **32/47 (68.1%)** | **+27** | 64% |

\* of the answers the base got wrong, the fraction the bank fixed. Every answer was **hand-scored** — an
automated substring check miscounts in both directions (it fails a correct answer that names the old API as a
contrast, and passes a semantically wrong one).
> **Honest note (12B):** ~3 of 47 cases regressed — the base was already right and the injected fact + reasoning made it worse (the reasoning-paradox tax). Reported, not hidden.

## How to run
The bank lives in the chat-template, so retrieval needs the template applied — run on **llama.cpp**:
```bash
llama-server -m gemma-4-E2B-dataplane-expert-Q4_K_M.gguf --jinja --port 8080 --ctx-size 8192
```
Then query normally — the same prompt you'd send the base model; the bank fires automatically for covered
topics. **Sampling — use Gemma-native**, not a bare low temperature:
`temperature 1.0, top_k 64, top_p 0.95, min_p 0.01` (the `min_p` floor prevents reasoning-loop empty answers).

**Best accuracy (authority + thinking) — this is how the numbers above were measured.** Send
`chat_template_kwargs={"enable_thinking": true}` and a system prompt telling the model the looked-up facts
are verified and supersede its training. A reasoning model otherwise tends to "correct" an injected fact back
to its trained prior; authority framing holds the fact.

## Limitations
- **Scoped to the 7 covered libraries.** Outside them it's the base model.
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
