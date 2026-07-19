# The Structured Extractor — Main Blueprint (domain-agnostic)

How to turn any fast-moving software domain into a rich, retrievable **landmine fact bank**.
Domain-independent: the same design built pandas, k8s, terraform, and the AI-ML expert (817 facts,
11 doors). Everything below is **measured or hand-read**, 2026-07-15.

---

## Thesis
**The LLM does the meaning; dumb code verifies every field.** Invert the old rules-miner: instead
of rules extracting and an LLM polishing, the LLM extracts into a **strict schema** and code checks
each field — above all that the `quote` is **verbatim in the source** (the anti-hallucination anchor).

## The pipeline
```
FIND            pick the RIGHT source doc (migration guide, not release notes)
  → extract     LLM fills a strict schema via function-calling; code derives type + keywords
  → repair      re-ground any paraphrased quote to a real source line (checker, no LLM)
  → check       raw checker; verbatim-quote anchor is the gate
  → assemble    facts become a door (namespace) in the bank
```
Retrieval on the bank: **soft doors + classic pointers + richer keywords + MMR** (see below).

> **Which retriever produced the benchmarks?** The recipe on this page is the **Served-Loop** Python
> prototype. The **baked GGUF** that produced the Gemma 12b/26b and Security pass@1 numbers used a
> simpler **hard-gated, single-query inverted index** (Baked-Index) — NOT this recipe. See
> [`../ARCHITECTURES.md`](../ARCHITECTURES.md) for the three distinct systems and the capability matrix.

> **2026-07-18 rebuild — `EXTRACTOR-2.0.md` is now canonical for mining/repair/dedupe/verification/retrieval
> specifics.** That pass (proven on the built + audited **appsec expert**, 3,984 facts / 1,075 with verbatim
> code; since SHIPPED — baked ×3 sizes × both thinking editions, published) added: code lives IN the fact (`code_bad`/`code_good`); mining runs
> through one shared `appsec_core.run()` engine with thin per-source adapters (retires the parallel-agent
> mining approach); repair uses sentence-boundary verbatim grounding (see the retirement note on item 4
> below); cross-source dedupe is prose-only — a shared `code_bad` is explicitly NOT a duplicate signal;
> and a MANDATORY adversarial correctness audit now runs before any bake (grounding proves a quote is REAL,
> not CORRECT — ~3.8% of a fully verbatim-grounded bank was still wrong/stale). Retrieval also gained a
> **HyDE double-key** mode (retrieve on the prompt AND the model's draft) for insecure-by-default domains
> where the prompt never contains the landmine keyword. Where this page disagrees with `EXTRACTOR-2.0.md`,
> **2.0 wins.**

---

## WHAT WORKS

| # | What | Evidence |
|---|---|---|
| 1 | **Schema DESIGN beats output mode.** Don't ask the model for what code can derive: derive `type` from presence of `new`, derive `from_fact` keywords from old/new/truth. | k8s control **35% → 96.5%** clean, same model/prompt. |
| 2 | **Function-calling for shape.** DeepSeek has **no** strict `json_schema` mode (verified); function-calling enforces required fields + enums. | probe returned "response_format type unavailable"; tool-call works. |
| 3 | **Verbatim `quote` anchor = anti-hallucination.** A fact whose quote isn't in the source is dropped. On messy prose it correctly drops paraphrases. **But it proves the quote is REAL, not CURRENT-VERSION-TRUE (see Caveats).** | pydantic messy: the 1 hallucinated fact was the 1 caught. |
| 4 | **Repair pass (snap quote to nearest real source line).** Recovers facts whose quote was paraphrased, only if the fact's own symbol is in that line. **RETIRED 2026-07-18:** this ellipsis-only-split / ≥3-word-guard / 0.6-threshold method was too strict (wrongly rejected good facts, e.g. `"allUsers"`) and was replaced by sentence-boundary verbatim grounding — see `EXTRACTOR-2.0.md` §3. | pydantic messy **81.5% → 97.8%**; ~8/9 snaps exact. |
| 5 | **Two-tier keywords.** `from_fact` (code-derived, always grounded) + `associative` (LLM: the "could-be" search phrases NOT in the fact, e.g. "connect to provider"). | fixed the "min_length not findable" retrieval miss. |
| 6 | **Migration guides >> release notes** — source targeting is the single biggest lever. | AI-ML core went from 18 → real facts once guides were used; `use_auth_token`, `ChatCompletion.create` only appear in guides. |
| 7 | **Banks stay RICH, not model-gated.** One bank serves 3b/12b/30b, so never drop "what the model knows." | owner decision; a 3b lacks a 12b's knowledge. |
| 8 | **Retrieval recipe:** soft doors (multiply matching door's score, never exclude) + classic pointer chains (bucket by lib+namespace) + richer keywords + **MMR** (dedup near-duplicates). Door comes from the **draft/context**, not query keywords. **This is the Served-Loop system; the baked GGUF benchmark used the simpler hard-gated Baked-Index — see [`../ARCHITECTURES.md`](../ARCHITECTURES.md).** | 7/8 hand-read hits at 508 facts / 4 doors, zero cross-door leaks (Python prototype). |
| 9 | **Cost is negligible** (~4¢/session) — extract more/deeper, don't optimise calls. | measured. |
| 10 | **Read the results by hand; the count lies.** | pydantic raw 58% hid ~51 good facts behind 2 checker bugs; vllm "22 rewritten" were marginal. |
| 11 | **Gate aliases: the OLD name of a rename must open the tab (2026-07-17).** The baked-index gate opens on the exact lib token; a stale user typing a NATURAL or OLD name ("BloodHound", "CrackMapExec") opens nothing and gets 0 facts. `gen_gate_aliases.py` derives aliases from each rename fact's OLD name + the lib's natural stem → `bake_index.py --extra-aliases`. | Proven with `bake/…/render_retrieval.py`: bh01 injected 0 facts on all 3 sizes pre-fix, 5 correct facts post-fix. Same class as the volatility3 "Volatility 3" vs `volatility3` gate death. |

## WHAT DOESN'T WORK (tested and rejected)

| What | Why it failed |
|---|---|
| **Rules-based extraction for prose** | Bullet+symbol miner reads changelogs, gets **0** from prose migration guides — where the best landmines live. |
| **Hard doors (route on the top-1 hit)** | A wrong-door top-1 gets amplified to an all-wrong result (fatal misroute). Use **soft** doors, fail open. |
| **`spec` rare-token² weighting** | Didn't fix targeting or dedup; 5 common words still beat 1 rare, even squared. |
| **The concrete-rewrite SECOND pass** | Only 5% of facts are vague, all from release notes; passing the source can't fix a source that's *itself* vague (garbage in, garbage out). Concreteness is an **extraction/source** property. |
| **Landmine-gate (drop what the model knows)** | Over-fits one model; the bank serves all sizes. Cancelled. |
| **`alias` query-expansion table** | Works but redundant once keyword-extraction is rich; a hand-built table to maintain. |
| **llama.cpp/GGUF from release notes** | Gives build/platform noise ("openEuler builds"). Real GGUF landmines live in the **format spec** (v2→v3, removed quant types). |
| **Trusting a pass/fail number as the verdict** | Every count here misled in some way; reading is the verdict (F-065). |

## Caveats / not yet verified
- **The quote anchor proves the quote is REAL, not CURRENT-VERSION-TRUE.** A migration guide is a
  *historical* record; a change it documents can be **reverted** in a later release. **Habit-reversal facts
  about defaults are the risk** — a "default changed X→Y" that a newer version quietly flipped back to X.
  Verify such facts against the library's **current source/docs**, not just the guide — a fact that's
  true-for-an-old-version but wrong-now is *worse than no fact*, because it "corrects" the model to the wrong
  answer. **Proven (2026-07-17):** an ldap3 fact "default `Connection` strategy changed SYNC→RESTARTABLE" was
  a reverted change — current ldap3 defaults to SYNC; the fact was removed before it could mislead. Same
  spirit as SCORE MANUALLY: the checker verifies grounding; a human verifies currency.
  **Formalized 2026-07-18:** "verbatim grounding is sufficient" is now explicitly retired as an assumption —
  currency verification plus a MANDATORY adversarial full-correctness audit (one verifier agent per 100-fact
  batch, every flag re-checked default-reject) runs before any bake. See `EXTRACTOR-2.0.md` §5.
- **WebFetch-sourced docs** (web-only migration guides) are model-*rendered* markdown; facts are real
  but the `quote` anchors against the rendered copy, not the original byte-for-byte. Raw GitHub is purer.
- **Jinja/GGUF parity NOT yet checked.** Retrieval (soft doors, pointers, MMR) is proven in Python only;
  it must be verified in the real llama.cpp engine before any bake (F-050).
- **No completeness meter** — fact count ≠ domain coverage; use a curriculum-derived coverage spec.

## The one law
**Source targeting decides everything.** A perfect extractor on the wrong document yields a bank of
the wrong facts. FIND the migration guide first; extract second.
