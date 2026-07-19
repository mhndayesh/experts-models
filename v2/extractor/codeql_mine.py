#!/usr/bin/env python3
"""codeql_mine.py - source ADAPTER: mines github/codeql .qhelp SECURITY queries into
insecure-by-default landmine facts (verbatim bad/good code) via the shared appsec_core pipeline.

The corpus is a sparse partial clone: only *.qhelp is on disk; the referenced <sample src="..."> code
files live in git and are read on demand with `git show HEAD:<path>` (blob:none partial clone fetches
one blob). Includes (<include src="X.inc.qhelp">) are resolved recursively; a <sample src> resolves
relative to the file that PHYSICALLY contains the tag (so an included .inc's samples resolve to the
.inc's own dir). corpus == llm_input so the verbatim code + prose quote both ground against it.

usage:  DEEPSEEK_API_KEY=$(cat /c/projects/api/deepseek.txt) python codeql_mine.py [--n N] [--lang js,py] [--offset K]
out:    experts/appsec/facts/codeql.jsonl (+ codeql.rejects.jsonl)
"""
import os, re, sys, glob, subprocess, xml.etree.ElementTree as ET
import appsec_core as C

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", "appsec-corpus", "codeql"))
LICENSE_NOTE = "CodeQL queries, MIT (github/codeql)"

LANG = {"javascript":"js","python":"py","csharp":"cs","ruby":"rb","cpp":"cpp","java":"java",
        "go":"go","rust":"rs","swift":"swift","kotlin":"kt"}

# CWE number -> door (deterministic, matches appsec_mine.DOOR_MAP so CodeQL + CWE share gate tokens)
DOOR_MAP = {c:d for d,cs in {
  "injection":[89,78,77,88,94,95,96,90,91,643,611,917,943,1236,113,116,74,75,1427,79,80,83,87,116,117,807,352],
  "memory-safety":[787,125,416,476,190,191,119,120,121,122,124,126,127,131,134,170,415,401,457,562,197,681,469,129,20,193,788,805,764,674,193],
  "crypto":[327,328,916,326,330,338,335,759,760,347,319,311,312,313,322,323,324,325,329,331,336,337,340,547,780,295,760],
  "auth-session":[287,306,288,302,307,384,613,620,640,259,565,521,285,862,863,269,266,273,384,639,798],
  "web-appsec":[601,434,614,1004,732,276,538,548,22,23,36,73,98,444,1021,1275,79,776,377],
  "deserialization-input":[502,470,915,913,1284],
  "secrets-config":[522,321,489,1188,15,526,532,209,200,359,377],
  "network-security":[918,523,346],
  "concurrency-race":[362,367,364,366,764],
  "api-supply-chain":[494,829,345,353,354,830,400,770,772,1333,834,405,409],
}.items() for c in cs}

def lt(e): return e.tag.split('}')[-1]

def gitshow(gitpath):
    try:
        return subprocess.run(["git","show",f"HEAD:{gitpath}"], cwd=ROOT,
            capture_output=True, text=True, encoding="utf-8", timeout=60).stdout
    except Exception:
        return None

def read_source(abspath):
    """Read a file: from disk if present (qhelp/.inc are checked out), else from git (code samples)."""
    if os.path.exists(abspath):
        try: return open(abspath, encoding="utf-8").read()
        except Exception: pass
    gitpath = os.path.relpath(abspath, ROOT).replace(os.sep, "/")
    return gitshow(gitpath)

def parse_xml(text):
    if not text: return None
    text = re.sub(r'<!DOCTYPE[^>]*(?:\[[^\]]*\])?>', '', text, flags=re.S)  # drop DOCTYPE (external dtd)
    try:
        return ET.fromstring(text)
    except ET.ParseError:
        return None

def prose_of(e):
    return ' '.join(''.join(e.itertext()).split())

def blocks_from(abspath, seen_inc):
    """Return ordered list of blocks: ('prose', txt) | ('code', label, lang, code). Resolves includes;
    samples resolve relative to `abspath`'s dir."""
    text = read_source(abspath)
    root = parse_xml(text)
    if root is None: return []
    d = os.path.dirname(abspath)
    out = []
    def walk(el):
        tag = lt(el)
        if tag == "include":
            src = el.get("src")
            if src:
                inc = os.path.normpath(os.path.join(d, src))
                if inc not in seen_inc:
                    seen_inc.add(inc)
                    out.extend(blocks_from(inc, seen_inc))
            return
        if tag == "sample":
            src = el.get("src")
            if src:
                sp = os.path.normpath(os.path.join(d, src))
                code = read_source(sp)
                if code and code.strip():
                    lang = LANG.get("", "") or os.path.splitext(src)[1].lstrip(".")
                    out.append(("code", os.path.basename(src), lang, code.rstrip()))
            else:
                code = ''.join(el.itertext())
                if code and code.strip():
                    out.append(("code", "inline", el.get("language") or "text", code.strip("\n")))
            return
        if tag in ("overview","recommendation"):
            txt = prose_of(el)
            if txt: out.append(("prose", f"{tag.upper()}: {txt}"))
            return
        if tag == "example":
            # walk children in order: interleaved <p> prose and <sample> code
            for ch in el:
                if lt(ch) == "sample": walk(ch)
                elif lt(ch) == "include": walk(ch)
                else:
                    txt = prose_of(ch)
                    if txt: out.append(("prose", txt))
            return
        if tag in ("qhelp","fragment"):
            for ch in el: walk(ch)
            return
        # top-level stray p etc
        if tag == "p":
            txt = prose_of(el)
            if txt: out.append(("prose", txt))
    walk(root)
    return out

def ext_lang(blocks):
    for b in blocks:
        if b[0] == "code":
            e = (b[2] or "").lower()
            m = {"js":"javascript","py":"python","rb":"ruby","cs":"csharp","cpp":"cpp","c":"c",
                 "java":"java","go":"go","rs":"rust","erb":"html","html":"html","xml":"xml"}
            return m.get(e, e)
    return "text"

def build_item(qpath):
    blocks = blocks_from(qpath, set())
    proses = [b[1] for b in blocks if b[0]=="prose"]
    codes  = [b for b in blocks if b[0]=="code"]
    if not proses and not codes: return None
    if sum(len(p) for p in proses) < 40 and not codes: return None  # references-only fragment
    # path -> lang, cwe, query name, source label
    rel = os.path.relpath(qpath, ROOT).replace(os.sep, "/")
    top = rel.split("/")[0]
    lang = LANG.get(top, top)
    m = re.search(r'CWE[-/]?(\d+)', rel)
    cwe = int(m.group(1)) if m else None
    qname = re.sub(r'(?<!^)(?=[A-Z])', '-', os.path.splitext(os.path.basename(qpath))[0]).lower()
    qname = re.sub(r'\.inc$', '', qname)
    source = f"CodeQL {lang}/{qname}"
    lib = f"cwe-{cwe:03d}" if cwe else f"codeql-{qname}"
    door = DOOR_MAP.get(cwe) if cwe else None
    # assemble llm_input (== corpus). code blocks raw & labeled (filename hints bad/good).
    L = [f"CodeQL security query: {source}" + (f" (CWE-{cwe})" if cwe else ""), ""]
    L += proses
    for _, label, clang, code in codes:
        L += ["", f"CODE SAMPLE [{label}] (language={clang or 'text'}):", code]
    text = "\n".join(L)
    return {"llm_input": text, "corpus": text, "source": source, "license_note": LICENSE_NOTE,
            "lib": lib, "version": "codeql", "door": door, "_lang": lang, "_ncode": len(codes)}

def collect(langs=None, n=None, offset=0):
    files = [f for f in glob.glob(os.path.join(ROOT, "**", "*.qhelp"), recursive=True)
             if re.search(r'[/\\][Ss]ecurity', f.replace("\\","/"))]
    # skip pure .inc fragments that exist only to be included by a sibling top-level query with the
    # same stem (avoid processing the include twice); keep an .inc only if no sibling .qhelp includes it
    files = sorted(files)
    if langs:
        files = [f for f in files if os.path.relpath(f, ROOT).replace("\\","/").split("/")[0] in
                 {k for k,v in LANG.items() if v in langs} | set(langs)]
    items, seen_hash = [], set()
    for f in files:
        it = build_item(f)
        if not it: continue
        h = hash(it["corpus"])
        if h in seen_hash: continue    # identical resolved content (top-level stub == its .inc) -> once
        seen_hash.add(h)
        items.append(it)
    items = items[offset:]
    if n: items = items[:n]
    return items

def main():
    langs = None
    if "--lang" in sys.argv: langs = set(sys.argv[sys.argv.index("--lang")+1].split(","))
    n = int(sys.argv[sys.argv.index("--n")+1]) if "--n" in sys.argv else None
    offset = int(sys.argv[sys.argv.index("--offset")+1]) if "--offset" in sys.argv else 0
    dry = "--dry" in sys.argv
    items = collect(langs, n, offset)
    from collections import Counter
    print(f"collected {len(items)} items | langs={Counter(it['_lang'] for it in items)} | "
          f"with-code={sum(1 for it in items if it['_ncode'])}")
    if dry:
        for it in items[:6]:
            print("\n" + "="*80 + f"\n{it['source']}  door={it['door']} lib={it['lib']} ncode={it['_ncode']}")
            print(it["llm_input"][:1500])
        return
    for it in items:  # strip helper keys the pipeline doesn't expect
        it.pop("_lang", None); it.pop("_ncode", None)
    C.run(items, os.path.join(HERE,"experts","appsec","facts","codeql"), id_prefix="cq")

if __name__ == "__main__":
    main()
