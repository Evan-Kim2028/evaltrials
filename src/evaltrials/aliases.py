"""Model and agent string normalization.

The single largest source of silent join failures. Harbor writes
`claude-haiku-4-5-20251001`; the Terminal-Bench scrape writes
`claude-opus-4-5-20251101@anthropic`; leaderboards write display names.
"""
from __future__ import annotations

import re

_PROVIDER_SUFFIX = re.compile(r"@[a-z0-9_.-]+$", re.I)
_DATE_SUFFIX = re.compile(r"[-_](20\d{6})$")


def normalize_model(raw: str | None) -> str | None:
    """Strip provider suffix and release date; lowercase; unify separators.

    claude-opus-4-5-20251101@anthropic -> claude-opus-4.5
    claude-haiku-4-5-20251001          -> claude-haiku-4.5
    """
    if not raw:
        return None
    s = str(raw).strip()
    s = _PROVIDER_SUFFIX.sub("", s)
    s = _DATE_SUFFIX.sub("", s)
    s = s.lower().replace("_", "-")
    # collapse "-4-5" / "-4-6" version segments into "4.5"
    s = re.sub(r"-(\d+)-(\d+)(?=$|-)", r"-\1.\2", s)
    return s


_AGENT_MAP = {
    "claude code": "claude-code",
    "claude-code": "claude-code",
    "terminus 2": "terminus-2",
    "terminus-2": "terminus-2",
    "codex": "codex",
    "gemini cli": "gemini-cli",
    "gemini-cli": "gemini-cli",
    "qwen coder": "qwen-coder",
    "qwen-coder": "qwen-coder",
    "openhands": "openhands",
}


def normalize_agent(raw: str | None) -> str | None:
    if not raw:
        return None
    s = str(raw).strip().lower()
    if s in _AGENT_MAP:
        return _AGENT_MAP[s]
    return re.sub(r"\s+", "-", s)
