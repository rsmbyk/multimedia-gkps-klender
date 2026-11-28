# Quickstart: an open modal keeps the scroll to itself

**Contracts**: [none](contracts/none.md). **Data model**: [data-model.md](data-model.md) — no stored state.

All commands use the project venv at `/home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python`
and the Compose stack must be up. No credential is written to disk or printed.

Live A/B measurements (runnable now):

```bash
<venv>/bin/python specs/257-modal-scroll-containment/preview/probe.py
<venv>/bin/python specs/257-modal-scroll-containment/preview/geometry.py
```

The two URLs are hard-coded in those scripts: `63404` serves unmodified `1cd9f081`, `8765` serves
the slice worktree. The static, hand-drivable preview is
`specs/257-modal-scroll-containment/preview/index.html`; rebuild it after a CSS edit with
`preview/build_preview.py`.

Behaviour test (declared in the plan, **not yet runnable** — the module is written in Implement):

```bash
<venv>/bin/python specs/257-modal-scroll-containment/preview/run-tests.py \
  tests.e2e.test_modal_scroll_containment
```

`preview/run-tests.py` derives the published Compose host/port at call time, points at throwaway
database `gkps257`, and honours `GKPS_WORKTREE` / `GKPS_DB` overrides for a base comparison. The
suite is executed at the push step, not between gates.
