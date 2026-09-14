"""Index entries. One YAML block per public eval-run dataset.

This repo is an index, not a pipeline. Nothing here downloads, normalizes or
rehosts anything. Each entry records what a dataset holds, how big it is, what
it costs to use, and — where the number exists — what it cost to *produce*.
"""
from __future__ import annotations

import pathlib
from dataclasses import dataclass, field

import yaml

REGISTRY_DIR = pathlib.Path(__file__).resolve().parents[2] / "registry"

KINDS = {"agent-trials", "llm-scores", "labeled-traces", "meta-index", "sft-traces"}
UNITS = {"trial", "cell", "score", "trajectory", "collection"}
GATES = {"open", "hf-gated", "account", "encrypted", "unknown"}
MULTI = {"yes", "no", "partial", "unknown"}
TRAJ = {"full", "derived", "none", "encrypted", "partial"}


@dataclass
class Entry:
    id: str
    title: str
    kind: str
    unit: str
    multi_trial: str
    trajectories: str
    upstream: dict
    license: dict
    gate: str
    raw: dict = field(repr=False, default_factory=dict)

    @property
    def scale(self) -> dict:
        return self.raw.get("scale") or {}

    @property
    def cost(self) -> dict:
        return self.raw.get("cost") or {}

    @property
    def bytes(self) -> int | None:
        return self.raw.get("bytes")

    @property
    def notes(self) -> list:
        return self.raw.get("notes") or []

    @property
    def cost_per_trial(self) -> float | None:
        usd, rows = self.cost.get("usd"), self.scale.get("rows")
        if usd and rows:
            return usd / rows
        return None


REQUIRED = ("id", "title", "kind", "unit", "multi_trial", "trajectories",
            "upstream", "license", "gate")


def _validate(d: dict, where: str) -> None:
    for k in REQUIRED:
        if k not in d:
            raise ValueError(f"{where}: entry missing required key {k!r}")
    for k, allowed in (("kind", KINDS), ("unit", UNITS), ("gate", GATES),
                       ("multi_trial", MULTI), ("trajectories", TRAJ)):
        if d[k] not in allowed:
            raise ValueError(f"{where}: {k}={d[k]!r} not in {sorted(allowed)}")
    if "redistributable" not in d["license"]:
        raise ValueError(f"{where}: license.redistributable is required (fail closed)")
    cost = d.get("cost") or {}
    if cost.get("usd") is not None and cost.get("basis") not in ("measured", "reported", "estimated"):
        raise ValueError(f"{where}: cost.usd needs basis measured|reported|estimated")


def load_all(registry_dir=None) -> dict[str, Entry]:
    rd = pathlib.Path(registry_dir or REGISTRY_DIR)
    out: dict[str, Entry] = {}
    for p in sorted(rd.glob("*.yaml")):
        doc = yaml.safe_load(p.read_text())
        for d in (doc if isinstance(doc, list) else [doc]):
            _validate(d, p.name)
            if d["id"] in out:
                raise ValueError(f"duplicate id {d['id']!r} in {p.name}")
            out[d["id"]] = Entry(
                id=d["id"], title=d["title"], kind=d["kind"], unit=d["unit"],
                multi_trial=d["multi_trial"], trajectories=d["trajectories"],
                upstream=d["upstream"], license=d["license"], gate=d["gate"], raw=d,
            )
    return out
