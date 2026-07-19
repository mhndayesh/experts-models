#!/usr/bin/env python3
"""test_write_baked.py - offline smoke for the wired write_baked():
builds a tiny synthetic GGUF (one dummy tensor), bakes a template + bank
into a copy, reads the copy back and asserts every key and the tensor
survived. No model files, no network, ~1 MB of disk in %TEMP%.
"""
import os, sys, tempfile
import numpy as np
import gguf
from bake_template_v3 import write_baked

TPL = "{%- for m in messages -%}[{{ m.role }}]{{ m.content }}{%- endfor -%}FBTEST"
BANK = '{"id":"t1","text":"synthetic fact"}\n'


def make_src(path):
    w = gguf.GGUFWriter(path, arch="llama")
    w.add_chat_template("{{ original }}")
    w.add_name("synthetic-src")
    w.add_tensor("dummy.weight", np.arange(16, dtype=np.float32).reshape(4, 4))
    w.write_header_to_file()
    w.write_kv_data_to_file()
    w.write_tensors_to_file()
    w.close()


def field_str(reader, key):
    f = reader.fields.get(key)
    assert f is not None, f"missing field {key}"
    return bytes(f.parts[f.data[0]]).decode("utf-8")


def main():
    d = tempfile.mkdtemp(prefix="fb_write_baked_")
    src, dst = os.path.join(d, "src.gguf"), os.path.join(d, "dst.gguf")
    make_src(src)

    info = write_baked(src, dst, TPL, BANK, version="0.3.1-test")
    assert info["out_bytes"] == os.path.getsize(dst)

    r = gguf.GGUFReader(dst, "r")
    assert field_str(r, "tokenizer.chat_template") == TPL, "template not written"
    assert field_str(r, "factbank.bank") == BANK, "factbank.bank not written"
    assert field_str(r, "factbank.version") == "0.3.1-test", "factbank.version not written"

    t = {t.name: t for t in r.tensors}["dummy.weight"]
    got = np.array(t.data, dtype=np.float32).reshape(4, 4)
    assert np.array_equal(got, np.arange(16, dtype=np.float32).reshape(4, 4)), \
        "tensor bytes changed"

    # source untouched
    rs = gguf.GGUFReader(src, "r")
    assert field_str(rs, "tokenizer.chat_template") == "{{ original }}"

    # GGUFReader keeps a memmap open; drop refs before deleting (Windows)
    del t, r, rs
    import gc
    gc.collect()
    try:
        for p in (src, dst):
            os.remove(p)
        os.rmdir(d)
    except PermissionError:
        print(f"[warn] temp files left behind (memmap still open): {d}")
    print("write_baked smoke: PASS (template, factbank.bank, factbank.version, tensor bit-exact)")


if __name__ == "__main__":
    main()
