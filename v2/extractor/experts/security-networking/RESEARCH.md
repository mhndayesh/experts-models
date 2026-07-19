# Security & Networking — elite-tier research (2026-07-16)

Research to branch this specialty into the *top-tier stacks elites actually run*, ranked by **landmine
value** = fast version churn × habit-reversal density × a mineable source. The best banks are where an
elite gets burned by drift, and where an official migration guide exists to mine.

## The seven branches (elite tools per branch)

### 1. Offensive / Red Team  — the 2026 core internal-network kit
Confirmed still manual (AI hasn't replaced them): **Impacket, NetExec, BloodHound, Metasploit, Certipy, Nuclei.**
- **NetExec (nxc)** — now the preferred internal-network rapid-assessment tool (SMB/WinRM/LDAP/MSSQL). *The
  `CrackMapExec` → `NetExec` rename is itself the landmine* (binary `cme`→`nxc`, module paths).
- **Impacket** — powers Pass-the-Hash, Kerberoasting, DCSync, SMB relay; example-script + class churn across releases.
- **Certipy** — AD CS attacks (shadow credentials, Golden Tickets); major v4/v5 command reshuffles.
- **Nuclei** — template-based web/API coverage; template schema (v2→v3) + SDK churn.
- Source: GitHub CHANGELOG/releases (mine via `gh`/raw).

### 2. Reverse Engineering / Malware / Forensics — highest skill floor
- **Volatility 3** — **total rewrite from v2** (the biggest RE landmine): Python 2→3; `--profile` removed →
  auto-detect via `requirements`; `table_header()`/`table_row()` → `TreeGrid()`; unified `--dump`; plugins
  gone (`notepad`, `clipboard`, `psxview`, `apihooks`). Source: Volatility 3 docs + JPCERT "Migrate Volatility
  Plugins 2 to 3" blog. **HIGH value.**
- **yara-x** — YARA's **Rust rewrite**, 1.0 stable June 2025; "YARA is dead, long live YARA-X." ~99% rule-compat
  but the **Python/C API and CLI changed**; YARA now maintenance-only. Source: yara-x docs (docs.rs/yara-x,
  virustotal.github.io/yara-x). **HIGH value** (habit reversal: everyone must move).
- **Frida** — dynamic instrumentation; API shifts across majors (JS + Python bindings).
- **angr**, **Ghidra scripting API**, **Unicorn/Capstone/Keystone**.

### 3. Deep Networking / Data Plane — kernel & carrier tier (true elites)
- **eBPF: BCC → libbpf + CO-RE** — the defining modern-networking migration. BCC's runtime-compile "magic"
  (auto structs, code rewriting, embedded LLVM, kernel-headers-on-host) is replaced by explicit libbpf +
  CO-RE (BTF, BPF skeletons, global variables, no on-host headers). BCC itself is porting its tools to CO-RE.
  Source: Facebook BPF "BCC to libbpf HOWTO", ebpf.io CO-RE docs. **HIGH value.**
- **Cilium**, **DPDK/VPP (FD.io)**, **XDP**, **P4**, **FRRouting**, **Scapy** (packet crafting standard).

### 4. Network Automation — elite NetDevOps
- **pyATS/Genie** (Cisco), **Batfish**, **Netmiko/NAPALM/Nornir**, **ncclient**. Source: per-project changelogs.

### 5. Cloud-Native / Container Security
- **Falco** (runtime, CNCF), **Prowler**/**Pacu** (cloud pentest), **OPA/Rego**, **Trivy**, **kube-bench**,
  **tfsec/checkov**. Source: release notes; Falco rules + Prowler check-ID churn are mineable.

### 6. Detection Engineering / DFIR
- **Sigma** (rule schema versions), **Suricata**/**Zeek** (rule + script), **Velociraptor**, **osquery**.

### 7. Applied Crypto / Protocols
- **OpenSSL 3.x** — **engines → providers** is *the* elite crypto landmine, with a canonical migration guide:
  the ENGINE API is deprecated; `EVP_MD_meth_new`/`EVP_CIPHER_meth_new`/`EVP_PKEY_meth_new`/`RSA_meth_new`/
  `EC_KEY_METHOD_new` deprecated; `EVP_PKEY_get0_RSA()` now returns a cached copy (provider-managed keys);
  provided keys are immutable (`EVP_PKEY_set_type`-style mutation removed); decoded keys are provider-based.
  Source: docs.openssl.org/3.0/man7/migration_guide. **HIGHEST value** (clean official guide, huge blast radius).
- **PyNaCl/libsodium**, **WireGuard**, **Noise**.

## Recommended build order (mineable + elite, highest first)
1. **OpenSSL 3.x providers** — official migration guide, huge blast radius. ✅ clean source.
2. **Volatility 3** (v2→v3 rewrite) — docs + JPCERT guide. ✅ clean source.
3. **eBPF BCC→libbpf/CO-RE** — FB HOWTO + ebpf.io. ✅ clean source.
4. **yara-x** (YARA rewrite) — yara-x docs. ✅ clean source.
5. **NetExec** (CME→nxc) — GitHub. ⚠ mine via `gh`.
6. **Impacket** — GitHub CHANGELOG. ⚠ `gh`.
7. **Certipy**, **Nuclei**, **Frida**, **Scapy**, **Suricata/Sigma** — mixed sources.

## Suggested folder branching
Split the specialty so retrieval doors map to sub-disciplines:
`security-networking/{offensive, reversing, dataplane, netauto, cloudsec, detection, crypto}/`.
(Current flat banks — cryptography, urllib3, paramiko — fold into `crypto` and `netauto`/`offensive`.)

## Sources
- Top red-team tools 2026 (Bishop Fox / FireCompass / StationX)
- eBPF BCC→libbpf HOWTO (facebookmicrosites.github.io/bpf), CO-RE (ebpf.io)
- OpenSSL 3.0 migration guide (docs.openssl.org)
- Volatility 3 parity + JPCERT plugin-migration guide
- YARA-X (VirusTotal blog + docs.rs/yara-x)
