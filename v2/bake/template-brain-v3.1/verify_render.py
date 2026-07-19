#!/usr/bin/env python3
"""verify_render.py - render a baked chat template across the synthetic inputs
llama.cpp probes at model-load time. If ANY throws, llama.cpp rejects the whole
model, so this must pass BEFORE we write the GGUF (the e2b lesson).

usage: python verify_render.py <baked.jinja>
exit 0 = all inputs render; nonzero = a probe threw (do NOT bake the GGUF).
"""
import sys, json
try:
    from jinja2 import Environment, BaseLoader
    from jinja2.exceptions import TemplateError
except Exception as e:
    sys.exit(f"jinja2 not available: {e}")

src = open(sys.argv[1], encoding="utf-8").read()

# gemma templates call a few methods llama.cpp/minja provide; stub them for jinja2.
def raise_exception(msg): raise RuntimeError(msg)

env = Environment(loader=BaseLoader(), trim_blocks=False, lstrip_blocks=False)
env.globals["raise_exception"] = raise_exception
env.globals["strftime_now"] = lambda fmt: "2026-07-17"
try:
    tpl = env.from_string(src)
except Exception as e:
    sys.exit(f"TEMPLATE PARSE ERROR: {type(e).__name__}: {e}")

TOOLS = [{"type": "function", "function": {"name": "get_weather",
          "description": "get weather", "parameters": {"type": "object",
          "properties": {"city": {"type": "string"}}, "required": ["city"]}}}]

# the probe set llama.cpp uses: empty, system, tools, multimodal content list,
# a tool-call round trip, and our real use (user asking about a landmine lib).
PROBES = {
    "single_user":        dict(messages=[{"role": "user", "content": "How do I use netexec?"}]),
    "system_user":        dict(messages=[{"role": "system", "content": "Be helpful."},
                                         {"role": "user", "content": "capstone v6 arm64?"}]),
    "assistant_turn":     dict(messages=[{"role": "user", "content": "hi"},
                                         {"role": "assistant", "content": "hello"},
                                         {"role": "user", "content": "libbpf map create?"}]),
    "with_tools":         dict(messages=[{"role": "user", "content": "weather in NYC?"}], tools=TOOLS),
    "multimodal_content": dict(messages=[{"role": "user", "content": [
                                {"type": "text", "text": "what is this"},
                                {"type": "image"}]}]),
    "tool_roundtrip":     dict(messages=[{"role": "user", "content": "weather?"},
                                {"role": "assistant", "content": "",
                                 "tool_calls": [{"type": "function", "function": {
                                    "name": "get_weather", "arguments": '{"city":"NYC"}'}}]},
                                {"role": "tool", "content": "sunny"}], tools=TOOLS),
    # NOTE: no empty-messages probe. gemma's own template reads messages[0] to find a
    # system turn, so BOTH the unbaked source AND the shipped netsec template raise on
    # []. llama.cpp does not probe gemma with empty messages (netsec ships and runs),
    # so an empty-messages failure is a false alarm, not a bake defect.
}

fails = []
for name, kw in PROBES.items():
    for think in (True, False):
        try:
            out = tpl.render(add_generation_prompt=True, bos_token="<bos>",
                             eos_token="<eos>", enable_thinking=think, **kw)
            if not isinstance(out, str):
                fails.append(f"{name}(think={think}): non-string output")
        except Exception as e:
            fails.append(f"{name}(think={think}): {type(e).__name__}: {e}")

if fails:
    print("RENDER FAILURES (do NOT bake):")
    for f in fails: print("  -", f)
    sys.exit(1)
print(f"OK: all {len(PROBES)} probe inputs x2 thinking modes rendered cleanly.")
