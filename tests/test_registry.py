"""The registry is the product. These tests keep it honest."""
import pytest

from evaltrials.card import GATES, KINDS, MULTI, TRAJ, UNITS, load_all

ENTRIES = load_all()


def test_registry_is_not_empty():
    assert len(ENTRIES) >= 20


@pytest.mark.parametrize("entry", ENTRIES.values(), ids=list(ENTRIES))
def test_enums_are_valid(entry):
    assert entry.kind in KINDS
    assert entry.unit in UNITS
    assert entry.gate in GATES
    assert entry.multi_trial in MULTI
    assert entry.trajectories in TRAJ


@pytest.mark.parametrize("entry", ENTRIES.values(), ids=list(ENTRIES))
def test_license_is_declared(entry):
    """Fail closed: an entry must say whether it may be redistributed."""
    assert isinstance(entry.license.get("redistributable"), bool)
    assert entry.license.get("spdx")


@pytest.mark.parametrize("entry", ENTRIES.values(), ids=list(ENTRIES))
def test_upstream_has_a_link(entry):
    assert entry.upstream.get("url") or entry.upstream.get("homepage")


@pytest.mark.parametrize("entry", ENTRIES.values(), ids=list(ENTRIES))
def test_bytes_are_positive_when_present(entry):
    if entry.bytes is not None:
        assert isinstance(entry.bytes, int) and entry.bytes > 0


@pytest.mark.parametrize("entry", ENTRIES.values(), ids=list(ENTRIES))
def test_cost_requires_a_basis(entry):
    """A dollar figure without a stated basis is a rumour, not data."""
    cost = entry.cost
    if cost.get("usd") is not None:
        assert cost["basis"] in ("measured", "reported", "estimated")
        assert cost.get("note"), "a cost needs a note saying where it came from"


@pytest.mark.parametrize("entry", ENTRIES.values(), ids=list(ENTRIES))
def test_cell_unit_is_not_advertised_as_trial_variance(entry):
    """unit=cell means pre-aggregated; it must not claim clean repeated trials."""
    if entry.unit == "cell":
        assert entry.multi_trial != "yes" or entry.notes, (
            "a cell-unit entry claiming multi_trial must explain itself in notes"
        )


def test_ids_are_unique_and_slugs():
    for i in ENTRIES:
        assert i == i.lower()
        assert " " not in i
