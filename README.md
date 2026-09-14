# evaltrials

**An agent-first catalog and fetcher for public AI-evaluation trial data.**

Re-running agent evals is expensive — HAL spent ~$40k on 21,730 rollouts. A lot of
that work is already public, but it is scattered across HuggingFace repos, GitHub
submission trees and leaderboard scrapes, each with a different shape, a different
license, and a different idea of what a "row" is.

`evaltrials` does not rehost any of it. It ships a **registry** describing each
source, **fetchers** that pull from upstream and verify, and a **normalizer** that
maps everything onto one row so you can join across sources.

Built for agents to drive. Every verb emits JSON when stdout is not a TTY, and
every call tells you what it will cost *before* it spends it.

## The six verbs

```sh
evaltrials catalog                        # every known source, one compact line each
evaltrials describe harbor-adapter        # full schema card: fields, coverage, caveats
evaltrials plan harbor-adapter            # bytes, seconds, license, blockers. zero I/O
evaltrials fetch  harbor-adapter          # download + normalize into ~/.cache/evaltrials
evaltrials sample harbor-adapter -n 5     # n rows + MEASURED per-field coverage
evaltrials query  "SELECT ... FROM trials"  # DuckDB over the cache
```

### `plan` is the point

An agent that naively clones `IntelligenceLab/LHTB-leaderboard` pulls **48.1 GB**
across 66,805 files; a single asciinema recording in there is 9.8 GB. Harbor-Adapter's
`trajectories` config is **316.6 GB**. `plan` refuses to make that the default and
says so out loud:

```json
{
  "source": "harbor-adapter",
  "verdict": "ok",
  "assets": ["manifest"],
  "download_human": "15.2 MB",
  "download_sec_est": 0.4,
  "obligations": [
    "attribute: Harbor-Adapter (kendx), arXiv:2609.04298",
    "NOT redistributable: fetch from upstream, never mirror the bytes"
  ],
  "skipped_assets": [
    {"name": "trajectories", "human": "316.6 GB",
     "note": "PER-SHARD fetch only. never pull the whole config."}
  ]
}
```

### `unit` is required, and agents must branch on it

`unit: trial` means one row is one independent run — you can compute pass-rate
variance. `unit: cell` means the source already aggregated; LHTB's `per_task`
config has no `trial_id` at all. An agent that treats cells as trials reports a
variance that does not exist, so the registry declares the unit and the CLI
repeats it on every response.

### Coverage is measured, not promised

`sample` reports the real non-null fraction per column, so nobody burns three turns
discovering a column exists but is empty:

```
input_tokens   0.661
n_steps        0.661     # derived from `steps`; only 34,462 of 52,104 rows carry it
exception_type 0.000     # present in the schema, absent in this source
```

## Sources

| id | unit | rows | license | redistributable | status |
|---|---|---|---|---|---|
| `harbor-adapter` | trial | 178,647 cells / 60 benchmarks / 6 agents / 16 models | `other` | no | implemented |
| `terminalbench-yoonholee` | trial | 52,104 / 89 tasks / 26 scaffolds / 49 models | `apache-2.0` | yes | implemented |
| `lhtb-leaderboard` | cell | 1,196 / 46 tasks / 26 models | `apache-2.0` | yes | implemented |
| `harbor-parity` | trial | adapter oracle/parity runs | `unset` | no | planned |
| `toolathlon-trajectories` | trial | 17 models × 3 runs × 108 tasks | `cc-by-4.0` | yes (gated) | planned |
| `malt-transcripts` | trial | 7,179 runs / 169 tasks | `mit` | no (gated) | planned |
| `hal-traces` | trial | 21,730 rollouts / 9 benchmarks | `unset` | no (encrypted) | planned |
| `epoch-benchmarks` | cell | 8–16 repeats per cell | `cc-by-4.0` | yes | planned |
| `swebench-experiments` | cell | official submissions | `mit` | yes | planned |

Licensing is handled by fetching, never mirroring. HAL encrypts its traces on
purpose to block scraping; `evaltrials` will decrypt only on your machine, opt-in,
and will never ship decrypted bytes. METR MALT is MIT but gated, so its fetcher
requires your own HF token. Every normalized row carries `license_spdx`,
`redistributable` and `verified_by` so downstream filters are possible.

`verified_by` matters: `official-harness` (the benchmark's own runner produced it)
is a stronger claim than `leaderboard-scrape` (self-reported). Terminal-Bench found
cheating on its 2.0 leaderboard in April 2026 and now mandates trajectories.

## The join that motivates the whole thing

Harbor's `terminal-bench` adapter and the Terminal-Bench scrape use an **identical
task-name namespace** — both write `adaptive-rejection-sampler`. That gives the same
89 tasks measured by 6 Harbor agents and 26 leaderboard scaffolds, which is what you
need to separate *this task is broken* from *this scaffold is weak*.

```sh
evaltrials query "
  SELECT task_id,
         count(*) FILTER (WHERE source='harbor-adapter')           AS harbor_trials,
         count(*) FILTER (WHERE source='terminalbench-yoonholee')  AS tb_trials,
         count(DISTINCT agent)                                     AS scaffolds,
         avg(outcome)                                              AS pass_rate
  FROM trials
  WHERE benchmark = 'terminal-bench' AND unit = 'trial'
  GROUP BY task_id ORDER BY pass_rate"
```

## What is deliberately not normalized

The trajectory body. Harbor `trajectory.json`, Terminal-Bench `steps`, SWE-bench
`.traj`, HAL Weave logs and OSWorld screenshots share no structure. A lossy parser
sends people back to origin; a faithful one is six parsers to maintain forever.
`evaltrials` keeps a `trajectory_uri` pointer plus **derived features**
(`n_steps`, `n_tool_calls`, and Harbor's `mentions_answer_file`,
`git_history_probe`, `network_fetch` reward-hack/contamination probes). See
[`docs/SCHEMA.md`](docs/SCHEMA.md).

Dropping the body is also why this is cheap: 211 MB of upstream Terminal-Bench
parquet normalizes to a **2.6 MB** trial table.

## Honest limits

The union is **not a balanced factorial**. Most `(task, model)` cells exist in one
source only. Always group by `source`, or include it as a fixed effect. Harbor's
`trial_ids` is capped at the 5 most recent, so trials-per-cell is censored rather
than sampled. Reward scales differ per benchmark — do not average `reward` across
benchmarks; use `outcome`.

## Install

```sh
uv venv .venv --python python3
uv pip install --python .venv/bin/python -e '.[hf,dev]'
.venv/bin/python -m pytest tests -q
```

Not published to PyPI. Clone it and install editable.

## License

MIT for the code and registry metadata. Each upstream dataset keeps its own
license, recorded per source in `registry/*.yaml` and echoed on every row.
