# Coverage — the Security & Networking bank

What the bank contains: **114 landmine facts** across **7 libraries**, one JSONL per library in
[`facts/`](facts/), each fact quote-grounded to a mined source in [`sources/`](sources/). Merge of the
networking + cybersecurity departments (owner call, 2026-07-16).

**Integrity:** 0 duplicate ids, 100% of facts carry a `truth` + verbatim `quote`, 0 bad types. All facts are
**landmine-only** (no fundamentals) — each is post-cutoff, reverses a trained habit, or fails silently.

## Banks

| library | facts | version focus | mined source | landmine class |
|---|---:|---|---|---|
| **openssl** | 31 | 1.1.1 → 3.0 | [openssl-3-migration.md](sources/openssl-3-migration.md) | engines→providers, low-level→EVP |
| **cryptography** | 20 | → 43.x | [cryptography-changelog.md](sources/cryptography-changelog.md) | moved imports, removed APIs, silent behavior changes |
| **paramiko** | 16 | → 3.x | [paramiko-changelog.md](sources/paramiko-changelog.md) | removed algos, renamed kwargs, config semantics |
| **ebpf** | 16 | BCC → libbpf/CO-RE | [ebpf-bcc-to-libbpf.md](sources/ebpf-bcc-to-libbpf.md) | macro→struct, method→helper, CO-RE reads |
| **urllib3** | 14 | 1.x → 2.x | [urllib3-v2-migration.md](sources/urllib3-v2-migration.md) | flipped TLS/encoding defaults, dropped support |
| **yara-x** | 9 | YARA 4.x → YARA-X 1.0 | [yara-x-differences.md](sources/yara-x-differences.md) | regex/base64/rule-syntax + matching semantics |
| **volatility3** | 8 | Vol2 → Vol3 rewrite | [volatility3-migration.md](sources/volatility3-migration.md) | total plugin-API rewrite |
| **total** | **114** | | **7 banks** | |

## Landmine examples (what bites, per library)

- **openssl** — `RSA_new()`→`EVP_PKEY_new()`; `RSA_generate_key()`→`EVP_PKEY_keygen()`; `RSA_sign()`→
  `EVP_DigestSign()`; `FIPS_mode()`→`EVP_default_properties_is_fips_enabled()`; ENGINE API→providers;
  `RAND_DRBG`→`EVP_RAND`; `EVP_PKEY_get0_RSA()` now returns a **const cached copy** (mutation silently lost).
- **cryptography** — `signer()/verifier()`→`sign()/verify()`; `TripleDES`/`CFB`/etc. moved to
  `hazmat.decrepit`; `EllipticCurvePublicNumbers.encode_point()`→`public_bytes()`/`from_encoded_point()`;
  ChaCha20 now reads the **first 4 nonce bytes as an LE block counter**; `load_ssh_private_key()` raises
  `TypeError` on wrong password/no-password.
- **paramiko** — DSA/DSS keys removed; SHA-1 RSA signatures no longer verified; `PKey.from_path(passphrase=)`
  →`password=`; `paramiko.common.asbytes`→`paramiko.util.asbytes`; `SSHConfig` now sets `proxycommand=None`
  instead of omitting the key (the `'x' in cfg` check silently flips).
- **ebpf (BCC→libbpf)** — `BPF_HASH` macro→explicit `struct … SEC(".maps")`; `map.lookup()`→
  `bpf_map_lookup_elem()`; `perf_submit()`→`bpf_perf_event_output()`; `bpf_trace_printk()`→`bpf_printk()`;
  `ptr->a->b`→`BPF_CORE_READ()`; `kprobe__fn`→`SEC("kprobe/fn") BPF_KPROBE(...)`.
- **urllib3 2.x** — default min TLS 1.0→**1.2**; body encoding ISO-8859-1→**UTF-8**; hostname verification
  drops **commonName** (SAN-only); `HTTPResponse.strict` removed; `VerifiedHTTPSConnection`→`HTTPSConnection`.
- **yara-x** — XOR now applied **before** the fullword delimiter check (was after); base64 patterns min 3
  chars; `base64`/`base64wide` may use different alphabets; wildcard rule names in `of` (`1 of (foo*)`)
  invalid; negative array index `@a[-1]` errors.
- **volatility3** — `calculate()`→`run()`; `render_text()`/`table_header()`/`table_row()`→return a
  `TreeGrid()`; inherit `interfaces.plugins.PluginInterface`; `--profile` removed → declare needs in
  `get_requirements()`.

## Provenance

Each fact carries a verbatim `quote` from the mined migration guide / changelog in [`sources/`](sources/).
The extraction pipeline (FIND → extract → repair → check) is documented in [METHODOLOGY.md](METHODOLOGY.md).
The seven sources were selected for landmine density — see [RESEARCH.md](RESEARCH.md) for the ranking that
picked these tools over the rest of the field.

## Not yet in the bank (roadmap)

Higher-effort sources that need careful targeting: Impacket, NetExec, Nuclei, Certipy, Frida, Scapy,
netmiko/NAPALM/Nornir, Sigma/Suricata rule schemas, checkov/trivy check-IDs. Defensive / authorized-testing
framing only. Full ranked roadmap in [RESEARCH.md](RESEARCH.md) and [`../DEPARTMENTS.md`](../DEPARTMENTS.md).
