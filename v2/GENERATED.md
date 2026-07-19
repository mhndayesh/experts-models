# Generated-artifact manifest (`v2/`)

This file separates **SOURCE** (hand-authored, the thing you edit) from **GENERATED**
(rebuildable output that is checked in for convenience). If a generated file drifts,
delete it and re-run its producing command — do not hand-edit it.

All producing commands run from `v2/bake/template-brain-v3.1/` unless noted. Sizes are
approximate.

---

## Baked GGUF chat-templates (`v2/bake/template-brain-v3.1/`)

| Artifact | Size | Produced by |
|---|---|---|
| `gc_baked_gemma4.jinja` | ~2.73 MB | `python bake_index.py --facts gitchameleon_bank.jsonl --out gc_baked_gemma4.jinja` (inverted-index bake of the GitChameleon bank into the gemma-4 base template) |
| `secnet_baked_gemma4.jinja` | ~0.12 MB | `python adapt_secnet.py` (bank + taskwords) → `python bake_index.py --facts secnet_bank.jsonl --out secnet_baked_gemma4.jinja` |
| `appsec_v3_baked_{e2b,e2b_off,e2b_think,gemma4,gemma4_off,gemma4_think}.jinja` | — | v3 faceted appsec bank (`FINAL_v3.jsonl`) baked per size (e2b / 12b-26b `gemma4`) × edition (`_off` thinking-OFF, `_think` thinking-ON). **Gitignored / regeneratable** — rebuild from the v3 bank via the bake route; the shipped security expert (2026-07-19) uses these. |

> **Dedup note (2026-07-16):** `gc_baked.jinja` was removed. It was **byte-identical**
> (`cmp`-verified, 2 729 945 bytes) to `gc_baked_gemma4.jinja`, which is the canonical
> name. Regenerate with the command above; do not recreate the `gc_baked.jinja` alias.

## Adapted bank + taskword indexes (`v2/bake/template-brain-v3.1/`)

| Artifact | Produced by | From |
|---|---|---|
| `gitchameleon_bank.jsonl` | `python adapt_gc.py` | `v2/extractor/experts/gitchameleon/facts/*.jsonl` |
| `gitchameleon_taskwords.json` | `python adapt_gc.py` | same |
| `secnet_bank.jsonl` | `python adapt_secnet.py` | `v2/extractor/experts/security-networking/facts/*.jsonl` |
| `secnet_taskwords.json` | `python adapt_secnet.py` | same |

`adapt_*.py` map an expert fact bank into the `bake_index.py` schema: `*_bank.jsonl`
is what the model reads; `*_taskwords.json` is the search index (from_fact +
associative keywords) kept out of the injected text.

## Intermediate extraction outputs

> **Superseded pipeline note (2026-07-18):** the `extract → repair → check` /
> `repair.py` pipeline described below is the **v1** mining pipeline (still what
> produced the GitChameleon and secnet banks baked above). New experts (e.g. `appsec`,
> 3,984 facts — SHIPPED 2026-07-19 as the v3 faceted bank `FINAL_v3.jsonl`, baked ×3
> sizes × both thinking editions and published) are mined by the **2.0** pipeline instead —
> one shared `appsec_core.py::run()` plus thin per-source adapters, with
> sentence-boundary verbatim repair and a mandatory adversarial correctness audit. See
> `v2/extractor/EXTRACTOR-2.0.md` (canonical) for the current method; where it
> disagrees with this section, 2.0 wins.

- `*.facts.repaired.kept.jsonl` — per-source intermediate outputs of the v1 extractor
  pipeline (`extract → repair → check`), where `repair.py` re-grounds paraphrased
  quotes and the checker keeps the survivors. These are GENERATED from the
  corresponding `sources/` document and are safe to delete/regenerate. *(None are
  currently checked in under `v2/`; the pattern is listed so future intermediates are
  recognized as rebuildable, not source.)*
- The per-library fact banks under `v2/extractor/experts/*/facts/*.jsonl` are the
  extractor's product (LLM-extracted from the matching `sources/` document). They are
  the durable curated banks the adapters consume; treat them as reviewed output rather
  than hand-source.

---

## SOURCE (edit these; not generated)

- `bake_index.py`, `adapt_gc.py`, `adapt_secnet.py` — the producers above.
- `v2/bake/template-brain-v3.1/family_bases/*.jinja` — the un-baked base chat-templates
  the bake is injected into.
- `v2/bake/template-brain-v3.1/inserts/**` — the Jinja insert fragments composed into a
  baked template.
- `v2/extractor/experts/*/sources/**`, `v2/extractor/sources_ext/**`,
  `v2/extractor/sources_harvested/**` — the mined upstream docs (see
  `THIRD-PARTY-NOTICES.md`).

---

## Not tracked at all

The **shipped GGUF model files** (the gemma-4 12b / 26b GGUFs with a baked template)
live **outside this repo**, under the user's LM Studio models directory
(`~/.lmstudio/models/…`). They are large binaries and are **not** checked in. Rebuild
one by baking a template (above) into the base GGUF via `bake_index.py`'s
`--src-gguf` / `--dst-gguf` route.
