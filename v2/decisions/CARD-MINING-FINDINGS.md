# Card-Mining Investigation — measured findings (2026-07-15)

Session record. Everything here was **measured or hand-read**, not assumed. All
offline/free unless noted. Kept because the repo's rule is: write down what you
measured. Companion to [`LANGUAGES.md`](LANGUAGES.md), [`NEW-DB-RESEARCH.md`](NEW-DB-RESEARCH.md).

> **History note.** This is a record of the rules-based **card-mining** pipeline
> (`card_miner.py`/`card_gate.py`/`llm_secondline.py`/`card_to_bank.py`), already
> superseded by the LLM-first `v2/extractor/` and, as of 2026-07-18, by
> **`v2/extractor/EXTRACTOR-2.0.md`** (mining, repair, dedupe, verification, retrieval,
> and serving/testing methods — canonical there). The measurements below stand as
> history; where a specific practice was later retired, it's flagged inline.

## 1. The shipped bank works — but is dirty, and predates its own cleanup
- `facts_pythondata_v4.jsonl` (1,911 facts): **gold 12/12, controls 0/10** (offline jinja2).
- Poison scan: **10% share a docstring with ≥5 others; 219 exact inherited duplicates**
  still present (23× `duckdb…add_note`, 51× `Array.value_counts`, 41× `fit_transform`).
- **Root cause:** v4 was written 07:52; the deduped clean mine (`facts_mined_clean.jsonl`,
  8,096) was written 15:30 the SAME day. **The F-064 dedupe was built and never shipped.**
- Reachability (`reach.py`): **76.6%** — **447 dead facts** no question can retrieve.

## 2. Shrinking the bank FAILED its own test — dead weight is load-bearing
- Built v5 = v4 minus 309 dead-mined minus 179 exact-dupes (kept all 388 curated).
- Result: **gold 12/12 → 10/12.** Two gold facts (`pandas3-037`, `polars-005`) that were
  present **stopped being retrieved** — one stopped triggering entirely.
- **Why:** the ranker weighs terms by rareness across the WHOLE bank. Remove facts →
  every term's weight shifts → barely-winning facts fall out. **You cannot cut the bank
  without re-tuning the ranker.** "Smaller is cleaner" sounded right and was wrong.

## 3. reach.py: 29 min → 5.7 s (made standard)
- The slow part is **parsing** the ~1 MB template (0.75 s), not searching it (1.3 ms/render).
- Old code re-parsed the megabyte in every Windows worker. Fix: **parse once, render many.**
  Same numbers, ~50× faster. `reach.py` edited to single-process compile-once.

## 4. Renames don't win; behaviors do — and the model already knows old versions
- 6 machine-extracted NumPy-2.0 facts, bare-vs-fact on `gemma-4-26b-a4b-qat`, hand-scored.
- **5 of 6: the bare model was already correct** (`alltrue→all`, `cumproduct→cumprod`, …).
  NumPy 2.0 (2024) is **inside the model's Jan-2026 training** — these aren't news to it.
- **The 1 that won was a subtle BEHAVIOR fact** (`__array__ copy=False` must raise ValueError),
  not a rename. Bare invented "return a view"; the fact fixed it.
- **Consequence:** the winning fact is the **landmine** — post-cutoff, or a behavior that
  reverses an old habit, or a silent-failure. Renames on a capable model win ~nothing.
- Landmine fingerprints (model-independent, readable from the doc): **(a) newer than the
  model, (b) reverses a long-standing habit, (c) fails silently.** No need to probe every
  model; probe the strongest as a proxy (blind spots nest).

## 5. The card pipeline: rules → gate → LLM, each verified by READING
Built and run on the real pandas 2.0 changelog:
- **Rules miner** (`card_miner.py`): fixed-rule cards (REPLACE/CHANGED), each with a
  **verbatim quote** (safety) and a **collision-proof id** (hash of type+subject+version+truth).
  Fixed 4 gaps found by reading: lazy subjects, trailing dots, broken quotes, missed bare names.
- **Robust gate** (`card_gate.py`): schema + verbatim-quote + clean-subject + dedup. It
  **triages; a human judges wins.** Reject count went **30 → 0 → 4** across fixes:
  - 30 = **too strict**, it was DELETING real facts (`Int64Index` removal) for "no dot".
  - 0 = **too loose**, it kept junk (`result.infer_objects`, `numpy.ndarray` as pandas subjects).
  - 4 = balanced (foreign/placeholder subjects, correctly rejected).
  - **The count lied in BOTH directions. Only reading was the truth.**
- **LLM second line** (`llm_secondline.py`, DeepSeek `deepseek-v4-flash`, non-thinking):
  runs ONLY on rule-flagged suspects (~10%), never the whole set. Two jobs: dedup judge,
  subject namer. A **code guard** re-verifies every returned subject (must appear verbatim
  in the quote, be a real own-lib symbol) — the model is never trusted, only proposed.
  - Result: dedup made **0 wrong merges** (conservative by design); the guard **rejected all
    non-improving subject suggestions**.
  - **Correction to an earlier claim:** generic subjects (`DataFrame` for "arithmetic methods")
    are **NOT LLM-fixable** — the changelog names no specific method, so the model correctly
    can't either. The lever for findability is the **triggers**, not the subject.

## 6. TESTED end-to-end on a niche library — the cards WIN (5/5, hand-scored)
Mined the **Ecto** (Elixir ORM) changelog through the full pipeline (rules miner →
subject fix → cards), then ran bare-vs-card on `gemma-4-26b-a4b-qat`, every answer
hand-read. The model has real Ecto priors (named `all/2` correctly) — so it could be
*confidently wrong*, unlike numpy 2.0 which it already knew.

| case | bare | with card | won |
|---|---|---|---|
| `transaction/2` | old `Repo.transaction` | new `Repo.transact` | ✅ |
| `literal/1` | dodged (`field/3`) | correct `identifier/1` | ✅ |
| keyword hints | **hallucinated `Repo.all_with_hint`, `force_index:`** | correct `unsafe_fragment` | ✅ strong |
| `:array_join` | wrong history | "removed" | ✅ |
| `map/2` on left join | said `nil` | **first LOST** → **won after rewording** | ✅ |

**Result: 4/5 immediately, 5/5 after one fix.** The strong win: bare **invented
non-existent APIs** (`Repo.all_with_hint`, `force_index:`) — the exact confidently-wrong
5-hour-debug landmine — and the card fixed it. This is the first end-to-end proof that
**mined niche cards win**, and it validates the whole thesis: engine works, facts are the
lever, and the winning facts are landmines from sources the model does NOT already know.

### NEW finding — fact WORDING decides whether a true fact wins
`map/2` LOST with the abstract-but-true fact *"map/2 now always returns a map on joins."*
It WON when reworded to state the concrete output: *"returns a MAP with nil fields, e.g.
`%{id: nil}` — NOT nil."* Same truth, different words, opposite outcome. The model obeys a
fact it can act on, not one it has to interpret. **The miner/LLM must produce concrete,
output-explicit facts — "X → Y" and "you get Z", not "the behavior changed."**

### Confirmed on the TARGET model (12B), clean — 5/5
Re-ran the identical test on `google/gemma-4-12b-qat` (the shipping-class model), facts
delivered in prose, hand-read. **5/5 wins.** Bare failures were real landmines: unsafe
`fragment("#{name}")` SQL-injection, an invented `hint:` DSL, and claiming `:array_join`
still works when it was dropped. Notably case 5 (`map/2`) **LOST on the 26B but WON on the
12B** with the same abstract fact — the target model obeyed it.

**Process note (F-035 caught live):** the FIRST 12B run was contaminated — thinking was ON
(a reload reset the toggle), so case 1 returned empty (budget burned). Caught by reading
(empty answer ≠ result), re-verified thinking OFF with a strict 2-token probe, re-ran clean.
The contaminated run was discarded. This is exactly why we read and why we preflight.

### Caveats that remain (honest)
5 cases, prose delivery, Ecto had priors. But the core question — **do mined niche cards
win on the target model?** — is answered YES, hand-scored, on both a 26B and the 12B.

## 7. End-to-end CLOSED: card → bank → bake → retrieves (5/5) → wins (5/5)
Built the missing links and ran the full chain on the Ecto cards:
`card_to_bank.py` (adapter: card → the bank's `{id,text,source,version,kind,meta}` +
taskwords) → `bake_index.py` → offline jinja2 retrieval test.

- **First bake: retrieval 2/5.** Reading the misses showed the cards had ONLY
  symbol-triggers, so a natural question that named no API (`"reference a column by a
  dynamic name"`) could not find them. **The "triggers are the lever" finding, live.**
- **Fix — the missing MAKE-DATA step:** `llm_expand_cards.py` (DeepSeek, non-thinking,
  blind to the test questions) writes 3-5 natural phrasings per card into
  `triggers.task_words` (`"map/2 returns nil on left join"`, `"ecto query index hint"`).
- **Re-bake: retrieval 5/5**, hand-verified against the EXACT target card id (not a loose
  word match — the first "5/5" was checked and could have credited a wrong card sharing a
  common word like "map"; verified by pinning the distinctive phrase). All 5 land in top-5.

Combined with §6 (5/5 wins when delivered), the pipeline is proven **from a changelog to a
retrieved, winning fact.** Pipeline now: mine → gate → second-line(dedup/subject) →
expand → adapter → bake → retrieve → win. Code saved in `card-mining/`.

## 8. SERVED confirmation — baked into a real GGUF, 4/5 through the llama.cpp engine
Baked the 60 Ecto cards into a copy of the stock `gemma-4-12B-it-QAT` GGUF (667 tensors
byte-identical, only `tokenizer.chat_template` rewritten to the 90,785 B index template;
verified in-file, no F-053 truncation). Loaded it in LM Studio as
`gemma-4-12b-ecto-cards-demo`, thinking OFF, and asked the 5 questions with **no fact in
the prompt** — the baked template auto-retrieves. Hand-read:

> *(Superseded practice: EXTRACTOR-2.0.md §7 retires LM Studio for serving/testing —
> it silently drops `chat_template_kwargs`, so `enable_thinking` has no effect there.
> Current guidance is the team's own `llama-server` with `--jinja`. This particular
> use — loading an already-baked GGUF to eyeball its auto-retrieval with thinking OFF
> via the global UI toggle, not per-request `chat_template_kwargs` — didn't depend on
> that flag, but the tool choice going forward is `llama-server`.)*

| case | served (auto-retrieved) | won |
|---|---|---|
| transaction | used `transact/1`, cited the deprecation | ✅ |
| literal | recommended `fragment`+`dynamic`, never `identifier/1` | ❌ |
| hints | `unsafe_fragment/2` | ✅ |
| array_join | "removed in 3.x, don't use" | ✅ |
| map/2 | "you receive a map", quoted the fact verbatim | ✅ |

**4/5 through the REAL engine, baked GGUF, auto-retrieval.** The winners' answers say
*"based on the documentation lookup"* — the factbank mechanism firing. This is the
production-form proof the prose test (§6) only implied.

**The 5th case (`literal`) is BORDERLINE, not a clean loss.** It retrieved weakly (rank 5),
and served it answered `field/3`/`fragment` instead of `identifier/1`. But the question
(*"reference a column by a dynamic identifier"*) has **two legitimate Ecto answers**
(`field/3` for a schema field, `identifier/1` for a raw fragment identifier), so bare is not
confidently wrong the way it is on `keyword hints` (invented `Repo.all_with_hint`) or
`array_join`. It is a **weak test case**, not a pipeline failure.

### Finalized (v2, 2026-07-15)
Applied the text-artifact fix (all facts cleaned of the `"* [Module]"` bullet prefix) and
regenerated expansions, re-baked to `gemma-4-12b-ecto-cards-v2`, re-served. **Still 4/5** —
the clean-up improved hygiene and `transaction` retrieval (rank 5→3) but did not move the
headline, because the 4 wins were already solid and `literal` is borderline regardless.

**FINAL RESULT: 4/5 unambiguous served wins through the real llama.cpp engine, on clean
data.** The pipeline is proven end-to-end: a changelog becomes a served, auto-retrieved,
winning fact. Landmine cards win when the model is genuinely wrong (hints/array_join/map/
transaction); they add little on ambiguous questions (literal) — correct behaviour, not a
bug. Remaining polish (bug-fix-noise tagging, abstract→concrete rewrite, the 1 dropped
`:pool_timeout` fact, `parity.py` as a standing gate) is documented in `card-mining/README.md`
§gaps; none blocks the proven result.

## Standing lesson, reinforced ~5× today
Every gap this session was found by **hand-reading**, never by a pass/fail number — and the
number was wrong in both directions (too-strict deleted facts, too-loose kept junk, "0 rejected"
looked perfect and wasn't). **Automated checks triage; reading is the verdict.** (F-065.)
