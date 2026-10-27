# Quickstart: reopening the projector window

**Slice**: `specs/141-projector-window-reopen`

## Look at it

The approved preview is a static page built from the project's own `tokens.css` and
`components.css`. Serve the worktree root so the relative stylesheet links resolve:

```bash
cd ~/Projects/multimedia-gkps-klender-141
/home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python -m http.server 8811 --bind 127.0.0.1
# http://127.0.0.1:8811/specs/141-projector-window-reopen/preview/preview.html
```

The switches at the top flip display state, Media files and theme; the three frames are the stage
column at a 1440, 1280 and 425 px window.

## Run the tests

The suite is Playwright (Python) through Django's `LiveServerTestCase`. The database is the compose
service; its host port is whatever Docker published:

```bash
cd ~/Projects/multimedia-gkps-klender-141
PY=/home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python
PORT=$(docker port multimedia-gkps-klender-db-1 5432/tcp | head -1 | sed 's/.*://')
PW=$(grep -m1 'POSTGRES_PASSWORD' docker-compose.yml | sed 's/.*: *//')
DATABASE_URL="postgres://multimedia:$PW@127.0.0.1:$PORT/multimedia" \
DJANGO_SECRET_KEY=dev-insecure-local-only-change-me \
$PY manage.py test tests.e2e.test_projector --keepdb
```

`--keepdb` reuses the test database; if another session holds it, wait for that run to end rather
than dropping it. The suite runs headless; nothing is started outside the test process.

## See it in the running app

The dev server the operator uses is whichever worktree runs one. For this slice:

```bash
cd ~/Projects/multimedia-gkps-klender-141
DATABASE_URL="postgres://multimedia:$PW@127.0.0.1:$PORT/multimedia" \
DJANGO_SECRET_KEY=dev-insecure-local-only-change-me \
$PY manage.py runserver 0.0.0.0:8812 --noreload
# a Tata Ibadah: http://127.0.0.1:8812/tatib/<id>/
```

Press **Project**, step the service, close the projector window, then press the new control in the
page's header: the window returns on the screen that was on air and the page still reads
**Stop projecting**.

Python edits need a restart (`--noreload`); template, JS and CSS changes are picked up per request
once `collectstatic` has run for the static files this worktree serves.
