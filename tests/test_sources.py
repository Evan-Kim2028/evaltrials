"""Source module lookup."""
import pytest

from evaltrials import sources


def test_get_returns_module_for_implemented_ids():
    assert sources.get("harbor-adapter") is sources.harbor
    assert sources.get("terminalbench-yoonholee") is sources.terminalbench
    assert sources.get("lhtb-leaderboard") is sources.lhtb


def test_get_unknown_id_raises_helpful_keyerror():
    with pytest.raises(KeyError) as exc:
        sources.get("not-a-real-source")
    msg = str(exc.value)
    assert "not-a-real-source" in msg
    assert "harbor-adapter" in msg  # tells the caller what IS implemented


def test_get_planned_source_raises_keyerror():
    """Planned cards exist in the registry but have no fetcher."""
    with pytest.raises(KeyError):
        sources.get("hal-traces")
