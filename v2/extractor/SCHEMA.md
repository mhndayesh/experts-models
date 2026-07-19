# Canonical fact schema

There is **one** canonical fact schema — the rich lab schema the extractor produces. Every consumer
(bake, package, retrieval) reads it; the package translation lives in exactly one place
(`factbank.bank.Fact.from_row`) and is exercised by the generic adapter `experts_to_package.py`.

> **2.0 (2026-07-18):** `EXTRACTOR-2.0.md` is now canonical for the extractor/mining/retrieval pipeline;
> where anything below disagrees, 2.0 wins. Relevant here: the schema below is a **subset** of the 2.0
> schema — 2.0 adds optional `code_bad`/`code_good`/`lang` fields (code lives IN the fact) and five new
> `type` values (`INSECURE_DEFAULT`, `HABIT_REVERSAL`, `SILENT_FAILURE`, `DEPRECATED_CRYPTO`,
> `MISSING_CONTROL`) — see EXTRACTOR-2.0.md §1. Everything else on this page (IDs, version applicability,
> provenance, package projection) is unaffected by 2.0.

## Canonical (lab) row — `experts/*/facts/*.jsonl`

```jsonc
{
  "id":          "sx-<10 hex>",     // content-complete hash (see IDs below)
  "type":        "REMOVED|REPLACED|CHANGED|...",
  "subject":     "the API/behavior the fact is about",   // may be null
  "old":         "the pre-change form",                   // may be null
  "new":         "the post-change form",                  // may be null
  "truth":       "the actionable statement the model reads",
  "why_it_bites":"post-cutoff | reverses-habit | silent-failure",
  "quote":       "verbatim span from the mined source (anti-hallucination anchor)",
  "keywords":    {"from_fact": [...api names...], "associative": [...user phrasings...]},
  "lib":         "library name",
  "version":     "applicability (see below)",
  "code_bad":    "verbatim vulnerable/insecure snippet (optional, added 2.0)",
  "code_good":   "verbatim secure fix (optional, added 2.0; MUST be present if code_bad is)",
  "lang":        "code language, lowercased, or 'text' (optional, added 2.0)"
}
```

`code_bad`/`code_good`/`lang` are new in 2.0 (see EXTRACTOR-2.0.md §1) and additive/optional — a fact
is text-only, text+good, or text+bad+good; code grounding is verbatim-modulo-whitespace, never `canon()`.

Pipeline-only keys (`_repaired`, `_flags`, `_unsalvageable`) may appear on lab rows during
build/QA. They are **not part of the schema** and are stripped from anything shipped
(`Fact.from_row` drops every `_`-prefixed key; the bank-lint gate rejects them in shipped banks).

## IDs — deterministic and collision-free

`id = "sx-" + sha256(lib|version|type|subject|old|new|truth[:80])[:10]` (`extract.py:cid`).
The earlier key hashed only `type|subject|old|new`, so distinct facts with null subject/old/new
collided (19 groups, incl. a cross-library flask/hf-datasets clash). Existing banks were repaired by
`fix_dup_ids.py`; the id function now includes `lib|version|truth`, so future extractions cannot
collide the same way. **Global id uniqueness is a CI gate.**

## Version applicability

`version` should express *where the fact applies*, not a bare `multi`. Today's distribution is coarse
(4,030 `multi`, 1,072 wildcard/range/latest, 429 major-only, 0 patch-pinned). Target: a real range or
pinned set (e.g. `">=3.0"`, `"2.x"`, `"43.0"`). Improving this is tracked in the remediation plan
(WS-SCHEMA S5) — the retrieval version-filter is only as precise as this field.

## Provenance (target — WS-SCHEMA S5)

Every fact should carry immutable provenance so a claim is auditable: `source_file`, `source_url`,
`source_commit_or_date`, `extraction_model`, `source_sha256`. Current rows carry only `lib` + coarse
`version`; the mined documents live under `experts/*/sources/`, `sources_ext/`, `sources_harvested/`
(see `THIRD-PARTY-NOTICES.md`). Backfilling provenance onto the existing 5,531 facts is planned.

## Package (shipped) row — `package/factbank/facts_v2.jsonl`

The package's own dataclass is a projection of the canonical row:

```jsonc
{ "id","text","source","version","kind","meta" }
```

- `text`   ← `truth` (symbol-prefixed when the api name is otherwise absent)
- `source` ← `lib`
- `kind`   ← `"landmine"` (vs the package's older `doc|signature|example`)
- `meta`   ← `{type, subject, old, new, why_it_bites, quote, keywords}` (structure preserved)

**Never hand-write package rows.** Regenerate with `python experts_to_package.py` so the mapping stays
single-sourced. `Fact.from_row` also loads native package rows directly, so a shipped `facts_v2.jsonl`
and a raw expert bank both load without a conversion step.
