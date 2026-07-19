"""watch.py - the auto-updater. The bank is its own watch list.

Flow per library found in the bank: PyPI JSON API (version + GitHub link)
-> GitHub releases API (notes for the missed versions) -> quote-gated
extraction (extract.py + gates.py, quotes matched against the release
notes) -> proposals -> FULL-AUTO apply (owner default) with snapshot,
atomic write, health check, rollback. Outbound requests carry ONLY
library names; user data never leaves the machine. `--offline` upstream
of this module simply never calls it.
"""

import json
import os
import re
import shutil
import time
import urllib.request

from .gates import run_gates, stamp

UA = {"User-Agent": "factbank-watch/0.1"}


def _get_json(url: str, timeout: int = 20):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read())


def vtuple(v: str):
    nums = re.findall(r"\d+", str(v))
    return tuple(int(x) for x in nums[:4]) if nums else None


def pypi_latest(name: str):
    """-> (version, github 'owner/repo' or None) or None on any failure."""
    try:
        d = _get_json(f"https://pypi.org/pypi/{name}/json")
    except Exception:
        return None
    ver = d.get("info", {}).get("version")
    gh = None
    urls = d.get("info", {}).get("project_urls") or {}
    for u in list(urls.values()) + [d.get("info", {}).get("home_page")]:
        m = re.match(r"https?://github\.com/([\w.-]+/[\w.-]+)/?", str(u))
        if m:
            gh = m.group(1).removesuffix(".git")
            break
    return (ver, gh) if ver else None


def github_release_notes(owner_repo: str, newer_than, limit: int = 10):
    """Concatenated bodies of releases newer than the bank's version."""
    try:
        rels = _get_json(f"https://api.github.com/repos/{owner_repo}"
                         f"/releases?per_page={limit}")
    except Exception:
        return ""
    chunks = []
    for r in rels:
        vt = vtuple(r.get("tag_name", ""))
        if vt and newer_than and vt <= newer_than:
            continue
        body = r.get("body") or ""
        if body.strip():
            chunks.append(f"# {r.get('tag_name')} — "
                          f"{r.get('name') or ''}\n{body}")
    return "\n\n".join(chunks)


def scan(bank_path: str, extractor, sources_filter=None,
         log=print) -> list[dict]:
    """-> proposals (stamped fact dicts). Network + extraction, NO bank
    writes — apply() is a separate, snapshotted step."""
    facts = [json.loads(l) for l in open(bank_path, encoding="utf-8")
             if l.strip()]
    ids = {f["id"] for f in facts}
    by_src = {}
    for f in facts:
        by_src.setdefault(f["source"], []).append(f)

    proposals, rejects = [], []
    for src, group in sorted(by_src.items()):
        if sources_filter and src not in sources_filter:
            continue
        have = max((vtuple(f.get("version")) or (0,) for f in group))
        info = pypi_latest(src)
        if not info:
            log(f"[watch] {src}: not on PyPI / unreachable — skipped")
            continue
        latest, gh = info
        if (vtuple(latest) or (0,)) <= have:
            log(f"[watch] {src}: up to date "
                f"(bank {'.'.join(map(str, have))}, pypi {latest})")
            continue
        log(f"[watch] {src}: bank {'.'.join(map(str, have))} -> "
            f"pypi {latest} — fetching release notes"
            + (f" ({gh})" if gh else ""))
        notes = github_release_notes(gh, have) if gh else ""
        if not notes.strip():
            log(f"[watch] {src}: no usable release notes — flagged for "
                f"manual review (sources.toml override)")
            continue
        try:
            cands = extractor(notes[:12000], src, latest)
        except Exception as e:   # Truncated, network, upstream 5xx
            log(f"[watch] {src}: extraction FAILED — {e} — skipped "
                f"(NOT '0 candidates')")
            continue
        url = f"https://github.com/{gh}/releases" if gh else \
            f"https://pypi.org/project/{src}/"
        ok, bad = run_gates(cands, notes)
        for c, why in bad:
            log(f"[gates] {src}: rejected ({why}): "
                f"{str(c.get('text'))[:70]}")
            rejects.append({"source": src, "why": why,
                            "text": c.get("text"), "kind": c.get("kind"),
                            "quote": c.get("quote")})
        proposals.extend(stamp(ok, src, latest, url, ids))
        log(f"[watch] {src}: {len(ok)} proposal(s), {len(bad)} rejected")
    if rejects:   # full texts, so a rejection can be audited, not guessed
        rp = bank_path + ".rejects.jsonl"
        with open(rp, "w", encoding="utf-8") as fh:
            for r in rejects:
                fh.write(json.dumps(r, ensure_ascii=False) + "\n")
        log(f"[watch] {len(rejects)} reject(s) in full -> {rp}")
    return proposals


PENDING = ".pending.jsonl"


def write_pending(bank_path: str, proposals: list[dict]) -> str:
    p = bank_path + PENDING
    with open(p, "w", encoding="utf-8") as fh:
        for f in proposals:
            fh.write(json.dumps(f, ensure_ascii=False) + "\n")
    return p


def snapshot(bank_path: str) -> str:
    snap = f"{bank_path}.bak-{time.strftime('%Y%m%d-%H%M%S')}"
    shutil.copyfile(bank_path, snap)
    return snap


def health_check(bank_path: str) -> bool:
    """Post-apply sanity: bank still parses, ids unique, BM25 finds a new
    fact by its own probe (cheap, offline)."""
    try:
        from .bank import Bank, Fact
        facts = [json.loads(l) for l in open(bank_path, encoding="utf-8")
                 if l.strip()]
        if len({f["id"] for f in facts}) != len(facts):
            return False
        bank = Bank([Fact(**f) for f in facts])
        new = [f for f in facts if f.get("meta", {}).get("extracted")]
        for f in new[-3:]:
            probes = f.get("meta", {}).get("probes") or []
            if not probes:
                continue
            top = [x.id for x, _ in bank.search(probes[0], k=8,
                                                min_score=0.0)]
            if f["id"] not in top:
                return False
        return True
    except Exception:
        return False


def apply(bank_path: str, proposals: list[dict], log=print):
    """Snapshot -> atomic append -> health check -> rollback on failure."""
    if not proposals:
        log("[apply] nothing to apply")
        return True
    snap = snapshot(bank_path)
    tmp = bank_path + ".tmp"
    shutil.copyfile(bank_path, tmp)
    with open(tmp, "a", encoding="utf-8") as fh:
        for f in proposals:
            fh.write(json.dumps(f, ensure_ascii=False) + "\n")
    os.replace(tmp, bank_path)
    if health_check(bank_path):
        log(f"[apply] {len(proposals)} fact(s) applied  "
            f"(snapshot: {os.path.basename(snap)})")
        pend = bank_path + PENDING
        if os.path.exists(pend):
            os.unlink(pend)
        return True
    shutil.copyfile(snap, bank_path)
    log("[apply] HEALTH CHECK FAILED — rolled back to snapshot")
    return False
