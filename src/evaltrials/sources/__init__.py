"""Per-source fetch + normalize. One module per upstream shape."""
from . import harbor, lhtb, terminalbench

REGISTRY = {
    "harbor-adapter": harbor,
    "terminalbench-yoonholee": terminalbench,
    "lhtb-leaderboard": lhtb,
}


def get(source_id: str):
    if source_id not in REGISTRY:
        raise KeyError(
            f"no fetcher for {source_id!r}. implemented: {sorted(REGISTRY)}. "
            f"run `evaltrials catalog` to see planned sources."
        )
    return REGISTRY[source_id]
