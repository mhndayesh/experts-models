#!/usr/bin/env python3
"""Bake the 12b/26b appsec template into copies of the QAT base GGUFs, and write the canary'd
ship template. CPU/disk only (write_baked copies tensors, sets chat_template + factbank.*)."""
import sys, os
BAKE = r"c:\projects\LLM BANK\v2\bake\template-brain-v3.1"
sys.path.insert(0, BAKE)
from bake_template_v3 import write_baked

TPL_SRC = os.path.join(BAKE, "appsec_v3_baked_gemma4.jinja")
BANK = os.path.join(BAKE, "appsec_v3_bank.jsonl")
CANARY = "FB_CANARY_APPSEC_GEMMA4_V3"
SCRATCH = r"C:\Users\mhnda\AppData\Local\Temp\claude\c--projects-LLM-BANK\8fa4c881-e73f-4318-8c6d-c5d450a53c5e\scratchpad"
PUB = r"c:\projects\LLM BANK\v2\publish\security-appsec"

# normalize newlines + prepend canary -> the ONE ship template both 12b and 26b use
tpl = open(TPL_SRC, encoding="utf-8").read().replace("\r\n", "\n")
if CANARY not in tpl:
    tpl = "{# " + CANARY + " #}\n" + tpl
bank = open(BANK, encoding="utf-8").read()
assert CANARY in tpl
print(f"ship template {len(tpl.encode()):,} B, canary={CANARY}")

SIZES = {
    "12B": (r"C:\Users\mhnda\.lmstudio\models\lmstudio-community\gemma-4-12B-it-QAT-GGUF\gemma-4-12B-it-QAT-Q4_0.gguf",
            "gemma-4-12B-security-expert-Q4_0.gguf"),
    "26B-A4B": (r"C:\Users\mhnda\.lmstudio\models\lmstudio-community\gemma-4-26B-A4B-it-QAT-GGUF\gemma-4-26B-A4B-it-QAT-Q4_0.gguf",
                "gemma-4-26B-A4B-security-expert-Q4_0.gguf"),
}
# write the shared ship template into each GGUF-repo publish folder
for size, (src, dstname) in SIZES.items():
    repo = f"gemma-4-{size}-security-expert-GGUF"
    d = os.path.join(PUB, repo)
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "chat-template.jinja"), "w", encoding="utf-8", newline="\n").write(tpl)
    dst = os.path.join(SCRATCH, dstname)
    print(f"baking {size} -> {dst}", flush=True)
    r = write_baked(src, dst, tpl, bank, version="0.4.0")
    print(f"  {size}:", r)
print("DONE")
