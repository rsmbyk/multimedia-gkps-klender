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

The site root `/` is **maintenance-gated** by `MAINTENANCE_MODE` (env, default on): while on it
serves a 503 notice (`reading/maintenance.html`), and the reading home is temporarily at `/home/`
(still the `web-home` url name, so header/search links follow it). While off, `/` serves the home.
Only `/` is gated; every other surface is unaffected.

Public reading pages use the project's own design language (`static/styles/design/tokens.css`,
`components.css`); Fomantic UI remains in use by the editor and OBS surfaces until they migrate.

## Boundaries

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
