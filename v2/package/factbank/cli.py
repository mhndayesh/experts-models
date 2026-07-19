"""factbank CLI — serve / check / watch / review / mine.

serve  the sealed loop as one OpenAI-compatible endpoint (P1, live)
check  bank schema + integrity gates, cache rebuild        (P1 basic; P4 full)
watch  release watcher -> quote-gated fact proposals       (P4)
review show/apply pending proposals                        (P4)
mine   flagged wrong answers -> proposed facts             (P4)
"""

import argparse
import json
import os
import sys

from . import __version__
from .config import apply_config, find_config


def cmd_check(args) -> int:
    """P1 schema gate: structure, ids, version tags. (The full boundary
    gates — quote/anchor/collision/self-retrieval — land in P4.)"""
    required = ("id", "text", "source", "version")
    kinds = {"doc", "signature", "example", "concept", "behavior",
             "removed"}
    seen, bad, n = set(), 0, 0
    for ln, line in enumerate(open(args.bank, encoding="utf-8"), 1):
        line = line.strip()
        if not line:
            continue
        n += 1
        try:
            d = json.loads(line)
        except json.JSONDecodeError as e:
            print(f"line {ln}: not JSON ({e})")
            bad += 1
            continue
        for f in required:
            if not str(d.get(f, "")).strip():
                print(f"line {ln} [{d.get('id', '?')}]: missing {f!r}")
                bad += 1
        if d.get("kind", "doc") not in kinds:
            print(f"line {ln} [{d.get('id')}]: unknown kind "
                  f"{d.get('kind')!r}")
            bad += 1
        if d.get("id") in seen:
            print(f"line {ln}: duplicate id {d.get('id')!r}")
            bad += 1
        seen.add(d.get("id"))
    print(f"{args.bank}: {n} facts, {bad} problems")
    if bad:
        return 1
    if args.rebuild:
        import json as _json

        from .bank import Fact
        from .bankio import bank_hash, cache_path, load_cache, write_cache
        from .lmstudio_embed import doc_strings, lmstudio_encode
        facts = [Fact(**_json.loads(l))
                 for l in open(args.bank, encoding="utf-8") if l.strip()]
        vecs = lmstudio_encode(doc_strings(facts), base_url=args.upstream,
                               model=args.embed_model)
        out = write_cache(args.bank, [f.id for f in facts], vecs,
                          args.embed_model, args.dims)
        ok = load_cache(args.bank, args.embed_model, args.dims)
        import os as _os
        print(f"cache: {out}  {_os.path.getsize(out):,} B  "
              f"({args.dims} dims, int8)  "
              f"verify: {'OK' if ok is not None else 'FAILED'}  "
              f"hash {bank_hash(args.bank)[:12]}")
        return 0 if ok is not None else 1
    return 0


def cmd_watch(args) -> int:
    """Release watcher. FULL-AUTO by default (owner decision): proposals
    that pass every gate are applied under snapshot+healthcheck+rollback.
    --propose-only restores the manual review flow."""
    from .extract import ModelExtractor
    from .server import GuardError, UpstreamGuard
    from .watch import apply, scan, write_pending
    if not args.extract_model:   # rule: each model extracts with itself
        cfg = find_config(args.config)
        if cfg:
            import tomllib
            with open(cfg, "rb") as fh:
                args.extract_model = (tomllib.load(fh)
                                      .get("serve", {}).get("model"))
    if not args.extract_model:
        print("no extractor model: pass --extract-model or set [serve] "
              "model in factbank.toml (each model extracts with itself)")
        return 2
    guard = UpstreamGuard(args.extract_upstream)
    try:
        guard.require(args.extract_model)   # never JIT-load, even here
    except GuardError as e:
        print(f"watch needs the extractor loaded: {e}")
        return 3
    extractor = ModelExtractor(args.extract_upstream, args.extract_model)
    props = scan(args.bank, extractor,
                 sources_filter=set(args.only.split(",")) if args.only
                 else None)
    if not props:
        print("[watch] no proposals")
        return 0
    p = write_pending(args.bank, props)
    print(f"[watch] {len(props)} proposal(s) -> {p}")
    if args.propose_only:
        print("[watch] review with: factbank review --bank "
              f"{args.bank} --apply")
        return 0
    return 0 if apply(args.bank, props) else 1


def cmd_review(args) -> int:
    from .watch import PENDING, apply
    p = args.bank + PENDING
    if not os.path.exists(p):
        print("no pending proposals")
        return 0
    props = [json.loads(l) for l in open(p, encoding="utf-8")
             if l.strip()]
    for f in props:
        print(f"+ [{f['source']} {f['version']} | {f['kind']}] "
              f"{f['text'][:100]}")
        print(f"    quote: {f['meta']['quote'][:90]}")
    print(f"\n{len(props)} pending proposal(s)")
    if args.apply:
        return 0 if apply(args.bank, props) else 1
    print("apply with: factbank review --bank "
          f"{args.bank} --apply")
    return 0


def cmd_mine(args) -> int:
    """v1: turn a logged wrong answer into a fact skeleton for editing."""
    rows = [json.loads(l) for l in open(args.log, encoding="utf-8")
            if l.strip()]
    ok = [r for r in rows if r.get("kind") == "ok"]
    if args.run_id is None:
        for r in ok[-args.last:]:
            print(f"{r.get('id', '?'):<24} {r.get('question', '')[:80]}")
        print(f"\npick one: factbank mine --log {args.log} "
              f"--run-id <id> --correction 'the true claim'")
        return 0
    row = next((r for r in ok if r.get("id") == args.run_id), None)
    if row is None:
        print(f"run id {args.run_id!r} not found")
        return 1
    skel = {"id": "FIXME-lib-001",
            "text": args.correction or "FIXME: the correct claim, "
            "self-contained, with exact identifiers",
            "source": "FIXME-lib", "version": "FIXME",
            "kind": "signature",
            "meta": {"url": "FIXME", "mined_from": args.run_id,
                     "question": row.get("question", "")[:200]}}
    print(json.dumps(skel, ensure_ascii=False))
    print("\nedit the FIXMEs, append to the bank, run: factbank check "
          "--rebuild", file=sys.stderr)
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        prog="factbank",
        description="a fact bank + sealed retrieval loop around your "
                    "local model")
    ap.add_argument("--version", action="version",
                    version=f"factbank {__version__}")
    ap.add_argument("--config", default=None,
                    help="factbank.toml path (default: ./factbank.toml "
                         "or $FACTBANK_CONFIG)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    from .server import add_serve_args, run_serve
    sp = sub.add_parser("serve", help="run the sealed-loop endpoint")
    sp.add_argument("--config", default=None,
                    help="factbank.toml path (also accepted before the "
                         "subcommand)")
    add_serve_args(sp)
    sp.set_defaults(fn=lambda a: run_serve(a) or 0, config_section="serve")

    cp = sub.add_parser("check", help="validate a bank file")
    cp.add_argument("bank")
    cp.add_argument("--rebuild", action="store_true",
                    help="re-encode and rewrite the F-034 index cache")
    cp.add_argument("--upstream", default="http://127.0.0.1:1234/v1")
    cp.add_argument("--embed-model",
                    default="text-embedding-nomic-embed-text-v1.5")
    cp.add_argument("--dims", type=int, default=256)
    cp.set_defaults(fn=cmd_check, config_section=None)

    wp = sub.add_parser("watch", help="check releases; extract, gate and "
                        "(by default) auto-apply new facts")
    wp.add_argument("--bank", required=True)
    wp.add_argument("--extract-upstream", default="http://127.0.0.1:1234/v1")
    wp.add_argument("--extract-model", default=None,
                    help="default: the [serve] model from factbank.toml "
                         "— each model extracts with itself (F-036)")
    wp.add_argument("--only", default=None,
                    help="comma-separated source filter")
    wp.add_argument("--propose-only", action="store_true",
                    help="write pending proposals, do not apply")
    wp.add_argument("--config", default=None)
    wp.set_defaults(fn=cmd_watch, config_section="watch")

    rp = sub.add_parser("review", help="show/apply pending proposals")
    rp.add_argument("--bank", required=True)
    rp.add_argument("--apply", action="store_true")
    rp.set_defaults(fn=cmd_review, config_section=None)

    mp = sub.add_parser("mine", help="turn a logged answer into a fact "
                        "skeleton")
    mp.add_argument("--log", default="serve_runs.jsonl")
    mp.add_argument("--last", type=int, default=10)
    mp.add_argument("--run-id", default=None)
    mp.add_argument("--correction", default=None)
    mp.set_defaults(fn=cmd_mine, config_section=None)

    bp = sub.add_parser("bake", help="burn the bank into a GGUF's chat "
                        "template: one static drop-in file for LM Studio "
                        "(no loop/retrieval/updates — re-bake to update)")
    bp.add_argument("--gguf", required=True, help="source GGUF")
    bp.add_argument("--bank", required=True)
    bp.add_argument("--out", required=True, help="output GGUF path")
    bp.add_argument("--name", default="factbank-baked",
                    help="general.name shown by the runner")
    from .bake import cmd_bake
    bp.set_defaults(fn=cmd_bake, config_section=None)

    # config file becomes defaults BEFORE final parse: CLI still wins
    pre, _ = ap.parse_known_args(argv)
    if getattr(pre, "config_section", None):
        cfg = find_config(pre.config)
        if cfg:
            for action in ap._subparsers._group_actions:
                sub_parser = action.choices.get(pre.cmd)
                if sub_parser is not None:
                    apply_config(sub_parser, pre.config_section, cfg)
    args = ap.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
