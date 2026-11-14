# Quickstart: Hymn songbooks above a single separator, the rest A–Z

**Spec**: `specs/128-songbook-hymn-separator/spec.md`

## Prerequisites

- The repository's compose `db` service (the panel reads songbooks from it).
- The main checkout's virtualenv: `/home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python`.
- `DATABASE_URL` pointing at the published database port.

## Setup

```sh
cd ~/.hermes/worktrees/128-songbook-hymn-separator
DATABASE_URL="postgres://multimedia:<pw>@127.0.0.1:59075/multimedia" \
  /home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python manage.py collectstatic --noinput
```

## Run

```sh
DATABASE_URL="postgres://multimedia:<pw>@127.0.0.1:59075/multimedia" \
DJANGO_SECRET_KEY=dev-insecure-local-only-change-me \
  /home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python manage.py runserver 0.0.0.0:8795 --noreload
```

Open `http://127.0.0.1:8795/songs/` — the Kidung panel. A songbook page (`/songs/book/<id>/`) and a song page
(`/songs/<song_id>/`) show the same panel.

## Verify

| Check | Command | Expected |
| --- | --- | --- |
| panel context | `… manage.py test multimedia.web.tests.ReadingViewTests --keepdb` | the new group/order assertions pass |
| rendered divider | `… manage.py test tests.e2e.test_reading.ReadingE2ETests --keepdb` | one divider, `2px`, `10px`/`10px`, filter drops it |
| saved parity | `… manage.py test tests.e2e.test_saved_render_parity --keepdb` | the saved panel draws the same two groups |
| nothing else moved | the same three commands over the existing assertions | green without edits |

## Not yet runnable

- none — the branch runs on the compose database; the saved-render parity test needs the static files collected
  (`collectstatic`) as with every StaticLiveServerTestCase in this repo.
