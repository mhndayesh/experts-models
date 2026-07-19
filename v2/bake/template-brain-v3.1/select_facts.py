#!/usr/bin/env python3
"""select_facts.py - pick the highest-value slice of a mined fact pool so a
model stays inside its PARSE budget.

*** THE LAW BELOW IS STALE - READ F-055 FIRST (2026-07-14) ***

Superseded: F-045's parse tax was measured on the LINEAR SCANNER under jinja2.
With the INVERTED INDEX on llama.cpp's current engine, render cost scales with
the QUERY, not with the bank: 21,203 facts / 5.06 MB renders a matched question
in 218 ms - FASTER than the 950 KB / 1,911-fact build - and the cost per fact
FALLS 8x as the bank grows (0.085 -> 0.010 ms/fact). Fact count is NOT a latency
budget on llama.cpp.

What DOES bind (F-056): RECALL. Gold decays 12/12 (2.3k facts) -> 11/12 (4.6k)
-> 9/12 (8.8k and 21k) while controls stay 0/10. The bank does not get noisy, it
gets UNFOCUSED. So quotas here still matter - not to buy milliseconds, but to
keep the ranker's job winnable. And on LM STUDIO the byte ceiling is real and
hard (~1 MB, F-053), which is the other reason to keep selecting.

Superseded law, kept for the record (2026-07-13, F-045): a serving engine
re-renders the chat template on EVERY request, and the cost is dominated by
PARSING the template bytes, not by the scan. Grouping the bank by library
(v3.4.0) made the scan nearly free (8 ms on a no-match question with 24.5k facts
loaded) but the parse remains linear in bank size: ~0.26 ms/fact in jinja2,
~0.15 ms/fact in LM Studio's engine, ~0.33 ms/fact in llama-server. So the fact
count per MODEL is a latency budget, and 30-40k facts ship as a LINE of domain
models, not as one file.

Value ranking (best first):
  1. curated dead-name / behavior facts (kind mistake|behavior|concept) -
     these beat a wrong prior and are what the bank exists for; never cut.
  2. signature facts that own a documented page (meta.url has a #anchor) -
     the public, documented API surface.
  3. signature facts by CENTRALITY: fewer dots in the symbol = closer to the
     library's front door (pandas.DataFrame.merge beats
     pandas.core.groupby.DataFrameGroupBy.corrwith).
  4. within a tie, shorter symbol name first.
Per-library quotas keep one huge library (matplotlib: 7,318 raw facts) from
eating the budget of the libraries people actually ask about.

usage: the pool is built from the curated facts + the mined domain (api_facts/),
then selected from. The old monolithic pool files are in archive/.

  python build_pool.py --domain data --out _pool.jsonl
  python select_facts.py --pool _pool.jsonl --out bank.jsonl \
         --quota pandas=1200,numpy=900,... --default-quota 200
  python bake_index.py --facts bank.jsonl --out tpl.jinja   # add --max-bytes for a MAX build
"""
import argparse, json, collections

# PROVENANCE, not kind (F-049). A curated research fact can be labelled
# kind="signature" (polars-001: "collect() has no streaming=True, use engine=")
# and the kind-based rule evicted it from the shipped bank. Curated facts are
# identified by where they CAME FROM: hand/agent-mined doc facts have plain ids
# (polars-003, pandas3-046, numpy2-001); machine-introspected signature facts
# all carry an "...api-" id prefix from mine_api.py.
CURATED = {"mistake", "behavior", "concept"}


def is_curated(r):
    return "api-" not in r["id"]


# MUST-SEAT: the API surface people actually ask about. Centrality ranking
# (fewer dots, shorter name) is a decent proxy but it silently dropped
# train_test_split, ttest_ind and pyplot.scatter - the exact functions a user
# reaches for. These are seated like curated facts, before any quota applies.
MUST_SEAT = [
    "train_test_split", "cross_val_score", "GridSearchCV", "StandardScaler",
    "classification_report", "confusion_matrix", "accuracy_score", "fit_transform",
    "ttest_ind", "ttest_rel", "pearsonr", "spearmanr", "linregress", "curve_fit",
    "pyplot.scatter", "pyplot.plot", "pyplot.subplots", "pyplot.savefig",
    "pyplot.hist", "pyplot.bar", "pyplot.legend", "pyplot.xlabel",
    "pyplot.imshow", "pyplot.figure", "pyplot.show", "pyplot.title",
    "read_csv", "to_csv", "read_parquet", "groupby", "merge(", "pivot_table",
    "drop_duplicates", "value_counts", "sort_values", "reset_index",
    "scan_csv", "unpivot", "group_by", "with_columns", "map_elements",
    "np.linalg.svd", "np.linalg.inv", "np.linalg.solve", "np.random.default_rng",
    "np.concatenate", "np.reshape", "np.where", "np.argsort", "np.isin",
]


def is_must_seat(r):
    sym = (r.get("meta") or {}).get("symbol", "") or ""
    return any(m in sym or m in r["text"][:90] for m in MUST_SEAT)


def rank_key(r):
    sym = (r.get("meta") or {}).get("symbol", "") or r["id"]
    documented = 0 if "#" in ((r.get("meta") or {}).get("url") or "") else 1
    return (documented, sym.count("."), len(sym), sym)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pool", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--quota", default="", help="lib=N,lib=N ...")
    ap.add_argument("--default-quota", type=int, default=200)
    a = ap.parse_args()

    quota = {}
    for part in a.quota.split(","):
        if "=" in part:
            k, v = part.split("=")
            quota[k.strip()] = int(v)

    rows = [json.loads(l) for l in open(a.pool, encoding="utf-8") if l.strip()]
    by_lib = collections.defaultdict(list)
    for r in rows:
        by_lib[r["source"]].append(r)

    keep, report = [], []
    for lib in sorted(by_lib):
        facts = by_lib[lib]
        curated = [r for r in facts if is_curated(r)]
        rest = [r for r in facts if not is_curated(r)]
        must = [r for r in rest if is_must_seat(r)]
        sigs = sorted([r for r in rest if not is_must_seat(r)], key=rank_key)
        q = quota.get(lib, a.default_quota)
        room = max(0, q - len(curated) - len(must))
        picked = curated + must + sigs[:room]
        keep.extend(picked)
        report.append((lib, len(facts), len(curated) + len(must), len(picked)))

    with open(a.out, "w", encoding="utf-8") as f:
        for r in keep:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    print(f"{'library':14} {'pool':>6} {'curated':>8} {'kept':>6}")
    for lib, pool, cur, kept in report:
        print(f"{lib:14} {pool:6} {cur:8} {kept:6}")
    print(f"\nSELECTED {len(keep)} facts -> {a.out}")


if __name__ == "__main__":
    main()
