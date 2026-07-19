# Third-Party Notices

This project (the FactBank tooling) is licensed under the MIT License (see `LICENSE`).
It also incorporates or draws upon third-party material that ships inside the tracked
`v2/` tree. That material remains under its original license, as noted below. Nothing
here relicenses third-party material; the MIT license in `LICENSE` covers only the
first-party FactBank code.

---

## 1. GitChameleon 2.0 benchmark (vendored)

- **Location in this repo:** `v2/eval/gitchameleon/`
- **Upstream:** https://github.com/mrcabbage972/GitChameleonBenchmark
- **Pinned commit:** `3a1b6045a6b2a276bd24d715589cb041f8eccb93`
- **License:** Apache License 2.0 — see `v2/eval/gitchameleon/LICENSE`

The GitChameleon benchmark (problem set, harness, and hidden tests) is vendored to
run the base-vs-bank evaluation. It retains its Apache-2.0 license and attribution
to its authors. Use of this material is subject to the terms of that license,
including the notice and attribution requirements in Apache-2.0.

---

## 2. Mined upstream changelogs / migration guides (extraction sources)

The FactBank extractor builds fact banks by reading migration guides and changelogs
copied from open-source projects. These copied documents live under the directories
listed below. **Each file retains the license of the project it was copied from**
(Apache-2.0, MIT, BSD, PSF, or the project's own documentation license, as
applicable). FactBank extracts only **short verbatim quotes** (single anchor lines
used as the anti-hallucination `quote` field) into the derived fact banks; the bulk
prose is not redistributed as a work of its own.

### Source directories

- `v2/extractor/experts/*/sources/` — per-department extraction sources. Covering, by department:
  - **web** (`experts/web/sources/`): Django, React, Vue, Svelte, Tailwind CSS, Pydantic, SQLAlchemy, Express, Next.js
  - **web3** (`experts/web3/sources/`): ethers.js, web3.py
  - **security-networking** (`experts/security-networking/sources/`): cryptography, OpenSSL, Paramiko, urllib3, Volatility3, YARA-X, eBPF (BCC → libbpf)
  - **devops** (`experts/devops/sources/`): Kubernetes, Terraform (AWS provider), GitHub Actions
  - **databases** (`experts/databases/sources/`): PyMongo
  - **data-eng**, **mobile**, **systems** (`experts/*/sources/`): additional department sources as populated
- `v2/extractor/experts/gitchameleon/sources/` — changelogs for the GitChameleon library set: Django, Falcon, Flask, GeoPandas, Gradio, Jinja2, Librosa, LightGBM, Matplotlib, mitmproxy, NetworkX, NLTK, NumPy, pandas, Pillow, Plotly, and the remaining GitChameleon libraries.
- `v2/extractor/sources_ext/` — extended AI/ML sources: HuggingFace Datasets, GGUF spec, Google GenAI, LangChain, LlamaIndex, OpenAI (v1 + Responses migration), Transformers, llama.cpp.
- `v2/extractor/sources_harvested/` — harvested source bundles (CVE/security, k8s+terraform, local-AI, python-AI, web/next/react) plus a `manifest.md` describing provenance.

Each project named above is the copyright holder of its own documentation. The
respective upstream repositories carry the authoritative license text. Consult the
upstream project for the full license of any given source document.

---

## 3. Appsec expert (2026-07-18 rebuild) — new source types, not vendored here

The 2026-07-18 Extractor/Facts/Retrieval 2.0 rebuild (canonical spec:
`v2/extractor/EXTRACTOR-2.0.md`) built a new **appsec** expert
(shipped bank `v2/extractor/experts/appsec/facts/FINAL_v3.jsonl` — the v3 faceted concept→variant bank,
258 concepts (254 CWE) → 3,984 variants, 1,075 carrying a verbatim `code_bad`/`code_good` pair;
correctness- and currency-audited). It is **baked ×3 sizes (e2b/12b/26b) × both thinking editions and
published to Hugging Face + LM Studio Hub.**

Its adapters (`codeql_mine.py`, `appsec_sast.py`, `appsec_owasp.py`, `appsec_mastg.py`,
`appsec_rustsec.py`, `appsec_mine_crypto_net.py`, `appsec_mine.py`) mine source *types* not
covered by the department list above: CodeQL `.qhelp` docs + git-blob code samples, SAST
rule catalogs (Bandit, gosec), the OWASP Cheat Sheet Series, the OWASP MASTG mobile guide,
the RustSec advisory-db, NIST/RFC/Mozilla crypto-network standards, and the CWE catalog. As
of this writing that raw source material is **not copied into a tracked `sources/` directory**
in this repo (unlike the departments in §2) — it is read from an untracked local corpus. What
does land in the derived fact bank is FactBank's own extracted output: short verbatim quote
anchors as in §2, **plus, new in this pass, verbatim code snippets** (`code_bad`/`code_good`).
Each quote or snippet retains the license of the project/standard it was copied from; consult
the upstream project for the full license before any redistribution of this bank.
