# Quickstart: the preview's verse tabs get their own row

**Spec**: `specs/153-preview-tabs-row/spec.md`

## Prerequisites

- The repo's virtualenv at `../multimedia-gkps-klender/.venv` (Playwright and its Chromium already
  installed).
- The compose `db` service, and a database URL no other worktree is using:
  `DATABASE_URL=postgres://multimedia:***@127.0.0.1:<db-port>/gkps153`.
- The static preview needs nothing but a browser.

## Setup

```sh
cd ~/Projects/multimedia-gkps-klender-153
export PY=../multimedia-gkps-klender/.venv/bin/python
PW=$(grep -m1 'POSTGRES_PASSWORD' docker-compose.yml | sed 's/.*POSTGRES_PASSWORD: *//; s/"//g; s/ *$//')
DBPORT=$(cd ../multimedia-gkps-klender && docker compose port db 5432 | cut -d: -f2)
export DATABASE_URL="postgres://multimedia:${PW}@127.0.0.1:${DBPORT}/gkps153"
```

## Run

```sh
$PY manage.py test tests.e2e.test_entry_preview --noinput
```

## Verify

| Check | Command | Expected |
| --- | --- | --- |
| the four new behaviours | the `Run` command above | red before the change (title 569.6px, tabs a child of the head, focus on `BUTTON.preview__tab`), green after |
| the module as a whole | the same | the preview's existing cases green; no case rewritten beyond its two locators |
| the preview's numbers | `$PY specs/153-preview-tabs-row/preview/probe.py` | the table in `spec.md`'s `## UI/UX`: title 660px, tab row at 52px, first tab at 22px, body at 97px, passage 704×52 / 52px, 358px-wide header block 95px |
| the live page, from this worktree | `DATABASE_URL=… DJANGO_SECRET_KEY=dev-insecure-local-only-change-me $PY manage.py runserver 0.0.0.0:8831 --noreload`, then `/tatib/144/` | Preview on the song: no ring on open, tabs under the title, Tab reaches tab `1`, Shift+Tab returns to the body |
| the shipped page, after the merge | `docker compose exec -T web python manage.py collectstatic --noinput && docker compose restart web`, then `http://localhost:63404/tatib/144/` | the same, with Whitenoise serving the new script and stylesheet |

## Not yet runnable

- Nothing blocks. The compose page above runs only after the merge, because the compose `web` service
  serves the `develop` checkout; the worktree server covers the same states before it.
