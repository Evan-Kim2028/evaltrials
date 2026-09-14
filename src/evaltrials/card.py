"""Source cards: the machine-readable description an agent reads before acting."""
from __future__ import annotations

import pathlib
from dataclasses import dataclass, field
from typing import Any

import yaml

REGISTRY_DIR = pathlib.Path(__file__).resolve().parents[2] / "registry"

VALID_UNITS = {"trial", "cell", "score"}
VALID_GATES = {"open", "hf-gated", "encrypted", "ask-first", "unknown"}
VALID_STATUS = {"implemented", "planned"}


@dataclass
class Card:
    id: str
    title: str
    status: str
    unit: str
    upstream: dict
    license: dict
    gate: str
    raw: dict = field(repr=False, default_factory=dict)

    # -- derived, agent-facing ------------------------------------------------
    @property
    def bytes_total(self) -> int:
        return sum(int(a.get("bytes") or 0) for a in self.raw.get("assets") or [])

    @property
    def bytes_cheapest(self) -> int:
        """Smallest asset - what `sample` and a first look actually cost."""
        sizes = [int(a.get("bytes") or 0) for a in self.raw.get("assets") or []]
        sizes = [s for s in sizes if s]
        return min(sizes) if sizes else 0

    @property
    def redistributable(self) -> bool:
        return bool(self.license.get("redistributable"))

    @property
    def scale(self) -> dict:
        return self.raw.get("scale") or {}

    @property
    def fields(self) -> dict:
        return self.raw.get("fields") or {}

    @property
    def joins_with(self) -> list:
        return self.raw.get("joins_with") or []

    @property
    def caveats(self) -> list:
        return self.raw.get("caveats") or []

    def asset(self, name: str) -> dict | None:
        for a in self.raw.get("assets") or []:
            if a.get("name") == name:
                return a
        return None

    def summary(self) -> dict:
        """One compact line per source. This is what fits in an agent's context."""
        return {
            "id": self.id,
            "status": self.status,
            "unit": self.unit,
            "rows": self.scale.get("rows") or self.scale.get("cells"),
            "benchmarks": self.scale.get("benchmarks"),
            "tasks": self.scale.get("tasks"),
            "models": self.scale.get("models"),
            "agents": self.scale.get("agents"),
            "bytes_min": self.bytes_cheapest,
            "bytes_max": self.bytes_total,
            "license": self.license.get("spdx"),
            "redistributable": self.redistributable,
            "gate": self.gate,
            "verified_by": self.raw.get("verified_by"),
        }


def _validate(d: dict, where: str) -> None:
    for k in ("id", "title", "status", "unit", "upstream", "license", "gate"):
        if k not in d:
            raise ValueError(f"{where}: card missing required key {k!r}")
    if d["unit"] not in VALID_UNITS:
        raise ValueError(f"{where}: unit {d['unit']!r} not in {sorted(VALID_UNITS)}")
    if d["gate"] not in VALID_GATES:
        raise ValueError(f"{where}: gate {d['gate']!r} not in {sorted(VALID_GATES)}")
    if d["status"] not in VALID_STATUS:
        raise ValueError(f"{where}: status {d['status']!r} not in {sorted(VALID_STATUS)}")
    if "redistributable" not in d["license"]:
        raise ValueError(f"{where}: license.redistributable is required (fail closed)")


def _mk(d: dict, where: str) -> Card:
    _validate(d, where)
    return Card(
        id=d["id"], title=d["title"], status=d["status"], unit=d["unit"],
        upstream=d["upstream"], license=d["license"], gate=d["gate"], raw=d,
    )


def load_all(registry_dir: pathlib.Path | None = None) -> dict[str, Card]:
    rd = pathlib.Path(registry_dir or REGISTRY_DIR)
    cards: dict[str, Card] = {}
    for p in sorted(rd.glob("*.yaml")):
        doc: Any = yaml.safe_load(p.read_text())
        docs = doc if isinstance(doc, list) else [doc]
        for d in docs:
            c = _mk(d, p.name)
            if c.id in cards:
                raise ValueError(f"duplicate source id {c.id!r} in {p.name}")
            cards[c.id] = c
    return cards
