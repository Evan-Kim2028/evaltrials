#!/usr/bin/env python3
"""Re-check every registry entry against its upstream. Maintainer tool.

Numbers drift. This re-reads sizes and row counts from the HuggingFace API and
reports where the registry disagrees, so `rows_note` and `verified` stay true.

The token, if you have one, comes from the environment or the standard
HuggingFace location. It is never read from, or written to, this repository:

    export HF_TOKEN=...                  # or
    huggingface-cli login                # writes ~/.cache/huggingface/token

Without a token, gated datasets report 401 and are left marked UNVERIFIED,
which is the correct outcome rather than a silent gap.
"""
from __future__ import annotations

import json
import os
import pathlib
import sys
import urllib.error
import urllib.parse
import urllib.request

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))
from evaltrials.card import load_all  # noqa: E402

API = "https://huggingface.co/api/datasets/{repo}?blobs=true"
SIZE = "https://datasets-server.huggingface.co/size?dataset={ds}"


def token() -> str | None:
    """Environment first, then the standard HF file. Never the repo."""
    for var in ("HF_TOKEN", "HUGGING_FACE_HUB_TOKEN", "HUGGINGFACEHUB_API_TOKEN"):
        if os.environ.get(var):
            return os.environ[var].strip()
    for p in (pathlib.Path.home() / ".cache/huggingface/token",
              pathlib.Path.home() / ".huggingface/token"):
        if p.is_file():
            val = p.read_text().strip()
            if val:
                return val
    return None


def _get(url: str, tok: str | None):
    req = urllib.request.Request(url)
    if tok:
        req.add_header("Authorization", f"Bearer {tok}")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r), None
    except urllib.error.HTTPError as e:
        return None, f"http {e.code}"
    except Exception as e:  # noqa: BLE001
        return None, str(e)[:40]


def main() -> int:
    tok = token()
    print(f"token: {'present' if tok else 'absent (gated entries will 401)'}\n")
    drift = 0
    for e in load_all().values():
        repo = e.upstream.get("repo")
        if not repo or "huggingface.co/datasets" not in (e.upstream.get("url") or ""):
            continue
        meta, err = _get(API.format(repo=repo), tok)
        if err:
            print(f"{e.id:<32} unreachable ({err})")
            continue
        got_bytes = sum(s.get("size") or 0 for s in (meta.get("siblings") or []))
        size, _ = _get(SIZE.format(ds=urllib.parse.quote(repo, safe="")), tok)
        sz = (size or {}).get("size") or {}
        got_rows = sz.get("dataset", {}).get("num_rows")
        # If the entry says which config its rows refer to, compare against THAT
        # config. Otherwise a multi-config dataset reports drift forever.
        per = {c["config"]: c["num_rows"] for c in sz.get("configs", [])}
        want_cfg = e.scale.get("rows_config")
        want_cfgs = e.scale.get("rows_configs")
        if want_cfg:
            got_rows = per.get(want_cfg, got_rows)
        elif want_cfgs:
            # some datasets ship a `default` config that restates the real ones
            picked = [per[c] for c in want_cfgs if c in per]
            if picked:
                got_rows = sum(picked)

        msgs = []
        if e.bytes and got_bytes and abs(e.bytes - got_bytes) / got_bytes > 0.05:
            msgs.append(f"bytes {e.bytes:,} -> {got_bytes:,}")
        if e.scale.get("rows") and got_rows and got_rows != e.scale["rows"]:
            msgs.append(f"rows {e.scale['rows']:,} -> {got_rows:,} (may be a config split)")
        if msgs:
            drift += 1
            print(f"{e.id:<32} DRIFT  " + " | ".join(msgs))
        else:
            print(f"{e.id:<32} ok")
    print(f"\n{drift} entr{'y' if drift == 1 else 'ies'} drifted from the registry.")
    return 1 if drift else 0


if __name__ == "__main__":
    raise SystemExit(main())
