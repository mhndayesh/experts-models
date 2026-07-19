# AI-ML Expert — Coverage Spec (2026-07-15)

**What this expert should KNOW, decided from trusted AI/ML curricula** (MIT 6.036/6.S191,
Stanford CS229/224n/231n/234/336, CMU 10-601, Berkeley CS182/285/294, fast.ai, DeepLearning.AI,
HF courses, Full Stack LLM) + library churn analysis. Sourced from 3 research passes.

## The filter
A fact bank only helps where knowledge goes **stale**. Stable theory (classical ML, attention
math, ReAct/CoT) the model already knows from weights — **skip it**. The expert's facts must
target the **high-churn STACKS**. Coverage below is the target; `✅ have · ⚠️ thin · ❌ missing`.

> **UPDATE (2026-07-16): this file's per-stack `have/thin/missing` counts audit an OLD 575-fact
> snapshot.** The **current AI-ML bank is 817 facts across 11 banks/doors** (anthropic, google-genai,
> hf-datasets, langchain, langgraph, llama-cpp, llamaindex, openai, pydantic, transformers, vllm) —
> so several stacks marked ❌/⚠️ below (llama.cpp, LlamaIndex, Google genai, HF datasets, OpenAI,
> LangChain, LangGraph, Anthropic) are now **built**. The tables are kept as the coverage *target*;
> the current counts are in `facts/`.

## Priority 1 — highest churn, core to modern AI
| stack | status | note |
|---|---|---|
| LangChain | ⚠️ 3 | very high churn (v0.1→0.3 package splits); flagship, near-empty |
| LlamaIndex | ❌ | very high churn (v0.10 restructure) |
| LangGraph | ⚠️ 3 | rising core agent orchestrator; 1.0 in 2026 |
| DSPy · Instructor · Pydantic-AI | ❌ | prompt-as-program / structured output |
| OpenAI SDK | ⚠️ 10 | missing v1 rewrite + 2025 Responses API shift |
| Anthropic SDK | ⚠️ 2 | Messages API, caching, thinking |
| Google genai SDK | ❌ | google-generativeai → google-genai migration |
| **vLLM** | ✅ 252 | serving, high churn — well covered |
| **llama.cpp** | ❌ | very high churn; GGUF format — *our own domain* |
| Ollama · TGI | ❌ | local/dev serving |
| **MCP** | ❌ | fastest-moving standard in the whole map |
| Quantization: GGUF/AWQ/GPTQ/bitsandbytes | ❌ | format war, quarterly shifts |
| Post-training: TRL (RLHF/DPO/GRPO) | ❌ | GRPO mainstream only since 2025; TRL 1.0 Apr 2026 |
| PEFT/LoRA · Unsloth · Axolotl · accelerate · DeepSpeed · FSDP2 | ❌ | fine-tuning/scaling |

## Priority 2 — high churn
| stack | status |
|---|---|
| RAG/Vector: Chroma · Pinecone(serverless) · Qdrant · Weaviate · pgvector · embeddings · rerankers | ❌ |
| transformers | ✅ 130 |
| pydantic (v1→v2) | ✅ 175 |
| PyTorch · Keras 3 · JAX/Flax-NNX | ❌ |
| NumPy 2.0 · pandas (CoW) · polars | ❌ |
| Eval: RAGAS · DeepEval · Promptfoo · LangSmith | ❌ |

## Priority 3 — MLOps (medium churn)
MLflow · Weights & Biases · Ray/Ray Serve · BentoML · Airflow/Prefect/Dagster — all ❌

## Skip — stable, answerable from weights
Classical ML theory, tokenization/attention math, scaling-law method, scikit-learn, XGBoost/LightGBM,
FAISS, SciPy, FastAPI, Docker/K8s, ReAct/CoT prompting.

## Status: ~3 of ~25 high-priority stacks covered
- **Solid:** vllm (252), pydantic (175), transformers (130) = 557 facts.
- **Thin:** openai, anthropic, langchain, langgraph (18 facts).
- **Missing:** llama.cpp, LlamaIndex, MCP, quantization, PEFT/TRL, vector DBs, PyTorch, NumPy, eval, MLOps.

## Extraction priority — ranked by CHURN (churn = where the bank beats the model)
Deep churn research (cited, 2024-2026). Extract highest-churn first; **use migration guides, not
release notes** (the [FIND] lesson). ✅ have · ⚠️ thin · ❌ missing.

**Tier 1 — VERY HIGH churn, big recent breaks (extract first):**
| target | status | the landmine / source |
|---|---|---|
| llama.cpp | ❌ | GGUF v1→v2→v3 format breaks, daily builds — *our own domain* |
| transformers v5 | ⚠️ 130 (release notes) | **`MIGRATION_GUIDE_V5.md` (raw on GitHub)** — use_auth_token→token, TF/JAX removed, 7 pipelines gone, Trainer args removed. Fixes Q8. |
| LangChain | ⚠️ 3 | 0.1→0.2→0.3→1.0; LLMChain/AgentExecutor → `langchain-classic`; migration guides |
| LlamaIndex | ❌ | v0.10 import restructure, v0.11 ServiceContext removed, v0.12 broke persisted graphs |
| OpenAI SDK | ⚠️ 10 | v1.0 + v2.0 rewrites, Responses API, **Assistants API sunset (Aug 2026)** |
| Google genai SDK | ❌ | google-generativeai → google-genai full replacement, hard sunsets 2025-26 |
| HF datasets v4.0 | ❌ | loading scripts removed, List type gone, broke lm-eval-harness |
| vLLM | ✅ 252 | V0→V1 engine rewrite — well covered |

**Tier 2 — HIGH churn:**
pandas 3.0 (CoW mandatory, Jan 2026) ❌ · NumPy 2.0 (NEP50) ❌ · polars 1.0 ❌ · PyTorch (weights_only flip, TorchScript deprecated) ❌ · Keras 3 ❌ · Flax NNX ❌ · FSDP2 ❌ · Accelerate 1.0 ❌ · PEFT ❌ · Chroma (Rust rewrite) ❌ · Pinecone (serverless) ❌ · Weaviate v4 ❌ · MLflow 3.0 ❌ · Airflow 3.0 ❌ · Prefect 3.0 ❌

**Tier 3 — LOW churn, skip (model knows / stable):** Anthropic SDK, scikit-learn, FAISS, pgvector, Qdrant, SciPy, LightGBM, DeepSpeed, TGI (frozen), FastAPI, Docker/K8s.

## Then
~~**Landmine-gate** the whole bank — drop facts the model already knows.~~ **REJECTED / CANCELLED.**
Banks stay **RICH, landmine-only, NOT model-gated** — one bank serves 3b/12b/30b, and a 3b lacks a 12b's
knowledge, so dropping "what the model knows" over-fits one model and starves the others. The precision
lever is **source targeting** (migration guides) + the verbatim-quote anchor, not a model-gate. See
`../../BLUEPRINT.md` (WHAT DOESN'T WORK → "Landmine-gate").
