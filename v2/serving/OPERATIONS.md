# Operations — what to run, and in what order

All commands run from `template-brain-v3.1/template-brain-v3.1/`. All paths are relative.

```bash
cd "template-brain-v3.1/template-brain-v3.1"
```

---

## The golden path — bank → template → gates

```bash
# 0. GATE THE MINE FIRST. It is ~66% junk (F-064) and the junk BREAKS RETRIEVAL:
#    duplicate terms flatten IDF and crowd the top-5. Never bake a mine straight.
python dedupe_mine.py                    # api_facts/data__*.jsonl -> facts_mined_clean.jsonl
#    ...then READ facts_mined_clean.rejects.jsonl. Four bugs in that gate were caught
#    that way and none by a test; two silently deleted REAL APIs.

# 1. build a fact pool: curated facts + one mined domain (data | web | ai | stdlib)
python build_pool.py --domain data --out _pool.jsonl

# 2. select the bank (per-library quotas; curated facts are never cut)
python select_facts.py --pool _pool.jsonl --out bank.jsonl --default-quota 200

# 3. bake the template (and optionally the GGUF)
python bake_index.py --facts bank.jsonl --out tpl.jinja \
    [--src-gguf <base.gguf> --dst-gguf <out.gguf>]
#    THERE IS NO DEFAULT SIZE CAP (F-059 - the wall is dead). The wall exists on ONE
#    route only: LM Studio loading a raw .gguf by hand. Opt into the guard with
#    --route rawgguf (hard-fails above 980,000 B = 957 KiB). llama.cpp and the Hub
#    model.yaml route have NO size limit - proven live at 1.5 MB and 2.0 MB.
#    For a llama.cpp-only "max" template, raise it: --max-bytes 40000000

# 4. GATES — never ship without these
python parity.py tpl.jinja          # jinja2 vs the real engine: 22/22 or do not bake
python lint.py tpl.jinja "scenarios_pydata/*.json"    # 8/8
```

The bake is **deterministic**: two runs of the same command produce byte-identical
templates. If they don't, something regressed.

## Measuring retrieval (free, offline, no GPU)

```bash
python jinja_lab/lab_bench.py       # retrieval quality of every design, offline
python jinja_lab/stress.py          # render latency in the real engine
python jinja_lab/probe_minja.py     # what the template engine actually allows
```

The gold set is `jinja_lab/gold.json`: **12 questions, each paired with the fact id it
must retrieve**, plus **10 controls that must retrieve nothing**. Retrieval is scorable for
free — no GPU, no bake, no model. Any template can be run in the **real engine** without a
7 GB bake:

```bash
llama-server --model <any small gguf> --chat-template-file <tpl.jinja> --port 8100
# then POST /apply-template with {"messages":[{"role":"user","content":"..."}]}
```

That renders the template against a real question in ~10 seconds. Use it. It is the
difference between measuring the language we ship and the one we don't.

## Verifying an LM Studio deployment

```bash
# after LM Studio has loaded the model:
python lmstudio_yaml_test/check_override.py --expect <the-template-you-published>.jinja
```

It reads the **actual `llama-server` process command line** LM Studio spawned, hashes the
temp template file it was handed, and asserts: not the sentinel, >1 MiB, canary present,
SHA-256 matches. A cached config cannot fool it.

Also worth a look, free and instant:
`~/.lmstudio/.internal/gguf-metadata-cache.json` — LM Studio's own record of the template
it read out of each GGUF. If the `chatTemplate` length is **48**, that build is bricked.

## Two rules that are not optional

**1. Never load or unload a model without permission.** Requesting an unloaded model id
makes LM Studio JIT-load it, which **evicts whatever the owner had resident**.

**2. Free the VRAM when a run finishes.** On this machine, inference processes do not
reliably release GPU memory. Kill the process explicitly, then *verify*:

```bash
tasklist | grep -i llama-server      # should be only LM Studio's own
```

A "finished" run that is still resident will OOM whatever comes next.

## Where things are

| | |
|---|---|
| shipped bank | `facts_pythondata_v4.jsonl` (1,911 facts) |
| shipped template | `baked_index_v6.jinja` (973,652 bytes — matches the live GGUF exactly). **Not reproducible from current code: `sanitize()` post-dates it, so 13 facts carry raw `repr()` memory addresses (F-066).** |
| Doc2Token expansions | `expansions_v2.json` (388 facts / 2,326 questions) |
| aliases | `aliases.json` |
| mined pool | `api_facts/` (46,834 raw facts, 45 libraries, 4 domains) — **~66% JUNK, gate with `dedupe_mine.py` before use (F-064).** Only `data` has been gated; `ai__*`/`std__*` are un-inspected |
| the search lab | `jinja_lab/` |
| LM Studio override harness | `lmstudio_yaml_test/` |
| retrieval template source | `inserts/gemma4_idx/` |

**Version your output filenames.** A stale background job once overwrote a good expansions
file (388 good → 90 garbage) because two runs shared an output path. `expansions.json` is
retired for that reason; `expansions_v2.json` is the good one.

## Gating a mined bank (free, offline, no GPU)

`mine_api.py` walks `inspect.signature` **including the inheritance chain**, so its raw
output is ~66% duplicates and boilerplate — and the duplicates actively break retrieval by
flattening IDF (F-064). Never bake a mine straight.

```bash
cd "template-brain-v3.1/template-brain-v3.1"
python dedupe_mine.py            # api_facts/data__*.jsonl -> facts_mined_clean.jsonl
                                 #                         -> facts_mined_clean.rejects.jsonl
```

Prints the cull, the reason breakdown, per-library kept%, and the two numbers that matter for
retrieval health: **facts sharing a docstring with ≥5 others** (want <5%) and **facts per
method name** (want <2.0).

**Then read the reject file.** This is not optional and it is not a formality — four bugs in
this gate were caught that way and none by a test. Two of them silently deleted real APIs:

```bash
# sample every rejection reason by hand before trusting the cull
python -c "
import json,random,collections
random.seed(3)
rej=[json.loads(l) for l in open('facts_mined_clean.rejects.jsonl',encoding='utf-8')]
by=collections.defaultdict(list)
for r in rej: by[r['reject_reason'].split(':')[0]].append(r)
for why,g in sorted(by.items(), key=lambda kv:-len(kv[1])):
    print('='*90); print('##',why,'--',len(g))
    for r in random.sample(g,min(14,len(g))): print('  [%-11s] %s'%(r['source'],r['text'][:140]))
"
```

Note `package/factbank/gates.py` is the **wrong tool** here: `gate_schema` requires `quote`
and `probes`, which only model-extracted candidates carry, so a mine dies on a schema error
rather than on its real defect. Same boundary principle, different candidate shape.

Only the `data` domain has been gated. `api_facts/ai__*` and `api_facts/std__*` have not been
inspected — assume they carry the same defects.
