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
  [`CHANGELOG.md`](../CHANGELOG.md), and annotated tags `vX.Y.Z`. `VERSION` was bootstrapped to
  `0.4.6` (latest tag reachable from `main` at adopt time) — see
  [ADR 0001](adr/0001-adopt-vexbook-process.md).

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

URL roots (`multimedia/urls.py`): `/admin/`, `/api/`, `/obs/`, and `/` (web).

## Boundaries

- Content domains (`bible`, `songs`, `tatib`, `bookmarks`) own their models and rules.
- `api` exposes the domains over REST; `obs` and `web` are presentation surfaces.
- Process and product docs live under `docs/`; they are not runtime code.

## Testing

- Django test runner (`manage.py test`); coverage output `.coverage` / `coverage-python.xml`.
- E2E tool named by PROCESS is **not yet chosen** for this stack *(confirm)*.
- CI: none on `main` yet.

## Hosting

- Production: Vercel (project `multimedia-gkps-klender`), configured by `vercel.json`.
- Allowed hosts / secrets come from environment (`.env` locally).
