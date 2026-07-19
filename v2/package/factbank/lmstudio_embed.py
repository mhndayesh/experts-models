"""VENDORED SNAPSHOT of NEW BANK/factbank/factbank/lmstudio_embed.py (2026-07-13, post live-smoke).
The research tree is the lab; this package ships the evaluated system. Do not
edit here without syncing intent with the lab copy.


lmstudio_embed.py - Embeddings retrieval backed by LM Studio, plus a hybrid
bank that unions BM25 with embeddings.

Why: FINDINGS F-005 (BM25 missed `raise_for_status` -- a fact the bank was
holding) and F-004 (the min_score threshold leaked a pathlib fact into
"what is a Python decorator?"). Retrieval, not the loop, was the top failure
source in run 2.

nomic-embed-text-v1.5 is trained with ASYMMETRIC task prefixes. Facts must be
embedded as `search_document:` and queries as `search_query:`. embed_bank.py's
EmbedBank uses one encoder for both, so it cannot express this -- hence the
subclass here rather than a plain drop-in.

HybridBank = BM25 (unbeatable on exact identifiers, which is what a draft is
full of) UNION embeddings (handles paraphrase, which is what a user prompt is
full of). TECHNICAL.md 5 calls this the best production setup; F-005 is the
reason it is no longer optional.
"""

import json
import urllib.request

import numpy as np

from .bank import Bank, Fact, _version_match, apply_version_filter

EMBED_MODEL = "text-embedding-nomic-embed-text-v1.5"
BASE_URL = "http://127.0.0.1:1234/v1"


def lmstudio_encode(texts: list[str], base_url: str = BASE_URL,
                    model: str = EMBED_MODEL) -> np.ndarray:
    body = json.dumps({"model": model, "input": texts}).encode()
    req = urllib.request.Request(
        f"{base_url}/embeddings", data=body,
        headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as resp:
        data = json.loads(resp.read())
    rows = sorted(data["data"], key=lambda d: d["index"])
    return np.asarray([r["embedding"] for r in rows], dtype=np.float32)


def _norm(M: np.ndarray) -> np.ndarray:
    return M / (np.linalg.norm(M, axis=1, keepdims=True) + 1e-9)


def doc_strings(facts: list) -> list[str]:
    """The exact strings the bank matrix is built from — single-sourced so
    the cache writer and the live encoder can never diverge."""
    return [f"search_document: {f.text} ({f.source})" for f in facts]


class EmbedBankLM:
    """Embeddings-only bank with nomic's asymmetric query/document prefixes.

    matrix: optional prebuilt (already normalized, possibly Matryoshka-
    reduced) bank matrix — the F-034 cache path. Queries are sliced to the
    matrix's dims at search time."""

    def __init__(self, facts: list[Fact], encode=lmstudio_encode,
                 matrix: np.ndarray | None = None):
        self.facts = facts
        self.encode = encode
        if matrix is not None:
            self._M = matrix
        else:
            self._M = _norm(encode(doc_strings(facts)))

    @classmethod
    def from_jsonl(cls, path: str, encode=lmstudio_encode) -> "EmbedBankLM":
        facts = [Fact(**json.loads(l)) for l in open(path) if l.strip()]
        return cls(facts, encode)

    def search(self, query: str, k: int = 5, version_filter: str | None = None,
               min_score: float = 0.5) -> list[tuple[Fact, float]]:
        """RETRIEVE FIRST, FILTER SECOND (F-019). The version filter picks the
        VERSION of an already-relevant fact; it must never pick the LIBRARY."""
        if not query.strip():
            return []
        q = _norm(self.encode([f"search_query: {query}"]))[0]
        if self._M.shape[1] < q.shape[0]:   # Matryoshka-reduced matrix
            q = q[: self._M.shape[1]]
            q = q / (np.linalg.norm(q) + 1e-9)
        sims = self._M @ q

        pool: list[tuple[Fact, float]] = []      # stage 1: relevance only
        for idx in np.argsort(-sims):
            s = float(sims[idx])
            if s < min_score:
                break
            pool.append((self.facts[idx], s))
            if len(pool) >= k * 4:
                break

        # stage 2: within the pool only -- shared helper handles str|dict
        # per-source semantics and the never-choose-the-library guarantee
        return apply_version_filter(pool, version_filter, k)


class HybridBank:
    """BM25 UNION embeddings. Each side keeps its own score scale and its own
    threshold; we merge on fact id.

    Ordering preserves the hole-2 fix: prompt-key hits outrank draft-key hits,
    so a poisoned draft cannot dominate the fact block.
    """

    # Thresholds calibrated on the 9-case retrieval diagnostic, not guessed:
    #
    #   embeddings : every RELEVANT top hit scored >= 0.701
    #                every IRRELEVANT top hit scored <= 0.658
    #                -> 0.68 separates them perfectly. (kills F-004)
    #
    #   BM25       : CANNOT be separated by any threshold. The relevant fact
    #                for "raise an error on failed status" scores 1.25, while
    #                an irrelevant pathlib fact scores 1.63 on "reverse a
    #                string". A wrong fact outranks a right one, so no cut
    #                keeps the first and drops the second. We therefore demote
    #                BM25 to a HIGH-PRECISION channel only (>=2.0): it fires
    #                just on strong exact-identifier matches, which is what
    #                it is genuinely unbeatable at. Embeddings carry recall.
    def __init__(self, facts: list[Fact], encode=lmstudio_encode,
                 bm25_min: float = 2.0, cos_min: float = 0.68,
                 emb: "EmbedBankLM | None" = None):
        self.facts = facts
        self.bm25 = Bank(facts)
        self.emb = emb if emb is not None else EmbedBankLM(facts, encode)
        self.bm25_min = bm25_min
        self.cos_min = cos_min

    @classmethod
    def from_jsonl(cls, path: str, **kw) -> "HybridBank":
        facts = [Fact(**json.loads(l)) for l in open(path) if l.strip()]
        return cls(facts, **kw)

    @classmethod
    def from_jsonl_cached(cls, path: str, base_url: str = BASE_URL,
                          model: str = EMBED_MODEL, dims: int | None = None,
                          **kw) -> "HybridBank":
        """Boot from the F-034 int8 cache; (re)build it when stale. The
        serving matrix IS the dequantized cache — what ships is exactly
        what runs. Queries still encode at request time via base_url."""
        from .bankio import DEFAULT_DIMS, load_cache, write_cache
        dims = dims or DEFAULT_DIMS
        facts = [Fact(**json.loads(l))
                 for l in open(path, encoding="utf-8") if l.strip()]
        ids = [f.id for f in facts]

        def enc(texts):
            return lmstudio_encode(texts, base_url=base_url, model=model)

        cached = load_cache(path, model, dims)
        if cached is None or cached[1] != ids:
            write_cache(path, ids, enc(doc_strings(facts)), model, dims)
            cached = load_cache(path, model, dims)
        emb = EmbedBankLM(facts, encode=enc, matrix=cached[0])
        return cls(facts, encode=enc, emb=emb, **kw)

    @property
    def sources(self) -> list[str]:
        return sorted({f.source for f in self.facts})

    def search(self, query: str, k: int = 5, version_filter: str | None = None,
               min_score: float | None = None) -> list[tuple[Fact, float]]:
        """min_score is ignored: each backend uses its own calibrated
        threshold (BM25 scores are unbounded, cosine is 0..1 -- one number
        cannot serve both, which is part of why F-004 leaked)."""
        b = self.bm25.search(query, k=k, version_filter=version_filter,
                             min_score=self.bm25_min)
        e = self.emb.search(query, k=k, version_filter=version_filter,
                            min_score=self.cos_min)
        merged, seen = [], set()
        for f, s in list(b) + list(e):     # BM25 first: exact match wins ties
            if f.id not in seen:
                seen.add(f.id)
                merged.append((f, s))
        return merged[:k]

    def double_key_search(self, prompt: str, draft: str, k_prompt: int = 5,
                          k_draft: int = 3, version_filter: str | None = None,
                          min_score: float | None = None) -> list[Fact]:
        def lookup(vf):
            p = self.search(prompt, k=k_prompt, version_filter=vf)
            d = self.search(draft, k=k_draft, version_filter=vf)
            merged, seen = [], set()
            for f, _ in p + d:             # prompt-key first (hole 2 fix)
                if f.id not in seen:
                    seen.add(f.id)
                    merged.append(f)
            return merged

        hits = lookup(version_filter)
        if version_filter and not hits:    # fail open, never shut (F-010)
            hits = lookup(None)
        return hits
