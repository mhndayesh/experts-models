# Rebuilding the appsec v3 bank (`FINAL_v3.jsonl`)

## The pipeline — `FINAL.jsonl` → `FINAL_v3.jsonl` (all inputs tracked)
From the audited base facts, **three DeepSeek enrichment passes** then **one deterministic merge**:

```bash
cd v2/extractor
K=$(cat /c/projects/api/deepseek.txt)
DEEPSEEK_API_KEY=$K python build_v3_llm.py       # -> v3_llm.jsonl      (cwe, framework, sub_pattern, symbols, aliases, query_phrases)
DEEPSEEK_API_KEY=$K python build_v3_tier1.py     # -> v3_tier1.jsonl    (feature_phrases, library_trigger, disambiguator, canonical_cwe)
DEEPSEEK_API_KEY=$K python build_v3_usecases.py  # -> v3_usecases.jsonl (use_cases)   ** run WITHOUT --sample = ALL facts **
python build_v3_assemble2.py                     # -> FINAL_v3.jsonl    (merge, no LLM)
```

> ⚠️ **Run `build_v3_usecases.py` WITHOUT `--sample`.** In `--sample` mode it writes only the sampled
> facts and **overwrites** `v3_usecases.jsonl` (no merge) — repeated sample runs is exactly what lost
> ~350 feature_phrases from the shipped bank. Plain (no `--sample`) does all 3,984 facts in one file.

**Two ways to run it:**
- **Offline, exact 91%** — the enrichment files (`v3_llm`/`v3_tier1`/`v3_usecases`) are committed, so just
  run step 4 (`build_v3_assemble2.py`) to reproduce the verified 91% (see fidelity below). No LLM/API needed.
- **Full rebuild from base facts** — re-run steps 1–3 (DeepSeek, cheap/no-GPU) then step 4. This produces an
  **equivalent** bank, not byte-identical (the LLM is non-deterministic — different phrasings, same meaning).

`build_v3_assemble2.py` is the **merge** step — it folds `build_v3` (derive) + `v3_llm` + `v3_tier1`
(feature_phrases/library_trigger/disambiguator/canonical_cwe) + `v3_usecases` (use_cases) into the
concept→variant store. It supersedes the partial `build_v3_assemble.py` (v3_llm only — no feature_phrases).

## Reproduction fidelity — verified 2026-07-19
Rebuilt from the on-disk inputs and compared field-by-field to the committed `FINAL_v3.jsonl`:
- **3630 / 3984 variants (91%) exact on every field.** Concept set 258/258; concept n-counts 256/258.
- Exact: `facets`, `claim`, `examples`, `evidence`, `verification`, and retrieval `exact_symbols`,
  `bad_pattern_symbols`, `aliases`, `query_phrases`, `anchor_provenance`, `library_trigger`.

## The 9% residual is irreducibly LOST SOURCE DATA — not a pipeline bug
- **350 `feature_phrases`**: the rebuilt list is a faithful **subset** of the shipped one (never
  wrong-extra). The shipped bank carries extra phrases from earlier `build_v3_usecases.py --sample`
  runs whose intermediate output was overwritten (it runs per-sample and merges in). Those phrases
  survive only inside the committed `FINAL_v3.jsonl`.
- **5 `concept_id`s**: shipped uses `CWE-367` where every committed input says `CWE-377` (a manual
  override, in no input).

## Consequence — `FINAL_v3.jsonl` stays canonical
The committed `FINAL_v3.jsonl` is the **richest** version (it carries the lost-run enrichments).
`build_v3_assemble2.py` faithfully documents and rebuilds the pipeline and is the builder for **future**
experts — but **re-running it over the shipped bank would drop the ~350 lost-run phrases**, so do NOT
overwrite `FINAL_v3.jsonl` from it. To extend the bank, merge new output *into* the committed file.

## concept_id precedence (verified)
`canonical_cwe` (tier1) → `cwe` (v3_llm) → `extract_cwe` (base fact) → `door:<door>`. (`v3_usecases`'
`canonical_cwe` is intentionally not consulted — it disagrees with the shipped door-fallback facts.)
