# The Model Is the Know-How, But This Is the Knowledge

**An unmodified 12B, served as a stock GGUF, answering correctly about
libraries released after it was trained.**

Template-brain chapter report · 2026-07-13, extended 2026-07-14 · repo `LLM BANK`
Evidence: FINDINGS F-041…F-052, RESULTS §9 and §11–§12,
`archive/docs/template-brain-v3.1-vs-repo.md` §6 (build log),
`template-brain-v3.1/template-brain-v3.1/` (kit: code, banks, transcripts,
timings). Every number in this paper is traceable to a saved file; the
provenance table is §9.

**Read §§1–9 as generation 1** (the niche-language model, linear scanner,
1,027 facts — shipped and measured, record intact). **§10 is generation 2**
(the Python-data model, inverted index, 1,911 facts): the retrieval engine
described in §3.2–§3.3 was replaced after it was caught failing a scored
test, and §10 documents what replaced it and why. Where the two disagree,
generation 2 is the current standard (`WORKS.md`).

---

## Abstract

We put a 1,027-fact documentation bank, a two-stage keyword search with
weighted ranking, and a native-format delivery channel **inside the chat
template of a single GGUF file** — no fine-tuning, no server, no client
code, no sidecar files. The weights are untouched: the model contributes
reasoning (the know-how); the template contributes retrieval (the
knowledge). Loaded in stock LM Studio and asked plain API questions, the
artifact answers correctly about post-training-cutoff APIs (Polars 1.0
`unpivot`, Zig 0.11 `@floatFromInt`, `whenever`, BQN) that the bare model
provably gets wrong or cannot know, at a cost of ~0.2 s added latency for
off-topic questions and ~1.8 s (once per topic) when facts inject. The
goal is not a better model. It is turning models that already exist into
experts on knowledge that did not exist when they were trained — and
shipping that expertise as one copyable file.

## 1. Thesis and lineage

Stage 0 of this repo established (RESULTS.md §1-§8, FINDINGS F-001…F-032) that
an untrained LLM plus a frozen fact bank plus a code-driven loop beats the
bare model on facts it cannot know — and that the *channel* matters:
facts delivered through the model's own tool protocol bound its compute,
while prose delivery invites drift. The practical chapter shipped that
loop as a package with a server (`factbank serve`).

This chapter asks a narrower, more portable question: **how much of that
architecture survives being compressed into the model file itself?** The
chat template inside a GGUF is a Jinja program that every serving stack
executes on every request. If the bank, the search, and the channel can
be expressed in the engine-safe subset of Jinja, then "install the
expert" reduces to "copy one file" — any machine, any app that renders
embedded templates, no code of ours running anywhere.

It can. The constraints (no `sort()`, no list-building, flat loops,
namespace accumulation only) shaped every design decision below, and none
of them proved fatal.

> **Correction (2026-07-14, §10.1).** Those constraints were *assumed*, never
> probed. When we finally probed the real engine, `sort`, `sort(attribute=)`,
> `list.append()` and `selectattr` all work; only dict item assignment
> genuinely fails. The five max-selection passes in §3.3 are therefore a
> workaround for a wall that was never there. The design still stands — it
> just costs more than it had to.

This is NOT the rejected F-040 artifact. F-040 (`factbank bake`) taxed
all facts (~6k tokens) onto every request unconditionally — the worst
channel. Template-brain injects only keyword-matched facts (≤5 plus tie
overflow), renders nothing at all for off-topic questions, and delivers
through the native tool channel. Same "one file" goal, opposite
mechanism.

## 2. The artifact

`C:\Users\mhnda\.lmstudio\models\template-brain\
gemma-4-12b-qat-factbank-1027-native-v4\
template-brain-gemma-4-12b-1027facts-NATIVE-v4-QAT-Q4_0.gguf`

- Base: gemma-4-12B-it QAT Q4_0 (lmstudio-community build). **All 667
  tensors byte-identical to the source** — the bake rewrites only
  metadata (read-back verified: template == bake, 1027 bank lines).
- `tokenizer.chat_template`: the source template + six anchored inserts
  (~380 KB total) holding the gate, the bank, the ranked scan, and both
  delivery lanes. The base-minus-anchors text is byte-equal to the
  source template (enforced by guard at bake time).
- `factbank.bank` metadata key: the raw 1,027-fact JSONL, carried as a
  read-only pouch for auditability; `factbank.version`: kit version.
- Nothing else. Copy the file to another machine, load it in LM Studio,
  and the whole system travels with it.

## 3. Architecture inside the template

### 3.1 Two-stage gate ("phone-book tabs")

Scanning 1,027 facts × ~10 keywords per fact per request would be
~200,000 substring checks. Instead, stage 1 checks ~42 library groups ×
up to 9 triggers each (the library name + up to 8 strong keywords unique
to that group, mistake-kind keywords first): ~400 checks. Only facts
whose library "tab" opened are deep-scanned. Keys are lowercase,
punctuation-normalized, and space-padded on both sides, so matching is
word-boundary-exact by construction (`" uv "` cannot fire inside
"suvenir").

### 3.2 Keyword classes (built offline by `enrich.py`)

- **strong (`s`)**: tokens with code signal — dots, parens, digits,
  camelCase, underscores — plus the library name. Dotted names emit both
  the spaced phrase and their ≥4-char segments.
- **weak (`w`)**: task phrases mined per fact (3,059 phrases across the
  bank), ≥5 chars — "reshape wide format", "split a string". Weak
  phrases act only inside an already-open tab, which is what makes them
  safe at scale.
- **dead (`d`)**: the strong keys of rename/removal facts (kind
  `mistake`, OR text containing renamed/removed/deprecated/no longer/
  replaced — the research bank labels its rename facts `concept`, which
  a kind-only rule missed). 73 facts carry 277 dead keys. The new name
  rides along with the dead one (they cannot be told apart
  automatically); acceptable, since a hit on either should surface the
  migration fact.
- A large STOP list keeps plain English out of the keyword space
  entirely. Every keyword that substring-matches any control line is
  culled at enrich time, with a report.

### 3.3 Weighted ranked selection (v3.3.0 — F-043)

The pressure probe (`rank_probe.py`, offline) showed why ranking is not
optional at this scale: opening a tab makes every fact in it eligible as
filler, so the FB_MAX=5 cap binds on **21 of 24** probe questions (an
OCaml question has 95 candidates). Before ranking, the winners were
"mistake-kind first, then bank-file order" — one live success (Zig
int→float) was pure file-position luck.

Per fact, a score accumulates: **dead-name hit +10, strong hit +4, weak
hit +1**. Selection runs in five flat passes over the bank (scores are
recomputed per pass — storing them would need list-building, the one
construct that risks engine compatibility):

1. find the best score among question-specific facts (strong count > 1
   or any weak hit);
2. emit the tie band (score == best) **uncapped** — finish-the-band, an
   owner decision: ties are never cut in file order;
3. emit the upper band (`score + 5 >= best`; band edges use addition so
   the template gains no new operator, not even subtraction), capped;
4. emit the lower band, capped;
5. fill leftovers with lib-name-only floor facts (unchanged legacy
   behavior).

Verified offline: the Polars melt question now top-ranks the
melt→unpivot migration fact at score 18 (dead-name weight) instead of
inheriting it from file order; controls 0/18 false fires; lint 8/8.

### 3.4 Delivery: the forged native exchange (default lane — F-041)

Stage 0's channel result reproduced dramatically at 1k facts: prose fact
notes plus thinking made gemma spiral on glyph-heavy content — a BQN
question burned **8,189 reasoning tokens and produced no answer**. The
same facts through the tool channel: **390–757 completion tokens and a
correct answer**.

Real tool delivery needs client cooperation nothing off-the-shelf
provides. So the template **forges the exchange**: for the last user
message, if facts matched, it renders a completed `factbank_search`
call and response in gemma's own token syntax, using the source
template's own `format_tool_response_block` macro — bit-identical to a
real exchange. The model's experience: a lookup result arrived, the user
asked, it answers. Its visible reasoning treats the forge as real
("based on the documentation lookup provided…"). Guards: the lane stands
down when a client genuinely declares `factbank_search` (real Lane 1
then owns delivery via a tool_body rebind), and for non-string
(multimodal) content. No match → nothing renders → the request is
byte-identical to the stock template's.

### 3.5 Placement and the echo (F-042)

LM Studio has an undocumented reply-boundary layer that **echoed any
template text rendered after the final user text** into
`message.content` (token counts proved the model did not regenerate it;
measured live twice). Two candidate mechanisms fit: (a) content =
diff of render(with generation prompt) − render(without); (b) content =
everything after the last occurrence of the user's text. The fix
satisfies both: the forge is anchored **inside the message loop, before
the last user turn renders**, so it appears in both boundary renders and
upstream of the user's text. One trap caught offline: the forged query
originally quoted the question verbatim — a copy of the question
upstream of the real one is a false split point for mechanism (b); the
query now reads `current <libs> documentation`. Live v4: 9/9 replies
clean.

The placement pays an unplanned dividend: facts-before-question means
same-topic requests share a prompt prefix, so llama.cpp's cache skips
re-evaluating the fact block — repeat-topic TTFT drops from ~1.8 s to
0.24 s (server log: 22 of 551 tokens evaluated, LCP similarity 0.967).

## 4. The bank

1,027 facts: 94 from the frozen research bank (`facts_v2.jsonl`,
untouched — the deployment copies, the research bank stays frozen) plus
933 authored for 12 niche language ecosystems (Zig, Nim, OCaml, Raku,
Gleam, Crystal, D, Odin, Racket, Haxe, Janet, BQN). Every fact carries a
version tag and source.

The airtightness property is preserved by construction: facts target
post-2024 APIs and niche ecosystems the model provably cannot answer
from weights, so any correct answer must have come through the template.
**Provenance caveat, stated plainly:** the 933 niche facts were authored
by Claude from its knowledge, not extracted and gate-verified against
live documentation (documented in `niche_facts/README.md`). They are
demonstration-grade until spot-verified. The 94 research facts passed
the repo's verbatim-quote gates.

Density was calibrated before ranking landed: four sweep rounds drove
false injections on 44 no-match questions from 4 to **0** while keeping
15/15 own-language probes injecting own-language facts only. Root causes
were real bugs (a STOP-bypass for `App()`-style tokens; generic
vocabulary leaking in via dotted-token segments), both fixed in
`enrich.py`, both now regression-guarded by the culling report.

## 5. Measurements

### 5.1 Live acceptance (LM Studio, plain API calls, 1 rep — RESULTS §9)

Nine questions, single user message each, no tools, no tags, thinking ON,
temp 0.2. Transcripts: `live_v4_results.jsonl`.

| question | facts | echo | outcome |
|---|---|---|---|
| hello there | 0 | clean | normal greeting |
| haiku about the sea | 0 | clean | haiku, no facts dragged in |
| Python closure | 0 | clean | correct, no facts dragged in |
| BQN: sum a list | 5 | clean | **correct**: `+´` fold† |
| Zig: int→float | 5 | clean | **correct**: `@floatFromInt`, notes 0.11 removal of `@intToFloat` |
| Polars: wide→long | 5 | clean | **correct**: `unpivot(index=, on=)`, deprecation explained |
| whenever: current time in tz | 5 | clean | **correct**: `ZonedDateTime.now("Europe/Paris")` + `Instant.now().to_tz()` |
| "my polars melt code stopped working" | 5 | clean | **correct**: full melt→unpivot migration map |
| weather in Paris + fix melt (mixed) | 5 | clean | declined weather honestly, gave the rename |

† The BQN answer appended an invented `𝕨` "seed" example beyond the
fact — the bank delivered, the 12B embellished. This is the stage-0
USES-vs-CODE gap in miniature and is fixable by a fact edit, not by
architecture. It is left in this report deliberately: the thesis is
expert *knowledge delivery*, not model quality.

Every reply finished `stop` (reasoning 129–616 tokens — no spirals),
every fact answer matches its bank fact, and the model's reasoning
explicitly cites "the documentation lookup".

### 5.2 Timings (n=1 per question — indicative, not certified)

Full table and caveats: `TIMINGS-v4.md`. Backend: LM Studio / llama.cpp
Vulkan, RX 7900 XTX.

| situation | time to first token | after that |
|---|---|---|
| off-topic question | ~0.2 s | 60–62 tok/s |
| first question on a covered topic | 1.7–1.8 s | 60 tok/s |
| repeat question, same topic (prefix cached) | ~0.24 s | 60 tok/s |

Decomposition (from server logs): the template render — gate plus the
full 5-pass ranked scan over 1,027 facts — is bundled inside every TTFT
and costs **under 0.2 s**; the 1.5 s difference on first-match is the
GPU evaluating ~370 injected fact tokens at ~220 tok/s prompt speed
(~74 prompt tokens per fact). The ranked scan added ≈0.1–0.25 s over the
old two-pass scan on matched questions and nothing measurable on
no-match. Reference curve (llama-server standalone, measured): render
scales ~0.33 ms/fact — 94 facts ≈ 60 ms, 10k ≈ 3.4 s — so latency does
not cap the bank at this size; the density wall does.

**These are single measurements.** A 3-rep run at temp 0.2 (~20 min GPU)
is the named next step before any of these numbers is quoted without
this asterisk.

### 5.3 Cap pressure and ranking effect (offline, reproducible free)

`python rank_probe.py bank_enriched_scale.jsonl` — replicates the
template's matching in Python. Cap binds on 21/24 questions; ranked
selection changes the winners wherever any keyword or task-phrase signal
exists; tie bands did not overflow FB_MAX on any probe question;
controls 0/18.

## 6. What broke on the way (kept, per repo policy)

1. **Prose delivery + thinking spirals on glyph languages** (F-041):
   8,189 reasoning tokens, no answer. The channel is the fix, not a
   bigger budget.
2. **The echo, twice** (F-042): two placements after the final user text
   both echoed the forged block into the reply. The mechanism is
   undocumented and closed-source; only placement-before-question
   survived both candidate mechanisms.
3. **The forged query itself nearly re-broke the echo fix**: quoting the
   user's question verbatim upstream of the real question planted a
   false split point. Caught by the offline proof, not by luck.
4. **False injections at scale**: `script.janet` → "script", `App()`
   bypassing the STOP list — 4 rounds of density sweeps to zero.
5. **Dead-name detection by `kind` alone missed the research bank's
   rename facts** (polars melt→unpivot is kind `concept`); text markers
   fixed it.
6. **Selection by file order looked like it worked** — the probe showed
   the Zig success was luck. Measurement, not vibes, is why the ranker
   exists.

## 7. Limits and open items

- **Recall, not ranking, is the residual gap**: when a question names no
  API and matches no task phrase ("convert an integer to a float"), the
  ranker has nothing to rank and selection falls to floor order.
  Task-word/synonym coverage is the lever; semantic retrieval does not
  fit in a template.
- **The 933 authored facts are not doc-verified** (§4). Spot-verification
  against real documentation is queued work.
- **Timings are n=1** (§5.2).
- **Validated on gemma-4-12b only** at this scale; a qwen3 family base
  exists (anchors verified) but the scale bank and lanes have not been
  run on it.
- **The density wall above FB_MAX=5 is unprobed**: raising the cap costs
  ~74 prompt tokens and ~0.25 s per extra fact, but the binding
  constraint is model obedience under more facts, which needs its own
  measurement.
- **LM Studio's reply layer remains undocumented**: the fix is robust to
  both hypothesized mechanisms, but a future LM Studio version could
  change the rules. llama-server is unaffected either way.
- Baked artifact metadata still reads `factbank.version 0.3.0` (kit
  version, set at write time); the template itself is v3.3.0.

## 8. Reproduction (offline; no GPU, no models)

From `template-brain-v3.1/template-brain-v3.1/`:

```bash
python enrich.py facts_scale_v1.jsonl bank_enriched_scale.jsonl \
    --controls controls_repo.txt --taskwords taskwords_scale.json
python rank_probe.py bank_enriched_scale.jsonl        # §5.3 numbers
python make_base_gemma4.py                            # base guard, byte-exact
python bake_template_v3.py --base family_bases/gemma4.jinja \
    --source-template family_bases/gemma4.source.jinja \
    --enriched bank_enriched_scale.jsonl --raw facts_scale_v1.jsonl \
    --family gemma4 --out baked_gemma4_1k.jinja --cap 1100 --gate-n 8 \
    [--src-gguf <source> --dst-gguf <target>]         # GGUF write
python lint.py baked_gemma4_1k.jinja "scenarios_gemma4/*.json"   # 8/8
```

The live half (§5.1–5.2) requires LM Studio with the artifact loaded and
owner run permission (repo hard rules 1–2); the exact client is
`live_test.py`, and its raw output is `live_v4_results.jsonl`.

## 9. Provenance of every number

| claim | source |
|---|---|
| 9/9 clean, answers, reasoning/completion tokens, finish reasons | `live_v4_results.jsonl` + LM Studio server logs (RESULTS §9) |
| TTFT / tok/s / prompt-eval decomposition | same files; `TIMINGS-v4.md` |
| cap binds 21/24; controls 0/18; melt fact score 18 | `rank_probe.py` on `bank_enriched_scale.jsonl` (deterministic) |
| 8,189-token BQN spiral vs 390–757 native | FINDINGS F-041 (live logs, 2026-07-13) |
| echo measurements + fix proofs | FINDINGS F-042; proofs re-runnable via jinja2 against `baked_gemma4_1k.jinja` |
| density calibration 4→0 / 15/15 | build log `archive/docs/template-brain-v3.1-vs-repo.md` §4 |
| 0.33 ms/fact render curve | `bench_device.py` measurements (build log; memory: template-brain-latency-tolerance) |
| 73 facts / 277 dead keys; 1027 facts; 42 libraries | `enrich.py` output on `facts_scale_v1.jsonl` (deterministic) |
| GGUF integrity (template==bake, 667 tensors, 1027 pouch lines) | read-back check in the bake session (re-runnable: GGUFReader) |

---

# Part II — Generation 2: the search was the ceiling

*2026-07-14 · model `factbank/gemma-4-12b-pythondatafactbank-idx` ·
evidence: FINDINGS F-044…F-052, RESULTS §11–§12, `archive/docs/SEARCH-LAB-REPORT.md`,
`PROGRESS.md`*

## 10. What the scored test found

Part I proved the mechanism on niche languages, where the bar is low: the
model knows *nothing*, so any fact that arrives wins. Generation 2 aimed at
the opposite case — the mainstream Python data stack (pandas, polars, numpy,
scipy, scikit-learn, matplotlib), where the model has strong, confident,
and sometimes **stale** priors. A 2,560-fact bank (315 curated migration
facts + mined API signatures, from 46,834 introspected offline) was baked
with the Part I scanner and put through a scored A/B (`eval_pydata.py`,
importing the repo's AST scorer).

It failed, and the failure was precise. Asked to *"reshape a wide DataFrame
into long format"*, the model answered with **`melt()`** — the dead API. The
melt→unpivot fact was **in the bank**, and was **never retrieved**: five
low-value mined signature facts took its five slots. More facts had not
helped; **the search was the ceiling.** (RESULTS §11.)

The probe delivered a second, sharper lesson: **11 of 15 test cases were
invalid** — the bare model already knew the answers (the `applymap`→`map`
rename predates its cutoff). A case only measures the bank if the model
cannot already answer it. Probe-before-run is a repo rule for exactly this
reason, and it still caught us.

## 10.1 First: find out what the engine actually allows

Every design in Part I rested on assumptions about the template language
that had never been tested. So we tested them — one-feature templates
rendered through a live `llama-server` (`jinja_lab/probe_minja.py`).
minja, llama.cpp's Jinja engine, is what LM Studio really runs.

29 of 31 probed features work, including three we had ruled out: **`sort`,
`sort(attribute=…, reverse=true)`, `list.append()`, and `selectattr`**. Only
**dict item assignment** fails. No imports, no filesystem, no state between
requests.

Two traps came out of the same probe, and both had already bitten us:

- **llama.cpp probes the chat template at load time**, rendering it with
  synthetic inputs (multimodal content lists, empty message arrays, tool
  definitions) to auto-detect the tool-call format. If the template throws on
  *any* of them, the **whole model is rejected** ("Unable to generate parser
  for this template"). Our first index template did exactly that. Every
  template must guard: `{%- if messages and messages[-1]['content'] is
  string -%}`.
- **jinja2 ≠ minja** (F-050). minja's `.split()` does *not* collapse
  whitespace, and `d[x | int]` parses filter-vs-subscript differently. Both
  silently changed *which facts were retrieved*: the same template pulled 5
  facts under jinja2 and **1** under minja. Every offline gate in this repo
  renders with jinja2 — so, without a parity check, every offline result was
  a statement about a language we do not ship. `parity.py` now renders every
  gold question in **both** engines and refuses the bake unless they agree.
  It is a mandatory gate. Current: 22/22.

## 10.2 A gold set, so retrieval could be scored for free

Retrieval is measurable without a GPU and without baking: 12 questions, each
paired with the fact id it **must** retrieve (verified present in the bank),
plus 10 controls that must retrieve **nothing** (`jinja_lab/gold.json`). The
whole design space could then be evaluated offline in seconds — and executed
in the *real* engine without a 7 GB bake, because `llama-server
--chat-template-file` + `POST /apply-template` renders any template against
any question in ~10 s.

Building the gold set immediately caught two bad fact ids and one fact that
the bank's seat policy had silently evicted. The metric found bugs before it
found results.

## 10.3 The inverted index (F-051)

Seven designs were built and measured (`jinja_lab/designs.py`,
`lab_bench.py`, `stress.py`). The winner replaces the linear scanner
outright:

- **Postings, not scans.** The bank ships a dict `term → "factid:weight …"`
  built offline. The template splits the question into terms and looks each
  one up. No fact is ever visited unless a term points at it.
- **Facts in a LIST, not a dict.** Same algorithm, two data layouts: moving
  the fact texts from dicts into integer-indexed lists cut per-request cost
  **4–5×** (2,485 ms → 545 ms). minja constructs dict entries slowly; the
  *number of entries built per render* is the cost, not the lookup. Curated
  facts are sorted first, so provenance is `id < NCUR` — zero extra bytes.
- **IDF at build time.** A term appearing in ≤3 facts is evidence (×3); ≤10,
  weak (×2); common, noise (×1). Runtime stays pure integer addition. This is
  what stopped *"t-test with scipy"* returning `scipy.stats.dunnett`.
- **Squash-normalisation + a real alias table.** `t-test`→`ttest`,
  `scikit-learn`→`scikitlearn`/`scikit`/`learn`; `scikit-learn`→`sklearn`
  verified from `importlib.metadata.packages_distributions()`, plus
  `np`/`pd`/`plt`/`mpl`. Applied to the query **and** the gate.
- **Tab discipline.** A *named* library wins; inferred tabs open only when the
  question names none.

| | scanner (gen 1) | index (gen 2) |
|---|---:|---:|
| gold HIT@5 | 6/12 | 9/12 |
| control false-fires | 0/10 | 0/10 |
| data bytes in template | 949 KB | 809 KB |
| matched-question render (minja) | 2,629 ms | **545 ms** |
| long question | 4,077 ms | 1,116 ms |

The scanner is cheap when it does nothing (76 ms on a haiku) and expensive
when it works, because opening a tab makes it walk every fact in that tab
five times. The index is the opposite: a flat floor, barely growing with
question length.

## 10.4 Vocabulary was the last 3/12 — and it is cured offline (F-052)

The three remaining misses were not ranking failures. *"In polars, how do I
turn columns into rows?"* shares **zero words** with the fact that says
`melt()` was renamed to `unpivot()`. No keyword engine can bridge that.

The literature has an answer, and — decisively for us — it works **offline**,
which is the only place we can afford to spend anything
(`archive/docs/PRIOR-ART-RETRIEVAL.md`): **doc2query / SPLADE-doc / Walmart's Doc2Token**
predict the words a *user* would type and index those, letting the runtime
matcher stay dumb. **Doc2Query--** adds the crucial refinement: filter the
generated expansions, and you get *better* effectiveness at *smaller* index
size.

So the served model wrote its own expansions: 6 everyday questions per
curated fact — *"how do I pivot longer in polars?"* — for all **388** curated
facts, **2,326 questions**, filtered to 5 phrases each (bigrams and long
unigrams), indexed at a weight strictly **below** real terms. Cost: 8 minutes
of CPU-side generation, zero runtime cost, bytes only on the facts that
deserve them.

Two operational lessons, both already in FINDINGS and both re-learned the
hard way:

- **Thinking ON silently destroys generation.** A model reload reset LM
  Studio's thinking toggle; the model then burned its whole token budget
  reasoning and returned **empty content** — 3 of 4 calls, 900 tokens of
  nothing, 90 s each. LM Studio drops `chat_template_kwargs` (F-018);
  **llama-server honours it**. Same work, thinking off, on llama-server:
  388/388 in 8 minutes.
- **The template has a hard byte ceiling** (F-048): LM Studio silently refuses
  templates above ~1 MiB — no error, 15-token prompts, garbage out. The bake's
  size guard (hard-fail >957 KB) fired **twice** during expansion work and
  prevented shipping a brick both times. To buy the bytes, the bank was cut
  **2,560 → 1,911 facts**. Retrieval doubled while the fact count fell 25%:
  the right trade, and the reason a terse-fact rewrite is the next lever.

## 10.5 Result (RESULTS §12)

Same bank, same weights, same delivery lane. **Only the search changed.**

| | scanner (was shipped) | index + cures (shipped now) |
|---|---:|---:|
| gold facts retrieved | 6/12 | **12/12** |
| control false-fires | 0/10 | 0/10 |
| matched-question render (minja) | 2,629 ms | **545 ms** |
| engine parity (jinja2 vs minja) | never tested | **22/22** |
| lint scenarios | 8/8 | 8/8 |
| live (plain API calls, LM Studio) | — | **10/10 clean**, TTFT 0.18–1.91 s |

The four questions that used to fail — *"turn columns into rows"* (answered
with the dead `melt()`), *"t-test with scipy"* (returned `dunnett`), *"split
data with scikit-learn"* (retrieved nothing), *"np.NaN"* — **all answer
correctly now.**

Shipped artifact:
`C:\Users\mhnda\.lmstudio\models\factbank\gemma-4-12b-pythondatafactbank-idx\
gemma-4-12B-it-QAT-Q4_0-pythondatafactbank-idx.gguf` — 1,911 facts, 950 KB
template, all 667 tensors byte-identical to the base, two metadata keys
rewritten.

## 11. What generation 2 still has not done

- **The ranker is still the generation-1 ranker**: five max-selection passes
  and O(h²) score totalling by re-walking a string — workarounds for
  constraints that **do not exist** (§10.1). Rewriting it with
  `append` + `sort(attribute=…, reverse=true)` is the cheapest remaining
  speed-up.
- **Gold is a retrieval metric, not an end-to-end score.** Proving the right
  fact reaches the model is necessary, not sufficient — the model still has
  to obey it. The end-to-end scored eval (`eval_pydata.py`) needs a rebuilt
  case set, because the probe showed 11 of 15 old cases were invalid.
- **Impact-ordered postings and eager quantized impacts** (bake the whole
  score into the posting weight, stop early) are known wins from prior art,
  not yet taken.
- **The terse-fact experiment is unmeasured**: ~3× smaller facts would fit
  ~3× more per template, but only if the model still *obeys* the shorthand.
- The other domain models (`pythonweb`, `aisdk`, `pystdlib`) sit unmined-but-
  ready in the 46,834 introspected facts.

## 12. The lesson, in one line

Part I asked whether a fact bank fits inside a chat template. It does.
Part II asked whether that is enough. It is not — **a bank you cannot search
is a bank you do not have**, and the search, not the fact count, was what
stood between an unmodified 12B and the right answer.

---

# Part III — What the ceiling actually was

*2026-07-14 · evidence: FINDINGS F-053…F-057, RESULTS §13 · all measurements
CPU-only on pure llama.cpp b9851*

## 13. The 1 MB wall was never ours

Both earlier parts were designed around a hard constraint: **templates above
~1 MiB do not work** (F-048). It shaped the bank size, forced the fact count
down from 2,560 to 1,911, and made "bytes" the currency of every design
decision in §10.

The constraint was real. It was also **entirely LM Studio's**, and its
mechanism is not what anyone would guess. LM Studio's GGUF metadata reader
**silently replaces** an over-long string with a 47-character placeholder
(`[LM Studio Patch - String too long; didn't read]`). The model then loads
"successfully" with a chat template that contains no `{{ messages }}` at all.
That is why the symptom was 15-token prompts and garbage answers with no error
anywhere: the template did not fail to *parse*, it failed to **exist**.

The evidence sits in LM Studio's own cache: our bricked bakes have a **48-char**
template; the shipped one has 972,985.

Meanwhile, the same backend binary LM Studio itself spawns:

| test | result |
|---|---|
| 1.5 MB template via `--chat-template-file` | **renders perfectly** |
| 1.5 MB template **embedded in a GGUF**, `--jinja` | **loads and renders**, forged tool block intact |

llama.cpp caps metadata strings at **1 GiB** and errors *loudly*. The GGUF format
length-prefixes strings with a `uint64`. **Nothing in the architecture had a 1 MB
limit.** One application did, and it hid it.

Two corrections fall out of the same investigation (F-054). LM Studio **renders
in llama.cpp** — it spawns `llama-server --jinja --chat-template-file` and hands
over a byte-identical copy of the template — so the parity gate of §10.1 was
aimed correctly all along. And **minja no longer exists**: llama.cpp PR #18462
replaced it with a new C++ Jinja engine. Where this paper says "minja", read
"llama.cpp's Jinja engine".

## 14. Latency was never the ceiling either

With the byte wall gone, the obvious next question is what *does* bound the
bank. The standing answer was F-045: the engine re-parses the template on every
request at ~0.33 ms/fact, so **fact count is a latency budget**. We measured it,
on pure llama.cpp, up to 21,203 facts:

| facts | template | no-match | matched | long question | ms/fact |
|---:|---:|---:|---:|---:|---:|
| 2,314 | 1.06 MB | 102 ms | 197 ms | 1,344 ms | 0.085 |
| 4,564 | 1.69 MB | 115 ms | 95 ms | 1,078 ms | 0.021 |
| 8,837 | 2.71 MB | 158 ms | 138 ms | 638 ms | 0.016 |
| **21,203** | **5.06 MB** | **239 ms** | **218 ms** | **655 ms** | **0.010** |

**A 5 MB, 21,000-fact template renders a matched question faster than the
950 KB one we shipped.** Cost per fact *falls* eightfold as the bank grows.

F-045 was not wrong — it was **measured on the linear scanner under jinja2**.
The inverted index changed the complexity class: it visits only the facts a
query's terms point at, so render cost tracks the **query**, not the bank. The
old law is retired for the index path, and the code that still preaches it
(`select_facts.py`'s header) has been marked stale.

**Bytes: abundant. Milliseconds: abundant.**

## 15. The real wall: precision at density

So we can hold 21,000 facts, cheaply and quickly. Can we *find* them?

| facts | template | GOLD | controls |
|---:|---:|:---:|:---:|
| 2,314 | 1.06 MB | **12/12** | 0/10 |
| 4,564 | 1.69 MB | 11/12 | 0/10 |
| 8,837 | 2.71 MB | **9/12** | 0/10 |
| 21,203 | 5.06 MB | **9/12** | 0/10 |

**Recall decays as the bank grows, and the controls never false-fire.** That
combination is the whole finding: a large bank does not become *noisy* — it
becomes **unfocused**. Nothing wrong is dragged in; the *right* fact simply
loses its slot to competitors. At 21k, the `resample` frequency-alias fact
retrieves **nothing at all** (its gate never opens), and `np.NaN` pulls five
facts, none of them the one that matters.

The causes are all the same shape: **constants calibrated at 2,000 facts,
applied to 21,000.** `DF_CAP=40`, the IDF buckets (≤3 postings ×3, ≤10 ×2), the
48 gate triggers per library, and `FB_MAX=5` slots — none of them scale with
bank size, and the last one got contested ten times harder while latency got
cheaper. On top of that, the Doc2Token expansions of §10.4 cover only the 388
curated facts, so the mined majority adds *competitors* without adding
*bridges*.

**Growing the bank is therefore a retrieval-calibration problem, not a capacity
problem.** A 20k bank that retrieves worse than a 2k bank is a regression, no
matter how much knowledge is nominally inside it.

## 16. The wall came down (F-059)

§13 concluded that the ~1 MB ceiling was LM Studio's and, for LM Studio users,
final: ship a second, llama-server-only edition and put the warning in the
filename. **That conclusion lasted one day, and it was wrong.**

The cap lives in exactly one code path — LM Studio's **GGUF-metadata reader**.
LM Studio has a *second* way to receive a chat template: the load-time config
field `llm.load.promptTemplate`, which a Hub `model.yaml` sets. It has **no size
limit**. LM Studio writes the string to a temp file and hands it to llama.cpp via
`--chat-template-file` — and llama.cpp never had a limit.

Proven live, against the real `llama-server` process LM Studio spawned:

| gate | 1.5 MB | 2.0 MB |
|---|---|---|
| bytes handed to the engine | **1,536,014** | **2,048,014** |
| not the sentinel · >1 MiB · canary · SHA-256 match | PASS | PASS |

On that same load a matched question rendered **390 prompt tokens** with the
melt→unpivot fact injected and `unpivot` in the answer; a control rendered **112
tokens** with no facts. And the Hub carries it: a 1.95 MB `model.yaml` was
accepted (1.53 MB uploaded — incompressible worst case) and cloned back with the
template **intact at 2,047,990 bytes**.

Three traps, each of which silently defeats the route, are recorded in
`FACTBANK-SHIPPING-BLUEPRINT.md`: it must be **load-only** (adding
`llm.prediction.promptTemplate` makes every completion return HTTP 500);
`metadataOverrides` is **mandatory** (without it the manifest is refused and the
model never appears at all); and the manifest is **cached** (an edited template
can silently reload as the old one).

**So there is one artifact, not two.** A single GGUF carries a safe ≤950 KB bank
that works everywhere and never bricks; the Hub manifest layers the multi-MB bank
on top for LM Studio users; llama.cpp users get it embedded or by file. Every
route degrades gracefully rather than bricking.

## 17. Where this leaves the thesis

Four questions, four ceilings, and the honest shape of the result:

1. **Can a fact bank live inside a model file?** Yes (Part I).
2. **Is holding the facts enough?** No — the search was the ceiling (Part II).
3. **Was the byte ceiling real?** It was one application's undocumented cap, and
   it is now bypassed (§16). Bytes and milliseconds are both abundant.
4. **Is the search fixed?** At 2k facts, yes: 12/12. At 21k, **no** — the binding
   constraint is **targeting** (§15).

Every wall we hit turned out to sit somewhere other than where we thought: not in
the format, not in the engine, not on the clock. The one that remains is the only
one that was ever really ours — **a bank you cannot search is a bank you do not
have** — and it is now true at scale as well as at rest.

The architecture scales. The retriever, so far, does not. That is a far better
problem to have than the one we thought we had, because every lever left is
offline, free, and measurable: no GPU, no bake, no training. But it is
unfinished, and this paper says so.

---

*Weights untouched. One file. The model is the know-how; this is the
knowledge.*
