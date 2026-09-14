"""Round-trip a tiny harbor_adapter_traj fixture through normalize()."""
import pathlib

import pytest

from evaltrials import schema, sources
from evaltrials.card import load_all

FIXTURE = pathlib.Path(__file__).resolve().parent / "fixtures" / "harbor_sample.jsonl"


@pytest.fixture(scope="module")
def table():
    card = load_all()["harbor-adapter"]
    return sources.harbor.normalize(card, [FIXTURE])


def test_columns_are_exactly_canonical(table):
    assert table.column_names == schema.COLUMNS


def test_three_rows_all_trial_unit(table):
    assert table.num_rows == 3
    units = table.column("unit").to_pylist()
    assert units == ["trial", "trial", "trial"]


def test_outcome_is_one_when_reward_positive(table):
    rewards = table.column("reward").to_pylist()
    outcomes = table.column("outcome").to_pylist()
    for r, o in zip(rewards, outcomes):
        if r is None:
            assert o is None
        elif r > 0:
            assert o == 1.0
        else:
            assert o == 0.0
    # fixture specifics: rewards 1.0, 0.0, 0.5
    assert outcomes == [1.0, 0.0, 1.0]


def test_provenance_and_derived_fields(table):
    d = table.to_pydict()
    assert d["source"] == ["harbor-adapter"] * 3
    assert d["license_spdx"] == ["other"] * 3
    assert d["redistributable"] == [False] * 3
    assert d["verified_by"] == ["official-harness"] * 3
    assert d["n_steps"] == [14, 22, 9]
    assert d["duration_sec"] == [412.5, 900.0, 233.75]
    assert d["hit_timeout"] == [False, True, False]
    assert d["mentions_answer_file"] == [0, 1, 0]
    assert all(uri.startswith("hf://datasets/kendx/Harbor-Adapter/")
               for uri in d["trajectory_uri"])


def test_aliases_applied_but_raw_kept(table):
    d = table.to_pydict()
    assert d["model"] == ["claude-haiku-4.5", "claude-haiku-4.5", "gpt-5.2-codex"]
    assert d["model_raw"] == [
        "claude-haiku-4-5-20251001", "claude-haiku-4-5-20251001", "gpt-5.2-codex@openai"
    ]
    assert d["agent"] == ["claude-code", "terminus-2", "codex"]
    assert d["agent_raw"] == ["claude-code", "terminus-2", "Codex"]
