#!/usr/bin/env python3
"""Bake all 6 security-expert GGUFs: {e2b,12b,26b} x {thinking-off, thinking-on}."""
import sys, os
BAKE = r"c:\projects\LLM BANK\v2\bake\template-brain-v3.1"
sys.path.insert(0, BAKE)
from bake_template_v3 import write_baked
SCR = r"C:\Users\mhnda\AppData\Local\Temp\claude\c--projects-LLM-BANK\8fa4c881-e73f-4318-8c6d-c5d450a53c5e\scratchpad"
LM = r"C:\Users\mhnda\.lmstudio\models\lmstudio-community"
bank = open(os.path.join(BAKE, "appsec_v3_bank.jsonl"), encoding="utf-8").read()

def tpl(name, canary):
    t = open(os.path.join(BAKE, name), encoding="utf-8").read().replace("\r\n", "\n")
    if canary not in t: t = "{# " + canary + " #}\n" + t
    return t

E, G = "FB_CANARY_APPSEC_E2B_V3", "FB_CANARY_APPSEC_GEMMA4_V3"
JOBS = [
    ("appsec_v3_baked_e2b_off.jinja",   E, rf"{LM}\gemma-4-E2B-it-GGUF\gemma-4-E2B-it-Q4_K_M.gguf",              "gemma-4-E2B-security-expert-Q4_K_M.gguf"),
    ("appsec_v3_baked_e2b_think.jinja", E, rf"{LM}\gemma-4-E2B-it-GGUF\gemma-4-E2B-it-Q4_K_M.gguf",              "gemma-4-E2B-security-expert-thinking-Q4_K_M.gguf"),
    ("appsec_v3_baked_gemma4_off.jinja",   G, rf"{LM}\gemma-4-12B-it-QAT-GGUF\gemma-4-12B-it-QAT-Q4_0.gguf",     "gemma-4-12B-security-expert-Q4_0.gguf"),
    ("appsec_v3_baked_gemma4_think.jinja", G, rf"{LM}\gemma-4-12B-it-QAT-GGUF\gemma-4-12B-it-QAT-Q4_0.gguf",     "gemma-4-12B-security-expert-thinking-Q4_0.gguf"),
    ("appsec_v3_baked_gemma4_off.jinja",   G, rf"{LM}\gemma-4-26B-A4B-it-QAT-GGUF\gemma-4-26B-A4B-it-QAT-Q4_0.gguf", "gemma-4-26B-A4B-security-expert-Q4_0.gguf"),
    ("appsec_v3_baked_gemma4_think.jinja", G, rf"{LM}\gemma-4-26B-A4B-it-QAT-GGUF\gemma-4-26B-A4B-it-QAT-Q4_0.gguf", "gemma-4-26B-A4B-security-expert-thinking-Q4_0.gguf"),
]
for tname, canary, src, dstname in JOBS:
    dst = os.path.join(SCR, dstname)
    t = tpl(tname, canary)
    print(f"baking {dstname} <- {tname}", flush=True)
    r = write_baked(src, dst, t, bank, version="0.4.0")
    print(f"   template {r['template_chars']:,} chars, out {r['out_bytes']:,} B")
print("ALL 6 BAKED")
