# Security & Networking expert — 12b bake test (base vs bank)

**Date:** 2026-07-16 · **Model:** `gemma-4-12B-it-QAT` (Q4_0) · **Bank:** netsec-expert
(114 landmine facts, 7 libraries) baked into the 12b GGUF chat-template (118 KiB template, in-engine retrieval).

The **middle point** of the 2B/12B/26B curve. For the cross-model synthesis see
[BAKE-TEST-CURVE-3MODEL.md](BAKE-TEST-CURVE-3MODEL.md).

## Bake (trivial — no re-anchoring)
The 12b's embedded chat-template is **byte-identical** to `family_bases/gemma4.source.jinja` (sha match), so
the existing `gemma4.jinja` anchored base + `gemma4_idx` insert family applied directly — unlike e2b, which
needed its own re-anchoring (`v2/bake/template-brain-v3.1/E2B-BAKE-NOTES.md`).
```
python bake_index.py --facts secnet_bank.jsonl --controls controls_repo.txt --taskwords secnet_taskwords.json \
  --base family_bases/gemma4.jinja --source-template family_bases/gemma4.source.jinja --family gemma4_idx \
  --out secnet_baked_gemma4.jinja \
  --src-gguf <clean 12b Q4_0> --dst-gguf gemma-4-12B-netsec-expert-Q4_0.gguf
```
Output: `factbank/gemma-4-12B-netsec-expert-GGUF/…-Q4_0.gguf` — **6.98 GB**, template 118,109 B,
115 facts, `factbank.version 0.4.0`, arch gemma4, anchors expanded, `fb_post` index present.

## Method (matches e2b, identical settings)
AUTHORITY system prompt + thinking-ON · Gemma-native sampling (temp 1.0, top_k 64, top_p 0.95, min_p 0.01) ·
max_tokens 6000 · **6 parallel** requests (`llama-server --parallel 6`, harness `--workers 6`) · same 48
questions (30 easy + 18 hard) base vs baked. Served on llama-server (LM Studio drops `chat_template_kwargs`).

## Result (hand-verified)
| set | base | baked | Δ | regressions |
|---|---|---|---|---|
| **Easy (30)** | 17 | **24** | **+7** | 0 |
| **Hard (18)** | 10 | **15** | **+5** | 1 (h04) |
| **Total (48)** | **27 (56.2%)** | **39 (81.2%)** | **+12 (+25 pts)** | 1 |

### Hand-read raised the baked score (auto-triage said 35/48 → hand-read 39/48)
Three auto "fails" were **triage false-fails** — the code was correct and the deprecated API name appeared
only in a **migration comment the model wrote to explain itself**. This is the bank's own fingerprint (it
*names* the old→new change) tripping the `avoid_old` substring check:
- **h09** — code uses `password=pw`; comment says `# use password= instead of passphrase=` → `passphrase=` hit.
- **h03** — code uses `public_bytes` / `from_encoded_point` / `.sign`; comments say `# encode_point()/signer()
  is deprecated` → those hits.
- **h18** — "raises ValueError at parsing **instead of only during validation**" → `only during validation` hit.

By the standing rule (**old name in a migration comment = pass**), all three are passes. Applied symmetrically;
the base rarely writes such comments (it usually just gives the wrong answer), so the correction favors the
bank legitimately. One **real regression** remains: **h04** — baked's 3-part OpenSSL answer generated keygen +
`EVP_DigestSign` but did not complete the modulus-extraction step (`EVP_PKEY_get_bn_param`) the base included.

**Robustness:** all 96 requests `finish_reason=stop` except one hard baked answer that hit the token cap but
still carried its answer; **zero empty answers** under 6-way parallel.

## Where the bank won (base gave the trained/old answer; baked the current one)
- **cryptography:** `TripleDES`→`hazmat.decrepit` (q02); `csr.attributes.get_attribute_for_oid` (q03);
  ChaCha20 16-byte-nonce counter (h01).
- **OpenSSL 3.0:** `RSA_new`→`EVP_PKEY_new` (q05); `BN_is_prime_ex`→`BN_check_prime` (q08);
  `OSSL_PROVIDER_available`→`EVP_default_properties_is_fips_enabled` (q10); `RAND_bytes_ex` with lib-ctx (h06);
  `SSL_CTX_new`→`SSL_CTX_new_ex` (h07); `EVP_PKEY_get0_RSA` returns a const cached copy (h05).
- **YARA-X:** base64 min-3 (q22); xor-before-fullword (h14, tie); the multi-part precise answer (h15, partial).
- **volatility3:** the full v3 plugin — `PluginInterface` + `TreeGrid` + `get_requirements` + `run` (h13).
- **eBPF:** `BPF_CORE_READ` for nested field access (q27).
- **urllib3:** TLS-1.0-fails, the two changed defaults (h11).
- **paramiko:** `SSHConfig` sets `proxycommand=None` instead of deleting the key (h08).

## Where both still fail (12b ceiling / weak facts)
- **volatility3** `TreeGrid` return (q18) and `get_requirements` phrasing (q19) — both models say "no declaration."
- **eBPF** `bpf_printk` (q25, baked hallucinated `BPF_LOG`), full BCC→libbpf convert (h16).
- **paramiko** `asbytes` util import (q14 — baked said `paramiko.utils`, it's `paramiko.util`).
- **OpenSSL** `RAND_bytes_ex` plain form (q09).

## Takeaway
On the 12B the bank is **+12 (56.2%→81.2%)** with a single regression — the middle of a clean curve where the
2B gains most in absolute terms (+13) and the 26B least (+8), while each larger model *applies* a retrieved
fact more reliably (error-closure 45%→57%→73%). See the curve doc.
