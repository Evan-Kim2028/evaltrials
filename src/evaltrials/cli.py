"""evaltrials - index of public AI-evaluation run data.

`list` and `show` read the registry. `render` regenerates README.md from it.
Emits JSON when --json is passed or stdout is not a TTY.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

from .card import load_all
from .render import ROOT, human_bytes, render


def _emit(obj, args) -> None:
    if getattr(args, "json", False) or not sys.stdout.isatty():
        json.dump(obj, sys.stdout, indent=2, default=str)
        sys.stdout.write("\n")
    else:
        print(json.dumps(obj, indent=2, default=str))


def _row(e) -> dict:
    return {
        "id": e.id, "kind": e.kind, "unit": e.unit,
        "multi_trial": e.multi_trial, "trajectories": e.trajectories,
        "rows": e.scale.get("rows"), "bytes": e.bytes,
        "bytes_human": human_bytes(e.bytes),
        "cost_usd": e.cost.get("usd"), "cost_basis": e.cost.get("basis"),
        "license": e.license.get("spdx"),
        "redistributable": e.license.get("redistributable"),
        "gate": e.gate,
    }


def cmd_list(args):
    rows = [_row(e) for e in load_all().values()]
    if args.kind:
        rows = [r for r in rows if r["kind"] == args.kind]
    if args.gate:
        rows = [r for r in rows if r["gate"] == args.gate]
    if args.multi_trial:
        rows = [r for r in rows if r["multi_trial"] == args.multi_trial]
    if args.redistributable:
        rows = [r for r in rows if r["redistributable"]]
    if args.has_cost:
        rows = [r for r in rows if r["cost_usd"]]
    rows.sort(key=lambda r: -(r["rows"] or 0))
    _emit({"n": len(rows), "datasets": rows}, args)


def cmd_show(args):
    all_e = load_all()
    out = []
    for i in args.id:
        if i not in all_e:
            raise SystemExit(f"unknown id {i!r}. try `evaltrials list`.")
        out.append(all_e[i].raw)
    _emit(out[0] if len(out) == 1 else out, args)


def cmd_render(args):
    text = render(load_all())
    target = pathlib.Path(ROOT) / "README.md"
    if args.check:
        current = target.read_text() if target.exists() else ""
        if current != text:
            print(f"README.md is stale: {len(current)} bytes on disk, "
                  f"{len(text)} bytes generated. run `evaltrials render`.", file=sys.stderr)
            return 1
        print("README.md is up to date.")
        return 0
    target.write_text(text)
    print(f"wrote {target} ({len(text)} bytes)")
    return 0


def main(argv=None) -> int:
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--json", action="store_true", default=argparse.SUPPRESS,
                        help="force JSON (default when stdout is not a TTY)")

    ap = argparse.ArgumentParser(prog="evaltrials", parents=[common],
                                 description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("list", parents=[common], help="list indexed datasets")
    p.add_argument("--kind")
    p.add_argument("--gate")
    p.add_argument("--multi-trial", dest="multi_trial")
    p.add_argument("--redistributable", action="store_true")
    p.add_argument("--has-cost", dest="has_cost", action="store_true")
    p.set_defaults(fn=cmd_list)

    p = sub.add_parser("show", parents=[common], help="full entry for one or more ids")
    p.add_argument("id", nargs="+")
    p.set_defaults(fn=cmd_show)

    p = sub.add_parser("render", parents=[common], help="regenerate README.md from the registry")
    p.add_argument("--check", action="store_true", help="exit 1 if README.md is stale")
    p.set_defaults(fn=cmd_render)

    args = ap.parse_args(argv)
    if not hasattr(args, "json"):
        args.json = False
    return args.fn(args) or 0


if __name__ == "__main__":
    raise SystemExit(main())
