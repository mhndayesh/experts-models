#!/usr/bin/env python3
"""appsec_mastg.py - ADAPTER: OWASP MASTG (Mobile App Security Testing Guide) -> insecure-by-default
landmine facts for a MOBILE code-gen model (Android Kotlin/Java, iOS Swift/Obj-C).

Thin adapter over the shared pipeline (appsec_core). It:
  - walks the code-rich MASTG dirs (demos/, best-practices/, tests/),
  - RESOLVES `{{ file }}` transclusions by inlining the referenced SOURCE file as a fenced block so the
    exact mobile code lands VERBATIM in the grounding corpus (code is ground truth; never rewritten),
  - forces a retrieval door from the MASVS category on the path (CRYPTO->crypto, NETWORK->network-security,
    STORAGE->secrets-config, AUTH->auth-session, PLATFORM->web-appsec), leaving CODE/RESILIENCE/PRIVACY
    to the LLM,
  - drops pure-methodology files (no real mobile source code).

usage: DEEPSEEK_API_KEY=$(cat /c/projects/api/deepseek.txt) python appsec_mastg.py [--n N] [--list]
out:   experts/appsec/facts/mastg.jsonl (+ mastg.rejects.jsonl)
"""
import os, re, sys, glob
import appsec_core as C

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "appsec-corpus", "owasp-mastg"))
OUT  = "experts/appsec/facts/mastg"
LICENSE_NOTE = "OWASP MASTG, CC BY-SA"

# directories that actually carry concrete insecure/secure mobile code (skip pure prose/methodology trees)
SCAN_DIRS = ["demos/android", "demos/ios", "best-practices", "tests/android", "tests/ios",
             "tests-beta/android", "tests-beta/ios"]

# source-code extensions we inline VERBATIM (skip run.sh / output.txt / *.yml / *.r2 / *.asm noise)
LANG = {".kt":"kotlin", ".java":"java", ".swift":"swift", ".m":"objectivec", ".mm":"objectivec",
        ".h":"objectivec", ".xml":"xml", ".gradle":"groovy", ".plist":"xml", ".c":"c", ".cpp":"cpp"}

# MASVS category on the path -> forced retrieval door (only the unambiguous ones)
MASVS_DOOR = {"crypto":"crypto", "network":"network-security", "storage":"secrets-config",
              "auth":"auth-session", "platform":"web-appsec", "privacy":"secrets-config"}

TRANSCLUDE = re.compile(r"\{\{\s*(.+?)\s*\}\}")

def frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    meta = {}
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1); meta[k.strip()] = v.strip()
        text = text[m.end():]
    return meta, text

def fence_for(path):
    ext = os.path.splitext(path)[1].lower()
    if ext not in LANG: return None
    try:
        body = open(path, encoding="utf-8", errors="replace").read().strip()
    except OSError:
        return None
    if len(body) < 12: return None
    return f"```{LANG[ext]}\n{body}\n```"

def resolve(text, base):
    """Inline every {{ src.kt # other.java }} transclusion as fenced code; drop non-source transclusions."""
    def sub(m):
        blocks = []
        for token in m.group(1).split("#"):
            rel = token.strip().split()[0] if token.strip() else ""
            if not rel: continue
            f = fence_for(os.path.normpath(os.path.join(base, rel)))
            if f: blocks.append(f)
        return "\n\n".join(blocks)  # empty string if nothing sourceable -> transclusion drops out
    return TRANSCLUDE.sub(sub, text)

MDLINK = re.compile(r"\[([^\]]+)\]\((?:[^)]*)\)")
def clean_prose(text):
    """Collapse markdown links [txt](url)->txt in PROSE only (leave fenced code blocks verbatim), so the
    verbatim `quote` anchor doesn't drag in a URL. Code fences are ground truth and untouched."""
    out, i = [], 0
    for m in re.finditer(r"```.*?```", text, re.S):
        out.append(MDLINK.sub(r"\1", text[i:m.start()])); out.append(m.group(0)); i = m.end()
    out.append(MDLINK.sub(r"\1", text[i:]))
    return "".join(out)

def area_and_door(path):
    m = re.search(r"MASVS-([A-Z]+)", path)
    area = m.group(1).lower() if m else "code"
    return area, MASVS_DOOR.get(area)  # door None -> let the LLM pick

def has_code(text):
    # at least one fenced block with a mobile/source language and real length
    for m in re.finditer(r"```(\w+)?\n(.*?)```", text, re.S):
        lang = (m.group(1) or "").lower()
        if lang in ("default", "plaintext", "text", "shell", "bash", "yaml", "yml", ""): continue
        if len(m.group(2).strip()) >= 20: return True
    return False

def build_items():
    items = []
    for d in SCAN_DIRS:
        for md in sorted(glob.glob(os.path.join(ROOT, d, "**", "*.md"), recursive=True)):
            raw = open(md, encoding="utf-8", errors="replace").read()
            meta, body = frontmatter(raw)
            resolved = clean_prose(resolve(body, os.path.dirname(md)))
            if not has_code(resolved):
                continue
            mid = meta.get("id") or os.path.splitext(os.path.basename(md))[0]
            platform = (meta.get("platform") or ("android" if "/android" in md.replace("\\","/") else
                        "ios" if "/ios" in md.replace("\\","/") else "mobile")).strip().lower()
            area, door = area_and_door(md)
            title = meta.get("title", "").strip()
            header = f"{mid} [{platform}/MASVS-{area.upper()}]: {title}\n\n"
            corpus = header + resolved
            items.append({
                "llm_input": corpus, "corpus": corpus,
                "source": mid, "license_note": LICENSE_NOTE,
                "lib": f"{platform}-{area}", "version": "mastg",
                **({"door": door} if door else {}),
                "_platform": platform,
            })
    return items

EXTRA_SYS = (
"This source is OWASP MASTG: MOBILE app security (Android Kotlin/Java, iOS Swift/Objective-C). Facts must be "
"MOBILE landmines a code-gen model writes insecurely by default: insecure local storage (SharedPreferences, "
"Keychain, plaintext files), weak/misused crypto & Keystore/Keychain, missing TLS hostname/cert validation & "
"pinning, insecure WebView (JavaScript bridge, file access), exported/insecure IPC components, secrets in "
"logs/config. Prefer the exact mobile API in code_bad (e.g. Random(), SSLSocket, setJavaScriptEnabled, "
"MODE_WORLD_READABLE, kSecAttrKeySizeInBits 1024). Copy mobile code VERBATIM.")

if __name__ == "__main__":
    items = build_items()
    if "--list" in sys.argv:
        from collections import Counter
        print(f"{len(items)} code-bearing items")
        print("platform:", Counter(i["_platform"] for i in items))
        print("door(forced):", Counter(i.get("door","<llm>") for i in items))
        sys.exit()
    if "--n" in sys.argv:
        items = items[:int(sys.argv[sys.argv.index("--n")+1])]
    for it in items: it.pop("_platform", None)
    print(f"MASTG: mining {len(items)} items -> {OUT}.jsonl")
    C.run(items, OUT, extra_sys=EXTRA_SYS, id_prefix="mas")
