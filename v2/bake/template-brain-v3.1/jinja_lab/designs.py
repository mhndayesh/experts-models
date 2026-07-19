#!/usr/bin/env python3
"""designs.py - candidate retrieval engines, each BUILT from the real bank and
SIMULATED in Python with EXACTLY the semantics the Jinja template would have.

Why simulate in Python first: a design is only worth compiling into Jinja if it
wins on the gold set. The simulation is the same arithmetic the template does
(padded-substring or word-lookup, integer weights, namespace accumulation), so
a win here is a win there - and the winner is then rendered in REAL minja to
prove the semantics survive the engine (verify_in_minja.py).

Designs
  D1 scan_v34   : what ships today - padded substring scan, 5 ranked passes.
  D2 index_word : inverted index; question is SPLIT INTO WORDS; each word looks
                  up a postings list "factid:weight". Fixes phrase-contiguity.
  D3 index_bigram: D2 + adjacent word pairs indexed, so "long format" is a term.
  D4 index_class: D3 + provenance weight (curated facts outrank mined listings)
                  + intent boost (broke/stopped/renamed/deprecated doubles the
                  curated weight).
"""
import json, re, collections

FB_MAX = 5
PUNCT = ".,()?!:;'\n"
STOPW = set("""the a an and or of in on for to from is are was be do does how i my
me it its this that with what when where why can could would should if then than
now new use using used get got make made want need help please code show me
example examples work works working stopped broke broken fix fixed after before
into out up down which who whom whose there here""".split())


def norm(q):
    s = " " + q.lower() + " "
    for ch in PUNCT:
        s = s.replace(ch, " ")
    return s


def words(q):
    return [w for w in norm(q).split() if len(w) > 2 and w not in STOPW]


# ---------------------------------------------------------------- D1: today
def build_d1(bank):
    return {"facts": bank}


def run_d1(model, q, cap=FB_MAX):
    k2 = norm(q)
    libs = {f["lib"] for f in model["facts"]
            if any(t in k2 for t in f["trig"])}
    elig = []
    for f in model["facts"]:
        if f["lib"] not in libs:
            continue
        rare = sum(1 for k in f["s"] if k in k2)
        common = sum(1 for k in f["c"] if k in k2)
        w = sum(1 for k in f["w"] if k in k2)
        d = sum(1 for k in f["d"] if k in k2)
        sc = rare + common
        if not (sc > 1 or w > 0):
            continue
        elig.append((10 * d + 4 * rare + common + w, f["id"]))
    elig.sort(key=lambda x: -x[0])
    return [fid for _, fid in elig[:cap]]


# ------------------------------------------------- D2/D3/D4: inverted index
def _terms_of_fact(f, bigrams):
    """the terms a fact is indexed under, with weights"""
    t = collections.Counter()
    for k in f["d"]:
        t[k.strip()] += 10                      # dead name: strongest evidence
    for k in f["s"]:
        t[k.strip()] += 4                       # rare API token
    for k in f["c"]:
        t[k.strip()] += 1                       # common token (library name etc)
    for phrase in f["w"]:                       # task phrases -> their words
        ws = [w for w in phrase.strip().split() if len(w) > 2 and w not in STOPW]
        for w in ws:
            t[w] += 2
        if bigrams:
            for a, b in zip(ws, ws[1:]):
                t[a + "_" + b] += 3
    # index the fact's own description words too (recall!) - low weight
    desc = f["txt"].split(" - ", 1)[1] if " - " in f["txt"] else f["txt"]
    for w in [w for w in norm(desc).split() if len(w) > 3 and w not in STOPW][:20]:
        t[w] += 1
    return t


def build_index(bank, bigrams=False, classw=False):
    post = collections.defaultdict(list)
    meta = {}
    for f in bank:
        meta[f["id"]] = f
        for term, wt in _terms_of_fact(f, bigrams).items():
            if not term:
                continue
            post[term].append((f["id"], wt))
    return {"post": dict(post), "meta": meta, "bank": bank,
            "bigrams": bigrams, "classw": classw}


INTENT = ("broke", "broken", "stopped", "fails", "failing", "error", "renamed",
          "removed", "deprecated", "upgrading", "upgraded", "migrate", "attributeerror")


def run_index(model, q, cap=FB_MAX):
    ws = words(q)
    terms = list(ws)
    if model["bigrams"]:
        terms += [a + "_" + b for a, b in zip(ws, ws[1:])]
    # GATE FIRST, and it is MANDATORY: if the question opened no library tab,
    # retrieve NOTHING. Without this the index happily matches "sort"/"value"
    # from a fact's description text against a control question and injects
    # facts into a haiku (measured: 8/10 controls false-fired). The gate is
    # what makes generous in-tab matching safe.
    libs = {f["lib"] for f in model["bank"]
            if any(t in norm(q) for t in f["trig"])}
    if not libs:
        return []
    intent = any(w in INTENT for w in norm(q).split())

    score = collections.Counter()
    for t in terms:
        for fid, wt in model["post"].get(t, ()):
            f = model["meta"][fid]
            if f["lib"] not in libs:
                continue                        # tab discipline
            score[fid] += wt
    if model["classw"]:
        for fid in list(score):
            f = model["meta"][fid]
            if f["curated"]:
                bonus = 6 if not intent else 12
                score[fid] += bonus
    ranked = sorted(score.items(), key=lambda x: (-x[1], x[0]))
    return [fid for fid, _ in ranked[:cap]]


# ---------------------------------------------------------------- D5: tuned
# Three changes, all aimed at BYTES (the 1 MiB ceiling is the real budget) and
# at the two recall misses D4 still had:
#   1. compact numeric fact ids ("f731" not "pandasapi-0186") - postings are
#      the bulk of the index, and every posting repeats an id.
#   2. document-frequency cap: a description word that appears in more than
#      DF_CAP facts of the same library carries no information - drop the
#      posting instead of paying bytes for noise.
#   3. curated facts get their description words indexed at a HIGHER weight
#      than mined listings do: on a "what changed" question, the sentence
#      "Polars renamed ... apply to map_elements" IS the evidence.
DF_CAP = 40


def build_index_v5(bank, bigrams=True, classw=True):
    raw = collections.defaultdict(list)
    meta, short = {}, {}
    for i, f in enumerate(bank):
        sid = f"f{i}"
        short[f["id"]] = sid
        meta[sid] = f
        t = collections.Counter()
        for k in f["d"]:
            t[k.strip()] += 10
        for k in f["s"]:
            t[k.strip()] += 4
        for k in f["c"]:
            t[k.strip()] += 1
        for phrase in f["w"]:
            ws = [w for w in phrase.strip().split() if len(w) > 2 and w not in STOPW]
            for w in ws:
                t[w] += 2
            if bigrams:
                for a, b in zip(ws, ws[1:]):
                    t[a + "_" + b] += 3
        desc = f["txt"].split(" - ", 1)[1] if " - " in f["txt"] else f["txt"]
        dw = 3 if f["curated"] else 1
        for w in [w for w in norm(desc).split() if len(w) > 3 and w not in STOPW][:24]:
            t[w] += dw
        for term, wt in t.items():
            if term:
                raw[term].append((sid, wt))
    # df cap: drop terms that point at too much of the bank to mean anything
    post = {t: pl for t, pl in raw.items() if len(pl) <= DF_CAP}
    dropped = len(raw) - len(post)
    return {"post": post, "meta": meta, "bank": bank, "short": short,
            "bigrams": bigrams, "classw": classw, "_dropped": dropped}


def run_index_v5(model, q, cap=FB_MAX):
    ws = words(q)
    terms = list(ws) + [a + "_" + b for a, b in zip(ws, ws[1:])]
    libs = {f["lib"] for f in model["bank"] if any(t in norm(q) for t in f["trig"])}
    if not libs:
        return []
    intent = any(w in INTENT for w in norm(q).split())
    score = collections.Counter()
    for t in terms:
        for sid, wt in model["post"].get(t, ()):
            f = model["meta"][sid]
            if f["lib"] not in libs:
                continue
            score[sid] += wt
    for sid in list(score):
        if model["meta"][sid]["curated"]:
            score[sid] += 12 if intent else 6
    ranked = sorted(score.items(), key=lambda x: (-x[1], x[0]))
    return [model["meta"][sid]["id"] for sid, _ in ranked[:cap]]


def run_index_v6(model, q, cap=FB_MAX):
    """D5 + TAB DISCIPLINE: if the question NAMES a library (or an alias), only
    that library's tab opens. Otherwise fall back to inferred tabs (a question
    like "FutureWarning about frequency alias M" names nothing and must still
    reach pandas). Without this, a pandas fact wins slots in a polars question
    because both libraries share a token."""
    k2 = norm(q)
    named = {f["lib"] for f in model["bank"] if f["lib"] in k2}
    inferred = {f["lib"] for f in model["bank"] if any(t in k2 for t in f["trig"])}
    libs = named or inferred
    if not libs:
        return []
    ws = words(q)
    terms = list(ws) + [a + "_" + b for a, b in zip(ws, ws[1:])]
    intent = any(w in INTENT for w in k2.split())
    score = collections.Counter()
    for t in terms:
        for sid, wt in model["post"].get(t, ()):
            f = model["meta"][sid]
            if f["lib"] not in libs:
                continue
            score[sid] += wt
    for sid in list(score):
        if model["meta"][sid]["curated"]:
            score[sid] += 12 if intent else 6
    ranked = sorted(score.items(), key=lambda x: (-x[1], x[0]))
    return [model["meta"][sid]["id"] for sid, _ in ranked[:cap]]


DESIGNS = {
    "D1_scan_today":  (lambda bank: build_d1(bank), run_d1),
    "D4_index_class": (lambda bank: build_index(bank, True, True), run_index),
    "D5_tuned":       (lambda bank: build_index_v5(bank), run_index_v5),
    "D6_tabdisc":     (lambda bank: build_index_v5(bank), run_index_v6),
}
