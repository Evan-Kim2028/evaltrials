# Canonical schema

`evaltrials.schema.COLUMNS` is the single row shape every source normalizes into.
Column order is stable; `blank_row()` returns every column and rejects unknown keys.

The schema has three tiers. Tier is about *how much we promise*, not importance.

## Tier 1 — universal, always present

These exist on every row from every source. `reward`/`outcome` may be `null` when
the source genuinely does not publish a score, but the column is never absent.

| column | type | meaning |
|---|---|---|
| `source` | string | registry id this row came from (e.g. `harbor-adapter`) |
| `unit` | string | `trial` or `cell` — **branch on this before any statistics** |
| `benchmark` | string | benchmark name within the source (e.g. `terminal-bench`) |
| `task_id` | string | upstream task identifier |
| `agent` | string | scaffold/agent, normalized via `aliases.normalize_agent` |
| `model` | string | model id, normalized via `aliases.normalize_model` |
| `trial_index` | int64 | repeat index within a cell; `null` when `unit='cell'` |
| `trial_id` | string | upstream trial/run id; `null` when `unit='cell'` |
| `reward` | float64 | raw score on the source's own scale; `null` if not published |
| `outcome` | float64 | 0.0/1.0 where the source defines a pass; else `null` |

## Tier 2 — nullable, per-source coverage

Measured facts about the run. Coverage varies per source and is declared on each
registry card under `fields:` — check `evaltrials describe <source>` before
relying on any of these. `null` means "not published", never "zero".

| column | type | meaning |
|---|---|---|
| `started_at` | string | first step timestamp (ISO, as upstream wrote it) |
| `ended_at` | string | last step timestamp |
| `duration_sec` | float64 | agent wall-clock seconds |
| `input_tokens` | int64 | prompt tokens, where published |
| `output_tokens` | int64 | completion tokens, where published |
| `cost_usd` | float64 | run cost in USD |
| `n_steps` | int64 | derived step count (see Tier 3) |
| `n_tool_calls` | int64 | derived tool-call count (see Tier 3) |
| `exception_type` | string | exception class if the run died; `null` on clean exits |
| `hit_timeout` | bool | run ended on the harness timeout |

### Tier 2 probes — derived behavioural features

Only Harbor ships these today; they are the reason a normalized corpus beats
reading each source at origin.

| column | type | meaning |
|---|---|---|
| `mentions_answer_file` | int64 | reward-hack probe: agent touched/read the answer file |
| `git_history_probe` | int64 | reward-hack probe: agent dug through git history for answers |
| `network_fetch` | int64 | contamination probe: agent fetched from the network |

### Provenance

| column | type | meaning |
|---|---|---|
| `agent_raw` | string | agent string exactly as upstream wrote it |
| `model_raw` | string | model string exactly as upstream wrote it |
| `trajectory_uri` | string | pointer to the Tier 3 body (e.g. `hf://datasets/<repo>/<shard>`) |
| `archive_sha256` | string | sha256 of the archive the row was extracted from |
| `license_spdx` | string | SPDX id from the registry card |
| `redistributable` | bool | may evaltrials (or you) mirror the bytes |
| `verified_by` | string | provenance class: `official-harness`, `leaderboard-scrape`, … |

## Tier 3 — the raw trajectory body, deliberately NOT normalized

Harbor `trajectory.json`, Terminal-Bench `steps`, SWE-bench `.traj`, HAL Weave
logs, and OSWorld screenshots do not share a structure. There is no honest common
row shape, and inventing one would either drop information or lie about coverage.
So evaltrials refuses: the body stays upstream, and the row carries a
`trajectory_uri` pointer plus *derived features* (`n_steps`, `n_tool_calls`, the
probes) extracted at fetch time.

If you need the body, follow `trajectory_uri` yourself — per-shard, never whole.

## `unit`: trial vs cell

`unit='trial'`: one row = one independent run of `(task, agent, model)`. This is
the only unit from which per-run variance, pass@k, or confidence intervals can
be computed.

`unit='cell'`: one row = one `(task, agent, model)` aggregate. Trial-level
repeats were averaged away upstream — `trial_index`/`trial_id` are `null`
because the trials are not in the data.

**Warning: computing trial variance from `unit='cell'` rows is wrong.** A cell's
spread across tasks is task-difficulty variance, not run-to-run variance; the
lhtb-leaderboard card says this outright (`do not compute trial variance from
this`). Filter or group on `unit` before any variance, stddev, or pass@k math.
