# Quickstart: A text entry is written and edited in the media modal's large frame

**Spec**: `specs/133-text-modal-large-frame/spec.md`

## Prerequisites

- The repository's virtualenv: `/home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python`
- The compose database running (`docker ps` → `multimedia-gkps-klender-db-1`), host port
  `docker compose port db 5432`
- `playwright` installed in that virtualenv (`import playwright`), Chromium available to it
- This worktree (`~/Projects/multimedia-gkps-klender-133`) — ports **8766/8767** belong to the 132
  worktree's server, so this slice uses **8768**

Contracts: `contracts/README.md` (none exposed) · design: `data-model.md` (no entity; the two attributes)

## Setup

```sh
cd /home/rsmbyk/Projects/multimedia-gkps-klender-133
export PW=$(grep -m1 'POSTGRES_PASSWORD:' docker-compose.yml | sed 's/.*POSTGRES_PASSWORD: *//')
export DATABASE_URL="postgres://multimedia:${PW}@127.0.0.1:59075/multimedia"
/home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python manage.py collectstatic --noinput
```

`collectstatic` is required: the project uses `CompressedManifestStaticFilesStorage`, so a served page
raises *Missing staticfiles manifest entry* until `_static/` holds the manifest for the current CSS.
Re-run it after any stylesheet edit, then restart the server — the manifest is read at startup.

## Run

```sh
/home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python manage.py runserver 0.0.0.0:8768 --noreload
```

Open `http://127.0.0.1:8768/`, click a Tata Ibadah, then `Add Text` (an empty service shows the four
tiles; `/tatib/144/` has the local text entry used for the edit case).

## Verify

| Check | Command | Expected |
| --- | --- | --- |
| The two create dialogs are the same box | `…/.venv/bin/python specs/133-text-modal-large-frame/preview/probe_modal_frame.py http://127.0.0.1:8768 /tmp/tatib-133 /tatib/148/ '[data-entry-edit="3"]' /tatib/144/` | `text` and `media` both `840x760 at (300,70)`, title 72.5, actions y=772 |
| The Text box fills the frame | same probe | textarea `419` create, `507` edit |
| Narrow windows keep the frame | same probe | `1280x800` → 840×760 at (220,20); `390x844` → 352×760 at (19,42), title 64.5 |
| The dialog ignores the page's scroll | same probe (edit row) + the README's scroll step | dialog top 70 at scrollY 556 |
| The marker is server-side and per kind | `.venv/bin/python manage.py test multimedia.web.ServiceEntryViewTests --keepdb` | the two new marker tests pass with the 269 existing ones |
| Box parity, fill, gutters, scrolled placement | `.venv/bin/python manage.py test tests.e2e.test_entry_modal_frame --keepdb` | green (browser suite — run at the push step, not per edit) |
| The switch and Save guard still work | `.venv/bin/python manage.py test tests.e2e.test_unified_text_screen_mode tests.e2e.test_entries --keepdb` | green, unmodified |

## Not yet runnable

- Nothing. Every command above runs in this checkout; the browser modules need a Playwright Chromium
  download the first time (`playwright install chromium`).
