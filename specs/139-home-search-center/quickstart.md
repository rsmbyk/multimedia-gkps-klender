# Quickstart: The landing search field sits on the window's middle

**Slice**: `specs/139-home-search-center`
**Contracts**: [`contracts/none.md`](./contracts/none.md) — no interface is exposed.
**Data model**: [`data-model.md`](./data-model.md) — no entity.

## Look at it

```bash
# the static preview (no server needed) — the rendered landing page + after.css
xdg-open specs/139-home-search-center/preview/after-home.html
xdg-open specs/139-home-search-center/preview/before-home.html

# rebuild it from a running instance (this checkout's dev server, or the compose web service)
../multimedia-gkps-klender/.venv/bin/python specs/139-home-search-center/preview/build_preview.py http://127.0.0.1:63404/

# the numbers, and fresh screenshots at 1440×900 and 390×844
../multimedia-gkps-klender/.venv/bin/python specs/139-home-search-center/preview/probe_preview.py --shots
```

## Run the slice's tests

The E2E module is written in Implement; until then this is the command it will answer to:

```bash
DATABASE_URL=postgres://multimedia:<pw>@127.0.0.1:<port>/multimedia \
  ../multimedia-gkps-klender/.venv/bin/python manage.py test tests.e2e.test_home_search_center --keepdb
```

It skips cleanly when Playwright is absent, like the other modules under `tests/e2e/`. The
`override_settings(STATICFILES_STORAGE=…)` decorator the neighbouring modules carry is required
locally: `ManifestStaticFilesStorage` raises on a missing manifest entry without a `collectstatic`.

## Look at the real page

```bash
# from this worktree, in a browser; the worktree uses the main checkout's venv
DATABASE_URL=postgres://multimedia:<pw>@127.0.0.1:59075/multimedia \
  ../multimedia-gkps-klender/.venv/bin/python manage.py runserver 0.0.0.0:8773 --noreload
```

Then open `http://127.0.0.1:8773/` and resize: the field should stay on the window's middle, and the
logo should stay whole above it, at every width down to 320px. Static files are served from `_static/`,
so after editing `static/` run `manage.py collectstatic` and restart the server, or the page keeps the
old CSS.
