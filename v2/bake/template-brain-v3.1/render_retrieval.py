#!/usr/bin/env python3
"""render_retrieval.py - render a baked template with a real question and show
EXACTLY which facts the in-engine retriever injected. Answers the only question
that matters for a miss: did the fact reach the model's context, or not?

Injected facts carry a '[src: <lib>]' marker (bake_index.py). We render the
template with the question as the user turn and extract those lines.

usage: python render_retrieval.py <baked.jinja> "<question>" "<target substring>"
"""
import sys, re
from jinja2 import Environment, BaseLoader

tpl_path, question, target = sys.argv[1], sys.argv[2], (sys.argv[3] if len(sys.argv) > 3 else "")
src = open(tpl_path, encoding="utf-8").read()
env = Environment(loader=BaseLoader())
env.globals["raise_exception"] = lambda m: (_ for _ in ()).throw(RuntimeError(m))
env.globals["strftime_now"] = lambda f: "2026-07-17"
tpl = env.from_string(src)
out = tpl.render(messages=[{"role": "user", "content": question}],
                 add_generation_prompt=True, bos_token="<bos>", eos_token="<eos>",
                 enable_thinking=True)

# injected facts are the lines carrying the [src: ...] provenance marker
facts = re.findall(r"[^\n]*\[src:[^\]]*\][^\n]*", out)
libs = {}
for f in facts:
    m = re.search(r"\[src:\s*([^\]]+)\]", f)
    if m: libs[m.group(1).strip()] = libs.get(m.group(1).strip(), 0) + 1

print(f"  injected facts: {len(facts)}   gate opened: {'YES' if facts else 'NO (no facts reached the model)'}")
if libs: print("  libs injected:", ", ".join(f"{k}({v})" for k, v in sorted(libs.items())))
if target:
    hit = target.lower() in out.lower()
    print(f"  target '{target}' present in injected context: {'YES' if hit else 'NO'}")
    if hit:
        for f in facts:
            if target.lower() in f.lower():
                print("   ->", f.strip()[:160]); break
