# GitChameleon 2.0 — FactBank vs. the frontier leaderboard

How the FactBank-baked local models land against the published GitChameleon 2.0 results (GPT-4.1, o1,
Claude, Gemini, …). **Read the caveat first — this is not an apples-to-apples comparison.**

> ## ⚠️ We did NOT run the container harness
> The **official** GitChameleon 2.0 leaderboard runs **all 328 problems inside pinned Docker containers**
> with the exact Python (3.7 / 3.9 / 3.10) and dependencies, execution-scored against hidden tests.
>
> **Our numbers do not.** They come from a **local Windows harness with no Docker**: 79 of the 328 problems
> couldn't build here (3.7-era pins with no Windows wheels), so we scored the **249 that did build**,
> hand-verified per problem, and some 3.7 problems were remapped to 3.9. So:
> - **Base-vs-baked is internally fair** — identical 249-problem set, identical harness. The *lift* is real.
> - **The frontier column is a DIFFERENT measurement** (328 problems, Docker, official scorer). Treat it as
>   "what neighborhood are we in," **not** a ranking or a claim of beating those models.
> - FactBank models carry **no external RAG** — the bank is baked into the GGUF chat-template (in-engine).
>
> Provenance + harness caveats: [`PROVENANCE.md`](PROVENANCE.md), [`BAKE-REPORT.md`](BAKE-REPORT.md), `run_tests.py`.

## Official leaderboard — GitChameleon 2.0 (328 problems, Docker, pass@1 on hidden tests)
Source: *GitChameleon 2.0*, arXiv [2507.12367](https://arxiv.org/abs/2507.12367).

| model | greedy (no RAG) | + RAG |
|---|---|---|
| o1 | 51.2% | — |
| Gemini 2.5 Pro | 50.0% | 56.7% |
| GPT-4o | 49.1% | — |
| Claude 3.7 Sonnet | 48.8% | 56.1% |
| **GPT-4.1** | **48.5%** | **58.5%** |
| Claude 4 Sonnet | — | **59.4%** (best reported) |

*The paper's headline: frontier enterprise models sit in the **48–51%** range greedy; RAG adds ~10 pts.*

## FactBank (ours) — local, non-Docker, 249/249 buildable subset, hand-verified, no RAG
Bank baked into the GGUF chat-template; retrieval runs in-engine. Same base weights, base-vs-baked on the
identical 249-problem set.

| model (Q4, local) | pass@1 (249 buildable) | vs. its own base |
|---|---|---|
| gemma-4-12B — base | 37.8% | — |
| gemma-4-12B — **+ FactBank** (thinking-OFF) | **44.2%** | **+6.4** |
| gemma-4-12B — **+ FactBank** (2-pass: authority+thinking on the misses) | **54.2%** | **+16.4** |
| gemma-4-26B-A4B — base | 43.4% | — |
| gemma-4-26B-A4B — **+ FactBank** (thinking-OFF) | **46.2%** | **+2.8** |

## What this does and doesn't say
- **Does:** the bank moves a **local Q4 model** by +6.4 (12B, one pass) and +16.4 (12B, two-pass) on our
  execution set — no weight training, no RAG service, facts baked into the template. The two-pass 12B (54.2%
  on our 249) lands **in the neighborhood of the frontier greedy baselines** (48–51% on their 328) and below
  the best RAG figure (59.4%). That a laptop-class 12B with a baked fact bank reaches that neighborhood at
  all is the point.
- **Doesn't:** claim to beat GPT-4.1 or anyone. Different problem count (249 vs 328), different harness (no
  Docker), a remap (3.7→3.9), and hand-scoring make the two columns **not directly comparable**. To make a
  real leaderboard entry we'd need the official containerized run (owner-gated; see WS-BENCH).

## To make it comparable (open, owner-gated)
Run the official Docker harness (`Dockerfile` / `Makefile` here) on all 328 problems for base and baked,
scored by the upstream scorer. That converts these provisional numbers into a leaderboard-legitimate row.
