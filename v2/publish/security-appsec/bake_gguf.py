#!/usr/bin/env python3
"""Embed the full 4.18 MB appsec bank template into a copy of the base e2b GGUF, for the HF
llama.cpp/server route. Uses the proven write_baked() path (GGUFReader -> GGUFWriter,
tensors copied untouched, chat_template + factbank.* metadata set)."""
import sys, os
BAKE = r"c:\projects\LLM BANK\v2\bake\template-brain-v3.1"
sys.path.insert(0, BAKE)
from bake_template_v3 import write_baked

TPL = r"c:\projects\LLM BANK\v2\publish\security-appsec\gemma-4-E2B-security-expert\chat-template.jinja"
BANK = os.path.join(BAKE, "appsec_v3_bank.jsonl")
SRC = r"C:\Users\mhnda\.lmstudio\models\lmstudio-community\gemma-4-E2B-it-GGUF\gemma-4-E2B-it-Q4_K_M.gguf"
DST = r"C:\Users\mhnda\AppData\Local\Temp\claude\c--projects-LLM-BANK\8fa4c881-e73f-4318-8c6d-c5d450a53c5e\scratchpad\gemma-4-E2B-security-expert-Q4_K_M.gguf"

tpl = open(TPL, encoding="utf-8").read()
bank = open(BANK, encoding="utf-8").read()
assert "FB_CANARY_APPSEC_E2B_V3" in tpl, "canary missing from template"
print(f"template {len(tpl.encode()):,} B, bank {len(bank.encode()):,} B")
r = write_baked(SRC, DST, tpl, bank, version="0.4.0")
print("baked:", DST)
print(r)
