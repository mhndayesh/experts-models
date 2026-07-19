#!/usr/bin/env python3
"""probe_minja.py - what can we actually EXECUTE inside tokenizer.chat_template?

Truth source is minja (llama.cpp's engine, which LM Studio runs) - NOT jinja2.
No baking: llama-server takes --chat-template-file, and POST /apply-template
renders a message list through it and returns the prompt. So we can test
template code directly, with a 0.6B model on CPU, in ~10s per template.

usage: python probe_minja.py            (runs the whole matrix)
"""
import json, os, subprocess, sys, time, urllib.request, glob

SRV = r"C:\Users\mhnda\.lmstudio\extensions\backends\llama.cpp-win-x86_64-vulkan-avx2-2.24.0\llama-server.exe"
MODEL = glob.glob(r"C:\Users\mhnda\.lmstudio\models\**\*Qwen3-0.6B*.gguf", recursive=True)[0]
PORT = 8099

FEATURES = {
    # --- data structures ---
    "dict_literal_varkey":  '{% set d={"a":"X","b":"Y"} %}{% set k="a" %}{{ d[k] }}',
    "dict_membership":      '{% set d={"a":1} %}{{ "a" in d }}{{ "z" in d }}',
    "dict_nested":          '{% set d={"a":{"b":[1,2,3]}} %}{{ d["a"]["b"][2] }}',
    "dict_items_filter":    '{% set d={"a":1,"b":2} %}{% for k,v in d|items %}{{k}}{{v}}{% endfor %}',
    "list_index_var":       '{% set L=[10,20,30] %}{% set i=2 %}{{ L[i] }}',
    "list_len":             '{{ [1,2,3]|length }}',
    "list_literal_in_loop": '{% for x in [1,2] %}{{x}}{% endfor %}',
    # --- strings ---
    "split_nosep":          '{{ "a b c".split()|length }}',
    "split_sep":            '{{ "p1:10".split(":")[1] }}',
    "slice":                '{{ "abcdef"[1:4] }}',
    "startswith":           '{{ "hello".startswith("he") }}',
    "replace_chain":        '{{ "a.b,c"|replace("."," ")|replace(","," ") }}',
    "lower_upper":          '{{ "AbC"|lower }}{{ "x"|upper }}',
    "concat_in_loop":       '{% set ns=namespace(s="") %}{% for w in "a b".split() %}{% set ns.s=ns.s+w %}{% endfor %}{{ ns.s }}',
    "string_contains":      '{{ "melt" in " my melt code " }}',
    "trim":                 '{{ "  x  "|trim }}',
    # --- numbers / logic ---
    "int_cast_math":        '{{ ("7"|int) + 3 }}',
    "compare_and_or":       '{{ 1 if (2>1 and 3>=3) else 0 }}',
    "max_via_if":           '{% set ns=namespace(m=0) %}{% for v in [3,9,2] %}{% if v>ns.m %}{% set ns.m=v %}{% endif %}{% endfor %}{{ ns.m }}',
    # --- control flow ---
    "nested_loops_3deep":   '{% for a in [1,2] %}{% for b in [1,2] %}{% for c in [1] %}{{a}}{{b}}{{c}}{% endfor %}{% endfor %}{% endfor %}',
    "loop_index":           '{% for x in ["a","b"] %}{{ loop.index0 }}{% endfor %}',
    "macro":                '{% macro f(x) %}[{{x}}]{% endmacro %}{{ f("z") }}',
    "namespace_mutate":     '{% set ns=namespace(n=0) %}{% for i in [1,1,1] %}{% set ns.n=ns.n+1 %}{% endfor %}{{ ns.n }}',
    # --- things we EXPECT to fail (know the wall) ---
    "sort_filter":          '{{ [3,1,2]|sort|join(",") }}',
    "list_append":          '{% set ns=namespace(L=[]) %}{% set _=ns.L.append(1) %}{{ ns.L|length }}',
    "dict_assign":          '{% set d={} %}{% set d["k"]=1 %}{{ d["k"] }}',
    "selectattr":           '{% set L=[{"k":1},{"k":9}] %}{{ L|selectattr("k","gt",5)|list|length }}',
    "map_filter":           '{{ [1,2]|map("string")|join(",") }}',
    "groupby":              '{% set L=[{"g":"a"},{"g":"b"}] %}{{ L|groupby("g")|list|length }}',
    "batch":                '{{ [1,2,3,4]|batch(2)|list|length }}',
    "regex_search":         '{{ "abc"|regex_search("b") }}',
}


def render_in_minja(tpl_body):
    """spawn llama-server with this template, POST /apply-template, return output"""
    path = os.path.abspath("_probe.jinja")
    open(path, "w", encoding="utf-8").write(
        "OUT>>" + tpl_body + "<<OUT")
    p = subprocess.Popen([SRV, "-m", MODEL, "--chat-template-file", path,
                          "--port", str(PORT), "--host", "127.0.0.1",
                          "-ngl", "0", "-c", "256"],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        for _ in range(60):
            time.sleep(0.5)
            try:
                urllib.request.urlopen(f"http://127.0.0.1:{PORT}/health", timeout=2)
                break
            except Exception:
                continue
        else:
            return None, "server never became healthy"
        body = json.dumps({"messages": [{"role": "user", "content": "hi"}]}).encode()
        req = urllib.request.Request(f"http://127.0.0.1:{PORT}/apply-template",
                                     data=body, headers={"Content-Type": "application/json"})
        try:
            out = json.loads(urllib.request.urlopen(req, timeout=20).read())
            prompt = out.get("prompt", "")
            if "OUT>>" in prompt and "<<OUT" in prompt:
                return prompt.split("OUT>>")[1].split("<<OUT")[0], None
            return prompt, None
        except urllib.error.HTTPError as e:
            return None, f"render error: {e.read().decode()[:120]}"
    finally:
        p.terminate()
        try:
            p.wait(timeout=10)
        except Exception:
            p.kill()


def main():
    results = {}
    for name, tpl in FEATURES.items():
        out, err = render_in_minja(tpl)
        ok = err is None and out is not None and out.strip() != ""
        results[name] = {"ok": ok, "out": (out or "").strip()[:40], "err": err}
        print(f"  {'PASS' if ok else 'FAIL'}  {name:22} {(out or err or '')[:46].strip()}")
    json.dump(results, open("minja_capabilities.json", "w"), indent=1)
    n_ok = sum(1 for r in results.values() if r["ok"])
    print(f"\n{n_ok}/{len(results)} features usable in minja -> minja_capabilities.json")


if __name__ == "__main__":
    main()
