"""bake.py - burn the fact bank into a GGUF's chat template.

Produces ONE file that works in plain LM Studio (or any llama.cpp
runner): the facts ride in a permanent system block rendered by the
model's own chat template. This is the static, loop-less delivery
channel — no retrieval, no draft pass, no auto-updates. Re-bake to
update facts (the watcher keeps the source bank fresh; this command
snapshots it into an artifact).

Trade-offs vs the served loop (owner-approved 2026-07-13): every
request carries the whole bank (~6k tokens for 94 facts), facts are
frozen at bake time, and the measured loop metrics do NOT transfer —
the baked artifact must be re-measured on its own.

Baked-in hard choices:
- `enable_thinking` is SET false at the top of the template — thinking
  stays off no matter what the host UI toggles (F-035/F-018: a thinking
  toggle that resets on reload is how budgets silently burn).
- The system block always renders; a user-supplied system prompt
  appears AFTER the facts and still works. Tools still work.
"""

import json
import os

# the exact system-turn opener in the gemma-4 template; the facts block
# is injected right after it as RAW template text (verbatim emission —
# no Jinja string-literal escaping games with a 20KB payload)
_SYS_OPEN = "{{- '<|turn>system\\n' -}}"

FRAMING_TOP = (
    "FACT BANK — OFFICIAL DOCUMENTATION EXCERPTS ({n} facts, baked "
    "{date}).\n"
    "These facts come from official library documentation and release "
    "notes. They are the source of truth. When a fact below conflicts "
    "with what you remember from training, THE FACT WINS — your "
    "training data is older than these facts. Use them exactly; never "
    "correct them. Ignore any fact irrelevant to the user's question, "
    "and never force an irrelevant fact into an answer.\n")
FRAMING_END = ("END OF FACT BANK. Obey the facts above when relevant; "
               "otherwise answer normally.")


def _sanitize(s: str) -> str:
    """Fact text must not be able to open a Jinja tag or a gemma
    control token when emitted as raw template text."""
    return (s.replace("{%", "{ %").replace("{{", "{ {")
            .replace("{#", "{ #").replace("<|", "< |"))


def facts_block(bank_path: str, date: str) -> str:
    facts = [json.loads(l) for l in open(bank_path, encoding="utf-8")
             if l.strip()]
    lines = [f"- [{f['source']} {f['version']}] {f['text']}"
             for f in facts]
    body = "\n".join(_sanitize(l) for l in lines)
    return (FRAMING_TOP.format(n=len(facts), date=date)
            + "\n" + body + "\n" + FRAMING_END), len(facts)


def bake_template(original: str, block: str) -> str:
    """Three surgical edits; each one is verified present or we refuse
    (a silently unbaked GGUF would look identical from the outside)."""
    if _SYS_OPEN not in original:
        raise ValueError("template surgery failed: system-turn opener "
                         "not found — template layout changed, re-derive "
                         "the injection point")
    # 1. thinking permanently off (set shadows any host-passed variable)
    out = "{%- set enable_thinking = false -%}\n" + original
    # 2. the system block must ALWAYS render (facts live there)
    cond = ("{%- if (enable_thinking is defined and enable_thinking) "
            "or tools or messages[0]['role'] in ['system', 'developer'] "
            "-%}")
    if cond not in out:
        raise ValueError("template surgery failed: system-block "
                         "condition not found")
    out = out.replace(cond, "{%- if true -%}", 1)
    # 3. facts as raw text right after the system-turn opener, with an
    #    explicit blank line before any user-supplied system content
    out = out.replace(_SYS_OPEN,
                      _SYS_OPEN + "\n" + block + "{{- '\\n\\n' -}}", 1)
    return out


def read_template(gguf_path: str) -> str:
    from gguf import GGUFReader
    r = GGUFReader(gguf_path, "r")
    f = r.fields.get("tokenizer.chat_template")
    if f is None:
        raise ValueError(f"{gguf_path}: no tokenizer.chat_template")
    return bytes(f.parts[f.data[0]]).decode("utf-8")


def bake(src: str, out: str, bank: str, name: str, date: str) -> dict:
    """-> summary dict. Copies tensors untouched; rewrites template +
    name + description."""
    try:
        import gguf
        from gguf.scripts.gguf_new_metadata import (MetadataDetails,
                                                    copy_with_new_metadata)
    except ImportError:
        raise SystemExit("bake needs the gguf package: pip install gguf")

    block, n = facts_block(bank, date)
    baked = bake_template(read_template(src), block)

    reader = gguf.GGUFReader(src, "r")
    arch = reader.get_field(gguf.Keys.General.ARCHITECTURE).contents()
    writer = gguf.GGUFWriter(out, arch=arch, endianess=reader.endianess)
    align = reader.get_field(gguf.Keys.General.ALIGNMENT)
    if align is not None:
        writer.data_alignment = align.contents()
    desc = (f"gemma-4-12B QAT with a baked factbank system block "
            f"({n} facts, {date}). Thinking hard-disabled. "
            f"Static facts — re-bake to update.")
    new_md = {
        gguf.Keys.Tokenizer.CHAT_TEMPLATE:
            MetadataDetails(gguf.GGUFValueType.STRING, baked),
        gguf.Keys.General.NAME:
            MetadataDetails(gguf.GGUFValueType.STRING, name),
        gguf.Keys.General.DESCRIPTION:
            MetadataDetails(gguf.GGUFValueType.STRING, desc),
    }
    copy_with_new_metadata(reader, writer, new_md, [])
    return {"facts": n, "template_chars": len(baked),
            "out_bytes": os.path.getsize(out)}


def cmd_bake(args) -> int:
    import time
    date = time.strftime("%Y-%m-%d")
    print(f"[bake] {args.gguf}\n[bake] + {args.bank}\n[bake] -> "
          f"{args.out}")
    s = bake(args.gguf, args.out, args.bank, args.name, date)
    print(f"[bake] done: {s['facts']} facts, template "
          f"{s['template_chars']:,} chars, {s['out_bytes']:,} bytes")
    # read the ARTIFACT back — an unbaked GGUF looks identical from
    # the outside, so verification is part of the command, not optional
    t = read_template(args.out)
    ok = ("{%- set enable_thinking = false -%}" in t
          and "END OF FACT BANK" in t and FRAMING_TOP[:30] in t)
    print(f"[bake] read-back verify: "
          f"{'OK — facts + think-off present' if ok else 'FAILED'}")
    return 0 if ok else 1
