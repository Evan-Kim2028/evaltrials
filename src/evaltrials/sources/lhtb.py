"""IntelligenceLab/LHTB-leaderboard -> canonical CELLS.

unit=cell on purpose: the per_task config has no trial_id. The 51.6 GB of raw
submissions (single asciinema casts reach 9.8 GB) are never fetched by default.
"""
from __future__ import annotations

import json
import pathlib
import urllib.parse
import urllib.request

from ..aliases import normalize_agent, normalize_model
from ..schema import blank_row
from ._util import to_table

ROWS_URL = ("https://datasets-server.huggingface.co/rows"
            "?dataset={ds}&config=per_task&split=train&offset={off}&length=100")


def fetch(card, dest: pathlib.Path, asset=None, from_path=None) -> list[pathlib.Path]:
    if from_path:
        return [pathlib.Path(from_path)]
    if asset == "submissions":
        raise NotImplementedError(
            "the `submissions` asset is 51.6 GB across 66,805 files. Fetch a single "
            "submission path from the card instead of the whole tree."
        )
    ds = urllib.parse.quote(card.upstream["repo"], safe="")
    out, off = [], 0
    dest.mkdir(parents=True, exist_ok=True)
    target = dest / "per_task.jsonl"
    with open(target, "w") as fh:
        while True:
            with urllib.request.urlopen(ROWS_URL.format(ds=ds, off=off), timeout=60) as r:
                payload = json.load(r)
            batch = payload.get("rows") or []
            for item in batch:
                fh.write(json.dumps(item["row"]) + "\n")
            off += len(batch)
            if len(batch) < 100 or off >= (payload.get("num_rows_total") or 0):
                break
    out.append(target)
    return out


def normalize(card, paths) -> "pa.Table":  # noqa: F821
    lic, rows = card.license, []
    for p in paths:
        with open(p) as fh:
            for line in fh:
                if not line.strip():
                    continue
                r = json.loads(line)
                reward = r.get("reward")
                solved = r.get("solved")
                rows.append(blank_row(
                    source=card.id, unit="cell", benchmark="long-horizon-terminal-bench",
                    task_id=r.get("task_id"),
                    agent=normalize_agent(r.get("agent")),
                    model=normalize_model(r.get("model_id") or r.get("model")),
                    agent_raw=r.get("agent"), model_raw=r.get("model"),
                    reward=reward,
                    outcome=None if solved is None else (1.0 if solved else 0.0),
                    exception_type=r.get("exception"),
                    trajectory_uri=r.get("submission_path"),
                    license_spdx=lic.get("spdx"), redistributable=lic.get("redistributable"),
                    verified_by=card.raw.get("verified_by"),
                ))
    return to_table(rows)
