# Quickstart: the copy confirmation as a dialog of its own, and the copy's name

**Spec**: `specs/215-copy-template-dialog/spec.md`
**Contracts**: [`contracts/README.md`](contracts/README.md) · **Data model**: [`data-model.md`](data-model.md)

## Prerequisites

- The project venv, in the main checkout: `/home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python`
- The compose `db` service running (`docker compose ps db`), which the focused test run needs
- Playwright's Chromium, already installed for the E2E lane

## Setup

```sh
cd ~/Projects/multimedia-gkps-klender-215
PW=$(docker exec multimedia-gkps-klender-db-1 printenv POSTGRES_PASSWORD)
PORT=$(docker compose port db 5432 | cut -d: -f2)   # or read it from the running container
export DATABASE_URL="postgres://multimedia:${PW}@127.0.0.1:${PORT}/gkps215"
```

A throwaway database name keeps this run off the one a parallel session may be using.

## Run

```sh
# the unit lane for the endpoint and the fragment context
.venv/bin/python manage.py test multimedia.web.test_tatib_templates --keepdb --noinput

# the E2E lane for the confirmation
DJANGO_DEVELOPMENT_MODE=true .venv/bin/python manage.py test tests.e2e.test_tatib_templates --keepdb --noinput

# the preview, and every number the spec cites
.venv/bin/python specs/215-copy-template-dialog/preview/build.py
.venv/bin/python specs/215-copy-template-dialog/preview/probe.py
```

A page-rendering test needs `override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')` or a `collectstatic` first, because the manifest storage raises *Missing staticfiles manifest entry* locally.

## Verify

| Check | Command | Expected |
| --- | --- | --- |
| the endpoint takes the posted name | `manage.py test multimedia.web.test_tatib_templates` | the new name tests pass; the two spec-167 copy tests still pass unchanged |
| the layer is the window's | `manage.py test tests.e2e.test_tatib_templates` | the rewritten geometry test passes: layer rect equals the viewport, `position: fixed` |
| the edit dialog survives | same | its title is still rendered and its height is unchanged across open and close |
| the name selects on click | same | `selectionStart` 0, `selectionEnd` = length; a second click gives a caret |
| the copy takes the typed name | same | the created row's `name` equals what was typed, and the source's is unchanged |
| the preview's numbers | `preview/probe.py` | the JSON it prints matches the spec's `## UI/UX` table |

## Not yet runnable

- Nothing. Every command above runs in this worktree today; the tests it names are the ones the slice adds or rewrites.
