# Quickstart: the empty notice leaves the stage

**Spec**: `specs/161-projector-empty-notice/spec.md`

## Prerequisites

- The repository's virtualenv at `~/Projects/multimedia-gkps-klender/.venv` (Django 4.0, Playwright).
- The compose stack's PostgreSQL, published on `127.0.0.1:59075` (password in `docker-compose.yml`).
- Playwright's Chromium installed in that virtualenv (`playwright install chromium`).

## Setup

```sh
cd ~/Projects/multimedia-gkps-klender-161
export DATABASE_URL="postgres://multimedia:***@127.0.0.1:59075/multimedia"
export DJANGO_SECRET_KEY=dev-insecure-local-only-change-me
```

## Run

```sh
~/Projects/multimedia-gkps-klender/.venv/bin/python manage.py runserver 0.0.0.0:8765 --noreload
```

Open `http://127.0.0.1:8765/projector?service=147` — a Tata Ibadah with no items. Press `g`, type
`Mat 5`, press `Enter`: the passage paints. With this slice's code the empty notice is gone; on the
base commit it sits under the words. `Escape` closes the detour and brings it back.

The static preview needs no server: open
`specs/161-projector-empty-notice/preview/preview.html` directly (its README has the build and probe
commands).

## Verify

| Check | Command | Expected |
| --- | --- | --- |
| US1 — the notice leaves for a Go To passage | `... test tests.e2e.test_projector.ProjectorE2ETests.test_the_empty_notice_leaves_the_stage_for_a_goto_passage` | green; red on the base commit for the reason named in `tasks.md` |
| US1 — it returns when the detour closes | `... test tests.e2e.test_projector.ProjectorE2ETests.test_closing_the_detour_brings_the_empty_notice_back` | green |
| US2 — a re-read with screens hides it | `... test tests.e2e.test_projector.ProjectorE2ETests.test_a_reread_with_screens_hides_the_empty_notice` | green |
| US2 — a re-read with none keeps it | `... test tests.e2e.test_projector.ProjectorE2ETests.test_a_reread_without_screens_keeps_the_empty_notice` | green |
| the empty state still exists | `... test tests.e2e.test_projector.ProjectorE2ETests.test_an_empty_service_shows_its_empty_state` | green, now reading visibility as well as copy |
| FR-005 — one decision point | `grep -n "projector__empty" static/web/projector.js` | the helper's body, and no other write to the notice |
| SC-002 — the band returns | `~/Projects/multimedia-gkps-klender/.venv/bin/python specs/161-projector-empty-notice/preview/probe.py` | notice `none`/no box on the Go To slice board; stage 1856×984; fitted lines 107px |

`...` stands for
`DATABASE_URL="$DATABASE_URL" ~/Projects/multimedia-gkps-klender/.venv/bin/python manage.py`.

## Not yet runnable

- The full suite and the whole browser E2E matrix: the push step, per the repo's practice (targeted
  modules while iterating).
