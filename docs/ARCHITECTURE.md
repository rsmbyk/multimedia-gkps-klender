# Architecture

As-built notes for this repository. Humans and agents follow **this doc**, not memory. Facts are
taken from the codebase; items marked *(confirm)* are the owner's call.

## Git and versioning

- **Git model:** **Git Flow** (locked by [ADR 0002](adr/0002-git-flow-merge-strategy.md)).
  - `main` — production (deployed to Vercel).
  - `develop` — integration.
  - **Features** (`feat/*`, `fix/*`, `chore/*`, `docs/*`) branch from `develop` and merge **into
    `develop` with a squash merge** (one commit per PR). Default PR target is `develop`.
  - **Releases** (`release/*`) branch from `develop`; **hotfixes** (`hotfix/*`) branch from `main`.
    Both target `main`, and **every merge into `main` uses a standard merge commit** (history is
    preserved, never squashed).
  - After a release/hotfix lands on `main`, merge `main` back into `develop` so `VERSION` stays
    aligned, then tag `vX.Y.Z` on the `main` commit.
  - **After any merge: delete the remote branch only. Keep the local branch intact.**
  - Never force-push `main` or `develop`; never create vendor/agent-named branches.
  Recorded here per [`docs/PROCESS.md`](PROCESS.md).
- **Versioning:** SemVer, locked by vexbook. Identity is repo-root [`VERSION`](../VERSION),
  [`CHANGELOG.md`](../CHANGELOG.md), and annotated tags `vX.Y.Z`. The changelog uses the Keep a
  Changelog structure; pre-adoption history is archived at
  [`docs/CHANGELOG-archive.md`](CHANGELOG-archive.md). `VERSION` continues from the highest tag
  shared with the parallel `develop` line (currently `0.6.0`, the first feature release after
  adoption). See [ADR 0001](adr/0001-adopt-vexbook-process.md).

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

URL roots (`multimedia/urls.py`): `/admin/`, `/api/`, `/obs/`, and the Django app at `/` — public
reading at `/songs/…`, editor at `/manage/…`.

The site root `/` serves the empty-search public reading index by default. Setting
`MAINTENANCE_MODE=true` serves a 503 notice (`reading/maintenance.html`) at `/`; `/home/` remains a
compatible reading-home route. Only `/` is gated; every other surface is unaffected.

Public reading pages use the project's own design language (`static/styles/design/tokens.css`,
`components.css`); Fomantic UI remains in use by the editor and OBS surfaces until they migrate.

### Offline public reading and projector

- `static/web/offline-library.js` owns the browser's revisioned IndexedDB library. It stages
  changed chunks as a new generation and publishes only a complete generation; public reading and
  projector Go To use that committed data.
- `static/web/service-worker.js` caches only the public reading and service-projector shells and
  their required versioned assets. Its navigation fallback is deliberately limited to those routes;
  legacy OBS docks, editors, and other pages continue using the network.
- `static/web/offline-render.js` reuses the saved public shell for in-page reading navigation.
  Online refreshes request data chunks asynchronously. `static/web/projector-library.js` resolves
  Go To and service detours from the same local Bible/song library.
- This storage is a presentation fallback and search source. It does not queue editor writes or
  replace the server as the authoritative content store.

## Boundaries

### Computer-level Media Library

`multimedia/local_media.py` is a separate Python companion process on the projector
computer. It stores file bytes and a SQLite index in the current operating-system
user's data directory: `%LOCALAPPDATA%\GKPS Klender\Media Library` on Windows,
`~/Library/Application Support/GKPS Klender/Media Library` on macOS, and
`$XDG_DATA_HOME/gkps-klender/media-library` (or `~/.local/share/...`) on Linux.
The `files/` directory uses SHA-256 names; the index holds the displayed filename,
detected family, upload date, usage state, and local retention setting. See
[`docs/local-media-companion.md`](local-media-companion.md) for startup.

The companion accepts requests only on `127.0.0.1:47863` from explicitly
configured application origins. Selection sends bytes to a temporary inspection
endpoint; Save sends them to the import endpoint for the verified atomic copy.
Both return the hash and metadata. Django stores only that identity and an immutable service-entry
reference. The same companion and folder serve Chrome and the OBS dock on one
computer. The Media Library page fetches service references from Django, then
sends a complete reference inventory to the companion before unused-file cleanup.
Neither browser profile nor Vercel stores these file bytes.

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
- CI: [`.github/workflows/ci.yml`](../.github/workflows/ci.yml) runs the fast lane for relevant PR
  updates to `develop`/`main` and pushes to those branches. Draft PRs do not run browser tests;
  ready-for-review PRs run each E2E module in parallel. Relevant code changes rerun E2E, while
  docs/spec/backlog/version/changelog-only changes do not. Every job uses its own ephemeral
  PostgreSQL service; no production data or credentials are configured.
- The current GitHub plan does not allow branch-protection/ruleset enforcement for this private
  repository, so maintainers must manually confirm the fast check and every E2E shard are green
  before merging.

## Hosting

- Production: Vercel (project `multimedia-gkps-klender`), configured by `vercel.json`.
- Allowed hosts / secrets come from environment (`.env` locally).
