# Publishing FactBank experts to Hugging Face

The GitHub repo carries the **banks** (fact JSONL) + the **bake code** — small, already public. The
**ready-baked GGUFs** are 3–13 GB, so they ship to **Hugging Face** (one model repo per size). This folder
holds the upload-ready **model cards** and an upload script; the GGUFs are pushed straight to HF (never into
git). **All three security experts are now published (2026-07-17); the local baked GGUFs were then deleted to
free ~89 GB — HF is the canonical store, and any expert re-bakes from base + bank in one `bake_index.py` call.**

## Naming (settled)
Line = **expert**; a variant is `<domain>-expert` with the domain shortened to the term people actually use
(`netsec` = network & security, as in r/netsec). HF repos follow the on-disk folder names:
`<hf-user>/gemma-4-<size>-netsec-expert-GGUF`.
(Built with the *FactBank* method; the model is the *expert*.)

## Published — 3 experts × 3 sizes (9 repos, all gate-alias-fixed, 2026-07-17)
All live on HF and in the [collection](https://huggingface.co/collections/mhndayesh/experts-models-6a595448703ca843051011a1);
each repo = model card (`README.md`, with a libraries table + mined-sources list) + one `.gguf`. Baked with
the gate-alias fix (`gen_gate_aliases.py` → `bake_index.py --extra-aliases`). Cards under
[`security-networking/`](security-networking/), [`offensive-security-re/`](offensive-security-re/),
[`ebpf-dataplane/`](ebpf-dataplane/).

| expert | HF repos (live) | facts / libs | base→baked % (e2b / 12b / 26b) |
|---|---|---|---|
| **netsec** (security & networking) | `mhndayesh/gemma-4-{E2B,12B,26B-A4B}-netsec-expert-GGUF` | 114 / 7 | 39.6→66.7 / 56.2→81.2 / 77.1→93.8 |
| **offsec** (offensive security + RE) | `mhndayesh/gemma-4-{E2B,12B,26B-A4B}-offsec-expert-GGUF` | 489 / 17 | 27.3→84.1 / 27.3→97.7 / 38.6→97.7 |
| **dataplane** (eBPF + kernel/userspace net) | `mhndayesh/gemma-4-{E2B,12B,26B-A4B}-dataplane-expert-GGUF` | 318 / 7 | 10.6→68.1 / 34.0→87.2 / 42.6→91.5 |

GGUF quant: **Q4_K_M** for e2b, **Q4_0** for 12b/26b (~3.19 / 6.50 / 13.45 GB). netsec's pre-fix bake is kept
on each netsec repo as tag **`v1-pre-gate-fix`**.

## Published — the SECURITY / APPSEC expert (2026-07-18/19) — a DIFFERENT route (model.yaml) + BOTH editions
The appsec bank's template is **4.18 MB** — over LM Studio's ~980 KB raw-GGUF cap (F-053) — so it ships the
**model.yaml / LM Studio Hub route** (not a raw GGUF drop-in), and it ships **two thinking editions** per size.
- **LM Studio Hub — 6 virtual models:** `mhndayesh/gemma-4-{e2b,12b,26b-a4b}-security-expert` (+ `-thinking`).
  Each is a `model.yaml` that references the base GGUF on HF and delivers the 4.18 MB bank via
  `llm.load.promptTemplate` (bypasses the cap), with **sampling + context baked into the settings**
  (`config.operation.fields`: temp 1.0 / topK 64 / topP{checked,0.95} / minP{checked,0.01}; `config.load`
  `contextLength 32768`). Push with `lms push -y` from a folder containing only `model.yaml` (slug MUST be
  lowercase; the transient "signed preamble" error just needs a retry).
- **Hugging Face — 3 GGUF repos:** `mhndayesh/gemma-4-{E2B,12B,26B-A4B}-security-expert-GGUF`, each holding
  **both** GGUFs (`…-Q4_*.gguf` thinking-off + `…-thinking-Q4_*.gguf`) + both templates + both model.yaml +
  one card documenting both editions. In the **Information Security EXPERTS** collection. (HF dedups the base
  weights → only ~5 MB of new template data uploads per GGUF.)
- **Thinking-ON fix** (why both editions work): `decisions/TICKET-thinking-on-enablement.md`.
- **Build/publish kit:** `publish/security-appsec/` — `build_publish.py` (model.yaml + templates),
  `write_cards.py` (the 3 cards), `bake6.py` (the 6 GGUFs). Bank source: `experts/appsec/facts/FINAL_v3.jsonl`.
  The generated templates/model.yaml/GGUFs are **gitignored** (regeneratable; canonical copies on HF).

Upload flow used: `create_repo(exist_ok=True)` → `upload_file` card as `README.md` → `add_collection_item`
→ `upload_file` the GGUF. **Local GGUFs have since been deleted** — to re-upload after a re-bake, point the
`--dst-gguf` at a fresh path and run the same flow.

## License — REQUIRED
These are derivatives of Google's **gemma-4** (weights untouched; only the chat-template carries the bank).
Redistribution must carry the **Gemma Terms of Use**. Each card sets `license: gemma` and links the base
model. Do not strip that. The fact bank itself is this project's content (see the repo `LICENSE`); mined
source docs keep their own licenses (recorded in each expert's `sources/`).

## Upload (you run this — needs your HF account)
```bash
pip install -U "huggingface_hub[cli]"
huggingface-cli login                       # or: export HF_TOKEN=hf_...
# then, per size (script does card + GGUF in one repo):
bash upload_hf.ps1   # PowerShell: ./upload_hf.ps1 -HfUser <you>
```
Or manually per model:
```bash
huggingface-cli repo create <you>/gemma-4-12B-netsec-expert-GGUF --type model -y
huggingface-cli upload <you>/gemma-4-12B-netsec-expert-GGUF \
  "security-networking/gemma-4-12B-netsec-expert/README.md" README.md
huggingface-cli upload <you>/gemma-4-12B-netsec-expert-GGUF \
  "C:/Users/mhnda/.lmstudio/models/factbank/gemma-4-12B-netsec-expert-GGUF/gemma-4-12B-netsec-expert-Q4_0.gguf" \
  gemma-4-12B-netsec-expert-Q4_0.gguf
```

## ✅ FIXED — netsec re-baked with the gate-alias fix (2026-07-17)
The three **netsec** models on Hugging Face (`gemma-4-{E2B,12B,26B-A4B}-netsec-expert-GGUF`) were originally
baked **before** the gate-alias fix, so a stale user typing a **natural or old name** ("Volatility 3" vs
`volatility3`) opened no tab and got 0 facts. **Now re-baked and re-uploaded in place** with
`gen_gate_aliases.py …/security-networking/facts secnet_aliases.json` (100 aliases) →
`bake_index.py --extra-aliases secnet_aliases.json`, render-verified. Proven with `render_retrieval.py`:
"Volatility 3" injected **0 facts before → 5 after** (gate opens on the `volatility` alias). The pre-fix
version is preserved on each repo as tag **`v1-pre-gate-fix`**. See `serving/LIMITS.md` and
`extractor/BLUEPRINT.md` (rule 11).

## Pre-flight checklist (per model)
- [ ] Card `README.md` uploaded as the repo README, `license: gemma`, `base_model:` set.
- [ ] GGUF uploaded with the exact filename in the card.
- [ ] Card's base-vs-baked numbers match [`../extractor/experts/security-networking/`](../extractor/experts/security-networking/).
- [ ] "How to run" says **llama-server `--jinja`** + native sampling (the bank lives in the template).
- [ ] Provenance block: base GGUF source, `factbank.version 0.4.0`, bake commit.
