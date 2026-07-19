"""bankio.py - the bank's embedding-index cache (F-034 format).

Measured decision (research repo, bench_bankstore.py, 36 gold queries):
int8-quantized 256-dim Matryoshka vectors retrieve IDENTICALLY to
fp32-768 (hit@5 0.972 both) at 260 B/fact vs 3,072 — 11.8x smaller. The
cliff is at 128 dims. nomic-embed-text-v1.5 is Matryoshka-trained, so
truncate + renormalize is a designed-for operation.

The cache is DERIVED data: content-hashed against the bank file, model-
and dims-stamped, rebuilt whenever stale. The bank JSONL remains the only
source of truth. Boot with a fresh cache skips re-embedding the bank;
queries still embed at request time (hybrid retrieval needs an encoder at
runtime — `--bm25-only` is the no-encoder mode).
"""

import hashlib
import json
import os

import numpy as np

CACHE_VERSION = 1
# 768, not 256: MRL-256 keeps RANKING (hit@5 identical, F-034) but
# inflates absolute cosines — measured 2026-07-13: control top-1 sims
# reach 0.783 at 256d while the weakest relevant hit is 0.692, so the
# calibrated cos_min=0.68 gate (the F-004 fix) stops separating. int8-768
# preserves the validated threshold semantics at 4.0x smaller. 256 stays
# available via --dims for setups not relying on absolute thresholds.
DEFAULT_DIMS = 768


def bank_hash(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def cache_path(bank_path: str) -> str:
    return bank_path + ".cache.npz"


def mrl(M: np.ndarray, dims: int) -> np.ndarray:
    """Matryoshka truncation: slice then renormalize."""
    M = np.asarray(M, dtype=np.float32)[:, :dims]
    return M / (np.linalg.norm(M, axis=1, keepdims=True) + 1e-9)


def quantize(M: np.ndarray):
    scale = np.abs(M).max(axis=1, keepdims=True) / 127.0
    # A zero row (all-zero embedding) gives scale=0 -> M/scale is nan/inf and
    # poisons the whole cache. Treat a zero row as zero: scale 1, quantized 0.
    scale = np.where(scale == 0.0, 1.0, scale)
    return np.round(M / scale).astype(np.int8), scale.astype(np.float32)


def dequantize(q: np.ndarray, scale: np.ndarray) -> np.ndarray:
    M = q.astype(np.float32) * scale
    return M / (np.linalg.norm(M, axis=1, keepdims=True) + 1e-9)


def write_cache(bank_path: str, ids: list, vectors: np.ndarray,
                model: str, dims: int = DEFAULT_DIMS) -> str:
    """vectors: raw encoder output [N, d_full] (any dtype)."""
    M = mrl(vectors, dims)
    q, scale = quantize(M)
    meta = json.dumps({"version": CACHE_VERSION, "model": model,
                       "dims": dims, "hash": bank_hash(bank_path),
                       "n": len(ids)})
    out = cache_path(bank_path)
    tmp = out + ".tmp"
    with open(tmp, "wb") as fh:      # handle, so savez can't rename it
        np.savez(fh, q=q, scale=scale, ids=np.array(ids),
                 meta=np.array(meta))
    os.replace(tmp, out)             # atomic: never a half-written cache
    return out


def load_cache(bank_path: str, model: str, dims: int = DEFAULT_DIMS):
    """-> (matrix fp32 [N, dims] normalized, ids list) or None if
    missing/stale/mismatched. Never raises for a bad cache — a cache
    problem is a rebuild, not a crash."""
    p = cache_path(bank_path)
    if not os.path.exists(p):
        return None
    try:
        with np.load(p, allow_pickle=False) as z:   # close the NPZ handle
            meta = json.loads(str(z["meta"]))
            if (meta.get("version") != CACHE_VERSION
                    or meta.get("model") != model
                    or meta.get("dims") != dims
                    or meta.get("hash") != bank_hash(bank_path)):
                return None
            q, scale, ids = z["q"], z["scale"], z["ids"]
            # structural validation: a corrupt/mismatched cache is a rebuild,
            # not a silent wrong-shape load.
            if q.ndim != 2 or q.shape[0] != len(ids) or q.shape[0] != meta.get("n") \
                    or q.shape[1] != dims or scale.shape[0] != q.shape[0]:
                return None
            return dequantize(q, scale), [str(i) for i in ids.tolist()]
    except Exception:
        return None
