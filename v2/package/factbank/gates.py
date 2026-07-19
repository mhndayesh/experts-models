"""gates.py - the boundary gates. Code decides what enters the bank;
models only propose. (PLAN P4: quote / anchor / collision / self-retrieval,
plus schema.) A gate failure is a REASON, not an exception — callers get
(survivors, rejects-with-reasons) and nothing is ever silently dropped.
"""

import json
import re

import numpy as np

VALID_KINDS = {"doc", "signature", "example", "concept", "behavior",
               "removed"}

# extractors invent labels ("bug fix", "enhancement"...) — mapping them is
# a YIELD fix, not a safety loosening: kind is descriptive, never load-
# bearing. Measured live 2026-07-13: 3 of 12 e2b candidates died on
# invented kinds alone.
KIND_ALIASES = {"feature": "behavior", "enhancement": "behavior",
                "bug fix": "behavior", "bugfix": "behavior",
                "fix": "behavior", "change": "behavior",
                "performance": "concept", "deprecation": "removed",
                "deprecated": "removed", "breaking": "removed",
                "breaking change": "removed", "api": "signature"}


def normalize(c: dict) -> dict:
    k = str(c.get("kind", "doc")).strip().lower()
    return {**c, "kind": KIND_ALIASES.get(k, k)}

# identifier-ish: dotted path, call, snake_case, -f/--flag, OPT_CONST,
# CamelCase class — at least one exact search anchor (BM25 needs it).
# Single-dash flags added 2026-07-13 (F-036 rejects audit: `-q`/`-qq`
# were real anchors the gate was blind to).
_ANCHOR = re.compile(
    r"[A-Za-z_][\w]*\.[A-Za-z_][\w.]*|[A-Za-z_][\w]*\("
    r"|(?<![\w-])--?[a-z][\w-]+"
    r"|\b[a-z][a-z0-9]*_[a-z0-9_]+\b|\b[A-Z][A-Z0-9]*_[A-Z0-9_]+\b"
    r"|\b[A-Z][a-z0-9]+[A-Z][A-Za-z0-9]*\b")

_BACKTICK = re.compile(r"`([^`\n]{2,60})`")

_WS = re.compile(r"\s+")


def _canon(s: str) -> str:
    """Whitespace/quote-mark canonicalization for verbatim matching —
    changelogs re-wrap lines; that must not fail an honest quote."""
    s = s.replace("‘", "'").replace("’", "'")
    s = s.replace("“", '"').replace("”", '"')
    s = s.replace("`", "")
    return _WS.sub(" ", s).strip().lower()


def gate_schema(c: dict):
    for f in ("text", "quote"):
        if not str(c.get(f, "")).strip():
            return f"missing {f!r}"
    if c.get("kind", "doc") not in VALID_KINDS:
        return f"unknown kind {c.get('kind')!r}"
    words = len(c["text"].split())
    if not 5 <= words <= 100:
        return f"text is {words} words (atomic facts are ~20-80)"
    probes = c.get("probes") or []
    if not isinstance(probes, list) or not (1 <= len(probes) <= 5):
        return "needs 1-5 probe questions"
    return None


def gate_quote(c: dict, source_text: str):
    """The load-bearing gate: the model may only assert what it can point
    to. Verbatim modulo whitespace/quote canonicalization."""
    q = _canon(c["quote"])
    if len(q) < 15:
        return "quote too short to anchor a claim (<15 chars)"
    if q not in _canon(source_text):
        return "quote not found verbatim in the source"
    return None


def _quote_span_in_text(c: dict) -> bool:
    """Backticked spans in the quote are source-blessed code marks
    (`uv tree`, `-q`, `file://`, `strict`) — the quote gate has already
    verified the quote verbatim, so a span reappearing in the text is a
    real anchor even when no regex class matches it (F-036 audit: bare
    CLI subcommands and short flags were true facts lost to the regex).
    Runs AFTER gate_quote by run_gates order — never trust an unverified
    quote for anchoring."""
    text = str(c.get("text", "")).lower()
    for span in _BACKTICK.findall(str(c.get("quote", ""))):
        s = span.strip().lower()
        if len(s) < 2:
            continue
        if re.fullmatch(r"[a-z][a-z0-9]*", s):   # plain word: whole-word
            if re.search(rf"\b{re.escape(s)}\b", text):   # `list`≠"lists"
                return True
        elif s in text:                          # flags, bigrams, uris
            return True
    return False


def gate_anchor(c: dict):
    if _ANCHOR.search(c["text"]) or _quote_span_in_text(c):
        return None
    return ("no identifier anchor (dotted path / call / flag / const / "
            "quote-marked span)")


def gate_collision(c: dict, bank_vectors, encode, threshold: float = 0.95):
    """Near-duplicate vs the existing bank. Needs an encoder; caller may
    pass encode=None to skip (reported as skipped, not passed)."""
    if encode is None or bank_vectors is None or not len(bank_vectors):
        return None
    v = encode([f"search_document: {c['text']}"])[0]
    v = np.asarray(v, dtype=np.float32)
    v = v[: bank_vectors.shape[1]]
    v /= (np.linalg.norm(v) + 1e-9)
    sim = float((bank_vectors @ v).max())
    if sim > threshold:
        return f"near-duplicate of an existing fact (cos {sim:.3f})"
    return None


def run_gates(candidates: list[dict], source_text: str,
              bank_vectors=None, encode=None):
    """-> (survivors, rejects) where rejects = [(candidate, reason)]."""
    ok, bad = [], []
    for raw in candidates:
        c = normalize(raw)
        reason = (gate_schema(c) or gate_quote(c, source_text)
                  or gate_anchor(c)
                  or gate_collision(c, bank_vectors, encode))
        (bad.append((c, reason)) if reason else ok.append(c))
    return ok, bad


def stamp(candidates: list[dict], source: str, version: str, url: str,
          existing_ids: set) -> list[dict]:
    """Pipeline-owned fields: the model never writes provenance."""
    out = []
    n = 1
    for c in candidates:
        while f"{source}-a{n:03d}" in existing_ids:
            n += 1
        fid = f"{source}-a{n:03d}"
        existing_ids.add(fid)
        out.append({"id": fid, "text": c["text"].strip(),
                    "source": source, "version": version,
                    "kind": c.get("kind", "doc"),
                    "meta": {"url": url, "quote": c["quote"].strip(),
                             "probes": c.get("probes", []),
                             "extracted": True}})
        n += 1
    return out
