from __future__ import annotations

import pyarrow as pa

from ..schema import COLUMNS, TYPES


def to_table(rows: list[dict]) -> pa.Table:
    """Build the canonical table with a stable column order and stable types."""
    cols = {}
    for c in COLUMNS:
        vals = [r.get(c) for r in rows]
        t = TYPES.get(c)
        if t == "int64":
            cols[c] = pa.array([None if v is None else int(v) for v in vals], type=pa.int64())
        elif t == "float64":
            cols[c] = pa.array([None if v is None else float(v) for v in vals], type=pa.float64())
        elif t == "bool":
            cols[c] = pa.array([None if v is None else bool(v) for v in vals], type=pa.bool_())
        else:
            cols[c] = pa.array([None if v is None else str(v) for v in vals], type=pa.string())
    return pa.table(cols)


def hf_download(repo: str, filename: str, dest, revision: str | None = None) -> str:
    try:
        from huggingface_hub import hf_hub_download
    except ImportError as e:  # pragma: no cover
        raise RuntimeError("pip install 'evaltrials[hf]' for HuggingFace sources") from e
    return hf_hub_download(
        repo_id=repo, filename=filename, repo_type="dataset",
        revision=revision, local_dir=str(dest),
    )
