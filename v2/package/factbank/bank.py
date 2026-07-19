"""VENDORED SNAPSHOT of NEW BANK/factbank/factbank/bank.py (2026-07-13, post live-smoke).
The research tree is the lab; this package ships the evaluated system. Do not
edit here without syncing intent with the lab copy.


bank.py - The frozen fact bank.

Stores facts as JSONL, searches with BM25 (v1) behind a swappable interface.
Implements the design fixes:
  - Hole 2 fix: prompt-key hits ranked above draft-key hits, draft-key capped.
  - Hole 3 fix: relevance threshold, below it a fact is not injected.
  - Hole 4 fix: version filter on retrieval.
"""

import json
import re
from dataclasses import dataclass, field
from rank_bm25 import BM25Okapi


_STOPWORDS = {
    "a", "an", "the", "is", "are", "was", "be", "to", "of", "in", "on",
    "for", "with", "and", "or", "how", "do", "i", "my", "it", "this",
    "that", "can", "does", "what", "when", "use", "using", "not", "no",
    "there", "via", "after", "set",
}


def _tokenize(text: str) -> list[str]:
    """Code-aware tokenizer: splits identifiers, keeps dotted API paths,
    drops stopwords so they cannot pollute BM25 ranking."""
    text = text.lower()
    # keep dotted paths like requests.get as their own token AND parts
    dotted = re.findall(r"[a-z_][a-z0-9_]*(?:\.[a-z_][a-z0-9_]*)+", text)
    words = [w for w in re.findall(r"[a-z0-9_]+", text)
             if w not in _STOPWORDS]
    return words + dotted


@dataclass
class Fact:
    id: str
    text: str          # the fact itself: signature, doc snippet, example
    source: str        # library / module name
    version: str       # mandatory version tag, e.g. "2.x", "3.12"
    kind: str = "doc"  # doc | signature | example | concept | landmine
    meta: dict = field(default_factory=dict)

    def render(self) -> str:
        return f"[{self.source} {self.version} | {self.kind}] {self.text}"

    # Pipeline-metadata keys that live on lab rows but are not part of the Fact.
    _EXPERT_META = ("type", "subject", "old", "new", "why_it_bites", "quote",
                    "keywords", "lib")

    @classmethod
    def from_row(cls, d: dict) -> "Fact":
        """Load a Fact from EITHER schema.

        * Native package rows carry `text`/`source` -> taken as-is (unknown keys
          folded into meta so a stray field never crashes the loader).
        * Lab/expert rows (the fact-extractor's schema: `truth`/`lib`/`type`/...)
          are mapped: text<-truth (symbol-prefixed if the api name is absent),
          source<-lib, kind='landmine', and the landmine structure preserved in
          meta. This is the "package adapts to the canonical lab schema" direction
          (see v2/extractor/SCHEMA.md) so ANY shipped bank loads without a
          separate conversion step.
        """
        d = {k: v for k, v in d.items() if not str(k).startswith("_")}  # drop _repaired/_flags/...
        if "text" in d and "source" in d:                              # native row
            known = {"id", "text", "source", "version", "kind", "meta"}
            meta = dict(d.get("meta") or {})
            meta.update({k: v for k, v in d.items() if k not in known})
            return cls(id=d["id"], text=d["text"], source=d["source"],
                       version=str(d.get("version") or "multi"),
                       kind=d.get("kind", "doc"), meta=meta)
        # lab / expert landmine row
        truth = (d.get("truth") or "").strip()
        kw = d.get("keywords") or {}
        ff = kw.get("from_fact") or []
        sym = next((k for k in ff if any(c in k for c in ".(")), (ff[0] if ff else ""))
        text = truth if (not sym or sym.split(".")[-1].lower() in truth.lower()) \
            else f"{sym}: {truth}"
        meta = {k: d[k] for k in cls._EXPERT_META if k in d}
        return cls(id=d["id"], text=text or (d.get("quote") or ""),
                   source=d.get("lib") or d.get("source") or "?",
                   version=str(d.get("version") or "multi"),
                   kind="landmine", meta=meta)


class Bank:
    """Read-only at runtime. Build offline, load, search."""

    def __init__(self, facts: list[Fact]):
        if not facts:
            # BM25Okapi([]) dies with ZeroDivisionError (audit find). An empty
            # bank is a configuration error, not a search result -- fail loud.
            raise ValueError("Bank requires at least one fact "
                             "(empty facts list / empty JSONL?)")
        self.facts = facts
        self._corpus_tokens = [_tokenize(f.text + " " + f.source) for f in facts]
        self._bm25 = BM25Okapi(self._corpus_tokens)

    # ---------- construction ----------

    @classmethod
    def from_jsonl(cls, path: str) -> "Bank":
        facts = []
        with open(path, encoding="utf-8") as fh:   # explicit: Windows default cp1252 corrupts banks
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                d = json.loads(line)
                facts.append(Fact.from_row(d))
        return cls(facts)

    # ---------- search ----------

    def search(self, query: str, k: int = 5,
               version_filter: str | None = None,
               min_score: float = 1.0) -> list[tuple[Fact, float]]:
        """Single-key search with relevance threshold (hole 3 fix)
        and version filter (hole 4 fix).

        RETRIEVE FIRST, FILTER SECOND. The version filter must never decide
        WHICH LIBRARY comes back -- only which VERSION of an already-relevant
        fact.

        (FINDINGS F-019: filtering during ranking let the filter cull the right
        library and promote a wrong one that merely shared a version number.
        "Migrate this pydantic v1 model to v2" detected version "1", dropped
        every pydantic fact (tagged 2.x), and returned POLARS facts -- because
        polars is tagged 1.x. The bank did not go empty, so fail-open never
        fired; it went confidently, authoritatively WRONG. That is the "right
        fact, wrong context" failure the design doc calls more dangerous than a
        wrong fact.)
        """
        scores = self._bm25.get_scores(_tokenize(query))
        ranked = sorted(enumerate(scores), key=lambda x: -x[1])

        # stage 1: relevance only. The candidate pool decides the LIBRARY.
        pool: list[tuple[Fact, float]] = []
        for idx, score in ranked:
            if score < min_score:
                break                      # below threshold: nothing further
            pool.append((self.facts[idx], float(score)))
            if len(pool) >= k * 4:         # deep enough to hold both versions
                break

        # stage 2: version filter, applied WITHIN the relevant pool only.
        return apply_version_filter(pool, version_filter, k)

    @property
    def sources(self) -> list[str]:
        return sorted({f.source for f in self.facts})

    def double_key_search(self, prompt: str, draft: str,
                          k_prompt: int = 5, k_draft: int = 3,
                          version_filter: str | None = None,
                          min_score: float = 1.0) -> list[Fact]:
        """The core lookup of the architecture.

        Hole 2 fix: prompt-key results come first and draft-key is capped
        (k_draft < k_prompt) so a poisoned draft cannot dominate the facts.
        """
        def lookup(vf):
            p = self.search(prompt, k=k_prompt, version_filter=vf,
                            min_score=min_score)
            d = self.search(draft, k=k_draft, version_filter=vf,
                            min_score=min_score)
            seen: set[str] = set()
            merged: list[Fact] = []
            for f, _ in p + d:              # prompt first = higher rank
                if f.id not in seen:
                    seen.add(f.id)
                    merged.append(f)
            return merged

        hits = lookup(version_filter)
        # FAIL OPEN, never shut. If the version filter wiped out every hit, a
        # misdetected version is far likelier than "the bank truly has nothing
        # for this query" -- and answering with NO facts is the failure the
        # bank exists to prevent. Better an unfiltered fact than none.
        if version_filter and not hits:
            hits = lookup(None)
        return hits


def apply_version_filter(pool, version_filter, k):
    """Stage 2 for BOTH banks (F-031): filter an already-ranked pool.

    version_filter may be:
      None      -> no filtering
      str       -> legacy global filter (kept for old callers/tests)
      dict      -> per-source constraints from detect_version_map():
                   - a NAMED library ("pydantic": "2") culls that library's
                     mismatching facts only;
                   - "python" binds SOFTLY to python-versioned facts: they
                     are deranked behind matching ones, never culled --
                     the correct answer to a 3.13 user asking about a 3.14
                     module IS the 3.14-tagged boundary fact.

    STRUCTURAL GUARANTEE (the audit's point): if a named-source constraint
    would remove EVERY fact of the top-ranked source -- i.e. the version
    filter is about to replace the LIBRARY relevance chose -- the filter
    loses and the pool returns unfiltered. Relevance picks the library;
    version only ever picks among versions of it.
    """
    if not version_filter:
        return pool[:k]
    if isinstance(version_filter, dict):
        py = version_filter.get("python")
        keep, soft = [], []
        for f, s in pool:
            src = f.source.lower()
            if src in version_filter and src != "python":
                if _version_match(f.version, version_filter[src]):
                    keep.append((f, s))
                continue
            if py and f.version.strip().startswith("3") \
                    and not _version_match(f.version, py):
                soft.append((f, s))
            else:
                keep.append((f, s))
        if pool:
            top_src = pool[0][0].source.lower()
            if top_src in version_filter and top_src != "python" \
                    and not any(f.source.lower() == top_src
                                for f, _ in keep + soft):
                return pool[:k]        # filter tried to choose the library
            # The #1 relevance hit is NEVER deranked. l-h2: the boundary
            # fact ("annotationlib does not exist before 3.14") outscored
            # everything 2:1 and soft-derank still buried it under weaker
            # 3.13-matching facts. Version may reorder the rest of the
            # pool; it does not outrank the single most relevant fact.
            if soft and soft[0] == pool[0]:
                keep.insert(0, soft.pop(0))
        return (keep + soft)[:k]
    return [(f, s) for f, s in pool
            if _version_match(f.version, version_filter)][:k]


def _version_match(fact_version: str, wanted: str) -> bool:
    """Match with the precision the filter specifies.
    wanted='3.12' requires the fact's first two components to be 3.12
    (a fact tagged '3.13' does NOT match). wanted='2' matches any 2.*.
    'x' in a fact version is a wildcard for that component."""
    fparts = fact_version.strip().lower().split(".")
    wparts = wanted.strip().lower().split(".")
    for i, wp in enumerate(wparts):
        fp = fparts[i] if i < len(fparts) else "x"
        if fp == "x" or wp == "x":
            continue
        if fp != wp:
            return False
    return True


# Version tags must be ANCHORED to a version-ish word. A bare number in code
# is not a version. (FINDINGS F-010: a draft containing
# `if response.status_code == 404:` was read as "version 404", the filter then
# matched no fact, and the ENTIRE BANK was silently discarded. The old bare
# patterns `==\s*(\d+)` and `\b\d+\.\d+\b` also swallowed every float in a
# prompt -- backoff_factor=0.5 became "version 0.5".)
_VERSION_PATS = [
    # "python 3.12", "python3.12"
    r"\bpython\s*(\d+(?:\.\d+)*)",
    # "v3", "version 3.12", "version=2"
    r"\bv(?:ersion)?[\s=]*(\d+(?:\.\d+)+)\b",
    r"\bv(\d+)\b",
    # pinned requirement: "requests==2.31", "pandas>=2.0".
    # TWO guards keep code comparisons out:
    #   no whitespace around the operator -- pip pins are written tight
    #     ("requests==2.31"), code comparisons are spaced ("status_code == 404")
    #   the version must contain a dot -- "404" and "200" are not versions
    r"\b[a-z_][a-z0-9_.-]*(?:==|>=|~=)(\d+\.\d+(?:\.\d+)*)",
]


# A MIGRATION names two versions, and the one the user cares about is the
# TARGET. "Migrate this pydantic v1 model to v2" used to detect "1" -- the
# version being LEFT -- which culled every pydantic 2.x fact (F-019, and the
# audit's per-library criticism). Direction patterns are checked FIRST.
_MIGRATION_PATS = [
    # anchored by a 'v' on either side: "v1 to v2", "v1 -> 2", "1 into v2"
    r"\bv(\d+(?:\.\d+)*)\s*(?:->|→|to|into)\s*v?(\d+(?:\.\d+)*)",
    r"\bv?(\d+(?:\.\d+)*)\s*(?:->|→|to|into)\s*v(\d+(?:\.\d+)*)",
    # anchored by '.x': "1.x to 2.x", "0.x -> 1"
    r"\b(\d+)\.x\s*(?:->|→|to|into)\s*(\d+)(?:\.x)?\b",
    # anchored by a migration VERB, dotted source: "upgrade polars 0.19 to 1.0"
    # (a bare "10 to 60" NEVER matches -- "increase timeout from 10 to 60"
    # must not be read as a version migration)
    r"\b(?:migrat\w+|port\w*|upgrad\w+|mov\w+|switch\w+)\b[^.!?]{0,60}?"
    r"\bv?(\d+\.\d+(?:\.\d+)*)\s*(?:->|→|to|into)\s*v?(\d+(?:\.\d+)*)",
    # verb + only the target named: "migrate the loader to v3"
    r"\b(?:migrat\w+|port\w*|upgrad\w+|mov\w+|switch\w+)\b[^.!?]{0,60}?"
    r"\bto\s+v(\d+(?:\.\d+)*)",
]


def detect_version(text: str, library: str | None = None) -> str | None:
    """Best-effort version detection from prompt or draft (hole 4 fix).

    Detects 'python 3.12', 'v3', 'version 2.1', 'requests==2.31', and
    '<library> 2' when a library hint is given. Deliberately does NOT treat a
    bare number or bare decimal as a version -- see _VERSION_PATS.

    Migration prompts ("v1 to v2") return the TARGET version -- the docs the
    user needs describe where they are GOING, not what they are leaving.
    """
    low = text.lower()
    for p in _MIGRATION_PATS:
        m = re.search(p, low)
        if m:
            return m.group(m.lastindex)          # last group = the target
    pats = list(_VERSION_PATS)
    if library:
        pats.insert(0, rf"\b{re.escape(library.lower())}\s*"
                       rf"(?:v|==|>=|~=)?\s*(\d+(?:\.\d+)*)")
    for p in pats:
        m = re.search(p, low)
        if m:
            return m.group(1)
    return None


def detect_version_map(text: str, sources: list[str]) -> dict[str, str]:
    """PER-SOURCE version constraints (F-031).

    One global version for the whole prompt is wrong the moment two versioned
    things are named: "On Python 3.13 use pydantic v2 model_dump" detected
    '3.13' and the global filter then deleted every pydantic 2.x fact. A
    version can only constrain THE LIBRARY IT WAS WRITTEN NEXT TO.

    Returns {source: version}. "python X.Y" is stored under "python" -- the
    caller decides which facts that binds to (stdlib-sourced ones), and binds
    it SOFTLY (prefer, never cull: the correct answer to a 3.13 user asking
    about a 3.14 module IS the 3.14-tagged boundary fact -- hard-culling it
    is how l-h2 became unwinnable, see FINDINGS).

    Migration direction applies per source too: "migrate pydantic 1 to 2"
    binds pydantic to the TARGET, 2.
    """
    low = text.lower()
    out: dict[str, str] = {}
    m = re.search(r"\bpython\s*(\d+(?:\.\d+)*)", low)
    if m:
        out["python"] = m.group(1)
    for src in sources:
        s = re.escape(src.lower())
        # migration next to the source name: "pydantic v1 ... to v2",
        # "pydantic 1 to 2", "upgrade polars 0.19 to 1.0"
        m = re.search(rf"{s}\s+v?(\d+(?:\.\d+)*)\s*(?:->|→|to|into)\s*"
                      rf"v?(\d+(?:\.\d+)*)", low)
        if m:
            out[src] = m.group(2)
            continue
        m = re.search(rf"{s}\s*(?:v|==|>=|~=|version\s*)?(\d+(?:\.\d+)*)\b",
                      low)
        if m and (m.group(0)[len(src):].strip()[:1] in "v=~>" or
                  "." in m.group(1) or len(m.group(1)) == 1):
            out[src] = m.group(1)
    return out
