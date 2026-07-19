# Appsec-Integration Benchmark

A **hard, complexity-focused** benchmark for the appsec expert. Hardness comes from **multi-library
integration + subtle insecure-by-default landmines**, NOT from long tasks — every task is a short function or
endpoint. Built alongside the appsec bank and cross-checked against it. (The SHIPPED bank is the v3 faceted
`../facts/FINAL_v3.jsonl` — 258 concepts (254 CWE) → 3,984 variants; `../facts/FINAL.jsonl` was the earlier
flat served run.)

## What it tests
Each task is a realistic coding request a developer would actually make. The *idiomatic / obvious* answer is
insecure-by-default; a passing answer must avoid the landmine(s) while still doing the job. Tasks draw from:
- **the bank itself** (`source: bank*`) — every task's CWE maps to real bank facts (coverage: **24/24**),
- **public benchmarks / standards** — CWE Top 25, OWASP Top 10 / ASVS, Purple-Llama CyberSecEval &
  SecurityEval-style insecure-coding tasks (`source: cwe-top25 | owasp | cyberseceval-style`),
- **post-cutoff currency cases** (`source: post-cutoff`) — the bank's proven edge: facts a strong base model
  can't have learned (e.g. `torch.load` `weights_only` default in PyTorch 2.6; lxml 5.0 XXE default; tarfile
  `filter='data'` / PEP 706).

## Coverage (30 tasks = 24 core + 6 held-out)
All 10 doors. Polyglot: python/javascript/c/rust/php/java. 3 post-cutoff currency tasks, 3 multi-landmine
tasks. **`held_out: true`** marks 6 general tasks from known benchmarks (PHP SQLi, Spring path traversal,
Express XSS, Flask upload, FastAPI IDOR, Java JAXP XXE) that may be OUTSIDE the bank's specific coverage — a
control for "does the bank help only where it knows, and stay out of the way elsewhere." Every core task's CWE
maps to real bank facts (coverage 24/24).

## Schema (`appsec_bench.jsonl`, one task per line)
```
id, title, category(door), lang, libraries[], difficulty, source,
task            : the prompt handed to the model
landmines[]     : {cwe, trap, insecure_default, secure_requirement, currency}
rubric          : {must[], must_not[]}   # OBJECTIVE grading
why_hard        : the complexity / integration reason
```

## Grading (objective)
A model's answer to a task **PASSES** iff **every `rubric.must` pattern is present** AND **no `rubric.must_not`
pattern is present**. `must` = the real fix; `must_not` = the insecure default. Grading is designed to be
checkable by inspection (and largely by pattern-match), but **final scoring is by hand-read** (the project
rule — automated scorers have been wrong in both directions).

## How to run (base vs bank)
Serve the base model on your **own llama-server** (NOT LM Studio — it drops `chat_template_kwargs`), gemma
sampling (temp 1.0 / top_k 64 / top_p 0.95 / min_p 0.01), thinking-ON. For each task:
1. **BASE**: send `task` directly → grade the answer against the rubric.
2. **BANK**: HyDE-retrieve from the shipped bank (`FINAL_v3.jsonl`; `FINAL.jsonl` for the earlier flat run)
   using `task` + the base draft, inject the retrieved facts
   authority-framed, re-ask → grade.
Report **SECURE@1** base vs bank per task and per category. Reuse the harness in
`../../../appsec_servetest.py` (swap its `TESTS` for these tasks and its scan for the rubric checks).

## Provenance
`build_bench.py` is the authoritative source (tasks as Python dicts → JSONL). The benchmark was put through
**two rounds** of adversarial correctness audit (one Sonnet agent per task, web-verifying every currency/library
claim and checking each rubric is objective and each landmine real): **0 broken across both rounds**, 17 + 12
precision fixes all folded in. Full trail in `AUDIT.md`.
