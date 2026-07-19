#!/usr/bin/env python3
"""gen_gate_aliases.py - derive gate aliases so natural names and OLD names open a
library's tab, not just the exact lib token.

The bug (2026-07-17): the retrieval gate opens on the exact lib token (e.g.
`bloodhound-py`) plus keywords. A user asking "BloodHound" or "successor to
CrackMapExec" never types that token, so the gate stays shut and ZERO facts reach
the model. The old NAME of a rename is exactly what a stale user types -> make it a
trigger. Same class as the volatility3 "Volatility 3" vs `volatility3` gate death.

Rules (conservative, to avoid over-opening):
 - candidate tokens come from each rename/removal fact's `old` value + the lib's
   natural-name stem.
 - a token qualifies only if it is DISTINCTIVE (identifier-like: has . _ - or a (),
   OR is the whole short old command name like cme/nxc) and NOT a generic word.
 - a token must map to exactly ONE library (ambiguous -> dropped).
 - a token equal to a lib name is skipped (already a trigger).

usage: python gen_gate_aliases.py <facts_dir> <out.json>
"""
import json, glob, re, sys, collections

FD = sys.argv[1].rstrip("/"); OUT = sys.argv[2]

# generic words that must NEVER become a standalone gate trigger (would open a tab
# on unrelated questions). Old *values* often contain these; we keep only the
# distinctive identifier tokens around them.
STOP = set("""the a an and or for to of in on by is are was were be been being with without use using
used old new default defaults removed renamed replaced deprecated value values option options flag flags
mode modes config configs file files name names api apis function functions method methods class classes
module modules import imports version versions support server client connection connections error errors
true false none null sync async days hours minutes seconds tunnel native disabled enabled overlay string
strings bytes byte int integer bool boolean list dict set map maps key keys type types field fields
struct structs pointer pointers size length data code path paths port ports host hosts user users
password packet packets memory kernel program programs section sections helper helpers global globals
variable variables read write open close load unload attach detach create delete update query info
default-address strict partial routing routing-mode""".split())

IDENT = re.compile(r"[A-Za-z_][A-Za-z0-9_]*(?:[.\-/][A-Za-z0-9_]+)*(?:\(\))?")

# curated cross-name aliases: OLD tool/product names a stale user types INSTEAD of
# the lib token, that don't appear verbatim in a fact's `old` field. lib must exist.
MANUAL = {"crackmapexec": "netexec", "cme": "netexec", "nxc": "netexec"}

def natural_stems(lib):
    out = set()
    base = re.sub(r"[-_]?(py|python|js|3|v?\d+(\.\d+)*|x)$", "", lib)
    if base and base != lib and len(base) >= 4:
        out.add(base)
    return out

tok2libs = collections.defaultdict(set)
for fn in sorted(glob.glob(FD + "/*.jsonl")):
    if fn.endswith(".review.jsonl"): continue
    for l in open(fn, encoding="utf-8"):
        if not l.strip(): continue
        r = json.loads(l)
        lib = r["lib"]
        for stem in natural_stems(lib):
            tok2libs[stem].add(lib)
        if r.get("type") not in ("REPLACED", "REMOVED"):   # only renames/removals carry an OLD name
            continue
        old = str(r.get("old") or "")
        for m in IDENT.findall(old):
            t = m.lower().rstrip("()")
            if not t: continue
            # ONLY identifier-like tokens qualify: they must carry a separator ( . _ - / )
            # or a call marker (). Bare alpha words ("str", "bgp", "pod", "you") are
            # generic phrasing from a multi-word `old` value and would over-open the gate.
            distinctive = any(c in t for c in "._-/") or ("(" in m)
            if not distinctive or t in STOP or len(t) < 3:
                continue
            tok2libs[t].add(lib)

aliases = {}
libnames = {json.loads(next(open(f, encoding="utf-8")))["lib"] for f in glob.glob(FD + "/*.jsonl")
            if not f.endswith(".review.jsonl")}
for t, libs in sorted(tok2libs.items()):
    if len(libs) != 1: continue          # ambiguous -> drop
    lib = next(iter(libs))
    if t == lib or t in libnames: continue
    aliases[t] = lib
for t, lib in MANUAL.items():            # curated cross-name aliases (only if the lib is present)
    if lib in libnames and t not in libnames:
        aliases[t] = lib

json.dump(aliases, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=0, sort_keys=True)
print(f"{len(aliases)} aliases -> {OUT}")
per = collections.defaultdict(list)
for t, lib in sorted(aliases.items()): per[lib].append(t)
for lib in sorted(per): print(f"  {lib}: {', '.join(per[lib])}")
