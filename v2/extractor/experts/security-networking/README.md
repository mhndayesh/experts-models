# Security & Networking Expert

A FactBank expert: **114 curated landmine facts** across **7 elite security/networking libraries**, baked
into **three** stock gemma-4 GGUFs — **2B (e2b), 12B, and 26B** — and proven to correct the model's
post-cutoff knowledge in-engine, at every size, hand-verified.

> **Thesis in one line:** the model supplies the reasoning; the bank supplies the knowledge it was never
> trained on. Nowhere is that clearer than security tooling, where a v2→v3 rewrite (volatility3) or a
> Rust rewrite (yara-x) leaves the model confidently wrong.

**⬇️ Download (Hugging Face):** [E2B](https://huggingface.co/mhndayesh/gemma-4-E2B-netsec-expert-GGUF) ·
[12B](https://huggingface.co/mhndayesh/gemma-4-12B-netsec-expert-GGUF) ·
[26B-A4B](https://huggingface.co/mhndayesh/gemma-4-26B-A4B-netsec-expert-GGUF) — or the whole
[🤗 Experts Models collection](https://huggingface.co/collections/mhndayesh/experts-models-6a595448703ca843051011a1).

---

> **Gate-alias fix applied (2026-07-17):** these three GGUFs are now re-baked with the **gate-alias fix**
> and re-uploaded in place. Previously the exact-token gate stayed shut on a natural/old name ("Volatility 3"
> vs `volatility3`), injecting 0 facts; now `gen_gate_aliases.py` (100 aliases, incl. `volatility`→volatility3)
> + `bake_index.py --extra-aliases` opens the tab. Verified offline: "Volatility 3" injects **0→5** facts.
> The pre-fix bake is preserved on each HF repo as tag `v1-pre-gate-fix`. See
> [`../../../publish/PUBLISH.md`](../../../publish/PUBLISH.md) and `serving/LIMITS.md`.

## At a glance

| | value |
|---|---|
| Libraries | cryptography, openssl 3, paramiko 3, urllib3 2, volatility3, yara-x, ebpf (BCC→libbpf) |
| Facts | **114** — all landmine (post-cutoff / reverses-a-habit / silent-failure), 100% quote-grounded, 0 integrity issues |
| Baked into | `factbank/gemma-4-{E2B,12B,26B-A4B}-netsec-expert-GGUF` (~118 KB template, 2317 index terms) |
| Config under test | thinking-ON + authority framing, Gemma-native sampling, 6-parallel |

### Results — the 2B / 12B / 26B curve (same bank, same 48 questions, every answer hand-verified)

| model | base | **baked** | Δ | base % | baked % | error-closure* |
|---|---|---|---|---|---|---|
| **e2b (~2B)** | 19/48 | **32/48** | **+13** | 39.6% | 66.7% | 45% |
| **12b** | 27/48 | **39/48** | **+12** | 56.2% | 81.2% | 57% |
| **26b (A4B)** | 37/48 | **45/48** | **+8** | 77.1% | 93.8% | 73% |

\* *of the answers the base got wrong, the fraction the bank fixed.*

Two honest trends: the **raw lift shrinks as the base grows** (+13→+12→+8 — the bigger model already knows
more), but **error-closure rises** (45%→57%→73% — the bigger model *applies* a retrieved fact more reliably).
The small model needs the bank most; the big model uses it best. Full synthesis:
**[BAKE-TEST-CURVE-3MODEL.md](BAKE-TEST-CURVE-3MODEL.md)**. The bank ties where the base already knows the
mainstream API and **wins decisively on the genuine rewrites** (volatility3, yara-x, OpenSSL-3 provider APIs).

> Note: the 26b easy set was scored earlier at `temp 0.6` (pre native-sampling fix); e2b/12b used native
> sampling + 6-parallel throughout. Direction is unaffected; a strict single-method curve wants the 26b easy
> set re-run (owner-gated). See the curve doc's caveats.

---

## Documentation map

| doc | what it covers |
|---|---|
| **[COVERAGE.md](COVERAGE.md)** | the bank itself — every library, fact count, landmine examples, and mined source |
| **[METHODOLOGY.md](METHODOLOGY.md)** | the reproducible pipeline: extract → bake → serve → test (all 3 models) |
| **[BAKE-TEST-CURVE-3MODEL.md](BAKE-TEST-CURVE-3MODEL.md)** | **the cross-model synthesis** — the 2B/12B/26B curve, error-closure trend, caveats |
| **[BAKE-TEST-REPORT.md](BAKE-TEST-REPORT.md)** | 26b base-vs-bank findings, hand-scored, per-question tables |
| **[BAKE-TEST-REPORT-12b.md](BAKE-TEST-REPORT-12b.md)** | 12b base-vs-bank (the middle point; trivial bake) |
| **[BAKE-TEST-REPORT-e2b.md](BAKE-TEST-REPORT-e2b.md)** | e2b base-vs-bank (the edge model; needed re-anchoring) |
| **[MODEL-SETTINGS.md](MODEL-SETTINGS.md)** | every model / serving / sampling setting + the sampling bug we fixed |
| **[RESEARCH.md](RESEARCH.md)** | elite-tier roadmap — which tools to mine next and why |

> The e2b bake needed a different chat-template revision re-anchored — documented at
> `../../../bake/template-brain-v3.1/E2B-BAKE-NOTES.md`. 12b and 26b share one template and bake with no
> re-anchoring.

## Folder layout

```
security-networking/
├── README.md                   ← you are here
├── COVERAGE.md                 ← the bank (what's in it)
├── METHODOLOGY.md              ← how it was built, baked, served (6-parallel), and tested
├── BAKE-TEST-CURVE-3MODEL.md   ← the 2B/12B/26B curve (cross-model synthesis)
├── BAKE-TEST-REPORT.md         ← 26b results (base vs bank, hand-verified)
├── BAKE-TEST-REPORT-12b.md     ← 12b results
├── BAKE-TEST-REPORT-e2b.md     ← e2b results
├── MODEL-SETTINGS.md           ← every setting (all 3 models) + the sampling finding
├── RESEARCH.md                 ← what to add next
├── facts/                      ← the 7 bank files (one JSONL per library)
├── sources/                    ← the 7 mined migration guides (provenance)
├── test_secnet.py              ← the test harness (now supports --workers for parallel)
├── test_questions.jsonl / test_questions_hard.jsonl / probe_vol.jsonl  ← the test sets
└── runs/                       ← raw evidence: every transcript, log, and score file (all 3 models)
```

## Findings worth carrying to the rest of the project

1. **Sampling dominates on hard tasks.** Serving Gemma with a bare low temperature caused repetition-loop
   *empty* answers (misread at first as a token-budget limit — it was not). The fix is the model's native
   sampling set, `min_p 0.01` in particular. Held even under **6-way parallel** (0 empties across 288
   parallel requests over the e2b+12b runs). See [MODEL-SETTINGS.md](MODEL-SETTINGS.md).
2. **The retrieval gate is exact-token.** Three volatility3 misses on the easy test were a *gate-vocabulary*
   mismatch ("Volatility 3" vs the token `volatility3`), not missing knowledge — they recovered 3/3 when the
   import token was used. See the gate section in [BAKE-TEST-REPORT.md](BAKE-TEST-REPORT.md).
3. **Auto-triage can *under*-count the bank; hand-read.** On 12b, three baked "fails" were correct answers
   whose only flaw was that the model **named the deprecated API in a migration comment** (`# use password=
   instead of passphrase=`) — the bank's own fingerprint tripping the `avoid_old` substring check.
   Hand-reading raised baked-12b 35→39/48. Read the outputs; the count misleads in both directions.
4. **Model-size trade-off is real and measurable.** Raw lift falls with size (+13→+12→+8) but error-closure
   rises (45%→57%→73%): small models need the bank most, big models use it best. See
   [BAKE-TEST-CURVE-3MODEL.md](BAKE-TEST-CURVE-3MODEL.md).

---
*Part of the FactBank expert-departments program — see [`../DEPARTMENTS.md`](../DEPARTMENTS.md). Built
2026-07-16; extended to the full 2B/12B/26B curve 2026-07-17.*
