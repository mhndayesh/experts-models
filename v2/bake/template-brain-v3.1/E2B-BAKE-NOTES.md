# e2b bake notes — why gemma-4-E2B is a *different* bake target

> Temp/progress note (2026-07-16). Categorizes **google/gemma-4-E2B-it** from the
> **chat-template-baking** aspect, so the family difference can be documented properly later.
> This is why the "e2b bake" was flagged **still-open** ("template differs — needs re-anchoring").

## 1. Model identity
- **google/gemma-4-E2B-it** — the community **`-it`** build (NOT the QAT line the 12b/26b use).
  E2B = Gemma-4's lightweight/edge class (~2B-effective). **Multimodal** (ships an `mmproj`:
  vision/audio). On disk: `lmstudio-community/gemma-4-E2B-it-GGUF/` → `gemma-4-E2B-it-Q4_K_M.gguf`,
  `gemma-4-E2B-it-Q8_0.gguf`, `mmproj-...-BF16.gguf`.
- Same **gemma-4 chat-template family** as 12b/26b, but a **different template revision**. The baker's
  base guard (`check_base_is_source_plus_anchors`) is byte-exact, so 12b/26b's anchored base
  (`family_bases/gemma4.jinja`) **cannot** be reused — e2b needs its own anchored base + (one) adapted insert.

## 2. Template differences (e2b source vs 12b/26b source)
Diffed `family_bases/gemma4_e2b.source.jinja` (343 lines) against `gemma4.source.jinja` (382 lines).

| # | Difference | Bake impact |
|---|---|---|
| 1 | **No `format_type_argument` macro** (e2b inlines the `\| upper` type logic). | **Auto-handled.** `bake_index.py` detects the absence and prepends `MACRO_PATCH` (a fallback shim). No manual work — but the shim must be present in the output. |
| 2 | `format_parameters` has **no `filter_keys` param**; type checks use `\| upper == 'STRING'` not `'string' in value['type']`. | Cosmetic to us — we don't touch these macros. |
| 3 | Type guards use **`is sequence`** where 12b uses `is iterable`. | Cosmetic to us. |
| 4 | **System block differs**: e2b takes `messages[0]['content'] \| trim` directly (assumes string system content); 12b iterates content-parts. | FB_SYS anchors *after* the system block regardless, so unaffected. |
| 5 | **No multimodal branch in the tool-body scan** (image/audio/video handled only in the message-content block). | FB_TOOLMSG rebinds `tool_body` before it's rendered — unaffected. |
| 6 | **No `captured_content` capture block.** 12b wraps user/assistant rendering in `{%- set captured_content -%}…{%- endset -%}`; e2b emits content inline. | **THE key one.** `fb_user.jinja` reads `captured_content` → must be **re-authored** to read `message['content']`. |
| 7 | **Thinking mechanism differs.** 12b appends a trailing `<\|channel>thought…` block keyed on `enable_thinking \| default(false)`. e2b instead injects a `<\|think\|>` token at the **top of the first system turn** (guarded by `enable_thinking is defined and enable_thinking`) and strips via the `strip_thinking` macro. | No anchor lands here, so the bake is unaffected — **but** the "thinking-off default" is achieved by a *different* code path. Relevant to the reasoning-reverts-facts finding: on e2b, thinking is off unless the caller sets `enable_thinking`, same net effect, different lever. |

## 3. Anchor map (12b → e2b)
Six anchors. Five reuse the 12b `gemma4_idx` inserts verbatim; one (FB_USER) is re-authored.

| anchor | 12b site | e2b site (`gemma4_e2b.source.jinja`) | insert reusable? |
|---|---|---|---|
| `{#FB_PRELOOP#}` | file top | file top (before `format_parameters` macro) | ✅ `fb_preloop` (needs only `tools`) |
| `{#FB_SYS#}` | after system-block `{%- endif %}` | after **L203** `{%- endif %}` | ✅ `fb_sys` |
| `{#FB_GEN#}` | before `if not continue_same_model_turn` | before **L231** `{%- if not continue_same_model_turn -%}` | ✅ `fb_gen` (uses `ns_turn.last_user_idx`, `message`, `loop.index0` — all present) |
| `{#FB_HOOK#}` | after `for tool_call in message['tool_calls']` | after **L242** `{%- for tool_call in … -%}` | ✅ `fb_hook` |
| `{#FB_TOOLMSG#}` | after `set tool_body = follow.get('content')` | after **L285** `{%- set tool_body = follow.get('content') -%}` | ✅ `fb_toolmsg` |
| `{#FB_USER#}` | after `{{ captured_content }}` | after the **content block (~L330 `{%- endif -%}`)**, in the user-message body | ⚠️ **re-author** `fb_user` |

**FB_USER re-author (the whole delta):**
```jinja
{#- 12b (reads the capture block) -#}
{%- if role == 'user' -%}{%- set fbns.cur_user = captured_content -%}{%- endif -%}
{#- e2b (no capture block; read the message directly) -#}
{%- if role == 'user' and message['content'] is string -%}{%- set fbns.cur_user = message['content'] -%}{%- endif -%}
```
`fbns.cur_user` only feeds the **real-tool Lane-1** path (fb_hook/fb_toolmsg exchange key). The
default-native lane (fb_gen) already reads `message['content']` directly, so it's unaffected either way.

## 4. Recipe to bake e2b (what "re-anchoring" concretely is)
1. `family_bases/gemma4_e2b.jinja` = `gemma4_e2b.source.jinja` + the 6 anchor markers at the sites above.
2. `inserts/gemma4_e2b_idx/` = copy of `inserts/gemma4_idx/` with **only `fb_user.jinja`** changed (above).
3. Bake:
   ```
   python bake_index.py --facts secnet_bank.jsonl --controls controls_repo.txt \
     --taskwords secnet_taskwords.json \
     --base family_bases/gemma4_e2b.jinja --source-template family_bases/gemma4_e2b.source.jinja \
     --family gemma4_e2b_idx --out secnet_baked_gemma4_e2b.jinja \
     --src-gguf <e2b .gguf> --dst-gguf <e2b netsec-expert .gguf>
   ```
4. **Verify OFFLINE (no GPU):** render the output template with a Jinja engine against synthetic inputs
   (empty messages, a tool def, a multimodal content-list) — this mirrors llama.cpp's load-time probe,
   which *rejects the whole model* if the template throws. Only bake the GGUF after a clean render.

## 5. RESULT — baked 2026-07-16 (verified offline, NOT run)
Re-anchoring done exactly as §4. Artifacts:
- `family_bases/gemma4_e2b.jinja` — anchored base (base−anchors == source, sha-verified).
- `inserts/gemma4_e2b_idx/` — copy of `gemma4_idx`; **only `fb_user.jinja`** changed (captured_content → `message['content']`).
- `secnet_baked_gemma4_e2b.jinja` — baked template, **116,516 B = 114 KiB** (same as 12b/26b secnet; far under the 980 KB LM-Studio wall → loads normally everywhere, no yaml workaround).
- **GGUF:** `factbank/gemma-4-E2B-netsec-expert-GGUF/gemma-4-E2B-netsec-expert-Q4_K_M.gguf`
  — 3,428,018,688 B (source 3,427,877,696 B; **+140 KB** = template+bank metadata, tensors copied untouched).

**Metadata read back from the GGUF:** arch `gemma4`, `factbank.version 0.4.0`, chat_template 116,516 B,
`factbank.bank` 40,715 B (115 facts), all anchors expanded, `fb_post` index present, **e2b macro shim
present** (MACRO_PATCH auto-applied since e2b lacks `format_type_argument`), template is the **e2b family**
(not 12b).

**Offline render (jinja2, in-process — no GPU, no model):** all 6 llama.cpp load-probe inputs render clean
on both source and baked (plain user / empty / system+user / with-tools / multimodal-list / tool-exchange).
Bank fires correctly: a `volatility3` query injects the Volatility-3 plugin-migration facts; the forged
native tool exchange fires on plain queries and **stands down** on multimodal / tool-declared inputs.

## 6. Tested 2026-07-16 — base vs bank (DONE)
Ran on llama-server (6 parallel slots), authority + thinking-ON, Gemma-native sampling, 48 questions.
**Base 19/48 → Baked 32/48 (+13, +27 pts); easy 12→20, hard 7→12; 1 regression (h09 paramiko).**
Zero empties/truncation under 6-way parallel. Full write-up:
`v2/extractor/experts/security-networking/BAKE-TEST-REPORT-e2b.md`; transcripts in that expert's `runs/`.

Still open (owner-gated): Q8_0 e2b variant; strengthen paramiko/eBPF fact coverage; a 12b run for a
full 2B/12B/26B curve.
