"""The canonical row contract."""
import pytest

from evaltrials import schema


def test_blank_row_has_every_column():
    row = schema.blank_row()
    assert set(row) == set(schema.COLUMNS)
    assert list(row) == schema.COLUMNS  # stable order
    assert all(v is None for v in row.values())


def test_blank_row_accepts_known_keys():
    row = schema.blank_row(source="harbor-adapter", unit="trial", reward=1.0)
    assert row["source"] == "harbor-adapter"
    assert row["unit"] == "trial"
    assert row["reward"] == 1.0
    assert row["task_id"] is None  # untouched columns stay null


def test_blank_row_rejects_unknown_key():
    with pytest.raises(ValueError, match="not in canonical schema"):
        schema.blank_row(bogus_column=1)


def test_column_lists_have_no_duplicates():
    assert len(schema.COLUMNS) == len(set(schema.COLUMNS))


def test_every_typed_column_is_a_column():
    for c in schema.TYPES:
        assert c in schema.COLUMNS, f"TYPES declares {c!r} which is not in COLUMNS"
