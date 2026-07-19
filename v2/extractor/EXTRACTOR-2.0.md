# Extractor / Facts / Retrieval **2.0** — the 2026-07-18 rebuild

**Status: canonical.** This supersedes the v1 mining/indexing/retrieval methods described in the older
sections of `PROGRESS.md`, `BLUEPRINT.md`, `EXTRACTOR-SPEC.md`, and `SCHEMA.md`. Where anything disagrees,
**2.0 wins.** v1 methods that were changed or retired this run are listed under **RETIRED** at the bottom.

The 2.0 pass was proven end-to-end by building the **appsec expert** (a large "real security expert", code
examples carried inside the facts) and testing it served against `gemma-4-12b-qat`. Extraction bank:
**`experts/appsec/facts/FINAL.jsonl` — 3,984 facts, 1,075 with verbatim bad/good code**, correctness- and
currency-audited.

> **SHIPPED 2026-07-19.** The bank that actually ships is the **v3 faceted rebuild
> `experts/appsec/facts/FINAL_v3.jsonl`** — the flat `FINAL.jsonl` facts re-cast as **258 concepts (254 CWE) →
> 3,984 variants** (concept→variant schema, per `../decisions/SCHEMA-V3.md`). **The build pipeline is scripted end-to-end** —
> `build_v3_assemble2.py` + `experts/appsec/facts/REBUILD.md` (rebuilds 91% of `FINAL_v3.jsonl` exactly from the
> now-tracked inputs; ~9% is lost source data, so `FINAL_v3.jsonl` stays canonical). It was **baked ×3 sizes
> (e2b/12b/26b) × both thinking editions (thinking-OFF and thinking-ON)** and published to the LM Studio Hub
> + Hugging Face. Read `FINAL.jsonl` below as the extraction output; `FINAL_v3.jsonl` is its shipped form.

---

## 1. Facts 2.0 — the schema (superset, backward-compatible)

A fact is still an LLM-made, code-verified, version-tagged landmine. **New in 2.0: code lives IN the fact.**

Added fields (all optional, additive to the v1 schema):
- **`code_bad`** — the vulnerable/insecure snippet, copied VERBATIM from the source.
- **`code_good`** — its secure fix, VERBATIM. **Law: a fact with `code_bad` MUST have `code_good`** (never
  ship the vuln without its fix; bad-only is rejected).
- **`lang`** — the code language, lowercased, or `text`.
- New `type` values for insecure-by-default work: `INSECURE_DEFAULT`, `HABIT_REVERSAL`, `SILENT_FAILURE`,
  `DEPRECATED_CRYPTO`, `MISSING_CONTROL`.

A fact is therefore one of: **text-only**, **text + good**, or **text + bad + good**. Code is DATA-DRIVEN —
if the source has a real example we capture it; if not, it is a normal text fact, missing nothing. Never
fabricate or force code.

**Grounding rules (the anti-hallucination gates):**
- prose **`quote`** stays the verbatim source anchor (normalized, see repair below).
- **`code_bad`/`code_good` are ground truth: verbatim-in-source modulo whitespace (`gnorm`), NEVER via
  `canon()`** — case and punctuation are load-bearing in code. A snippet that is not verbatim is dropped
  (the fact falls back to text-only), never rewritten.
- `code_good` is syntax-gated for Python (compiles) and never accepted if it isn't the same operation as
  `code_bad`.

---

## 2. Mining 2.0 — one shared pipeline, thin adapters per source

The center of gravity is the **data/mining step**, not the baker. The engine is now a single shared module:

**`appsec_core.py` — `run(items, out_prefix, extra_sys, id_prefix)`** runs the identical proven drill for
every source: **extract (DeepSeek function-calling, verbatim code) → code-ground → repair quote → assign
door → dedupe → write `<out>.jsonl` + `<out>.rejects.jsonl`.** The LLM does meaning; dumb code verifies every
field. The GROUND-TRUTH RULE is baked into the system prompt: *"SELECT and COPY; do NOT rewrite / reformat /
fix / shorten / translate / improve any code, and do not change a fact's meaning. Never invent code."*

**Every source is a thin ADAPTER** that only produces `items` (`{llm_input, corpus, source, license_note,
lib, version, door?}`) and calls `appsec_core.run()`. Adapters built this run:
`codeql_mine.py` (qhelp XML + git-blob code samples), `appsec_sast.py` (Bandit+gosec catalogs),
`appsec_owasp.py` (Cheat Sheets, packed-section chunking), `appsec_mastg.py` (mobile, transclusion-resolved),
`appsec_rustsec.py` (advisory-db), `appsec_mine_crypto_net.py` (NIST/RFC/Mozilla), `appsec_mine.py` (CWE).

Per-source facts (w/verbatim code): CWE 259 (44) · CodeQL 1,416 (831) · SAST 208 (112) · MASTG 546 (56) ·
RustSec 66 (2) · crypto-net 546 (0, standards have no code) · OWASP 962 (75).

**Mining learnings (this run):**
- **Source targeting applies INSIDE a source, not just across sources.** CWE is a mixed catalog (drop
  hardware/Verilog + code-quality); RustSec over-produced obscure single-crate memory-CVEs (added a
  `LOW_BITE_ONLY` category drop: 137→66, bite up); crypto-net/OWASP carry policy/process facts that don't
  bite a code-gen model (flagged for the behavioral filter, not blunt-cut).
- **FIND the migration/security guide, not the changelog/release-notes** (unchanged v1 law, reconfirmed).
- **DeepSeek cost is negligible** (~cents/session) — extract more, deeper; the real limits are source
  targeting, grounding, and retrieval.

---

## 3. Repair 2.0 — sentence-boundary verbatim grounding

`repair_quote` (in `appsec_core.py`) re-grounds a paraphrased/abbreviated `quote` to real source text.
**2.0 change:** it now splits the quote on **ellipses AND sentence boundaries** and returns the **longest
verbatim-grounded span**, then falls back to best token-overlap line (threshold 0.5). This is strictly safe
— it only ever returns text that is actually present in the corpus, never admits paraphrase. It recovers
near-verbatim multi-sentence quotes whose full span isn't verbatim (a punctuation artifact or a mid-sentence
newline) but whose first sentence is (e.g. Bandit B310, MASTG `drand48`).
**RETIRES** the v1 ellipsis-only split + the ≥3-word guard + the 0.6 threshold (all too strict; they
wrongly rejected good facts, e.g. `"allUsers"`).

---

## 4. Dedupe 2.0 — prose-only, cross-source; code is NOT a dup signal

Per-source dedupe (Jaccard ≥0.6 on subject+truth) runs inside `run()`. **Cross-source dedupe**
(`appsec_merge.py` → `FINAL.jsonl`) is **prose-only**. Hard lesson: **a shared `code_bad` is NOT a duplicate
signal** — sibling CodeQL queries reuse ONE boilerplate sample (`doGet`, `merge()`, `set_cookie`) to teach
DIFFERENT lessons; keying dedupe on code wrongly cut 251 distinct facts. At the safe 0.72 prose threshold
cross-source dedupe removes ~0 (the bank is already prose-distinct); even 0.60 touches only 13/4002, most of
which are cross-LANGUAGE variants worth keeping (`reqwest::get` vs `http.Get`, py `yaml.load` vs rb
`YAML.load`). Law: **keep the bank RICH; only collapse near-identical LESSONS, never language variants.**

---

## 5. Verification 2.0 — currency + a MANDATORY full correctness audit

**This is the stage that decides whether the model is helped or harmed: a wrong fact corrects the model
toward the wrong answer — worse than no fact.** Two passes, both required before bake:

**(a) Currency verification.** A verbatim quote proves a fact is REAL, not TRUE-for-today. Triage
habit-reversal + deprecated-crypto facts for volatility markers (library-default / version claims), then
web-verify the mutable-default ones against current docs/source. Confirmed flips this run: **lxml** default
parser hardened in 5.0 (external XXE now blocked) — the "default resolves external entities" fact was stale
and removed; PyTorch `torch.load` `weights_only` default flipped True in 2.6; PBKDF2 100k→600k; tarfile
`filter='data'` default (3.14); `checkSignatures()`→`hasSigningCertificate()`; NIST SP 800-63B→800-63B-4.

**(b) Full correctness audit — MANDATORY, adversarial.** Workflow `appsec-verify-all`: **one verifier agent
per 100-fact batch** (web-checks every library/API/version claim), then **every flag adversarially
re-checked** by a second agent (default-reject) so false flags are dropped. Ran on **Sonnet** (checking does
not need Opus). Over all 4,002 facts: **152 confirmed problems (38 WRONG, 38 STALE, 58 MISLEADING, 18 WEAK),
30 false flags dropped.** WRONG = broken code pairs (byte-identical bad/good, invalid syntax), nonexistent
APIs (`bzero_explicit`→`explicit_bzero`, `Regex.escape`→`Regexp.escape`), inverted advice, mislabeled
Bandit/gosec/CWE tags, quote-contradicts-truth. Remediation (`appsec_remediate.py`, SAFE — never inject
unverifiable code): 18 WEAK removed, 36 broken-code stripped to text-only, 118 truths reworded to the
confirmed correction. **THE LESSON: even LLM-first + verbatim-grounded mining ships ~3.8% wrong/stale facts.
A full adversarial correctness audit is MANDATORY before bake, not optional.**

---

## 6. Retrieval 2.0 — HyDE double-key, proven served (no bake needed to test)

For an **insecure-by-default** bank the user's prompt does NOT contain the security keyword (they ask "look
up a user by name", the fact is "use parameterized queries"). So retrieval on the prompt alone under-fires.
**HyDE / double-key retrieval:** retrieve with the PROMPT **and the model's DRAFT** — the draft names the
insecure API/pattern (`cursor.execute(f"…")`, `torch.load(f)`, `md5(`, `verify=False`) that matches a fact's
`code_bad` symbols. Prompt hits outrank; the draft key is capped; light MMR keeps the top-k spanning distinct
libs. (`appsec_servetest.py::retrieve`.) The mined `from_fact` symbol keywords are what make the draft key
land.

**Injection = authority framing + thinking-ON** (the cure for reasoning-reverts-the-fact): the retrieved
facts are injected as an AUTHORITATIVE, must-obey security policy that overrides the model's defaults, and
the model runs thinking-ON. This is now the default posture.

---

## 7. Serving/test harness 2.0 — own llama-server, not LM Studio

Test the bank **served** against a loaded base model with NO bake: retrieve → inject (authority-framed) →
call. **Run it on your OWN `llama-server` (`../bake/serve_factbank.ps1`), NOT LM Studio** — LM Studio
silently drops `chat_template_kwargs`, so thinking-ON/`enable_thinking` has no effect there; llama-server
(`--jinja`) honors it and lets you control sampling directly. Gemma-native sampling: **temp 1.0 / top_k 64 /
top_p 0.95 / min_p 0.01** (bare low-temp causes repetition-loop EMPTY answers; min_p is the fix). Rule 3:
kill your llama-server and free VRAM after the run.

**Serve-test finding (gemma-4-12b-qat, 2026-07-18):** a well-trained 12b already writes secure code for
textbook AND many subtle cases (SQL→PreparedStatement, AES→GCM+nonce, cookies→HttpOnly/Secure/SameSite,
YAML→`safe_load`, JWT→`ParseWithClaims`, lxml→`resolve_entities=False`, tar→`filter='data'`, tokens→
`secrets`). **SECURE@1: base 14/15 → bank 15/15, zero regressions.** The bank's decisive win is the
**post-cutoff / reversed-default** fact the model could not have learned — `torch.load` `weights_only=True`
(PyTorch 2.6, Jan 2025). **This confirms the thesis:** the model supplies reasoning; the bank supplies the
knowledge it can't have. Implication: stress the bank with a HARD post-cutoff/subtle set, not textbook
OWASP-Top-10. (Harness bug fixed: thinking-ON over a long injected prompt overran `max_tokens` → empty
answer; raise the budget — the "max_tokens is one shared reasoning-THEN-answer budget" trap.)

---

## RETIRED this run (legacy — do not reuse)

- **Parallel-agent mining** (one opaque agent per source, fired together) → **retired** for
  main-thread, one-source-at-a-time adapters on `appsec_core`, each hand-read to "perfect" before the next.
- **v1 `repair_quote`** (ellipsis-only split, ≥3-word guard, 0.6 threshold) → replaced by §3.
- **Code-signature dedup** (treating a shared `code_bad` as a duplicate) → rejected; dedupe is prose-only (§4).
- **"Verbatim grounding is sufficient"** assumption → **retired**: grounding proves REAL, not CORRECT or
  CURRENT; the full correctness audit (§5b) is now mandatory.
- **LM Studio for serving/testing** → retired for own `llama-server` (§7); LM Studio drops
  `chat_template_kwargs` and raw-loads >980 KB templates as a sentinel.
- **`lookup.py` v1 retrieval fields** (`old`/`new` migration-schema keys) → superseded by the Facts 2.0
  schema + HyDE served retrieval (§6); `lookup.py` remains only as the doors+pointers+MMR algorithm prototype.
- **Pre-audit fact counts** (bank of 4,003 before the correctness audit) → superseded by the audited
  **3,984**.
