# The Exact Extractor — Implementation Spec

> **Superseded in part by `EXTRACTOR-2.0.md` (2026-07-18 rebuild) — where anything disagrees, 2.0 wins.**
> This doc still describes the original text-fact pipeline accurately (extract/repair/check/run for
> migration-guide facts). 2.0 adds a parallel, code-bearing mining path (shared `appsec_core.py` +
> thin per-source adapters), changes `repair_quote`'s grounding method, adds a mandatory adversarial
> correctness audit, and moves served retrieval/testing to HyDE double-key + your own `llama-server`
> (never LM Studio). See per-section notes below and `EXTRACTOR-2.0.md` for the full detail.

The precise, reproducible spec of THIS extractor (the design rationale is in `BLUEPRINT.md`).
Backend: DeepSeek `deepseek-v4-flash`, thinking OFF, function-calling. Key from `DEEPSEEK_API_KEY`
(never written into the repo). Cloud, no GPU.

---

## Files
| file | role | LLM? |
|---|---|---|
| `extract.py` | LLM fills the strict schema (function-calling) + derives type/from_fact/id in code | yes (1 call/chunk) |
| `repair.py` | snap paraphrased quotes to the real source line — **grounding method superseded by EXTRACTOR-2.0.md §3** (sentence-boundary split, longest verbatim span; RETIRES the ellipsis-only split + ≥3-word guard below) | no |
| `check.py` | raw checker — verbatim-quote anchor + field validation | no |
| `run.py` | driver: extract → repair → check | — |
| `lookup.py` | retrieval prototype (soft doors + pointers + MMR); `BANK_DIR` env selects the bank — for code-bearing (appsec) banks, served retrieval is now HyDE double-key (EXTRACTOR-2.0.md §6); `lookup.py` remains the doors+pointers+MMR algorithm reference | no |
| `refine.py` | second concrete-rewrite pass — **evidence only, NOT in the pipeline** (BLUEPRINT §rejected) | yes |

## The schema
**LLM fills** (via function-call `emit_facts(facts:[…])`):
```
type          REMOVED | REPLACED | CHANGED   (enum)
subject       the API/symbol this is about
old           the exact dead/changed symbol
new           the replacement, or null
truth         ONE concrete, actionable sentence (stop X, use Y / you now get Z) — never vague
why_it_bites  post-cutoff | reverses-habit | silent-failure   (enum)
quote         VERBATIM span copied from the source (the anchor)
associative   3-8 short phrases a dev would TYPE that are NOT in the fact (task/symptom/question)
```
**Code derives** (never trust the model for these): `type` reconciled from `new` presence · `from_fact`
keywords pulled from old/new/truth · `id = sx-<hash(type|subject|old|new)>` · `lib`, `version` stamped.

**Facts 2.0 (EXTRACTOR-2.0.md §1)** adds optional, backward-compatible fields on top of this schema:
`code_bad`/`code_good` (verbatim vulnerable/fixed snippets, `code_good` mandatory whenever `code_bad`
is present), `lang`, and new `type` values `INSECURE_DEFAULT | HABIT_REVERSAL | SILENT_FAILURE |
DEPRECATED_CRYPTO | MISSING_CONTROL`. This schema above is unchanged/still valid for text-only facts.

## Run it (one source)
```bash
DEEPSEEK_API_KEY=$(cat /path/deepseek.key) \
  python run.py <source.md> <lib> <version>
# → <lib>.facts.repaired.kept.jsonl   (the door)
```
Or stage-by-stage: `extract.py src lib ver` → `repair.py <lib>.facts.jsonl src` → `check.py <lib>.facts.repaired.jsonl src`.

## Config (exact values, in the code)
| knob | value | where |
|---|---|---|
| model / thinking | `deepseek-v4-flash` / disabled | extract.py, refine.py |
| chunk size | 3500 chars, split on blank lines | extract.py `chunks()` |
| max_tokens | 8000 (extract), 300 (refine) | — |
| quote min length | 12 chars, must be canon-substring of source | check.py |
| `old`-in-source | enforced only when `old` is a single token (symbols); prose `old` relies on quote | check.py |
| associative count | 1–8, each 1–6 words, not duplicating from_fact | check.py |
| repair snap | needs ≥1 fact-symbol in the line **and** ≥2 shared tokens | repair.py — **superseded by EXTRACTOR-2.0.md §3** (sentence-boundary split, longest verbatim span, 0.5 token-overlap fallback) |
| soft-door weight `W` | 0.8 (matching door × 1.8, never exclude) | lookup.py |
| pointer depth | 4 hops, bucket = (lib, primary-namespace) | lookup.py |
| MMR penalty | 1.2 × max-similarity-to-picked | lookup.py |

## FIND checklist (do this BEFORE extracting — the one law)
For each library, get the **migration/breaking-changes doc**, not release notes:
1. Raw GitHub first: `MIGRATION_GUIDE*.md`, `docs/…/migrat*`, `CHANGELOG.md`, deprecated-terms pages.
   `curl -o file.md <raw-url>` then `grep -iE "deprecat|removed|no longer|renamed"` to confirm it's the right doc.
2. Web-only docs → WebFetch, save the returned markdown as the source (self-consistent anchor; note it's rendered).
3. Format/spec landmines (e.g. GGUF) live in the **spec**, not the changelog.
4. Scan the fetched file for the domain's known flagship landmine before extracting.

## Build a new expert (a bank of many doors)
1. Write a coverage spec from trusted curricula → `experts/<name>/COVERAGE.md` (domains + stacks, churn-ranked).
2. FIND + extract each stack → one `.jsonl` door per lib in `experts/<name>/facts/`.
3. Merge multi-source doors by `id` (dedup). Keep banks **rich** (no model-gating). For code-bearing
   experts, cross-source dedupe is **prose-only** — a shared `code_bad` is NOT a duplicate signal
   (EXTRACTOR-2.0.md §4).
4. Test retrieval: `BANK_DIR=experts/<name>/facts python lookup.py` with domain queries; **read by hand**.

## File conventions
- One door = `experts/<expert>/facts/<lib>.jsonl`, schema-per-line.
- Intermediates (`*.facts.jsonl`, `*.repaired*`) are scratch — delete after merging into a door.
- Sources kept in `sources_ext/` and `sources_harvested/` (the harvested migration guides / changelogs, self-contained in v2).

## Standing rules
- **Score, then READ MANUALLY** — the count lies (F-065). For code-bearing (appsec) banks this is now a
  **mandatory adversarial correctness audit**, not just a manual read: verbatim grounding proves a fact is
  REAL, not CORRECT or CURRENT (~3.8% of the audited appsec bank was wrong/stale) — EXTRACTOR-2.0.md §5.
- **DeepSeek only**, key from env, never in the repo.
- **Nothing baked** until Jinja/real-engine parity passes (F-050/F-053). *(Repo-wide when written; other
  pipelines have since baked+published experts — see `CLAUDE.md`. Within EXTRACTOR-2.0.md's own scope, the
  appsec/security expert — 3,984 facts, 1,075 w/verbatim code, correctness- and currency-audited — SHIPPED
  2026-07-19: baked ×3 sizes (e2b/12b/26b) × both thinking editions and published to LM Studio Hub + HF
  (shipped bank = the v3 faceted `FINAL_v3.jsonl`, 258 concepts (254 CWE) → 3,984 variants).)*
