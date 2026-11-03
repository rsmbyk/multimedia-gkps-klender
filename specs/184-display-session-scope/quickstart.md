# Quickstart: the active Tata Ibadah lasts only the browser session

**Spec**: [`spec.md`](./spec.md) · **Plan**: [`plan.md`](./plan.md) · **Data model**:
[`data-model.md`](./data-model.md) · **Contracts**: [`contracts/none.md`](./contracts/none.md)

Everything below runs from this slice's worktree (`~/Projects/multimedia-gkps-klender-184`) with the
main checkout's virtualenv. The compose Postgres is the only service needed; a throwaway database
keeps the dev data untouched (and keeps another agent's test run from colliding).

## 1 — A database of this slice's own

```sh
docker exec -e PGPASSWORD=multimedia multimedia-gkps-klender-db-1 \
  psql -U multimedia -d postgres -c 'CREATE DATABASE gkps184'
export DATABASE_URL="postgres://multimedia:***@127.0.0.1:59075/gkps184"
~/Projects/multimedia-gkps-klender/.venv/bin/python manage.py migrate --noinput
```

The tests create `test_gkps184` from this connection; `--keepdb` makes the second run cheap.

## 2 — The acceptance tests

```sh
~/Projects/multimedia-gkps-klender/.venv/bin/python manage.py test \
  tests.e2e.test_display_session --keepdb --noinput
```

The module covers both directions of the boundary:

- a prior session's state paints nothing — injected into a fresh context with
  `add_init_script`, with a `MutationObserver` installed from document start so "not even a frame" is
  a number, not an impression;
- the same session keeps the display across a reload and across every surface closing;
- a real browser restart — `launch_persistent_context` on a temporary profile — ends it while
  `localStorage` still holds the state.

The existing suites that must stay green (they read the same state):

```sh
~/Projects/multimedia-gkps-klender/.venv/bin/python manage.py test \
  tests.e2e.test_obs_dock tests.e2e.test_obs_overlay tests.e2e.test_projector \
  --keepdb --noinput
```

`tests.e2e.test_reading` carries the Project/Stop and reopen controls; run it too when the change
touches `display.js`'s button path (it does).

## 3 — See it by hand

```sh
~/Projects/multimedia-gkps-klender/.venv/bin/python manage.py runserver 127.0.0.1:8765
```

1. Open `http://127.0.0.1:8765/obs/dock`, pick a Tata Ibadah, press an entry: the dock shows the
   display control filled and the picker row wears "On screen".
2. Open `http://127.0.0.1:8765/obs/source/overlay` in a second window: it paints the screen.
3. Close both windows, and quit the browser completely.
4. Reopen the browser on the dock: no row wears "On screen", the control reads "Display this
   service", and the overlay (opened again) paints nothing.
5. Project again; close only the overlay and the dock, reopen the dock in the same browser: the
   service is still on air — spec 119's rule survives inside the session.

## 4 — What a reviewer should look at

- `static/web/display-session.js` — the whole rule: `current`, `stamp` (write-then-re-read),
  `owns`.
- `static/web/display.js` — `read()` and `write()` are the only changes.
- `static/web/projector.js` — its own `read()`/`write()` gain the same two calls.
- `static/web/obs-overlay.js` — `readState()` gains the check; the first paint follows it.
- `static/web/../templates/reading/{base,obs_dock,projector,obs_overlay}.html` — one script tag each.
