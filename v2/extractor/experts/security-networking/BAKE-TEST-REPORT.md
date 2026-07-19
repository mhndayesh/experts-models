# Security & Networking expert — bake + test report (26b)

**Date:** 2026-07-16 · **Model:** gemma-4-26B-A4B (QAT Q4_0) · **Method:** baked GGUF chat-template
(in-engine retrieval), thinking-ON + authority framing. **All scores hand-verified** (SCORE-MANUALLY rule).
**All model/serving/sampling settings:** `MODEL-SETTINGS.md`.

## Headline
| test | base 26b | baked 26b | delta |
|---|---|---|---|
| **Easy** (30 single-API landmines, temp 0.6) | 21/30 | **27/30** | **+6**, 0 regressions |
| **Hard** (18 silent-failure + multi-fact chains, Gemma-native sampling) | 16/18 | **18/18** | **+2**, 0 regressions |

Two findings the hard test surfaced: (1) **sampling dominates** — bare `temp 0.6` caused repetition-loop
EMPTY answers on hard tasks; Gemma-native sampling (temp 1.0, top_k 64, top_p 0.95, **min_p 0.01**) removed
them and lifted BOTH models. (2) On mainstream libraries the 26b base *already knows* the silent-failure
semantics; the bank's clean wins concentrate on the **genuine rewrites** (volatility3 v2→v3, yara-x Rust) —
exactly the untrained-tool case the thesis targets. **Zero regressions in either test.**

## What was built
- **Bank:** 114 landmine facts across **7 elite libraries** — cryptography (20), openssl (31),
  paramiko (16), urllib3 (14), volatility3 (8), yara-x (9), ebpf/BCC→libbpf (16). All DeepSeek-extracted,
  100% quote-grounded, 0 integrity issues.
- **Bake:** `adapt_secnet.py` → `bake_index.py` into a **fresh clean 26b** (not the GitChameleon one).
  Template **118 KB** (2317 index terms) — far under any size wall.
  Output: `factbank/gemma-4-26B-A4B-netsec-expert-GGUF/…-Q4_0.gguf`.
- **Test:** 30 hand-authored landmine questions (`test_questions.jsonl`), ≥1 per library. Each targets a
  fact where the *trained-prior* answer is the OLD API and the correct post-migration answer is the NEW one.
  Harness: `test_secnet.py` (auto-triage = substring pre-check; **verdict = hand-read**).

---

# EASY TEST — 30 single-API landmines

## Conditions (identical prompts, the only variable is the bank)
- **base-26b** — clean gemma-4-26b, no bank. think-ON, authority prompt, temp 0.6, max_tokens 4096.
- **baked-26b** — security bank baked in (fires in-engine). Same settings.

## Result (hand-scored)

| | score | vs base |
|---|---|---|
| **base 26b (no bank)** | **21 / 30** | — |
| **baked 26b (bank fires), as-phrased** | **27 / 30** | **+6, zero regressions** |
| **baked 26b, gate-corrected** | **30 / 30** | see volatility note |

**6 bank wins, 0 regressions.** Every case the bank flipped is an *obscure / silent* landmine the base
model got wrong from stale training:

| q | lib | base (wrong) | baked (correct, cites the fact) |
|---|---|---|---|
| q02 | cryptography | `from cryptography.hazmat.primitives.ciphers.algorithms import TripleDES` | `…hazmat.decrepit…` |
| q03 | cryptography | invented `csr.get_attributes()` loop | `csr.attributes.get_attribute_for_oid(oid)` |
| q08 | openssl | deprecated `BN_is_prime_ex()` | `BN_check_prime()` |
| q14 | paramiko | `from paramiko.common import asbytes` | `from paramiko.util import asbytes` |
| q22 | yara-x | "minimum **2** characters" | "no — minimum **3** characters" |
| q28 | openssl | wrong `EVP_PKEY_get_octet_string_param` + wrong param macro | `EVP_PKEY_get_bn_param()` |

The 21 the base already knew are mostly **headline** OpenSSL-3.0 / libbpf changes that predate the cutoff
(providers, `EVP_MAC`, `EVP_default_properties_is_fips_enabled`, `EVP_PKEY_keygen`, `bpf_map_lookup_elem`,
`BPF_CORE_READ`, …). The bank correctly left those untouched — no regression. **This is the thesis in
miniature: the model already reasons about the common cases; the bank supplies the knowledge it lacks on
the silent ones.**

## The 3 "both fail" (volatility3) — a GATE finding, not a knowledge gap
q17/q18/q19 failed on BOTH base and baked *as-phrased*. Cause is **not** missing facts — it is a
retrieval-gate vocabulary mismatch. The gate trigger for the library is:
`volatility3|layers|context|plugins|treegrid|calculate|table_row|interfaces|render_text|short_option|table_header|plugininterface|get_requirements`.
My questions said "**Volatility 3**" (spaced), "**plugin**" (singular), "**layer**" (singular) — none match
the exact gate tokens `volatility3`/`plugins`/`layers`, so **the gate never opened and no facts injected**
(the model's own reasoning: *"use documentation lookup facts (if available, but … I need to recall")*).

Re-asked with the real import token **`volatility3`** (`probe_vol.jsonl`, max_tokens 6144), all three flip
to correct and cite the injected fact:
- q17b → `class MyPlugin(interfaces.plugins.PluginInterface): def run(...)`  ✓
- q18b → returns a `TreeGrid(columns=[…])`  ✓
- q19b → `get_requirements()`  ✓

So the knowledge is present and correct; **3/3 recover when the gate opens.** (q19 also hit the thinking-ON
shared-budget truncation at 4096 → empty answer; 6144 fixed it.) This is the same gate-vocabulary
brittleness the GitChameleon work documented — the fix is gate normalization: token-normalize the query
(`"volatility 3"`→`volatility3`), add singular/plural stemming, and register `volatility`/`vol3` aliases.

## Verdict (easy test)
On the easy security landmine test the bank is a clean **+6 (21→27/30, 30/30 gate-corrected) with zero
regressions** on a **26b**, using thinking-ON + authority — exactly the deployable configuration. The bank
fires in-engine (llama.cpp), the reasoning cites the injected facts and defers to them, and it only moves
the needle where the base model is actually wrong.

---

# HARD TEST — 18 silent-failure + multi-fact chains
*(owner request: "if base got 21 it means it's relatively easy — make real complex test")*
18 deliberately hard questions (`test_questions_hard.jsonl`): **silent-failure / behaviour-change** facts
(where the base is *confidently wrong*, not just missing a rename) and **multi-fact chains** (one task
needing 3–5 landmines at once — full OpenSSL-3 keygen→sign→modulus, a complete volatility3 plugin, a full
BCC→libbpf/CO-RE conversion). Library named with its canonical import token so the gate reliably opens
(knowledge is under test, not gating).

### The sampling finding (this is a real result, not a footnote)
First hard run used **`temperature 0.6` with no top_k/top_p/min_p**. On hard multi-step tasks the model
collapsed into a **repetition loop** — repeating one uncertain token (e.g. *"It's `EVP_PKEY_get_param_asc`…
no."* ×20), running the thinking channel to `finish_reason=length` and committing an **EMPTY answer**. This
is **NOT** a budget/context limit: h04 looped identically at 12,288 tokens. Root cause = **sampling**.
Official Gemma-3 config is `temp 1.0, top_k 64, top_p 0.95, min_p 0.0–0.01`; the **`min_p` floor is what
breaks the loop**. Switching to it removed **all** empties (0/18 vs 3/54 before) AND lifted both models
(base 13→16, baked 17→18). Lesson: **always send the model's native sampling set — never a bare low temp.**
Full detail in `MODEL-SETTINGS.md`.

### Result (Gemma-native sampling, hand-scored)
| | score | vs base |
|---|---|---|
| **base 26b (no bank)** | **16 / 18** | — |
| **baked 26b (bank fires)** | **18 / 18** | **+2, zero regressions, zero empties** |

**2 clean bank wins, both on genuine rewrites the base has no training for:**
| q | lib | base (wrong) | baked (correct) |
|---|---|---|---|
| h13 | volatility3 | ran to `length`, empty (floundered recalling the v3 API) | complete plugin: `PluginInterface` + `get_requirements()` + `run()`→`TreeGrid()` |
| h15 | yara-x | "(a) yes (b) **yes** (c) **yes**" — 2 of 3 wrong | "(a) yes (b) **no** (c) **no**" — all 3 correct |

**Why only +2 (and why that's the honest, thesis-confirming result):** at its native sampling the 26b base
is genuinely strong on *mainstream* silent-failure semantics — it already knows ChaCha20's counter-in-nonce
(h01), `EVP_PKEY_get0_RSA` returning a provider-managed cached copy (h05), `RAND_bytes_ex`/`EVP_RAND` (h06),
`SSL_CTX_new_ex` (h07), the SSHConfig `proxycommand=None` trap (h08), urllib3's UTF-8/TLS-1.2/SAN changes
(h10–h12), the full BCC→libbpf/CO-RE conversion (h16), and `EVP_MAC` HMAC (h17). The bank correctly **ties**
there and **never regresses** a right answer. Its decisive value is exactly where the thesis says it should
be: the **post-cutoff rewrites** (volatility3 v2→v3, yara-x's Rust rewrite) — tools the model was never
trained on, where it either flounders to empty or is confidently wrong.

> Scoring note: borderline calls (h06 base used `EVP_RAND` fetch instead of `RAND_bytes_ex`; h07/h14 checker
> false-negatives; h14's precedence phrasing) were resolved **in the base's favour** — so +2 is a lower
> bound. Strict scoring of h14 would make it +3.

## Reproduce
Full pipeline (extract → bake → serve → test) with rationale: **[METHODOLOGY.md](METHODOLOGY.md)**.
All settings: **[MODEL-SETTINGS.md](MODEL-SETTINGS.md)**. In brief:
```
# bake
cd v2/bake/template-brain-v3.1
python adapt_secnet.py
python bake_index.py --facts secnet_bank.jsonl --controls controls_repo.txt \
  --taskwords secnet_taskwords.json --out secnet_baked_gemma4.jinja \
  --src-gguf <clean-26b.gguf> --dst-gguf <netsec-expert.gguf>
# serve (own test server; never touches the user's loaded model)
powershell -File v2/bake/serve_factbank.ps1 -Gguf <baked.gguf> -Port 8080 -Ctx 8192
# test (Gemma-native sampling is the default now)
cd v2/extractor/experts/security-networking
python test_secnet.py --tag hard-baked-26b-native --port 8080 --think --authority \
  --qfile test_questions_hard.jsonl
```

## Artifacts
- **Docs:** [README.md](README.md) · [COVERAGE.md](COVERAGE.md) · [METHODOLOGY.md](METHODOLOGY.md) · [MODEL-SETTINGS.md](MODEL-SETTINGS.md) · [RESEARCH.md](RESEARCH.md)
- **Test sets:** `test_questions.jsonl` (easy), `test_questions_hard.jsonl` (hard), `probe_vol.jsonl` (gate probe); harness `test_secnet.py`
- **Raw evidence → [`runs/`](runs/):** every `*_transcript.jsonl` / `*_run.log` / `*_score.txt`. The
  headline numbers come from `runs/hard-base-26b-native_*` and `runs/hard-baked-26b-native_*` (hard) and
  `runs/base-26b_*` / `runs/baked-26b_*` (easy).
- **Baked GGUF:** `factbank/gemma-4-26B-A4B-netsec-expert-GGUF/…-Q4_0.gguf`
