# Quickstart: a newly created songbook or song opens as its row would

**Spec**: `specs/225-open-created-songbook-song/spec.md`

## Prerequisites

- Python 3.12 with the repo venv at `~/Projects/multimedia-gkps-klender/.venv`.
- Playwright Chromium available in that venv.
- A running dev server from this worktree on `127.0.0.1:8768`, with `DATABASE_URL` pointing at the
  compose database (host port `59075`).

## Setup

```sh
cd ~/Projects/multimedia-gkps-klender-225
git status --short                     # branch: feat/225-open-created-songbook-song
```

## Run

```sh
DJANGO_DEVELOPMENT_MODE=true ~/Projects/multimedia-gkps-klender/.venv/bin/python manage.py test \
  tests.e2e.test_editor --noinput
```

For the before/after measurement against the running app:

```sh
~/Projects/multimedia-gkps-klender/.venv/bin/python \
  specs/225-open-created-songbook-song/reproduce.py
~/Projects/multimedia-gkps-klender/.venv/bin/python \
  specs/225-open-created-songbook-song/probe_click.py
```

They create two records and print the base and click-through snapshots respectively.

## Verify

| Check | Command | Expected |
| --- | --- | --- |
| Sidebar editor E2E | the `tests.e2e.test_editor` command above | all tests OK, including the new create-open scenarios |
| Reading suite | `... manage.py test tests.e2e.test_reading --noinput` | no regression in row clicks and stage state |
| Defect reproduction | the two probes on the base commit | after-save has no current row and `data-read=off`; the click-through snapshots show the target |
