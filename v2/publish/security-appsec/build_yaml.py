#!/usr/bin/env python3
"""Build the LM Studio Hub model.yaml for the e2b security expert.

The baked appsec template is 4.18 MB — far over LM Studio's ~980,000-byte raw-GGUF
metadata cap (F-053, silent truncation to a 48-char sentinel). So we ship it the ONLY
way that works for a template this big in LM Studio: the model.yaml route
(`llm.load.promptTemplate`), where LM Studio spawns its own llama-server and hands it the
full template via `--chat-template-file` (no size limit — proven F-059 at 1.5/2.0 MB).

- LOAD-ONLY: only llm.load.promptTemplate is set (SHIPPING.md §4 trap 1: also setting
  llm.prediction.promptTemplate makes every completion 500).
- metadataOverrides is MANDATORY or the model never appears in `lms ls` (§4 trap 2).
- A canary comment is prepended so check_override.py can verify the handoff after a load.
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = r"c:\projects\LLM BANK\v2\bake\template-brain-v3.1\appsec_v3_baked_e2b.jinja"
OUTDIR = os.path.join(HERE, "gemma-4-E2B-security-expert")
SHIP_JINJA = os.path.join(OUTDIR, "chat-template.jinja")   # full template + canary
MODEL_YAML = os.path.join(OUTDIR, "model.yaml")

CANARY = "FB_CANARY_APPSEC_E2B_V3"
os.makedirs(OUTDIR, exist_ok=True)

tpl = open(SRC, encoding="utf-8").read()
if CANARY not in tpl:
    tpl = "{# " + CANARY + " #}\n" + tpl          # a Jinja comment => renders to nothing
open(SHIP_JINJA, "w", encoding="utf-8", newline="\n").write(tpl)
print(f"ship template : {SHIP_JINJA}  ({len(tpl.encode()):,} bytes, canary={CANARY})")

# YAML block scalar: every template line indented 14 spaces under `template: |`
indented = "\n".join(("              " + ln).rstrip() if ln.strip() else "" for ln in tpl.split("\n"))

yaml = f"""model: mhndayesh/gemma-4-e2b-security-expert
base:
  - key: lmstudio-community/gemma-4-E2B-it-GGUF
    sources:
      - type: huggingface
        user: lmstudio-community
        repo: gemma-4-E2B-it-GGUF
config:
  load:
    fields:
      - key: llm.load.promptTemplate
        value:
          type: jinja
          jinjaPromptTemplate:
            template: |
{indented}
metadataOverrides:
  domain: llm
  architectures: [gemma4]
  compatibilityTypes: [gguf]
  paramsStrings: ["4.6B"]
  minMemoryUsageBytes: 4000000000
  contextLengths: [32768]
  vision: true
  reasoning: true
  trainedForToolUse: true
"""
open(MODEL_YAML, "w", encoding="utf-8", newline="\n").write(yaml)
print(f"model.yaml    : {MODEL_YAML}  ({len(yaml.encode()):,} bytes)")
