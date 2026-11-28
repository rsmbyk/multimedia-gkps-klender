# Quickstart: No empty groups after the last row is deleted

**Contracts**: [none](contracts/none.md). **Data model**: [data-model.md](data-model.md) — no stored state.

The helper `preview/run-tests.py` reads the Compose database credential at run time, derives the
published host/port, points at a throwaway database and never writes the credential to disk. It runs
with the project venv from any directory.

```bash
/home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python \
  specs/252-empty-date-group/preview/run-tests.py \
  tests.e2e.test_empty_date_group
```

On unmodified `1c86096f` this reports **4 failed**; on the slice worktree it reports **4 OK**.
For a base comparison, set `GKPS_WORKTREE` to the detached base worktree and `GKPS_DB` to a different
throwaway name.

Neighbouring check (same helper, two labels):

```bash
… run-tests.py tests.e2e.test_deleted_stage tests.e2e.test_song_sort_retained
```

Live preview (measured before gate 1):

```bash
…/.venv/bin/python specs/252-empty-date-group/preview/serve.py     # port 8776, seeds gkps252
…/.venv/bin/python /home/rsmbyk/.hermes/cache/scratch/gkps252-serve-base.py  # control, port 8777
…/.venv/bin/python specs/252-empty-date-group/preview/probe.py http://127.0.0.1:8776
…/.venv/bin/python specs/252-empty-date-group/preview/probe.py http://127.0.0.1:8777
```

All commands are runnable on this machine with the Compose stack up. The base control helper lives in
scratch because it is a one-run comparison instrument, not a slice artifact.
