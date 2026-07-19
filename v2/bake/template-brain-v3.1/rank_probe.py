#!/usr/bin/env python3
"""rank_probe.py - offline cap-pressure + ranking probe. NO GPU, NO models.

Replicates the template's gate + deep-scan selection in Python (same k2
normalization, same padded-substring matching, same pass conditions) and
answers two questions per probe prompt:

  1. pressure - how many facts are ELIGIBLE vs the FB_MAX cap? (if eligible
     never exceeds the cap, a ranker cannot change any answer)
  2. selection - which facts win the slots under (a) today's bank-order
     rule and (b) the weighted score rule (10*dead + 4*strong + 1*weak,
     tie band finishes uncapped, then descending bands)

usage: python rank_probe.py bank_enriched_scale.jsonl [--gate-n 8] [--cap 5]
"""
import json, sys, argparse
from bake_template_v3 import build_gate

TIE_MAX = 8      # matches FB_TIE_MAX in fb_preloop.jinja

FB_PUNCT = ".,()?!:;'\n"

QUESTIONS = [
    # the 9 live LM Studio questions (2026-07-13 v3 test)
    ("live", "hello there"),
    ("live", "write a haiku about the sea"),
    ("live", "Explain what a closure is in Python, briefly."),
    ("live", "in bqn how do I sum a list of numbers?"),
    ("live", "in zig how do I convert an integer to a float?"),
    ("live", "quick polars question: how do i reshape wide format into long format"),
    ("live", "quick whenever question: how do i get the current time in a specific timezone"),
    ("live", "my polars melt code stopped working after upgrading, fix it"),
    ("live", "what is the weather in paris and fix my polars melt code"),
    # one natural question per niche language (own-language probes)
    ("probe", "in zig, how do I handle errors with try and catch?"),
    ("probe", "in nim, how do I split a comma separated string and parse the numbers?"),
    ("probe", "in ocaml, how do I pattern match on a list?"),
    ("probe", "in raku, how do I define a subroutine with named arguments?"),
    ("probe", "in crystal, how do I handle nil values safely?"),
    ("probe", "in gleam, how do I handle errors without exceptions?"),
    ("probe", "in dlang, how do I sort an array of structs by a field?"),
    ("probe", "in odin, how do I allocate and free memory?"),
    ("probe", "in racket, how do I define a struct and use it?"),
    ("probe", "in haxe, how do I compile to javascript?"),
    ("probe", "in janet, how do I loop over a table?"),
    ("probe", "in bqn, how do I reverse a list?"),
    ("probe", "how do i validate a nested model in pydantic v2?"),
    ("probe", "async http request with httpx, how?"),
    ("probe", "parse an iso date string with whenever"),
]

def k2_of(text):
    s = " " + text + " "
    s = s.lower()
    for ch in FB_PUNCT:
        s = s.replace(ch, " ")
    return s

def open_tabs(gate, k2):
    libs = ""
    for g in gate:
        if any(k in k2 for k in g["trig"]):
            libs += g["lib"]
    return libs

def score_fact(f, k2):
    """mirrors the template: rare strong keys +4, common strong keys +1
    (both count toward sc), weak +1, dead-name +10 (F-047)."""
    rare = sum(1 for k in f["s"] if k in k2)
    common = sum(1 for k in f.get("c", []) if k in k2)
    sc = rare + common
    wc = sum(1 for k in f["w"] if k in k2)
    dc = sum(1 for k in f.get("d", []) if k in k2)
    return sc, wc, dc, 10 * dc + 4 * rare + common + wc

def select_today(bank, libs, k2, cap):
    """current template rule: pass A (sc>1 or wc>0) bank order, pass B fill."""
    picked = []
    for f in bank:
        if f["lib"] in libs:
            sc, wc, _, _ = score_fact(f, k2)
            if (sc > 1 or wc > 0) and len(picked) < cap:
                picked.append((f["txt"], "A"))
    for f in bank:
        if f["lib"] in libs:
            sc, wc, _, _ = score_fact(f, k2)
            if sc == 1 and wc == 0 and len(picked) < cap:
                picked.append((f["txt"], "B"))
    return picked

def select_ranked(bank, libs, k2, cap):
    """weighted rule: find best among pass-A eligibles; emit tie band
    uncapped (finish-the-band), then lower bands to cap, then pass-B."""
    best = 0
    for f in bank:
        if f["lib"] in libs:
            sc, wc, _, score = score_fact(f, k2)
            if (sc > 1 or wc > 0) and score > best:
                best = score
    picked = []
    for f in bank:                                   # tie band, uncapped
        if f["lib"] in libs:
            sc, wc, _, score = score_fact(f, k2)
            if (sc > 1 or wc > 0) and score == best and best > 0 and len(picked) < TIE_MAX:
                picked.append((f["txt"], f"tie@{score}"))
    for f in bank:                                   # upper band
        if f["lib"] in libs:
            sc, wc, _, score = score_fact(f, k2)
            if (sc > 1 or wc > 0) and best - 5 <= score < best and len(picked) < cap:
                picked.append((f["txt"], f"band1@{score}"))
    for f in bank:                                   # remaining pass-A
        if f["lib"] in libs:
            sc, wc, _, score = score_fact(f, k2)
            if (sc > 1 or wc > 0) and 0 < score < best - 5 and len(picked) < cap:
                picked.append((f["txt"], f"band2@{score}"))
    for f in bank:                                   # pass-B floor filler
        if f["lib"] in libs:
            sc, wc, _, _ = score_fact(f, k2)
            if sc == 1 and wc == 0 and len(picked) < cap:
                picked.append((f["txt"], "floor"))
    return picked

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("enriched")
    ap.add_argument("--gate-n", type=int, default=8)
    ap.add_argument("--cap", type=int, default=5)
    ap.add_argument("--controls", default="controls_repo.txt")
    ap.add_argument("--full", action="store_true", help="print selected fact texts")
    ap.add_argument("--questions", help="JSON file: list of [tag, question] pairs; replaces the built-in set")
    a = ap.parse_args()
    global QUESTIONS
    if a.questions:
        QUESTIONS = [tuple(x) for x in json.load(open(a.questions, encoding="utf-8"))]

    lines = open(a.enriched, encoding="utf-8").read().splitlines()
    rows = [json.loads(l) for l in lines[1:] if l.strip()]
    gate, groups, _ = build_gate(rows, a.gate_n)
    # bake now emits a GROUPED bank ({lib, f:[...]}); the probe replicates the
    # template's selection, which is order-identical to walking the groups in
    # order, so flatten with the lib stamped back onto each fact.
    bank = [dict(f, lib=g["lib"]) for g in groups for f in g["f"]]

    bound = 0
    for tag, q in QUESTIONS:
        k2 = k2_of(q)
        libs = open_tabs(gate, k2)
        elig_a = elig_b = 0
        for f in bank:
            if f["lib"] in libs:
                sc, wc, _, _ = score_fact(f, k2)
                if sc > 1 or wc > 0:
                    elig_a += 1
                elif sc == 1 and wc == 0:
                    elig_b += 1
        total = elig_a + elig_b
        binds = total > a.cap
        bound += binds
        today = select_today(bank, libs, k2, a.cap)
        ranked = select_ranked(bank, libs, k2, a.cap)
        changed = [t for t, _ in ranked] != [t for t, _ in today]
        print(f"[{tag}] {q}")
        print(f"  tabs={libs.strip() or '-'} | eligible A={elig_a} B={elig_b} "
              f"total={total} cap={a.cap} -> {'CAP BINDS' if binds else 'no pressure'}"
              f"{' | ranked CHANGES selection' if changed else ''}")
        if a.full:
            for t, why in ranked:
                print(f"    [{why}] {t[:110]}")
        print()

    controls = [l.strip() for l in open(a.controls, encoding="utf-8") if l.strip()]
    fires = 0
    for c in controls:
        k2 = k2_of(c)
        libs = open_tabs(gate, k2)
        sel = select_ranked(bank, libs, k2, a.cap) if libs else []
        if sel:
            fires += 1
            print(f"FALSE FIRE on control: {c[:70]!r} -> {len(sel)} facts, tabs={libs}")
    print(f"=== cap binds on {bound}/{len(QUESTIONS)} questions | "
          f"false fires on controls: {fires}/{len(controls)}")

if __name__ == "__main__":
    main()
