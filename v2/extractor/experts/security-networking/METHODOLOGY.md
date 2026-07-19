# Methodology — how the expert was built, baked, served, and tested

The full pipeline that turned seven migration guides into a measured lift on **three** models (2B/12B/26B),
reproducible end to end. Four stages: **extract → bake → serve → test**. All settings are in
[MODEL-SETTINGS.md](MODEL-SETTINGS.md); the cross-model result in
[BAKE-TEST-CURVE-3MODEL.md](BAKE-TEST-CURVE-3MODEL.md); per-model detail in the three `BAKE-TEST-REPORT*.md`.

---

## 1. Extract — migration guides → landmine facts

**The one law: source targeting decides everything.** Find the migration guide / changelog *first*; the rest
is mechanical. For each library we mined an official upgrade doc (see [`sources/`](sources/)), then ran the
DeepSeek structured extractor.

```bash
cd v2/extractor
DEEPSEEK_API_KEY=$(cat /c/Users/mhnda/OneDrive/Desktop/api/deepseek.txt | tr -d '\r\n ') \
  python run.py <source.md> <lib> <version>
# -> <lib>.facts.repaired.kept.jsonl
```

- **Model:** `deepseek-v4-flash`, thinking OFF, **function-calling** (no `json_schema`); `type`/`from_fact`
  derived in code, not asked of the model. **Endpoint-agnostic:** the extractor speaks the standard OpenAI
  API — point it at OpenAI or any compatible server with `LLM_BASE_URL` / `LLM_MODEL` + `LLM_API_KEY`
  (or `OPENAI_API_KEY`); the DeepSeek-only `thinking:disabled` flag is sent only when the endpoint is DeepSeek.
- **Anti-hallucination gate:** every fact carries a verbatim `quote`; `repair.py` re-grounds any paraphrased
  quote to a real source line. A fact whose quote can't be grounded is dropped.
- **Cost:** ~4¢/library — negligible. Extract deeper, don't optimize calls.
- **Output → [`facts/`](facts/):** 114 facts, 7 files, hand-checked (0 dup ids, 100% quote-grounded, 0 bad
  types). See [COVERAGE.md](COVERAGE.md).

> Security key handling: the DeepSeek key lives at `C:\Users\mhnda\OneDrive\Desktop\api\deepseek.txt` and is
> read inline at call time — **never written into the repo**.

## 2. Bake — facts → GGUF chat-template

The bank is delivered *inside* the GGUF's chat-template as an inverted-index retriever, so retrieval runs
**in-engine** (llama.cpp) with no external RAG service. The base weights are untouched.

```bash
cd v2/bake/template-brain-v3.1
python adapt_secnet.py                        # facts/*.jsonl -> secnet_bank.jsonl + secnet_taskwords.json
python bake_index.py \
  --facts secnet_bank.jsonl --controls controls_repo.txt --taskwords secnet_taskwords.json \
  --out secnet_baked_gemma4.jinja \
  --src-gguf <clean gemma-4-26B-A4B-it-QAT-Q4_0.gguf> \
  --dst-gguf <gemma-4-26B-A4B-netsec-expert-Q4_0.gguf>
```

- `adapt_secnet.py` maps the fact schema into the index schema; searchable phrases (`from_fact` +
  associative keywords) go to a taskwords side-channel so they don't pollute the injected text.
- `bake_index.py` builds the inverted index (term → `factid:weight`), a per-library **gate** (a named
  library wins; inferred only when nothing is named), and splices it into the template.
- **Result:** 114 facts, 2317 index terms, 7 libraries, **~118 KB template** — far under the LM Studio
  raw-load size wall (980 KB), so it fires everywhere.

### Baked into three models
| model | src GGUF (quant) | dst | re-anchoring? |
|---|---|---|---|
| **26b** | `gemma-4-26B-A4B-it-QAT-Q4_0` | `factbank/gemma-4-26B-A4B-netsec-expert-…Q4_0.gguf` (14.4 GB) | none — uses `gemma4.jinja` |
| **12b** | `gemma-4-12B-it-QAT-Q4_0` | `factbank/gemma-4-12B-netsec-expert-…Q4_0.gguf` (6.98 GB) | **none** — 12b template is byte-identical to `gemma4.source.jinja` |
| **e2b** | `gemma-4-E2B-it-Q4_K_M` | `factbank/gemma-4-E2B-netsec-expert-…Q4_K_M.gguf` (3.43 GB) | **yes** — e2b ships a different template revision; needed its own anchored base + one adapted insert (`fb_user`). See `../../../bake/template-brain-v3.1/E2B-BAKE-NOTES.md` |

Each bake is a full metadata-rewrite copy of the base (tensors untouched). **Always verify the template
renders offline** before shipping the GGUF: llama.cpp probes the template at load with synthetic inputs
(empty/system/tools/multimodal) and rejects the whole model if it throws — a quick jinja2 render across
those inputs (no GPU) catches it. The e2b bake was verified this way before the GGUF was written.

## 3. Serve — llama.cpp, not LM Studio raw-load (6 parallel slots)

```powershell
# -Parallel N gives N concurrent request slots; --ctx-size is split ACROSS slots (per-slot = Ctx / Parallel)
powershell -File v2/bake/serve_factbank.ps1 -Gguf <baked.gguf> -Port 8080 -Ngl 99 -Ctx 49152 -Parallel 6
```

- Runs `llama-server` with `--jinja` (uses the embedded template — **required**, that's where retrieval
  lives) on the ROCm backend, prepending the HIP/BLAS vendor DLLs to PATH (the launcher's whole reason to
  exist).
- **`-Parallel 6`** (added 2026-07-16) launches `llama-server --parallel 6` — 6 real concurrent slots via
  continuous batching, matched by the harness `--workers 6`. `--ctx-size` is the **total**, divided across
  slots (49152 / 6 = 8192 per slot), so size it as `parallel × per-request context`.
- **Never** LM Studio raw-load: it silently truncates >980 KB templates to a 48-char sentinel (F-053) and
  **honors none of the `chat_template_kwargs`** — so thinking-ON would never reach the template there. This
  is the reason the whole test runs on `llama-server`, which honors `enable_thinking`.
- This is our own test server on port 8080 — it never touches the user's LM Studio model. VRAM is freed
  (process killed + verified: no `llama-server` process, port free) between every base/baked swap and after
  the final run (Rule 3). Models are run **one at a time**, sequentially.

## 4. Test — base vs. bank, identical prompts

The baked template injects facts in-engine, so **the prompt is identical** for base and baked; the only
variable is whether the bank fires. Run the same harness against each served model.

```bash
cd v2/extractor/experts/security-networking
python test_secnet.py --tag <tag> --port 8080 --think --authority --workers 6 \
  --max-tokens 6000 --qfile <questions.jsonl>
# defaults: temp 1.0, top_k 64, top_p 0.95, min_p 0.01  (Gemma-native)
# --workers 6 fans out 6 concurrent requests (server must be launched with -Parallel 6);
#   executor.map preserves input order, so the transcript stays question-ordered.
# max_tokens 6000 chosen for the 6-slot runs (per-slot ctx 8192 = prompt + answer headroom);
#   the earlier sequential 26b run used 12288. Thinking-ON shares this budget with the answer.
```

- **Configuration under test:** thinking-ON + the **authority system prompt** (`AUTHORITY_SYS`) — the framing
  that stops a reasoning model reverting an injected fact to its trained prior ("VERIFIED FACTS … SUPERSEDE
  your training … the FACT wins").
- **Sampling:** Gemma-native (see [MODEL-SETTINGS.md](MODEL-SETTINGS.md) for why a bare low temperature
  caused repetition-loop empty answers).
- **Two test sets:**
  - `test_questions.jsonl` — 30 single-API landmines (easy).
  - `test_questions_hard.jsonl` — 18 silent-failure + multi-fact chains (hard).
  - `probe_vol.jsonl` — the gate-vocabulary probe (proves the volatility3 misses were gating, not knowledge).
- **Outputs → [`runs/`](runs/):** `<tag>_transcript.jsonl` (full prompt/reasoning/answer/triage) and
  `<tag>_score.txt` (auto-triage summary).

### Scoring — the auto-triage is a filter; **the verdict is hand-read**

The harness runs a substring pre-check (`expect_new` present, `avoid_old` absent) purely to **triage** which
answers to read closely. Every reported number in [BAKE-TEST-REPORT.md](BAKE-TEST-REPORT.md) is a **human
reading of the actual model output** — the project rule, and it repeatedly mattered here:

- The checker flags a *pass* when the model writes "don't use `RSA_sign()`, use `EVP_DigestSign()`" (old
  token appears in a contrast) — hand-read as a pass.
- The checker flags a *fail* when a valid alternative API is used (`EVP_PKEY_sign` vs `EVP_DigestSign`) —
  hand-read as a pass.
- **Empty committed answer = fail**, applied uniformly to both models regardless of what the hidden
  reasoning contained (a user receives the answer, not the reasoning).

Borderline calls were resolved **in the base model's favour**, making the reported bank advantage a lower
bound.
