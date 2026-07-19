#!/usr/bin/env python3
"""dedupe.py - collapse PARAPHRASE-duplicate facts and flag quote/truth mismatches.

The content-hash id dedup in extract.py only catches BYTE-identical facts. Long,
repetitive migration guides (capstone v6, libbpf, OpenZeppelin...) restate the same
breaking change across sections; each chunk paraphrases it differently, so the hashes
differ and duplicates survive. This pass groups facts by token-set similarity of
(subject + old + new) and keeps ONE representative per cluster (the longest `truth`,
i.e. the most complete statement).

It also FLAGS (never auto-drops) facts whose `quote` barely overlaps their own
old/new/truth - a sign the verbatim anchor got attached to the wrong sentence
(e.g. an ARM claim carrying a RISC-V quote). Flagged facts go to .review.jsonl for
a human read; they are NOT written to the deduped output.

Reading is still the verdict: this only TRIAGES. Read the .dedup-report.txt and the
.review.jsonl before trusting the kept set.

usage: python dedupe.py <facts.jsonl> [sim_threshold=0.6]
out:   <facts>.dedup.jsonl   (kept representatives)
       <facts>.review.jsonl  (quote/truth-mismatch flags to hand-read)
       <facts>.dedup-report.txt (every merge group, for audit)
"""
import json, re, sys

STOP = set("the a an is are was were to of in for now no longer not and or it its with by "
           "as be been being that this which you your stop using use instead new old previously "
           "before after them they there here on at from into only also more less than".split())
TOK = re.compile(r"[a-z0-9_]+")

def toks(*vals):
    out = set()
    for v in vals:
        if not v: continue
        for t in TOK.findall(str(v).lower()):
            if t not in STOP and len(t) > 1:
                out.add(t)
    return out

def jaccard(a, b):
    if not a or not b: return 0.0
    i = len(a & b)
    return i / len(a | b)

def subset(a, b):
    if not a or not b: return False
    s, l = (a, b) if len(a) <= len(b) else (b, a)
    return len(s & l) / len(s) >= 0.85   # small set almost entirely inside the large one

def main():
    src = sys.argv[1]
    thr = float(sys.argv[2]) if len(sys.argv) > 2 else 0.6
    facts = [json.loads(l) for l in open(src, encoding="utf-8") if l.strip()]
    for f in facts:
        f["_sig"] = toks(f.get("subject"), f.get("old"), f.get("new"))
        f["_qtok"] = toks(f.get("quote"))
        f["_btok"] = toks(f.get("subject"), f.get("old"), f.get("new"), f.get("truth"))

    # quote/truth mismatch flag: verbatim anchor should share vocabulary with the claim
    review, body = [], []
    for f in facts:
        ov = jaccard(f["_qtok"], f["_btok"])
        if ov < 0.15 and f["_qtok"]:
            f["_flag"] = f"quote/claim overlap {ov:.2f}"
            review.append(f)
        else:
            body.append(f)

    # greedy similarity clustering on the claim signature
    clusters = []
    for f in body:
        placed = False
        for c in clusters:
            rep = c[0]
            if jaccard(f["_sig"], rep["_sig"]) >= thr or subset(f["_sig"], rep["_sig"]):
                c.append(f); placed = True; break
        if not placed:
            clusters.append([f])

    kept, report = [], []
    for c in clusters:
        rep = max(c, key=lambda x: len((x.get("truth") or "")))   # most complete statement
        kept.append(rep)
        if len(c) > 1:
            report.append("MERGED %d -> kept %s\n   keep: %s\n%s" % (
                len(c), rep["id"], rep.get("truth", "")[:110],
                "\n".join("   drop: %s | %s" % (x["id"], (x.get("truth") or "")[:100])
                          for x in c if x is not rep)))

    for f in facts:
        for k in ("_sig", "_qtok", "_btok"):
            f.pop(k, None)
    out = src.replace(".jsonl", "") + ".dedup.jsonl"
    rev = src.replace(".jsonl", "") + ".review.jsonl"
    rpt = src.replace(".jsonl", "") + ".dedup-report.txt"
    with open(out, "w", encoding="utf-8") as fh:
        for f in kept: f.pop("_flag", None); fh.write(json.dumps(f, ensure_ascii=False) + "\n")
    with open(rev, "w", encoding="utf-8") as fh:
        for f in review: fh.write(json.dumps(f, ensure_ascii=False) + "\n")
    with open(rpt, "w", encoding="utf-8") as fh:
        fh.write("\n\n".join(report) if report else "no merges")
    print(f"{len(facts)} in -> {len(kept)} kept, {len(facts)-len(body)} flagged for review, "
          f"{len(body)-len(kept)} paraphrase-dups merged")
    print(f"  kept   -> {out}")
    print(f"  review -> {rev}   ({len(review)} facts; hand-read)")
    print(f"  report -> {rpt}")

if __name__ == "__main__":
    main()
