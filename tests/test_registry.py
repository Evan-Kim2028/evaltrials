"""Registry integrity: every card must load clean and stay honest about cost."""
import pathlib

import pytest

from evaltrials import card as cardmod

REGISTRY_DIR = pathlib.Path(__file__).resolve().parents[1] / "registry"


@pytest.fixture(scope="module")
def cards():
    return cardmod.load_all(REGISTRY_DIR)


def test_registry_loads_without_error(cards):
    assert cards, "registry/*.yaml produced zero cards"


def test_no_duplicate_ids(cards):
    # load_all() raises on duplicates; a second manual pass asserts it directly.
    import yaml

    ids = []
    for p in sorted(REGISTRY_DIR.glob("*.yaml")):
        doc = yaml.safe_load(p.read_text())
        for d in (doc if isinstance(doc, list) else [doc]):
            ids.append(d["id"])
    assert len(ids) == len(set(ids)), f"duplicate source ids: {ids}"


def test_unit_gate_status_are_valid(cards):
    for c in cards.values():
        assert c.unit in cardmod.VALID_UNITS, f"{c.id}: bad unit {c.unit!r}"
        assert c.gate in cardmod.VALID_GATES, f"{c.id}: bad gate {c.gate!r}"
        assert c.status in cardmod.VALID_STATUS, f"{c.id}: bad status {c.status!r}"


def test_every_card_declares_redistributable(cards):
    for c in cards.values():
        assert "redistributable" in c.license, f"{c.id}: license.redistributable missing"
        assert isinstance(c.license["redistributable"], bool), (
            f"{c.id}: redistributable must be a bool, got "
            f"{c.license['redistributable']!r}"
        )


def test_asset_bytes_are_positive_ints(cards):
    for c in cards.values():
        for a in c.raw.get("assets") or []:
            if "bytes" not in a:
                continue
            assert isinstance(a["bytes"], int), (
                f"{c.id}: asset {a.get('name')!r} bytes is not an int: {a['bytes']!r}"
            )
            assert a["bytes"] > 0, (
                f"{c.id}: asset {a.get('name')!r} has non-positive bytes {a['bytes']}"
            )


def test_implemented_sources_have_a_fetcher(cards):
    from evaltrials import sources

    for c in cards.values():
        if c.status == "implemented":
            assert sources.get(c.id) is not None
