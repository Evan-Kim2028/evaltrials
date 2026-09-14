"""Local cache. evaltrials never rehosts bytes; it caches them on your machine."""
from __future__ import annotations

import hashlib
import os
import pathlib

DEFAULT = pathlib.Path(os.environ.get("EVALTRIALS_CACHE", "~/.cache/evaltrials")).expanduser()


def root() -> pathlib.Path:
    DEFAULT.mkdir(parents=True, exist_ok=True)
    return DEFAULT


def source_dir(source_id: str) -> pathlib.Path:
    p = root() / source_id
    p.mkdir(parents=True, exist_ok=True)
    return p


def normalized_path(source_id: str) -> pathlib.Path:
    return source_dir(source_id) / "trials.parquet"


def sha256(path: str | pathlib.Path, chunk: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        while True:
            b = fh.read(chunk)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def verify(path, expected: str | None) -> tuple[bool, str]:
    """Fail closed: an unexpected hash is an error, a missing expectation is a warning."""
    got = sha256(path)
    if expected is None:
        return True, f"unpinned (sha256={got[:16]})"
    if got != expected:
        raise ValueError(f"sha256 mismatch for {path}: expected {expected}, got {got}")
    return True, "verified"


def disk_free_bytes(path=None) -> int:
    st = os.statvfs(str(path or root()))
    return st.f_bavail * st.f_frsize
