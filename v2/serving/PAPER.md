# The Model Is the Know-How. This Is the Knowledge.

**An unmodified 12B, served as a stock GGUF, answering correctly about libraries released
after it was trained.**

FactBank · written 2026-07-14 · every number re-verified against the live artifacts
Evidence trail: `../../archive/docs/FINDINGS.md` (65 numbered findings) · numbers: [RESULTS.md](RESULTS.md)

---

## Abstract

We placed a documentation bank, an inverted-index retriever, and a native-protocol delivery
lane **inside the chat template of a single GGUF file**. No fine-tuning, no server, no
client code, no sidecar files: all 667 tensors are byte-identical to the base model, and
exactly two metadata keys are rewritten. Loaded in stock LM Studio and asked plain API
questions, the artifact answers correctly about post-cutoff APIs — Polars 1.0 `unpivot`,
pandas 3.0 copy-on-write, NumPy 2 removals — that the bare model provably gets wrong. The
goal was never a better model. It was to turn models that already exist into experts on
knowledge that did not exist when they were trained, and to ship that expertise as one
copyable file.

The result that took the longest to learn is not the architecture. It is this: **a bank you
cannot search is a bank you do not have.** Our first build carried *more* facts and answered
*worse* — confidently, with a dead API — because the right fact was never retrieved.
Replacing the search doubled retrieval (6/12 → 12/12) while the bank *shrank* by 25%.

And every wall we hit turned out to sit somewhere other than where we thought.

## 1. The question

Stage 0 of this project established that an untrained LLM, plus a frozen fact bank, plus a
code-driven retrieval loop, beats the bare model on facts it cannot know — and that the
*delivery channel* matters as much as the facts. A 12B model **with** the bank beat a 35B
model **without** it by 4×. Scale does not close a knowledge gap, because there is nothing
to scale into.

That system needed a server. This chapter asks a narrower, more portable question:

> **How much of the architecture survives being compressed into the model file itself?**

The chat template inside a GGUF is a Jinja program that every serving stack executes on
every request. If the bank, the search, and the channel can be expressed in the engine-safe
subset of that language, then "install the expert" collapses to "copy one file" — any
machine, any app, no code of ours running anywhere.

It survives. But what the substrate gives you is *string operations and integer arithmetic*,
and everything below is shaped by that.

## 2. What is in the file

```
gemma-4-12B-it-QAT-Q4_0-pythondatafactbank-idx.gguf
├── 667 tensors ................ byte-identical to the base. Untouched.
├── tokenizer.chat_template .... 973,652 bytes: bank + index + retriever + delivery
└── factbank.bank .............. the raw JSONL, carried for auditability
```

**1,911 facts.** 388 curated (renames, removals, gotchas — the facts that beat a *wrong*
prior) and 1,523 mined by introspection (`inspect.signature` on the installed library, plus
the doc URL from its Sphinx index — verbatim, hallucination-proof, and shallow).

Every fact targets a **post-training-cutoff API**. This is deliberate and load-bearing:
with `requests` and old `pandas` you could never separate "the bank told it" from "it
already knew." Here, **any correct answer must have come from the bank.**

## 3. Retrieval, in a language that has no data structures

The runtime does four things: split strings, look up dict keys, index lists, and add
integers. There is no regex, no state between requests, no sorting a list of objects into
a ranked result — and, notably, **no dict item assignment**, which rules out the obvious
implementation of a score table.

So everything that could be done at build time was moved to build time.

**The index.** Each fact becomes weighted terms in one dict: `term → "factid:weight …"`.
A dead API name is the strongest evidence there is (weight 10); a rare API token is strong
(4); a description word is weak (1–3). At runtime, a term that no query mentions is never
touched, and a fact no term points at is never visited.

**IDF, precomputed.** A term appearing in ≤3 facts is evidence (×3); one appearing in 40 is
noise (×1). Runtime stays integer addition. Without this, `test` — which appears in every
SciPy docstring — outvoted `ttest`, and a question about a t-test returned
`scipy.stats.dunnett`.

**Squash-normalisation and aliases.** `ttest_ind` also indexes as `ttest`; `scikit-learn` as
`scikitlearn` and (via a table built from real package metadata) as `sklearn`. This is what
lets a user's *"t-test"* find `scipy.stats.ttest_ind`.

**A gate, like the tabs on a phone book.** If the question *names* a library, only that tab
opens — named always wins. If the question names none, tabs open on trigger words. If no tab
opens, **nothing renders at all**, and the request is byte-identical to a stock model's.

**The layout is the performance.** Fact texts live in a **list**, not a dict. Same
algorithm, two data structures: moving them cut per-request cost **4–5×** (2,485 ms →
545 ms). The engine builds list entries fast and dict entries slowly; the cost is the number
of entries constructed per render, not the lookups.

### The hardest problem in keyword retrieval, solved offline

*"In polars, how do I turn columns into rows?"* shares **zero words** with the fact that
says `melt()` was renamed to `unpivot()`. No keyword engine can bridge that. Neither
squashing, nor IDF, nor better ranking — the signal is simply not present.

The literature's answer (doc2query, SPLADE-doc, Doc2Token) is to **predict the words a user
would type, at build time, and index those** — leaving the runtime matcher dumb, which is
exactly our constraint. So the served model wrote its own expansions: **six everyday
questions for each of the 388 curated facts — 2,326 in total** — filtered, and indexed at a
weight strictly *below* real terms.

That is what finally retrieved the melt fact. Thirty-five terms now point at it, and one of
them is the bigram `columns_rows`.

### Delivery: a forged tool exchange

Facts are not handed over as prose. The template renders a **completed tool call and
response in the model's own syntax**, using the base template's own macro — bit-identical to
a real exchange. The model's experience: *a documentation lookup already ran; here are the
results; now answer.*

This is not cosmetic. Handed the same facts as prose, the model **arbitrates**: one
glyph-heavy question burned **8,189 reasoning tokens and produced no answer at all**.
Through the tool channel: **390–757 tokens, and a correct answer**. A `tool_response` is not
something a model argues with.

The forged block renders *before* the user's question — which kills an echo bug in LM Studio
and, as a bonus, lets prompt-prefix caching skip re-evaluating the fact block (repeat-topic
time-to-first-token drops from ~1.8 s to ~0.24 s).

## 4. The result that reframed the project

The first Python-data build carried **2,560 facts** and failed a scored test. Asked to
reshape a wide DataFrame into long format, it answered with **`melt()`** — the dead API. The
melt→unpivot fact was **in the bank**. It was never retrieved: five low-value mined
signatures took its five slots.

More facts had not helped. **The search was the ceiling.**

| | scanner | index + cures |
|---|---:|---:|
| facts in the bank | 2,560 | **1,911** *(fewer)* |
| **gold retrieval** | **6/12** | **12/12** |
| control false-fires | 0/10 | 0/10 |
| matched-question render | 2,629 ms | **545 ms** |

Retrieval doubled while the bank shrank by a quarter. That trade — *fewer facts, better
found* — is the single most useful thing this project has learned.

## 5. Three ceilings that were not where we thought

### Bytes

LM Studio silently refused templates above ~1 MB. No error: the model loaded "fine" and
produced garbage. We took this as a hard wall, cut the bank to fit, and planned a second,
llama.cpp-only edition.

The cause turned out to be **one application's undocumented patch**: its GGUF-metadata
reader replaces an over-long string with a 48-character sentinel
(`[LM Studio Patch - String too long; didn't read]`), leaving a chat template with no
`{{ messages }}` in it. The GGUF format never had a limit. llama.cpp caps metadata strings
at 1 GiB and **errors loudly**. A 1.5 MB template embedded in a GGUF loads and renders
correctly there.

And LM Studio itself has a *second* template path — the load-time config field a Hub
`model.yaml` sets — with **no size limit at all**. We proved it live at **1.5 MB and 2.0 MB**:
the template LM Studio hands to the engine is byte-for-byte what we published, over 1 MiB,
and retrieval works through it. The Hub accepts the manifest and returns it intact.

**The wall was real. It just wasn't ours, and it wasn't final.**

### Time

Our own law said the engine re-parses the template on every request at ~0.33 ms/fact — so
fact count was a **latency budget**, and 30k facts would have to ship as a line of small
models.

That law was measured on the *linear scanner under jinja2*. It does not survive the index,
because an index visits only the facts a query's terms point at. Measured on pure llama.cpp:

| facts | template | no-match | matched | ms/fact |
|---:|---:|---:|---:|---:|
| 2,314 | 1.06 MB | 102 ms | 197 ms | 0.085 |
| 21,203 | **5.06 MB** | 239 ms | **218 ms** | **0.010** |

**A 5 MB, 21,000-fact template answers a matched question faster than the 950 KB one we
ship**, and cost *per fact* falls eightfold. Bytes: abundant. Milliseconds: abundant.

### Targeting — the wall that is real

So we can hold 21,000 facts, cheaply and quickly. Can we *find* them?

| facts | gold | controls |
|---:|:---:|:---:|
| 2,314 | **12/12** | 0/10 |
| 4,564 | 11/12 | 0/10 |
| 8,837 | 9/12 | 0/10 |
| 21,203 | **9/12** | 0/10 |

**Recall decays as the bank grows — and the controls never false-fire.** That combination is
the whole finding. A large bank does not become *noisy*; it becomes **unfocused**. Nothing
wrong is dragged in. The *right* fact simply loses its slot.

The causes are all the same shape: **constants calibrated at 2,000 facts, applied to
21,000.** A document-frequency cap, a set of IDF buckets, 48 gate triggers per library, five
answer slots. None of them scale with the bank — and the slots got contested ten times
harder while latency got *cheaper*. On top of that, the expansions of §3 cover only the 388
curated facts, so the mined majority adds *competitors* without adding *bridges*.

## 6. What this cost, and what it taught

Three things are worth stating plainly, because they were expensive.

**We tested the wrong language for weeks.** Every offline gate rendered the template with
Python's jinja2. Production runs llama.cpp's Jinja. They are not the same language — its
`.split()` does not collapse whitespace, and operator precedence differs — and the
difference silently changed *which facts were retrieved*: five under jinja2, one in
production. A parity gate is now mandatory and runs before every bake.

**Two of our design constraints did not exist.** The ranker uses five max-selection passes
and totals scores by re-walking a string, because we believed the engine had no `sort` and
no `append`. When we finally *probed* the engine instead of assuming, it had both. The
design still works; it just costs more than it had to.

**Every silent failure cost more than every loud one.** The template that was replaced by a
48-character sentinel. The manifest LM Studio refused to index, with the reason buried in an
internal cache file. The background job that overwrote a good expansions file with garbage.
The bake that was not byte-reproducible because Python randomises set order per process.
None of these announced themselves. All of them were found by asserting on the artifact
rather than trusting the process.

## 7. Where it stands

Four questions, four ceilings:

1. **Can a fact bank live inside a model file?** **Yes.** One file, no server, no client
   code, weights untouched.
2. **Is holding the facts enough?** **No.** The search was the ceiling, and fixing it
   mattered more than any fact we added.
3. **Was the byte ceiling real?** **It was one application's cap, and it is bypassed.**
   Bytes and milliseconds are both abundant.
4. **Is the search fixed?** **At 2,000 facts, yes: 12/12. At 21,000, no.** The binding
   constraint is targeting.

The architecture scales. The retriever, so far, does not. That is a far better problem to
have than the one we thought we had — because every remaining lever is offline, free, and
measurable: no GPU, no bake, no training. But it is unfinished, and this paper says so.

The shipped model — 1,911 facts, 12/12 retrieval, 10/10 live — is real, and it does the
thing on the tin: an unmodified 12B, served as a stock GGUF, answering correctly about
libraries released after it was trained.

---

*Weights untouched. One file. The model is the know-how; this is the knowledge.*
