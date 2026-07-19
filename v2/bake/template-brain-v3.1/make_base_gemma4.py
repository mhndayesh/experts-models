#!/usr/bin/env python3
"""make_base_gemma4.py - build family_bases/gemma4.jinja = the template
extracted from the shipped gemma-4-12B-it-QAT-Q4_0.gguf + the 5 anchors
inserted INLINE (zero extra bytes), then verify base-minus-anchors ==
source byte-exact. Anchor spots (see inserts/gemma4/*.jinja for the why):
  FB_PRELOOP  very top, before the macros
  FB_SYS      after the source's system-block endif (own <|turn>system)
  FB_USER     after {{- captured_content -}}, still inside the open turn
  FB_HOOK     top of the per-tool-call loop body
  FB_TOOLMSG  after the forward-scan's tool_body set (rebind trick)
"""
import hashlib

SRC = "family_bases/gemma4.source.jinja"
DST = "family_bases/gemma4.jinja"

SPOTS = [  # (unique existing text, anchor, before/after)
    ("    {{- '<turn|>\\n' -}}\n{%- endif %}", "{#FB_SYS#}", "after"),
    ("{{- captured_content -}}", "{#FB_USER#}", "after"),
    ("{%- for tool_call in message['tool_calls'] -%}", "{#FB_HOOK#}", "after"),
    ("{%- set tool_body = follow.get('content') -%}", "{#FB_TOOLMSG#}", "after"),
    # v3.2.3 default-native lane: INSIDE the message loop, immediately
    # BEFORE the turn header renders - the insert guards itself to fire
    # only for the LAST user message. LM Studio's undocumented layer
    # echoed the forge whenever it rendered after the final user text
    # (measured live twice, 2026-07-13; two candidate mechanisms, both
    # satisfied by this placement: the forge is in both boundary renders
    # AND upstream of the last-user-text split point).
    ("{%- if not continue_same_model_turn -%}", "{#FB_GEN#}", "before"),
]

def main():
    src = open(SRC, encoding="utf-8", newline="").read()
    out = "{#FB_PRELOOP#}" + src
    for text, anchor, where in SPOTS:
        n = out.count(text)
        assert n == 1, f"spot not unique ({n}x): {text[:60]!r}"
        out = out.replace(text, anchor + text if where == "before" else text + anchor, 1)
    stripped = out
    for a in ("{#FB_PRELOOP#}", "{#FB_SYS#}", "{#FB_USER#}", "{#FB_HOOK#}",
              "{#FB_TOOLMSG#}", "{#FB_GEN#}"):
        assert out.count(a) == 1, f"anchor {a} not exactly once"
        stripped = stripped.replace(a, "", 1)
    assert hashlib.sha256(stripped.encode()).hexdigest() == \
           hashlib.sha256(src.encode()).hexdigest(), "byte-exact guard failed"
    open(DST, "w", encoding="utf-8", newline="").write(out)
    print(f"wrote {DST} ({len(out)} chars); base-minus-anchors == source: OK")

if __name__ == "__main__":
    main()
