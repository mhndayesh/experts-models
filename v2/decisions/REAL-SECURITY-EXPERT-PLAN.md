# The Real Security Expert — build plan (code-carrying facts, 12b + 26b)

> ✅ SHIPPED 2026-07-19 — this plan is fully executed. The appsec/security expert baked ×3 sizes × both
> thinking editions, published to LM Studio Hub + HF. Canonical now: EXTRACTOR-2.0.md +
> TICKET-thinking-on-enablement.md + the security-appsec cards. Kept as the historical plan record.

> Status: **PLAN / research complete for 3 of 4 tracks** (2026-07-18). No code changed, no GPU run.
> This is the "what we build and what we change in the code" document. Nothing here is executed until
> the owner says go. Scope: ONE large security / cybersecurity / networking expert that **carries code
> examples** (vulnerable pattern + secure fix), 4,000+ facts fine, baked into **12b and 26b** (skip e2b
> for this flagship). Researched by four Opus workers reading the real pipeline + the GitChameleon
> 4,167-fact precedent.
>
> **UPDATE (2026-07-18) — executed; canonical spec is `v2/extractor/EXTRACTOR-2.0.md`.** The plan below
> drove real work: the appsec expert is now **BUILT + AUDITED** (`experts/appsec/facts/FINAL.jsonl`,
> 3,984 facts, 1,075 with verbatim `code_bad`/`code_good`, currency- and correctness-audited) and is
> **PRE-BAKE — not yet baked, not yet published.** This design doc is kept intact as the historical
> record of the plan; several specifics below were changed or overturned by build experience — see the
> inline **Superseded** notes and EXTRACTOR-2.0.md, which wins wherever the two disagree.

---

## 1. What is new versus every expert so far

Every FactBank fact today is **short text** (a rename, a removed flag, a changed default). This expert
adds a genuinely new capability: **facts carry multi-line CODE** — a vulnerable snippet next to its
secure fix. That one change ripples through the whole pipeline (extract → check → dedupe → adapt → bake →
serve → test). The good news from the research: **most of the pipeline is additive and low-risk; the
load-bearing, easy-to-break parts are validation and delivery, and they are now precisely identified.**

The distinctive, publishable claim we are set up to prove: *carrying the secure code pattern, not just a
prose fact, measurably improves the model's secure code — specifically on code-generation tasks.*

---

## 1a. Design principle (owner, 2026-07-18) — the code lives IN the fact

**The code example is embedded in the fact record and travels with it on retrieval. There is NO separate
"code search."** The retriever still matches on the fact's keywords/symbols (text + `from_fact`); when a
fact is selected, its `code_bad`/`code_good` ride out with it as payload (the `fb_code` array is indexed by
the SAME fact id — §4). One fact = one claim + its own example.

Two consequences that shape the whole effort:
- **Baking is additive to `template-brain-v3.1` — NO v3/v4 rewrite.** Retrieval (gate, inverted index,
  keyword/IDF scoring, MMR, soft-doors, top-5 injection) is unchanged. The code is a parallel payload array
  read only at the final injection step, guarded by `fb_code[id] != ""` so existing experts bake
  byte-identical. Total baker delta ≈ 5 additive edits + one `parity.py` test (§4). Not a new architecture.
- **The center of gravity is the MINING / DATA step.** The hard, valuable work is producing facts that each
  carry a grounded, minimal bad/good code pair. Everything downstream (bake/serve) is small and mostly done
  on paper. So the build effort concentrates in: source mining → the extractor producing `code_bad`/
  `code_good` → the code-aware grounding checks → hand-verifying each pair.
- **Subtlety that keeps it findable:** we still mine the *insecure symbols* out of the code into the fact's
  `from_fact` keywords (so a draft emitting `pickle.loads`/`md5`/`verify=False` opens that fact), but the
  code BLOCK itself is not indexed — it's payload. Searchable by the symbol, delivered with the block.

## 1b. Scope: this is a fact-making v2 (extractor + schema); the baker stays v3.1

Decided (owner, 2026-07-18): the appsec expert needs a genuine **v2 of the fact-making side** — the baker
does NOT change beyond §4's additive edits. Split cleanly:

- **Facts 2.0 = a SUPERSET schema (backward compatible).** Every v1 fact stays valid; v2 adds the security/
  code fields (`code_bad`/`code_good`/`lang`, `PATTERN`/`INSECURE_DEFAULT`, `weakness`/CWE-id, `door`,
  `source`, `license_note`, provenance `source_url`/`date`). A migration-style fact is just a v2 fact with no
  code. So this is an evolution, not a break — netsec/offsec/dataplane facts remain loadable.
- **Extractor 2.0 = the pipeline evolved.** The core is unchanged (LLM extracts → code verifies every field →
  verbatim-quote anchor). What's genuinely new:
  1. **Multi-source ingestion (the biggest new build).** v1 only ate markdown migration guides. v2 needs
     per-format *source adapters*: CWE **XML** (schema-structured), CodeQL **qhelp** + test fixtures, the
     permissive SAST rule catalogs (Bandit/gosec), RFC/NIST text, OWASP markdown. Each adapter chunks its
     format and feeds the same extractor core.
  2. **Code emission + code-aware grounding** (§2/§3): `code_bad` grounded by exact-substring-modulo-
     whitespace, `code_good` syntax-gated, **never `canon()`**; robust JSON salvage for multi-line code.
  3. **Behavioral value function** (§5.0): score a candidate by "does the base model EMIT the bad pattern?"
     not "is it post-cutoff." Different probe set, same manual discipline.
  4. **License/attribution capture per fact** (`license_note`) + currency checks for crypto/TLS.
- **Data mining 2.0 = the per-source pipelines** that ride on those adapters (CWE → SEI CERT → OWASP → CodeQL,
  then NIST/RFC/SAST), plus code-aware dedup.

**Naming caution:** the whole repo is already the `v2/` tree, so "v2" collides. In code/docs call this the
**fact model 2.0 / extractor 2.0** (or a codename) to avoid confusion with the `v2/` directory. Implement it
**in place** in `v2/extractor/` (additive, backward-compatible — worker A confirmed) rather than forking a
parallel tree, so the proven core is reused and v1 experts keep working. `SCHEMA.md`/`EXTRACTOR-SPEC.md` get a
"2.0" section, not a rewrite.

## 1c. Learnings from the CWE proof run (2026-07-18) — read before scaling
First real mining (`v2/extractor/appsec_mine.py` on CWE, 120 software pairs → 228 facts, 118 with verbatim
code). What we learned:

1. **The pipeline works.** Extractor 2.0 produces clean code-carrying facts; the verbatim-grounding
   (substring-modulo-whitespace, never `canon()`) held and enforced the "don't change code" rule. Best facts:
   HttpOnly cookie, `window.open` opener, `strcpy`→bounded, SQL-injection, even CWE-1427 LangChain
   prompt-injection — the diff IS the fix.
2. **Source-targeting applies INSIDE CWE.** CWE is a mixed catalog: security + **hardware (Verilog/VHDL)** +
   **code-quality** (CWE-1061 "declare members private", CWE-1106 "use a named constant") — the 1000+ range is
   hardware/quality-heavy. Linear mining by ID gives volume with uneven *bite*. Fix: mine a **curated
   security-CWE set** (Top 25 + OWASP mappings + injection/crypto/authz/memory), not the whole catalog.
3. **Hardware leaks at TWO levels.** A weakness-level software-language filter is not enough — a weakness with
   *both* a software and a Verilog example still emits a Verilog fact. Need a **per-fact** hardware-lang drop.
4. **"Has bad+good code" ≠ "bites".** Some code-quality CWEs pass the code filter but aren't landmines a model
   gets wrong by default. The real gate is the **behavioral value function** ("does the base model emit the
   insecure pattern?") — that's a GPU/model step for phase 5; curated targeting is the cheap proxy until then.
5. **Doors get mis-assigned by the LLM** (CWE-1061 → auth-session). Curated targeting + hand-review needed;
   consider deriving/validating the door from the CWE→door map rather than trusting the model.
6. **~15% of facts rejected for an ungrounded quote.** The anti-hallucination gate is strict (good). A
   **repair pass** (snap the quote to the nearest source line, like v1 `repair.py`) would recover facts whose
   only flaw is a paraphrased quote — worth adding.
7. **Small robustness fixes** that bit: coerce out-of-enum `type` (model invented `RACE_CONDITION`); Windows
   console is cp1252 (ASCII-only in print); log malformed-JSON chunks instead of silently dropping.
8. **Curated CWE is code-SPARSE (36/245 carried verbatim code).** Classic security CWEs put the fix in
   mitigation *text*, not a paired Good code block → they correctly become **text landmine facts**. This
   validates the multi-source design: **CWE = taxonomy + text landmines + its few code pairs; the verbatim
   bad/good CODE density comes from the sources built AS pairs — SEI CERT (Noncompliant/Compliant), CodeQL
   (qhelp vuln/fixed, 1,472), OWASP Cheat Sheets.** Do not force code onto CWE; get code from the right source.
   Result so far: **245 high-bite security facts, 111 CWEs, 0 hardware** = a strong CWE base to build on.

**Superseded (2026-07-18):** the counts above were the first CWE-only slice. The completed, audited bank
across all seven sources is **3,984 facts, 1,075 with verbatim code** (final per-source counts — CWE 259/44,
CodeQL 1,416/831, SAST 208/112, MASTG 546/56, RustSec 66/2, crypto-net 546/0, OWASP 962/75 — are in
`EXTRACTOR-2.0.md` §2).

## 2. Schema change (the core decision)

Add to the fact row:

```jsonc
"code_bad":  "verbatim vulnerable / wrong-usage snippet from the source, or null",
"code_good": "secure / correct-usage snippet (may be model-authored), or null",
"lang":      "python | c | bash | ...   (for fenced rendering)"
```

Decisions and why:
- **Two named slots (`code_bad`/`code_good`), not one blob.** The value of this domain is the *contrast*.
  Named slots let the renderer label WRONG/CORRECT, let retrieval keyword-derive from both, and let a fact
  carry only one side (pure correct-usage example = `code_good` only).
- **New `type` value `PATTERN`** — a vulnerable→secure pair is not a breaking change, so forcing it into
  REMOVED/REPLACED/CHANGED corrupts the type-vs-`new` logic. `PATTERN` is exempt from the `new`-presence gates.
- **New `why_it_bites` value `insecure-default`** — "the idiomatic/obvious code is exploitable." Without
  adding it, `extract.py` silently coerces it to `silent-failure` and the security framing is lost.
- **`old` becomes optional for `PATTERN`** (a correct-usage example has no "old form"); require instead that
  at least one of `code_bad`/`code_good` is present.
- **Provenance fields land now** (`source_url`, `source_date`/CVE id) — security facts go stale when a vuln
  is patched; currency matters more here than anywhere (see the ldap3 lesson in BLUEPRINT).

### The anti-hallucination anchor, for code
The verbatim-`quote` machine uses `canon()` which **lowercases and deletes all punctuation** — fatal for
code (`shell=True` vs `shell=False`, `==` vs `=`). So:
1. **Keep `quote` as a prose anchor, unchanged** — every PATTERN fact still carries a verbatim prose quote
   validated by `canon()`. Proves the *claim* is real even when code is reconstructed.
2. **`code_bad` gets a separate code-aware grounding check** — a normalize-whitespace-but-preserve-
   everything-else comparator (never `canon()`): must be a source substring modulo insignificant whitespace.
3. **`code_good` (the fix) may be model-authored** → not required to be a source substring; instead
   **syntax-gate** it (`compile()` for Python; bracket/quote balance otherwise). Flag failures for hand-read,
   never silently drop. A fix that doesn't parse is worse than none.
4. `repair.py` must **never** touch `code_bad`/`code_good` (snapping a multi-line block to one source line
   corrupts it). It already only rewrites `quote`; just confirm code fields pass through.

---

## 3. What changes in the code — EXTRACTION side (`v2/extractor/`)

**Superseded (2026-07-18):** the table below planned in-place edits to `extract.py`/`check.py`/`dedupe.py`.
The actual build instead centered the mining step on one shared module, **`appsec_core.py::run()`**
(extract → code-ground → repair quote → assign door → dedupe), called by thin per-source adapters
(`codeql_mine.py`, `appsec_sast.py`, `appsec_owasp.py`, `appsec_mastg.py`, `appsec_rustsec.py`,
`appsec_mine_crypto_net.py`, `appsec_mine.py`) rather than fired as parallel opaque agents — see
`EXTRACTOR-2.0.md` §2. The row-by-row intent below (code fields, grounding, PATTERN type) mostly carried
through; row 7 (dedupe) was specifically overturned — see the note after the table.

| # | File → function | Change | Risk |
|---|---|---|---|
| 1 | `extract.py` → `TOOL`/`SYS` | add `code_bad/code_good/lang` to tool props; add `PATTERN` to type enum + `insecure-default` to why enum; drop `old` from required; prompt: emit PATTERN when source shows vuln+fix, copy `code_bad` verbatim, defensive framing | Low, additive |
| 2 | `extract.py` → `ask()` JSON parse | **replace the silent `except: pass`** with logged salvage of malformed JSON. Multi-line code is the worst case for LLM JSON validity, and today one bad snippet silently discards the whole chunk | **High value / med risk** |
| 3 | `extract.py` → `main()` derive block | gate the `type`-vs-`new` coercion on `type!="PATTERN"`; accept `insecure-default`; stamp `lang`; pass code fields into the row | Med — the coercion will mangle PATTERN facts if not gated |
| 4 | `extract.py` → `derive_from_fact()` | mine symbols from `code_bad/code_good` (so `os.system`, `shell=True`, `yaml.load` become retrievable keywords); raise cap 8→12 | Low |
| 5 | `check.py` → `check()` | add `PATTERN`/`insecure-default` to enums; exempt `old` for PATTERN; skip REPLACED/REMOVED `new`-gates for PATTERN; **add `code_bad+code_good` to the `hay` string** (or code-derived keywords fail validation); add `code_grounded(code_bad)` + `code_good` syntax check | **High risk of silent fact loss — build, run, READ the rejects by hand** |
| 6 | `check.py` → new helpers | add `code_norm`/`code_grounded`; **never** route code through `canon()` | Med — whitespace rules need tuning on real advisories |
| 7 | `dedupe.py` → `main()` | add code tokens to `_btok`/`_sig`; **skip the quote/claim flag for PATTERN** (else every code fact is auto-quarantined to `.review.jsonl`); fold a code hash into the cluster signature (else distinct examples merge) | Med — without this, code facts are quarantined or over-merged |
| 8 | `SCHEMA.md`/`EXTRACTOR-SPEC.md`/`BLUEPRINT.md` | document the new fields, PATTERN, the code-grounding rule, and "code reaches the model only via adapt-time `text`/`code` payload" | Low |

**RETIRED (row 7, per `EXTRACTOR-2.0.md` §4):** folding a code hash into the dedupe cluster signature was
tried and rejected — **a shared `code_bad` is NOT a duplicate signal.** Sibling facts (e.g. different CodeQL
queries) reuse one boilerplate code sample to teach different lessons; keying dedupe on code wrongly cut 251
distinct facts. Actual cross-source dedupe is **prose-only** (`appsec_merge.py`, Jaccard on subject+truth).

---

## 4. What changes in the code — BAKE + SERVE side (`v2/bake/template-brain-v3.1/`)

Hard measurements the worker took from the real GitChameleon artifacts (4,167 facts, 2.73 MB template):
**the inverted index (`fb_post`) is 70% of the template; fact text is only 27%.** That single fact drives
the whole design: **keep code OUT of the index, carry it as a separate payload.**

| # | File → function | Change | Risk |
|---|---|---|---|
| P1 | `adapt_expert.py` → main loop | map `r["code_good"]`/`code_bad` into the bank record as a new `code` field; add `normalize_code()` (keep `\n`/`\t`, strip other control chars, **cap ~15 lines** at bake time) — do NOT append code into `text` | none structural |
| P2 | `bake_index.py` → `build()` + `main()` | build a parallel `code` list aligned to fact-id order; return + serialize it (`__CODE__` via `json.dumps(..., ensure_ascii=False)`); **keep it out of `df`/`keys`/`terms`/gate** (verified `strong_keywords`/`auto_phrases` read only `text`) | Med — never feed code to the indexers |
| P3 | `inserts/gemma4_idx/fb_preloop.jinja` | add `{%- set fb_code = __CODE__ -%}`; register `__CODE__` in the anchor-consume list or the bake assert fails | Low |
| P4 | `fb_gen.jinja` **and** `fb_toolmsg.jinja` | tiered injection: inject the **corrected** snippet only for the **top 1–2 ranked facts** (`slot < 2`), guarded by `fb_code[id] != ""` so text-only facts are byte-identical. Edit **both** (duplicated logic) | Med — forgetting one breaks the real-tool lane |
| P5 | `verify_render.py` / **`parity.py`** / `render_retrieval.py` | mandatory offline gates: render clean on all probes ×2 thinking modes; **parity test that json-dumped strings with embedded `\n`/backticks/quotes retrieve+render identically under jinja2 and minja** (the one genuinely unproven escaping element); confirm injected context actually contains the code lines | **parity is the top technical unknown** (low probability, high impact) |

Why code survives to the model unescaped: injection goes through `format_argument(..., escape_keys=False)`
which passes the string **raw** — newlines and backticks reach the model. The only escaping that matters is
`json.dumps` at bake time (newline→`\n`), which is already correct. Text already round-trips json-escaped
quotes in-engine today; embedded-newline array elements are the one delta to parity-test.

### Size & delivery (measured, not guessed)
- **Single corrected snippet / fact @ 4,000 facts ≈ 4.5 MB template.** **Both bad+good ≈ 6.3 MB.**
- Render latency is measured **flat to 5.06 MB**; beyond is unmeasured. → **Default: inject a single
  corrected snippet (~4.5 MB, inside the tested-flat zone).** Make bad+good opt-in and re-measure latency.
- **Route: ship a GGUF baked for `llama-server` (`--route llamacpp`, 1 GiB cap, errors loudly).** LM Studio
  raw-load is dead above 980 KB (F-053 silent sentinel) — never a route here. Keep the GGUF's embedded
  metadata template a small SAFE sentinel; deliver the big template via `--chat-template-file` /
  `serve_factbank.ps1`.

### Injection count — raise `FB_MAX` (5) but make it dynamic (owner, 2026-07-18)
`FB_MAX = 5` is too low for chained security tasks (a "complete secure auth flow" needs hashing + JWT +
session + CSRF + TLS facts at once, 8-12). Token budget is NOT the constraint (12 facts + 3 code snippets ≈
~1,000 tokens at 16k ctx). The real limit is **attention dilution + over-deference** — a flat raise to 15
injects low-relevance facts (ranks 6-15) that bury the decisive one and risk force-fitting an inapplicable
"fix." **Decision: don't flat-raise — go dynamic:** (1) lift the ceiling to ~10-12; (2) gate by a
relevance-SCORE floor so the actual count varies (simple Q → 1-2, chain → up to ceiling; weak matches never
inject → no dilution); (3) attach CODE only to the top ~2-3 facts (recall up, token/attention cost bounded).
Matters MORE in thinking-ON mode (more facts = more for reasoning to argue away). Tune exact numbers
(ceiling, threshold, code-cap) by measurement with `render_retrieval.py` on real chained questions. Small
additive change to `bake_index.py` (`FB_MAX` + score threshold) + the `fb_gen`/`fb_toolmsg` injection loop.

### Serving behavior
- **Ship thinking-OFF** (chain-of-thought reverts habit-reversal facts to the prior and spirals to empty;
  code is *more* to re-litigate). Offer authority+thinking as a **targeted second pass on the misses**.
  **Superseded (2026-07-18, `EXTRACTOR-2.0.md` §6):** the served appsec test settled on the OPPOSITE
  default — **authority framing + thinking-ON** is now the cure for reasoning-reverts-the-fact and is the
  default posture, not a targeted second pass. Also new: retrieval uses **HyDE double-key** (prompt +
  the model's own draft) because an insecure-by-default prompt often doesn't contain the security keyword.
- **Inject the corrected snippet only by default** — with the vulnerable code in context the model can copy
  it. If both are shown, label `WRONG:` / `CORRECT:` unambiguously. This is the biggest new behavioral risk.
- Gemma-native sampling unchanged (temp 1.0 / top_k 64 / top_p 0.95 / **min_p 0.01**); `--ctx-size 16384`+.

---

## 5. Sources & content

### 5.0 The strategic reframe (decide this first)
This expert **breaks the project's default thesis** on purpose. Every prior security bank was a
*library-migration* bank (post-cutoff API churn × low training representation). CWE/OWASP/CERT are the
opposite — stable, canonical, *heavily* trained-on; a naive "OWASP Top 10" bank fails our own value function
because the base model can already recite the rule.

**The reason to build it anyway:** the landmine here is **behavioral, not recency**. LLMs *know* the rule
abstractly yet *write insecure code by default* — they emit `hashlib.md5(pw)`, `pickle.loads(untrusted)`,
`verify=False`, `eval(user)`, `jwt.decode(..., algorithms=None)`, f-string SQL, unprompted. That is exactly
our two most valuable fact classes — **silent failure** (wrong-but-runs) and **habit reversal** (the trained
default is the wrong one). The bank's job is to **fire at generation time and flip the default** the instant
a vulnerable pattern is about to be produced.

Consequences: (a) **bank facts that BITE, not facts that are true** — a fact earns its place only if the
base model's *default code output* is insecure; score by "does base emit the bad pattern?" (a new probe set,
same manual discipline). (b) Lean into the slices where currency *also* helps (crypto/TLS: Argon2id params,
TLS 1.3-only, MD5/SHA-1 forbidden, PQC; **ASVS 5.0** and **OWASP Top 10:2025** are genuinely post-cutoff).
(c) The BLUEPRINT currency caveat bites hard — verify crypto/TLS facts against *current* guidance.

**Proposed name: `gemma-4-<size>-appsec-expert`** (domain term `appsec`), framed as an
**"insecure-by-default / secure-coding landmine"** expert.

### 5.1 Sources — FULL SET (owner 2026-07-18: mine them ALL, license permitting)
Decision: build the broad multi-language security+networking expert, not a web/C/Python subset. Tier A is the
license-clear, code-rich core to mine first; B/C/D add language breadth, authority, and freshness. The only
things that stay out are the ones that legally cannot ship.

**Note (2026-07-18):** per `EXTRACTOR-2.0.md` §2, the adapters actually built and mined this run are CWE,
CodeQL, SAST (Bandit+gosec), MASTG, RustSec, crypto-net (NIST/RFC/Mozilla), and OWASP Cheat Sheets — **SEI
CERT does not appear** in the shipped 3,984-fact bank's source list below. Left as planned (Tier A); flag
for the owner rather than assumed dropped.

**Tier A — core (start here; license-clear, code-dense):**
| Source | Why | Code | License | ~facts |
|---|---|---|---|---|
| **MITRE CWE (XML)** | taxonomic spine; native bad-code + mitigations | ✅✅ | royalty-free, commercial OK | 1,500–2,500 |
| **SEI CERT C/C++/Java/Android** | Noncompliant/Compliant pairs; memory-safety | ✅✅✅ | CMU permission (short quotes, re-author, owner sign-off) | 800–1,500 |
| **OWASP Cheat Sheet Series** | highest insecure-by-default hit rate; web pairs | ✅✅ | CC BY-SA | 600–1,000 |
| **CodeQL query pack** (`github/codeql`) | qhelp + fixtures = vuln/fixed pairs | ✅✅ | MIT (queries) | 400–600 |

**Tier B — language/ecosystem breadth (permissive SAST catalogs + framework guides):**
| Source | Fills | Code | License | ~facts |
|---|---|---|---|---|
| **Bandit** (PyCQA) | Python insecure patterns | ✅ | Apache-2.0 | ~150 |
| **gosec** (securego) | Go insecure patterns | ✅ | Apache-2.0 | ~150 |
| **ESLint security plugins** | Node/JS | ✅ | MIT | ~100 |
| **RustSec advisory-db** | Rust | ~ | CC0 | ~200 |
| **OWASP MASVS / MASTG** | mobile (Android/iOS) | ✅ | CC BY-SA | ~300 |
| **OWASP API Security Top 10** | API-specific | ~ | CC BY-SA | ~100 |
| **Brakeman** (Ruby/Rails) | Ruby | ✅ | ⚠️ verify license before mining | ~100 |

**Tier C — authoritative & free (the backing + the "good-code" library side):**
| Source | Why | License |
|---|---|---|
| **NIST SP 800-series** (52/63/131A/175B) | authoritative crypto/auth/TLS/identity | **US-gov public domain** |
| **Curated security RFCs** (TLS 1.3 8446, JWT BCP 8725, OAuth BCP 9700, cookies, HSTS) | protocol habit-reversals | IETF TLP — short quotes |
| **Mozilla Server-Side TLS** | current secure-config | MPL 2.0 |
| **Secure-lib docs** (Google Tink, libsodium/PyNaCl, pyca/cryptography, argon2-cffi, defusedxml) | idiomatic `good_code` fixes stay current | Apache-2.0 / ISC / permissive |

**Tier D — coverage & freshness:** OWASP **ASVS 5.0** + **Top 10:2025** (CC BY-SA; the coverage spine, 2025
recency); **GHSA** (CC BY 4.0; freshness/cross-ref). Optional small `threat-context` door from **D3FEND**
(defensive-by-construction) if breadth is wanted.

**EXCLUDED — cannot ship (not a scope choice, a license fact):** **Semgrep registry** (Commons Clause / no
redistribution), **CIS Benchmarks** (CC BY-**NC** vs the commercial gemma license), **PortSwigger Academy**
(proprietary — use for test-question *inspiration* only), raw **NVD/CVE** (too thin — via GHSA cross-ref only).

> Before mining each Tier B/C source, confirm its license + code density + attribution string (most are
> locked above; **Brakeman** and any newly-added source need a check). Get the pattern from a permissive
> source or author it ourselves if a source turns out restrictive.

### 5.2 Door structure (10 doors, soft-gated)
`injection` · `web-appsec` · `crypto` · `auth-session` · `memory-safety` · `deserialization-input` ·
`secrets-config` · `network-security` · `concurrency-race` · `api-supply-chain`. Bucketed by shared
retrieval vocabulary + audience (the bundling law). **Gate-alias law with a security twist:** the *insecure
symbol the model is about to emit* must open the door — `md5`, `pickle.loads`, `verify=False`, `alg:none`,
`eval`, `system(` become gate aliases, because that token is exactly what appears in the model's draft.

### 5.3 Fact taxonomy (security-with-code) — supersedes `old`/`new` with `bad_code`/`good_code`
Fields: `type` (INSECURE_DEFAULT | HABIT_REVERSAL | SILENT_FAILURE | DEPRECATED_CRYPTO | MISSING_CONTROL) ·
`weakness` (CWE/CERT id) · `subject` · **`bad_code`** (minimal illustrative mistake) · **`good_code`**
(always present — a bad-only fact is rejected) · `truth` · `why_it_bites` · `quote` (short verbatim anchor) ·
`keywords{from_fact, associative}` · `door` · `source` · `license_note` · `lang` · `id`. This maps cleanly
onto the §2 schema (`bad_code`≈`code_bad`, `good_code`≈`code_good`); reconcile the two names during
implementation.

**Code is DATA-DRIVEN, not optional (owner, 2026-07-18).** It's not a per-fact toggle we choose. The rule is
simple: **if the source has a real code example for the fact, we capture it; if not, it's just a normal text
fact** (exactly like today's facts, missing nothing). We never fabricate or force an example. It's *all about
the data* — the mining/source decides whether a fact has code. The only ETHICAL constraint: **if a fact
carries `code_bad`, it MUST also carry `code_good`** (never ship a vulnerable snippet without its fix; reject
bad-only). So a fact is: normal text, or text + good-code (correct usage), or text + bad+good pair. Worker C wrote out four concrete example facts (CWE-89 SQLi, CWE-916 password hashing,
CWE-502 pickle, CWE-347 JWT `alg:none`) — use them as the extractor's few-shot seeds.

### 5.4 Ethical / legal guardrails (hard gates, encoded in `check.py`)
1. **Defensive-only, enforced by schema:** code is optional per fact, but **a fact with `bad_code` must also
   have `good_code`** (never ship the vulnerable snippet without its fix — reject bad-only). `bad_code` is a
   minimal illustrative mistake, **never a working exploit/payload/shellcode or an attack on a real target**.
   Reject any fact whose `bad_code` is operational rather than illustrative.
2. **No weaponization even from defensive sources** — CAPEC/ATT&CK mined as detect+mitigate only; prefer
   D3FEND; skip attack-runbook text.
3. **Per-source attribution in every fact** (`license_note`) + a bundled `THIRD-PARTY-NOTICES` in the model
   card: MITRE "reproduced with permission"; OWASP CC BY-SA (+ShareAlike note); SEI CERT credit CMU/SEI
   (short quotes, owner sign-off); CodeQL MIT; RFCs short-quote only; Mozilla MPL-2.0.
4. **Hard-exclude Semgrep + CIS** (license-incompatible). Get the pattern from a permissive source or author
   it ourselves.
5. **Currency check for crypto/TLS/network facts** before bake (stale "use X" corrects toward wrong).

---

## 6. Evaluation plan (how we prove it — and prove the CODE specifically helps)

Reuse both proven rigs: the security **landmine** rig (`test_secnet.py`, hand-scored, thinking-ON+authority,
Gemma-native — works everywhere, no Docker) as the backbone, and the GitChameleon **execution** idea for the
Python-executable subset (with a security twist: **property/negative tests**, because vulnerable code runs
fine).

- **Test set: ~75–90 hand-authored questions**, ≥3 per door, spanning appsec / crypto / memory-safety /
  network, in three difficulty gears (single-landmine / silent / multi-fact chain) **and** tagged by task
  type: T1 rewrite, T2 generate, T3 explain, T4 semantics. Plus per-door **gate-vocab probes** (the
  "Volatility 3" lesson) and **~15 controls** including a **no-fact-applies over-deference probe** and a
  mainstream-already-known regression guard.
- **Metrics:** keep USES (fact reached the answer) and CODE (code obeys it); the **USES−CODE gap is the
  finding**. Add a 5-point security rubric — IDENTIFIES / NAMES(CWE) / SECURE-CODE / AVOIDS /
  **NO-NEW-VULN**. Headline = **SECURE@1** = AVOIDS ∧ SECURE-CODE ∧ NO-NEW-VULN.
- **The core novel measurement — three-arm ablation** (identical retrieval, only the injected payload
  differs): **BASE** (no bank) vs **BANK-TEXT** (prose fact, code stripped from injection) vs **BANK-CODE**
  (full fact + code pair). **Code contribution = SECURE@1(BANK-CODE) − SECURE@1(BANK-TEXT)**, sliced by task
  type — expect the code to add most on T1/T2 (code-out) and ~0 on T3/T4. Run on both 12b and 26b (lift
  shrinks on 26b — stronger base).
- **Execution scoring, tiered:** Tier-E (Python: cryptography/urllib3/paramiko/PyYAML/subprocess) via a
  uv-venv property-test harness (adapt `run_tests.py`); Tier-S (C/OpenSSL/eBPF/volatility3 — no Docker here)
  hand-read. State the split up front (the honest PROVENANCE analogue).
- **Safety of the eval:** every question is remediation/analysis, never weaponization; NO-NEW-VULN + the
  no-fact-applies controls are the headline safety metrics (authority framing must not force-fit an
  inapplicable "fix" into insecure code).

---

## 7. Phased build plan (each phase gated on owner go for anything GPU)

1. **Schema + extractor changes** (no GPU) — implement §2–§3, run ONE security source (e.g. a CWE slice with
   code) end-to-end, **read every kept and rejected fact by hand**. Proves the code path produces grounded
   facts before we scale.
2. **Bake + parity** (no GPU) — implement §4, run `verify_render` + the new `parity.py` code fixtures +
   `render_retrieval` to prove code reaches the model in-engine on a small bank.
3. **Content build** (no GPU, cheap DeepSeek) — mine the ranked sources (§5) to 4,000+ facts; dedupe;
   hand-verify; author the ~75–90 question test set + property tests.
4. **Three-arm bake** (no GPU) — BASE / BANK-TEXT / BANK-CODE for 12b and 26b (6 configs).
5. **Evaluate** (GPU — **explicit permission required**, one model at a time, free VRAM after each, never
   touch the user's model) — run the matrix, hand-score, produce the SECURE@1 table + the code-delta.
6. **Publish** if the result holds — cards, papers, HF + GitHub, per the established flow.

**Status (2026-07-18):** phases 1 and 3 are DONE — see `EXTRACTOR-2.0.md`. Step 3's "hand-verify" turned out
to mean a MANDATORY two-pass audit (currency-verify + adversarial correctness audit, ~3.8% of facts found
wrong/stale and remediated), which ran before rather than after a bake. The bank is now **PRE-BAKE**: phase 2
(bake + parity) and phase 4 (three-arm bake) have not run; phase 5 (evaluate) still needs explicit GPU
permission per the three hard rules.

---

## 8. Top risks (ranked)

1. **`check.py` silent fact loss** — every gate there drops facts; a too-strict code check can quietly kill
   the whole point. Build, run, READ rejects.
2. **minja escape parity** on embedded-newline string literals — low probability, high impact; the one hard
   technical unknown. Gate with `parity.py` before any bake.
3. **Model copies `code_bad`** — inject corrected code only, label WRONG/CORRECT.
4. **Over-deference** — authority framing force-fitting an inapplicable "fix" into *insecure* code. The
   security-specific danger; the no-fact-applies controls + NO-NEW-VULN metric exist to catch it, and a
   regression there is a **shipping blocker, not a footnote**.
5. **Currency** — a PoC for a patched CVE is stale; carry provenance and verify against current guidance.
6. **Size beyond the proven envelope** — default to single-snippet (~4.5 MB, tested-flat); re-measure if
   bad+good (~6.3 MB) is used.

---

## 9. What needs the owner's go
- **The reframe (§5.0):** agree this is an **"insecure-by-default" appsec expert** (behavioral landmine),
  not a migration bank — and the name `gemma-4-<size>-appsec-expert`. This is the biggest decision.
- **Schema:** approve `bad_code`/`good_code` + `PATTERN`/`INSECURE_DEFAULT` types, and the code-grounding
  rule (prose `quote` stays the anchor; `code_bad` source-substring modulo whitespace; `code_good`
  syntax-gated).
- **Delivery:** "single corrected snippet by default" (~4.5 MB, llama-server route), bad+good opt-in.
- **Scope:** 12b + 26b only; 4,000+ facts; the **10 doors** in §5.2; sources 1–4 first (CWE, SEI CERT,
  OWASP Cheat Sheets, CodeQL), ASVS/RFCs/Mozilla for coverage + networking; Semgrep + CIS excluded.
- **Sequencing:** everything through phase 4 is **no-GPU** and can proceed on approval; **phase 5
  (evaluate) needs explicit GPU permission** per the three hard rules.

**UPDATE (2026-07-18):** this line is now stale for phases 1 and 3 — code was written and facts were
extracted (no GPU touched, so the hard rule was still honored). See `EXTRACTOR-2.0.md` for what shipped:
the appsec expert is **built, audited, and pre-bake**; nothing has been baked or published yet, so phases
2/4/5/6 below are still pending exactly as described.

*This plan is research + design only. No code changed, no facts extracted, no GPU touched.*
