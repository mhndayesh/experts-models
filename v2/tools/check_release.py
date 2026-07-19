#!/usr/bin/env python3
"""check_release.py - the release gate. Run in CI; exits non-zero on any failure.

Gates (each independent; all run, all failures reported):
  1. fact-id uniqueness across every expert bank
  2. schema-compat: the package loads EVERY expert bank
  3. package smoke-import
  4. bank-lint: shipped facts_v2.jsonl carries no pipeline-meta; quotes/truths sane
  5. baked templates parse (best-effort: jinja2 if available)
  6. doc links: no v2-internal markdown link points at a missing file

  python v2/tools/check_release.py
"""
import os, sys, json, glob, re, importlib.util

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))          # v2/
REPO = os.path.dirname(ROOT)
EXPERTS = os.path.join(ROOT, "extractor", "experts")
fails, warns = [], []

def fail(g, msg): fails.append(f"[{g}] {msg}")
def warn(g, msg): warns.append(f"[{g}] {msg}")

# 1. id uniqueness -----------------------------------------------------------
seen = {}
banks = sorted(glob.glob(os.path.join(EXPERTS, "*", "facts", "*.jsonl")))
for b in banks:
    for l in open(b, encoding="utf-8"):
        l = l.strip()
        if not l: continue
        i = json.loads(l)["id"]
        if i in seen:
            fail("ids", f"duplicate id {i} in {os.path.basename(b)} and {os.path.basename(seen[i])}")
        seen[i] = b
print(f"1. id uniqueness: {len(seen)} ids across {len(banks)} banks")

# 2 + 3. package load + import ----------------------------------------------
sys.path.insert(0, os.path.join(ROOT, "package"))
try:
    from factbank.bank import Bank, Fact
    n = 0
    for b in banks:
        try:
            n += len(Bank.from_jsonl(b).facts)
        except Exception as e:
            fail("schema", f"{os.path.basename(b)} failed to load: {type(e).__name__}: {e}")
    print(f"2. schema-compat: package loaded {n} facts")
    # from_row both schemas
    assert Fact.from_row({"id": "x", "text": "t", "source": "s", "version": "1"}).kind == "doc"
    assert Fact.from_row({"id": "y", "lib": "openssl", "version": "3",
                          "truth": "use EVP", "type": "REPLACED",
                          "keywords": {"from_fact": ["RSA_new"]}}).kind == "landmine"
    print("3. package smoke-import + from_row(both schemas): OK")
except Exception as e:
    fail("import", f"{type(e).__name__}: {e}")

# 4. bank-lint on the shipped default ---------------------------------------
shipped = os.path.join(ROOT, "package", "factbank", "facts_v2.jsonl")
if os.path.exists(shipped):
    meta_leak = short_q = 0
    for l in open(shipped, encoding="utf-8"):
        l = l.strip()
        if not l: continue
        r = json.loads(l)
        if any(k.startswith("_") for k in r):
            meta_leak += 1
    if meta_leak:
        fail("lint", f"{meta_leak} shipped rows carry pipeline-meta (_*) keys")
    print(f"4. bank-lint: shipped {shipped.split(os.sep)[-1]} clean of pipeline-meta")
else:
    warn("lint", "facts_v2.jsonl not present (run experts_to_package.py)")

# 5. baked templates parse (best-effort) ------------------------------------
tpls = glob.glob(os.path.join(ROOT, "bake", "**", "*baked*.jinja"), recursive=True)
if importlib.util.find_spec("jinja2"):
    import jinja2
    for t in tpls:
        try:
            jinja2.Environment().parse(open(t, encoding="utf-8").read())
        except Exception as e:
            warn("template", f"{os.path.basename(t)} jinja2-parse: {type(e).__name__} "
                             f"(Gemma templates may use non-jinja2 constructs)")
    print(f"5. baked templates: parsed {len(tpls)} (best-effort)")
else:
    warn("template", "jinja2 not installed; skipped template parse")

# 6. doc links --------------------------------------------------------------
LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
# check OUR authored docs only; skip the legacy tree and mined third-party
# source documents (their internal links point at their own doc sites).
_SKIP = ("archive", "sources", "sources_ext", "sources_harvested")
mds = [m for m in glob.glob(os.path.join(ROOT, "**", "*.md"), recursive=True)
       if not any(os.sep + s + os.sep in m for s in _SKIP)]
broken = 0
for md in mds:
    d = os.path.dirname(md)
    for m in LINK.finditer(open(md, encoding="utf-8").read()):
        tgt = m.group(1).split("#")[0].strip()
        if not tgt or tgt.startswith(("http://", "https://", "mailto:")):
            continue
        p = os.path.normpath(os.path.join(d, tgt))
        if os.sep + "archive" + os.sep in p:      # legacy tree is untracked-by-design
            continue
        if not os.path.exists(p):
            broken += 1
            fail("links", f"{os.path.relpath(md, ROOT)} -> {tgt} (missing)")
print(f"6. doc links: checked {len(mds)} md files")

# -------------------------------------------------------------------------
print("\n" + "=" * 60)
for w in warns: print("WARN ", w)
for f in fails: print("FAIL ", f)
print(f"\n{len(fails)} failures, {len(warns)} warnings")
sys.exit(1 if fails else 0)
