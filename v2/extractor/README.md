# structured-extractor — LLM-first fact extraction (the current fact-making engine)

> **Status: this is the CURRENT engine that built every shipped bank.** Proven end-to-end
> (k8s 96.5%, pydantic 97.8% clean, hand-read) and used to build all shipped experts —
> AI-ML (817 facts), GitChameleon (4,167, baked + benchmarked), Web (279), DevOps (74),
> Security & Networking (114, baked + tested). It is the successor to the *rules* extractor
> (now archived in `archive/pre-v2-2026-07-15/card-mining/`) for the hard case: mining landmine
> facts out of **prose** (migration guides, upgrade docs) that the bullet-rules miner cannot read.
> The rules chapter still stands for clean bulleted changelogs; this is the mechanism for everything else.
>
> **2026-07-18: see `EXTRACTOR-2.0.md` for the newer code-bearing pipeline.** A parallel, newer engine
> (`appsec_core.py` + thin per-source adapters — code lives IN the fact as verbatim `code_bad`/`code_good`)
> built the **appsec expert** (3,984 variants, 1,075 w/code), currency- and correctness-audited. **SHIPPED** —
> shipped bank `FINAL_v3.jsonl`; baked ×3 sizes × both thinking editions, published to HF + LM Studio Hub.
> Where the two disagree, 2.0 wins for that lane; the `extract.py`/`repair.py`/
> `check.py` pipeline below remains the mechanism that built the experts listed above.

## Why this exists — the four things the rules miner couldn't do
1. **Source targeting** was a manual guess (transformers got 8 facts instead of hundreds).
2. **Narrow intake** — the rules miner reads bulleted changelogs only; prose guides → ~0 facts.
3. **No landmine-vs-noise judgment** — the gate checked structure, not "would a user hit this."
4. **Blind to what it missed** — fact count ≠ real churn density.

This design attacks #2 and #3 head-on by **inverting the roles**: the LLM does the *meaning*
(read any shape, extract the change), and **dumb code verifies every bit** because the LLM fills
a strict schema.

## The mechanism

```
extract.py   LLM reads ANY-shape source, fills a STRICT schema via function-calling.
             Code DERIVES what the model shouldn't decide:
               - type      (reconciled from presence of `new`)
               - from_fact keywords (pulled from old/new/truth in code -> always grounded)
             The model fills ONLY meaning: subject, old, new?, truth, why_it_bites, quote,
             and `associative` keywords (the logical "could-be" search terms NOT in the fact -
             e.g. an API that connects to a provider gets "connect to provider").

repair.py    A SECOND pass that is a CHECKER, not an extractor. Facts dropped for a paraphrased
             quote are re-grounded by SNAPPING the quote to the real verbatim source line that
             mentions the fact's own symbol. No LLM, no new facts. If no source line mentions the
             symbol, the fact was genuinely ungrounded and STAYS dropped.

check.py     Raw checker over the clean JSON. The load-bearing gate is the anti-hallucination
             anchor: `quote` must appear VERBATIM in the source. Triage, not verdict (F-065).
```

Run it end-to-end with `run.py`:

```bash
DEEPSEEK_API_KEY=... python run.py <source> <lib> <version>
# e.g. python run.py sources_harvested/python-ai/pydantic.migration.md pydantic 2.x
```

Backend: DeepSeek `deepseek-v4-flash`, thinking OFF, **function-calling** (DeepSeek has no strict
`json_schema` mode — verified). Cloud, no GPU. Key read from `DEEPSEEK_API_KEY`, never written to disk.

## Proven (measured 2026-07-15, hand-read)

| source | shape | extracted | verified clean | vs rules |
|---|---|---|---|---|
| k8s deprecation guide | clean prose | 86 | **83 (96.5%)** | rules got 44 |
| pydantic v1→v2 migration | **messy** prose+code+tables | 178 | **145 (81.5%)** → **174 (97.8%) after repair** | rules under-read it |

- The two-tier keywords work: `from_fact` (code-derived, always grounded) + `associative`
  (LLM, the searchable "could-be" phrases, e.g. `assuredConcurrencyShares renamed`).
- On messy prose the LLM paraphrases quotes more → the anchor **drops** them (safe failure);
  `repair.py` then re-grounds ~all of them to real source lines. No unverifiable fact reaches the bank.
- **The count lies; reading is the verdict** — the raw pydantic number (58%) hid ~51 good facts
  behind two checker bugs, found only by reading the rejects.

## Not done yet (the 🚧)
- **~10% sibling-snap.** `repair.py` can snap to a *token-adjacent* source line about a neighbouring
  change. Fix: require the snap to share a *distinctive* token from `old`/`truth`, not just any.
- **Landmine-gate.** Nothing yet checks "does this fact actually beat the bare model" (the numpy-2.0
  lesson — 5/6 were already known). That's the real precision filter, still unbuilt.
- **Verbatim grounding proves REAL, not CORRECT or CURRENT.** Confirmed by the 2.0 appsec run: even with
  this LLM-first + verbatim-grounded pipeline, a MANDATORY adversarial correctness audit (a second pass,
  web-checking every library/API/version claim) still found ~3.8% of facts wrong or stale — see
  `EXTRACTOR-2.0.md` §5. `check.py`'s verbatim-quote anchor above is triage, not a correctness verdict;
  a currency + correctness audit should run before any bank ships.
- **Wiring to the bank — DONE for the baked experts.** The adapter path (bank → index schema →
  `bake_index.py`) is wired and proven: GitChameleon and Security & Networking are baked and benchmarked
  (see `../ARCHITECTURES.md`). Not every expert is baked yet (Web, AI-ML pending; appsec is SHIPPED —
  baked ×3 sizes × both thinking editions, published — see `EXTRACTOR-2.0.md`).
- **Scale + completeness signal.** One source at a time; no density/coverage meter (problem #4).

## Files
- `extract.py` — LLM extraction (function-calling + derive-in-code)
- `repair.py` — quote re-grounding (checker pass, no LLM)
- `check.py` — raw checker (verbatim-quote anchor)
- `run.py` — driver: extract → repair → check
