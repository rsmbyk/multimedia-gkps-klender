# Quickstart: Keep Add song when the songbooks sidebar is closed

**Spec**: `specs/222-add-song-parent-closed/spec.md`

## Prerequisites

- Python 3.12 with the repository's `.venv` (the main checkout holds it); Playwright Chromium
  installed for the E2E suite; the compose PostgreSQL service running.
- The E2E suite uses Django's `StaticLiveServerTestCase`; static files are served directly.

## Setup

```sh
cd /home/rsmbyk/Projects/multimedia-gkps-klender-222
# The venv lives in the main checkout. Use a throwaway database name to avoid colliding
# with any other GKPS test run sharing the same PostgreSQL service.
DATABASE_URL=postgres://multimedia:PASSWORD@127.0.0.1:59075/gkps222 \
  /home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python manage.py test \
  tests.e2e.test_editor.EditorE2ETests.test_add_song_stays_when_the_songbooks_sidebar_is_closed \
  --keepdb --noinput
```

`PASSWORD` is the compose db service's own `POSTGRES_PASSWORD`, read from the container at run
time; it is never written into the spec pack.

## Run

```sh
# from the slice worktree, after collectstatic when static files changed
DATABASE_URL=... /home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python \
  manage.py runserver 0.0.0.0:8765 --noreload
```

Open `http://127.0.0.1:8765/`, click Kidung, open a non-hymn songbook, click the songbooks
collapse control, then click `Add song`.

## Verify

| Check | Command | Expected |
| --- | --- | --- |
| Regression test | the `manage.py test` command above | 1 test, OK |
| Preview parity | open `specs/222-add-song-parent-closed/preview/index.html`, click **Close songbooks only** | `#songAdd flex 38px`, `#panelAdd none` |
| Whole editor suite | `manage.py test tests.e2e.test_editor --keepdb --noinput` | green, apart from any card-recorded failures already red on develop |

## Not yet runnable

Nothing. The commands above are run in this slice; the exact `DATABASE_URL` is assembled at run
time from the compose container's environment.
