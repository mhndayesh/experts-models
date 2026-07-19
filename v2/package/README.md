# factbank

Keep reasoning in the model, keep facts in a bank you own. `factbank` wraps any local
OpenAI-compatible model with a sealed **draft → retrieve → refine** loop over an editable JSONL
fact bank, and serves the result as one OpenAI-compatible endpoint. The model stays stock; the
knowledge stays yours and stays correct for fast-moving libraries the model was never trained on.

This is the **Served-Loop** architecture. For how it relates to the baked-GGUF path (which produced
the benchmark numbers), see [`../ARCHITECTURES.md`](../ARCHITECTURES.md).

## Install

```bash
pip install -e .            # core (serve + loop)
pip install -e ".[bake]"    # also enables `factbank bake` (writes a bank into a GGUF; needs gguf)
```

Requires Python ≥ 3.11. Core deps: `numpy`, `rank-bm25`.

## Quickstart

1. Load a model in your local OpenAI-compatible server (LM Studio / llama-server) — **factbank
   never loads or unloads a model; it only calls the one you loaded.**
2. Serve:

```bash
factbank serve --config factbank/factbank.toml
# or explicitly:
factbank serve --upstream http://127.0.0.1:1234/v1 \
               --model <your-loaded-model-id> \
               --bank factbank/facts_v2.jsonl \
               --api-key "$FACTBANK_KEY"
```

3. Point any OpenAI client at `http://127.0.0.1:8000/v1`.

A ready-to-use bank ships as [`factbank/facts_v2.jsonl`](factbank/facts_v2.jsonl) (5,531 landmine facts
across 54 libraries). Configuration: [`factbank/factbank.toml`](factbank/factbank.toml) (all keys, with
comments).

## The fact bank

Facts are plain JSONL and load in either schema (see [`../extractor/SCHEMA.md`](../extractor/SCHEMA.md)):

- **Package rows** — `{id, text, source, version, kind, meta}`.
- **Lab/expert rows** — the extractor's rich schema (`truth`, `lib`, `type`, …); the loader maps them
  automatically via `Fact.from_row`.

Regenerate the shipped bank from the expert banks (single source of truth for the mapping):

```bash
python ../extractor/experts_to_package.py --out factbank/facts_v2.jsonl
```

## Security

If the serving port is reachable by anything other than you, set `--api-key` (or `[serve] api-key`).
With a key set, `/v1/*` and the admin/update endpoints require a bearer token, `/admin/update` also
requires a loopback origin + CSRF token, and a chat message can no longer trigger a bank update.
`/health` reports only liveness. The background updater is wrapped by the same upstream guard as the
chat path, so an auto-update can never JIT-load a different model.

## Layout

| file | role |
|---|---|
| `factbank/bank.py` | the frozen bank + BM25 retrieval + `Fact.from_row` schema mapping |
| `factbank/server.py` | the OpenAI-compatible HTTP server |
| `factbank/factloop.py` | the draft → retrieve → refine loop |
| `factbank/watch.py` | optional auto-updater (fetch releases → extract → apply) |
| `factbank/bake.py` | `factbank bake` — writes a static all-facts bank into a GGUF (Static-Bake) |
| `factbank/facts_v2.jsonl` | the shipped default bank |
| `factbank/factbank.toml` | sample config |

## License

MIT — see [`LICENSE`](LICENSE). Third-party material bundled in the research tree is attributed in
[`../../THIRD-PARTY-NOTICES.md`](../../THIRD-PARTY-NOTICES.md).
