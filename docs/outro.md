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

Corrections are more useful than additions. Several sizes and row counts here were read
off the HuggingFace API on 2026-09-14 and will drift.

## License

MIT for the index itself. Every dataset listed keeps its own license, recorded per
entry and flagged in the table.
