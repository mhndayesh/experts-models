# FactBank — Expert Departments (catalog & roadmap)

*What experts can we build, and which are worth building first?* An "expert" is a fact bank for one
domain's fast-moving stack. This catalogs the departments, the candidate experts in each, where their
facts live, and how landmine-rich (therefore how valuable) each is.

> **Mining/repair/dedupe/verification/retrieval method note (2026-07-18):** the pipeline referenced below
> (FIND → extract → repair → check) is now superseded by **`../EXTRACTOR-2.0.md`** — shared
> `appsec_core.run` + thin per-source adapters, code-in-fact (`code_bad`/`code_good`), sentence-boundary
> repair, prose-only cross-source dedupe, and a MANDATORY adversarial correctness audit on top of currency
> verification. Where this doc's pipeline description disagrees, 2.0 wins.

## What makes a domain a good expert (the value function)
A bank is worth building where the model is **most likely to be wrong**. That is highest when a domain has:
- **Fast release cadence** — multiple breaking versions since the model's cutoff.
- **Habit reversals** — renames, moved imports, flipped defaults (the model "knows" the old way and reverts — see the thinking findings; these are the facts that pay off most).
- **Silent failures** — wrong-but-runs behavior (no error to self-correct against).
- **A mineable source** — an official **migration guide / changelog / upgrade doc** (the one law: source targeting decides everything). *No prose changelog → no bank* (why `kymatio`/`lightgbm`/`tqdm` are uncoverable).

**Landmine density (LD)** below is a rough 1–5 rating of expected facts-that-bite per library. **Priority**
weighs LD × audience size × how post-cutoff the churn is.

## Built so far
| expert | doors/libs | facts | status |
|---|---|---|---|
| **AI-ML** | 11 (openai, langchain, llamaindex, transformers, vllm, pydantic, llama-cpp, hf-datasets, langgraph, anthropic, google) | 817 | built, not yet baked/scored |
| **GitChameleon (Python scientific/web)** | 23 (torch, pandas, scipy, sklearn, pytest, gradio, pillow, django, flask, sympy, networkx, numpy, plotly, seaborn, matplotlib, geopandas, librosa, mitmproxy, falcon, nltk, tornado, jinja2, spacy) | 4,167 | built, **baked + benchmarked** (12b +6.4, 26b +2.8) |
| **Web** (merge of frontend+backend) | 9 (tailwind v4, pydantic v2, react 19, svelte 5, vue 3, sqlalchemy 2.0, django 5, express 5, nextjs 15) | 279 | **built 2026-07-16**, checked (0 issues). Not yet baked/scored. `web/COVERAGE.md` |
| **Security & Networking** (`netsec`) | 7 (cryptography, openssl 3, paramiko 3, urllib3 v2, volatility3, yara-x, ebpf BCC→libbpf) | 114 | **built + baked ×3 + tested + PUBLISHED** (HF+GH, gate-alias fix, 2026-07-17). 3-size curve (48 Qs, thinking-ON + authority): e2b 19→32, 12b 27→39, 26b 37→45 /48. Old pre-fix bake tagged `v1-pre-gate-fix`. Docs: `security-networking/README.md`. |
| **Offensive Security + RE** (`offsec`) | 17 (angr, ldap3, capstone, netexec, pwntools, nuclei, responder, impacket, volatility3, frida, unicorn, plaso, certipy, yara-x, dnfile, bloodhound-py, pefile) | 489 | **built + baked ×3 + tested + PUBLISHED** (2026-07-17, gate-fixed). Hand-scored (thinking-ON + authority): e2b 12→37, 12b 12→43, 26b 17→43 /44. `offensive-security-re/`. |
| **eBPF / Networking Data Plane** (`dataplane`) | 7 (libbpf, cilium, frr, ebpf, dpdk, xdp/libxdp, vpp) | 318 | **built + baked ×3 + tested + PUBLISHED** (2026-07-17, gate-fixed). Hand-scored: e2b 5→32, 12b 16→41, 26b 20→43 /47 (~3 12b regressions, reported). `ebpf-dataplane/`. |
| **DevOps** | 3 (kubernetes deprecations, github-actions, terraform-aws v5) | 74 | **built**, checked. k8s gold (proven 96.5%). Next: ansible/docker/helm. |
| **Databases** | 1 (pymongo 4) | 32 | **built**, checked. Next: psycopg 3 (403'd), redis-py, alembic. |
| **Web3** | 2 (ethers v6, web3.py) | 48 | **built**, checked. Next: OpenZeppelin 5 (404'd), viem, solidity. |
| **Appsec** (code-in-fact) | 7 sources (CWE, CodeQL, SAST/Bandit+gosec, MASTG, RustSec, crypto-net NIST/RFC/Mozilla, OWASP Cheat Sheets) | 3,984 variants (1,075 w/verbatim `code_bad`/`code_good`) | **SHIPPED** — shipped bank `FINAL_v3.jsonl` (258 concepts (254 CWE) → 3,984 variants); baked ×3 sizes × both thinking editions, published to HF + LM Studio Hub. Method + audit results: `../EXTRACTOR-2.0.md`. |

**Totals (banks built):** the original 22 new banks (547 facts) plus the deepened **offsec (489)** and
**dataplane (318)** security experts, on top of AI-ML (817) and GitChameleon (4,167), plus the **appsec**
expert (`FINAL_v3.jsonl`, 258 concepts (254 CWE) → 3,984 variants, audited, SHIPPED). **Three security
experts — netsec / offsec / dataplane — are baked into GGUFs at all 3 sizes, hand-scored base-vs-bank, and
published to Hugging Face + GitHub with the gate-alias fix** (9 model repos in one collection). **Appsec is
also SHIPPED** — baked ×3 sizes × both thinking editions, published to HF + LM Studio Hub. Web, AI-ML,
DevOps, Databases, and Web3 remain built-but-not-yet-baked.

**Policy (owner call 2026-07-16): landmine-only, no fundamentals.** Full landmine banks; fundamentals were
dropped per owner direction (and aligned with LIMITS.md §1 recall-decay / §8 signature-facts-lose).

---

## The departments (candidate experts)

> **Merges (owner call, 2026-07-16):** **Networking + Cybersecurity → one "Security & Networking"
> department**; **Frontend + Backend → one "Web (full-stack)" department**. Rationale: they share an
> audience and ship as one bundle. Sub-sections below are kept for source-targeting clarity but bake
> together.

### 1. Frontend — **highest priority** (extreme churn, huge audience)
The fastest-moving, most habit-reversal-heavy domain. Framework majors break constantly and the model's
training is always stale here.
| expert | libraries | source | LD |
|---|---|---|---|
| React ecosystem | react 18→19, react-dom, hooks rules, RSC | react.dev "Upgrading" + blog | 5 |
| Next.js | 13→14→15 (app router, server actions, caching flips) | nextjs.org upgrade guides | **5** |
| Vue/Nuxt | vue 2→3 (Composition API), nuxt 2→3 | vuejs migration guide | 5 |
| Svelte | svelte 4→5 (runes — total reversal) | svelte.dev migration | 5 |
| Tailwind | 3→4 (config→CSS, renamed utilities) | tailwind upgrade guide | 4 |
| Build tools | vite, webpack 4→5, esbuild | per-tool migration | 3 |
| Angular | standalone components, signals | angular.dev update guide | 4 |

### 2. DevOps / Infrastructure — **high priority** (proven mineable: k8s 96.5%)
| expert | libraries | source | LD |
|---|---|---|---|
| Kubernetes | apiVersion churn, removed APIs | k8s deprecation guide (proven 96.5%) | **5** |
| Terraform | provider major bumps (aws, azurerm, google) | provider upgrade guides | 5 |
| Docker/Compose | compose v1→v2, buildx | docs upgrade notes | 3 |
| Helm / Ansible | helm 2→3, ansible collections split | changelogs | 4 |
| Cloud SDKs | boto3, google-cloud-*, azure-sdk | per-service changelogs | 4 |
| CI | GitHub Actions (node20, deprecated set-output) | GH changelog | 4 |

### 3. Cybersecurity — **high priority** (fast tooling, silent-failure heavy, CTF/pentest audience)
| expert | libraries/tools | source | LD |
|---|---|---|---|
| Offensive Python | impacket, pwntools, scapy, requests-oauthlib | project changelogs | 4 |
| Forensics/IR | volatility3 (v2→v3 total rewrite), yara-python | migration docs | 5 |
| Detection-as-code | Sigma (schema versions), Suricata rules, Semgrep | rule-schema changelogs | 4 |
| Cloud security | prowler, checkov, trivy (check IDs churn) | release notes | 4 |
| Web/appsec | burp extension API, OWASP ZAP API, sqlmap flags | API docs | 3 |
> Dual-use note: keep this to **defensive / authorized-testing / CTF** framing — API-correctness facts,
> not exploit payloads.
>
> **Update (2026-07-18):** a large "real security expert" covering the code-vulnerability side of this
> department (CWE, CodeQL, SAST/Bandit+gosec, MASTG, RustSec, crypto-net standards, OWASP Cheat Sheets) is
> already **built, audited, and SHIPPED** (baked ×3 sizes × both thinking editions, published to HF + LM
> Studio Hub) — 3,984 variants, 1,075 carrying verbatim `code_bad`/`code_good`
> pairs in the fact itself (no separate code search). Mined via the new shared `appsec_core.run` pipeline,
> not the per-source candidates listed above. See `../EXTRACTOR-2.0.md` and the "Built so far" table.
> The tooling-changelog candidates above (impacket/pwntools/volatility3/etc.) remain open — they overlap
> with the already-published `offsec`/`dataplane`/`netsec` experts and are not superseded by appsec.

### 4. Networking — medium-high (automation stacks churn; niche but sticky audience)
| expert | libraries | source | LD |
|---|---|---|---|
| Network automation | netmiko, napalm, nornir, ncclient | project changelogs | 4 |
| Packet/protocol | scapy, dpkt, pyshark | changelogs | 3 |
| Vendor SDKs | Cisco (pyATS/genie), Juniper PyEZ, Meraki/DNAC APIs | SDK release notes | 4 |
| IaC networking | terraform network providers, cloud VPC APIs | provider guides | 4 |

### 5. Backend / Web frameworks — high (overlaps GitChameleon on Python; extend to other langs)
| expert | libraries | source | LD |
|---|---|---|---|
| Python web | FastAPI, Django, Flask, SQLAlchemy 1.4→2.0, Pydantic 1→2 | migration guides (pydantic proven 97.8%) | **5** |
| Node backend | Express 5, NestJS, Prisma, Drizzle | upgrade guides | 4 |
| JVM | Spring Boot 2→3 (jakarta namespace), Hibernate | spring migration guide | 5 |
| Ruby/PHP | Rails, Laravel major bumps | upgrade guides | 4 |

### 6. Databases / Data engineering — medium-high
| expert | libraries | source | LD |
|---|---|---|---|
| Python DB | SQLAlchemy 2.0, psycopg 2→3, redis-py, pymongo | migration guides | 5 |
| Data platforms | Spark (PySpark API), dbt, Airflow 1→2→3 (huge) | upgrade docs | 5 |
| Vector/newSQL | pinecone/weaviate/qdrant clients, duckdb, polars | changelogs | 4 |

### 7. Mobile — medium (fast but smaller overlap with our tooling)
| expert | libraries | source | LD |
|---|---|---|---|
| iOS | SwiftUI (yearly API churn), Swift concurrency | Apple release notes | 4 |
| Android | Jetpack Compose, Kotlin coroutines | AndroidX release notes | 4 |
| Cross-platform | React Native (new arch), Flutter, Expo | migration guides | 4 |

### 8. Systems languages — medium
| expert | libraries | source | LD |
|---|---|---|---|
| Rust | tokio, serde, axum, edition churn | crate CHANGELOGs | 4 |
| Go | modules, generics-era libs, stdlib | release notes | 3 |
| .NET | EF Core, ASP.NET major bumps | MS upgrade docs | 4 |

### 9. Web3 / Blockchain — medium (extreme churn, niche)
| expert | libraries | source | LD |
|---|---|---|---|
| EVM tooling | ethers.js 5→6, web3.py, viem, hardhat/foundry | migration guides | 5 |
| Contracts | solidity version breaks, OpenZeppelin 4→5 | changelogs | 5 |

### 10. Game / graphics / ML-infra — lower priority (smaller audience or thin changelogs)
Unity/Unreal/Godot API churn (5), but sources are release-note-heavy not migration-guide-clean; harder to mine.

---

## How many experts, realistically?
- **Immediately mineable (clean migration guides):** ~40–50 individual library experts across departments
  1–6. These are the ones the proven pipeline (FIND migration guide → extract → repair → check) handles
  today, at ~4¢/library of DeepSeek cost.
- **Bundle strategy:** ship **department bundles** (e.g. one "Frontend" GGUF bake), not per-library — the
  bake and retrieval scale fine (size wall is overcome; a 2.73 MB, 4k-fact template already ships).
- **The gate is source targeting, not extraction.** Any library with a real upgrade/migration doc is
  buildable; any without one (thin changelogs, marketing release notes) is not — mine the doc first.

## Recommended first three (after AI-ML/GitChameleon)
1. **Frontend (React + Next.js + Tailwind + Svelte 5)** — highest churn × largest audience; the domain
   where models are *most* wrong.
2. **DevOps (Kubernetes + Terraform + GitHub Actions)** — k8s already proven 96.5%; enterprise value.
3. **Python backend (Pydantic 2 + SQLAlchemy 2 + FastAPI)** — pydantic already proven 97.8% clean; extends
   GitChameleon into the everyday web stack.

> **Cross-links:** language/tooling coverage decisions live in `../../decisions/LANGUAGES.md`; the
> proven extraction pipeline was `../BLUEPRINT.md` — **superseded by `../EXTRACTOR-2.0.md`** (2026-07-18
> rebuild: shared-core mining, code-in-fact, sentence-boundary repair, prose-only dedupe, mandatory
> adversarial audit, HyDE double-key retrieval); retrieval/serving limits in `../../serving/LIMITS.md`.
> The thinking findings (`../../eval/gitchameleon/QWEN-THINKING-AUTHORITY.md`) mean each department bank can
> serve reasoning-native models too, via authority framing — 2.0 reconfirms authority-framing +
> thinking-ON as the default retrieval posture (§6 of EXTRACTOR-2.0.md).
