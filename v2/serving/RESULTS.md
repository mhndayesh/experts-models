# Results — every measured number

Re-verified 2026-07-14 against the live artifacts. Nothing here is an estimate.
Where a number is single-sample or otherwise weak, it says so.

> **Scope note (2026-07-18, Extractor/Facts/Retrieval 2.0 rebuild):** everything below is about the
> **pydata factbank** (baking + the inverted index), predating 2.0. It is unaffected by 2.0's mining/
> repair/dedupe/verification changes. One thing IS adjacent: §5's LM Studio findings are about the
> raw-load GGUF-template size sentinel (still valid) — a **different** LM Studio problem from the one
> that made 2.0 retire LM Studio for the *serve-test-without-bake* harness (it silently drops
> `chat_template_kwargs`, so `enable_thinking` has no effect, which breaks the HyDE + authority-framing +
> thinking-ON test loop). For live serve-testing a bank with no bake, use your OWN `llama-server`, not LM
> Studio — see `../extractor/EXTRACTOR-2.0.md` §6–7.

**Two metrics, always both.** *Retrieval* = did the right fact reach the model?
*Answer* = did the model then obey it? A system can pass the first and fail the second,
and reporting only one hides the central failure mode.

---

## 1. The shipped model

`factbank/gemma-4-12b-pythondatafactbank-idx` — gemma-4-12B-it QAT Q4_0, 667 tensors
byte-identical to the base, 1,911 facts, 973,652-byte template (= 972,985 chars; **chars are not bytes** — F-066).

| gate | result |
|---|---|
| **gold retrieval** (12 questions, each with a known required fact) | **12/12** |
| **controls** (10 questions that must retrieve nothing) | **0/10 false fires** |
| **lint** (`scenarios_pydata/`) | **8/8** |
| **engine parity** (jinja2 vs the real engine, 22 questions) | **22/22** |
| **live** (LM Studio, plain API calls) | **10/10 clean** |
| time to first token | 0.18–1.91 s |

## 2. The search was the ceiling — not the fact count

The first build carried **more** facts and answered **worse**. Asked to reshape a wide
DataFrame, it produced the **dead `melt()` API** — while the melt→unpivot fact sat in the
bank, never retrieved, its five slots taken by low-value mined signatures.

Replacing the linear scanner with an inverted index (same delivery lane, same model):

| | scanner | index + cures |
|---|---:|---:|
| facts in the bank | 2,560 | **1,911** *(fewer)* |
| **gold retrieval** | **6/12** | **12/12** |
| control false-fires | 0/10 | 0/10 |
| matched-question render | 2,629 ms | **545 ms** |
| long-question render | 4,077 ms | 1,116 ms |
| engine parity | never tested | **22/22** |

**Retrieval doubled while the bank shrank 25%.** The four questions that used to fail —
*"turn columns into rows"* (answered with dead `melt()`), *"t-test with scipy"* (returned
`dunnett`), *"split data with scikit-learn"* (retrieved nothing), *"np.NaN"* — all answer
correctly now.

The cures, in the order they mattered: **Doc2Token expansions** (the model writing the
user's words for its own facts), **build-time IDF**, **squash-normalisation + a real alias
table**, **seat policy keyed on provenance**, and an **engine-parity gate**.

## 3. Bytes are not the constraint

Pure llama.cpp, CPU only, median of 3. Same retriever, banks selected from the 24,521-fact
data pool.

| facts | template | no-match | matched | long question | ms/fact |
|---:|---:|---:|---:|---:|---:|
| 2,314 | 1.06 MB | 102 ms | 197 ms | 1,344 ms | 0.085 |
| 4,564 | 1.69 MB | 115 ms | 95 ms | 1,078 ms | 0.021 |
| 8,837 | 2.71 MB | 158 ms | 138 ms | 638 ms | 0.016 |
| **21,203** | **5.06 MB** | **239 ms** | **218 ms** | **655 ms** | **0.010** |

**A 5 MB, 21,000-fact template renders a matched question faster than the 950 KB one we
ship** — and cost *per fact* falls 8× as the bank grows. The index visits only the facts a
query's terms point at, so render cost tracks the **query**, not the bank.

This retired an earlier law of ours ("the engine re-parses the template every request at
~0.33 ms/fact, so fact count is a latency budget"). That was measured on the **linear
scanner under jinja2**, and it does not survive the index.

## 4. Targeting IS the constraint

Same retriever, same expansions, same gold set — only the bank grows:

| facts | template | **gold** | controls |
|---:|---:|:---:|:---:|
| 2,314 | 1.06 MB | **12/12** | 0/10 |
| 4,564 | 1.69 MB | 11/12 | 0/10 |
| 8,837 | 2.71 MB | **9/12** | 0/10 |
| 21,203 | 5.06 MB | **9/12** | 0/10 |

**Recall decays as the bank grows, and the controls never false-fire.** That combination
is the finding: a big bank does not become *noisy* — it becomes **unfocused**. Nothing
wrong is dragged in; the *right* fact simply loses its slot to competitors.

At 21k the failures are specific: `resample`'s frequency-alias fact retrieves **nothing at
all** (its gate never opens), and `np.NaN` pulls five facts, none of them the right one.

**Cause: constants calibrated at 2,000 facts, applied to 21,000** — `DF_CAP=40`, the IDF
buckets, 48 gate triggers per library, and 5 answer slots. None scale with bank size, and
the slots got contested 10× harder while latency got *cheaper*.

## 5. The LM Studio ceiling — and its bypass

**The cap is real, silent, and belongs to one code path.** LM Studio's GGUF-metadata reader
replaces an over-long `tokenizer.chat_template` with a 48-character sentinel
(`[LM Studio Patch - String too long; didn't read]`). The model then loads "successfully"
and answers **garbage**, because its template is a constant with no `{{ messages }}` in it.
No error anywhere.

| embedded template | outcome |
|---:|---|
| 972,985 chars (shipped) | works |
| 994,885 chars | works |
| ~1.51 MB | **sentinel — bricked** |

llama.cpp has no such limit (its cap is 1 GiB, and it errors *loudly*): a **1.5 MB template
embedded in a GGUF loads and renders correctly**.

**The bypass:** LM Studio's *load-config* path (`llm.load.promptTemplate`, set by a Hub
`model.yaml`) has **no size limit**. Proven live, against the real `llama-server` process
LM Studio spawned:

| gate | 1.5 MB | 2.0 MB |
|---|---|---|
| bytes handed to the engine | **1,536,014** | **2,048,014** |
| not the sentinel · >1 MiB · canary present · SHA-256 match | PASS | PASS |

Functional on the same load: matched question → **390 prompt tokens** with the
melt→unpivot fact injected and `unpivot` in the answer; control → **112 tokens**, no facts.

**The Hub carries it:** `lms push` of a 1.95 MB `model.yaml` was **accepted** (1.53 MB
uploaded — incompressible worst case), and `lms clone` returned the template **intact at
2,047,990 bytes**. The real 2 MB FactBank template gzips to **0.22 MB**, so production sits
far inside the limit.

## 6. Index compression — measured, not adopted

Against the real 540 KB index (17,260 terms, 34,671 postings):

| change | claimed | **measured** |
|---|---|---|
| dedupe identical posting lists ("57% are duplicates!") | the big win | **+28 KB — it makes the file BIGGER** |
| fixed-width base-62 postings | −60…70% | **−99 KB** (decode verified bit-exact) |
| 4-char hashed term keys | −153 KB | **−137 KB** — *only with a prime modulus* |

Three things the proposal got wrong, each caught by measurement:

- **Dedup is a regression.** Posting lists average **2.0 entries**; the indirection costs
  more than the payload it shares. (No production engine interns whole posting lists.)
- **`h*31 % 62⁴` collapses** — 2,895 colliding keys, because 62⁴ = 2⁴·31⁴ shares the factor
  31 and the hash degenerates into a suffix match (`float` = `numpy_float`). With a **prime
  modulus and multiplier 131: 8 collisions in 17,260 terms**, and a <1 KB exception table
  makes it lossless.
- **A 1-char weight field truncates our strongest evidence** — max weight after IDF is
  **72**, not ≤61. Dead-name facts would corrupt.

Unpriced cost: the engine has no `ord()`, so hashing query tokens is a per-character loop —
**289 ms for 40 tokens**, measured in the real engine. The real trade is **−235 KB for
~+290 ms**. Nothing is implemented; with bytes no longer scarce (§3), this is now a *speed*
tool, not a capacity tool.

## 7. Prior chapter (context)

The same architecture, before it was compressed into a template — bank + code-driven loop,
served by a package. Structurally-correct code, on APIs the model provably could not know:

| model | without bank | with bank |
|---|---:|---:|
| qwen3-0.6b | 0.04 | **0.54** |
| gemma-4-12b | 0.00 | **0.62–0.71** |
| qwen3.6-35b MoE | 0.36 | **0.67–0.71** |

The 12B **with** facts beat the 35B **without** them by 4×. Scale does not close a
knowledge gap — there is nothing to scale into.

## 8. The mined bank was 66% junk (2026-07-14)

Full evidence: `archive/docs/FINDINGS.md` F-064 (the project's full archive, not included in this repo). Offline, free, no GPU.
Reproduce: `python dedupe_mine.py` in `template-brain-v3.1/template-brain-v3.1/`.

`mine_api.py` walked `inspect.signature` — including the **inheritance chain** — over 10
Python data libraries. Nobody had read the output.

| the raw mine (24,133 facts) | |
|---|---|
| share a docstring with ≥5 other facts | **63%** |
| docstring merely re-prints the signature | 16% |
| facts per distinct method name | **4.9** |

`Get parameters for this estimator.` ×144. `Exception.add_note(note)` ×69. duckdb's entire
64-fact bank was Python exception boilerplate. `str.join` was in there as a *matplotlib* fact.

**This is why recall collapsed at scale** (§4: gold 12/12 at 2.3k → 9/12 at 21k). 205 facts
containing the token `fit` and 165 containing `get_metadata_routing` index the same terms,
flatten document frequency so IDF stops discriminating, and crowd the top-5. The bank was
poisoning its own index. *(Mechanism + correlation — the causal test is queued, not run.)*

### After the gate

**24,133 → 8,096 kept. 16,037 rejected (66%).** Every rejection with its reason in
`facts_mined_clean.rejects.jsonl`.

| index health | before | after |
|---|---|---|
| facts sharing a docstring with ≥5 others | 63% | **3%** |
| facts per method name | 4.9 | **1.7** |

| library | mined | kept | |
|---|---|---|---|
| matplotlib | 7,318 | 1,329 | 18% |
| numpy | 3,866 | 810 | 21% |
| pyarrow | 3,307 | 828 | 25% |
| scipy | 2,372 | 1,285 | 54% |
| sklearn | 1,945 | 895 | 46% |
| polars | 1,722 | 982 | 57% |
| pandas | 1,581 | 856 | 54% |
| statsmodels | 1,185 | 508 | 43% |
| xarray | 773 | 603 | 78% |
| duckdb | 64 | **0** | 0% |

The split is the tell: libraries mined from real public API surface kept 50–78%; the ones
whose mine walked inheritance chains kept ~20%.

### Four bugs in the gate, all caught by reading the reject file

A dedupe gate is a scorer, and this repo's scorers are wrong by default. None of these was
caught by a test:

1. Grouping on `(lib, name, docstring)` ate `polars.Series.search_sorted` — it shares a
   summary line with `Expr.search_sorted` but takes different arguments. **The signature had
   to be in the group key.**
2. `str.join` survived as matplotlib. Fixed by *introspecting* the builtins, not banning names.
3. **Deleting real APIs for having lazy docstrings** — `pyarrow.Table.join_asof(right_table,
   on, by, tolerance, ...)` was killed because pyarrow re-prints the call in its docstring.
   The signature *is* the fact. Fixing it recovered ~2,500 facts.
4. **Keeping the subclass, deleting the base class** — `pandas.CategoricalIndex.to_series` beat
   `pandas.Index.to_series` because "C" < "I" in an alphabetical tie-break.

Bugs 3 and 4 would each have silently destroyed thousands of legitimate facts while reporting
a clean-looking cull.

### The caveat that does not go away

The **1,523** mined signatures in the *shipped* bank **won zero cases** in the dense eval
(F-065). Every case the bank carried was won by a curated `mistake` fact. A cleaner signature
bank is a better-behaved bank; there is still no evidence signature facts move obedience at
all.

*(Count correction: the 24,133-fact raw mine has never been shipped in any model. The eval ran
against the 1,911-fact shipped bank = 1,523 mined + 388 curated.)*
