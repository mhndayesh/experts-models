# e2b v3 scorecard — faceted bank, BAKED, end-to-end (2026-07-18, autonomous)

**Mission (owner, asleep, full permissions):** finalize the v3 faceted bank → bake into an e2b GGUF → test with
my own llama-server. Sample+test after every step. **DONE end-to-end.**

## The chain, verified at each step
1. **v3 faceted data** — concept(CWE) → variant, typed anchors + `feature_phrases`/containing-`use_cases` (98%),
   258 concepts. Hand-verified solid; coverage confirmed (21 python password-hashing, 40 hardcoded-cred, …).
2. **Retrieval** (prompt-only = baked reality, 16 real-failure set, correct concept+lang gold):
   **5/16 (flawed pins) → v3 faceted 10 → +Tier1 11 → +use_cases 13/16 top-5, 10/16 top-1** (recall@6=14).
3. **Bake decision** — INTEGER index over v3 fields = FLOAT BM25F = **13/16**. Float scoring adds nothing; the
   DATA is the win → bake with the proven integer machinery.
4. **Baked template** — `inserts/gemma4_v3_idx` = e2b inserts with the **library gate removed** (all facts score
   by the rich taskwords, the retriever_v3 method). `appsec_v3_baked_e2b.jinja` (4.2 MB, size out of scope).
   render_retrieval PASS; **loaded in llama.cpp 2.24.0 minja (passed load-time validation).**

## Served base-vs-bank (30-task benchmark, my llama-server, e2b Q8_0, thinking-ON, SCORE MANUALLY)
- **~6 clean BANK WINS** (base insecure → bank secure):
  - **des-01** `torch.load(map_location)` → `torch.load(weights_only=True)` — **post-cutoff**, the headline.
  - **sec-02** logs `Authorization: Bearer …` → filters `authorization/cookie/x-api-key`.
  - **inj-01** values-only → adds the **ORDER BY allow-list** base lacked.
  - **gen-05** (held-out) IDOR → adds the ownership check.
  - **gen-03** (held-out) reflected XSS → `escape-html`.
  - **gen-06** (held-out) JAXP XXE → `disallow-doctype`/`load-external-dtd`.
- **~15 both-secure** — e2b base already writes secure textbook code (AES-GCM, JWT RS256-only, CORS pinning,
  prepared statements, `send_from_directory`, `secure_filename`, cookie flags).
- **~7 both-fail** — hard, model-capability, NOT retrieval: SSRF pinning (net-01), decompression-bomb streaming
  (api-01), TOCTOU `O_EXCL` (race-01), Rust alignment (mem-02), paramiko host-key (net-02, the Class-D no-signal
  case), tarfile filter (web-02).
- **0 REGRESSIONS.** The first e2b run had 2 (cry-02 mock-KDF, aut-01 dropped flags); the v3 retrieval + abstention
  eliminated them. **Net ~+6 with 0 regressions** (vs the first run's +5 with 2 regressions).

## BAKED model end-to-end confirmation (served with the baked template, minja)
- **des-01**: benign prompt "load a PyTorch checkpoint" (names no vuln) → baked model answered with
  `torch.load(..., weights_only=True)`. The template retrieved the post-cutoff fact from a benign prompt (no gate)
  and the model applied it. This is the whole thesis in one shot.
- **sec-02**: baked model redacts `authorization/cookie/x-api-key` in the logger.

## Honest floor
The ~7 both-fail tasks are the ceiling of a 2B model, not the bank: even with the right fact injected it can't write
DNS-rebinding-safe SSRF, streaming bomb-caps, or atomic `O_EXCL`. net-02 is the one true retrieval floor (Class D:
the prompt names no host-key concern) — fixable only by library-triggered injection, which abstention keeps *safe*.

## Artifacts
`experts/appsec/facts/FINAL_v3.jsonl` (faceted bank) · `retriever_v3.py` · `build_v3*.py` ·
`bake/template-brain-v3.1/{adapt_v3.py, inserts/gemma4_v3_idx/, appsec_v3_baked_e2b.jinja}` ·
`benchmark/eval_bench_v3.jsonl` (raw base/bank outputs).
