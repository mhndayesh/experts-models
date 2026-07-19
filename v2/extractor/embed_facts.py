#!/usr/bin/env python3
"""embed_facts.py - Tier-2 BAKE-TIME embedding via LM Studio's local nomic-embed. Vectorizes each v3 variant's
retrieval text (feature_phrases + query_phrases + truth) with the search_document: prefix. Bake-time build tool
ONLY - the vectors get frozen; nomic never ships. Rule 1: the owner LOADS nomic; this only CALLS /v1/embeddings.

usage: python embed_facts.py            # embeds FINAL_v3 variants -> v3_vectors.jsonl
       python embed_facts.py --probe    # 1-call sanity check that the endpoint + model are up
"""
import json, os, sys, urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

HERE = os.path.dirname(os.path.abspath(__file__))
V3   = os.path.join(HERE, "experts", "appsec", "facts", "FINAL_v3.jsonl")
OUT  = os.path.join(HERE, "experts", "appsec", "facts", "v3_vectors.jsonl")
URL  = os.environ.get("LMS_URL", "http://localhost:1234/v1") + "/embeddings"
EMBED_MODEL = os.environ.get("EMBED_MODEL", "text-embedding-nomic-embed-text-v1.5")

def embed(texts):
    body = json.dumps({"model": EMBED_MODEL, "input": texts}).encode()
    req = urllib.request.Request(URL, data=body, headers={"Content-Type": "application/json"})
    d = json.loads(urllib.request.urlopen(req, timeout=120).read())
    return [row["embedding"] for row in d["data"]]

def doc_text(v):
    r = v["retrieval"]
    parts = (r.get("query_phrases") or []) + (r.get("aliases") or []) + [v["claim"].get("truth","")]
    return "search_document: " + " | ".join(p for p in parts if p)[:1200]

def main():
    if "--probe" in sys.argv:
        vs = embed(["search_query: load an uploaded model checkpoint",
                    "search_document: use torch.load weights_only=True for untrusted files"])
        import math
        a, b = vs[0], vs[1]; dot = sum(x*y for x,y in zip(a,b))
        na = math.sqrt(sum(x*x for x in a)); nb = math.sqrt(sum(x*x for x in b))
        print(f"OK: model up, dim={len(a)}, cos(query,doc)={dot/(na*nb):.3f}"); return
    variants = [json.loads(l) for l in open(V3, encoding="utf-8") if json.loads(l).get("kind")=="variant"]
    B = 32
    batches = [variants[i:i+B] for i in range(0, len(variants), B)]
    vecs = {}; done = 0
    def do(batch):
        return batch, embed([doc_text(v) for v in batch])
    with ThreadPoolExecutor(max_workers=8) as ex:   # LM Studio is local; keep concurrency modest
        futs = [ex.submit(do, b) for b in batches]
        for fut in as_completed(futs):
            try:
                batch, es = fut.result()
                for v, e in zip(batch, es): vecs[v["id"]] = e
            except Exception as ex_:
                print("  batch err", type(ex_).__name__)
            done += 1
            if done % 20 == 0: print(f"  {done}/{len(batches)}")
    with open(OUT, "w", encoding="utf-8") as fh:
        for fid, e in vecs.items(): fh.write(json.dumps({"id": fid, "v": e}) + "\n")
    print(f"embedded {len(vecs)}/{len(variants)} facts (dim {len(next(iter(vecs.values())))}) -> {OUT}")

if __name__ == "__main__":
    main()
