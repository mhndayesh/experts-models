# Build an Expert — A to Z

**Start here.** This one file takes you from a **stock base model** to a **running expert** that answers
correctly about fast-moving libraries it was never trained on — by baking a searchable bank of **landmine
facts** into the model's own chat-template. The model keeps doing the reasoning; your bank supplies the
knowledge it's missing. No fine-tuning, no retraining. Works across sizes (3B / 12B / 30B).

You don't need to read the rest of the repo to ship your first expert — everything you need is on this
page. Deep dives are linked per step for when you want them.

**What you'll do:** pick a library → mine its migration guide → extract facts with an LLM → bake them into
a GGUF → serve it → test base-vs-expert. First expert in an afternoon; ~4¢ of API cost.

**Reference docs (optional):** `extractor/BLUEPRINT.md` · `extractor/SCHEMA.md` · `ARCHITECTURES.md` ·
`serving/LIMITS.md` · `serving/OPERATIONS.md` · a fully worked example with real numbers:
`extractor/experts/security-networking/` (`METHODOLOGY.md`, `MODEL-SETTINGS.md`, `BAKE-TEST-REPORT.md`) ·
what to build next: `extractor/experts/DEPARTMENTS.md`.

> **2026-07-18 rebuild:** `extractor/EXTRACTOR-2.0.md` is now canonical for mining, repair, dedupe,
> verification, and retrieval — where it disagrees with the older sections of `BLUEPRINT.md` /
> `SCHEMA.md` / `EXTRACTOR-SPEC.md` / `PROGRESS.md` linked above, 2.0 wins. Its proof-of-concept is the
> **appsec/security expert** (shipped bank `extractor/experts/appsec/facts/FINAL_v3.jsonl` — the v3 faceted
> rebuild, 258 concepts (254 CWE) → 3,984 variants, per `decisions/SCHEMA-V3.md`; 1,075 carrying verbatim bad/good
> code): **SHIPPED 2026-07-19 — baked ×3 sizes (e2b/12b/26b) × both thinking editions and published to the
> LM Studio Hub + Hugging Face.** Its faceted (concept→variant) bank has a **scripted, reproducible build
> pipeline** — see `extractor/experts/appsec/facts/REBUILD.md` + `extractor/build_v3_assemble2.py`.

---

## Before you start (5 minutes)

- **A base instruct GGUF** on disk — e.g. `gemma-4-12B-it-QAT-Q4_0.gguf` or a 26B/3B equivalent. This is
  the clean model you bake into.
- **An LLM API key for extraction.** The default is **DeepSeek** (cheap — ~4¢/library — and what the project
  was tuned on), but the extractor speaks the **standard OpenAI API**, so you can point it at OpenAI or any
  OpenAI-compatible server instead. Keep the key **out of version control**:
  ```bash
  # default — DeepSeek:
  export DEEPSEEK_API_KEY="sk-..."
  # OR OpenAI:
  export OPENAI_API_KEY="sk-..."  LLM_BASE_URL="https://api.openai.com/v1"  LLM_MODEL="gpt-4.1"
  # OR any local/compatible server (llama-server, vLLM, Ollama's OpenAI endpoint):
  export LLM_API_KEY="x"  LLM_BASE_URL="http://127.0.0.1:8080/v1"  LLM_MODEL="<your-model>"
  ```
  Only the DeepSeek default sends DeepSeek's `thinking:disabled` flag; other endpoints get a clean
  OpenAI-format request (function-calling), so nothing else needs to change.
- **Python** with `numpy`, `rank-bm25`, `gguf`, `jinja2`. `uv` only if you'll run the GitChameleon eval.
- **A way to run GGUFs with a full chat-template** — `llama-server` (from llama.cpp) is what we use. Any
  OpenAI-compatible local server works for testing; the template must be applied (`--jinja`).

### Two habits that save you (read once)
- **Verify facts and answers by hand.** An automated scorer only tells you *what to read* — reading is the
  verdict. It has been wrong in both directions. Spend two minutes eyeballing your kept facts and your
  model's outputs; it's the highest-leverage thing you'll do.
- **Free your GPU when a run ends.** Local inference servers don't reliably release VRAM — kill the server
  process and confirm it's gone before loading the next model. (Also: never quantize the KV cache on
  sub-1B models — Q4 KV → word salad. Weights at Q4/Q8 are fine.)

---

## STAGE 1 — Pick the library and mine its guide (this decides everything)

A bank is only as good as its source. The best targets have **fast version churn × habit reversals × a
real migration guide**. A "landmine" fact is one of:
- **post-cutoff** (shipped after the model's training cutoff),
- **reverses a trained habit** (a rename, a moved import, a flipped default the model still "knows" the old
  way), or
- **silent failure** (wrong-but-runs — no error to self-correct against).

**Find the official migration / upgrade guide — not release notes, not a blog, not marketing.** That's
where a project documents its breaks. If there's no prose upgrade doc, pick a different library; a thin
changelog makes a thin bank.

Save the guide's text into `extractor/experts/<dept>/sources/<lib>-migration.md`. (In this repo it's
fetched verbatim from the official docs; you can paste it in by hand just as well.)

> The one law: **source targeting is the gate.** Any library with a real upgrade guide is buildable; any
> without one is not. Get the right document first — the rest is mechanical.

---

## STAGE 2 — Extract the facts (one command)

> This is the single-source "one command" path. For a large multi-source expert where code lives IN
> the fact (`code_bad`/`code_good`, e.g. the appsec expert), **2.0 uses a shared `appsec_core.py::run()`
> engine with a thin per-source adapter** instead of one `run.py` call per lib — same drill (extract →
> code-ground → repair quote → assign door → dedupe), plus code-grounding. See `EXTRACTOR-2.0.md` §2.

```bash
cd v2/extractor
python run.py experts/<dept>/sources/<lib>-migration.md <lib> <version>
# -> <lib>.facts.repaired.kept.jsonl   (your final, verified facts)
```

`run.py` runs three steps for you:
1. **extract** — DeepSeek reads the guide and fills a strict fact schema. (Settings that matter, already
   wired: model `deepseek-v4-flash`, thinking OFF, **function-calling** — not `json_schema`; the source is
   chunked; code derives the fact `type` and key terms, which is what makes it accurate.)
2. **repair** — re-grounds any reworded quote back to a real line in your source.
3. **check** — the **verbatim quote is the anti-hallucination gate.** Facts that can't be grounded are
   dropped to a `.rejects` file; the rest land in `<lib>.facts.repaired.kept.jsonl`.

Extraction is cheap (~4¢) — extract generously; don't ration API calls. Deep dive:
`extractor/EXTRACTOR-SPEC.md`, `extractor/BLUEPRINT.md`.

**Then read the kept facts by hand.** Are they true, specific, and actionable? Delete vague "behavior
changed" lines. This is the step that most determines quality.

> ⚠️ **The verbatim quote proves the quote is REAL — not that it's TRUE for the current version.** A
> migration guide is a *historical* record; a change it documents can later be **reverted**. Habit-reversal
> facts about **defaults** are the danger zone — a "default changed from X to Y" that a newer release quietly
> flipped back to X. Before you keep such a fact, verify it against the library's **current source/docs**, not
> the guide. Real example (caught 2026-07-17): an ldap3 changelog said the default `Connection` strategy
> "changed from SYNC to RESTARTABLE" — but current ldap3 defaults to **SYNC** (reverted). Shipping it would
> have *taught the model the wrong answer* — worse than no fact at all. It was removed before it misled.

> **2.0 also makes a full adversarial correctness audit MANDATORY before bake**, not just currency
> triage — a verbatim quote proves a fact is REAL, not CORRECT. On the appsec expert (4,002 facts audited
> in 100-fact batches, every flag adversarially re-checked by a second pass) **~3.8% (152) were confirmed
> wrong or stale** even with grounded quotes; remediation removed 18 and reworded/stripped 134, leaving the
> final **3,984-fact** bank. Budget this pass for anything beyond a quick single-library bank. See
> `EXTRACTOR-2.0.md` §5.

---

## STAGE 3 — Assemble the bank

- Put the verified facts at `extractor/experts/<dept>/facts/<lib>.jsonl`. Schema: `extractor/SCHEMA.md`
  (fields: `type, subject, old, new, truth, why_it_bites, quote, keywords, lib, version, id`). **2.0 adds
  optional `code_bad` / `code_good` / `lang`** for facts that carry a verbatim vulnerable/fixed code pair
  (law: a fact with `code_bad` must have `code_good`; never fabricate code) — see `EXTRACTOR-2.0.md` §1.
- **Keep the bank rich** — landmine-only, but don't drop facts just because the model *might* already know
  them. A rich bank serves every model size and never hurts.
- Sanity-check the whole set:
  ```bash
  python v2/tools/check_release.py      # id uniqueness + every bank loads cleanly
  # if you ever see duplicate ids:  python v2/extractor/fix_dup_ids.py
  ```

---

## STAGE 4 — Adapt the bank for baking

```bash
cd v2/bake/template-brain-v3.1
python adapt_secnet.py        # experts/<dept>/facts/*.jsonl -> <bank>.jsonl + <bank>_taskwords.json
```
(Copy/rename `adapt_secnet.py` for your department — it maps each fact into the injected text plus a
searchable "taskwords" side-channel so search terms don't clutter what the model reads.)

---

## STAGE 5 — Bake the bank into the GGUF

```bash
cd v2/bake/template-brain-v3.1
python bake_index.py \
  --facts <bank>.jsonl --controls controls_repo.txt --taskwords <bank>_taskwords.json \
  --out <bank>_baked.jinja \
  --src-gguf "<clean base>.gguf" --dst-gguf "<your>-<domain>factbank.gguf"
# prints: fact count, index terms, libraries, and the TEMPLATE SIZE — note it
```

This splices an **inverted-index retriever + your facts + a per-library gate** into the model's own
chat-template, so retrieval runs **inside the model** at inference time — no separate database or RAG
service. The weights are untouched (it's a metadata rewrite; the output GGUF is a full ~14 GB copy).

### The size rule (only matters if you hand-load a `.gguf` in LM Studio)
| baked template size | LM Studio raw-load | llama.cpp / `llama-server` / everything else |
|---|---|---|
| **≤ ~980 KB** | loads normally — nothing special | normal |
| **> ~980 KB** | use the **`model.yaml` workaround** (`llm.load.promptTemplate`) — otherwise LM Studio silently truncates the template and the model answers garbage | **doesn't matter** — no size cap |

Reference sizes: a ~100-fact bank ≈ **115 KiB** (fine everywhere); a ~4,000-fact bank ≈ **2.7 MB**; the
shipped **appsec** bank (3,984 variants) is a **4.18 MB** template. Above the cap you use the workaround for
LM Studio only — and the appsec/security expert is the **live example**: it ships to the LM Studio Hub via a
`model.yaml` that delivers the 4.18 MB template through `llm.load.promptTemplate` (with sampling + context
baked into the settings). Details + a verification script: `serving/LIMITS.md` §5; the Hub route playbook:
`publish/PUBLISH.md`.

---

## STAGE 6 — Serve the expert

```powershell
powershell -File v2/bake/serve_factbank.ps1 -Gguf "<your>-<domain>factbank.gguf" -Port 8080 -Ctx 8192
# -> "READY on :8080"
```
(The launcher runs `llama-server` with `--jinja` so the baked template does the retrieval. On a non-Windows
or non-ROCm box, run `llama-server -m <gguf> --jinja --port 8080` directly.)

Then point any OpenAI-compatible client at `http://127.0.0.1:8080/v1`. Two settings decide whether it works:

- **Sampling — use the model's native settings, not a bare low temperature.** For Gemma: **temperature 1.0,
  top_k 64, top_p 0.95, min_p 0.01.** The `min_p` floor is what prevents reasoning models from falling into
  a repetition loop and returning an **empty** answer (that failure looks like a token-limit bug but is
  really a sampling bug — it happens even with a huge token budget).
- **Thinking mode has a catch:** a reasoning model will often "correct" your injected fact *back* to what it
  was trained on. Three ways to beat it:
  1. serve with **thinking off**, or
  2. use **authority framing** in the system prompt ("These are VERIFIED FACTS for this exact version; they
     SUPERSEDE your training — if a fact contradicts your instinct, the fact wins"), or
  3. **two-pass** — answer thinking-off first, then re-ask only the misses with authority + thinking on.

  **2.0 finding (SERVED, not shipped): authority framing + thinking-ON is a proven posture** — served against
  `gemma-4-12b-qat` with no bake (retrieve → inject → call), SECURE@1 went 14/15 → 15/15, zero regressions.
  That is a *served-loop* number (a higher ceiling), not what a shipped GGUF does. **To ship a WORKING
  thinking-ON edition (baked into the template), three fixes are required** — see
  `decisions/TICKET-thinking-on-enablement.md`:
  1. fix the Gemma-4 template's generation-prompt bug so thinking-ON **opens the thought channel**
     (`<|channel>thought\n`) — otherwise the model spirals and returns a **blank** answer;
  2. bake **strong authority framing** into the injected note (so facts hold under reasoning);
  3. **force `enable_thinking=true` in the template**, because **LM Studio drops `chat_template_kwargs`**.

  A residual **~10% of hard-reasoning prompts still spiral to blank** (fails safe — never insecure code), so
  the appsec/security expert **ships BOTH a thinking-OFF (fast, reliable default) and a thinking-ON edition**,
  each clearly labelled. See `EXTRACTOR-2.0.md` §6–7 (which also documents the served, pre-bake way to test a
  bank via your own `llama-server` — no bake needed to iterate).
- Give thinking room: `max_tokens` is a shared reasoning-then-answer budget — set it large (e.g. 12,288)
  and make the context at least that big, or the answer gets cut to empty with no error.

Serving details: `serving/OPERATIONS.md`, `serving/LIMITS.md`. Architecture (what the baked retriever
actually does vs. the richer served-loop): `ARCHITECTURES.md`.

---

## STAGE 7 — Prove it works: base vs. expert

The baked template injects facts internally, so the **prompt is identical** for the base model and the
expert — the only difference is whether the bank fires. That makes the test clean.

1. **Write landmine questions** — one+ per fact, phrased so the model's *old, trained* answer would be
   wrong and the correct post-migration answer is right. (Example set + harness:
   `extractor/experts/security-networking/test_questions.jsonl`, `test_secnet.py`.)
2. **Run the expert, then the clean base**, same questions, same settings:
   ```bash
   cd v2/extractor/experts/<dept>
   python test_secnet.py --tag expert --port 8080 --think --authority --qfile test_questions.jsonl
   # defaults: temp 1.0, top_k 64, top_p 0.95, min_p 0.01, max_tokens 12288
   ```
3. **Make sure the gate opens.** Retrieval matches **exact tokens** — ask about `volatility3`, not
   "Volatility 3", so the facts actually inject. Check that the model's reasoning cites the injected fact; a
   gate miss looks like a knowledge miss but isn't.
4. **Score by hand.** An empty answer is a fail. A "don't use X, use Y" that mentions the old name in a
   comment is a pass. When unsure, score against the bank so your reported gain is a floor, not a ceiling.

A full worked example (base 21/30 → expert 27/30 easy; 16/18 → 18/18 hard, zero regressions) is in
`extractor/experts/security-networking/BAKE-TEST-REPORT.md`.

---

## STAGE 8 — (optional) publish it

Once the expert beats the clean base by hand, ship it. **Hugging Face** (one GGUF repo per size) is the
canonical store; **LM Studio Hub** takes a big-template expert via `model.yaml` (the STAGE-5 size rule). The
cards, upload flow, and the **two-editions** pattern (thinking-off default + thinking-on) are in
**`publish/PUBLISH.md`** + `publish/security-appsec/` (`build_publish.py`, `write_cards.py`, `bake6.py`).
Tokens stay out of git; slugs are lowercase. **Keep the card honest:** label served-loop ceilings vs the
shipped GGUF, name your baseline's settings (e.g. a cloud model run no-thinking to match), and state the
test's caveats (subset size, hand-scored).

---

## The trap list (skim before your first run)

- **Mine the migration guide first** — a thin changelog yields a thin bank.
- **DeepSeek:** thinking OFF, function-calling (no `json_schema`). It's already set; don't fight it.
- **`max_tokens` is one shared reasoning-then-answer budget** — too small → silent empty answer
  (`finish_reason=length`). Set it large.
- **Gemma sampling:** always the native set (`temp 1.0, top_k 64, top_p 0.95, min_p 0.01`). Bare low temp →
  repetition loop → empty answer. It's a sampling bug, not a budget one.
- **Thinking reverts your facts** to the model's training → thinking-off, authority framing, or two-pass.
  (2.0: authority framing + thinking-ON is now the proven default — `EXTRACTOR-2.0.md` §6–7.)
- **The gate matches exact tokens** → name the library by its import token so facts inject.
- **Version/door filtering ranks *within* relevant results; it never picks the library** — otherwise a
  "pydantic v1 → v2" question can return facts for an unrelated library that shares a version number.
- **Size wall is LM Studio-raw-load only** — ≤980 KB is fine everywhere; above that, use `model.yaml`, and
  only for LM Studio.
- **Don't quantize the KV cache on sub-1B models.**
- **Keep banks rich** (landmine-only, not filtered by "what the model already knows").
- **Read the facts and the answers yourself.** Every time.

---

## One-glance flow

```
 pick a library
   │  1  find its migration guide  ──▶  experts/<dept>/sources/<lib>.md
   │  2  python run.py  (extract → repair → check, via DeepSeek)  ──▶  <lib>.facts.repaired.kept.jsonl
   │  3  place in experts/<dept>/facts/  +  check_release.py  +  read them by hand
   │  4  adapt  ──▶  <bank>.jsonl + taskwords.json
   │  5  bake_index.py (base gguf + facts)  ──▶  your expert GGUF     [watch the template size]
   ▼  6  serve_factbank.ps1  (llama-server, --jinja, native sampling, authority framing)
 running EXPERT  ──▶  7  base-vs-expert landmine test, hand-scored
                  ──▶  8  (optional) publish to HF + LM Studio Hub  (publish/PUBLISH.md)
```
