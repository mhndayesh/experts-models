# Card-Mining Blueprint — plan of record (2026-07-15)

The decision document for the **fact-making** chapter. Every number here is traceable to
[`CARD-MINING-FINDINGS.md`](CARD-MINING-FINDINGS.md); the runnable pipeline is **archived** (this rules
chapter was superseded by the LLM-first `v2/extractor/`) in
`archive/pre-v2-2026-07-15/card-mining/` (in the project's full archive, not included in this repo; untracked
legacy). This is the sibling of `PACKAGING-BLUEPRINT.md` (serving)
and `FACTBANK-SHIPPING-BLUEPRINT.md` (delivery) — it covers **how facts are MADE**.

## 1. What is settled (measured, not assumed)

- **Signature mining is dead for landmine facts.** `mine_api.py` emitted call signatures;
  F-065 measured them winning **zero** cases. It is SUPERSEDED (header marked), not deleted —
  it built the shipped bank and is the reference for introspection mining.
- **The winning fact is a landmine:** *"X is dead, use Y"* / *"behaviour changed, you now
  get Z."* Post-cutoff, reverses an old habit, or fails silently.
- **The card pipeline works end to end.** A changelog becomes a served, auto-retrieved,
  winning fact. Proven on Ecto (Elixir): **4/5 unambiguous served wins on the real
  `gemma-4-12b` GGUF**, clean data. The 5th case (`literal`) is a borderline question with
  two valid answers — not a failure.
- **The method:** rules propose, code disposes, the LLM touches only the ~10% where meaning
  is needed (dedup, subject, natural triggers), a code guard re-verifies it, a human reads
  the verdict. No automated scorer is ever the verdict (F-065).

## 2. The pipeline (archived in `../../archive/pre-v2-2026-07-15/card-mining/`)

```
changelog → card_miner*.py → card_gate*.py → llm_secondline*.py (dedup/subject)
          → llm_expand_cards.py (natural triggers) → card_to_bank.py (adapter)
          → bake_index.py (into a GGUF) → serve → win
```

| stage | tool | engine | trust |
|---|---|---|---|
| mine | `card_miner*.py` | rules | verbatim quote, no LLM |
| gate | `card_gate*.py` | rules | triage; quote is the safety anchor |
| dedup / subject | `llm_secondline*.py` | DeepSeek v4-flash | code-guarded |
| natural triggers | `llm_expand_cards.py` | DeepSeek v4-flash | short/distinct filter |
| adapter | `card_to_bank.py` | code | card → bank JSONL + taskwords |
| bake | `bake_index.py` | code | inverted index in the template |
| verdict | `test_win_ecto.py` | the loaded model | HAND-scored |

Two library profiles proven: pandas (RST) and Ecto (Elixir/markdown). Retargeting to a new
library = a new `card_miner`/`card_gate` symbol grammar + markdown/RST cleanup.

## 3. Card contract

`{id, type(REPLACE|CHANGED|GOTCHA|ERROR|RECIPE|SIGNATURE), lib, version, subject, truth,
source, tier, quote, triggers{old_symbols,error_texts,task_words,code_tokens}}`
- **quote** = verbatim source line → the gate verifies the claim (the safety rule the
  original "cards" zip-plan dropped).
- **id** = hash of `type|subject|version|truth` → two claims can't collide.
- **truth** must be CONCRETE (*"you get `%{id: nil}`"*), not abstract (*"behaviour changed"*)
  — measured: abstract loses, concrete wins.

## 4. What is DONE vs OPEN

**Done & proven:** miner + gate (2 profiles), DeepSeek second-line + expansions, the
`card_to_bank` adapter, bake into a real GGUF, offline retrieval 5/5, served 4/5. Code saved,
findings recorded, `mine_api.py` superseded.

**Open (ranked, none blocks the proven result):**
1. **`parity.py` as a standing gate** — offline retrieval is jinja2; the `literal` case showed
   jinja2 ≠ the real engine (F-050). Run parity on every bank before shipping.
2. **LLM noise-tag** (developer-facing vs internal) — 4/60 Ecto cards were bug fixes. Can't
   keyword-filter (deletes real facts, F-064); needs a tag pass.
3. **Abstract→concrete rewrite** — 18/60 truths are vague; an LLM rewrite pass.
4. **Miner subject-selection** — 1 real fact (`:pool_timeout`) dropped for a foreign subject.
5. **Scale** — proven on 1 library end-to-end; repeat across the target library set.

## 5. Productionization path (proposed — owner decision)

The card pipeline MAKES facts; it does not yet feed the **shipped** bank/serve path. To make
it production:
1. **Integrate** `card_to_bank.py` output into the real bank JSONL + the `bake_index.py`
   shipping route (not the demo GGUF) — the adapter exists; wire it to the shipped model.
2. **Gate every bank** with gold + `parity.py` + reachability before it ships (the existing
   three gates, now mandatory for card banks too).
3. **Choose delivery:** the same routes as the FactBank shipping blueprint (Hub `model.yaml`
   / llama.cpp / raw GGUF ≤950 KB). Ecto's bank is 89 KB — any route.
4. **Decide the model line name** for card-derived banks (memory: `<domain>factbank`).

Nothing production-shaped ships until the owner picks from this §5.

## 6. What this SUPERSEDES / does NOT touch

- **Supersedes:** `mine_api.py` for making landmine facts (marked in its header).
- **Does NOT touch or replace:** the shipped bank (`facts_pythondata_v4.jsonl`), the serving
  architecture, the template-brain retrieval work, the evidence base
  (`archive/docs/FINDINGS.md`, `archive/docs/RESULTS.md` — moved there 2026-07-15), the
  `papers/`, or the factbank research models. Those are the EVIDENCE BASE and the current
  production — card-mining is a **new fact-making chapter added alongside them**, not a
  rewrite of them.

## 7. Demo artifacts (safe to remove)

- `.lmstudio/models/card-mining/gemma-4-12b-ecto-cards-v2` — the current clean demo (keep for
  the served-test reference, or remove after).
- `gemma-4-12b-ecto-cards-demo` (v1, junk text) — SUPERSEDED by v2; removed 2026-07-15.
