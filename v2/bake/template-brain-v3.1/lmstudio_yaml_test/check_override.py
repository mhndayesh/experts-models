#!/usr/bin/env python3
"""check_override.py - prove or FALSIFY the model.yaml prompt-template workaround.

Run this AFTER LM Studio has loaded a test model. It reads nothing but the truth:
the actual llama-server process LM Studio spawned, and the actual template file it
was handed.

What it asserts (the handoff's integrity checks 1-7, plus the cache check):
  1. find LM Studio's llama-server process
  2. extract its --chat-template-file path
  3. hash that temp file
  4. it must EQUAL the oversized template we published in model.yaml
  5. it must be > 1 MiB   (i.e. the metadata cap was bypassed)
  6. it must NOT be the 48-char sentinel
  7. the size canary must be present
  8. the GGUF metadata cache should STILL show the safe embedded template
     (the max template is expected in the load-time temp file, not in the cache)

usage: python check_override.py --expect fb_1500kb.jinja [--canary FB_CANARY_1500KB]
"""
import argparse, glob, hashlib, json, os, re, subprocess, sys

SENTINEL = "[LM Studio Patch - String too long; didn" + chr(39) + "t read]"
CACHE = os.path.expanduser(r"~\.lmstudio\.internal\gguf-metadata-cache.json")


def md5(b):
    return hashlib.md5(b).hexdigest()


def sha256(b):
    return hashlib.sha256(b).hexdigest()


def llama_server_cmdlines():
    """Every running llama-server and its command line (Windows, via CIM)."""
    ps = ("Get-CimInstance Win32_Process -Filter \"Name='llama-server.exe'\" | "
          "Select-Object -ExpandProperty CommandLine")
    out = subprocess.run(["powershell", "-NoProfile", "-Command", ps],
                         capture_output=True, text=True).stdout
    return [l.strip() for l in out.splitlines() if l.strip()]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--expect", required=True, help="the oversized template we put in model.yaml")
    ap.add_argument("--canary", default=None, help="defaults to FB_CANARY_<NNNN>KB from --expect")
    a = ap.parse_args()

    want = open(a.expect, encoding="utf-8").read()
    canary = a.canary
    if not canary:
        m = re.search(r"FB_CANARY_\w+", want)
        canary = m.group(0) if m else None

    fails = []
    print(f"expected template : {a.expect}  ({len(want.encode()):,} bytes, canary={canary})")

    cmds = llama_server_cmdlines()
    if not cmds:
        sys.exit("FAIL: no llama-server process. Is the model loaded in LM Studio?")
    print(f"llama-server procs: {len(cmds)}")

    proven = False
    for c in cmds:
        m = re.search(r"--chat-template-file\s+(\S+(?:\\[^\\]+)*chat-template\.jinja)", c)
        if not m:
            m = re.search(r"--chat-template-file\s+(.+?\.jinja)", c)
        model = re.search(r"--model\s+(\S+\.gguf)", c)
        print(f"\n  model : {os.path.basename(model.group(1)) if model else '?'}")
        if not m:
            print("  FAIL: this process got NO --chat-template-file "
                  "(LM Studio did not hand a template file to the engine)")
            fails.append("no --chat-template-file")
            continue
        tf = m.group(1)
        print(f"  temp  : {tf}")
        if not os.path.exists(tf):
            print("  FAIL: temp template file does not exist")
            fails.append("temp file missing")
            continue
        got = open(tf, encoding="utf-8").read()
        n = len(got.encode())
        print(f"  bytes : {n:,}")

        checks = [
            ("is NOT the sentinel",            SENTINEL not in got),
            ("is larger than 1 MiB",           n > 1024 * 1024),
            ("carries the canary",             bool(canary) and canary in got),
            # A YAML block scalar always appends ONE trailing newline, so the applied
            # template is published + a newline. Compare CONTENT, not raw bytes, or
            # this check cries wolf on a 1-byte difference that means nothing.
            ("SHA-256 == published template (modulo YAML's trailing newline)",
             sha256(got.rstrip().encode()) == sha256(want.rstrip().encode())),
        ]
        for label, ok in checks:
            print(f"    [{'PASS' if ok else 'FAIL'}] {label}")
            if not ok:
                fails.append(label)
        if all(ok for _, ok in checks):
            proven = True

    # 8. the GGUF metadata cache should still hold the SAFE embedded template
    if os.path.exists(CACHE):
        try:
            d = json.load(open(CACHE, encoding="utf-8"))
            rows = []
            for k, v in d["json"]["map"]:
                ct = (v.get("metadata") or {}).get("chatTemplate")
                if ct and "factbank" in str(k).lower():
                    rows.append((os.path.basename(str(k)), len(ct), SENTINEL in ct))
            print("\nGGUF metadata cache (should show the SAFE embedded template, not the max):")
            for name, ln, sent in rows:
                print(f"  {ln:>9,} chars {'<-- SENTINEL' if sent else ''}  {name[:58]}")
        except Exception as e:
            print(f"\n(cache read failed: {e})")

    print("\n" + "=" * 62)
    if proven and not fails:
        print("WORKAROUND PROVEN: LM Studio applied an OVER-1-MiB template from model.yaml.")
    else:
        print("WORKAROUND NOT PROVEN. Failures: " + ", ".join(sorted(set(fails))))
        print("If the temp file is the SAFE template, the override was ignored ->\n"
              "  the model.yaml route does not bypass the cap (fall back to the .bat / lite edition).")
    print("=" * 62)


if __name__ == "__main__":
    main()
