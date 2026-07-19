# structured-extractor — progress & notes

Running log + decisions for this chapter. Companion to [`README.md`](README.md) (the design).
Everything below was **measured or hand-read**, not assumed.

> **⚑ 2.0 REBUILD (2026-07-18) — read [`EXTRACTOR-2.0.md`](EXTRACTOR-2.0.md) FIRST.** The mining, indexing,
> and retrieval methods were rebuilt this run while building the **appsec expert** — **3,984 facts, 1,075
> with verbatim bad/good code, currency- and correctness-audited.** **SHIPPED 2026-07-19:** the security
> expert is now BAKED ×3 sizes (e2b/12b/26b) in **BOTH thinking editions (thinking-OFF and thinking-ON)** and
> published to the **LM Studio Hub** + **Hugging Face** (collection "Information Security EXPERTS"). The
> shipped bank is the v3 faceted rebuild **`FINAL_v3.jsonl`** (258 concepts (254 CWE) → 3,984 variants, per
> `../decisions/SCHEMA-V3.md`), NOT the pre-v3 flat `FINAL.jsonl`. **The v3 build pipeline is now scripted & reproducible** (`build_v3_assemble2.py`
> + `experts/appsec/facts/REBUILD.md`) — it rebuilds **91% of `FINAL_v3.jsonl` exactly** from the now-tracked inputs;
> the ~9% residual is lost source data, so `FINAL_v3.jsonl` stays canonical. **`EXTRACTOR-2.0.md` is canonical**; the
> §1–§9 below describe the v1 pipeline and are
> superseded where they disagree. Headline changes: code lives IN the fact (`code_bad`/`code_good`, verbatim,
> never `canon()`); one shared `appsec_core.run()` pipeline + thin per-source adapters (retires the
> parallel-agent mining); sentence-boundary repair (retires the ellipsis-only/word-guard repair); prose-only
> cross-source dedupe (a shared `code_bad` is NOT a dup signal); **a MANDATORY adversarial correctness audit**
> (found ~3.8% wrong/stale — grounding proves REAL, not CORRECT); HyDE double-key served retrieval with
> authority-framing + thinking-ON on your OWN llama-server (retires LM Studio for serving). See RETIRED list
> in `EXTRACTOR-2.0.md`.

> **UPDATE (2026-07-15/16): banks are now baked + benchmarked.** GitChameleon (gemma-4 **12b + 26b**)
> and Security & Networking (**26b**) are baked into GGUFs and scored in-engine — see §8/§9 below and
> `../ARCHITECTURES.md`. The early "nothing baked yet" notes in §5 are historical (they described the
> pre-bake Python-prototype state) and are superseded by §9.

---

## Where we are (2026-07-15)

Two things are proven, in Python, hand-read:
1. **Extraction** — LLM-first, strict schema, derive-in-code, quote-anchor + repair pass.
2. **Retrieval** — soft doors + classic pointers + richer keywords + MMR.

The remaining gap before a GGUF bake is **source targeting** (point the extractor at
migration *guides*, not release notes) and the **Jinja/real-engine parity check**.

---

## 1. Extraction — what we built and measured

Pipeline: `extract.py → repair.py → check.py` (driver: `run.py`).

- **LLM is the main extractor** (inverts the old rules-miner). Reads ANY shape (prose guides,
  release notes, changelogs), fills a **strict schema** via DeepSeek **function-calling**.
- **DeepSeek has NO strict `json_schema` mode** (API returns "unavailable"). Function-calling
  works and enforces shape. Verified live.
- **The big win was schema DESIGN, not the output mode:** stop asking the model for what code
  can derive. `type` reconciled from `new`; `from_fact` keywords pulled from old/new/truth in
  code. That alone took the k8s control **35% → 96.5% clean** — same model, same prompt.
- **Quote-anchor** (`check.py`): a fact's `quote` must be VERBATIM in the source. This is the
  anti-hallucination gate; on messy prose it correctly *drops* paraphrased quotes.
- **Repair pass** (`repair.py`): a SECOND checker pass (no LLM) that snaps a dropped fact's
  quote to the real source line mentioning its symbol. Owner's idea: *"the dropped needs
  another run as checker not extractor."* If no line mentions the symbol → stays dropped.

**Measured extraction quality (hand-read):**

| source | shape | clean facts | vs rules-miner |
|---|---|---|---|
| k8s deprecation guide | clean prose | 83/86 (96.5%) | rules: 44 |
| pydantic v1→v2 migration | messy prose+code+tables | 145/178 → **174/178 (97.8%) after repair** | rules under-read it |
| transformers release notes | release notes | 130 | rules: **8** |
| terraform-aws v6 upgrade | HCL prose | 114 | rules: **~0** |

Repair snap quality: ~8/9 exact; ~1/9 grabs a token-adjacent *sibling* line (real fact,
imprecise anchor — fixable with a distinctive-token requirement).

---

## 2. Retrieval — fixes tested ONE BY ONE, hand-read

Prototype: `lookup.py` (pure Python; Jinja port is a later parity concern).
Bank for testing: **508 facts, 4 doors** (pydantic 175, kubernetes 89, terraform-aws 114,
transformers 130).

**Foundation (proven earlier):**
- **Doors = soft nudge, not a wall.** Multiply the matching door's scores (`W=0.8`), never
  exclude. Fixes misroutes while staying fail-open (F-019).
- **Hard doors REJECTED** — routing on the top-1 hit amplifies a wrong-door false positive into
  a total miss (demonstrated live).
- **Door comes from CONTEXT (the draft/HyDE), not keyword-guessing.** Auto-infer from query
  words still misrouted; the `hint` (lib the user is in) fixed it.
- **Classic pointers** — facts bucketed by `(lib, namespace)`, linked into a ring; `next` walks
  the cluster. Edges DERIVED from structure (old→new, namespace siblings) — no LLM. Modest
  combine-boost.

**The four fixes, isolated, hand-read verdicts:**

| fix | targets | verdict |
|---|---|---|
| 1. `spec` (rare-token weight²) | Q1, Q5 | ❌ **REJECT** — moved neither; 5 common words still beat 1 rare, even squared |
| 2. `mmr` (dedup diversity) | Q5 burial | ✅ **KEEP** — buried FlowSchema fact → top-5; holds at 508-fact scale |
| 3. `alias` (query expansion) | Q1 keyword gap | ✅ works but **STOPGAP** — needs a hand-built table; **redundant once #4 is in** |
| 4. richer keywords (extraction) | Q1 keyword gap | ✅ **KEEP** — the real fix; `min_length` findable with no crutch, no regressions, scalable |

**FINAL recipe: soft doors + pointers + richer keywords (4) + MMR (2).**
Dropped: `spec`, hard-doors. Optional: `alias` (only to patch an already-baked bank).

**Bigger-bank test (508 facts, 4 doors), hand-read: 7/8 queries hit target in top-5**,
zero cross-door contamination, MMR + richer keywords both held at scale.

---

## 3. Open items — before any bake

1. **Source targeting (`[FIND]` step)** — the ONE real miss (Q8 `use_auth_token`) was because
   transformers was extracted from *release notes*, not its *v5 migration guide*. The fact was
   never in the bank. **The extractor is only as good as the doc you point it at.** Biggest lever.
2. **Jinja / real-engine parity** — `mmr`, soft-doors, and pointer-walk are proven in Python
   only. Must be verified in the actual llama.cpp Jinja engine before baking (F-050 parity,
   F-053 metadata-cache assert). "Can express it" ≠ "verified."
3. **Bigger scored eval** — current results are hand-read on ~8 queries. Build a `gold.json`-style
   set (like `jinja_lab/`) to score properly at scale.
4. **Landmine-gate** (does a fact actually beat the bare model) — still unbuilt. The real
   precision filter (numpy-2.0 lesson: the model already knew 5/6). Turns "clean facts" into
   "facts that win."
5. **Minor extraction nits** — tf-aws `vpc` fact has `new=None` (replacement only in `truth`);
   repair's ~10% sibling-snap.

---

## 4. Files

| file | role |
|---|---|
| `extract.py` | LLM extraction (function-calling + derive-in-code + richer keywords) |
| `repair.py` | quote re-grounding (checker pass, no LLM) |
| `check.py` | raw checker (verbatim-quote anchor) |
| `run.py` | driver: extract → repair → check |
| `lookup.py` | retrieval prototype (soft doors + pointers + MMR + alias/spec toggles) |
| `facts/` | the 4-door test bank (508 facts) |
| `README.md` | the design | `PROGRESS.md` | this log |

---

## 5. Standing rules honored
- **Score, then READ MANUALLY and re-score** — every verdict here is hand-read; the count lied
  in both directions more than once (e.g. pydantic 58% hid ~51 good facts behind checker bugs).
- **DeepSeek only** (cloud, no GPU). Key read from env, never written into the repo.
- **~~Nothing baked~~ — SUPERSEDED (see §9).** This was true when §1–§5 were written (Python/prototype,
  pre-parity). The parity gate (F-050) has since CLOSED for the baked experts: GitChameleon (12b+26b) and
  Security & Networking (26b) are baked into GGUFs and benchmarked in-engine.

---

## 6. First expert built: AI-ML (2026-07-15)

Coverage decided from trusted curricula (see `experts/ai-ml/COVERAGE.md`), then source-hunted and
extracted. **817 facts, 11 doors.**

- **Source targeting is everything.** First pass pulled *release notes* and got a lopsided bank
  (vllm 252 / the LLM-app core ~18). Fixed by hunting **migration guides**: transformers
  `MIGRATION_GUIDE_V5.md` (raw), OpenAI v1 + Responses (WebFetch), LangChain v1, LlamaIndex
  deprecated-terms, Google genai, HF datasets v4, GGUF spec. Flagship landmines now present
  (`ChatCompletion.create→client.chat.completions.create`, `use_auth_token→token`, GGUF v2→v3).
- **Fetch reality:** raw GitHub for some (transformers, GGUF spec); WebFetch-rendered for web-only
  docs (openai/langchain/llamaindex/google) — facts real, `quote` anchors against the rendered copy.
- **Banks stay RICH, not model-gated** ([[banks-rich-not-model-gated]]) — one bank serves 3b/12b/30b,
  so the landmine-gate (drop-what-model-knows) is CANCELLED.

## 7. Second DeepSeek pass (concrete-rewrite) — TESTED, NOT ADOPTED

Built `refine.py`: for each *vague* fact, pass the **actual source section** (owner requirement) to
DeepSeek and ask for a concrete, output-explicit rewrite; keep the `quote` anchor; write a
before/after diff to READ. Verdict from **manual reading**:

- **Vagueness is only ~5% (42/817), all in release-note doors** (vllm 38, transformers 4).
  **Every migration-guide door is already 100% concrete** — `extract.py`'s prompt handles it.
- **Passing the source does NOT rescue a vague fact when the SOURCE is vague.** vllm's 22 rewrites
  were marginal — mostly appended a PR number or reworded "it changed" → "has changed (#42311)".
  Garbage in, garbage out (matches the Ecto "generic subjects aren't LLM-fixable" finding). Discarded.
- **Conclusion:** concreteness is an **extraction / source-quality** property, not a second-pass fix.
  The lever is *migration guides > release notes* + the `extract.py` prompt — NOT a refine pass.
  `refine.py` kept as evidence; not part of the standard pipeline.

**Blueprint takeaway:** pipeline = FIND (migration guides) → extract → repair → check. No second pass.

---

## §8 GitChameleon expert build + three extractor bug-fixes (2026-07-15)
Built the **GitChameleon 2.0 expert** (benchmark chosen to test base vs. bank): mined official
changelogs for 24 of 26 libraries → **4,167 facts across 23 doors**, 100% quote-grounded.
Sources/targeting/coverage in `experts/gitchameleon/`.

**Three bugs found by hand-reading rejects (F-065: the count lied, reading was the verdict) — fixing
them recovered +901 facts (28%):**
1. **DEPRECATED enum leak** (`extract.py`): LLM emits `type:"DEPRECATED"`; derive step passed it
   through; checker killed it. Fix: coerce any out-of-enum type from `new`-presence. Every changelog
   says "X is deprecated," so this bled removal facts from every lib.
2. **canon markup bug** (`check.py`+`repair.py`): the verbatim anchor stripped single backticks but
   mangled rst `` ``code`` `` and `:role:` markup, so quote≠source on markup differences → **777
   false "not verbatim" rejects**. Fix: normalize BOTH sides to a bare lowercase word-sequence
   (`re.sub(r"[^a-z0-9]+"," ",…)`). This is the big one; rst/sphinx sources need it.
3. **repair anchors too narrow** (`repair.py`): snapped only on symbols in `old/new/subject`; when
   those are prose ("returned None") the real symbol lived in `truth`/`from_fact` and was invisible.
   Fix: add `keywords.from_fact` to `anchors()`.

**Reachability (model-free, `reach.py`):** 69.6% with door hint (222/319), door purity 94.5%. Misses:
10 no-source, 58 coverage/absence (undocumentable), 29 retrieval-headroom (in-bank, out-ranked → ~79%).
Live base-vs-expert pass@1 NOT run (rule #1: no model loaded; also no Docker for scoring). Served-loop
harness `gen.py` built + load-guarded; run sequence in `../eval/gitchameleon/REPORT.md §6`.

---

## §9 GitChameleon expert BAKED + BENCHMARKED (2026-07-15)
Baked the 4,167-fact bank into gemma-4 **12b + 26b** GGUFs (e2b deferred — its chat-template differs,
needs re-anchoring). Pipeline: `../bake/template-brain-v3.1/adapt_gc.py` (bank→index schema + taskwords)
→ `bake_index.py` (58,877-term inverted index, 2.73 MB template) → written into the GGUF via the `gguf`
package (all tensors byte-identical, only metadata changed).

**Parity gate (F-050) CLOSED** for this expert: served via llama.cpp `llama-server`, the baked bank
fires in-engine (e.g. pandas 2.0 `to_sql→int`, flask `script_info→click ctx`, falcon `body→text`).

**Serving fixes (all in `../bake/serve_factbank.ps1`):** LM Studio raw-load sentinels >980 KB templates
(F-053) → use llama-server; ROCm exe needs the rocm-vendor bin on PATH (else DLL_NOT_FOUND); launch via
PowerShell not Git-Bash (CRT DLLs); **thinking ON empties the answer** → pass `enable_thinking:false`.

**FINAL SCORE — execution pass@1 on the hidden pytest tests** (`../eval/gitchameleon/run_tests.py`, uv
venvs per lib/version; scored on the 249/328 problems whose pinned old-version env builds on Windows —
same set both models; hand-verified vs ground truth, 0 empty/no-code answers):
- **12b:** base 37.8% → baked **44.2%** (+6.4 pts; fixed 30 / broke 14)
- **26b-a4b:** base 43.4% → baked **46.2%** (+2.8 pts; fixed 21 / broke 14)
Baked > base at both sizes; the lift shrinks as the base model gets stronger. Full write-up:
`../eval/gitchameleon/BAKE-REPORT.md`.
