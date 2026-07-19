# Model settings — Security & Networking bake + test (2B / 12B / 26B)

Every setting used in the base-vs-bank runs, so the numbers are reproducible. **Dates:** 26b 2026-07-16;
e2b + 12b 2026-07-16/17 (native sampling, 6-parallel). Results: [BAKE-TEST-CURVE-3MODEL.md](BAKE-TEST-CURVE-3MODEL.md).

## Models — three base/baked pairs
Each pair shares base weights; the baked GGUF carries the 114-fact bank + inverted-index retriever in its
chat-template (~118 KB). Prompts are identical within a pair — the baked template injects facts in-engine.

| size | quant | base GGUF (control) | baked GGUF (treatment) | GGUF size |
|---|---|---|---|---|
| **26b** (A4B MoE) | Q4_0 QAT | `lmstudio-community/gemma-4-26B-A4B-it-QAT-GGUF/…Q4_0.gguf` | `factbank/gemma-4-26B-A4B-netsec-expert-GGUF/…Q4_0.gguf` | 14.4 GB |
| **12b** | Q4_0 QAT | `lmstudio-community/gemma-4-12B-it-QAT-GGUF/…Q4_0.gguf` | `factbank/gemma-4-12B-netsec-expert-GGUF/…Q4_0.gguf` | 6.98 GB |
| **e2b** (~2B edge) | Q4_K_M | `lmstudio-community/gemma-4-E2B-it-GGUF/…Q4_K_M.gguf` | `factbank/gemma-4-E2B-netsec-expert-GGUF/…Q4_K_M.gguf` | 3.43 GB |

> Quants differ by what's on disk (e2b is Q4_K_M, 12b/26b are Q4_0 QAT). Base-vs-baked **within each size
> shares the quant**, which is what the comparison requires. e2b needed template re-anchoring (different
> revision); 12b/26b did not — see METHODOLOGY §2 and `E2B-BAKE-NOTES.md`.

## Serving — llama.cpp `llama-server` (via `v2/bake/serve_factbank.ps1`), 6 parallel slots
- backend: `llama.cpp-win-x86_64-amd-rocm-avx2-2.24.0` (ROCm, AMD **RX 7900 XTX, 24 GB**)
- `-ngl 99` — all layers on GPU
- **`--parallel 6`** (launcher `-Parallel 6`) — 6 concurrent request slots (continuous batching)
- **`--ctx-size 49152`** — the **total**, split across slots → **8192 per slot** (`Ctx / Parallel`). Size as
  `parallel × per-request context`.
- `--jinja` — **required**: uses the GGUF's embedded chat-template (that's where retrieval lives). Without it the bank never fires.
- `--host 127.0.0.1 --port 8080`
- **NOT** LM Studio raw-load: it honors none of the `chat_template_kwargs`, so thinking-ON can't reach the
  template there (and F-053 truncates >980 KB templates to a 48-char sentinel — our 118 KB would fit, but the
  kwargs issue alone rules it out). `llama-server` honors `enable_thinking`.
- One model at a time; VRAM freed (process killed + verified: no `llama-server` process, port free) between
  every base/baked swap and after the final run (Rule 3). VRAM headroom: e2b/12b baked + 6-slot KV fit well
  inside 24 GB (peaks ~14 GB); the user's LM Studio model was left untouched throughout.

## Generation settings (FINAL — Gemma-native)
Official Gemma 3 inference config ([Google/Unsloth](https://unsloth.ai/docs/models/tutorials/gemma-3-how-to-run-and-fine-tune)):
| param | value | why |
|---|---|---|
| `temperature` | **1.0** | Gemma's intended operating point (esp. QAT) |
| `top_k` | **64** | Gemma default |
| `top_p` | **0.95** | Gemma default |
| `min_p` | **0.01** | probability floor — **this is what breaks repetition loops** |
| `repetition_penalty` | 1.0 | disabled (Gemma recommendation) |
| `max_tokens` | **6000** (parallel) / 12288 (sequential) | thinking-ON shares this budget (reasoning THEN answer). The e2b/12b 6-slot runs used **6000** (per-slot ctx 8192 = prompt + answer headroom); the earlier sequential 26b run used 12288. All runs came back `finish_reason=stop` with **0 empties** |
| `chat_template_kwargs.enable_thinking` | **true** | thinking-ON (the run under test); reaches the template only via `llama-server`, never LM Studio |
| `--workers` (harness) / `--parallel` (server) | **6** | 6 concurrent requests via continuous batching; `executor.map` keeps the transcript question-ordered |

**System prompt:** `AUTHORITY_SYS` — the documented "authority framing" that stops a reasoning model
reverting an injected fact to its trained prior: *"A documentation lookup provides VERIFIED FACTS … they
are ABSOLUTELY CORRECT and SUPERSEDE your training … if a fact contradicts your instinct, your instinct is
stale training and the FACT wins."* (see `test_secnet.py`).

## The sampling bug we fixed (why the first hard run had empty answers)
The first hard run used **`temperature: 0.6` with NO top_k/top_p/min_p** — nothing else set. On hard
multi-step tasks that collapsed into a **repetition loop**: the model repeated one uncertain token
(e.g. *"It's `EVP_PKEY_get_param_asc`… no."* ×20), ran the reasoning channel to `finish_reason=length`, and
committed an **empty answer**. It was **NOT** a budget or context limit — h04 looped identically at 12288
tokens. Root cause = sampling. Switching to Gemma-native sampling (temp 1.0 + top_k 64 + top_p 0.95 +
**min_p 0.01**) removed **all** empties on the re-run (0/18 empty vs 3/54 before). The `min_p` floor is the
key: it prevents the distribution from collapsing onto the single repeated token.

**Rule of thumb going forward:** always send the model's *native* sampling set, not a bare low temperature.
For gemma-4: `temp 1.0, top_k 64, top_p 0.95, min_p 0.01`. Never send `temperature` alone.

## Extraction settings (how the bank was made) — for completeness
- DeepSeek `deepseek-v4-flash`, thinking OFF (`"thinking":{"type":"disabled"}`), function-calling (no json_schema).
- Pipeline: FIND migration guide → WebFetch → extract → repair (re-ground quotes) → check. ~4¢/library.
- Key: `C:\Users\mhnda\OneDrive\Desktop\api\deepseek.txt` (read inline; never written into the repo).

## Bake command
```
cd v2/bake/template-brain-v3.1
python adapt_secnet.py                       # 114 facts -> secnet_bank.jsonl + secnet_taskwords.json
python bake_index.py --facts secnet_bank.jsonl --controls controls_repo.txt \
  --taskwords secnet_taskwords.json --out secnet_baked_gemma4.jinja \
  --src-gguf <clean-26b.gguf> --dst-gguf <netsec-expert.gguf>
# -> 114 facts, 2317 index terms, 7 libraries, 118 KB template
```

## Test command (final)
```
cd v2/extractor/experts/security-networking
python test_secnet.py --tag <tag> --port 8080 --think --authority \
  --qfile test_questions_hard.jsonl
# defaults now: temp 1.0, top_k 64, top_p 0.95, min_p 0.01, max_tokens 12288
```
