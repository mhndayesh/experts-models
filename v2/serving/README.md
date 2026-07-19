# FactBank — documentation (serving)

> **v2 PATHS (2026-07-15).** This folder is `v2/serving/`. Fact-**making** is now the LLM-first
> extractor in [`../extractor/`](../extractor/) (see its `BLUEPRINT.md`); the bake **code** is in
> [`../bake/`](../bake/); the GGUF/model **binaries** are archived in
> `archive/pre-v2-2026-07-15/template-brain-v3.1/`. Command examples below that say
> `template-brain-v3.1/template-brain-v3.1/` refer to that archived kit — run them from `../bake/…`
> for the code, or from the archived kit if you need the binaries. Older `card-mining` references
> are the superseded rules chapter, now in `archive/pre-v2-2026-07-15/card-mining/`.

**A stock 12B model, unmodified, answering correctly about libraries released after it
was trained — shipped as one GGUF file.**

Written from scratch on **2026-07-14**. Every number here was re-verified against the
live artifacts on that date; nothing is inherited on faith. This folder replaces the
older scattered docs at the repo root, which remain as the historical record.

---

## What it is, in one paragraph

The model's weights are untouched. Inside the GGUF's `tokenizer.chat_template` — a Jinja
program every serving stack already runs on every request — we put a **fact bank**, an
**inverted-index retriever**, and a **delivery lane** that hands retrieved facts to the
model through its own native tool protocol. The model supplies reasoning (the know-how);
the template supplies knowledge. Copy the file, load it in LM Studio, ask a plain API
question: it answers correctly about APIs that did not exist when it was trained.

## Current state

| | |
|---|---|
| shipped model | `factbank/gemma-4-12b-pythondatafactbank-idx` |
| base | gemma-4-12B-it QAT Q4_0 — **all 667 tensors byte-identical**, 2 metadata keys rewritten |
| bank | **1,911 facts** (388 curated + 1,523 mined signatures), 10 Python data libraries. **The 388 curated `mistake` facts do all the work — mined signatures have won ZERO eval cases (F-065).** |
| template | **973,652 bytes** = 972,985 chars (951 KiB). *Chars are not bytes — every size cap in this project is a BYTE cap (F-066).* |
| retrieval | **gold 12/12** · controls 0/10 · lint 8/8 · parity 22/22 |
| live | **10/10 clean**, TTFT 0.18–1.91 s |
| status | **delivery is solved** (all three routes). NOT unqualified "ready to ship": on the 76-case dense eval v7 is **level with the shipped v6** (21/25 vs 20/25 decisive; bare 3/25 — F-065), the mined half of the bank has won **zero** cases, and the mine it came from was **66% junk** (F-064) |

## The documents

| file | what it answers |
|---|---|
| **[ARCHITECTURE.md](ARCHITECTURE.md)** | How it works — how facts are stored, shaped, retrieved, and delivered |
| **[RESULTS.md](RESULTS.md)** | Every measured number, with the conditions it was measured under |
| **[SHIPPING.md](SHIPPING.md)** | How to publish it — three routes, the `model.yaml`, the gates, the traps |
| **[OPERATIONS.md](OPERATIONS.md)** | Commands: build a bank, bake, gate, test. What to run and in what order |
| **[RETRIEVAL-V7.md](RETRIEVAL-V7.md)** | **Current retrieval design (2026-07-14).** The *gate*, not the ranking, was the bottleneck: 66% of unreachable facts never reached the index. All gates pass — gold 12/12, controls 0/10, parity 22/22, obedience 8/8 vs 3/8 bare. Both shipping routes verified |
| **[RESULTS.md §8](RESULTS.md)** | **Fact quality (2026-07-14).** The mined bank was **66% junk** — inherited duplicates, `str.join` filed as a matplotlib fact. 24,133 → 8,096. The junk is the likely cause of the recall collapse at scale |
| [RETRIEVAL-NEXT.md](RETRIEVAL-NEXT.md) | Research from IR fundamentals. **Its headline proposal (delete the gate) was tested and FAILED** — kept as the record of why |
| **[LIMITS.md](LIMITS.md)** | What is broken, unproven, or unfinished — read before promising anything |
| **[PAPER.md](PAPER.md)** | The research paper: the question, the four ceilings, and what was learned |

## The three claims worth remembering

1. **A retrieval system fits inside a chat template.** No server, no client code, no
   sidecar files, no fine-tuning. One file, and the expertise travels with it.

2. **A bank you cannot search is a bank you do not have.** The first version held 2,560
   facts and answered with a *dead* API, because the right fact was never retrieved. The
   fix was the search, not the fact count — and it doubled retrieval (6/12 → 12/12)
   while the bank *shrank* to 1,911.

3. **Every wall we hit was somewhere other than where we thought.** Not the GGUF format.
   Not the engine. Not the clock. The ~1 MB LM Studio ceiling turned out to be one
   application's undocumented cap, and it is now bypassed. The only wall left is
   **targeting**: at 21k facts the retriever finds *fewer* of the right facts, not more.

## Provenance

The full chronological evidence trail — 65 numbered findings, including every mistake —
lives in `archive/docs/FINDINGS.md` (the project's full archive, not included in this repo). That file is the history; this folder is the
current truth. Where they disagree, this folder is newer.
