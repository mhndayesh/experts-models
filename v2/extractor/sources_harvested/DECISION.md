# Source-harvest build-cost decision (2026-07-15)

Sources for 5 candidate domains were harvested (see `manifest.md`). The card pipeline is a
**code-changelog miner** (miner grammar + gate + LLM second-line + expand + bake). Sorting the
harvest by BUILD COST — not market value, which was decided earlier — gives:

## KEEP — cheap, reuses / lightly extends proven tooling (all code-changelog-shaped)

| target | sources | why cheap |
|---|---|---|
| **python-ai** (lead) | openai / anthropic / langchain / langgraph / llama_index / pydantic | Python symbol grammar ALREADY exists (pandas miner reuses); symbol-rich changelogs; zero new tooling |
| **web-next-react** | next.js, react | one new JS/TS miner grammar = the Ecto retarget again (~an afternoon, proven) |
| **k8s deprecated-APIs** | k8s.deprecation-guide.md | `"X no longer served as of vN.M"` = pure rules, the cheapest mine of all |
| **transformers** | transformers (from local-ai) | Python, reuse the grammar; carries the local-AI flavor for free |

## DROP / DEFER — different tooling or too heavy ("takes a lot")

| target | sources (kept on disk, not mined now) | why deferred |
|---|---|---|
| **CVE / CISA-KEV** | cisa-kev.json | NOT a changelog — needs a from-scratch data-feed miner; corpus is huge (F-055 targeting wall). Biggest lift. |
| **Terraform-AWS** | terraform-aws.CHANGELOG.md, terraform-aws.v6-upgrade.md | 386 KB HCL changelog + a 2nd new grammar; K8s already carries DevOps |
| **llama.cpp / Ollama / vLLM** | llama.cpp / ollama / vllm release notes | noisy PR-title release notes + C++/CLI grammar; transformers covers local-AI |

**Net: 5 domains -> 4 clean mineable targets, all in the pipeline's sweet spot.**
A genuine NON-CODING expert (CVE etc.) is a separate, larger build — flagged, not pretended cheap.
Deferred source files are retained (small, reversible); delete only on owner request.
