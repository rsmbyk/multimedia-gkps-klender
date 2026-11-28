# Quickstart: refit the Go To detour on a stage resize

**Spec**: `specs/249-goto-fullscreen-fit/spec.md`
**Design**: [`data-model.md`](../data-model.md) · [`contracts/README.md`](../contracts/README.md)

## Prerequisites

- Python 3.12 at `~/Projects/multimedia-gkps-klender/.venv/bin/python` (main checkout venv).
- Compose stack running: `web` 63404, `db` 59075, `media` 63174.
- Playwright with Chromium in that venv.

## Run

```sh
cd ~/Projects/multimedia-gkps-klender-249
PY=../multimedia-gkps-klender/.venv/bin/python
python3 specs/249-goto-fullscreen-fit/preview/run_local.py -- \
  $PY manage.py runserver 0.0.0.0:8772 --noreload
```

`preview/run_local.py` reads `DATABASE_URL` from the compose web container at run time, translates
`db:5432` to the published host port and never prints the credential. `GKPS_DB` overrides only the
database name.

## Verify

| Check | Command | Expected |
| --- | --- | --- |
| Before/after | `$PY specs/249-goto-fullscreen-fit/preview/probe.py --base 'http://127.0.0.1:63404/projector?service=144' --slice 'http://127.0.0.1:8772/projector?service=144'` | base `87 → 87 → 87` in both orderings; slice `87 → 109 → 87` |
| Targeted E2E | `GKPS_DB=gkps249 python3 specs/249-goto-fullscreen-fit/preview/run_local.py -- $PY manage.py test tests.e2e.test_projector.ProjectorE2ETests.test_a_goto_detour_refits_on_a_resize tests.e2e.test_projector.ProjectorE2ETests.test_a_fullscreen_signal_before_resize_still_fits_the_detour tests.e2e.test_projector.ProjectorE2ETests.test_a_resize_without_a_detour_keeps_service_screens --keepdb --noinput` | three named cases pass |
| Full suite | same runner with `tests` as the single target | push step only |

## Not yet runnable

- An OS-level fullscreen cannot be produced in the headless harness; the cases use CDP viewport
  changes and the same public browser signals.
- The fonts-ready detour gap remains: faces arriving while a detour is up clear its key but do not
  fit it. Not part of this slice.
