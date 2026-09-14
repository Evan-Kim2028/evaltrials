"""The canonical row. Tier 1 is universal; Tier 2 is nullable; Tier 3 is refused.

Tier 3 (the raw trajectory body) is deliberately NOT normalized. Harbor
trajectory.json, Terminal-Bench `steps`, SWE-bench .traj, HAL Weave logs and
OSWorld screenshots do not share a structure. We carry a pointer and derived
features instead. See docs/SCHEMA.md.
"""

TIER1 = [
    "source",          # registry id this row came from
    "unit",            # "trial" | "cell" - an agent MUST branch on this
    "benchmark",
    "task_id",
    "agent",           # normalized via aliases.py
    "model",           # normalized via aliases.py
    "trial_index",     # null when unit == "cell"
    "trial_id",        # null when unit == "cell"
    "reward",
    "outcome",         # 0/1 where the source defines a pass; else null
]

TIER2 = [
    "started_at", "ended_at", "duration_sec",
    "input_tokens", "output_tokens", "cost_usd",
    "n_steps", "n_tool_calls",
    "exception_type", "hit_timeout",
]

# Derived behavioural probes. Only Harbor ships these today; they are the
# reason a normalized corpus beats reading each source at origin.
TIER2_PROBES = ["mentions_answer_file", "git_history_probe", "network_fetch"]

PROVENANCE = [
    "agent_raw", "model_raw",        # what upstream actually wrote
    "trajectory_uri", "archive_sha256",
    "license_spdx", "redistributable", "verified_by",
]

COLUMNS = TIER1 + TIER2 + TIER2_PROBES + PROVENANCE

TYPES = {
    "trial_index": "int64", "input_tokens": "int64", "output_tokens": "int64",
    "n_steps": "int64", "n_tool_calls": "int64",
    "mentions_answer_file": "int64", "git_history_probe": "int64", "network_fetch": "int64",
    "reward": "float64", "outcome": "float64", "duration_sec": "float64", "cost_usd": "float64",
    "hit_timeout": "bool", "redistributable": "bool",
}


def blank_row(**kw):
    row = {c: None for c in COLUMNS}
    row.update(kw)
    unknown = set(kw) - set(COLUMNS)
    if unknown:
        raise ValueError(f"not in canonical schema: {sorted(unknown)}")
    return row
