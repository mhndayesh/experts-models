# FactBank — shipping blueprint

**One GGUF. Three delivery routes. No route bricks.**

A stock gemma-4-12B QAT GGUF whose `tokenizer.chat_template` carries a fact bank, an
inverted-index retriever, and a forged native-tool delivery lane. Weights untouched
(667 tensors byte-identical); two metadata keys rewritten.

Evidence: FINDINGS F-041…F-059 · RESULTS §12–§14 · kit
`template-brain-v3.1/template-brain-v3.1/`
Supersedes the old two-edition split (`archive/docs/FACTBANK-EDITIONS.md`) — that document
assumed LM Studio's ~1 MB ceiling was unbeatable. **It is not** (F-059).

---

## 1. The three routes

| route | how the template arrives | bank | user does |
|---|---|---|---|
| **LM Studio Hub** | `model.yaml` → `llm.load.promptTemplate` | **big** (multi-MB, no cap) | Download → Run |
| **llama.cpp / llama-server** | embedded in the GGUF, or `--chat-template-file` | **big** | run the `.bat` |
| **raw GGUF, dropped in by hand** | embedded (must be ≤ **980,000 B = 957 KiB**) | **safe/lite** | nothing |

The third row is the safety net, and it is why the embedded template must stay under the
cap: anyone who bypasses the Hub still gets a **working smaller FactBank** instead of the
48-character sentinel brick.

## 2. The ceiling, and why it no longer constrains us (F-053 → F-059)

LM Studio's **GGUF-metadata reader** silently replaces an over-long
`tokenizer.chat_template` with:

```
[LM Studio Patch - String too long; didn't read]
```

48 characters, no `{{ messages }}`. The model loads "successfully" and answers garbage.
No error, anywhere. Bracket: **994,885 bytes works, 1.51 MB bricks.**

**But that cap belongs to one code path only.** LM Studio's *load-config* path
(`llm.load.promptTemplate`) has **no size limit**: it writes the string to a temp file and
passes it to llama.cpp with `--chat-template-file` — and llama.cpp never had a limit (cap
1 GiB, errors loudly). Proven live:

| gate | 1.5 MB | 2.0 MB |
|---|---|---|
| bytes handed to the engine | **1,536,014** | **2,048,014** |
| not the sentinel · >1 MiB · canary · SHA-256 match | PASS | PASS |

Functional on the same load: matched question → **390 prompt tokens** with the
melt→unpivot fact injected; control → **112 tokens**, no facts.

And the Hub carries it: `lms push` of a 1.95 MB `model.yaml` was **accepted**
(1.53 MB uploaded, incompressible worst case), and `lms clone` returned the template
**intact at 2,047,990 bytes**. The real FactBank template gzips to **0.22 MB**, so
production sits far inside the limit.

## 3. The production `model.yaml`

**LOAD-ONLY.** Do not add `llm.prediction.promptTemplate` (see §5).

```yaml
model: <your-handle>/factbank-pythondata
base:
  - key: <your-hf-user>/<your-gguf-repo>
    sources:
      - type: huggingface
        user: <your-hf-user>
        repo: <Your-GGUF-Repo>
config:
  load:
    fields:
      - key: llm.load.promptTemplate
        value:
          type: jinja
          jinjaPromptTemplate:
            template: |
              <THE FULL BIG-BANK TEMPLATE, indented 14 spaces>
metadataOverrides:            # MANDATORY - see §5
  domain: llm
  architectures: [gemma4]
  compatibilityTypes: [gguf]
  paramsStrings: ["12B"]
  minMemoryUsageBytes: 7400000000
  contextLengths: [262144]
  vision: true
  reasoning: true
  trainedForToolUse: true
```

Publish with `lms push` from the folder containing it. **The GGUF does not go to the
Hub** — the manifest points at Hugging Face for the weights. The Hub artifact is a couple
of MB of YAML, nothing more.

## 4. The llama.cpp route

Reproduce LM Studio's own spawn line (captured live), minus the ceiling:

```bat
llama-server.exe --model <factbank.gguf> --jinja ^
  --host 127.0.0.1 --port 1234 --ctx-size 16384 --n-gpu-layers 999999 ^
  --batch-size 2048 --ubatch-size 512 --threads 10 --parallel 4 ^
  --cache-type-k f16 --cache-type-v f16 --flash-attn auto --mlock
```

The template travels inside the GGUF, so `--jinja` alone suffices. To serve a bank bigger
than the embedded one, add `--chat-template-file factbank-max.jinja`.

## 5. Three traps that silently defeat the Hub route

1. **LOAD-ONLY.** With `llm.prediction.promptTemplate` *also* set, the model loads and the
   oversized template **is** applied — but every chat completion returns **HTTP 500**.
2. **`metadataOverrides` is mandatory.** Without it LM Studio refuses the manifest and the
   model **never appears in `lms ls`** — no error, no toast. The reason is only visible in
   `.internal/model-index-cache.json`:
   `{"type":"virtualModelBadManifest","error":"Cannot read properties of undefined (reading 'paramsStrings')"}`
3. **The manifest is cached.** After editing `model.yaml`, a reload can silently reuse the
   previous template (a 2 MB edit reloaded as the old 1.5 MB one). Force a rescan and
   **re-verify the applied bytes** every time.

Also: a YAML block scalar (`|`) appends exactly one trailing newline, so the applied
template is `published + "\n"`. Compare **content**, not raw bytes.

## 6. Gates — run all of these before publishing

| gate | what it catches |
|---|---|
| `parity.py` | the template must retrieve identically in jinja2 and the real engine (F-050). 22/22 |
| **size guard** (`bake_index.py --route rawgguf`, 980,000 B = 957 KiB) | **OPT-IN, not a default** — the wall is dead on every other route (F-059). Keeps the **embedded** template under LM Studio's raw-GGUF cap so that route degrades instead of bricking |
| **metadata-cache assert** | after LM Studio indexes the GGUF, `gguf-metadata-cache.json`'s `chatTemplate` length must equal what was baked (catches the sentinel) |
| **`lmstudio_yaml_test/check_override.py`** | after a Hub load: the applied template is >1 MiB, not the sentinel, carries the canary, and SHA-matches. Reads the **real process cmdline** — a cache cannot fool it |
| `lint.py` + `scenarios_pydata/` | 8/8. (`scenarios_gemma4/` is the *niche* model's set — not interchangeable) |

**`llm.load.promptTemplate` is marked EXPERIMENTAL in the SDK.** It can change between LM
Studio versions. `check_override.py` is therefore a **permanent regression gate**, not a
one-off.

## 7. What ships today, and what does not

**Ready now:** the **1,911-fact** model — gold retrieval **12/12**, controls 0/10, lint
8/8, parity 22/22, live 10/10 clean, TTFT 0.18–1.91 s, 950 KB embedded template (under the
cap, so every route works).

**Not ready:** a genuinely *bigger* bank. Bytes and milliseconds are no longer the limit —
a 21k-fact / 5 MB template renders a matched question in **218 ms, faster than the 950 KB
build** (F-055). What breaks is **recall**: gold decays **12/12 → 11/12 → 9/12** as the
bank grows to 21k, while controls stay clean (F-056). The bank does not get noisy, it gets
**unfocused**.

So growing the bank is a **retrieval-calibration** job, not a capacity job. The constants
to fix — `DF_CAP=40`, the IDF buckets, `FB_MAX=5`, the 48 gate triggers per library — were
all calibrated at ~2k facts, and Doc2Token expansions cover only the 388 curated facts. All
of it is offline, free, and measurable. **The gold set (12 questions) must grow first; it
cannot honestly calibrate a 21k bank.**
