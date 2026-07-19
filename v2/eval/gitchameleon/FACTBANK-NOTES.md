# GitChameleon 2.0 — our test harness for base vs. expert

Cloned 2026-07-15 from https://github.com/mrcabbage972/GitChameleonBenchmark (Apache-2.0 code,
MIT dataset). This is the recognized benchmark we picked to measure **base model vs. base + FactBank**.
Paper: arXiv 2507.12367 (ACL 2026 Main). Website: gitchameleon-2-0.github.io.

## Why this one
It tests the *exact* thing our bank exists for: can a model use a library API **as it existed at a
specific version** — real, documented breaking changes, not synthetic. It is **execution-scored**
(hidden pytest), it is **hard** (enterprise SOTA ~48–51% base), and it already ships the comparison
we want to win: **base vs. base + doc-RAG** (GPT-4.1 +RAG hit 58.5%). Our bank is a sharper RAG lane,
so the headline is: `base 48–51% → published RAG 58.5% → FactBank ___%`.

## What's in the box
- `dataset/dataset.jsonl` — **328 problems**, self-contained (no HF download needed).
- `dataset/ground_truth_solutions.jsonl` — reference answers keyed by `example_id`.
- `dataset/visible_tests/`, `dataset/hidden_tests/` — the pytest suites (visible = self-debug, hidden = score).
- `gitchameleon/` — the eval harness package. Run: `make evals-setup` then `evaluate --solution-path FILE`.
  **Needs Python 3.9+, Poetry, and Docker** (each problem runs in a pinned-version container).

### One record (fields we use)
`library`, `version`, `python_version`, `problem` (NL task), `starting_code` (stub to complete),
`test` (visible assertions), `solution` (reference), `type_of_change`, `api_calls`, `release_date`,
and **`docs`** (documentation URLs) — that last field is a ready-made source list for our extractor.

## Coverage — 26 libraries, 328 problems (2014–2024, most 2021–2023)
```
librosa 42  scipy 40  sympy 33  flask 22  falcon 21  torch 18  numpy 15  scikit-learn 12
pandas 10  django 10  mitmproxy 10  networkx 9  lightgbm 9  pytest 9  plotly 9  geopandas 8
seaborn 8  tornado 8  gradio 7  nltk 6  matplotlib 6  pillow 6  jinja2 4  spacy 3  tqdm 2  kymatio 1
```
Change types: argument change 59 · name change 52 · new func/class 46 · argument/attribute 44 ·
new feature 40 · breaking change 15 · output behaviour 13 · deprecation 13 · other. (213 functional / 115 webdev.)

## THE GAP to close before this measures our expert
Our current AI-ML expert (817 facts, 11 doors: transformers/vLLM/LangChain/OpenAI/llama-cpp/pydantic/…)
**does not overlap these 26 libraries.** So this benchmark does NOT test the existing bank. To use it we
build a **GitChameleon bank**: point the extractor at each library's migration/changelog (the dataset's
`docs` URLs are a head start), one door per lib. Cheap (DeepSeek, no GPU), and it yields a recognized,
apples-to-apples number with a RAG baseline built in.

## The run plan (when approved — nothing run yet)
1. **Base pass:** feed each `problem` + `starting_code` (at its pinned `version`) to the loaded model,
   capture the completion as `answer` → `solutions.base.jsonl`. Score with `evaluate`.
2. **Expert pass:** same, but with the FactBank retrieval loop injecting version-matched facts. Score.
3. Report both, **read outputs by hand** (SCORE MANUALLY), compare against the paper's 48–51% / 58.5%.

Gates unchanged: no model load/unload, no experiment without the owner's OK, free VRAM after.
