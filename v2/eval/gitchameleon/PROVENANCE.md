# Vendored upstream — GitChameleon 2.0 benchmark

This directory vendors the GitChameleon benchmark. It was previously an **embedded git clone**
(a nested `.git`), which made the parent repo want to record it as a gitlink and left our own
FactBank files untracked. The nested `.git` has been removed; the files are now first-class,
tracked members of the `v2` tree.

## Upstream
- **Repository:** https://github.com/mrcabbage972/GitChameleonBenchmark.git
- **Pinned commit:** `3a1b6045a6b2a276bd24d715589cb041f8eccb93`
- **License:** Apache-2.0 (see `LICENSE` in this directory — it is the *upstream's* license,
  not FactBank's).

To refresh the vendored copy, re-clone at the pinned commit and re-apply our added files (below).

## What is upstream vs. ours
**Upstream (do not edit):** `dataset/`, `gitchameleon/` (the benchmark package), `Dockerfile`,
`Makefile`, `poetry.lock`, `pyproject.toml`, `images/`, `LICENSE`, upstream `README.md`,
`.github/` (upstream CI).

**Ours (FactBank-specific, added on top):** `run_tests.py` (local runner — see the faithfulness
notes in `BAKE-REPORT.md` / the remediation plan), `BAKE-REPORT.md`, `FACTBANK-NOTES.md`,
`QWEN-THINKING-AUTHORITY.md`, and this `PROVENANCE.md`.

## Reproducibility note
The official benchmark evaluates in **pinned Docker environments** with Python **3.7 / 3.9 / 3.10**.
Our local `run_tests.py` historically diverged from that (see the remediation plan, WS-BENCH); any
pass@1 numbers produced by the local runner are **local-harness, provisional** and must not be
placed beside the official leaderboard without that caveat.
