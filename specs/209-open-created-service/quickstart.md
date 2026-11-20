# Quickstart: a newly created service opens on the reading stage

**Spec**: `specs/209-open-created-service/spec.md`

## Prerequisites

- Python 3.12 with the repo's venv at `~/Projects/multimedia-gkps-klender/.venv`.
- Playwright Chromium available in that venv (the existing E2E suite uses it).
- No database service is required for the focused run: `DJANGO_DEVELOPMENT_MODE=true` selects SQLite.

## Setup

```sh
cd ~/Projects/multimedia-gkps-klender-209
git status --short                     # branch: feat/209-open-created-service
```

## Run

```sh
DJANGO_DEVELOPMENT_MODE=true ~/Projects/multimedia-gkps-klender/.venv/bin/python manage.py test \
  tests.e2e.test_editor --noinput
```

For the before/after measurement, start the compose web service from the main checkout and run:

```sh
~/Projects/multimedia-gkps-klender/.venv/bin/python \
  specs/209-open-created-service/reproduce.py
```

It creates one dated service on the running app and prints three snapshots (before save, after save,
after a manual click of the new row).

## Verify

| Check | Command | Expected |
| --- | --- | --- |
| Sidebar editor E2E | the `tests.e2e.test_editor` command above | all tests OK, including the new create-open scenarios |
| Template flows | `DJANGO_DEVELOPMENT_MODE=true ... manage.py test tests.e2e.test_tatib_templates --noinput` | all tests OK; generate and copy still navigate |
| Defect reproduction | the `reproduce.py` command above on the base commit | `after_save.url == '/tatib/'`, `#readName` empty, no current row |

## Not yet runnable

- A live review server from this worktree has not been started at drafting time; the gate-1
  measurement used the compose web service at `127.0.0.1:63404`, which serves the main checkout.
