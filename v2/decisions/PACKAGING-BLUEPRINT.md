# PACKAGING BLUEPRINT — factbank

**Date:** 2026-07-13 · **Status:** DECISION DOCUMENT (nothing here is
built beyond what says BUILT) · **Owner decides; each option ends in a
decision box.** Every number in this file is measured and traceable to
`FINDINGS.md` / `RESULTS.md`.

---

## 0. What we are packaging (the inventory — all BUILT, all measured)

The product is the **sealed loop**, not the model: an OpenAI-compatible
endpoint that wraps ANY local model with the fact bank.

| piece | state | proof |
|---|---|---|
| `factbank` python package v0.1.0 (serve / check / watch / review / mine / bake) | BUILT, 24 offline tests | test_pkg.py |
| Sealed-loop endpoint (draft → double-key retrieve → native channel → refine) | LIVE at :8000 | acceptance: **USES 0.89 / CODE 0.75 / WRONG 0.11** vs bare 12B 0.44 / 0.00 / 0.33 (RESULTS §7) |
| Three backend modes: LM Studio upstream · spawned llama-server (`--gguf`) · mock | BUILT; upstream+spawn live-proven | DONE gate 2026-07-13; NuExtract/bake tests used spawn |
| Retrieval: BM25∪embeddings hybrid, int8-768 cache (4x smaller, warm boot 0.00s) | BUILT, calibrated | F-034, F-039 |
| Gates v3 (quote verbatim / anchor+quote-span / schema / collision) | BUILT; 72% pass, 0 bad facts ever entered | F-038 |
| Auto-updater (PyPI→GitHub→extract→gate→snapshot→apply→rollback), full-auto default | BUILT, live-proven | fact auto-extracted from a real release answered a question same day |
| Self-extraction rule: served model = extractor (think OFF) | DECIDED + wired | F-036/F-037 |
| Calibration: entry bar + thresholds all measured | DONE | F-039 |
| Baked one-file GGUF + `factbank bake` | BUILT, smoke-PASS, **REJECTED for serving** (~6k-token tax per request) | F-040 |
| Bank: 94 facts, 361 B/fact raw; 10k facts ≈ 7.9MB index | measured | F-034 |

**Runtime deps:** python ≥3.11, `numpy`, `rank_bm25` (+ optional `gguf`
for bake). Embedder required: nomic-embed-text-v1.5 (via LM Studio or a
spawned embedding server).

---

## 1. The problem packaging must solve

A stranger with a PC must get from *download* to *asking a question and
getting a fact-correct answer* with as few decisions as possible. Five
sub-problems, every option below is scored on them:

1. **Code delivery** — how they get factbank.
2. **Model delivery** — 6.5–7.2GB GGUF: bundled, fetched, or theirs?
3. **Chat surface** — what they type into. (Hard constraint discovered
   today: **LM Studio's own chat UI cannot point at an external
   endpoint** — anyone using our loop needs a different chat window.)
4. **Update flow** — bank freshness (auto-updater is built and on).
5. **Failure surface** — what breaks on THEIR machine that didn't on
   ours (all four traps below are things that actually bit us):
   - LM Studio idle-TTL evicts the model → endpoint 503s until reload
     (guard recovers cleanly; measured).
   - **Model reload resets the thinking toggle** → extraction budget
     silently burns (F-035 amendment; loud `Truncated` now, but it
     still stops updates until the user flips the toggle).
   - GPU variance: our llama.cpp build is Vulkan (AMD box). NVIDIA
     users want CUDA builds; CPUs work but slow (measured: 12B on CPU
     ≈ 125s for one short answer).
   - Windows-only so far. Linux/mac never verified (open backlog).

---

## 2. The delivery channels, ranked by evidence

| channel | facts per request | measured quality | verdict |
|---|---|---|---|
| Sealed loop (retrieve-then-refine) | only relevant ones (k≤5) | 0.89/0.75 | **the product** |
| Baked GGUF (all facts in template) | ALL 94 (~6k tokens) every time | smoke-pass only; exam stopped | demo/gift artifact only (owner call, F-040) |
| Bare model | none | 0.44/0.00 | the control |

Everything below packages the **sealed loop**.

---

## 3. OPTION A — "The Folder": one self-contained ZIP, no LM Studio

**Audience:** anyone. **This is the "normal clerk" answer.**

```
factbank-win64/
├── start.bat                  <- double-click. that's ALL.
├── factbank/                  <- embedded python env OR single exe
├── llama/llama-server.exe     <- bundled llama.cpp (per-GPU builds, see A3)
├── models/
│   ├── gemma-4-12B-QAT-Q4_0.gguf     (6.5GB — see decision A2)
│   └── nomic-embed-text-v1.5.Q8_0.gguf (~80MB)
├── bank.jsonl                 <- starter bank (94 facts) + auto-updates
├── factbank.toml              <- prewired: gguf mode, port 8000
└── README.txt                 <- 10 lines max
```

`start.bat` → `factbank serve --gguf models\gemma... --embed-gguf
models\nomic...` → spawns both servers on private ports, health-waits,
builds the index cache on first boot (needs ~30s once; 0.00s after),
serves `http://localhost:8000`. Spawn/teardown code is BUILT and was
battle-tested today (NuExtract + bake smokes, incl. orphan-kill).

**What still must be built/decided (A1–A5):**
- **A1 Chat surface.** The folder serves an API, not a chat window.
  Cheapest complete answer: a minimal `/chat` web page served by
  factbank itself (loopback-only, ~200 lines, plain HTML+fetch — the
  `/admin` page pattern already exists). Then the README says: run
  start.bat, open `localhost:8000/chat`. Zero third-party UI. [size M]
- **A2 Model shipping.** (a) bundle the GGUF → ~7GB download, zero
  steps, **check gemma redistribution license first** (flag: gemma
  weights carry use terms; llama.cpp is MIT, nomic is Apache-2 — only
  gemma needs a license read); (b) fetch-on-first-run from HF → 300MB
  download + resumable fetch code [size S] + first run needs network;
  (c) bring-your-own-GGUF → back to decisions. Recommend (b) with (a)
  as a torrent/alt link.
- **A3 GPU builds.** Ship 2–3 llama.cpp variants (Vulkan = universal
  fallback incl. AMD; CUDA for NVIDIA; CPU-only) and pick at first run
  by probing. Vulkan-only is an acceptable v1 (works everywhere with a
  GPU driver, slower than CUDA on NVIDIA). [size S–M]
- **A4 Python embedding.** Two routes: embeddable CPython + venv in
  the folder (simple, ~60MB, no compile) vs PyInstaller single exe
  (smaller-looking, but antivirus/SmartScreen flags unsigned exes —
  real risk for "normal clerk" users). Recommend embeddable python;
  it's boring and debuggable. [size S]
- **A5 First-boot UX.** Cache build + model load ≈ 30–60s the first
  time. start.bat must SAY that ("first start takes a minute"). [size XS]

**Failure surface:** immune to BOTH LM Studio traps (no LM Studio).
Thinking control is ours (request-side; gemma template defaults think
OFF without the flag — verified in the bake test). Port 8000 conflict →
config. Antivirus on bat+exe → A4 choice matters.

**Update flow:** already full-auto (watch on the bundled bank; "update
your facts" in chat works today).

> **DECISION BOX A:** ship it? A2 model delivery (a/b/c)? A1 include
> `/chat` page? A3 Vulkan-only v1 or multi-build?

---

## 4. OPTION B — "The Sidecar": for people who already run LM Studio

**Audience:** LM Studio users (the machine this was built on).
**State: this ALREADY EXISTS** — it is exactly the live deployment
(`C:\Users\mhnda\factbank\`): venv + factbank.toml + start-factbank.bat;
LM Studio hosts the models, factbank wraps them at :8000.

**To make it shippable:** zip the pattern with an `install.bat` that
creates the venv, installs the wheel, writes a default toml [size S].
User steps: install LM Studio → download 2 models → load them → run
install.bat → run start-factbank.bat → chat at :8000 *from a non-LM
Studio client* (A1's `/chat` page solves this here too).

**Failure surface (all measured, all today):** TTL eviction (503 until
reload — tell users to disable TTL); **thinking-toggle reset on every
reload** (extraction stalls loudly); user must load the exact model ids
the toml names. This option inherits every LM Studio trap and adds a
manual model-management burden the Folder doesn't have.

**Honest role:** power-user mode and OUR dev rig — not the flagship.
It's also free: it exists today.

> **DECISION BOX B:** keep as documented power-user mode only, or
> polish the installer?

---

## 5. OPTION C — "The Package": pip/pipx for developers

**Audience:** developers. `pipx install factbank` → `factbank serve
--gguf ~/models/x.gguf` or against LM Studio/llama.cpp they already run.

**State:** the wheel is BUILT and installs clean (DONE gate passed in a
fresh venv). Missing for PyPI: README/quickstart, starter-bank download
command, name check on PyPI, version/tag discipline, Linux CI pass
[size M total]. This is the smallest-work public artifact and the
natural home for `bake`, `watch`, `mine` power tools.

> **DECISION BOX C:** publish to PyPI (public) or keep private wheel?

---

## 6. OPTION D — Container / server

Docker+compose for homelab/server people. GPU passthrough on Windows/
ROCm is the pain we already know (rocm-smi doesn't even work in WSL
here). Real value only after Linux verification. **Recommend: PARK.**

## 7. OPTION E — Baked GGUF (exists; demo only)

`factbank bake` produces a real drop-in-LM-Studio file (smoke-passed).
Owner-rejected for serving: ~6k tokens of facts taxed onto EVERY
request — the anti-thesis of retrieval (F-040). Keep for: offline
demos, "try the idea in 10 seconds" marketing, gifting a friend a
fact-locked model. Costs nothing to keep; re-bake refreshes facts.

---

## 8. Cross-cutting decisions (apply to whichever option ships)

1. **Starter bank.** Ship the 94-fact research bank, or curate a
   "backend dev" starter (per the ~110MB-docs → 1.4–8MB estimate)?
   The watcher grows whatever we ship. [owner]
2. **Update default.** Full-auto is the standing owner decision;
   `--propose-only` exists for the cautious. Keep full-auto? [owner]
3. **Telemetry: none.** Nothing phones home except PyPI/GitHub fact
   fetches with library names only (already the wired behavior —
   worth SAYING in the README as a feature).
4. **Naming/versioning.** "factbank" 0.2.0 for the first public cut?
   PyPI name availability unchecked. [owner]
5. **License of OUR code.** Unset. MIT/Apache-2 for the package;
   the bank JSONL is data (CC0/CC-BY?). [owner]
6. **Gemma weights license** — must be read before ANY option bundles
   the GGUF (A2a / E distribution). [blocking flag for A2a only]
7. **Linux/mac.** Everything is Windows-proven only. C and D die
   without a Linux pass; A/B ship Windows-first honestly. [backlog M]

---

## 9. Work remaining, by option (sizes: XS<1h, S≈half-day, M≈1-2d)

| task | A | B | C |
|---|---|---|---|
| `/chat` micro-page (loopback) | M | M (shared) | – |
| README / quickstart | S | S | S |
| Model fetch-on-first-run | S (if A2b) | – | – |
| Embedded python folder build | S | – | – |
| GPU build selection | S–M | – | – |
| install.bat | – | S | – |
| PyPI publish + name + CI | – | – | M |
| Linux verify | – | – | M |
| starter-bank curation | owner | owner | owner |
| license file + gemma license read | S | XS | XS |

Open engineering backlog that benefits ALL options (from F-036/F-039,
none blocking): repair round-trip for mistake-bans; wire dormant
collision + self-retrieval gates (calibrated numbers ready); execution-
based scoring (parked, needs 3.13/3.14 runtimes).

---

## 10. Recommendation (mine, with reasons)

**Phase 1 (days): C + B-as-docs.** Publish the wheel properly with a
real README (C), document the sidecar pattern (B) — near-zero new code,
makes the work shareable and testable by others immediately.

**Phase 2 (the flagship): A with A2b.** One folder, small download,
model fetched on first run, `/chat` page included, Vulkan-only v1.
This is the only option a non-developer can survive, and it dodges
both LM Studio traps we measured. The `/chat` page built for A is
reused by B.

**Never:** D before Linux; E beyond demos.

The single highest-leverage build after this document is the **`/chat`
page** — it completes A *and* B, and it is the first time a normal
person can SEE the product without curl.

---

## 11. Open questions for the owner (the actual decide-list)

- [ ] A: build "The Folder"? bundle model (A2a) or fetch (A2b)?
- [ ] A1: build the `/chat` page? (my strong yes)
- [ ] C: publish on PyPI, or private?
- [ ] Starter bank: research 94 or curated backend-dev set?
- [ ] Code license? Bank license?
- [ ] Windows-first ship while Linux waits? (my yes)
- [ ] Name stays "factbank"?
