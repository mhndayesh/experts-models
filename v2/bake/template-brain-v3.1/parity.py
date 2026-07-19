#!/usr/bin/env python3
"""parity.py - jinja2 and minja MUST retrieve identically. Prove it.

Why this exists (F-050): the two engines are NOT the same language.
  * minja's `.split()` does NOT collapse whitespace (Python's does), so empty
    tokens leak into term lists and create junk bigrams.
  * `d[x | int]` - filter-vs-subscript precedence differs.
Both hazards silently changed WHICH FACTS WERE RETRIEVED in the shipped model
(minja injected 1 fact where jinja2 injected 5). Every offline gate in this
repo renders with jinja2, so without this test the offline result is a
statement about a language we do not ship.

Rule: bake nothing until parity is 100%.

usage: python parity.py [template.jinja]
"""
import glob, json, os, subprocess, sys, time, urllib.request

import jinja2

SRV = r"C:\Users\mhnda\.lmstudio\extensions\backends\llama.cpp-win-x86_64-vulkan-avx2-2.24.0\llama-server.exe"
MODEL = glob.glob(r"C:\Users\mhnda\.lmstudio\models\**\*Qwen3-0.6B*.gguf", recursive=True)[0]
PORT = 8191
FORGE = "<|tool_call>call:factbank_search"


def facts_of(prompt):
    if FORGE not in prompt:
        return []
    block = prompt.split(FORGE, 1)[1].split("<turn|>", 1)[0]
    return [l.strip()[2:82] for l in block.splitlines() if l.strip().startswith("- ")]


def render_jinja2(tpl, q):
    t = jinja2.Environment(undefined=jinja2.Undefined).from_string(tpl)
    return facts_of(t.render(messages=[{"role": "user", "content": q}], tools=None,
                             add_generation_prompt=True, bos_token=""))


def render_minja(path, questions):
    p = subprocess.Popen([SRV, "-m", MODEL, "--chat-template-file", os.path.abspath(path),
                          "--port", str(PORT), "--host", "127.0.0.1", "-ngl", "0", "-c", "512"],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        for _ in range(80):
            time.sleep(0.5)
            try:
                urllib.request.urlopen(f"http://127.0.0.1:{PORT}/health", timeout=2)
                break
            except Exception:
                pass
        else:
            return None
        out = []
        for q in questions:
            body = json.dumps({"messages": [{"role": "user", "content": q}]}).encode()
            req = urllib.request.Request(f"http://127.0.0.1:{PORT}/apply-template", data=body,
                                         headers={"Content-Type": "application/json"})
            r = json.loads(urllib.request.urlopen(req, timeout=90).read())
            out.append(facts_of(r.get("prompt", "")))
        return out
    finally:
        p.terminate()
        try: p.wait(timeout=10)
        except Exception: p.kill()


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "baked_index_v6.jinja"
    tpl = open(path, encoding="utf-8").read()
    gold = json.load(open("jinja_lab/gold.json", encoding="utf-8"))
    qs = [c["q"] for c in gold["cases"]] + gold["controls"]

    mj = render_minja(path, qs)
    if mj is None:
        sys.exit("minja server never came up")

    bad = 0
    for q, m in zip(qs, mj):
        j = render_jinja2(tpl, q)
        if j != m:
            bad += 1
            print(f"  MISMATCH  {q[:52]}")
            print(f"     jinja2 ({len(j)}): {[x[:34] for x in j]}")
            print(f"     minja  ({len(m)}): {[x[:34] for x in m]}")
    print(f"\nparity: {len(qs)-bad}/{len(qs)} questions identical in both engines")
    if bad:
        sys.exit(f"PARITY BROKEN on {bad} question(s) - do NOT bake")
    print("OK - the template means the same thing in both engines")


if __name__ == "__main__":
    main()
