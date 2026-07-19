# A fresh retrieval design, from fundamentals

Research + design, 2026-07-14.

> ## ⚠ §1 HAS SINCE BEEN TESTED — AND IT FAILED
>
> The headline proposal below was **"delete the gate."** It was measured the same day and
> is **wrong**: with the gate removed, **8 of 10 controls fired** (a haiku retrieved five
> polars facts) and gold fell 12/12 → 10/12.
>
> **Why the argument failed:** it assumed control words are culled from the index, so the
> index protects itself. But the cull only removes **strong keys** — every fact *also*
> indexes its **description words**, which are ordinary English. The gate is
> **load-bearing, not vestigial.**
>
> The **narrow fallback worked**: keep the gate, and only when nothing opens, let a
> **weight-10 dead API name** open its own library. That shipped as the *rescue gate*
> (curated reachability 74.5% → 77.6%, controls still 0/10).
>
> The failed run was still worth its cost: it measured **the ceiling — 82.5% curated.**
>
> **See `FINDINGS.md` F-062 and `RETRIEVAL-V7.md` §9.** §2–§6 below remain untested
> proposals.

The premise: stop patching the design we inherited and ask what the *literature* would
build on *this substrate*, under *these budgets*.

---

## 0. The substrate, stated honestly

The runtime is a Jinja template executed by llama.cpp's C++ engine on every request. It
can: split strings, look up dict keys, index lists, add integers, compare. It cannot:
sort a list of objects into a ranked result, assign into a dict, hold state between
requests, run a regex, or do floating-point work worth trusting.

**This is not a prison. It is a deployment target.** An entire research line —
[DeepImpact](https://dl.acm.org/doi/10.1145/3404835.3463030),
[uniCOIL](https://ar5iv.labs.arxiv.org/html/2106.14807), SPLADE — exists *because*
inverted indexes with integer scoring are fast and portable. Their whole method is:

> do the neural work **offline**, quantize the intelligence into integer term weights,
> and let the runtime stay dumb.

DeepImpact quantizes weights to **8-bit integers stored directly in the inverted index**,
and the query–document score is **just the sum of the weights of the query's terms**.
That is *literally* what our template does. We built a learned sparse impact index by
accident, without its rigor.

So the design question is not "how do we escape the substrate" — it is **"what does a
properly-built impact index look like, and where does ours diverge from it?"**

### The three budgets

| budget | current | what actually binds |
|---|---|---|
| **bytes** | ~1 MB (LM Studio raw-GGUF); multi-MB on llama.cpp / Hub | only the raw-GGUF route (F-059) |
| **render time** | ~0.01 ms/fact at 21k (F-055) | cost is per *index entry parsed*, not per fact |
| **slots** | `FB_MAX = 5` facts reach the model | **the tightest budget by far** |

The slot budget is the one nobody optimises for, and it is the one that decides whether a
fact is knowledge or dead weight.

---

## 1. The idea with the most potential: **delete the gate**

**The measurement:** 66% of unreachable curated facts die at the gate — no library tab
opens, so the index is never consulted and ranking never runs (`RETRIEVAL-V7.md` §1).

**The fundamental error:** an inverted index *is already a filter*. A fact is only visited
if a query term points at it. Putting a hard library pre-filter *in front* of an inverted
index is a second, cruder filter that can only ever **remove** recall the index would have
found. No database does this. It is a full-table-scan optimisation applied to a system
that doesn't scan.

The gate was designed when the retriever was a **linear scanner** over every fact — there,
a gate was the whole performance story. **When we replaced the scanner with an index
(generation 2), the gate's reason to exist disappeared, and we kept it anyway.** It is a
vestigial organ from the previous architecture, and it is now the single largest source of
failure.

**The proposal:** score whatever the query's terms touch. No tabs. The index restricts the
work; evidence decides the answer.

**The obvious objection — controls.** Won't a haiku drag facts in? Almost certainly not,
and the reason is elegant: **control words are already culled from the index** (F-046).
A term that appears in a control question is deleted from the postings. So a control query
touches *no postings*, scores *nothing*, and retrieves *nothing* — **the index provides
control safety, not the gate.** The gate is redundant *for controls too*.

That claim is precisely falsifiable, offline, for free, in one afternoon: bake with the
gate disabled, run `baseline.py` (controls must stay 0/10) and `reach.py`.

**Expected value: very high.** It targets the 66%, not the 22%. If controls hold, this
single change is worth more than everything else on this page combined.

**If it fails** (controls fire), the fallback is a *soft* gate: the library tab becomes a
**score bonus**, not a veto. Same information, no ability to zero out recall — which is
what the literature would do anyway (evidence combination, not hard filtering).

---

## 2. Fix the pruning: keep the term, drop the postings

**Today:** `DF_CAP = 40` — a term appearing in more than 40 facts is **deleted from the
index entirely.**

This is the crudest possible pruning and it is *backwards*. It throws away a term's
usefulness *for the facts it discriminates best*, in order to stop it being noisy for the
rest. Delete `dataframe` and no query can ever use the word "dataframe" as evidence — for
any fact.

**The literature:**
[Carmel et al.'s static index pruning](https://research.engineering.nyu.edu/~suel/papers/prune.pdf)
prunes **postings, not terms**, in two forms — a global impact cut-off (**UP**), and
**top-k postings per inverted list** (**TCP**), which comes with a guarantee on the top-k
results being preserved.

**The proposal:** replace `DF_CAP` with **TCP** — for every term, keep its `k` highest-impact
postings. A common word survives, pointing only at the facts it genuinely discriminates.
Bytes stay bounded (that was `DF_CAP`'s only real job), and recall stops being collateral
damage.

**Expected value: high**, and it is a strictly better-founded version of a knob we already
have. Cheap to implement, free to measure.

---

## 3. Make the weights an impact score, not a hand-written table

**Today:** dead name = 10, rare API = 4, description word = 3, bigram = 3/2, expansion = 1
— multiplied by a 3-bucket IDF guess (×3 / ×2 / ×1). Every number was chosen by hand.

**The literature:** compute a real impact per (term, document) pair and **quantize to a
small integer** (DeepImpact: 8 bits). Score = sum of impacts. Runtime unchanged.

**The proposal, in ascending order of ambition:**

1. **Proper BM25 impacts, quantized.** Real IDF (`--idf smooth` already showed +6 points on
   mined facts), *plus the half we have never had*: **term-frequency saturation and
   document-length normalisation** — the parts of BM25 that stop a long fact winning by
   matching more words. (Naive length normalisation *hurt* in our test; BM25's saturating
   form is not the same thing, and deserves its own trial.)
2. **Learned impacts.** The served model already writes expansions offline. It could also
   *score* which terms in a fact actually matter — a poor man's uniCOIL. Offline, batched,
   baked to integers.

**Expected value: medium-high.** Principled, but it is refining the 22% (ranking), not the
66% (gate). Do it *after* §1.

---

## 4. Filter the expansions — and give them to the mined facts

**Today:** the model writes 6 questions per curated fact; we index ~5 of them. **No
filtering.** And the 1,523 mined facts get **zero** expansions — they are reachable only by
literal API token.

**The literature:**
[Doc2Query--](https://arxiv.org/abs/2301.03266) — expansion models hallucinate, and the bad
queries both hurt effectiveness and inflate the index. Filtering out poor queries before
indexing improved effectiveness **+16%**, cut query time **−23%**, and shrank the index
**−33%**.

**The proposal — and the filter is free:**

> **Keep an expansion only if it retrieves its own fact.**

Bake, ask the expansion, check the fact lands top-5. A question that can't find its own
fact is noise: it costs bytes and pollutes other facts' postings. This is the same
machinery `reach.py` already runs — it just becomes an *admission gate for expansions*
instead of a report.

Then **expand the mined facts too**, with the byte budget the filter just freed. That
attacks their real ceiling: a signature fact today can only be found by someone who
already knows its name.

**Expected value: high.** It is the known coverage gap, the literature says the filter pays
for itself in bytes, and the filter costs nothing we haven't already built.

---

## 5. Spend the slot budget deliberately

`FB_MAX = 5` is the tightest budget in the system and it has **no policy at all**: if five
facts score, five facts ship, however weak.

Two cheap, orthodox controls:

- **A relative score floor** — admit a fact only if it scores within some fraction of the
  top hit. Costs nothing, stops junk filling seats on weak matches.
- **Diversity in the result set (MMR).** Only if measurement says duplicates are still
  crowding the slots — our data says this is a *secondary* effect (the four near-duplicate
  pandas facts are real, but they explain the 22%, not the 66%).

**Expected value: medium.** But this is where the *product* is decided: five facts is what
the model actually sees.

---

## 6. Storage, as a data-engineering problem

Render cost is **per index entry parsed**, not per fact (F-055) — and the engine builds
list entries ~4–5× faster than dict entries (measured: 2,485 ms → 545 ms just by moving
fact texts from a dict to a list). Bytes and parse time are therefore the *same* budget.

Untried, and all offline:

- **Dictionary/front-coding of terms.** Shared prefixes are everywhere in an API index
  (`ttest_ind`, `ttest_rel`, `ttest_1samp`). Measured at −235 KB (F-057) and shelved when
  bytes stopped being scarce — but bytes *are* parse time, so it is a **speed** tool now.
- **Denser posting encoding.** `"0:4 14:4 69:1"` is verbose. Base-62 varints or delta-coded
  ids shrink the string the engine must parse.
- **Fewer, larger entries.** The cost is the *number* of entries constructed per render.
  Sharding the postings dict into a small number of large strings, parsed lazily, may beat
  one entry per term.

**Expected value: low for accuracy, high for headroom.** This is what buys the 20k-fact
bank, once accuracy at 2k is solved.

---

## 7. What must be re-established before any of this is built

- **The engine capability map is stale.** `minja_capabilities.json` describes minja —
  which llama.cpp **replaced** (PR #18462, a new C++ lexer→AST→runtime). Nothing above
  *needs* a new construct (it is still dict lookup + integer adds, which is the point), but
  no design decision should cite that file again until it is re-probed against the engine
  that actually ships.
- **`parity.py` is non-negotiable** for anything that changes template code. §1 does.
- **Reachability is the metric**, not gold. Gold is 12 questions and cannot calibrate a
  bank; reachability scales to any size and is free. But it measures **delivery, not
  obedience** — and obedience has never been measured for any of this.

---

## The order I would actually do it

| # | change | attacks | cost | risk |
|---|---|---|---|---|
| **1** | **Delete the gate** (fallback: make it a bonus, not a veto) | **the 66%** | one bake | controls — *falsifiable in an afternoon* |
| 2 | TCP pruning instead of `DF_CAP` deletion | recall lost to a blunt cap | small | none |
| 3 | Filter expansions by self-retrieval; then expand mined facts | the coverage gap | medium | none |
| 4 | Quantized BM25 impacts (saturation + length norm) | the 22% | medium | must re-tune |
| 5 | Score floor + slot policy | what the model actually sees | small | none |
| 6 | Front-coding / dense postings | headroom for 20k+ | medium | none |

**One sentence:** we built a learned sparse impact index by accident, then bolted a
full-table-scan optimisation onto the front of it — and that bolt is now the single largest
cause of failure. Remove it, prune properly, filter the expansions, and the rest is
tuning.

---

### Sources

- [Learning Passage Impacts for Inverted Indexes (DeepImpact, SIGIR'21)](https://dl.acm.org/doi/10.1145/3404835.3463030)
- [A Few Brief Notes on DeepImpact, COIL, and a Conceptual Framework for IR (uniCOIL)](https://ar5iv.labs.arxiv.org/html/2106.14807)
- [Improved Methods for Static Index Pruning (Carmel et al.)](https://research.engineering.nyu.edu/~suel/papers/prune.pdf)
- [Doc2Query--: When Less is More (ECIR'23)](https://arxiv.org/abs/2301.03266)
- [Towards Effective and Efficient Sparse Neural Information Retrieval (TOIS)](https://dl.acm.org/doi/10.1145/3634912)
