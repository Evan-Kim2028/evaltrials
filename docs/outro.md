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

- **Cost is almost never published.** Five of 27 entries report it, totalling $376,563.
  Harbor (>$300K) and HAL (~$40K) are the only projects that treated campaign spend as a
  headline result. The [EvalEval cost survey](https://huggingface.co/blog/evaleval/eval-costs-bottleneck)
  (April 2026) is the best single collection of what evals actually cost.
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

## Maintaining

`scripts/verify_upstream.py` re-reads every HuggingFace entry's size and row count and
reports where the registry has drifted. It reads metadata only — it never downloads a
dataset.

```sh
python scripts/verify_upstream.py     # 0 drifted = the registry matches upstream
```

Four entries are gated. To verify those you need a HuggingFace read token with
"read gated repos" enabled, supplied through the environment or the standard location:

```sh
export HF_TOKEN=...          # or
huggingface-cli login        # writes ~/.cache/huggingface/token, chmod 600
```

**No token is ever stored in this repository.** `.env` is gitignored, and CI reads an
encrypted GitHub Actions secret. A token committed to a public repo is a revoked token —
HuggingFace scans public GitHub and disables anything it finds.

Note that a token alone is not enough for a gated dataset: you must also accept each
dataset's terms on its HuggingFace page as that user.

## License

MIT for the index itself. Every dataset listed keeps its own license, recorded per
entry and flagged in the table.
