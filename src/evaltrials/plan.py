"""Preflight. Zero I/O. Tells an agent the price before it pays."""
from __future__ import annotations

from . import cache
from .card import Card

THROUGHPUT_BPS = 40 * 1024 * 1024  # conservative 40 MB/s


def human_bytes(n: int | None) -> str:
    if not n:
        return "0 B"
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if n < 1024 or unit == "TB":
            return f"{n:.1f} {unit}" if unit != "B" else f"{int(n)} B"
        n /= 1024.0
    return f"{n:.1f} TB"


def _gate_verdict(card: Card) -> tuple[str, list[str]]:
    blockers: list[str] = []
    if card.status != "implemented":
        blockers.append(f"source status is '{card.status}': no fetcher yet")
    if card.gate == "hf-gated":
        blockers.append("requires an HF token and accepted dataset terms (HF_TOKEN)")
    if card.gate == "encrypted":
        blockers.append("upstream encrypts traces on purpose; decrypt is user-side and opt-in")
    if card.gate == "unknown":
        blockers.append("gate unknown; probe upstream before scripting against it")
    if blockers:
        return ("blocked" if card.status != "implemented" else "needs-action"), blockers
    return "ok", []


def plan_source(card: Card, asset: str | None = None) -> dict:
    assets = card.raw.get("assets") or []
    if asset:
        chosen = [a for a in assets if a.get("name") == asset]
        if not chosen:
            raise KeyError(f"{card.id}: no asset named {asset!r}; have {[a.get('name') for a in assets]}")
    else:
        # An asset may declare itself the default (the one the fetcher implements).
        # Otherwise take the cheapest. Never default to 340 GB.
        explicit = [a for a in assets if a.get("default")]
        if explicit:
            chosen = explicit
        else:
            sized = [a for a in assets if a.get("bytes")]
            chosen = [min(sized, key=lambda a: a["bytes"])] if sized else assets[:1]

    nbytes = sum(int(a.get("bytes") or 0) for a in chosen)
    verdict, blockers = _gate_verdict(card)
    free = cache.disk_free_bytes()
    if nbytes > free:
        verdict, blockers = "blocked", blockers + [
            f"needs {human_bytes(nbytes)}, cache disk has {human_bytes(free)} free"
        ]

    obligations = []
    if card.license.get("attribution"):
        obligations.append(f"attribute: {card.license['attribution']}")
    if not card.redistributable:
        obligations.append("NOT redistributable: fetch from upstream, never mirror the bytes")

    return {
        "source": card.id,
        "verdict": verdict,
        "unit": card.unit,
        "assets": [a.get("name") for a in chosen],
        "download_bytes": nbytes,
        "download_human": human_bytes(nbytes),
        "download_sec_est": round(nbytes / THROUGHPUT_BPS, 1) if nbytes else 0.0,
        "download_usd": 0.0,
        "license": card.license.get("spdx"),
        "gate": card.gate,
        "blockers": blockers,
        "obligations": obligations,
        "skipped_assets": [
            {"name": a.get("name"), "bytes": a.get("bytes"), "human": human_bytes(a.get("bytes")),
             "note": a.get("note")}
            for a in assets if a not in chosen and a.get("bytes")
        ],
        "caveats": card.caveats,
    }


def plan(cards: list[Card], asset: str | None = None) -> dict:
    per = [plan_source(c, asset) for c in cards]
    total = sum(p["download_bytes"] for p in per)
    return {
        "sources": per,
        "total_bytes": total,
        "total_human": human_bytes(total),
        "total_sec_est": round(total / THROUGHPUT_BPS, 1) if total else 0.0,
        "total_usd": 0.0,
        "verdict": "blocked" if any(p["verdict"] == "blocked" for p in per)
                   else ("needs-action" if any(p["verdict"] == "needs-action" for p in per) else "ok"),
        "disk_free_human": human_bytes(cache.disk_free_bytes()),
    }
