# Schema v3 — Faceted Concept → Variant (the bank rebuild)

> **⚠️ As-shipped note (2026-07-19 audit).** This document is the **design**; the shipped bank
> (`FINAL_v3.jsonl`) diverged in two ways worth knowing before building on it:
> 1. **Concept records are minimal stubs.** All 258 shipped concept records are `{kind, concept_id, n}` —
>    the `lesson`/`sub_patterns` fields shown below were **never populated**, and **no retriever reads concept
>    records** (both `adapt_v3.py` and `retriever_v3.py` filter to `kind=="variant"` and route on each
>    variant's own `concept_id`). The concept records are inert routing metadata, not the designed lesson store.
> 2. **The build pipeline IS now committed & reproducible (2026-07-19).** `build_v3_assemble2.py` (the merge
>    step referenced in `build_v3_tier1.py`) was reconstructed, committed, and verified to rebuild **3630/3984
>    (91%) of `FINAL_v3.jsonl` exactly** from the now-tracked inputs (`FINAL.jsonl` + `v3_llm`/`v3_tier1`/
>    `v3_usecases`). The ~9% residual is **irreducibly lost source data** (feature_phrases from overwritten
>    `build_v3_usecases.py --sample` runs + 5 manual `CWE-367` overrides), so `FINAL_v3.jsonl` **stays
>    canonical** as the exact artifact. Full detail: `../extractor/experts/appsec/facts/REBUILD.md`.

**Decision (owner, 2026-07-18):** rebuild the bank as **concept → variant**, optimized for large look-alike data
+ the float BM25F / concept-routing retriever. Separates the **shared lesson** (concept) from the
**discriminators** (facets + typed anchors), so near-duplicate facts stop competing on shared vocabulary.

**Owner: FULL REDO authorized — "ok to waste the current bank."** Reuse the *verified content* (audited truths,
code pairs, evidence — the expensive 11M-token audit/currency work) as raw material, but **restructure freely:
dedupe aggressively, drop weak/redundant facts, do not preserve the old schema or the 3,984 count.** This lets
Option 2 (faceting) absorb Option 3's strength (collapse look-alikes within a concept).

## The core idea
The bank is thousands of facts that look alike (200+ SQL-injection facts sharing "SQL/injection/parameterize").
A **concept** holds the reusable lesson once; each fact is a **variant** distinguished by facets. Retrieval routes
to the concept (coarse) then picks the variant by facet + exact anchor (fine).

**Concept backbone = CWE** (a fixed standard taxonomy the facts already partly carry). A concept is
`CWE + optional sub-pattern`; facts with no clean CWE get a derived concept label (fallback = door).

## Structure (two record kinds in one store)

### Concept record
```json
{
  "kind": "concept",
  "concept_id": "cwe-89",
  "label": "SQL injection",
  "cwe": ["CWE-89"],
  "door": "injection",
  "lesson": "Never build SQL from string interpolation; use parameterized queries / bound params.",
  "sub_patterns": ["string-interpolation", "dynamic-order-by", "orm-raw", "stored-proc"]
}
```

### Variant record (a fact hanging off a concept)
```json
{
  "kind": "variant",
  "id": "cq-d1381ee092",
  "concept_id": "cwe-89",
  "facets": {
    "language": "java",
    "ecosystem": "maven",
    "package": "java.sql",
    "namespace": "PreparedStatement",
    "framework": null,
    "sub_pattern": "string-interpolation"
  },
  "retrieval": {
    "exact_symbols": ["PreparedStatement", "Statement.executeQuery", "setString"],
    "bad_pattern_symbols": ["Statement", "createStatement", "\"...\"+"],
    "aliases": ["jdbc sql query"],
    "query_phrases": ["fetch a row by id from a request parameter"],
    "anchor_provenance": "code_derived"       // code_derived | keyword_derived | llm_generated
  },
  "claim": {
    "type": "INSECURE_DEFAULT",
    "truth": "Use PreparedStatement with ? placeholders instead of Statement with concatenated SQL."
  },
  "examples": [
    {"role": "bad",  "language": "java", "code": "..."},
    {"role": "good", "language": "java", "code": "..."}
  ],
  "evidence": {"source": "codeql", "source_edition": "codeql", "quote": "...", "version": "multi"},
  "verification": {"status": "current", "checked_at": "2026-07-18", "audit_fix": true},
  "relations": {"bundle_id": null, "supersedes": [], "related": []}
}
```

## Facets (the discriminators — what makes look-alikes distinct)
| facet | source (build order) | example |
|---|---|---|
| `language` | existing `lang`, normalized (56→canonical enum); fill blanks from code/anchors | python, java, php |
| `ecosystem` | derived from package (pypi/maven/npm/cargo/…) | pypi |
| `package` | **code-derived first** from `code_bad`/`from_fact` (the real import/lib); LLM for gaps | torch, boto3 |
| `namespace` | the API family (dotted head) | torch.load, PreparedStatement |
| `framework` | LLM (flask/spring/express/…) or null | flask |
| `sub_pattern` | LLM against the concept's `sub_patterns` list | dynamic-order-by |

## Typed retrieval block (replaces the flat `anchors` array — audit)
- `exact_symbols` — the API a *secure/aware* dev types (matches the model's intent). **Code-derived first.**
- `bad_pattern_symbols` — the vulnerable call (matches a draft that wrote the bug).
- `aliases` — natural-language names ("pytorch checkpoint loader").
- `query_phrases` — the task a dev would ask ("load an uploaded model checkpoint").
- `anchor_provenance` — code_derived / keyword_derived / llm_generated (+ trust).

## Why this fits the retriever
- **Concept routing** (BM25F/cluster) matches the shared topic ONCE — shared vocab no longer competes.
- **Facet + exact_symbols** disambiguate the variant — precision on look-alikes.
- **language facet** = the abstention language filter (already built).
- **bundle_id** = coverage (retrieve session-fixation *and* cookie-security together).
- Concepts are the **fixed cluster ids** the IVF/routing table needs (stable, unlike numeric k-means ids).

## Build pipeline (`build_v3.py`)
1. **concept assignment** — CWE from `lib`/content (LLM for facts lacking one) → group → concept records.
2. **facets** — language (normalize `lang`); package/namespace/ecosystem (code-derived first); framework +
   sub_pattern (LLM, cheap DeepSeek batch).
3. **typed anchors** — exact/bad symbols code-derived from `code_bad`/`code_good`/`from_fact`; aliases +
   query_phrases LLM; provenance tagged.
4. **validate** — every variant links a real concept; language non-blank where code exists; anchors non-empty.
5. **emit** `FINAL_v3.jsonl` (concepts + variants) + `manifest.json` release entry.

## Acceptance
- Every look-alike group collapses under one concept; variants distinguished by facet+anchor.
- Strict failure-set retrieval (prompt-only) materially > current 5/16.
- 0 blank language where code exists; every variant has ≥1 code-derived or keyword-derived anchor.
