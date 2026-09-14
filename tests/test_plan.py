"""Preflight planning: cost honesty and gate verdicts, zero I/O."""
import pytest

from evaltrials.card import load_all
from evaltrials.plan import plan_source


@pytest.fixture(scope="module")
def cards():
    return load_all()


def test_harbor_default_is_manifest_not_trajectories(cards):
    """The default plan must never silently pick the 340 GB asset."""
    p = plan_source(cards["harbor-adapter"])
    assert p["assets"] == ["manifest"]
    assert p["download_bytes"] == 15_952_527

    skipped = {a["name"]: a for a in p["skipped_assets"]}
    assert "trajectories" in skipped
    assert skipped["trajectories"]["bytes"] == 340_000_293_953


def test_cheapest_asset_wins_without_explicit_default():
    """A card with no `default: true` asset picks the smallest sized asset."""
    from evaltrials.card import Card

    raw = {
        "id": "synthetic", "title": "t", "status": "implemented", "unit": "trial",
        "upstream": {}, "license": {"redistributable": True}, "gate": "open",
        "assets": [
            {"name": "huge", "bytes": 10**12},
            {"name": "tiny", "bytes": 10**4},
            {"name": "mid", "bytes": 10**8},
        ],
    }
    card = Card(id="synthetic", title="t", status="implemented", unit="trial",
                upstream={}, license={"redistributable": True}, gate="open", raw=raw)
    p = plan_source(card)
    assert p["assets"] == ["tiny"]
    assert {a["name"] for a in p["skipped_assets"]} == {"huge", "mid"}


def test_planned_source_is_blocked(cards):
    planned = [c for c in cards.values() if c.status == "planned"]
    assert planned, "registry has no planned source to test"
    for c in planned:
        p = plan_source(c)
        assert p["verdict"] == "blocked", f"{c.id}: expected blocked, got {p['verdict']}"
        assert p["blockers"], f"{c.id}: blocked but blockers list is empty"


def test_hf_gated_source_mentions_token(cards):
    gated = [c for c in cards.values() if c.gate == "hf-gated"]
    assert gated, "registry has no hf-gated source to test"
    for c in gated:
        p = plan_source(c)
        assert any("token" in b.lower() for b in p["blockers"]), (
            f"{c.id}: hf-gated blockers never mention a token: {p['blockers']}"
        )


def test_implemented_open_source_is_ok(cards):
    p = plan_source(cards["harbor-adapter"])
    assert p["verdict"] == "ok"
    assert p["blockers"] == []


def test_unknown_asset_raises_keyerror(cards):
    with pytest.raises(KeyError, match="no asset named"):
        plan_source(cards["harbor-adapter"], asset="does-not-exist")


def test_non_redistributable_carries_an_obligation(cards):
    p = plan_source(cards["harbor-adapter"])
    assert any("NOT redistributable" in o for o in p["obligations"])
