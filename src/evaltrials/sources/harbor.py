"""kendx/Harbor-Adapter -> canonical trials.

Two very different assets:
  manifest      16 MB, unit=cell, NO reward column.
  trajectories  340 GB across 495 shard parquets. per-shard only, never whole.

If you already extracted trial rows locally (task_validation produces
`harbor_adapter_traj.jsonl`), pass --from <path> and skip the network entirely.
"""
from __future__ import annotations

import json
import pathlib

import pyarrow.parquet as pq

from ..aliases import normalize_agent, normalize_model
from ..schema import blank_row
from ._util import hf_download, to_table

MANIFEST = "harbor_adapters.manifest.parquet"


def fetch(card, dest: pathlib.Path, asset=None, from_path=None) -> list[pathlib.Path]:
    if from_path:
        return [pathlib.Path(from_path)]
    if asset in (None, "manifest"):
        rev = card.upstream.get("revision")
        return [pathlib.Path(hf_download(card.upstream["repo"], MANIFEST, dest, rev))]
    raise NotImplementedError(
        "the `trajectories` asset is 340 GB across 495 shards. Fetch specific shards "
        "with `--asset trajectories --shard data/harbor_adapters/<benchmark>/NNNNN.parquet`, "
        "or import already-extracted rows with `--from <path.jsonl>`."
    )


def _from_manifest(card, path) -> list[dict]:
    """Manifest is cell-level and carries no reward. Say so on every row."""
    d = pq.read_table(path).to_pydict()
    lic, rows = card.license, []
    for i in range(len(d["benchmark"])):
        trial_ids = d["trial_ids"][i] or []
        rows.append(blank_row(
            source=card.id, unit="cell", benchmark=d["benchmark"][i],
            task_id=d["task_name"][i],
            agent=normalize_agent(d["agent"][i]), model=normalize_model(d["model"][i]),
            agent_raw=d["agent"][i], model_raw=d["model"][i],
            reward=None, outcome=None,
            n_steps=None, trial_index=None, trial_id=None,
            license_spdx=lic.get("spdx"), redistributable=lic.get("redistributable"),
            verified_by=card.raw.get("verified_by"),
            trajectory_uri=f"hf://datasets/{card.upstream['repo']}#trials={len(trial_ids)}",
        ))
    return rows


def _from_extracted_jsonl(card, path) -> list[dict]:
    """Rows produced by task_validation's harbor_adapter_traj extractor."""
    lic, rows = card.license, []
    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            reward = r.get("reward")
            rows.append(blank_row(
                source=card.id, unit="trial", benchmark=r.get("benchmark"),
                task_id=r.get("task_name"),
                agent=normalize_agent(r.get("agent")), model=normalize_model(r.get("model")),
                agent_raw=r.get("agent"), model_raw=r.get("model"),
                trial_index=r.get("trial_index"), trial_id=r.get("trial_id"),
                reward=reward,
                outcome=None if reward is None else (1.0 if float(reward) > 0 else 0.0),
                started_at=r.get("first_step_at"), ended_at=r.get("last_step_at"),
                duration_sec=r.get("agent_wall_sec"),
                n_steps=r.get("n_steps"), n_tool_calls=r.get("n_tool_calls"),
                exception_type=r.get("exception_type"), hit_timeout=r.get("hit_timeout"),
                mentions_answer_file=r.get("mentions_answer_file"),
                git_history_probe=r.get("git_history_probe"),
                network_fetch=r.get("network_fetch"),
                archive_sha256=r.get("archive_sha256"),
                trajectory_uri=f"hf://datasets/{card.upstream['repo']}/{r.get('shard')}",
                license_spdx=lic.get("spdx"), redistributable=lic.get("redistributable"),
                verified_by=card.raw.get("verified_by"),
            ))
    return rows


def normalize(card, paths) -> "pa.Table":  # noqa: F821
    rows = []
    for p in paths:
        p = pathlib.Path(p)
        if p.suffix == ".jsonl":
            rows += _from_extracted_jsonl(card, p)
        else:
            rows += _from_manifest(card, p)
    return to_table(rows)
