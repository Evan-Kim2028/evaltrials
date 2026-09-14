"""Render the README from the registry. The YAML is the source of truth."""
from __future__ import annotations

import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs"

BASIS_MARK = {"measured": "m", "reported": "r", "estimated": "e"}

KIND_ORDER = ["agent-trials", "llm-scores", "labeled-traces", "sft-traces", "meta-index"]
KIND_TITLE = {
    "agent-trials": "Agent evaluation runs",
    "llm-scores": "Score tables",
    "labeled-traces": "Human-labelled traces",
    "sft-traces": "Training trajectory dumps (not evaluation)",
    "meta-index": "Other indexes",
}


def human_bytes(n) -> str:
    if not n:
        return "—"
    n = float(n)
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if n < 1024 or unit == "TB":
            return f"{n:.0f} B" if unit == "B" else f"{n:.1f} {unit}"
        n /= 1024.0
    return f"{n:.1f} TB"


def _num(n) -> str:
    return f"{n:,}" if isinstance(n, int) else "—"


def _cost(entry) -> str:
    usd = entry.cost.get("usd")
    if not usd:
        return "—"
    return f"${usd:,.0f} ({BASIS_MARK.get(entry.cost.get('basis'), '?')})"


def _license(entry) -> str:
    spdx = entry.license.get("spdx") or "unset"
    return spdx if entry.license.get("redistributable") else f"{spdx} ⚠"


def _sort_key(e):
    """Most recently run first. That is what people want to see at the top."""
    return (_invert(e.run_date_key), e.id)


def _invert(key: str) -> str:
    """Descending string sort without reverse=, so ties stay id-ascending."""
    return "".join(chr(0x7E - ord(c)) if c.isdigit() else c for c in key)


def _detail_sort_key(e):
    kind_rank = KIND_ORDER.index(e.kind) if e.kind in KIND_ORDER else len(KIND_ORDER)
    return (kind_rank, _invert(e.run_date_key), e.id)


def _runs(e) -> str:
    r = e.runs
    first, last, basis = r.get("first"), r.get("last"), r.get("basis")
    if not last:
        # No run dates at all. Say so, and show what the sort actually used.
        upstream = e.raw.get("updated")
        return f"unknown (upstream {upstream[:7]}) (u)" if upstream else "unknown"
    span = f"{first} → {last}" if first and first != last else str(last)
    mark = BASIS_MARK.get(basis)
    return f"{span} ({mark})" if mark else span


def _read(name: str) -> str:
    p = DOCS / name
    return p.read_text().rstrip() + "\n\n" if p.exists() else ""


def _table(entries) -> list[str]:
    out = [
        "| Dataset | Trials run | Kind | Unit | Multi-trial | Trajectories | Rows | Size | Cost to produce | License | Gate |",
        "| --- | --- | --- | --- | --- | --- | ---: | ---: | ---: | --- | --- |",
    ]
    for e in entries:
        url = e.upstream.get("url") or e.upstream.get("homepage") or ""
        name = f"[{e.title}]({url})" if url else e.title
        out.append(
            f"| {name} | {_runs(e)} | {e.kind} | {e.unit} | {e.multi_trial} | {e.trajectories} | "
            f"{_num(e.scale.get('rows'))} | {human_bytes(e.bytes)} | {_cost(e)} | "
            f"{_license(e)} | {e.gate} |"
        )
    return out


def _detail(e) -> list[str]:
    out = [f"### {e.title}", ""]
    links = []
    for key, label in (("url", "dataset"), ("repo", "repo"), ("paper", "paper"), ("homepage", "home")):
        v = e.upstream.get(key)
        if not v:
            continue
        links.append(f"[{label}]({v})" if v.startswith("http") else f"{label}: `{v}`")
    out.append(f"`{e.id}` · " + " · ".join(links))
    out.append("")
    r = e.runs
    if r.get("last"):
        out.append(f"- **trials run** {_runs(e)}" + (f" — {r['note']}" if r.get("note") else ""))
    out.append(f"- **unit** `{e.unit}` · **multi-trial** `{e.multi_trial}` · "
               f"**trajectories** `{e.trajectories}` · **gate** `{e.gate}`")
    if e.scale:
        out.append("- **scale** " + " · ".join(
            f"{k} {_num(v) if isinstance(v, int) else v}" for k, v in e.scale.items() if v is not None))
    if e.bytes:
        out.append(f"- **size** {human_bytes(e.bytes)}")
    cost = e.cost or {}
    if cost.get("usd"):
        bits = [f"**cost to produce** ${cost['usd']:,.0f} ({cost.get('basis')})"]
        for k, label in (("tokens_in", "input tokens"), ("tokens_out", "output tokens"),
                         ("agent_hours", "agent-hours")):
            if cost.get(k):
                bits.append(f"{label} {cost[k]:,}")
        out.append("- " + " · ".join(bits))
    if cost.get("note"):
        out.append(f"- **cost note** {cost['note']}")
    out.append(f"- **license** `{e.license.get('spdx')}`"
               + ("" if e.license.get("redistributable") else " — **not redistributable**"))
    if e.raw.get("updated"):
        out.append(f"- **upstream updated** {e.raw['updated']}")
    for n in e.notes:
        out.append(f"- {n}")
    out.append("")
    return out


def _totals(entries) -> list[str]:
    by_kind: dict[str, int] = {}
    for e in entries:
        by_kind[e.kind] = by_kind.get(e.kind, 0) + 1
    total_bytes = sum(e.bytes or 0 for e in entries)
    known = [e for e in entries if e.cost.get("usd")]
    total_cost = sum(e.cost["usd"] for e in known)
    out = ["## Totals", ""]
    out.append(f"- **{len(entries)} datasets indexed** — "
               + ", ".join(f"{v} {k}" for k, v in sorted(by_kind.items())))
    out.append(f"- **{human_bytes(total_bytes)}** of data across entries that report a size")
    out.append(f"- **${total_cost:,.0f}** of known compute spend, from the "
               f"{len(known)} of {len(entries)} entries where the cost is published or measurable")
    multi = [e for e in entries if e.multi_trial == "yes"]
    out.append(f"- **{len(multi)}** entries have repeated trials per cell; "
               f"{len(entries) - len(multi)} do not or do not say")
    out.append("")
    return out


def render(entries: dict) -> str:
    items = sorted(entries.values(), key=_sort_key)
    lines: list[str] = []
    intro = _read("intro.md")
    if intro:
        lines.append(intro.rstrip())
        lines.append("")
    lines.append("## Index")
    lines.append("")
    lines += _table(items)
    lines.append("")
    lines.append("Sorted by when the trials were run, most recent first. "
                 "`(m)` measured from the data itself · `(r)` reported by the authors · "
                 "`(e)` estimated · `(u)` no run dates published, so the upstream update date "
                 "is shown and used for sorting. `⚠` marks a dataset that may not be redistributed.")
    lines.append("")
    lines.append("## Detail")
    lines.append("")
    current = None
    for e in sorted(entries.values(), key=_detail_sort_key):
        if e.kind != current:
            current = e.kind
            lines.append(f"## {KIND_TITLE.get(e.kind, e.kind)}")
            lines.append("")
        lines += _detail(e)
    lines += _totals(items)
    outro = _read("outro.md")
    if outro:
        lines.append(outro.rstrip())
        lines.append("")
    lines.append("<!-- generated by `evaltrials render`; "
                 "edit registry/*.yaml and docs/intro.md, not this file -->")
    return "\n".join(lines) + "\n"
