# Security & Networking expert — e2b bake test (base vs bank)

**Date:** 2026-07-16 · **Model:** `google/gemma-4-E2B-it` (Q4_K_M) · **Bank:** netsec-expert
(114 landmine facts, 7 libraries) baked into the e2b GGUF chat-template (114 KiB template, in-engine retrieval).

This is the **third** model to carry this bank (after 26b), and the **first e2b bake** — e2b uses a different
gemma-4 template revision, so it needed its own re-anchoring (see `v2/bake/template-brain-v3.1/E2B-BAKE-NOTES.md`).

## Method (matches the 26b "standard")
- **Same prompt** base vs baked (the baked template injects facts internally; the question is identical).
- **AUTHORITY system prompt + thinking-ON** (the documented trick that stops a reasoning model reverting an
  injected fact to its trained prior).
- **Gemma-native sampling:** temp 1.0, top_k 64, top_p 0.95, min_p 0.01. **max_tokens 6000.**
- **6 parallel requests** (`llama-server --parallel 6`, harness `--workers 6`) — the model is small, so 6
  in-flight is real throughput via continuous batching.
- Served on **llama-server** (NOT LM Studio — it drops `chat_template_kwargs`, so thinking-on wouldn't reach
  the template). Base and baked scored on the **same 48 questions** (30 easy + 18 hard), same settings.
- **Auto-triage → then HAND-READ every answer** (the verdict). Transcripts: `*-e2b-*_transcript.jsonl`.

## Result (hand-verified)
| set | base | baked | Δ | regressions |
|---|---|---|---|---|
| **Easy (30)** | 12 | **20** | **+8** | 0 |
| **Hard (18)** | 7 | **12** | **+5** | 1 (h09) |
| **Total (48)** | **19 (39.6%)** | **32 (66.7%)** | **+13 (+27 pts)** | 1 |

Hand-read **confirmed the auto-triage exactly** in both directions (no false pass/fail changed a cell).
**Robustness:** all 96 requests returned `finish_reason=stop` — **zero empty answers, zero truncation, zero
errors** even under 6-way parallelism. The native-sampling `min_p` floor held; no repetition-loop empties.

## Where the bank won (genuine habit-reversal landmines)
Base gave the trained (old) answer; baked gave the post-migration one:
- **cryptography:** `TripleDES` → `hazmat.decrepit` (q02); `csr.attributes.get_attribute_for_oid` (q03);
  EC serialize→reload→sign roundtrip (h03).
- **OpenSSL 3.0:** `RSA_new()` → `EVP_PKEY_new()` (q05); `BN_isprime` → `BN_check_prime()` (q08);
  `FIPS_mode()` → `EVP_default_properties_is_fips_enabled()` (q10); modern `EVP_MAC` HMAC (q11);
  `RSA_get0_n` → `EVP_PKEY` param API (q28); `EVP_PKEY_get0_RSA` returns a **const cached copy** (h05);
  `SSL_CTX_new` → `SSL_CTX_new_ex()` (h07).
- **YARA-X:** base64 min-3-char rule (q22); different custom alphabets + 3-char + wildcard rules (h15).
- **volatility3:** full v3 plugin — `interfaces.plugins.PluginInterface` + `TreeGrid()` + `run()` (h13).
- **paramiko:** `SSHConfig` sets `proxycommand=None` instead of deleting the key (h08).

## Where BOTH still fail (bank did not rescue — the e2b ceiling + weak facts)
- **eBPF / CO-RE:** `bpf_printk` (q25), `BPF_CORE_READ` (q27), full BCC→libbpf convert (h16). The 2B model
  struggles to apply these even with facts present; retrieval/coverage worth a look.
- **volatility3:** `TreeGrid` return (q18), `get_requirements` (q19) — baked was sometimes *confidently wrong*.
- **paramiko:** `asbytes` util import (q14, both gave the same wrong `from paramiko import asbytes`);
  `password=` kwarg (q13).
- **OpenSSL:** `RAND_bytes_ex` lib-context variant (q09, h06 — baked got `EVP_RAND` but not `RAND_bytes_ex`);
  full `EVP_MAC` fetch/ctx sequence (h17).

## The one regression
- **h09 (paramiko, encrypted key + connect):** base used the correct `password=`; baked reverted to the old
  `passphrase=`. Paramiko's `password=` landmine is weak/under-retrieved in this bank (q13/q14 also failed on
  both models) — this is a **fact-coverage gap**, the place to strengthen next, not a template problem.

## Takeaway
On a **2B-class edge model**, the bank moved security-landmine accuracy **39.6% → 66.7% (+27 points)** with a
single regression, and the wins land squarely on genuine reverses-a-habit APIs. e2b now joins 26b as a proven
carrier of this bank. The e2b template re-anchoring works in-engine (llama.cpp), zero empties under 6-way
parallel — the small model is the most bank-dependent of the three and shows the largest relative lift.

**Not done (owner-gated):** Q8_0 e2b variant; strengthening paramiko/eBPF fact coverage; a 12b run of this
same bank for a 3-size (2B/12B/26B) curve.
