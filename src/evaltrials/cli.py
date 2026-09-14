"""evaltrials CLI. Six verbs. Structured output. Cost stated before it is spent.

Output is JSON whenever stdout is not a TTY, so an agent gets machine-readable
results without having to know to pass --json.
"""
from __future__ import annotations

import argparse
import json
import sys

from . import cache, plan as planmod, sources
from .card import load_all
from .plan import human_bytes
from .schema import COLUMNS


def _emit(obj, args) -> None:
    if args.json or not sys.stdout.isatty():
        json.dump(obj, sys.stdout, indent=2, default=str)
        sys.stdout.write("\n")
    else:
        _pretty(obj)


def _pretty(obj, indent=0) -> None:
    pad = "  " * indent
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(v, (dict, list)) and v:
                print(f"{pad}{k}:")
                _pretty(v, indent + 1)
            else:
                print(f"{pad}{k}: {v}")
    elif isinstance(obj, list):
        for v in obj:
            if isinstance(v, (dict, list)):
                _pretty(v, indent)
                print()
            else:
                print(f"{pad}- {v}")
    else:
        print(f"{pad}{obj}")


def _cards(args, require_implemented=False):
    allc = load_all()
    ids = args.source or list(allc)
    out = []
    for i in ids:
        if i not in allc:
            raise SystemExit(f"unknown source {i!r}. known: {sorted(allc)}")
        c = allc[i]
        if require_implemented and c.status != "implemented":
            raise SystemExit(
                f"{i} is status={c.status}: no fetcher yet. `evaltrials catalog` lists what is implemented."
            )
        out.append(c)
    return out


# -- verbs -------------------------------------------------------------------

def cmd_catalog(args):
    allc = load_all()
    rows = [c.summary() for c in allc.values()]
    if args.unit:
        rows = [r for r in rows if r["unit"] == args.unit]
    if args.implemented:
        rows = [r for r in rows if r["status"] == "implemented"]
    if args.redistributable:
        rows = [r for r in rows if r["redistributable"]]
    _emit({
        "schema_version": "0.1.0",
        "canonical_columns": COLUMNS,
        "n_sources": len(rows),
        "sources": rows,
        "hint": "unit=trial gives per-run variance; unit=cell is already aggregated. Branch on it.",
    }, args)


def cmd_describe(args):
    out = []
    for c in _cards(args):
        out.append({
            **c.summary(),
            "title": c.title,
            "upstream": c.upstream,
            "trials_per_cell": c.raw.get("trials_per_cell"),
            "assets": [
                {**a, "human": human_bytes(a.get("bytes"))} for a in (c.raw.get("assets") or [])
            ],
            "fields": c.fields,
            "joins_with": c.joins_with,
            "caveats": c.caveats,
            "cached": cache.normalized_path(c.id).exists(),
        })
    _emit(out[0] if len(out) == 1 else out, args)


def cmd_plan(args):
    cards = _cards(args)
    if args.benchmark:
        cards = [c for c in cards
                 if args.benchmark in (c.raw.get("benchmarks") or [])
                 or any(args.benchmark in str(j) for j in c.joins_with)
                 or args.benchmark in str(c.raw.get("scale"))]
        if not cards:
            cards = _cards(args)
    _emit(planmod.plan(cards, asset=args.asset), args)


def cmd_fetch(args):
    import pyarrow.parquet as pq
    results = []
    for c in _cards(args, require_implemented=True):
        p = planmod.plan_source(c, args.asset)
        if p["verdict"] == "blocked" and not args.force:
            results.append({**p, "fetched": False, "reason": "blocked; pass --force to override"})
            continue
        mod = sources.get(c.id)
        dest = cache.source_dir(c.id)
        paths = mod.fetch(c, dest, asset=args.asset, from_path=args.from_path)
        table = mod.normalize(c, paths)
        out = cache.normalized_path(c.id)
        pq.write_table(table, out)
        results.append({
            "source": c.id, "fetched": True, "unit": c.unit,
            "rows": table.num_rows, "path": str(out),
            "bytes_on_disk": out.stat().st_size,
            "human": human_bytes(out.stat().st_size),
            "obligations": p["obligations"],
        })
    _emit(results[0] if len(results) == 1 else results, args)


def cmd_sample(args):
    import pyarrow.parquet as pq
    out = []
    for c in _cards(args):
        path = cache.normalized_path(c.id)
        if not path.exists():
            out.append({"source": c.id, "cached": False,
                        "hint": f"run `evaltrials fetch {c.id}` first; "
                                f"`evaltrials plan {c.id}` shows the cost"})
            continue
        t = pq.read_table(path)
        head = t.slice(0, args.n).to_pylist()
        nonnull = {c2: t.column(c2).null_count for c2 in t.column_names}
        out.append({
            "source": c.id, "cached": True, "unit": c.unit, "rows": t.num_rows,
            "coverage": {k: round(1 - v / max(t.num_rows, 1), 3) for k, v in nonnull.items()},
            "sample": head,
        })
    _emit(out[0] if len(out) == 1 else out, args)


def cmd_query(args):
    try:
        import duckdb
    except ImportError:
        raise SystemExit("duckdb is required for `query`: uv pip install duckdb")
    con = duckdb.connect()
    registered = []
    for c in load_all().values():
        p = cache.normalized_path(c.id)
        if p.exists():
            con.execute(f"CREATE VIEW \"{c.id}\" AS SELECT * FROM read_parquet('{p}')")
            registered.append(c.id)
    if not registered:
        raise SystemExit("nothing cached. run `evaltrials fetch <source>` first.")
    con.execute("CREATE VIEW trials AS SELECT * FROM (" +
                " UNION ALL BY NAME ".join(f'SELECT * FROM "{r}"' for r in registered) + ")")
    rel = con.execute(args.sql)
    cols = [d[0] for d in rel.description]
    rows = rel.fetchall()
    # Agent-first: never dump a result set into context. Summarize, cap, point.
    capped = rows[: args.limit]
    _emit({
        "views": registered + ["trials"],
        "columns": cols,
        "n_rows": len(rows),
        "returned": len(capped),
        "truncated": len(rows) > len(capped),
        "rows": [dict(zip(cols, r)) for r in capped],
        "cache_dir": str(cache.root()),
    }, args)


def main(argv=None) -> int:
    # --json accepted both before and after the verb; agents should not have to care.
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--json", action="store_true", default=argparse.SUPPRESS,
                        help="force JSON (default when stdout is not a TTY)")

    ap = argparse.ArgumentParser(prog="evaltrials", description=__doc__.splitlines()[0],
                                 parents=[common])
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("catalog", parents=[common], help="list every known source, one compact line each")
    p.add_argument("--unit", choices=["trial", "cell", "score"])
    p.add_argument("--implemented", action="store_true")
    p.add_argument("--redistributable", action="store_true")
    p.set_defaults(fn=cmd_catalog, source=None)

    p = sub.add_parser("describe", parents=[common], help="full schema card for a source")
    p.add_argument("source", nargs="+")
    p.set_defaults(fn=cmd_describe)

    p = sub.add_parser("plan", parents=[common], help="preflight: bytes, time, licence, blockers. zero I/O")
    p.add_argument("source", nargs="*")
    p.add_argument("--asset")
    p.add_argument("--benchmark")
    p.set_defaults(fn=cmd_plan)

    p = sub.add_parser("fetch", parents=[common], help="download + normalize into the local cache")
    p.add_argument("source", nargs="+")
    p.add_argument("--asset")
    p.add_argument("--from", dest="from_path", help="import a local file instead of downloading")
    p.add_argument("--force", action="store_true")
    p.set_defaults(fn=cmd_fetch)

    p = sub.add_parser("sample", parents=[common], help="cheap look: n rows + measured per-field coverage")
    p.add_argument("source", nargs="+")
    p.add_argument("-n", type=int, default=5)
    p.set_defaults(fn=cmd_sample)

    p = sub.add_parser("query", parents=[common], help="DuckDB over the cache; per-source views plus `trials`")
    p.add_argument("sql")
    p.add_argument("--limit", type=int, default=50)
    p.set_defaults(fn=cmd_query, source=None)

    args = ap.parse_args(argv)
    if not hasattr(args, "json"):
        args.json = False
    args.fn(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
