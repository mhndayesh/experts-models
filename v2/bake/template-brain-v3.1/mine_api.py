#!/usr/bin/env python3
"""
*** SUPERSEDED 2026-07-15 for LANDMINE facts - see ../../card-mining/ ***

This miner emits SIGNATURE facts (what a callable's arguments are). Measured
result F-065: signature facts won ZERO cases - the model already knows call
signatures, so they teach it nothing. Every win came from curated "X is dead,
use Y" / behaviour facts. The replacement is the CARD MINER (card-mining/):
mine changelogs/migration guides by fixed rules -> typed cards (REPLACE/CHANGED/
GOTCHA) -> gate -> LLM second line. Proven end-to-end 5/5 on the 12B (Ecto).
Keep THIS file: it built the shipped bank and is the reference for introspection
mining if signature facts are ever wanted again. Do not use it for new banks.
(Also read card-mining/README.md and CARD-MINING-FINDINGS.md.)

mine_api.py - INDUSTRIAL fact miner: introspect an INSTALLED library and
emit one signature fact per public callable, each carrying:

  - the EXACT signature (inspect.signature on the installed object - verbatim,
    zero hallucination risk, no doc-site scraping, no LLM in the loop)
  - the docstring's summary line (the library's own words = the official docs)
  - the official doc URL for that symbol, resolved from the project's Sphinx
    intersphinx inventory (objects.inv), so every fact is doc-anchored
  - the installed version, which is the version the fact is true for

Why signature facts are worth banking even for pre-cutoff libraries: models
hallucinate keyword names, defaults and argument ORDER constantly, even for
APIs they "know". An exact signature is the highest-density correction per
token in the bank.

usage:
  python mine_api.py --lib pandas --module pandas \
      --inv https://pandas.pydata.org/docs/objects.inv \
      --inv-base https://pandas.pydata.org/docs/ \
      --python <venv python> --out pydata_facts/pandas_api.jsonl [--max 4000]

The --python interpreter is the one with the target library INSTALLED; this
script runs the introspection inside it as a subprocess (so the miner never
imports the library into its own process).
"""
import argparse, json, os, re, subprocess, sys, urllib.request, zlib

INTROSPECT = r'''
import importlib, inspect, json, sys, pkgutil
mod_name = sys.argv[1]
depth_pkgs = json.loads(sys.argv[2])   # submodules to also walk
root = importlib.import_module(mod_name)
version = getattr(root, "__version__", "")
seen, out = set(), []

def summary(obj):
    try:
        d = inspect.getdoc(obj) or ""
    except Exception:
        return ""
    if not d:
        return ""
    lines = [l.strip() for l in d.splitlines()]
    buf = []
    for l in lines:
        if not l:
            if buf: break
            continue
        if l.startswith((".. ", ":param", ":return", "Parameters", "----")):
            break
        buf.append(l)
        if l.endswith("."):
            break
    return " ".join(buf).strip()

def sig_of(obj):
    # broad except on purpose: flask's LocalProxy raises RuntimeError
    # ("working outside of application context") merely on introspection,
    # and other libraries raise their own types from __getattr__ magic.
    try:
        return str(inspect.signature(obj))
    except Exception:
        return None

def emit(qual, obj, kindhint):
    if qual in seen:
        return
    s = sig_of(obj)
    if s is None:
        return
    doc = summary(obj)
    if not doc:
        return
    seen.add(qual)
    out.append({"qual": qual, "sig": s, "doc": doc, "kind": kindhint})

def walk_module(m, prefix):
    names = getattr(m, "__all__", None) or [n for n in dir(m) if not n.startswith("_")]
    for n in sorted(set(names)):
        if n.startswith("_"):
            continue
        try:
            obj = getattr(m, n)
        except Exception:
            continue
        qual = prefix + "." + n
        if inspect.isclass(obj):
            emit(qual, obj, "class")
            for mn in sorted(set(dir(obj))):
                if mn.startswith("_"):
                    continue
                try:
                    member = inspect.getattr_static(obj, mn)
                    member = getattr(obj, mn)
                except Exception:
                    continue
                if callable(member) or isinstance(member, (property,)):
                    tgt = member.fget if isinstance(member, property) else member
                    if tgt is None:
                        continue
                    emit(qual + "." + mn, tgt, "method")
        elif inspect.isfunction(obj) or inspect.isbuiltin(obj) or callable(obj):
            emit(qual, obj, "function")

walk_module(root, mod_name)
for sub in depth_pkgs:
    try:
        m = importlib.import_module(sub)
    except Exception:
        continue
    walk_module(m, sub)

print(json.dumps({"version": version, "items": out}))
'''


def load_inventory(url, base):
    """Sphinx objects.inv v2 -> {symbol: absolute doc url}. Optional: a library
    without a Sphinx inventory (mkdocs sites, SDK READMEs) still mines - every
    fact then anchors to the doc root instead of a per-symbol page."""
    if not url:
        return {}
    try:
        return _load_inventory(url, base)
    except Exception as e:
        print(f"  [inv] no inventory ({type(e).__name__}) - anchoring facts to {base}")
        return {}


def _load_inventory(url, base):
    req = urllib.request.Request(url, headers={"User-Agent": "factbank-miner/1.0"})
    raw = urllib.request.urlopen(req, timeout=60).read()
    head, rest = raw.split(b"\n", 4)[:4], raw.split(b"\n", 4)[4]
    data = zlib.decompress(rest).decode("utf-8", errors="replace")
    inv = {}
    for line in data.splitlines():
        m = re.match(r"^(\S+)\s+(\S+)\s+(-?\d+)\s+(\S+)\s+(.*)$", line)
        if not m:
            continue
        name, role, _prio, loc, _disp = m.groups()
        if not role.startswith("py:"):
            continue
        loc = loc.replace("$", name)
        inv[name] = base.rstrip("/") + "/" + loc.lstrip("/")
    return inv


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lib", required=True, help="retrieval tab name, e.g. pandas")
    ap.add_argument("--module", required=True, help="import name")
    ap.add_argument("--submodules", default="", help="comma list of extra modules to walk")
    ap.add_argument("--inv", default="")
    ap.add_argument("--inv-base", required=True)
    ap.add_argument("--python", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--prefix", default=None, help="fact id prefix (default: <lib>api)")
    ap.add_argument("--max", type=int, default=100000)
    ap.add_argument("--max-sig", type=int, default=420, help="skip absurdly long signatures")
    a = ap.parse_args()

    subs = [s for s in a.submodules.split(",") if s.strip()]
    proc = subprocess.run([a.python, "-c", INTROSPECT, a.module, json.dumps(subs)],
                          capture_output=True, text=True, encoding="utf-8")
    if proc.returncode != 0:
        sys.exit(f"introspection failed:\n{proc.stderr[-2000:]}")
    payload = json.loads(proc.stdout)
    version, items = payload["version"], payload["items"]
    inv = load_inventory(a.inv, a.inv_base)

    prefix = a.prefix or (a.lib + "api")
    facts, n_url, skipped = [], 0, 0
    for it in items:
        qual, sig, doc = it["qual"], it["sig"], it["doc"]
        if len(sig) > a.max_sig:
            skipped += 1
            continue
        url = inv.get(qual)
        if url:
            n_url += 1
        else:
            # method pages are often documented under the class page
            url = inv.get(qual.rsplit(".", 1)[0], a.inv_base)
        # LM Studio silently refuses to render a chat template above ~1 MiB
        # (F-048), so every byte in the bank is rationed: the summary is the
        # first sentence, hard-capped.
        doc = doc if len(doc) <= 130 else doc[:127].rstrip() + "..."
        text = f"{qual}{sig} - {doc}"
        facts.append({
            "id": f"{prefix}-{len(facts)+1:04d}",
            "text": text,
            "source": a.lib,
            "version": version or "current",
            "kind": "signature",
            "meta": {"url": url, "symbol": qual},
        })
        if len(facts) >= a.max:
            break

    os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
    with open(a.out, "w", encoding="utf-8") as f:
        for r in facts:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"{a.lib} {version}: {len(facts)} signature facts "
          f"({n_url} with exact doc URL, {skipped} skipped for signature length) -> {a.out}")


if __name__ == "__main__":
    main()
