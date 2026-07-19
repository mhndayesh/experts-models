#!/usr/bin/env python3
"""dedupe_mine.py - gate the MINED signature facts.

WHY THIS EXISTS. mine_api.py walked `inspect.signature` over each library's
public surface. It also walked the INHERITANCE CHAIN, so every sklearn estimator
donated its own copy of get_params/set_params/score/get_metadata_routing, and
every duckdb exception class donated add_note/with_traceback. Measured on the
24,133 data-domain facts: 63% share a docstring with >=5 other facts, and 16%
have a docstring that merely re-prints the signature.

That is not dead weight, it is ADVERSARIAL. 205 facts all containing the token
`fit` and 165 all containing `get_metadata_routing` flatten document frequency,
so IDF stops discriminating exactly the terms that should, and the duplicates
crowd the top-5. It is a mechanical explanation for gold retrieval falling from
12/12 at 2.3k facts to 9/12 at 21k.

WHY NOT package/factbank/gates.py. Those gates are for MODEL-EXTRACTED
candidates: gate_schema requires `quote` and `probes`, which a mined signature
has neither of, so the whole mine would die on a schema error rather than on its
real defect. gate_collision would work but needs 24k embedder calls to find
duplicates that are byte-identical strings. Wrong tool, right idea - this is the
same boundary principle (code decides what enters the bank) applied to a
different candidate shape.

NOTHING IS SILENTLY DROPPED (repo rule). Every rejection is written to
<out>.rejects.jsonl with its reason, so the cull is auditable without re-mining.
"""
import collections
import json
import glob
import re
import sys

IN_GLOB = "api_facts/data__*.jsonl"
OUT = "facts_mined_clean.jsonl"
REJ = "facts_mined_clean.rejects.jsonl"

# Python-object boilerplate every class inherits. Not library knowledge - the
# model knows what Exception.add_note does, and it does not need 69 copies.
STDLIB_LEAVES = {"add_note", "with_traceback", "__init__", "__new__"}
STDLIB_DOC = re.compile(r"^(Exception|BaseException)\.")

# numpy re-exposes every ndarray method on every scalar type (float64.sum,
# complex64.resize, ...). The docstring says so itself. The ndarray method is
# kept separately - these are 20+ copies of it.
SCALAR_DOC = re.compile(r"^Scalar method identical to\b", re.I)

ALIAS_DOC = re.compile(r"^Alias for\b", re.I)

# mine_api took the docstring's first line as the summary. When a numpydoc
# docstring opens straight into a section, that first line is the section
# HEADER, so the "fact" reads `PolarAxes.get_rmax(self) - Returns`. A mining
# defect, not a fact.
NUMPYDOC_HEADERS = {"returns", "return", "parameters", "notes", "examples",
                    "example", "see also", "raises", "yields", "attributes",
                    "warnings", "references", "other parameters"}


def _builtin_docs():
    """Derive - not hand-list - the docstrings Python's own builtins carry.

    matplotlib's CapStyle is an `str` enum, so mine_api dutifully recorded
    `CapStyle.join(self, iterable, /) - Concatenate any number of strings.`
    That is str.join. It is not matplotlib knowledge, and a bank that teaches
    the model str.join is a bank wasting a retrieval slot. Introspecting the
    builtins finds every such leak (str/list/dict/set/tuple/int/float/enum)
    without me guessing at a name list.
    """
    out = set()
    for base in (str, bytes, list, dict, set, frozenset, tuple, int, float,
                 complex, bool, object, BaseException):
        for name in dir(base):
            doc = (getattr(getattr(base, name, None), "__doc__", "") or "")
            first = doc.strip().split("\n")[0].strip()
            if first:
                out.add((name, first))
    return out


BUILTIN_DOCS = _builtin_docs()


def _sig_key(sig: str) -> str:
    """Signature normalized for comparison: whitespace and quote style vary,
    the parameter list does not."""
    return re.sub(r"\s+", "", sig).replace("'", '"')


def split(text):
    """'pkg.Cls.meth(sig) - docstring' -> (symbol, sig, doc)"""
    i = text.find(" - ")
    head = text[:i] if i > 0 else text
    doc = text[i + 3:].strip() if i > 0 else ""
    j = head.find("(")
    sym = head[:j] if j > 0 else head
    return sym.strip(), head[j:].strip() if j > 0 else "", doc


def has_real_params(sig: str) -> bool:
    """Does the signature teach anything? `(self)` and `()` do not; a real
    parameter list does."""
    inner = sig.strip().lstrip("(").rstrip(")").strip()
    parts = [p.strip() for p in inner.split(",") if p.strip()]
    parts = [p for p in parts if p not in ("self", "/", "*", "cls")]
    return bool(parts)


def is_echo(sym, sig, doc):
    """pyarrow-style: the docstring just re-prints the call.
        'pyarrow.Decimal256Array.drop_null(self) - Array.drop_null(self)'

    BUT a redundant docstring does not make the fact worthless - THE SIGNATURE
    IS THE FACT. The first version of this gate deleted
        pyarrow.Table.join_asof(self, right_table, on, by, tolerance,
                                right_on=None, right_by=None)
    because pyarrow writes lazy docstrings. That is a real, useful API and
    exactly the kind of signature a model invents wrong. Caught by reading the
    reject file.

    So: an echo is junk only when the signature is ALSO empty - `is_valid(self)`
    teaches nothing whether or not the docstring repeats it.
    """
    if not doc:
        return not has_real_params(sig)
    leaf = sym.split(".")[-1]
    d = doc.split("(")[0].strip()
    echoes = d.split(".")[-1] == leaf and "(" in doc and len(doc) < 120
    return echoes and not has_real_params(sig)


def main():
    rows = []
    for f in sorted(glob.glob(IN_GLOB)):
        rows += [json.loads(l) for l in open(f, encoding="utf-8")]
    n0 = len(rows)

    for r in rows:
        r["_sym"], r["_sig"], r["_doc"] = split(r["text"])
        r["_leaf"] = r["_sym"].split(".")[-1]
        r["_depth"] = r["_sym"].count(".")

    keep, rej = [], []

    def drop(r, why):
        rej.append({**{k: v for k, v in r.items() if not k.startswith("_")},
                    "reject_reason": why})

    # ---- pass 1: per-fact defects -------------------------------------------
    survivors = []
    for r in rows:
        if r["_leaf"] in STDLIB_LEAVES or STDLIB_DOC.match(r["_doc"]):
            drop(r, "stdlib object boilerplate (not library knowledge)")
        elif (r["_leaf"], r["_doc"]) in BUILTIN_DOCS:
            drop(r, "python builtin inherited (str/list/dict/int/... method "
                    "surfaced on a library class - not library knowledge)")
        elif SCALAR_DOC.match(r["_doc"]):
            drop(r, "numpy scalar re-export ('Scalar method identical to "
                    "ndarray.X') - the ndarray method is kept separately")
        elif ALIAS_DOC.match(r["_doc"]):
            drop(r, "alias stub ('Alias for X') - carries no signature info")
        elif r["_doc"].strip().lower().rstrip(":") in NUMPYDOC_HEADERS:
            drop(r, "docstring is a numpydoc section header, not a summary "
                    "(mining defect)")
        elif is_echo(r["_sym"], r["_sig"], r["_doc"]):
            drop(r, "no information: docstring echoes the symbol AND the "
                    "signature takes no real parameters")
        else:
            survivors.append(r)

    # ---- pass 2: inherited duplicates ---------------------------------------
    # Same library + same leaf name + same docstring + SAME SIGNATURE, spread
    # across many classes = ONE method inherited N times. Keep the copy nearest
    # the canonical public path (shallowest dotted name; ties -> alphabetical,
    # so the choice is deterministic and re-runnable). Drop the rest.
    #
    # The signature must be in the key. Without it this gate ate
    # `polars.Series.search_sorted`, which shares its one-line docstring with
    # `Expr.search_sorted` but takes different arguments - and the arguments ARE
    # the fact. Two methods sharing a summary line are not the same method.
    # Caught by reading the reject file, which is why the reject file exists.
    groups = collections.defaultdict(list)
    for r in survivors:
        groups[(r["source"], r["_leaf"], r["_doc"], _sig_key(r["_sig"]))].append(r)

    for (src, leaf, doc, _sk), g in groups.items():
        if len(g) == 1:
            keep.append(g[0])
            continue
        # Which copy represents the group? The one on the class that most
        # likely DEFINES the method - i.e. the base class.
        #
        # Sorting by (depth, alphabetical) kept `pandas.CategoricalIndex.
        # to_series` and threw away `pandas.Index.to_series`, because "C" < "I".
        # The bank ended up holding the subclass and discarding the canonical
        # base. Shortest CLASS NAME is a crude but effective proxy for the base:
        # Index < CategoricalIndex, Array < LargeStringArray, Axes < Subplot.
        g.sort(key=lambda r: (r["_depth"], len(r["_sym"].split(".")[-2])
                              if r["_depth"] >= 2 else 0, r["_sym"]))
        keep.append(g[0])
        for r in g[1:]:
            drop(r, f"inherited duplicate: '{leaf}' with this exact docstring "
                    f"appears on {len(g)} {src} classes; kept {g[0]['_sym']}")

    keep.sort(key=lambda r: r["id"])
    with open(OUT, "w", encoding="utf-8") as fh:
        for r in keep:
            fh.write(json.dumps({k: v for k, v in r.items()
                                 if not k.startswith("_")}) + "\n")
    with open(REJ, "w", encoding="utf-8") as fh:
        for r in rej:
            fh.write(json.dumps(r) + "\n")

    # ---- report --------------------------------------------------------------
    why = collections.Counter(r["reject_reason"].split(":")[0] for r in rej)
    print(f"mined      {n0:>7,}")
    print(f"kept       {len(keep):>7,}   ({100*len(keep)/n0:.0f}%)")
    print(f"rejected   {len(rej):>7,}   ({100*len(rej)/n0:.0f}%)\n")
    for w, c in why.most_common():
        print(f"  {c:>7,}  {w}")

    print("\nper library:")
    kb = collections.Counter(r["source"] for r in keep)
    ab = collections.Counter(r["source"] for r in rows)
    print(f"  {'lib':<12} {'mined':>7} {'kept':>7} {'kept%':>6}")
    for lib, tot in ab.most_common():
        k = kb[lib]
        print(f"  {lib:<12} {tot:>7,} {k:>7,} {100*k/tot:>5.0f}%")

    # the number that actually matters for retrieval
    docs = collections.Counter(r["_doc"] for r in keep)
    dup = sum(1 for r in keep if docs[r["_doc"]] >= 5)
    print(f"\nfacts still sharing a docstring with >=5 others: "
          f"{dup:,} ({100*dup/max(1,len(keep)):.0f}%)   [was 63%]")
    leaf = collections.Counter(r["_leaf"] for r in keep)
    print(f"distinct leaf names: {len(leaf):,} for {len(keep):,} facts "
          f"-> {len(keep)/len(leaf):.1f} facts/name   [was 4.9]")
    print(f"\n-> {OUT}\n-> {REJ}")


if __name__ == "__main__":
    main()
