#!/usr/bin/env python3
"""stress.py - engine-level cost of each design, measured in REAL minja.

Compares templates head to head on the same server harness:
  * the old scanner (baked_pythondata_v3.jinja, 2,560 facts - now in archive/)
  * D6 inverted index (d6.jinja, same 2,560 facts)
  * a trivial template (isolates llama-server /apply-template overhead)

Reports per-request render time (the tax every message pays), for a matched
question, a no-match question, and a long question.

usage: python stress.py
"""
import glob, json, os, subprocess, sys, time, urllib.request

SRV = r"C:\Users\mhnda\.lmstudio\extensions\backends\llama.cpp-win-x86_64-vulkan-avx2-2.24.0\llama-server.exe"
MODEL = glob.glob(r"C:\Users\mhnda\.lmstudio\models\**\*Qwen3-0.6B*.gguf", recursive=True)[0]
PORT = 8131

QUESTIONS = [
    ("no-match ", "write a haiku about the sea"),
    ("matched  ", "my polars melt code stopped working after upgrading, fix it"),
    ("long      ", "I have a big data pipeline in polars 1.x reading parquet files "
                   "and I need to reshape a wide DataFrame into long format, then "
                   "group by a key and aggregate, and finally write it back out; "
                   "my melt call stopped working after upgrading, please fix it"),
]
REPS = 5


def serve(tpl_path):
    p = subprocess.Popen([SRV, "-m", MODEL, "--chat-template-file", os.path.abspath(tpl_path),
                          "--port", str(PORT), "--host", "127.0.0.1", "-ngl", "0", "-c", "256"],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(80):
        time.sleep(0.5)
        try:
            urllib.request.urlopen(f"http://127.0.0.1:{PORT}/health", timeout=2)
            return p
        except Exception:
            pass
    p.kill()
    return None


def timeit(q):
    body = json.dumps({"messages": [{"role": "user", "content": q}]}).encode()
    ts = []
    for _ in range(REPS):
        req = urllib.request.Request(f"http://127.0.0.1:{PORT}/apply-template", data=body,
                                     headers={"Content-Type": "application/json"})
        t0 = time.perf_counter()
        try:
            urllib.request.urlopen(req, timeout=120).read()
        except Exception as e:
            return None
        ts.append((time.perf_counter() - t0) * 1000)
    ts.sort()
    return ts[len(ts) // 2]          # median


def main():
    open("_trivial.jinja", "w", encoding="utf-8").write(
        "{% for m in messages %}{{ m['content'] }}{% endfor %}")
    targets = [
        ("baseline (no bank)", "_trivial.jinja"),
        ("D1 scanner (archived)", "../../../archive/template-brain/superseded-2026-07-14/baked_pythondata_v3.jinja"),
        ("D6 index (dict facts)", "d6.jinja"),
        ("D7 index (list facts)", "d7.jinja"),
    ]
    rows = []
    for name, path in targets:
        kb = os.path.getsize(path) / 1024
        p = serve(path)
        if not p:
            print(f"{name}: server failed"); continue
        try:
            res = {label: timeit(q) for label, q in QUESTIONS}
        finally:
            p.terminate()
            try: p.wait(timeout=10)
            except Exception: p.kill()
        rows.append((name, kb, res))
        print(f"  measured {name}")

    print(f"\n{'design':22} {'template':>10} " +
          " ".join(f"{lbl.strip():>11}" for lbl, _ in QUESTIONS))
    print("-" * 70)
    for name, kb, res in rows:
        cells = " ".join(f"{(str(round(res[l]))+' ms') if res[l] else 'ERR':>11}"
                         for l, _ in QUESTIONS)
        print(f"{name:22} {kb:8.0f}KB {cells}")
    print("\n(median of 5, llama-server /apply-template, CPU; includes HTTP + "
          "template parse + render. The delta vs baseline IS the bank's tax.)")


if __name__ == "__main__":
    main()
