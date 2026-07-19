#!/usr/bin/env python3
"""run.py - drive the whole chain on one source: extract -> repair -> check.

  extract.py  LLM fills a strict schema (function-calling); code derives type + from_fact
  repair.py   snaps any un-verbatim quote to the real source line (checker, no LLM)
  check.py    raw checker; the quote-anchor is the final gate

usage: DEEPSEEK_API_KEY=... python run.py <source> <lib> <version>
final facts: <lib>.facts.repaired.kept.jsonl
"""
import subprocess, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
if len(sys.argv) < 3:
    sys.exit("usage: python run.py <source> <lib> [version]")
SRC, LIB = sys.argv[1], sys.argv[2]
VER = sys.argv[3] if len(sys.argv) > 3 else "x"
py = sys.executable

def step(name, *args):
    print(f"\n===== {name} =====")
    r = subprocess.run([py, os.path.join(HERE, name), *args])
    if r.returncode != 0: sys.exit(f"{name} failed ({r.returncode})")

step("extract.py", SRC, LIB, VER)                       # -> <lib>.facts.jsonl
step("repair.py", f"{LIB}.facts.jsonl", SRC)            # -> <lib>.facts.repaired.jsonl
step("check.py", f"{LIB}.facts.repaired.jsonl", SRC)    # -> <lib>.facts.repaired.kept.jsonl / .rejects
print(f"\nDONE. final verified facts -> {LIB}.facts.repaired.kept.jsonl")
