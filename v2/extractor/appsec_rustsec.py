#!/usr/bin/env python3
"""appsec_rustsec.py - adapter: RustSec advisory-db -> insecure-by-default landmine facts.

Each advisory is TOML front-matter (package/categories/keywords/patched/affected.functions) + a
markdown prose body describing a real vulnerability in a Rust crate. Rust value is mostly TEXT facts
(a vulnerable crate/API usage and its fix); verbatim good/bad code pairs are rare -> ships text-only.

SELECTIVITY (the point): most RustSec entries are one-off crate CVEs with no reusable lesson. We keep
the ones that teach a general secure-coding rule (a named API that is insecure-by-default, a crypto/
validation/injection/deserialization mistake a dev would repeat) and skip pure "fixed in vX" one-liners,
unmaintained/notice maintenance flags, malicious-crate takedowns, and withdrawn advisories.

usage:  DEEPSEEK_API_KEY=$(cat /c/projects/api/deepseek.txt) python appsec_rustsec.py [--n N] [--stats] [--test]
out:    experts/appsec/facts/rustsec.jsonl (+ .rejects.jsonl)
"""
import glob, os, re, sys, tomllib
import appsec_core as C

HERE = os.path.dirname(os.path.abspath(__file__))
DB   = os.path.join(HERE, "..", "..", "appsec-corpus", "rustsec-advisory-db", "crates")
OUT  = "experts/appsec/facts/rustsec"
LICENSE_NOTE = "RustSec advisory-db, CC0"

# category -> retrieval door (only when the category maps cleanly; else let the LLM pick).
CAT_DOOR = {
    "crypto-failure":       "crypto",
    "format-injection":     "injection",
    "memory-corruption":    "memory-safety",
    "memory-exposure":      "memory-safety",
    "thread-safety":        "concurrency-race",
    "file-disclosure":      "web-appsec",
    "privilege-escalation": "auth-session",
}
# categories whose advisories most reliably teach a REUSABLE api-misuse lesson.
HIGH_LESSON = {"crypto-failure", "format-injection", "code-execution", "memory-exposure",
               "file-disclosure", "privilege-escalation"}
# maintenance / one-off flags that carry no secure-coding lesson -> drop.
SKIP_INFORMATIONAL = {"unmaintained", "notice"}
# low-bite for a CODE-GEN model: obscure per-crate memory-corruption / exposure / DoS CVEs. A model does not
# write these niche crate APIs by default, so they don't "bite". Drop an advisory ONLY if EVERY category it
# carries is low-bite (keep it when it also teaches a reusable lesson like crypto/injection/privilege).
LOW_BITE_ONLY = {"memory-corruption", "memory-exposure", "denial-of-service"}

LESSON_RE = re.compile(r"bypass|validat|sanitiz|inject|overflow|traversal|deserializ|"
                       r"constant[- ]time|timing|nonce|random|verif|certificate|"
                       r"authenticat|escap|panic|out[- ]of[- ]bounds|use[- ]after[- ]free|"
                       r"uninitializ|double[- ]free|signature|secret|padding|null", re.I)
API_RE = re.compile(r"`[^`]*(?:::|\(\))[^`]*`")


def parse(path):
    raw = open(path, encoding="utf-8").read()
    m = re.search(r"```toml\s*(.*?)```", raw, re.S)
    if not m:
        return None
    try:
        fm = tomllib.loads(m.group(1))
    except Exception:
        return None
    body = raw[m.end():].strip()
    adv = fm.get("advisory", {})
    title = ""
    tm = re.search(r"^#\s+(.*)$", body, re.M)
    if tm:
        title = tm.group(1).strip()
    has_funcs = bool(adv.get("affected", {}).get("functions") or
                     fm.get("affected", {}).get("functions") or
                     fm.get("affected.functions"))
    # tomllib nests [affected.functions] under affected->functions:
    has_funcs = has_funcs or bool(fm.get("affected", {}).get("functions"))
    funcs = list((fm.get("affected", {}).get("functions") or {}).keys())
    return {
        "id": adv.get("id", os.path.basename(path)[:-3]),
        "package": adv.get("package", ""),
        "categories": adv.get("categories", []) or [],
        "keywords": adv.get("keywords", []) or [],
        "informational": adv.get("informational"),
        "withdrawn": bool(adv.get("withdrawn")),
        "patched": (fm.get("versions", {}) or {}).get("patched", []),
        "aliases": adv.get("aliases", []) or [],
        "funcs": funcs,
        "title": title,
        "body": body,
        "path": path,
    }


def keeps(a):
    """Selectivity gate: True if this advisory likely teaches a reusable secure-coding lesson."""
    if a["withdrawn"]:
        return False
    if a["informational"] in SKIP_INFORMATIONAL:
        return False
    if "malicious" in a["categories"]:          # crate-takedown, not a coding pattern
        return False
    cats = set(a["categories"])
    if cats and cats <= LOW_BITE_ONLY:           # ONLY niche memory/DoS crate CVEs -> no reusable landmine
        return False
    body = a["body"]
    if len(body) < 120:                          # bare "fixed in vX" stub, nothing to learn
        return False
    score = 0
    if a["funcs"]:                               # names a concrete affected API -> reusable
        score += 3
    if HIGH_LESSON & set(a["categories"]):
        score += 2
    if API_RE.search(body):                      # backticked ::/() identifier in prose
        score += 1
    if len(body) >= 300:
        score += 1
    if LESSON_RE.search(body):
        score += 1
    a["_score"] = score
    return score >= 3


def door_for(a):
    for c in a["categories"]:
        if c in CAT_DOOR:
            return CAT_DOOR[c]
    return None


def make_item(a):
    L = [f"Rust crate: {a['package']}"]
    if a["categories"]:
        L.append("Category: " + ", ".join(a["categories"]))
    if a["funcs"]:
        L.append("Affected API(s): " + ", ".join(a["funcs"][:8]))
    if a["patched"]:
        L.append("Patched versions: " + ", ".join(str(p) for p in a["patched"]))
    L += ["", "ADVISORY:", a["body"]]
    llm_input = "\n".join(L)
    # ground the quote against the verbatim advisory prose (title + body).
    corpus = (a["title"] + "\n\n" + a["body"]) if a["title"] else a["body"]
    item = {
        "llm_input": llm_input,
        "corpus": corpus,
        "source": a["id"],
        "license_note": LICENSE_NOTE,
        "lib": a["package"],
        "version": "rustsec",
    }
    d = door_for(a)
    if d:
        item["door"] = d
    return item


def main():
    paths = sorted(glob.glob(os.path.join(DB, "**", "RUSTSEC-*.md"), recursive=True))
    advs = [x for x in (parse(p) for p in paths) if x]
    kept = [a for a in advs if keeps(a)]
    kept.sort(key=lambda a: -a["_score"])

    if "--stats" in sys.argv:
        from collections import Counter
        print(f"advisories parsed: {len(advs)}  kept by gate: {len(kept)}")
        print("kept category spread:", Counter(c for a in kept for c in a["categories"]).most_common())
        print("kept score spread:", Counter(a["_score"] for a in kept).most_common())
        print("dropped: unmaintained/notice=%d withdrawn=%d malicious=%d" % (
            sum(1 for a in advs if a["informational"] in SKIP_INFORMATIONAL),
            sum(1 for a in advs if a["withdrawn"]),
            sum(1 for a in advs if "malicious" in a["categories"])))
        return

    if "--test" in sys.argv:
        kept = kept[:4]
    elif "--n" in sys.argv:
        kept = kept[:int(sys.argv[sys.argv.index("--n") + 1])]
    else:
        kept = [a for a in kept if a["_score"] >= 6]   # top tier: names an API + a lesson signal

    # anti-redundancy nudge: the base SYS invites up to 4 facts and the model tends to restate the same
    # lesson under 3 different type labels (dedupe's token-Jaccard misses reworded restatements).
    extra = ("Emit AT MOST 2 facts for this advisory, and prefer ONE. Each fact must be a DISTINCT "
             "lesson; never restate the same lesson reworded or under a different type label (that is a "
             "duplicate). If the advisory teaches a single lesson, emit exactly one fact.")

    items = [make_item(a) for a in kept]
    print(f"RustSec: {len(advs)} advisories; mining {len(items)} selected (of {sum(1 for a in advs if keeps(a))} gated)")
    C.run(items, OUT, extra_sys=extra, id_prefix="rs")


if __name__ == "__main__":
    main()
