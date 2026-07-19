# Shipping — one GGUF, three routes, none of them brick

Everything here was proven live on 2026-07-14. The traps in §4 each *silently* defeat the
whole thing, which is why they are stated before the recipe.

---

## 1. The three routes

| route | how the template arrives | bank the user gets | what the user does |
|---|---|---|---|
| **LM Studio Hub** | `model.yaml` → `llm.load.promptTemplate` | **big** (multi-MB, no cap) | Download → Run |
| **llama.cpp / llama-server** | embedded in the GGUF, or `--chat-template-file` | **big** | run the `.bat` |
| **raw GGUF, moved in by hand** | embedded (must stay ≤ **980,000 B = 957 KiB**) | **safe/lite** | nothing |

**The third row is the safety net, and it is why the embedded template must stay under the
cap.** Anyone who bypasses the Hub still gets a *working, smaller* FactBank instead of a
48-character brick that gets blamed on the model.

You do **not** need two GGUFs. The weights are one file; the big bank is just text,
delivered alongside.

## 2. The ceiling you are working around

LM Studio's **GGUF-metadata reader** silently replaces an over-long
`tokenizer.chat_template` with:

```
[LM Studio Patch - String too long; didn't read]
```

48 characters, no `{{ messages }}`. The model loads "successfully" and answers garbage; no
error appears anywhere. **Works at 994,885 bytes; bricks by 1.51 MB.**

That cap lives in **one code path only**. LM Studio's *load-config* path has no size limit:
it writes the template to a temp file and hands it to llama.cpp with
`--chat-template-file` — and llama.cpp never had a limit (cap 1 GiB, and it errors
*loudly*). Proven at **1.5 MB and 2.0 MB**, with the Hub accepting and returning the
manifest intact.

## 3. The production `model.yaml`

**LOAD-ONLY.** Read §4 before changing anything here.

```yaml
model: <your-hub-handle>/factbank-pythondata
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
              <THE FULL BIG-BANK TEMPLATE, every line indented 14 spaces>
metadataOverrides:          # MANDATORY — without this the model never appears at all
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

Publish with `lms push` from the folder containing it.

**The GGUF does not go to the Hub** — the manifest points at Hugging Face for the weights.
The Hub artifact is a couple of MB of YAML and nothing else. (A 1.95 MB manifest was
accepted; the real template gzips to 0.22 MB, so there is room.)

## 4. The three traps

Each of these fails **silently**. Each cost real time to find.

**1. LOAD-ONLY — do not also set `llm.prediction.promptTemplate`.**
With both set, the model loads *and the oversized template is correctly applied* — but
**every chat completion returns HTTP 500**. Load-only works end to end.

**2. `metadataOverrides` is mandatory.**
Without it, LM Studio refuses the manifest and the model **never appears in `lms ls`** — no
error, no toast, nothing. The reason is visible only in
`~/.lmstudio/.internal/model-index-cache.json`:

```json
{"type":"virtualModelBadManifest",
 "error":"Cannot read properties of undefined (reading 'paramsStrings')"}
```

**3. The manifest is cached.**
After editing `model.yaml`, a reload can silently reuse the *previous* template — a 2 MB
edit once reloaded as the old 1.5 MB one. Force a rescan and **re-verify the applied
bytes**. Never trust a reload to have picked up an edit.

Minor but real: a YAML block scalar (`|`) appends exactly one trailing newline, so the
applied template is `published + "\n"`. Compare **content**, not raw bytes, or your
integrity check will cry wolf over one byte.

## 5. The llama.cpp route

Reproduce LM Studio's own spawn line (captured from the live process), minus the ceiling:

```bat
llama-server.exe --model <factbank.gguf> --jinja ^
  --host 127.0.0.1 --port 1234 --ctx-size 16384 --n-gpu-layers 999999 ^
  --batch-size 2048 --ubatch-size 512 --threads 10 --parallel 4 ^
  --cache-type-k f16 --cache-type-v f16 --flash-attn auto --mlock
```

The template travels inside the GGUF, so `--jinja` alone is enough. To serve a bank larger
than the embedded one, add `--chat-template-file factbank-max.jinja`.

## 6. Gates — all of these, before publishing

| gate | what it catches |
|---|---|
| `parity.py` | the template must retrieve identically in jinja2 and the real engine. Offline tests render with jinja2; the shipped engine is llama.cpp's, and they are **not** the same language. **22/22 or do not bake.** |
| **size guard** (`bake_index.py --route rawgguf`, 980,000 B = 957 KiB) | **OPT-IN, not a default** (F-059: the wall is dead on every other route). Keeps the *embedded* template under LM Studio's raw-GGUF cap so that route degrades instead of bricking. Bakes over the cap still print a loud warning on every route, because F-053's failure is SILENT |
| **metadata-cache assert** | after LM Studio indexes the GGUF, `gguf-metadata-cache.json`'s `chatTemplate` length must equal what was baked — this catches the sentinel, free and without a GPU |
| **`check_override.py`** | after a Hub load: applied template is >1 MiB, not the sentinel, carries the canary, SHA-matches. It reads the **real process command line**, so a cached config cannot fool it |
| `lint.py` + `scenarios_pydata/` | 8/8. (`scenarios_gemma4/` belongs to the *niche* model — the two sets are **not** interchangeable) |

## 7. One standing risk

**`llm.load.promptTemplate` is marked EXPERIMENTAL in the LM Studio SDK.** It works today.
It can change between versions. Anything you ship on it needs `check_override.py` as a
**permanent regression gate**, not a one-time check.

If LM Studio ever closes this path, nothing is lost: the GGUF still works everywhere with
its embedded bank, and llama.cpp users still get the big one.
