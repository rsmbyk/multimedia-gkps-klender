# Quickstart: Media Library filter-pill hover

**Spec**: `specs/239-media-filter-pill-hover/spec.md`

## Prerequisites

- The slice worktree at `~/Projects/multimedia-gkps-klender-239` with the Python
  environment at `../multimedia-gkps-klender/.venv/bin/python` and Chromium installed
  for Playwright.
- The local dev server (currently running). No database credentials are stored in the
  spec pack: `DJANGO_DEVELOPMENT_MODE=true` uses the worktree's own SQLite file.

## Setup

```sh
cd ~/Projects/multimedia-gkps-klender-239
DJANGO_DEVELOPMENT_MODE=true ../multimedia-gkps-klender/.venv/bin/python manage.py runserver 0.0.0.0:8767 --noreload
```

`DEBUG` is on, so static files are read from source and a hard reload picks up CSS
edits. See `data-model.md` for the boxes and tokens and `contracts/README.md` for the
explicit `none` interface decision.

## Run

```sh
# Live preview: open / first, then click the Media Library rail.
xdg-open http://127.0.0.1:8767/media-library/

# Frozen before/after readouts in both themes:
../multimedia-gkps-klender/.venv/bin/python \
  specs/239-media-filter-pill-hover/preview/probe.py
```

## Verify

| Check | Command | Expected |
| --- | --- | --- |
| Live probe | command above | unpressed pill rest `transparent / #D9D6CD` → hover `rgba(31,31,29,.08) / #1C5C3C` in light, `rgba(255,255,255,.09) / #7C9CF0` in dark; 63.36 × 30 px throughout; pressed pill unchanged |
| Targeted E2E | `DJANGO_DEVELOPMENT_MODE=true ../multimedia-gkps-klender/.venv/bin/python manage.py test tests.e2e.test_media_filter_pill_hover --keepdb` | all tests in the new module pass; without the rule the hover assertions fail |
| Full browser suite | deferred to the push step per the owner's standing preference | report only; do not run between pushes |

## Not yet runnable

- The targeted E2E module is written during Implement, not at Plan; its command is a
  path, not a claim that it has passed.
- The probe needs a running local server and a Python with Playwright; both are
  machine-specific and intentionally not stored in the spec pack.
