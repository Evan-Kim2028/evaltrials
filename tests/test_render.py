from evaltrials.card import load_all
from evaltrials.render import human_bytes, render

ENTRIES = load_all()


def test_render_is_deterministic():
    assert render(ENTRIES) == render(ENTRIES)


def test_every_entry_appears():
    out = render(ENTRIES)
    for entry in ENTRIES.values():
        assert entry.title in out, entry.id
        assert entry.id in out, entry.id


def test_human_bytes():
    assert human_bytes(340000293953) == "316.6 GB"
    assert human_bytes(None) == "—"
    assert human_bytes(0) == "—"
    assert human_bytes(221003563) == "210.8 MB"


def test_not_redistributable_is_flagged():
    out = render(ENTRIES)
    assert "⚠" in out
    # harbor-adapter is license `other` with no text -> must carry the warning
    assert "other ⚠" in out


def test_cost_basis_markers_render():
    out = render(ENTRIES)
    assert "$21,563 (m)" in out   # measured by us from the data
    assert "$40,000 (r)" in out   # reported in the HAL paper


def test_readme_on_disk_is_current():
    import pathlib
    from evaltrials.render import ROOT
    assert (pathlib.Path(ROOT) / "README.md").read_text() == render(ENTRIES)
