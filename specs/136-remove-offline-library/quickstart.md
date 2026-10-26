# Quickstart — remove the offline library; the projector fetches on selection

**Slice**: `specs/136-remove-offline-library` · **Date**: 2026-10-26

Worktree: `~/Projects/multimedia-gkps-klender-136`. The venv lives in the main checkout; the compose
database is on `127.0.0.1:59075` (password from `docker-compose.yml`). `docker compose` fails in a
worktree without the missing `.env`, so the database is addressed by URL.

```sh
export DATABASE_URL="postgres://multimedia:multimedia@127.0.0.1:59075/multimedia"
VENV=~/Projects/multimedia-gkps-klender/.venv/bin/python
```

## The slice's checks

```sh
# 1. The server payloads and the removed routes (not yet runnable — the endpoints land in T004/T005)
$VENV manage.py test multimedia.web.tests --keepdb

# 2. The projector's behaviour in a browser (not yet runnable — the page changes land in T010)
$VENV manage.py test tests.e2e.test_projector --keepdb

# 3. The reading path without the saved copy (not yet runnable — T008)
$VENV manage.py test tests.e2e.test_navigation_freshness --keepdb
```

Page-rendering tests need a collected static tree or the plain storage backend; locally:

```sh
$VENV manage.py collectstatic --noinput
# or override STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage'
```

## The preview (already runnable)

```sh
$VENV manage.py runserver 0.0.0.0:8769 --noreload        # a second terminal
$VENV specs/136-remove-offline-library/preview/build_preview.py
$VENV specs/136-remove-offline-library/preview/probe_loading.py
```

`build_preview.py` writes `preview/after.html` and the four projector state pages from the pages the
server serves; `probe_loading.py` prints the rail and panel geometry the spec quotes, and writes the
screenshots.

## Manual checks after Implement

| Check | How |
| --- | --- |
| Nothing is stored | open `/home/`, browse a chapter and a song, then in the console: `navigator.serviceWorker.getRegistrations()`, `caches.keys()`, `indexedDB.databases()` |
| The routes are gone | `curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:8769/offline/manifest/` (and the other three) |
| The loading lock | open `/projector?service=144`, press `g`, type `Mat 5`, press Enter; during the fetch no key or click changes the screen and both spinners show |
| A chapter crossing | in a passage detour, hold Shift+→ from a chapter's last verse; the corner spinner appears and the next chapter paints at verse 1 |
| The index size | `curl -s http://127.0.0.1:8769/projector/goto/index/ \| wc -c`, and gzipped through `curl --compressed -w '%{size_download}'` |
