# Retrieval v7 — the gate was the bottleneck, not the ranking

> **2026-07-17 addendum — the gate also dies on NATURAL/OLD names.** This doc showed 66% of misses die
> because "the gate opened no tab at all." Building the offsec + dataplane experts found a further trigger
> of that same failure: the gate opens on the exact lib token but a user types a natural or old name
> ("BloodHound" not `bloodhound-py`, "CrackMapExec" not `netexec`), so no tab opens and 0 facts inject
> (proven with `render_retrieval.py`: bh01 = 0 facts on all 3 sizes). Fix = **gate aliases** derived from
> each rename fact's OLD name + the lib's natural stem (`gen_gate_aliases.py` → `bake_index.py
> --extra-aliases`). The OLD name of a rename is precisely the query a stale user issues; make it a trigger.

Measured 2026-07-14. Shipping candidate: **`rescue_v7.jinja`** (1,023,287 bytes).
Evidence: `../../archive/docs/FINDINGS.md` F-060…F-063.

**All gates pass, including obedience and both shipping routes.** The previous model
(`baked_index_v6.jinja`) is untouched and still the one in `factbank/gemma-4-12b-pythondatafactbank-idx`.

| gate | result |
|---|---|
| gold | 12/12 |
| controls (fact-slavery) | 0/10 |
| engine parity (jinja2 vs llama.cpp) | 22/22 |
| lint scenarios | 8/8 |
| **answer obedience** (76-case dense eval, MANUALLY scored — F-065) | **v7 21/25 decisive · shipped v6 20/25 · bare 3/25.** The bank is worth 12%→80%. **v7 buys essentially ZERO gain over the model already shipped.** |
| **GGUF → llama.cpp** | verified: SHA matches, 667 tensors untouched, retrieves from the file alone |
| **LM Studio Hub** | verified: pushed, pulled, SHA-256 identical, still retrieves |
| deterministic bake | byte-identical |

**The eval RAN, and v7 did not pay.** 76 cases, every answer hand-read (F-065). v7's gains
are **retrieval-only** — reachability 76.6% → 84.1%, dead facts 447 → 303 — and those gains
**did not convert into answer quality**. Head-to-head v7 wins twice (polars `.melt`, where
bare *and* shipped both emit broken code; `np.cast`, which shipped cannot retrieve at all) and
loses once (it answers about **pandas** on a question that names no library — the rescue gate
firing when it should not).

**Shipping v7 is therefore an open owner decision, not a foregone conclusion.** It is
strictly better at retrieval and level on answers. The case for it is future-proofing at
scale; the case against is that it buys one case in 76 and adds a fact-slavery failure mode.

---

## 1. The diagnosis that changed the design

The shipped model scores 12/12 on its gold set. But gold measures **twelve questions**.
Asked instead what fraction of the *whole* bank any realistic question can pull, the
answer was **76.6%** — **447 facts that nothing could retrieve.**

Worse, the split was inverted: the **curated** facts (renames, removals, gotchas — the
reason the bank exists) were the *least* reachable at **64.4%**, below the shallow mined
signatures at 79.7%.

Then the question that mattered: are those facts **outranked**, or never **scored**?

| why a curated fact was unreachable | share |
|---|---:|
| **the gate opened no tab at all — the index was never consulted** | **66%** |
| gate opened tabs, but not its library | 12% |
| gate opened its library; it lost on rank | 22% |

**Two thirds of failures happen before ranking runs.** Every ranking idea — dedup, MMR,
discriminative weighting, seat reservation — addresses the 22%.

The killer questions are **symptom language**: they name no library and no API.

```
"why is setting strides not allowed anymore"            → no tab opens
"how to fix chained assignment error after upgrade"     → no tab opens
"what should i use instead of safe_eval for strings?"   → no tab opens
```

## 2. The fix: three build-time changes, zero runtime changes

The template's Jinja code is **byte-for-byte unchanged**. No new engine feature, no
`sort`, no `append`. Everything moved into the index at bake time.

| # | change | flag | why |
|---|---|---|---|
| 1 | gate trigger cap **48 → 150** | `--gate-n 150` | a constant nobody had ever swept |
| 2 | **real IDF**, `log(N/df)`, replacing the 3-bucket guess (×3/×2/×1) | `--idf smooth` | this is what fixed the *mined* facts |
| 3 | **the gate can see the Doc2Token expansions** | `--gate-expansions` | biggest lever. We already had the model's predictions of how users phrase things — we indexed them and never told the gate |

Change 3 is the one to understand. The expansions exist precisely to bridge
symptom-language ("chained assignment error after upgrade") to a fact. They were in the
**index** but not in the **gate** — so the gate slammed the door before the index it
would have matched was ever opened.

Gate triggers from expansions are filtered: a word must be unique to one library and
control-safe (the F-046 cull applies here too), so a haiku still opens nothing.

## 3. Results

Held-out evaluation: 2 of each curated fact's 6 expansion questions are **removed from
the index**, and the fact is probed with exactly those. It has never seen the words it is
asked with. (Without this, facts retrieve themselves and every design scores ~100%.)

| | shipped | **candidate v7** |
|---|---:|---:|
| curated reachability | 64.4% | **74.5%** |
| mined reachability | 79.6% | **85.8%** |
| **bank reachability** | 76.6% | **83.5%** |
| dead facts | 447 | **315** |
| questions that retrieved nothing | 287 | **147** |
| precision (paired, see below) | 90.4% | **90.9%** |
| gold | 12/12 | **12/12** |
| controls fired (fact-slavery) | 0/10 | **0/10** |
| engine parity (jinja2 vs llama.cpp) | — | **22/22** |
| lint scenarios | — | **8/8** |

**Not overfit.** The config was chosen by sweeping, so the questions were split in half:
tune vs. verify. The gain is *larger* on the half the sweep never saw.

| | tune half | verify half (unseen) |
|---|---:|---:|
| shipped | 67.5% | 61.3% |
| candidate | 76.3% | **72.7%** |

**The precision "regression" was an artifact.** Raw precision appeared to fall
(90.4% → 87.4%), but the shipped template earns its score partly by **staying silent** on
287 questions — and silence cannot be imprecise. Compared only on the 489 questions where
*both* templates speak, the candidate is slightly **more** precise (90.9% vs 90.4%). It is
not a recall/precision trade; it is strictly better.

## 4. What was tried and FAILED

Recorded because these were the confident ideas, and the data killed them.

| idea | result |
|---|---|
| **discriminative weighting** (weight a term by how well it separates a fact from its near-duplicate siblings) | **+0.0 curated.** The clustering keyed on API names; the colliding pandas facts overlap on *description* words, so it never fired on them |
| **BM25 length normalisation** | **−0.2 curated**, and cost a gold case |
| **dedup / MMR / seat reservation** | aimed at ranking losses — only **22%** of failures |
| **tightening the expansion-gate** (longer, rarer triggers) | lost recall, recovered **no** precision (there was none to recover) |

The "seat-stealer" story — four near-duplicate pandas `str`-dtype facts stealing 247 slots
— is **real but secondary**. It is a symptom of the 22%, not the 66%.

## 5. A real bug fixed on the way

**13 facts in the shipped bank contain raw memory addresses:**

```
pandas.Timedelta(value=<object object at 0x000001A8A4C73BD0>, unit=None, ...)
sklearn.feature_selection.SelectFdr(score_func=<function f_classif at 0x000002BF11C20F40>)
```

The miner introspected live sentinel defaults and captured their `repr()`. Beyond being
useless to the model, **the address changes every process — so those facts made the bank
non-reproducible**, silently violating the determinism rule F-058 exists to enforce.

`bake_index.sanitize()` now strips the address and keeps the description
(`<function f_classif>`). Zero addresses remain; two bakes are byte-identical.

## 6. Size and the shipping route

The candidate is **1,006,990 bytes**. That is over LM Studio's **raw-GGUF metadata cap**
(980,000) — and *only* that route. Per F-059:

| route | cap | candidate v7 |
|---|---|---|
| **llama.cpp** | 1 GiB, errors loudly | **ships as-is** |
| **LM Studio via Hub `model.yaml`** (`llm.load.promptTemplate`) | none (proven at 1.5 MB, 2.0 MB) | **ships as-is** |
| raw GGUF loaded by hand in LM Studio | **980 KB — fails silently** | needs a trimmed build |

`baseline.py --route {rawgguf,llamacpp,hub}` now reports against the right ceiling instead
of a false failure.

## 7. The harness (all offline, no GPU)

| script | what it does |
|---|---|
| `baseline.py` | **the regression contract**: gold, controls, size, route. Run before and after every change |
| `reach.py` | **reachability**: holds out 2 expansions per fact, re-bakes, probes with them. Reports dead facts + seat-stealers |
| `exp_retrieval.py` | scores design variants side by side |
| `exp_gate.py` | sweeps gate specificity, reporting **recall and precision together** |

Reachability is the metric that scales: it needs no hand-written gold questions, so it
stays meaningful at 2k, 21k, or 200k facts.

**Speed note:** the probe renders a 1 MB template ~2,300 times. Compiling the template
once (instead of per render) and fanning across cores took a run from ~4 minutes to
**4.9 seconds**, with identical results.

### Reproduce

```bash
cd "template-brain-v3.1/template-brain-v3.1"

python bake_index.py --facts facts_pythondata_v4.jsonl --expansions expansions_v2.json \
    --out candidate_v7.jinja --gate-n 150 --idf smooth --gate-expansions --max-bytes 2000000

python baseline.py candidate_v7.jinja --route llamacpp     # gold 12/12, controls 0/10
python reach.py                                            # reachability, dead facts
python parity.py candidate_v7.jinja                        # 22/22  (spawns llama-server)
python lint.py candidate_v7.jinja "scenarios_pydata/*.json"   # 8/8   (spawns llama-server)
```

## 8. What is NOT proven

- ~~**Obedience — not yet run.**~~ **RUN, and it did not pay** (F-065). Against the shipped
  v6 as control, on 76 hand-scored cases: **v7 21/25 decisive, shipped 20/25, bare 3/25.**
  Every number in this document says the fact *reaches* the model; the eval says the model
  **already used it just as well without v7**. Retrieval reachability did not convert into
  answer quality. That is the USES/CODE gap, and v7 does not close it.
- **Mined signature facts have never won a case.** Every case the bank carried was won by a
  curated `mistake` fact. Do not assume a bigger or cleaner signature bank improves
  obedience — there is no evidence either way (F-064, F-065).
- **315 facts are still dead**, and ~61% of those still die at the gate on symptom-only
  questions. The next lever is a **runtime gate fallback** (if no tab opens but a weight-10
  dead-API term hits, open it anyway) — a template change, so it must clear `parity.py`,
  and it is the one change that could reopen control false-fires.
- **The bake path.** `write_baked` writing this template into a GGUF has not been
  re-verified at this size. Cheap check, no model needed: bake, read the metadata back,
  diff.


---

## 9. The rescue gate (F-062) — and the idea it replaced

**The proposal was to delete the gate entirely.** The argument was strong: an inverted
index *is already a filter* — a fact is only visited if a query term points at it — so a
hard library pre-filter in front of it can only ever *remove* recall. And the gate was
designed for the **linear scanner** (generation 1), where it was the whole performance
story. When the scanner was replaced by an index, its reason to exist disappeared.

**Measured: the argument is wrong.**

```
controls fired  8/10        FACT-SLAVERY
gold           10/12        REGRESSED
'write a haiku about the sea'  ->  polars1-011, pandas3-001, pandas3-137, ...
```

The claim was "control words are culled from the index (F-046), so the index protects
itself." But the cull only removes **strong keys**. Every fact *also* indexes its
**description words** at weight 3 — ordinary English. A haiku hits enough of them to drag
five polars facts in. **The gate is load-bearing, not vestigial.**

The failed run still bought something: it measured **the ceiling — 82.5% curated** — what
perfect gating would be worth.

**The rescue gate is the narrow version, and it works.** Keep the gate. Only when *nothing*
opens, let a **weight-10 dead API name** open its own library. 657 such terms, every one an
API name (`safe_eval`, `row_stack`, `__setitem__`), each unique to one library and absent
from every control question. A haiku contains none of them.

| | shipped | v7 | **v7 + rescue** |
|---|---:|---:|---:|
| curated reachability | 64.4% | 74.5% | **77.6%** |
| bank reachability | 76.6% | 83.5% | **84.1%** |
| dead facts | 447 | 315 | **303** |
| gold | 12/12 | 12/12 | **12/12** |
| controls | 0/10 | 0/10 | **0/10** |

It captures ~40% of the gap to the ceiling. The rest is symptom-language questions with no
API name in them at all — no gate rule can rescue those. Only filtered expansions
(Doc2Query--) can.

## 10. Live obedience (F-063) — the model uses what it is given

Every other number measures **delivery**. This measures **use**.

**Method, and it costs no extra VRAM:** the template's only job is to build a prompt. So
render it in Python and POST the result to `/v1/completions` on the model the owner already
loaded — **stock `google/gemma-4-12b-qat`, unmodified weights.** The model sees the exact
bytes the baked GGUF would give it. Arms: the stock gemma template (no bank) vs. the rescue
template. Same model, same decoding; the only variable is the template. Scoring is
**structural** — inside code fences only, comments stripped (F-029).

```
bare (stock template, no bank)   3/8 obeyed
rescue (bank + index + gate)     8/8 obeyed
```

The stock model wrote a **dead API in real code three times** (`np.cast`, `np.row_stack`,
`DataFrame.first()`). With the bank, it used the live API every time. Controls stayed clean
*live*, not just in the harness.

**The honest limit:** 3 of the 8 cases the bare model already answers, so they cannot
measure the bank at all (F-028). On the **5 discriminating cases: bare 0/5, rescue 5/5.**
Five cases at n=1 is a signal, not a result — hence the 100-case eval.

## 11. Both shipping routes, verified end to end

**Route 1 — GGUF for llama.cpp.** Baked into the stock 12B:

```
template in GGUF : 1,023,287 chars     SHA matches source
sentinel         : none                not swapped by any reader
bank carried     : 746,598 chars
tensors          : 667 -> 667          weights byte-identical
```

Loaded in `llama-server` **with no `--chat-template-file`**, the model file retrieved on its
own — the `"M"` → `"ME"` fact at rank 1, its `Q`/`Y`/`H` siblings behind it.

**Route 2 — LM Studio Hub.** Pushed to `mhndayesh/factbank-hubroute-v7`, pulled back, and
diffed: **SHA-256 identical** (modulo YAML's trailing newline), rescue map intact, and it
still retrieves through the Hub-returned template.

**One correction:** at 1,023,287 bytes the v7 template is **0.98 MiB — just *under* 1 MiB**.
It does not by itself re-prove F-059's >1 MiB delivery (that stands at 1.5 MB and 2.0 MB).
What it proves is that the *real* bank template survives the Hub route intact and works. It
is still over the **980 KB raw-GGUF guard**, so the raw-GGUF-by-hand route needs a trimmed
build.

## 12. Reproduce

```bash
cd "template-brain-v3.1/template-brain-v3.1"

python bake_index.py --facts facts_pythondata_v4.jsonl --expansions expansions_v2.json     --family gemma4_rescue --gate-n 150 --idf smooth --gate-expansions --rescue-gate     --max-bytes 2000000 --out rescue_v7.jinja     [--src-gguf <stock.gguf> --dst-gguf <out.gguf>]

python baseline.py rescue_v7.jinja --route llamacpp      # gold 12/12, controls 0/10
python reach.py                                          # reachability, dead facts
python parity.py rescue_v7.jinja                         # 22/22   (spawns llama-server)
python lint.py rescue_v7.jinja "scenarios_pydata/*.json" # 8/8     (spawns llama-server)
python live_obey.py                                      # obedience vs bare (uses the LOADED model)
```
