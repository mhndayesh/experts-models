#!/usr/bin/env python3
"""make_base_qwen3.py - build family_bases/qwen3.jinja = qwen3 source
template + the 5 anchors inserted INLINE (zero extra bytes), then verify
the bake guard invariant: base with anchors stripped == source, byte-exact.

The source is the template EMBEDDED IN THE SHIPPED GGUF
(Qwen3-0.6B-Q8_0.gguf), NOT the HF tokenizer_config.json one - they
differ (kept as qwen3.source.hf.jinja for reference). Anchor spots (see
inserts/qwen3/*.jinja headers for the why):
  FB_PRELOOP  very top, before the tools/system block
  FB_SYS      after the source's system if/else, before its own ns set
  FB_USER     AFTER the user/system render expression (notes = own turn)
  FB_HOOK     top of the per-tool-call loop body (before normalization)
  FB_TOOLMSG  before the tool branch's raw content render (empty-bounce
              contract suppresses the echo; see harness.py)
"""
import hashlib, sys

SRC = "family_bases/qwen3.source.jinja"
DST = "family_bases/qwen3.jinja"

SPOTS = [  # (unique existing text, anchor, before/after)
    ("{%- set ns = namespace(multi_step_tool=true", "{#FB_SYS#}", "before"),
    ("{{- '<|im_start|>' + message.role + '\\n' + message.content + '<|im_end|>' + '\\n' }}",
     "{#FB_USER#}", "after"),
    ("{%- for tool_call in message.tool_calls %}", "{#FB_HOOK#}", "after"),
    ("{{- message.content }}", "{#FB_TOOLMSG#}", "before"),
]

def main():
    src = open(SRC, encoding="utf-8", newline="").read()
    out = "{#FB_PRELOOP#}" + src
    for text, anchor, where in SPOTS:
        n = out.count(text)
        assert n == 1, f"spot not unique ({n}x): {text[:60]!r}"
        out = out.replace(text, anchor + text if where == "before" else text + anchor, 1)
    stripped = out
    for a in ("{#FB_PRELOOP#}", "{#FB_SYS#}", "{#FB_USER#}", "{#FB_HOOK#}", "{#FB_TOOLMSG#}"):
        assert out.count(a) == 1, f"anchor {a} not exactly once"
        stripped = stripped.replace(a, "", 1)
    assert hashlib.sha256(stripped.encode()).hexdigest() == \
           hashlib.sha256(src.encode()).hexdigest(), "byte-exact guard failed"
    open(DST, "w", encoding="utf-8", newline="").write(out)
    print(f"wrote {DST} ({len(out)} chars); base-minus-anchors == source: OK")

if __name__ == "__main__":
    main()
