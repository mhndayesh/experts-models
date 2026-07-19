# GitChameleon expert — coverage & targeting

Bank purpose: give the base Gemma models ([[ai-ml-expert-base-models]] — gemma-4-12b-qat,
gemma-4-26b-a4b-qat, gemma-4-e2b) the **version-specific API facts** they need to pass
**GitChameleon 2.0** (`v2/eval/gitchameleon`, 328 problems, 26 libraries, execution-scored).

Unlike the AI-ML expert (where we hunted migration guides blind), here **the benchmark hands us the
targeting**: `targeting.json` (built from the dataset) lists, per library, the exact versions, changed
APIs (`name_of_class_or_func`), change types, and doc URLs. That is the "one law" (source targeting)
solved. We still mine **independent official changelogs** (not the dataset's own answers) so the bank
is earned, not teaching-to-the-test — same as the paper's doc-RAG baseline.

## Sources harvested (FIND phase — done, in `sources/`)
One `<lib>.changelog.md` per library, pulled from official changelogs / release notes / release-API
bodies, concatenated across the versions the dataset needs. **316/328 problems well-sourced.**

| tier | libs | note |
|---|---|---|
| solid (24 libs, 316 problems) | librosa, scipy, sympy, flask, falcon, torch, numpy, scikit-learn, pandas, django, mitmproxy, networkx, pytest, plotly, geopandas, seaborn, tornado, gradio, nltk, matplotlib, pillow, jinja2, spacy | full changelogs |
| **weak — revisit** | lightgbm (9 probs), tqdm (2) | GitHub release bodies were near-empty; need a better source (docs/milestones) |
| **missing** | kymatio (1 prob) | no changelog file found; low value (single problem) |

Big changelogs (gradio 798 KB, torch 607 KB, pytest 489 KB, scipy 426 KB, pandas 263 KB, pillow 199 KB)
should be **trimmed to the dataset's version sections** before extraction — otherwise we mine 800 KB of
gradio for 7 problems. Rich is good, but scope to the relevant releases.

## Extraction — DONE (2026-07-15): 4,167 facts, 23 doors, 100% grounded
Mined all 24 solid libraries; QC recovered +901 facts after fixing 3 extractor bugs (see PROGRESS §8).
Reachability 69.6% w/hint, 94.5% door purity (`reach.py`). Full write-up:
`../../../eval/gitchameleon/BAKE-REPORT.md` (the bake + live-score report; the older pre-bake `REPORT.md`
was archived to `archive/superseded-docs/REPORT.md`).
Live base-vs-expert pass@1 is DONE (baked into 12b + 26b GGUFs, execution-scored): 12b 37.8%→44.2%,
26b 43.4%→46.2%. The current scorer is `../../../eval/gitchameleon/run_tests.py` (the old served-loop
`gen.py` was archived to `archive/superseded-scripts/gen.py`). See BAKE-REPORT.md.

## Known design note — version stamping
`run.py` stamps ONE `version` per run, but each library spans several benchmark versions (e.g. flask
2.0.0 / 3.0.0). The changelogs are version-sectioned, so each fact's `quote` carries its version header.
For the eval's version-conditioned retrieval we may need per-fact version precision — flagged for the
retrieval-wiring step, not a blocker for extraction. Retrieve-first / filter-second / fail-open still holds.
