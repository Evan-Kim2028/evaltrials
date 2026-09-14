"""Alias normalization: the fix for the largest silent join failure."""
import pytest

from evaltrials.aliases import normalize_agent, normalize_model

MODEL_CASES = [
    ("claude-opus-4-5-20251101@anthropic", "claude-opus-4.5"),
    ("claude-opus-4-5", "claude-opus-4.5"),
    ("claude-haiku-4-5-20251001", "claude-haiku-4.5"),
    ("claude-sonnet-4-5-20250929@anthropic", "claude-sonnet-4.5"),
    ("gpt-5.2-codex@openai", "gpt-5.2-codex"),
    ("Claude_Opus_4_5", "claude-opus-4.5"),  # underscores unify, version collapses
    ("gemini-3-pro-preview", "gemini-3-pro-preview"),
    ("  claude-haiku-4-5  ", "claude-haiku-4.5"),
    (None, None),
    ("", None),
]

AGENT_CASES = [
    ("Factory Droid", "factory-droid"),
    ("Claude Code", "claude-code"),
    ("claude-code", "claude-code"),
    ("Terminus 2", "terminus-2"),
    ("Gemini CLI", "gemini-cli"),
    ("Qwen Coder", "qwen-coder"),
    ("Some Brand New Scaffold", "some-brand-new-scaffold"),
    (None, None),
    ("", None),
]


@pytest.mark.parametrize("raw,expected", MODEL_CASES)
def test_normalize_model(raw, expected):
    assert normalize_model(raw) == expected


@pytest.mark.parametrize("raw,expected", AGENT_CASES)
def test_normalize_agent(raw, expected):
    assert normalize_agent(raw) == expected


def test_dated_and_undated_model_ids_join():
    """The two spellings of the same model must land on the same key."""
    assert normalize_model("claude-opus-4-5-20251101@anthropic") == normalize_model(
        "claude-opus-4-5"
    )
