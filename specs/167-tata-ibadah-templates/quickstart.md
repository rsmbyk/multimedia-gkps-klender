# Quickstart: a Tata Ibadah is a service or a template

**Spec**: `specs/167-tata-ibadah-templates/spec.md`
**Contracts**: `contracts/README.md` · **Model**: `data-model.md`

## Prerequisites

- Python 3.12 and the repo's venv — on this machine the main checkout holds it at
  `~/Projects/multimedia-gkps-klender/.venv/bin/python`; a worktree runs the worktree's `manage.py` with it.
- The compose database service. Its host port moves: `docker compose port db 5432`, password in
  `docker-compose.yml`.
- Playwright (Python) with Chromium installed for the E2E module.

## Setup

```sh
cd ~/Projects/multimedia-gkps-klender-167
export DATABASE_URL=postgres://multimedia:<pw>@127.0.0.1:<port>/gkps167   # a throwaway database
~/Projects/multimedia-gkps-klender/.venv/bin/python manage.py migrate
~/Projects/multimedia-gkps-klender/.venv/bin/python manage.py collectstatic --noinput
```

The throwaway database name matters: sibling slices share the compose service, and `test_<name>` keeps
this run out of theirs.

## Run

```sh
~/Projects/multimedia-gkps-klender/.venv/bin/python manage.py runserver 0.0.0.0:8766 --noreload
```

Then open `http://127.0.0.1:8766/tatib/` and click through in-page — the panel's **+** creates a Tata
Ibadah, its Normal/Template chips pick the type, and a template's page carries **Use template** where a
service carries its projector controls.

Static files are served from `_static/`: after editing `static/`, run `collectstatic` and restart, or the
page keeps the old CSS.

## Verify

| Check | Command | Expected |
| --- | --- | --- |
| Model, forms, endpoints, guards | `manage.py test multimedia.web.test_tatib_templates --keepdb` | all green |
| Neighbouring suites still green | `manage.py test multimedia.web multimedia.api.tatib tests.e2e.test_entries --keepdb` | all green |
| The operator's flow in a browser | `python tests/e2e/test_tatib_templates.py` (Playwright, live server above) | all green; screenshots on failure in `test-results/` |
| The preview still matches the spec | `python specs/167-tata-ibadah-templates/preview/probe.py` | exit 0, `console_errors: []` |
| The type never disagrees with the date | `manage.py shell -c "from multimedia.tatib.models import TataIbadah as T; print(T.objects.filter(kind=0, date=None).count(), T.objects.filter(kind=1, date__isnull=False).count())"` | `0 0` |
| A template carries no payload | open `/projector?service=<template id>` | the empty display, no screens |

## Not yet runnable

- Nothing. Every command above runs against the working tree; the E2E module needs the dev server named
  under **Run**, which is why it is listed separately from the unit tests.
