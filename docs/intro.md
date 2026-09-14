# evaltrials

**An index of public AI-evaluation run data.**

Re-running agent evals is expensive. Harbor's 54-benchmark sweep burned **226 billion
tokens and over $300,000** of compute. HAL spent about **$40,000** on 21,730 rollouts.
The Terminal-Bench trajectory dump represents at least **$21,563** of compute,
32.8 billion input tokens and 10,251 agent-hours — and that spend is already public,
sitting in a HuggingFace repo, free to download.

A lot of work like that exists. It is scattered across HuggingFace, GitHub
submission trees, ModelScope and leaderboard scrapes, under a dozen different
licenses, and there is no single place that says what is out there or what it holds.
This repo is that list.

**This is an index, not a pipeline.** Nothing here downloads, converts, mirrors or
rehosts anything. Each entry records what a dataset contains, how big it is, how many
rows, whether it has repeated trials, whether trajectories are included, what it costs
to use, and — where the number exists — what it cost to *produce*.

## How to read it

- **Unit** is the most important column. `trial` means one row is one independent run,
  so you can compute pass-rate variance. `cell` means the source already aggregated.
  `score` and `trajectory` are neither. Computing variance from `cell` rows gives you
  a number that does not exist.
- **Multi-trial** is what most people actually come here for. Only a handful of public
  datasets run the same task more than once per model.
- **Trials run** is when the runs actually happened, which is often months before the dataset was uploaded — Harbor's trials ran March–May 2026 but landed on HuggingFace in July. Marked `(m)` measured, `(r)` reported, `(u)` unknown (upstream date shown instead).
- **Cost to produce** is marked `(m)` measured by us from the data itself, `(r)` reported
  by the authors, or `(e)` estimated. Most entries are blank because nobody published it.
- **Announced** links the primary source — the post or page the authors wrote. 21 of 27
  have one; the rest shipped with nothing but a dataset card.
- **License ⚠** means not redistributable — fetch it from upstream yourself, and do not
  mirror the bytes.
