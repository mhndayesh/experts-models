#!/usr/bin/env python3
"""appsec_sast.py - ADAPTER: mine the permissive SAST rule CATALOGS (Bandit + gosec) into
insecure-by-default landmine facts. Uses the shared pipeline in appsec_core.py.

These repos ARE catalogs of insecure patterns with example code:
  - Bandit (PyCQA, Apache-2.0): each plugins/*.py docstring describes an insecure Python pattern and
    usually shows the bad line inline; blacklists/calls.py describes the dangerous-call rules (B3xx);
    examples/*.py hold the vulnerable (and sometimes the safe) sample code.
  - gosec (securego, Apache-2.0): RULES.md names every rule (Gxxx -> description); testutils/gXXX_samples.go
    hold the vulnerable Go code as raw-string CodeSamples, each tagged with an expected-issue count
    (>0 = flagged/BAD, 0 = clean/GOOD -> a verbatim secure counterpart).

Each rule -> one adapter item. corpus carries the rule description + the VERBATIM example code. The model
selects the fact and copies bad (and, when present, good) code verbatim; code that isn't verbatim-in-corpus
is dropped to a text fact by the pipeline.

usage:
  DEEPSEEK_API_KEY=$(cat /c/projects/api/deepseek.txt) python appsec_sast.py [--only bandit|gosec]
                                                                             [--limit N] [--test]
out:  experts/appsec/facts/sast.jsonl  (+ sast.rejects.jsonl)
"""
import ast, glob, os, re, sys
import appsec_core as C

HERE   = os.path.dirname(os.path.abspath(__file__))
CORPUS = os.path.join(HERE, "..", "..", "appsec-corpus")
BANDIT = os.path.join(CORPUS, "bandit")
GOSEC  = os.path.join(CORPUS, "gosec")
BANDIT_LICENSE = "Bandit (PyCQA), Apache-2.0"
GOSEC_LICENSE  = "gosec (securego), Apache-2.0"

def read(p):
    try: return open(p, encoding="utf-8", errors="replace").read()
    except OSError: return ""

# ---- door heuristic (forces retrieval consistency; scanned in priority order) ----
DOOR_KW = [
 ("deserialization-input", ["pickle","marshal","unpickl","yaml.load","yaml load","deseriali","unmarshal",
                            "jsonpickle","dill","shelve","read_pickle"]),
 ("crypto", ["md5","md4","sha1","ripemd","cipher","des ","3des","tripledes","rc4","blowfish","arc2","arc4",
             "rsa","weak crypto","weak cryptographic","weak key","insecure hash","hash for security",
             "certificate valid","cert valid","insecure random","random number","math/rand","hardcoded iv",
             "hardcoded nonce","nonce","key strength","key length","broken crypto"]),
 ("injection", ["sql inject","sql query","command inject","command execution","os command","exec(","shell=true",
                "subprocess","injection","cross-site scripting","xss","template inject","ssti","xpath","ldap",
                "paramiko","wildcard","os.system","smtp","log inject","request smuggling","unescaped","mako",
                "jinja","autoescape","xml","external entity","xxe","trojan source","bidirectional"]),
 ("secrets-config", ["hardcoded password","hardcoded credential","hardcoded secret","hard-coded","hard coded",
                     "credential","secret","private_key","password","token","debug mode","flask","app_debug",
                     "snmp","marshaling of secret","secret serialization"]),
 ("network-security", ["ssh","host key","insecureignorehostkey","bind to all","bind all","all interfaces",
                       "ssrf","server-side request","open redirect","redirect","http request","urlopen","urllib",
                       "cors","cookie","serve function","timeout","slowloris","readheadertimeout","tls","ssl",
                       "profiling endpoint","pprof","http.dir"]),
 ("memory-safety", ["unsafe block","unsafe.pointer","integer overflow","slice bounds","out of range",
                    "implicit memory aliasing","conversion which leads","overflow"]),
]
def door_for(text):
    t = (text or "").lower()
    for door, kws in DOOR_KW:
        if any(k in t for k in kws): return door
    return "web-appsec"

# =================== BANDIT: plugins ===================
def bandit_plugin_items():
    items = []
    for path in sorted(glob.glob(os.path.join(BANDIT, "bandit", "plugins", "*.py"))):
        if os.path.basename(path) == "__init__.py": continue
        src = read(path)
        try: doc = ast.get_docstring(ast.parse(src)) or ""
        except SyntaxError: doc = ""
        if not doc.strip(): continue
        stem = os.path.splitext(os.path.basename(path))[0]
        # gather example files: those named in the docstring + a same-stem file
        names = set(re.findall(r"examples/([\w\-]+\.py)", doc))
        cand = os.path.join(BANDIT, "examples", stem + ".py")
        if os.path.exists(cand): names.add(stem + ".py")
        ex_blocks = []
        for nm in sorted(names):
            code = read(os.path.join(BANDIT, "examples", nm))
            if code.strip(): ex_blocks.append(f"# vulnerable example: examples/{nm}\n{code.strip()}")
        rid = (re.search(r"\bB\d{3}\b", doc) or [None])
        rid = re.search(r"\bB\d{3}\b", doc)
        rid = rid.group(0) if rid else stem
        L = [f"Bandit rule {rid} ({stem}) - security lint rule.", "", "RULE DESCRIPTION:", doc.strip()]
        if ex_blocks:
            L += ["", "VULNERABLE EXAMPLE CODE (copy bad lines verbatim; a safe variant may also appear):", ""]
            L += ex_blocks
        text = "\n".join(L)
        items.append({"llm_input": text, "corpus": text, "source": f"Bandit {rid}",
                      "license_note": BANDIT_LICENSE, "lib": f"bandit-{rid.lower()}",
                      "version": "bandit", "door": door_for(doc + " " + stem), "lang": "python"})
    return items

# =================== BANDIT: blacklist B3xx (dangerous calls) ===================
BL_EXAMPLES = {
 "B301": ["pickle_deserialize.py","dill.py","pandas_read_pickle.py","jsonpickle.py"],
 "B302": ["marshal_deserialize.py"],
 "B303": ["crypto-md5.py"],
 "B304": ["ciphers.py","cipher-modes.py"],
 "B306": ["mktemp.py"],
 "B307": ["eval.py"],
 "B308": ["mark_safe.py","mark_safe_insecure.py","mark_safe_secure.py"],
 "B310": ["urlopen.py"],
 "B311": ["random_module.py"],
 "B312": ["telnetlib.py"],
 "B321": ["ftplib.py"],
}
def bandit_blacklist_items():
    src = read(os.path.join(BANDIT, "bandit", "blacklists", "calls.py"))
    try: doc = ast.get_docstring(ast.parse(src)) or ""
    except SyntaxError: doc = ""
    # split into per-rule blocks at "Bxxx: name" / "Bxxx - Byyy: name" headers (line start)
    hdr = re.compile(r"^(B\d{3}(?:\s*-\s*B\d{3})?)\s*:\s*(.+)$", re.M)
    marks = list(hdr.finditer(doc))
    items = []
    for i, m in enumerate(marks):
        rid = m.group(1).split()[0].split("-")[0].strip()   # leading id
        name = m.group(2).strip()
        end = marks[i+1].start() if i+1 < len(marks) else len(doc)
        block = doc[m.start():end].strip()
        ex_blocks = []
        for nm in BL_EXAMPLES.get(rid, []):
            code = read(os.path.join(BANDIT, "examples", nm))
            if code.strip(): ex_blocks.append(f"# vulnerable example: examples/{nm}\n{code.strip()}")
        L = [f"Bandit blacklist rule {rid} ({name}) - dangerous Python call.", "", "RULE DESCRIPTION:", block]
        if ex_blocks:
            L += ["", "VULNERABLE EXAMPLE CODE (copy bad lines verbatim; a safe variant may also appear):", ""]
            L += ex_blocks
        text = "\n".join(L)
        items.append({"llm_input": text, "corpus": text, "source": f"Bandit {rid}",
                      "license_note": BANDIT_LICENSE, "lib": f"bandit-{rid.lower()}",
                      "version": "bandit", "door": door_for(block + " " + name), "lang": "python"})
    return items

# =================== GOSEC ===================
def gosec_rule_descriptions():
    md = read(os.path.join(GOSEC, "RULES.md"))
    out = {}
    for m in re.finditer(r"^-?\s*\[?(G\d{3})\]?\s*[-—]+\s*(.+?)\s*(?:\(\*\*\w+\*\*\))?\s*$", md, re.M):
        gid, desc = m.group(1), m.group(2).strip()
        # strip markdown links/backticks noise but keep text
        desc = re.sub(r"`", "", desc)
        out.setdefault(gid, desc)
    return out

SAMPLE = re.compile(r"\[\]string\{\s*(`.*?`(?:\s*,\s*`.*?`)*)\s*\}\s*,\s*(\d+)", re.S)
def gosec_samples(gid):
    """Return (bad_snippets, good_snippets) for a gosec rule id from testutils/gXXX_samples.go."""
    path = os.path.join(GOSEC, "testutils", f"{gid.lower()}_samples.go")
    txt = read(path)
    bad, good = [], []
    for m in SAMPLE.finditer(txt):
        strs = re.findall(r"`([^`]*)`", m.group(1))
        code = "\n// ---\n".join(s.strip("\n") for s in strs if s.strip())
        if not code.strip(): continue
        (bad if int(m.group(2)) > 0 else good).append(code)
    return bad, good

def gosec_items():
    desc = gosec_rule_descriptions()
    items = []
    for path in sorted(glob.glob(os.path.join(GOSEC, "testutils", "g*_samples.go"))):
        m = re.match(r"(g\d{3})_samples\.go", os.path.basename(path))
        if not m: continue
        gid = m.group(1).upper()
        bad, good = gosec_samples(gid)
        if not bad: continue           # nothing insecure to teach
        d = desc.get(gid, f"gosec rule {gid}")
        L = [f"gosec rule {gid}: {d}", "", "VULNERABLE Go examples (gosec FLAGS these - copy bad lines verbatim):"]
        for b in bad[:6]: L += ["", b]
        if good:
            L += ["", "SECURE Go examples (gosec does NOT flag these - a verbatim good fix may live here):"]
            for g in good[:6]: L += ["", g]
        text = "\n".join(L)
        items.append({"llm_input": text, "corpus": text, "source": f"gosec {gid}",
                      "license_note": GOSEC_LICENSE, "lib": f"gosec-{gid.lower()}",
                      "version": "gosec-v2", "door": door_for(gid + " " + d), "lang": "go"})
    return items

# =================== driver ===================
def main():
    only  = sys.argv[sys.argv.index("--only")+1] if "--only" in sys.argv else None
    limit = int(sys.argv[sys.argv.index("--limit")+1]) if "--limit" in sys.argv else None
    test  = "--test" in sys.argv

    items = []
    if only in (None, "bandit"):
        items += bandit_plugin_items() + bandit_blacklist_items()
    if only in (None, "gosec"):
        items += gosec_items()

    nb = sum(1 for it in items if it["source"].startswith("Bandit"))
    ng = sum(1 for it in items if it["source"].startswith("gosec"))
    print(f"built {len(items)} items ({nb} bandit, {ng} gosec)")
    if limit: items = items[:limit]
    if test:
        # small hand-read slice: a few bandit + a few gosec
        band = [it for it in items if it["source"].startswith("Bandit")][:3]
        gos  = [it for it in items if it["source"].startswith("gosec")][:3]
        items = band + gos
        out = "experts/appsec/facts/sast_test"
        print(f"TEST mode: mining {len(items)} items -> {out}.jsonl")
        for it in items: print("   -", it["source"], "| door=", it["door"])
    else:
        out = "experts/appsec/facts/sast"

    # 'lang' is an adapter hint only; the pipeline reads lang from the model. Drop it from the item.
    for it in items: it.pop("lang", None)
    C.run(items, out, id_prefix="sast")

if __name__ == "__main__":
    main()
