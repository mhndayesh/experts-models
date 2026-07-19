#!/usr/bin/env python3
"""compile_d6.py - compile design D6 (inverted index + weighted postings + tab
discipline + curated bonus) into REAL Jinja, and prove it executes in minja.

The engine has no dict assignment, no sort, no append. So scoring is done the
only way minja allows:
  1. walk the question's words/bigrams, look each up in the postings dict,
     append "sid:weight" pairs into ONE namespace string;
  2. de-duplicate and total by re-walking that string (h is tiny, ~<200);
  3. select the top 5 by five max-selection passes over the totals string.

Fact ids encode provenance: c### = curated, m### = mined. No extra dict.

usage:
  python compile_d6.py --out d6.jinja            # emit the template
  python compile_d6.py --verify                  # + render it in real minja
"""
import argparse, collections, json, os, subprocess, sys, time, urllib.request, glob

sys.path.insert(0, ".")
sys.path.insert(0, "..")
from designs import build_index_v5, norm, words, STOPW, INTENT
from lab_bench import load_bank

SRV = r"C:\Users\mhnda\.lmstudio\extensions\backends\llama.cpp-win-x86_64-vulkan-avx2-2.24.0\llama-server.exe"
PORT = 8123

HEAD = r"""{%- set fb_post = __POST__ -%}
{%- set fb_txt = __TXT__ -%}
{%- set fb_lib = __LIB__ -%}
{%- set fb_names = __NAMES__ -%}
{%- set fb_trig = __TRIG__ -%}
{%- set FB_MAX = 5 -%}
{%- set STOPW = __STOPW__ -%}
{%- set INTENT = __INTENT__ -%}
"""

BODY = r"""
{%- set fbok = messages and (messages[-1]['content'] is string) -%}
{%- if fbok -%}
{%- set q = (" " + messages[-1]['content'] + " ") | lower | replace("."," ") | replace(","," ") | replace("("," ") | replace(")"," ") | replace("?"," ") | replace("!"," ") | replace(":"," ") | replace(";"," ") | replace("'"," ") -%}
{%- set ns = namespace(libs="", hits="", tot="", seen="", picked="", out="", best="", bestsc=0, intent=0) -%}

{#- gate: a NAMED library wins; otherwise fall back to trigger words -#}
{%- for lib in fb_names -%}
  {%- if (" " + lib + " ") in q -%}{%- set ns.libs = ns.libs + lib + " " -%}{%- endif -%}
{%- endfor -%}
{%- if ns.libs == "" -%}
  {%- for lib, trigs in fb_trig | items -%}
    {%- for t in trigs.split("|") -%}
      {%- if (" " + t + " ") in q and (lib + " ") not in ns.libs -%}
        {%- set ns.libs = ns.libs + lib + " " -%}
      {%- endif -%}
    {%- endfor -%}
  {%- endfor -%}
{%- endif -%}

{%- if ns.libs != "" -%}
{#- intent: does the user say something broke? -#}
{%- for w in q.split() -%}
  {%- if w in INTENT -%}{%- set ns.intent = 1 -%}{%- endif -%}
{%- endfor -%}

{#- query terms = content words + adjacent bigrams -#}
{%- set ws = [] -%}
{%- set qs = namespace(list="") -%}
{%- for w in q.split() -%}
  {%- if w|length > 2 and w not in STOPW -%}{%- set qs.list = qs.list + w + " " -%}{%- endif -%}
{%- endfor -%}
{%- set qw = qs.list.split() -%}
{%- set terms = namespace(all="") -%}
{%- for w in qw -%}{%- set terms.all = terms.all + w + " " -%}{%- endfor -%}
{%- for i in range(qw|length - 1) -%}
  {%- set terms.all = terms.all + qw[i] + "_" + qw[i+1] + " " -%}
{%- endfor -%}

{#- 1. postings lookup -> one flat "sid:wt" string -#}
{%- for t in terms.all.split() -%}
  {%- if t in fb_post -%}
    {%- for p in fb_post[t].split() -%}
      {%- set sid = p.split(":")[0] -%}
      {%- if (" " + fb_lib[sid] + " ") in (" " + ns.libs) -%}
        {%- set ns.hits = ns.hits + p + " " -%}
      {%- endif -%}
    {%- endfor -%}
  {%- endif -%}
{%- endfor -%}

{#- 2. de-dup + total (no dict assignment in minja: re-walk the string) -#}
{%- for p in ns.hits.split() -%}
  {%- set sid = p.split(":")[0] -%}
  {%- if (" " + sid + " ") not in (" " + ns.seen) -%}
    {%- set ns.seen = ns.seen + sid + " " -%}
    {%- set acc = namespace(v=0) -%}
    {%- for p2 in ns.hits.split() -%}
      {%- if ":" in p2 and p2.split(":")[0] == sid -%}
        {%- set acc.v = acc.v + (p2.split(":")[1] | int) -%}
      {%- endif -%}
    {%- endfor -%}
    {%- if sid[0] == "c" -%}
      {%- set acc.v = acc.v + (12 if ns.intent == 1 else 6) -%}
    {%- endif -%}
    {%- set ns.tot = ns.tot + sid + ":" + (acc.v | string) + " " -%}
  {%- endif -%}
{%- endfor -%}

{#- 3. top-5 by five max-selection passes (no sort in minja) -#}
{%- for slot in range(FB_MAX) -%}
  {%- set sel = namespace(id="", sc=0) -%}
  {%- for p in ns.tot.split() -%}
    {%- if ":" in p -%}
    {%- set sid = p.split(":")[0] -%}
    {%- set sc = p.split(":")[1] | int -%}
    {%- if sc > sel.sc and (" " + sid + " ") not in (" " + ns.picked) -%}
      {%- set sel.id = sid -%}{%- set sel.sc = sc -%}
    {%- endif -%}
    {%- endif -%}
  {%- endfor -%}
  {%- if sel.id != "" -%}
    {%- set ns.picked = ns.picked + sel.id + " " -%}
    {%- set ns.out = ns.out + "\n- " + fb_txt[sel.id] -%}
  {%- endif -%}
{%- endfor -%}
{%- endif -%}
{%- endif -%}
FACTS:{{ ns.picked if fbok else "" }}
"""


def compile_template(bank, sample=None):
    idx = build_index_v5(bank)
    # re-key: c### curated / m### mined  (provenance encoded in the id itself)
    remap, post, txt, lib = {}, collections.defaultdict(list), {}, {}
    cc = mc = 0
    for f in bank:
        old = idx["short"][f["id"]]
        if f["curated"]:
            new = f"c{cc}"; cc += 1
        else:
            new = f"m{mc}"; mc += 1
        remap[old] = new
        txt[new] = f["txt"]
        lib[new] = f["lib"].strip()
    for term, pl in idx["post"].items():
        if " " in term or ":" in term:
            continue                     # postings are space/colon delimited
        for sid, wt in pl:
            post[term].append(f"{remap[sid]}:{wt}")
    post = {t: " ".join(v) for t, v in post.items()}

    libs = sorted({f["lib"].strip() for f in bank})
    trig = {}
    for f in bank:
        l = f["lib"].strip()
        if l not in trig:
            trig[l] = sorted({t.strip() for t in f["trig"] if t.strip() and " " not in t.strip()})
    trig = {l: "|".join(t) for l, t in trig.items()}

    tpl = (HEAD.replace("__POST__", json.dumps(post, ensure_ascii=False))
               .replace("__TXT__", json.dumps(txt, ensure_ascii=False))
               .replace("__LIB__", json.dumps(lib, ensure_ascii=False))
               .replace("__NAMES__", json.dumps(libs, ensure_ascii=False))
               .replace("__TRIG__", json.dumps(trig, ensure_ascii=False))
               .replace("__STOPW__", json.dumps(sorted(STOPW), ensure_ascii=False))
               .replace("__INTENT__", json.dumps(sorted(INTENT), ensure_ascii=False))
           + BODY)
    return tpl, remap, idx


def render_minja(tpl_path, question):
    model = glob.glob(r"C:\Users\mhnda\.lmstudio\models\**\*Qwen3-0.6B*.gguf", recursive=True)[0]
    p = subprocess.Popen([SRV, "-m", model, "--chat-template-file", os.path.abspath(tpl_path),
                          "--port", str(PORT), "--host", "127.0.0.1", "-ngl", "0", "-c", "256"],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        for _ in range(80):
            time.sleep(0.5)
            try:
                urllib.request.urlopen(f"http://127.0.0.1:{PORT}/health", timeout=2)
                break
            except Exception:
                pass
        else:
            return None, 0
        out = []
        t0 = time.time()
        for q in question:
            body = json.dumps({"messages": [{"role": "user", "content": q}]}).encode()
            req = urllib.request.Request(f"http://127.0.0.1:{PORT}/apply-template", data=body,
                                         headers={"Content-Type": "application/json"})
            try:
                r = json.loads(urllib.request.urlopen(req, timeout=60).read())
                out.append(r.get("prompt", "").split("FACTS:")[-1].strip())
            except urllib.error.HTTPError as e:
                out.append("ERROR:" + e.read().decode()[:100])
        return out, (time.time() - t0) / max(1, len(question))
    finally:
        p.terminate()
        try:
            p.wait(timeout=10)
        except Exception:
            p.kill()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="d6.jinja")
    ap.add_argument("--verify", action="store_true")
    a = ap.parse_args()
    bank = load_bank()
    tpl, remap, idx = compile_template(bank)
    open(a.out, "w", encoding="utf-8").write(tpl)
    print(f"compiled {a.out}: {len(tpl)/1024:.0f} KB template, {len(bank)} facts, "
          f"{len(idx['post'])} index terms")

    if a.verify:
        gold = json.load(open("gold.json", encoding="utf-8"))
        qs = [c["q"] for c in gold["cases"]] + gold["controls"][:4]
        outs, per = render_minja(a.out, qs)
        if outs is None:
            print("minja: server never came up"); return
        print(f"\nminja render: {per*1000:.0f} ms/request (incl. HTTP)\n")
        hits = 0
        for c, o in zip(gold["cases"], outs):
            sid = remap[idx["short"][c["gold"]]] if c["gold"] in idx["short"] else None
            got = o.split()
            ok = sid in got
            hits += ok
            print(f"  {'HIT ' if ok else 'miss'} {c['q'][:46]:46} -> {' '.join(got[:5])}")
        for q, o in zip(gold["controls"][:4], outs[len(gold['cases']):]):
            print(f"  {'LEAK' if o.strip() else 'clean'} (control) {q[:40]}")
        print(f"\nminja HIT@5: {hits}/{len(gold['cases'])}")


if __name__ == "__main__":
    main()
