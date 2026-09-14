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


def test_index_is_sorted_by_run_date_descending():
    """The table rows must come out in strictly non-increasing run-date order."""
    from evaltrials.render import _sort_key

    out = render(ENTRIES)
    table = [l for l in out.splitlines() if l.startswith("| [")]
    assert len(table) == len(ENTRIES)

    ordered = sorted(ENTRIES.values(), key=_sort_key)
    dates = [e.run_date_key for e in ordered]
    assert dates == sorted(dates, reverse=True), dates

    # first row is the most recently run dataset, ties broken by id ascending
    assert ordered[0].title in table[0]
    assert ordered[-1].title in table[-1]


def test_unknown_run_dates_are_labelled():
    out = render(ENTRIES)
    if any(not e.runs.get("last") for e in ENTRIES.values()):
        assert "(u)" in out and "unknown (upstream" in out


def test_measured_dates_render_as_spans():
    out = render(ENTRIES)
    assert "2026-03-25 → 2026-05-26 (m)" in out   # harbor, measured
    assert "2025-10-31 → 2026-03-05 (m)" in out   # terminal-bench, measured


def test_by_the_numbers_section_exists():
    out = render(ENTRIES)
    assert "## By the numbers" in out
    assert "Where it lives" in out and "What it cost to make" in out
    assert "usable for variance work" in out


def test_host_totals_add_up():
    from evaltrials.render import human_bytes
    out = render(ENTRIES)
    total = human_bytes(sum(e.bytes or 0 for e in ENTRIES.values()))
    assert f"**{total}**" in out


def test_headline_is_present_and_computed():
    out = render(ENTRIES)
    head = out.splitlines()[:8]
    joined = "\n".join(head)
    assert "{{HEADLINE}}" not in out, "the headline placeholder must be substituted"
    assert f"{len(ENTRIES)} datasets" in joined
    trials = sum(e.scale.get("trials") or 0 for e in ENTRIES.values())
    assert f"{trials:,}+ recorded agent trials" in joined
    cost = sum(e.cost.get("usd") or 0 for e in ENTRIES.values())
    assert f"${cost:,.0f} of disclosed compute" in joined


def test_trial_total_is_material():
    """The headline claim is the point of the repo; guard it against silent decay."""
    trials = sum(e.scale.get("trials") or 0 for e in ENTRIES.values())
    assert trials > 500_000, trials


def test_dropped_entries_stay_dropped():
    assert "harbor-parity" not in ENTRIES
