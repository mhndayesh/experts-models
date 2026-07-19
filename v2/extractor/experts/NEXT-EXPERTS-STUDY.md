# Next Experts — the linking study (2026-07-17)

*Six parallel doc-scouts validated mineable migration sources across the domains where the **base model is
blindest**. This folds ~45 candidate libraries into the **fewest experts** that still retrieve cleanly.*

## The sharpened target function
The old value function (DEPARTMENTS.md) was *churn × habit-reversal × silent-failure × mineable source*.
The owner added the axis that actually separates a useful bank from a redundant one:

> **× LOW TRAINING REPRESENTATION.** Fast churn isn't enough — the base model has to be genuinely *thin* on
> it. Frontend churns hard but the internet documents it for free the day it ships, so the model tracks it.
> The lift lives in **niche/elite tooling**: small community, few tutorials, yet an official migration doc
> exists to mine. (Our own netsec curve proved this — the raw lift came from volatility3/yara-x rewrites,
> not the mainstream APIs where the base already ties.)

So we **drop** anything the model already knows even though it churns (SQLAlchemy 2.0, mainstream PySpark
API, React/Next/Vue/Tailwind) and **target** the blind spots below.

## The bundling law
An expert = one GGUF bake with **soft-door** retrieval. Bundle by **shared retrieval vocabulary** (so
soft-doors + draft-key cross-hits fire) and **shared operator/audience** — NOT by vendor or by domain label.
Merging two clusters whose vocabularies diverge pollutes door-gating (the exact gate-vocab failure that cost
volatility3 3/3 on the easy set). Netsec already proves one bake can hold 7 different-vocab libs via doors,
so we bundle aggressively — but stop where the vocabulary stops overlapping.

---

## The five experts (down from ~45 tiny banks)

### A — Offensive Security & Reverse Engineering  *(red-team + malware analysis)*
The richest vein and the natural extension of the already-published netsec line. One audience (offensive
security practitioner / malware analyst), bundled by internal doors.

| door | libraries | source quality | ~facts |
|---|---|---|---|
| `ad-offensive` | impacket, **netexec** (`cme`→`nxc`), certipy, responder, ldap3, bloodhound.py (+mitm6/Coercer) | PARTIAL–CLEAN | ~95 |
| `re-runtime` | **angr**, **capstone** (v6), **frida** (17), unicorn (2), keystone | CLEAN (best in study) | ~130 |
| `pe-static` | pefile, dnfile | PARTIAL | ~24 |
| `forensics` | **volatility3** ↑ (8→~25), plaso | PARTIAL | ~40 |
| `detection` | **yara-x** ↑ (9→~25) | CLEAN | ~25 |
| `exploit-ctf` | pwntools | CLEAN | ~16 |
| `scanner` | nuclei (v2→v3) | CLEAN | ~20 |
| | | **total** | **~350** |

Standout landmines: `cme`→`nxc` (textbook habit-reversal), certipy `-debug` went global, nuclei
`requests:`→`http:`, angr/capstone/frida/unicorn each ship explicit "what breaks" prose. **Absorbs** the
existing volatility3 + yara-x banks (currently parked in netsec).

### B — Deep Networking: eBPF & Dataplane  *(kernel / carrier tier — HIGHEST base-blindness)*
Almost zero training representation, three independent CLEAN guides. We already have a 16-fact eBPF seed
that's a strict subset of one guide.

| door | libraries | source quality | ~facts |
|---|---|---|---|
| `ebpf-loader` | **BCC→libbpf/CO-RE** ↑ (16→~40), **libbpf 1.0** (~50), XDP/libxdp (~20) | CLEAN ×3 | ~110 |
| `ebpf-ops` | Cilium (CLI + Helm/CRD) | CLEAN | ~40 |
| `userspace-dataplane` | DPDK (`rte_*`), VPP (weak) | CLEAN / PARTIAL | ~75 |
| `routing` | FRRouting | PARTIAL | ~12 |
| | | **total** | **~235** |

Standout landmines: libbpf 1.0 collapsed six map-create APIs → `bpf_map_create()`, getters drop `get_`,
`SEC("maps")`→`SEC(".maps")`; `setrlimit(RLIMIT_MEMLOCK)` now manual; Cilium `kube-proxy-replacement`
`strict`→`true`. **Absorbs** the existing ebpf bank (deepen it).

### C — Network Automation (NetDevOps)  *(stays SEPARATE from netsec & from B)*
Same engineers, but the vocabulary diverges hard (device-drivers / getters / inventory / NETCONF vs.
packets/crypto vs. `bpf_`/`rte_`). Merging would pollute gating — keep sibling, don't fuse.

| door | libraries | source quality | ~facts |
|---|---|---|---|
| `multivendor-driver` | Netmiko (4.0), NAPALM (5.0), Nornir (3.0) | CLEAN / PARTIAL | ~63 |
| `netconf-yang` | ncclient, Juniper PyEZ | PARTIAL | ~30 |
| `vendor-rest` | Cisco Meraki, DNAC SDK | PARTIAL (auto-gen churn) | ~40 |
| `validate` | pyATS/Genie, Batfish | PARTIAL / CLEAN | ~60 |
| `inventory` | pynetbox | PARTIAL | ~18 |
| `packet` | scapy (+pyshark/dpkt, weak) | PARTIAL | ~15 |
| | | **total** | **~225** |

### D — Data Engineering & Orchestration  *(biggest raw yield, broad enterprise audience)*
Enterprise-internal, less blogged than data-science basics → model weaker than the audience size implies.

| door | libraries | source quality | ~facts |
|---|---|---|---|
| `orchestration` | **Airflow 3** (120–180!), Prefect 1→2→3, Dagster | CLEAN / PARTIAL | ~280 |
| `data-quality` | **Great Expectations** V0→V1 (cleanest in cluster) | CLEAN | ~100 |
| `lakehouse` | Delta Lake (delta-rs), PyIceberg | PARTIAL | ~55 |
| `transform` | dbt (core) | PARTIAL | ~55 |
| `compute` | PySpark — **silent-default flips only** (drop broad API) | CLEAN (subset) | ~50 |
| | | **total** | **~540** |

**DROP: SQLAlchemy 2.0** — 3 years of blogs, base already emits 2.0 idioms; fails "base is blind."

### E — Web3 / Smart Contracts  *(expand the existing 48-fact seed)*
Violent, correlated churn; the base confuses viem/wagmi, ethers v5/v6, web3modal/AppKit. One bake, 3 doors.

| door | libraries | source quality | ~facts |
|---|---|---|---|
| `js-client` | **ethers 5→6** ↑, viem, **web3.py** ↑, web3.js (legacy) | CLEAN | ~120 |
| `wallet-ui` | **wagmi 1→2**, thirdweb v4→v5, web3modal→**Reown AppKit**, RainbowKit | CLEAN | ~92 |
| `contracts-tooling` | **OpenZeppelin 4→5**, Solidity 0.8, **Hardhat 2→3**, Foundry | CLEAN | ~142 |
| | | **total** | **~354** |

Standout landmines: OZ override `_update` not `_beforeTokenTransfer`, reverts→custom errors (silent
off-chain break); ethers `BigNumber`→`bigint`, `callStatic`→`staticCall`; Solidity 0.8 checked-arithmetic.
**Absorbs** the existing ethers + web3.py bank.

---

## The consolidation
**~45 candidate libraries → 5 experts** (~1,700 landmine facts), plus the already-published **netsec**
(crypto, openssl3, paramiko, urllib3) = **6 experts total.** That is the "fewest, not tons of tiny" answer:
every bundle shares a retrieval vocabulary and an operator, so soft-doors route within it and the bakes stay
one-per-audience.

### One open decision — the netsec overlap
Experts A and B want to absorb volatility3, yara-x, and ebpf, which currently ship *inside* the published
netsec model. Two ways:
- **(i) Leave netsec as shipped; A/B carry their own (deeper) copies.** No re-bake of a published model;
  minor fact duplication across banks (cheap). **Recommended now.**
- **(ii) Re-cut:** netsec shrinks to *Applied Crypto & Secure Comms* (cryptography, openssl3, paramiko,
  urllib3); vol3/yara-x → A, ebpf → B. Cleanest taxonomy, but re-bakes + re-publishes a live model.
  The clean end-state — do it once A/B exist and are proven.

## Priority (base-blindness × source-cleanliness × density × audience)
1. **A — Offensive Security & RE** — extends the proven netsec line, cleanest+densest sources, top audience.
2. **B — eBPF & Dataplane** — highest base-blindness, dense ~110-fact eBPF core from 3 clean guides, 16-fact seed.
3. **D — Data Eng & Orchestration** — biggest raw yield (Airflow 3 alone), broad new audience, clean sources.
4. **E — Web3** — expand the 48-fact seed; one bake, 3 doors, correlated violent churn.
5. **C — Network Automation** — solid, but more auto-gen/PARTIAL sources (thinner landmines) → do last.

## Uncoverable / dropped (no mineable prose source, or base already knows)
SQLAlchemy 2.0 (base knows), mainstream PySpark broad API (base knows), pyshark, dpkt, VPP binary-API
deprecations, keystone (standalone), Foundry as a *migration* target, plaso/Ghidra beyond stitched
deprecated-lists. Meraki/DNAC are auto-gen spec churn (thinner landmines — include but low priority).

---
*Sources: the six scout reports (offensive, RE/forensics, eBPF/dataplane, network-automation, data-eng,
web3), each fetching the canonical migration doc per library. This study feeds a bundling decision only — no
banks built yet. Cross-ref: [`DEPARTMENTS.md`](DEPARTMENTS.md), `security-networking/RESEARCH.md`.*
