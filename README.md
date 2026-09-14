# evaltrials

**An index of public AI-evaluation run data.**

Re-running agent evals is expensive. HAL spent about **$40,000** on 21,730 rollouts.
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
- **License ⚠** means not redistributable — fetch it from upstream yourself, and do not
  mirror the bytes.

## Index

| Dataset | Trials run | Kind | Unit | Multi-trial | Trajectories | Rows | Size | Cost to produce | License | Gate |
| --- | --- | --- | --- | --- | --- | ---: | ---: | ---: | --- | --- |
| [Every Eval Ever (EvalEval datastore)](https://huggingface.co/datasets/evaleval/EEE_datastore) | 2026-09 (r) | meta-index | collection | no | none | 107 | 3.1 GB | — | mit | open |
| [Epoch AI Benchmarking Hub](https://epoch.ai/benchmarks) | 2023 → 2026-09 (r) | llm-scores | cell | yes | none | 1,103 | — | — | cc-by-4.0 | open |
| [OpenEval (Open-Eval-Commons)](https://huggingface.co/datasets/Open-Eval-Commons/OpenEval) | 2026-09 (r) | meta-index | score | no | none | — | 8.6 GB | — | cc-by-nc-4.0 | open |
| [SWE-bench official submissions](https://github.com/SWE-bench/experiments) | 2023-10 → 2026-09 (r) | llm-scores | cell | no | partial | — | — | — | mit | open |
| [OSWorld-Verified Ubuntu trajectories](https://modelscope.cn/datasets/xlangai/ubuntu_osworld_verified_trajs) | 2026-08 (r) | agent-trials | trial | yes | full | — | 447.0 GB | — | mit | account |
| [tau-bench / tau2-bench simulations](https://github.com/sierra-research/tau2-bench) | unknown (upstream 2026-07) (u) | agent-trials | trial | yes | full | — | — | — | mit | open |
| [Long-Horizon Terminal-Bench leaderboard](https://huggingface.co/datasets/IntelligenceLab/LHTB-leaderboard) | 2026-07 (r) | agent-trials | cell | partial | full | 1,196 | 48.1 GB | — | apache-2.0 | open |
| [AndroidWorld evaluation traces (SeerRay)](https://huggingface.co/datasets/SeerRay-Lab/Android-World-Eval) | 2026-06 (r) | agent-trials | trial | yes | full | 464 | 2.5 GB | — | mit | open |
| [NVIDIA Open-SWE-Traces](https://huggingface.co/datasets/nvidia/Open-SWE-Traces) | 2026-06 (r) | sft-traces | trajectory | no | full | 200,000 | 39.7 GB | — | cc-by-4.0 | open |
| [Harbor-Adapter](https://huggingface.co/datasets/kendx/Harbor-Adapter) | 2026-03-25 → 2026-05-26 (m) | agent-trials | trial | yes | full | 178,647 | 316.6 GB | — | other ⚠ | open |
| [Agent Launch Pad trajectories](https://huggingface.co/datasets/AlexWortega/agent-launch-pad-trajectories) | 2026-05 (r) | agent-trials | trial | no | full | 1,380 | 136.3 MB | — | apache-2.0 | open |
| [Harbor adapter parity experiments](https://huggingface.co/datasets/harborframework/parity-experiments) | 2026-04 (r) | agent-trials | trial | yes | full | — | — | — | unset ⚠ | unknown |
| [Terminal-Bench leaderboard trajectories](https://huggingface.co/datasets/yoonholee/terminalbench-trajectories) | 2025-10-31 → 2026-03-05 (m) | agent-trials | trial | yes | full | 52,104 | 210.8 MB | $21,563 (m) | apache-2.0 | open |
| [ASSERT-KTH agentic eval artifacts](https://huggingface.co/datasets/ASSERT-KTH/agentic-evals-artifacts) | 2026-03 (r) | agent-trials | trial | yes | full | — | 44.7 GB | — | cc-by-4.0 | open |
| [ITBench SRE trajectories](https://huggingface.co/datasets/ibm-research/ITBench-Trajectories) | 2026-01 (r) | agent-trials | trial | unknown | full | 105 | 22.1 MB | — | cc-by-nc-4.0 | open |
| [METR eval-analysis-public (time-horizon runs)](https://github.com/METR/eval-analysis-public) | 2026-01 (r) | agent-trials | trial | yes | none | — | 21.4 MB | — | mit | open |
| [HAL (Holistic Agent Leaderboard) traces](https://huggingface.co/datasets/agent-evals/hal_traces) | 2025-10 (r) | agent-trials | trial | yes | encrypted | 21,730 | 105.3 GB | $40,000 (r) | unset ⚠ | encrypted |
| [METR MALT public transcripts](https://huggingface.co/datasets/metr-evals/malt-transcripts-public) | 2025-10 (r) | agent-trials | trial | yes | full | 7,179 | 7.9 GB | — | mit ⚠ | hf-gated |
| [Toolathlon trajectories](https://huggingface.co/datasets/hkust-nlp/Toolathlon-Trajectories) | 2025-10 (r) | agent-trials | trial | yes | full | 5,000 | 1.9 GB | — | cc-by-4.0 | hf-gated |
| [TheAgentCompany experiments](https://github.com/TheAgentCompany/experiments) | 2025-06 (r) | agent-trials | cell | no | full | — | — | — | mit | open |
| [TRAIL failure-attribution traces](https://huggingface.co/datasets/PatronusAI/TRAIL) | 2025-05 (r) | labeled-traces | trajectory | no | full | 148 | 229.9 MB | — | mit | hf-gated |
| [AgentRewardBench](https://huggingface.co/datasets/McGill-NLP/agent-reward-bench) | 2025-04 (r) | labeled-traces | trajectory | no | full | 1,302 | 35.7 GB | — | unset ⚠ | open |
| [PaperBench runs](https://github.com/openai/frontier-evals/tree/main/project/paperbench) | 2025-04 (r) | agent-trials | trial | yes | full | — | — | — | mit | open |
| [SWE-smith trajectories](https://huggingface.co/datasets/SWE-bench/SWE-smith-trajectories) | 2025-04 (r) | sft-traces | trajectory | partial | full | 76,002 | 3.9 GB | — | mit | open |
| [MLE-bench run groups](https://github.com/openai/mle-bench) | 2024-10 (r) | agent-trials | cell | yes | partial | — | — | — | mit | open |
| [SWE-bench Verified human annotations](https://openai.com/index/introducing-swe-bench-verified/) | 2024-08 (r) | labeled-traces | score | no | none | 1,699 | 7.6 MB | — | apache-2.0 | open |
| [LMSYS-Chat-1M](https://huggingface.co/datasets/lmsys/lmsys-chat-1m) | 2023-04 → 2023-08 (r) | llm-scores | score | no | none | 1,000,000 | 1.4 GB | — | other | hf-gated |

Sorted by when the trials were run, most recent first. `(m)` measured from the data itself · `(r)` reported by the authors · `(e)` estimated · `(u)` no run dates published, so the upstream update date is shown and used for sorting. `⚠` marks a dataset that may not be redistributed.

## Detail

## Agent evaluation runs

### OSWorld-Verified Ubuntu trajectories

`osworld-verified-trajs` · [dataset](https://modelscope.cn/datasets/xlangai/ubuntu_osworld_verified_trajs) · [home](https://github.com/xlang-ai/OSWorld)

- **trials run** 2026-08 (r) — dataset updated 2026-08; run dates not published. 480 GB is the card's decimal figure.
- **unit** `trial` · **multi-trial** `yes` · **trajectories** `full` · **gate** `account`
- **scale** tasks 369 · models 15 · trials_per_cell multiple, at 15/50/100 step budgets
- **size** 447.0 GB
- **cost note** not published
- **license** `mit`
- **upstream updated** 2026-08-01
- Largest entry in the index by bytes: 480 GB of GUI screenshots and actions.
- MIT, but the card asks that it not be used as computer-use training data.
- Screenshots capture third-party desktop and web UIs; that, not the licence header, is the real redistribution question.
- Hosted on ModelScope, not HuggingFace.

### tau-bench / tau2-bench simulations

`tau-bench-trials` · [dataset](https://github.com/sierra-research/tau2-bench) · repo: `sierra-research/tau2-bench` · [paper](https://arxiv.org/abs/2506.07982)

- **unit** `trial` · **multi-trial** `yes` · **trajectories** `full` · **gate** `open`
- **scale** tasks 300 · trials_per_cell 4-8 (pass^k is the point of the benchmark)
- **cost note** not published
- **license** `mit`
- **upstream updated** 2026-07-15
- One of the few benchmarks where repeated trials are the headline metric rather than an afterthought.
- Retail, airline and telecom domains. Leaderboard asks for 4 trials x 3 domains.
- The repo CHANGELOG documents 75+ task fixes, which doubles as a list of known-invalid tasks.

### Long-Horizon Terminal-Bench leaderboard

`lhtb-leaderboard` · [dataset](https://huggingface.co/datasets/IntelligenceLab/LHTB-leaderboard) · repo: `IntelligenceLab/LHTB-leaderboard` · [paper](https://arxiv.org/abs/2607.08964)

- **trials run** 2026-07 (r) — paper arXiv:2607.08964; per-submission dates are inside submissions/.
- **unit** `cell` · **multi-trial** `partial` · **trajectories** `full` · **gate** `open`
- **scale** rows 1,196 · benchmarks 1 · tasks 46 · models 26
- **size** 48.1 GB
- **cost note** not published. long-horizon tasks with per-model agent_budget_sec, so per-trial spend is high.
- **license** `apache-2.0`
- **upstream updated** 2026-08-20
- The `per_task` config has NO trial_id: it is already aggregated. Do not compute trial variance from it.
- 48.1 GB across 66,805 files. A single asciinema recording reaches 9.8 GB. Never clone the whole repo.
- Raw per-trial trajectory.json + recording.cast + reward.txt live under submissions/.

### AndroidWorld evaluation traces (SeerRay)

`androidworld-seerray` · [dataset](https://huggingface.co/datasets/SeerRay-Lab/Android-World-Eval) · repo: `SeerRay-Lab/Android-World-Eval`

- **trials run** 2026-06 (r) — upstream last modified 2026-06-30; run dates not published.
- **unit** `trial` · **multi-trial** `yes` · **trajectories** `full` · **gate** `open`
- **scale** rows 464 · tasks 116 · models 1 · trials_per_cell 4
- **size** 2.5 GB
- **cost note** not published
- **license** `mit`
- **upstream updated** 2026-06-30
- Small but clean: 4 rollouts on each of 116 tasks. Mobile GUI axis.
- Single method (Xiaomi-GUI-0), so there is no model axis.

### Harbor-Adapter

`harbor-adapter` · [dataset](https://huggingface.co/datasets/kendx/Harbor-Adapter) · repo: `kendx/Harbor-Adapter` · [paper](https://arxiv.org/abs/2609.04298) · [home](https://harbor-index.org/)

- **trials run** 2026-03-25 → 2026-05-26 (m) — measured from first_step_at across 783,135 extracted trials; 94% ran in April 2026. Dataset was not uploaded until 2026-07-11.
- **unit** `trial` · **multi-trial** `yes` · **trajectories** `full` · **gate** `open`
- **scale** rows 178,647 · trials 793,698 · benchmarks 60 · tasks 7,819 · agents 6 · models 16 · trials_per_cell 1-5 (capped at the 5 most recent)
- **size** 316.6 GB
- **cost note** not published. 794k frontier-agent trials; the compute behind this is the largest single spend in the index.
- **license** `other` — **not redistributable**
- **upstream updated** 2026-07-11
- The broadest public multi-benchmark agent run dump: 60 benchmarks in one schema.
- Dataset card says license `other` and ships no license text. Fetch from upstream; do not mirror.
- trials_per_cell is censored at 5, not sampled - do not treat it as a designed k.
- Reward scale differs per benchmark. Never average reward across benchmarks.
- The 16 MB manifest parquet is cell-level and carries no reward column; rewards live inside the 316 GB of per-trial archives.

### Agent Launch Pad trajectories

`agent-launch-pad` · [dataset](https://huggingface.co/datasets/AlexWortega/agent-launch-pad-trajectories) · repo: `AlexWortega/agent-launch-pad-trajectories`

- **trials run** 2026-05 (r) — upstream last modified 2026-05-12.
- **unit** `trial` · **multi-trial** `no` · **trajectories** `full` · **gate** `open`
- **scale** rows 1,380 · models 7 · agents 2
- **size** 136.3 MB
- **cost note** not published
- **license** `apache-2.0`
- **upstream updated** 2026-05-12
- Terminal-Bench 2 (1,204) + ScienceAgentBench (176). One trajectory per cell, so no variance.

### Harbor adapter parity experiments

`harbor-parity` · [dataset](https://huggingface.co/datasets/harborframework/parity-experiments) · repo: `harborframework/parity-experiments`

- **trials run** 2026-04 (r) — upstream last modified 2026-04-22.
- **unit** `trial` · **multi-trial** `yes` · **trajectories** `full` · **gate** `unknown`
- **scale** trials_per_cell often 3
- **cost note** not published
- **license** `unset` — **not redistributable**
- **upstream updated** 2026-04-22
- Oracle and parity runs per Harbor adapter - evidence about whether an adapter preserves the original benchmark.
- The HF API returns zero file entries for this repo; gate is genuinely unverified.

### Terminal-Bench leaderboard trajectories

`terminalbench-trajectories` · [dataset](https://huggingface.co/datasets/yoonholee/terminalbench-trajectories) · repo: `yoonholee/terminalbench-trajectories` · [home](https://www.tbench.ai/)

- **trials run** 2025-10-31 → 2026-03-05 (m) — measured from started_at. PARTIAL: only 22,598 of 52,104 rows carry a usable timestamp; 29,506 have an empty string.
- **unit** `trial` · **multi-trial** `yes` · **trajectories** `full` · **gate** `open`
- **scale** rows 52,104 · benchmarks 1 · tasks 89 · agents 26 · models 49 · trials_per_cell ~5 (TB requires 5 independent runs per submission)
- **size** 210.8 MB
- **cost to produce** $21,563 (measured) · input tokens 32,753,686,924 · output tokens 632,468,325 · agent-hours 10,251
- **cost note** summed from the dataset's own cost_cents column, 2026-09-14. LOWER BOUND: 39.2% of trials report zero cost, and 237 rows carry a NEGATIVE cost (min -$15.99).
- **license** `apache-2.0`
- **upstream updated** 2026-03-09
- Best cost data in the index: per-trial USD, tokens and wall-clock on every row.
- 26 scaffolds on the same 89 tasks - the widest scaffold axis available anywhere.
- Shares an identical task-name namespace with Harbor's terminal-bench adapter (89 tasks in both), so the two can be compared task-for-task.
- Scraped from a public leaderboard, not re-run. Self-reported. TB found cheating on the 2.0 board in April 2026 and now mandates trajectories.
- `steps` (the trajectory body) is present on 34,462 of 52,104 rows; token counts on the same 66.1%.

### ASSERT-KTH agentic eval artifacts

`assert-kth-agentic-evals` · [dataset](https://huggingface.co/datasets/ASSERT-KTH/agentic-evals-artifacts) · repo: `ASSERT-KTH/agentic-evals-artifacts`

- **trials run** 2026-03 (r) — upstream last modified 2026-03-20.
- **unit** `trial` · **multi-trial** `yes` · **trajectories** `full` · **gate** `open`
- **scale** tasks 500 · trials_per_cell 10 per setting
- **size** 44.7 GB
- **cost note** not published
- **license** `cc-by-4.0`
- **upstream updated** 2026-03-20
- SWE-bench Verified at 10 runs per setting - unusually deep k for SWE-bench.

### ITBench SRE trajectories

`itbench-trajectories` · [dataset](https://huggingface.co/datasets/ibm-research/ITBench-Trajectories) · repo: `ibm-research/ITBench-Trajectories`

- **trials run** 2026-01 (r) — upstream last modified 2026-01-19.
- **unit** `trial` · **multi-trial** `unknown` · **trajectories** `full` · **gate** `open`
- **scale** rows 105
- **size** 22.1 MB
- **cost note** not published
- **license** `cc-by-nc-4.0`
- **upstream updated** 2026-01-19
- Site-reliability-engineering task domain, rare in this index.
- Non-commercial licence.

### METR eval-analysis-public (time-horizon runs)

`metr-eval-analysis` · [dataset](https://github.com/METR/eval-analysis-public) · repo: `METR/eval-analysis-public` · [paper](https://arxiv.org/abs/2503.17354)

- **trials run** 2026-01 (r) — Time Horizon 1.1 published 2026-01-29.
- **unit** `trial` · **multi-trial** `yes` · **trajectories** `none` · **gate** `open`
- **scale** tasks 228 · trials_per_cell ~8 per (model, task)
- **size** 21.4 MB
- **cost note** not published
- **license** `mit`
- **upstream updated** 2026-01-29
- runs.jsonl is only 22.4 MB and carries task_id, model alias, score_binarized, score_cont and human_minutes.
- human_minutes is the rarest field in the index: a human-time calibration per task.
- Scores only, no trajectories. Transcripts live separately at transcripts.metr.org.

### HAL (Holistic Agent Leaderboard) traces

`hal-traces` · [dataset](https://huggingface.co/datasets/agent-evals/hal_traces) · repo: `agent-evals/hal_traces` · [paper](https://arxiv.org/abs/2510.11977) · [home](https://hal.cs.princeton.edu/)

- **trials run** 2025-10 (r) — run dates are not in the public metadata; the flagship 21,730-rollout study was published 2025-10.
- **unit** `trial` · **multi-trial** `yes` · **trajectories** `encrypted` · **gate** `encrypted`
- **scale** rows 21,730 · benchmarks 9 · models 9 · trials_per_cell varies by benchmark protocol
- **size** 105.3 GB
- **cost to produce** $40,000 (reported)
- **cost note** the HAL paper reports ~$40k and 2.5B tokens for the flagship 21,730-rollout study.
- **license** `unset` — **not redistributable**
- **upstream updated** 2026-02-01
- The clearest published cost-per-rollout in the field: ~$1.84 per rollout.
- Traces are encrypted ON PURPOSE to stop scraping and benchmark contamination. Decrypt locally via hal-decrypt; do not redistribute decrypted bytes.
- Covers AssistantBench, GAIA, Online Mind2Web, CORE-Bench, SciCode, ScienceAgentBench, SWE-bench Verified Mini, TAU-bench Airline, USACO.

### METR MALT public transcripts

`malt-transcripts` · [dataset](https://huggingface.co/datasets/metr-evals/malt-transcripts-public) · repo: `metr-evals/malt-transcripts-public` · [home](https://metr.org/blog/2025-10-14-malt-dataset-of-natural-and-prompted-behaviors)

- **trials run** 2025-10 (r) — MALT released 2025-10-14; per-run dates not published.
- **unit** `trial` · **multi-trial** `yes` · **trajectories** `full` · **gate** `hf-gated`
- **scale** rows 7,179 · tasks 169 · models 19 · trials_per_cell >=5 under the HCAST protocol
- **size** 7.9 GB
- **cost note** not published
- **license** `mit` — **not redistributable**
- **upstream updated** 2026-03-24
- Public split is 7,179 of 10,919 runs; the rest is request-only.
- MIT licensed but HF-gated, and METR withheld internal-task transcripts to limit contamination. Fetch with your own token; do not mirror.
- Paired with METR/eval-analysis-public runs.jsonl, which carries per-run score_binarized and human_minutes.

### Toolathlon trajectories

`toolathlon-trajectories` · [dataset](https://huggingface.co/datasets/hkust-nlp/Toolathlon-Trajectories) · repo: `hkust-nlp/Toolathlon-Trajectories` · [paper](https://arxiv.org/abs/2510.25726)

- **trials run** 2025-10 (r) — paper arXiv:2510.25726; not recorded per trial in the public dump.
- **unit** `trial` · **multi-trial** `yes` · **trajectories** `full` · **gate** `hf-gated`
- **scale** rows 5,000 · tasks 108 · models 17 · trials_per_cell 3
- **size** 1.9 GB
- **cost note** not published
- **license** `cc-by-4.0`
- **upstream updated** 2025-12-05
- Clean 17 models x 3 runs x 108 tasks design - one of the few balanced factorials in the index.
- Tool-use axis; JSONL messages + tool_calls + an eval boolean.
- Gated: requires accepting terms with an HF token.

### TheAgentCompany experiments

`theagentcompany-experiments` · [dataset](https://github.com/TheAgentCompany/experiments) · repo: `TheAgentCompany/experiments`

- **trials run** 2025-06 (r) — upstream last updated 2025-06.
- **unit** `cell` · **multi-trial** `no` · **trajectories** `full` · **gate** `open`
- **scale** tasks 175 · trials_per_cell 1
- **cost note** not published
- **license** `mit`
- **upstream updated** 2025-06-01
- Trajectories and screenshots per model, but the leaderboard is one attempt per task. No variance.

### PaperBench runs

`paperbench-runs` · [dataset](https://github.com/openai/frontier-evals/tree/main/project/paperbench) · repo: `openai/frontier-evals`

- **trials run** 2025-04 (r) — paper published 2025-04.
- **unit** `trial` · **multi-trial** `yes` · **trajectories** `full` · **gate** `open`
- **scale** tasks 20 · trials_per_cell 3
- **cost note** not published; long-horizon paper-reproduction runs are expensive per trial
- **license** `mit`
- **upstream updated** 2025-04-01
- Leaderboard reports 3 runs with SEM, so error bars are available.

### MLE-bench run groups

`mle-bench-runs` · [dataset](https://github.com/openai/mle-bench) · repo: `openai/mle-bench` · [paper](https://arxiv.org/abs/2410.07095)

- **trials run** 2024-10 (r) — paper arXiv:2410.07095.
- **unit** `cell` · **multi-trial** `yes` · **trajectories** `partial` · **gate** `open`
- **scale** tasks 75 · trials_per_cell multiple seeds; the paper reports pass@8
- **cost note** not published
- **license** `mit`
- **upstream updated** 2024-10-01
- 75 Kaggle competitions x AIDE / MLAB / OpenDevin scaffolds.
- Grading reports per run group; step traces are not packaged per trial.

## Score tables

### Epoch AI Benchmarking Hub

`epoch-benchmarking-hub` · [dataset](https://epoch.ai/benchmarks) · [home](https://epoch.ai/benchmarks/use-this-data)

- **trials run** 2023 → 2026-09 (r) — the hub is continuously updated; CSV regenerated 2026-09-14.
- **unit** `cell` · **multi-trial** `yes` · **trajectories** `none` · **gate** `open`
- **scale** rows 1,103 · benchmarks 37 · models 126 · trials_per_cell 16 on GPQA Diamond and Mock AIME, 8 on MATH L5
- **cost note** not published as a total, though Epoch reports per-benchmark inference costs in places
- **license** `cc-by-4.0`
- **upstream updated** 2026-09-14
- The deepest repeat count of any open source: 16 runs per cell. Best available reference for what eval variance actually looks like.
- Epoch's own run tables are CC-BY and redistributable with credit. The underlying benchmark questions are not Epoch's to relicense.
- Per-question Inspect logs exist behind a CAPTCHA-gated viewer, not as a bulk download.
- LLM benchmarks, not agent trajectories. SWE-bench Verified here is score-level.

### SWE-bench official submissions

`swebench-experiments` · [dataset](https://github.com/SWE-bench/experiments) · repo: `SWE-bench/experiments`

- **trials run** 2023-10 → 2026-09 (r) — submissions accumulate continuously; each folder carries its own metadata.yaml date.
- **unit** `cell` · **multi-trial** `no` · **trajectories** `partial` · **gate** `open`
- **scale** tasks 2,294 · trials_per_cell 1 (pass@1 required; pass@k disallowed for the headline number)
- **cost note** not published
- **license** `mit`
- **upstream updated** 2026-09-01
- LOOKS like a multi-trial corpus and is not. Different submissions are different systems, not i.i.d. repeats. Never read it as trial variance.
- The field's longest-running per-run archive: every official submission has carried trajectories since 2024.
- Per submission: all_preds.jsonl, metadata.yaml, evaluation logs, trajs/*.traj.

### LMSYS-Chat-1M

`lmsys-chat-1m` · [dataset](https://huggingface.co/datasets/lmsys/lmsys-chat-1m) · repo: `lmsys/lmsys-chat-1m`

- **trials run** 2023-04 → 2023-08 (r) — in-the-wild traffic collected Apr-Aug 2023, per the dataset card.
- **unit** `score` · **multi-trial** `no` · **trajectories** `none` · **gate** `hf-gated`
- **scale** rows 1,000,000 · models 25
- **size** 1.4 GB
- **cost note** in-the-wild traffic, not commissioned runs
- **license** `other`
- **upstream updated** 2023-08-01
- In-the-wild conversations and human preference, not benchmark trials. Wrong unit for variance work; listed to close the loop.

## Human-labelled traces

### TRAIL failure-attribution traces

`trail-traces` · [dataset](https://huggingface.co/datasets/PatronusAI/TRAIL) · repo: `PatronusAI/TRAIL` · [paper](https://arxiv.org/abs/2505.08638)

- **trials run** 2025-05 (r) — paper arXiv:2505.08638.
- **unit** `trajectory` · **multi-trial** `no` · **trajectories** `full` · **gate** `hf-gated`
- **scale** rows 148 · benchmarks 2
- **size** 229.9 MB
- **cost note** not published
- **license** `mit`
- **upstream updated** 2025-05-01
- 148 traces with 841 human-annotated errors across 1,987 OpenTelemetry spans.
- Encoded as OTel spans - the only entry here that already speaks a standard observability schema.
- 118 GAIA + 30 SWE-bench. Tiny, but densely labelled.

### AgentRewardBench

`agent-reward-bench` · [dataset](https://huggingface.co/datasets/McGill-NLP/agent-reward-bench) · repo: `McGill-NLP/agent-reward-bench` · [paper](https://arxiv.org/abs/2504.08942)

- **trials run** 2025-04 (r) — paper arXiv:2504.08942.
- **unit** `trajectory` · **multi-trial** `no` · **trajectories** `full` · **gate** `open`
- **scale** rows 1,302 · benchmarks 5 · models 4
- **size** 35.7 GB
- **cost note** not published
- **license** `unset` — **not redistributable**
- **upstream updated** 2025-04-21
- 1,302 web-agent trajectories with EXPERT human review of whether the run actually succeeded.
- Built to evaluate LLM judges, so it is labelled where almost nothing else is.
- One trajectory per (task, model). No repeats.

### SWE-bench Verified human annotations

`swebench-verified-annotations` · [dataset](https://openai.com/index/introducing-swe-bench-verified/) · [home](https://huggingface.co/datasets/SWE-bench/SWE-bench_Verified)

- **trials run** 2024-08 (r) — human annotation campaign, published 2024-08-13. Not model runs.
- **unit** `score` · **multi-trial** `no` · **trajectories** `none` · **gate** `open`
- **scale** rows 1,699 · tasks 1,699 · trials_per_cell 3 human raters per task
- **size** 7.6 MB
- **cost note** human annotation cost, not compute; not published
- **license** `apache-2.0`
- **upstream updated** 2024-08-13
- Task-validity labels, not agent runs. 3 independent human raters on 1,699 candidate tasks.
- The closest thing the field has to ground truth on whether a benchmark task is broken.

## Training trajectory dumps (not evaluation)

### NVIDIA Open-SWE-Traces

`nvidia-open-swe-traces` · [dataset](https://huggingface.co/datasets/nvidia/Open-SWE-Traces) · repo: `nvidia/Open-SWE-Traces`

- **trials run** 2026-06 (r) — upstream last modified 2026-06; SFT generation, not an eval campaign.
- **unit** `trajectory` · **multi-trial** `no` · **trajectories** `full` · **gate** `open`
- **scale** rows 200,000
- **size** 39.7 GB
- **cost note** not published; 200k+ agent rollouts is a very large spend
- **license** `cc-by-4.0`
- **upstream updated** 2026-06-01
- Training data, not evaluation. Success-filtered and usually single-teacher.
- Listed so nobody mistakes its size for eval coverage. Representative of a whole family: SWE-smith (76k), SWE-Gym, nebius SWE-rebench (67k), R2E-Gym.

### SWE-smith trajectories

`swe-smith-trajectories` · [dataset](https://huggingface.co/datasets/SWE-bench/SWE-smith-trajectories) · repo: `SWE-bench/SWE-smith-trajectories` · [paper](https://arxiv.org/abs/2504.21798)

- **trials run** 2025-04 (r) — paper arXiv:2504.21798; SFT generation.
- **unit** `trajectory` · **multi-trial** `partial` · **trajectories** `full` · **gate** `open`
- **scale** rows 76,002 · trials_per_cell up to 3 per task instance, after filtering
- **size** 3.9 GB
- **cost note** not published
- **license** `mit`
- **upstream updated** 2025-04-01
- SFT corpus generated with SWE-agent + Claude 3.7. Repeats exist but are success-filtered.

## Other indexes

### Every Eval Ever (EvalEval datastore)

`eee-datastore` · [dataset](https://huggingface.co/datasets/evaleval/EEE_datastore) · repo: `evaleval/EEE_datastore`

- **trials run** 2026-09 (r) — continuously updated aggregation, not a run campaign.
- **unit** `collection` · **multi-trial** `no` · **trajectories** `none` · **gate** `open`
- **scale** rows 107
- **size** 3.1 GB
- **cost note** aggregation of published scores; no compute of its own
- **license** `mit`
- **upstream updated** 2026-09-14
- The largest existing consolidation effort - 107 eval collections normalized to one score schema.
- Converts Inspect, HELM and lm-eval-harness output. Samples are optional; trial archives are out of scope.
- Closest prior art to this index, but it consolidates SCORES, not runs.

### OpenEval (Open-Eval-Commons)

`openeval-commons` · [dataset](https://huggingface.co/datasets/Open-Eval-Commons/OpenEval) · repo: `Open-Eval-Commons/OpenEval`

- **trials run** 2026-09 (r) — aggregation, not a run campaign.
- **unit** `score` · **multi-trial** `no` · **trajectories** `none` · **gate** `open`
- **scale** 
- **size** 8.6 GB
- **cost note** aggregation; no compute of its own
- **license** `cc-by-nc-4.0`
- **upstream updated** 2026-09-05
- Item-level LLM responses rather than agent runs. Good for item-response-theory work.
- Non-commercial licence, which rules it out of a lot of downstream use.

## Totals

- **27 datasets indexed** — 17 agent-trials, 3 labeled-traces, 3 llm-scores, 2 meta-index, 2 sft-traces
- **1.0 TB** of data across entries that report a size
- **$61,563** of known compute spend, from the 2 of 27 entries where the cost is published or measurable
- **14** entries have repeated trials per cell; 13 do not or do not say

## Scope

Included: public datasets where the unit of record is an evaluation *run*, *score* or
*trajectory* produced by a model or agent.

Also included, marked clearly, are three kinds of near-miss that are easy to mistake
for the real thing:

- **Single-shot archives** (`swebench-experiments`, `theagentcompany-experiments`) —
  every official submission is a different system, not an i.i.d. repeat.
- **SFT trajectory dumps** (`nvidia-open-swe-traces`, `swe-smith-trajectories`) — huge,
  but success-filtered training data from usually one teacher model.
- **Wrong-unit corpora** (`lmsys-chat-1m`) — in-the-wild traffic and human preference.

Not included: benchmark *task* definitions with no run data attached, private or
request-only corpora, and leaderboards that publish a number with no underlying records.

## Notable gaps

- **Cost is almost never published.** Two of 27 entries report it. HAL is the only
  project that treated spend as a headline result.
- **Balanced factorials are rare.** Toolathlon (17 models × 3 runs × 108 tasks) is one
  of the only clean designs. Most coverage is ragged.
- **Nobody publishes negative results.** Failed runs get filtered out of SFT dumps,
  which is precisely what you would need to study failure.

## Contributing

Add a block to `registry/*.yaml` and run `evaltrials render`. The README is generated
from the registry — edit the YAML, not the markdown.

Required per entry: `id`, `title`, `kind`, `unit`, `multi_trial`, `trajectories`,
`upstream`, `license` (including `redistributable`), `gate`. If you set `cost.usd` you
must also set `cost.basis` to `measured`, `reported` or `estimated`, and say in
`cost.note` where the number came from.

Corrections are more useful than additions.

**Verification status.** Sizes for the 18 HuggingFace-hosted entries were read from the
HF API on 2026-09-14 and match the cards. The 7 entries hosted on GitHub or ModelScope
have no size recorded because it was not cheaply checkable. Run dates are measured from
the data for two entries and taken from papers or upstream metadata for the rest — the
`(m)`/`(r)`/`(u)` markers say which. Row counts largely come from dataset cards and
papers and are the least verified numbers here.

## License

MIT for the index itself. Every dataset listed keeps its own license, recorded per
entry and flagged in the table.

<!-- generated by `evaltrials render`; edit registry/*.yaml and docs/intro.md, not this file -->
