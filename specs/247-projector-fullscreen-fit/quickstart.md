# Quickstart: refit the projector words when fullscreen changes the stage

**Spec**: `specs/247-projector-fullscreen-fit/spec.md`
**Design**: [`data-model.md`](../data-model.md) · [`contracts/README.md`](../contracts/README.md)

## Prerequisites

- Python 3.12 at `~/Projects/multimedia-gkps-klender/.venv/bin/python` (the main checkout's venv;
  the slice worktree has none).
- The local compose stack running: `web` on 63404, `db` on 59075, `media` on 63174.
- Playwright with Chromium available to that venv for E2E cases and the preview probe.

## Setup

```sh
cd ~/Projects/multimedia-gkps-klender-247
PY=../multimedia-gkps-klender/.venv/bin/python
```

`preview/run_local.py` reads `DATABASE_URL` from the compose web container at run time, decodes
it, translates `db:5432` to the published `127.0.0.1:59075` and never prints the password. `GKPS_DB`
overrides only the database name, so a test run gets a throwaway database no parallel session
touches. The dev server needs the real database name, not the throwaway one.

## Run

```sh
python3 specs/247-projector-fullscreen-fit/preview/run_local.py -- \
  $PY manage.py runserver 0.0.0.0:8771 --noreload
```

Open `http://127.0.0.1:8771/projector?service=144`. Static changes need `collectstatic` and a
server restart; Python edits need a restart too (`--noreload`). The served JS is read directly from
`static/` in DEBUG, so a hard reload is enough after a JS edit.

## Verify

| Check | Command | Expected |
| --- | --- | --- |
| Before/after numbers | `$PY specs/247-projector-fullscreen-fit/preview/probe.py --base 'http://127.0.0.1:63404/projector?service=144' --slice 'http://127.0.0.1:8771/projector?service=144'` | base `87 → 87 → 87`, slice `87 → 93 → 87`, heading `53.769 → 57.4772 → 53.769` |
| Targeted E2E (in-between) | `GKPS_DB=gkps247 python3 specs/247-projector-fullscreen-fit/preview/run_local.py -- $PY manage.py test tests.e2e.test_projector.ProjectorE2ETests.test_fullscreen_signal_refits_the_words_without_a_resize tests.e2e.test_projector.ProjectorE2ETests.test_a_second_fullscreen_signal_does_not_change_the_fit tests.e2e.test_projector.ProjectorE2ETests.test_fullscreen_signal_refits_the_neighbours tests.e2e.test_projector.ProjectorE2ETests.test_a_fullscreen_signal_with_an_unchanged_stage_does_not_resize_words tests.e2e.test_projector.ProjectorE2ETests.test_display_mode_signal_refits_for_browser_fullscreen tests.e2e.test_projector.ProjectorE2ETests.test_resize_driven_fullscreen_still_settles_at_87_and_109 --keepdb --noinput` | six named cases pass; full suite waits for the push step |
| Full browser suite | same runner with `tests` as the single target | run at the push step, on a throwaway database |

## Not yet runnable

- An OS-level fullscreen transition cannot be produced in the headless harness; the E2E cases drive
  the same browser signals after changing the stage box and assert the rendered font size. The
  operator's F key, mouse zone and F11 paths were confirmed on the live surface.
- Safari's `(display-mode: fullscreen)` behaviour is not verified here; the existing `resize`
  path remains for browsers that do not change the query.

## Preview URL

`http://127.0.0.1:8771/projector?service=144` — the real code path with the change applied and left
uncommitted for gate 1. The comparison surface is the compose server on 63404; both serve
byte-identical projector fit code before the slice edit.
