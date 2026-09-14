"""yoonholee/terminalbench-trajectories -> canonical trials.

unit=trial. 52,104 rows, 89 TB tasks, 26 scaffolds, 49 models, Apache-2.0.
Joins to harbor-adapter on task_id (identical TB slug namespace).
"""
from __future__ import annotations

import json
import pathlib

import pyarrow.parquet as pq

from ..aliases import normalize_agent, normalize_model
from ..schema import blank_row
from ._util import hf_download, to_table

FILES = ["data/train-00000-of-00002.parquet", "data/train-00001-of-00002.parquet"]


def fetch(card, dest: pathlib.Path, asset=None, from_path=None) -> list[pathlib.Path]:
    if from_path:
        return [pathlib.Path(from_path)]
    rev = card.upstream.get("revision")
    return [pathlib.Path(hf_download(card.upstream["repo"], f, dest, rev)) for f in FILES]


def _derive_steps(steps_val):
    """Tier-2 from Tier-3. Count steps and tool calls; never keep the body."""
    if steps_val in (None, "", "null"):
        return None, None
    try:
        s = json.loads(steps_val) if isinstance(steps_val, str) else steps_val
    except (ValueError, TypeError):
        return None, None
    if not isinstance(s, list):
        return None, None
    n_tools = sum(1 for x in s if isinstance(x, dict) and (x.get("tool_calls") or x.get("tool")))
    return len(s), n_tools


def normalize(card, paths) -> "pa.Table":  # noqa: F821
    lic = card.license
    rows = []
    for p in paths:
        tbl = pq.read_table(p)
        d = tbl.to_pydict()
        n = tbl.num_rows
        # per-cell trial ordering: upstream has no trial_index, so derive one
        seen: dict[tuple, int] = {}
        for i in range(n):
            task = d["task_name"][i]
            agent_raw, model_raw = d["agent"][i], d["model"][i]
            agent, model = normalize_agent(agent_raw), normalize_model(model_raw)
            key = (task, agent, model)
            idx = seen.get(key, 0)
            seen[key] = idx + 1
            reward = d["reward"][i]
            n_steps, n_tools = _derive_steps(d.get("steps", [None] * n)[i])
            cost_cents = d.get("cost_cents", [None] * n)[i]
            rows.append(blank_row(
                source=card.id, unit="trial", benchmark="terminal-bench",
                task_id=task, agent=agent, model=model,
                agent_raw=agent_raw, model_raw=model_raw,
                trial_index=idx, trial_id=d.get("trial_id", [None] * n)[i],
                reward=reward,
                outcome=None if reward is None else (1.0 if float(reward) > 0 else 0.0),
                started_at=d.get("started_at", [None] * n)[i],
                ended_at=d.get("ended_at", [None] * n)[i],
                duration_sec=d.get("duration_seconds", [None] * n)[i],
                input_tokens=d.get("input_tokens", [None] * n)[i],
                output_tokens=d.get("output_tokens", [None] * n)[i],
                cost_usd=None if cost_cents is None else float(cost_cents) / 100.0,
                n_steps=n_steps, n_tool_calls=n_tools,
                license_spdx=lic.get("spdx"), redistributable=lic.get("redistributable"),
                verified_by=card.raw.get("verified_by"),
            ))
    return to_table(rows)
