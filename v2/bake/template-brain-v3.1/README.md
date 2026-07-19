> # ⚠⚠ SUPERSEDED — GENERATION 1 (the linear scanner). DO NOT FOLLOW THIS README. ⚠⚠
>
> This file describes the **gen-1 linear scanner** (`bake_template_v3.py`), which was replaced.
> **The current baker is [`bake_index.py`](bake_index.py) + [`inserts/gemma4_idx/`](inserts/gemma4_idx/)**
> (an **inverted index**, not a linear scan) — that is what baked the shipped GitChameleon and
> Security & Networking GGUFs. This file is kept only for the §Anchoring checklist and as historical record.
>
> **For current truth, read the serving docs:** [`../../serving/README.md`](../../serving/README.md),
> then [`../../serving/OPERATIONS.md`](../../serving/OPERATIONS.md) for what to run and
> [`../../serving/LIMITS.md`](../../serving/LIMITS.md) before promising anything. Architecture of the
> three distinct bake systems: [`../../ARCHITECTURES.md`](../../ARCHITECTURES.md).
>
> What below is now WRONG:
> - **"hard cap 500 facts"** — the shipped bank is **1,911**, and 8,096 clean mined facts exist.
> - **the pipeline (`bake_template_v3.py`)** — superseded by **`bake_index.py`** + `inserts/gemma4_idx/`
>   (inverted index). The linear scanner was the ceiling that RESULTS §11 caught: it answered
>   with a *dead* `melt()` because the right fact was never retrieved.
> - **"the wall is one-time PARSE cost and raw size"** — RETIRED (F-055). 21k facts / 5 MB
>   renders a matched question in **218 ms, faster than the 950 KB build**; cost per fact *falls* 8×.
> - **"jinja2 passing does not guarantee minja"** — **minja no longer exists** (F-054; llama.cpp
>   PR #18462 replaced it). LM Studio renders in llama.cpp. Use `parity.py`.
> - **the 957 KB cap is not a default** — the ~1 MB wall is dead (F-059); it survives only as
>   `bake_index.py --route rawgguf`.
>
> Missing entirely: the three MANDATORY gates (`parity.py`, the size guard, the metadata-cache
> assert), `dedupe_mine.py` (the mine is **66% junk** — F-064), and the rule that **all scoring
> is MANUAL** (F-065).
>
> Kept only for the §Anchoring checklist and as the historical record.

# template-brain v3

## SCOPE, read first (audit points 3 and 21)
This lane is the small-bank, in-file tier: hard cap 500 facts, keyword
matching, quality target BETWEEN bare model and the sealed loop. It is
NOT the 10k-100k product; that stays pouch + factbank serve (HybridBank:
embeddings, BM25, scores, version filters, real top-k). "Works
everywhere" means precisely: every path that renders the embedded
chat template with tool-aware Jinja. Excluded by nature: raw-completion
mode, clients that override or ignore templates, non-Jinja engines.

## Lanes
- Lane 2 (universal): final user turn matched against the bank, hits
  injected as natural text inside that user turn. Single call. Fires
  only when factbank_search was NOT passed in tools.
- Lane 1 (upgrade): model writes the slip; a tools-capable client
  bounces; the paired tool_response is rendered as the matched facts,
  keyed by that exchange's user text + slip. Selected only when
  factbank_search IS among the passed tools (by name, audit point 12).

## Files
inserts/reference/   top.jinja, fb_preloop, fb_sys, fb_user, fb_hook, fb_toolmsg
enrich.py            raw bank -> enriched (keywords, culling, review)
controls_default.txt culling corpus (extend with your 18 controls)
bake_template_v3.py  splice + guards; --template-only runs today
lint.py + scenarios/ 12 rendered gates, all passing under jinja2
harness.py           TEST bounce controller + --no-tools Lane 2 mode
exam.py              arms x 18 x 3 reps -> transcripts
check_transcripts.py mechanical transcript gate
test_family/         toy base for lint ONLY, not a real family
smoke_facts.jsonl    5 facts in the real project schema

## Pipeline
1. python enrich.py facts_v2.jsonl bank_enriched.jsonl \
       --controls controls_default.txt [--taskwords tw.json]
   -> READ the review lines (CULLED / UNREACHABLE / unreviewed)
2. python bake_template_v3.py --base family_bases/<fam>.jinja \
       --source-template <extracted>.jinja --enriched bank_enriched.jsonl \
       --raw facts_v2.jsonl --family <fam> --out baked_template.jinja
3. python lint.py baked_template.jinja
4. on-device gates (below), then exam.py

## Anchoring checklist (audit point 16), once per model family
1. Extract the CURRENT template from the exact GGUF you ship; save it
   untouched as <fam>.source.jinja
2. Copy it to family_bases/<fam>.jinja and insert ONLY the five anchors:
   {#FB_PRELOOP#} before the message loop; {#FB_SYS#} where system text
   renders; {#FB_USER#} in the user branch after content; {#FB_HOOK#}
   inside the assistant per-tool-call loop; {#FB_TOOLMSG#} in the tool
   branch replacing content rendering
3. bake verifies base minus anchors == source, byte-exact (point 20)
4. If the family's loop variables are not `msg`/`tc`/`loop`, copy
   inserts/reference/ to inserts/<fam>/ and rename variables THERE,
   never in the base
5. Rerun lint with a family-shaped scenario before any device test

## Division of labor (audit points 1, 22)
- This kit ships template + enrich + gates, runnable end to end in
  --template-only mode (paste into LM Studio's template override to
  test without any GGUF write)
- The repo side wires write_baked() to the project's proven GGUF
  writer (package/factbank/bake.py ~line 94, real 4-arg signature)
  and runs the on-device gates below

## On-device gates (cannot run off-device by definition)
G1 canary: `lms log stream` shows [fb1]; the branch wording shows which
   lane rendered ("Rule:" vs "Note:")
G2 Lane 2 pair in the LM Studio CHAT window: matching question injects,
   haiku does not; reply free of tool markup
G3 Lane 1 pair via harness.py on :1234 AND llama-server --jinja :8080
G4 mixed tools: dummy second tool passes through raw
G5 think -> call -> think -> answer renders clean
G6 exam.py, then check_transcripts.py, then v2 scorer on transcripts
G7 scaling on-device: paste bench_out/tpl_<n>.jinja via LM Studio
   template override and llama-server --chat-template-file; measure
   time-to-first-token cold and warm at each size; the knee sets --cap

## Two-stage gate (v3.1)
Stage 1 scans ~one small trigger list per library (name + up to
--gate-n unique keywords, mistake-kind first); stage 2 deep-scans only
facts behind open tabs. Flat facts + `f.lib in ns.libs` keeps Jinja at
depth 2. bake prints GATE-SHADOWED for facts reachable only when their
library is named (the recall price, tunable via --gate-n).

## Benchmark (bench.py) and the cap
Local jinja2 curve (this kit's build box):
  facts   tpl_KB  parse_ms  render_ms  false_inj
    100     25       67       0.2         0
    500    102      227       1.0         0
   1000    199      434       1.7         0
   2000    398      792       3.5         0
   5000    997     2041       8.4         0
  10000   1994     3938      18.9         0
Reading: per-request render scales fine to 10k; the wall is one-time
PARSE cost and raw size. Whether engines compile once per load or per
request is the open device question -> G7. Synthetic facts use unique
keywords, so false_inj=0 is optimistic; rerun precision with a real
10k-vocabulary bank before trusting it. Raise --cap only after G7.

## Repo-side wiring (DONE 2026-07-13, all offline - no models touched)
- write_baked() WIRED in bake_template_v3.py: GGUFReader -> GGUFWriter ->
  copy_with_new_metadata (same proven path as package/factbank/bake.py,
  minus its F-040 template surgery), adds factbank.bank/factbank.version.
  test_write_baked.py = synthetic-GGUF smoke (template + keys + tensor
  bit-exact), PASSES.
- enrich.py adapted to the REAL bank schema: facts_v2.jsonl's `source` is
  the module name (URL lives in meta.url) and is used as the library;
  library names are exempt from the 3-char keyword floor (" uv ").
  94 facts -> bank_enriched_real.jsonl: 30 libraries, 0 UNREVIEWED,
  0 UNREACHABLE, 0 CULLED against controls_repo.txt (= the 12 defaults +
  the repo's 6 control prompts from sets.py = the 18 controls).
- family_bases/: qwen3 (source = template EMBEDDED IN Qwen3-0.6B-Q8_0.gguf,
  which DIFFERS from the HF tokenizer_config template - kept as
  qwen3.source.hf.jinja) and gemma4 (extracted from
  gemma-4-12B-it-QAT-Q4_0.gguf). Bases generated by make_base_qwen3.py /
  make_base_gemma4.py, byte-exact guard verified. Family inserts in
  inserts/qwen3/ and inserts/gemma4/ (fbns namespace - both sources define
  their own `ns`; top.jinja is a no-op in both - forcing enable_thinking
  would break the repo's think-off rule, F-018/F-035).
- baked_qwen3.jinja / baked_gemma4.jinja: real 94-fact bakes, linted green
  against scenarios_qwen3/ (6) and scenarios_gemma4/ (7; those run
  "lenient": true because the gemma SOURCE template needs lenient
  undefined). lint.py grew that per-scenario flag.
- Lane 1 client contract tightened in harness.py: the bounce sends
  content="" (qwen3's GGUF template renders message.content directly and
  cannot blank it) and the assistant echo always carries content.
- to_rescore.py: exam transcripts -> repo rescore.py jsonl
  (gemma-runner schema; --baseline-arm renames the bare-model arm, which
  rescore REQUIRES). Verified end-to-end against the real rescore.py.
- bench_out/tpl_10000.jinja generated (was missing); parse 2.3s local.
- BAKED GGUFs (out/, read-back verified: template LF-exact, all tensors
  bit-copied, factbank.bank=94 lines, factbank.version=0.3.0, and the
  template re-read FROM the GGUF renders + injects):
    .lmstudio\models\template-brain\qwen3-0.6b-factbank-94\
        template-brain-qwen3-0.6b-94facts-Q8_0.gguf        (768 MB)
    .lmstudio\models\template-brain\gemma-4-12b-qat-factbank-94\
        template-brain-gemma-4-12b-94facts-QAT-Q4_0.gguf   (6.5 GB)
  (baked in out/, MOVED into LM Studio's tree under publisher
  "template-brain" so they are unmistakable). Source GGUFs untouched.
- NEXT = on-device gates G1-G7 + exam.py: needs owner-loaded models and
  explicit run permission (repo hard rules 1-2).

## Known limitations (accepted, documented)
- Parallel factbank calls in ONE assistant turn: only the last is
  dressed; earlier ones pass through raw (s10 documents this)
- Trailing-inflection matches remain possible ("melted" hits " melt");
  leading and punctuation boundaries are fixed (s11, s12)
- jinja2 passing does not guarantee minja/LM Studio; G1-G5 exist for
  exactly that reason, with the replace-filter chain as the most
  engine-sensitive piece
