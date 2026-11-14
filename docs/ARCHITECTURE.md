# Architecture

As-built notes for this repository. Humans and agents follow **this doc**, not recollection. Facts are
taken from the codebase; items marked *(confirm)* are the owner's call.

## Git and versioning

- **Git model:** Git Flow; the repository's deviations and additions are in
  [ADR 0002](adr/0002-git-flow-merge-strategy.md).
- **Versioning:** SemVer. Identity is repo-root [`VERSION`](../VERSION),
  [`CHANGELOG.md`](../CHANGELOG.md), and annotated tags `vX.Y.Z`. `VERSION` moves on
  `develop` with each merged slice; the tag matches `main`. Pre-adoption history is
  archived at [`docs/CHANGELOG-archive.md`](CHANGELOG-archive.md).

## Stack

- **Runtime:** Python 3.12 (pinned by Vercel build; `.python-version`), Django 4.0.1.
- **API:** Django REST Framework 3.13, django-filter, drf-dynamic-fields, uritemplate.
- **DB:** PostgreSQL via `DATABASE_URL` (`dj-database-url`); SQLite when
  `DJANGO_DEVELOPMENT_MODE` is set.
- **Config:** `python-decouple` reading `.env` (secrets, hosts, debug).
- **Static/serving:** WhiteNoise (`CompressedManifestStaticFilesStorage`), Gunicorn.
- **Frontend:** server-rendered Django templates plus static vanilla JS with jQuery, RxJS, and
  Fomantic UI (`static/libs/`, `static/helpers/`, `static/styles/`).
- **Hosting:** Vercel `@vercel/python`, entry `multimedia/wsgi.py`, route `/(.*)` → WSGI app.

## System shape

Django project `multimedia` with apps:

| App | Role |
| --- | --- |
| `bible` | Bible content: `Language`, `Version`, `Book`, `BookTranslation`, `Verse` |
| `songs` | Song/hymn content: `Language`, `Book`, `Song` (+ `Verse` lyrics, key) |
| `tatib` | Service order: `TataIbadah`, `TataIbadahItem` (typed, ordered) |
| `bookmarks` | Song setlists: `SongBookmark`, `SongBookmarkItem` (ordered, verse refs) |
| `api` | DRF routers/views over the domains + search |
| `obs` | OBS projection source pages and their static JS |
| `web` | Server-rendered web management UI |

URL roots (`multimedia/urls.py`): `/admin/`, `/api/`, `/obs/`, `/archive/`, and the Django app at
`/` — public reading at `/songs/…`, editor at `/editor/…`.

The site root `/` serves the empty-search public reading index by default. Setting
`MAINTENANCE_MODE=true` serves a 503 notice (`reading/maintenance.html`) at `/`; only `/` is gated.
The addresses the last release retired — `/home/`, every `/manage/…` path, the old OBS docks and
sources — answer one 302 to their live successor, and `/songs/books*` keep their 301 to the reading
pages (spec 193). The old version stays reachable for one release at `/archive/…`, which answers the
same successor in one hop, and `/obs/blank` is the transparent watermark page an old OBS source lands
on.

Public reading pages use the project's own design language (`static/styles/design/tokens.css`,
`components.css`); Fomantic UI remains in use by the editor and OBS surfaces until they migrate.

### Public reading and the projector are online-only

- Every page is painted from the response to the request that opened it. There is no saved copy, no
  service worker and no browser store of the public library (ADR 0007 retires ADR 0003).
- The projector's Go To holds a page-memory index — books, their editions' chapter and verse counts,
  songbooks and song titles, with no verse text or lyric — fetched once when the page loads and
  re-fetched by the page's Update (`multimedia/web/reading/goto.py`,
  `static/web/projector-library.js`). The search itself makes no request.
- Choosing a result fetches the whole chapter (both editions) or the whole song from
  `/projector/goto/…`, and the page locks every input until it paints. A step that leaves the loaded
  chapter is the same fetch, under the same lock.
- The server remains the only content store; nothing is cached between selections.

## Boundaries

### Computer-level Media Library

`multimedia/local_media.py` runs as the `media` service in the projector
computer's Docker Compose stack. The `media_library_data` named volume stores
file bytes and the SQLite index at `/var/lib/gkps-media`; its `files/` directory
uses SHA-256 names, and its index holds the displayed filename, detected family,
upload date, usage state, and local retention setting. The volume is local to
that Docker host and is shared by Chrome and the OBS browser dock through
`127.0.0.1:63174`. It is not mounted into the host filesystem. See
[`docs/local-media-companion.md`](local-media-companion.md) for first-time setup
and volume lifecycle.

Compose publishes the companion only on host loopback and seeds its origin
allowlist with the local web app's origins (`http://localhost:<WEB_PORT>` and
`http://127.0.0.1:<WEB_PORT>`); the operator records further origins — the
production site, a staging environment — on the companion's own page at
`http://127.0.0.1:63174/`, and the set is enforced per request from the
companion's volume. Selection sends bytes to a temporary inspection
endpoint; Save sends them to the import endpoint for the verified atomic copy.
Both return the hash and metadata. Django stores only that identity and an
immutable service-entry reference. The Media Library page fetches service
references from Django, then sends a complete reference inventory to the
companion before unused-file cleanup. Neither browser profile nor Vercel stores
these file bytes. `docker compose down` preserves the named volume;
`docker compose down -v` removes it along with the Compose database volume.

- Content domains (`bible`, `songs`, `tatib`, `bookmarks`) own their models and rules.
- `api` exposes the domains over REST; `obs` and `web` are presentation surfaces.
- Process and product docs live under `docs/`; they are not runtime code.

## Testing

- Django test runner (`manage.py test`); coverage output `.coverage` / `coverage-python.xml`.
- Local fast lane: `docker compose exec -T web python manage.py test --exclude-tag=e2e --noinput -v 1`,
  with `manage.py check` and `manage.py makemigrations --check --dry-run`.
- E2E: **Playwright (Python)**, driven from Django `StaticLiveServerTestCase` under
  `tests/e2e/`; every E2E test class has the Django `e2e` tag. Browser tests run through
  `python manage.py test` after `playwright install chromium`.

## Hosting

- Production: Vercel (project `multimedia-gkps-klender`), configured by `vercel.json`.
- Allowed hosts / secrets come from environment (`.env` locally).
