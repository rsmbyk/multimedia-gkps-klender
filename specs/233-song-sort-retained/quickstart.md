# Quickstart: song list keeps its chosen order

**Spec**: `specs/233-song-sort-retained/spec.md`

## Prerequisites

- The venv at `/home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python` (worktree tests use it).
- The compose PostgreSQL service with a published host port; a throwaway database name such as
  `gkps233` so a parallel session's test run is never locked.
- Playwright with a Chromium browser.

## Setup

The preview database and its env file already exist at
`/home/rsmbyk/.hermes/cache/scratch/gkps233.env` (mode 600). To run the E2E module from a slice
worktree, load it and point Django at the throwaway database:

```sh
cd /home/rsmbyk/Projects/multimedia-gkps-klender-233
set -a && . /home/rsmbyk/.hermes/cache/scratch/gkps233.env && set +a
/home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python manage.py test \
  tests.e2e.test_song_sort_retained --noinput -v 2
```

The test runner creates and destroys `test_gkps233`; the preview data in `gkps233` is untouched.

## Run

```sh
# from the slice worktree, with the env file sourced
.../python manage.py runserver 0.0.0.0:8773 --noreload
```

Open `http://127.0.0.1:8773/songs/book/1/`. The worktree's `static/web/reading.js` is served with
`DEBUG=True`; hard-reload after any edit. States to drive are listed in `preview/README.md`.

## Verify

| Check | Command | Expected |
| --- | --- | --- |
| Create keeps alphabetical order | `manage.py test tests.e2e.test_song_sort_retained` | green; base commit fails with `['Beta','Zebra','Alpha']` |
| Sort toggle still works | existing `tests.e2e.test_reading.py::test_song_sort_toggles_between_last_modified_and_alphabetical` | green |
| Live page serves the change | `curl -s localhost:8773/static/web/reading.js \| grep -c 'Re-apply the'` | `1` |

## Not yet runnable

The full E2E suite and the full unit suite are deferred to the push step, per the repository's
local-verification custom. Only the targeted module above is run in between.
