#!/usr/bin/env python3
"""Generate the 6 LM Studio Hub model.yaml artifacts (e2b/12b/26b x thinking-off/on) for the
security-expert line. Each model.yaml carries:
  - config.operation.fields: gemma-native sampling baked into the SETTINGS (the 'settings that work')
      temperature 1.0, topKSampling 64, topPSampling {checked,0.95}, minPSampling {checked,0.01}
  - config.load.fields: llm.load.contextLength 32768 (thinking needs the headroom) + llm.load.promptTemplate
  - metadataOverrides (mandatory)
Also writes each variant's canary'd chat-template.jinja into its Hub folder.
"""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
BAKE = r"c:\projects\LLM BANK\v2\bake\template-brain-v3.1"

SIZES = {
    "E2B":     dict(base="gemma-4-E2B-it-GGUF",        params="4.6B", minmem=4000000000,  canary="FB_CANARY_APPSEC_E2B_V3",    off="appsec_v3_baked_e2b_off.jinja",    on="appsec_v3_baked_e2b_think.jinja"),
    "12B":     dict(base="gemma-4-12B-it-QAT-GGUF",    params="12B",  minmem=9000000000,  canary="FB_CANARY_APPSEC_GEMMA4_V3", off="appsec_v3_baked_gemma4_off.jinja", on="appsec_v3_baked_gemma4_think.jinja"),
    "26B-A4B": dict(base="gemma-4-26B-A4B-it-QAT-GGUF",params="26B",  minmem=16000000000, canary="FB_CANARY_APPSEC_GEMMA4_V3", off="appsec_v3_baked_gemma4_off.jinja", on="appsec_v3_baked_gemma4_think.jinja"),
}
CTX = 32768

def emit(size, mode):
    c = SIZES[size]
    tpl_name = c[mode]
    hub = f"gemma-4-{size.lower()}-security-expert" + ("-thinking" if mode == "on" else "")
    folder = f"gemma-4-{size}-security-expert" + ("-thinking" if mode == "on" else "")
    outdir = os.path.join(HERE, folder); os.makedirs(outdir, exist_ok=True)
    t = open(os.path.join(BAKE, tpl_name), encoding="utf-8").read().replace("\r\n", "\n")
    if c["canary"] not in t: t = "{# " + c["canary"] + " #}\n" + t
    open(os.path.join(outdir, "chat-template.jinja"), "w", encoding="utf-8", newline="\n").write(t)
    ind = "\n".join(("              " + ln).rstrip() if ln.strip() else "" for ln in t.split("\n"))
    y = f"""model: mhndayesh/{hub}
base:
  - key: lmstudio-community/{c['base']}
    sources:
      - type: huggingface
        user: lmstudio-community
        repo: {c['base']}
config:
  operation:
    fields:
      - key: llm.prediction.temperature
        value: 1.0
      - key: llm.prediction.topKSampling
        value: 64
      - key: llm.prediction.topPSampling
        value:
          checked: true
          value: 0.95
      - key: llm.prediction.minPSampling
        value:
          checked: true
          value: 0.01
  load:
    fields:
      - key: llm.load.contextLength
        value: {CTX}
      - key: llm.load.promptTemplate
        value:
          type: jinja
          jinjaPromptTemplate:
            template: |
{ind}
metadataOverrides:
  domain: llm
  architectures: [gemma4]
  compatibilityTypes: [gguf]
  paramsStrings: ["{c['params']}"]
  minMemoryUsageBytes: {c['minmem']}
  contextLengths: [{CTX}]
  vision: true
  reasoning: {'true' if mode == 'on' else 'false'}
  trainedForToolUse: true
"""
    open(os.path.join(outdir, "model.yaml"), "w", encoding="utf-8", newline="\n").write(y)
    print(f"{hub}: model.yaml {len(y.encode()):,} B, tpl {len(t.encode()):,} B")

for size in SIZES:
    for mode in ("off", "on"):
        emit(size, mode)
