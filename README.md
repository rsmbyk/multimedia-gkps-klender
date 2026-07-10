# Multimedia GKPS Klender

Web application that helps the multimedia team at **GKPS Klender** (Gereja
Kristen Protestan Simalungun) prepare worship content and project it live with
**OBS** (Open Broadcaster Software).

## What it includes

| Area | Role |
|------|------|
| **Songs** | Hymn books, songs, verses; OBS dock + source |
| **Bible** | Passages (e.g. TB / Simalungun); OBS dock + source |
| **Tatib** | Tata ibadah (service order); OBS dock + source |
| **Project** | Combined live projection / control surfaces |
| **Bookmarks** | Song setlists for services |
| **Web admin** | Django UI to manage content |
| **REST API** | Django REST Framework endpoints used by OBS and web |

## Stack

- **Backend:** Django 4, Django REST Framework, WhiteNoise
- **Database:** PostgreSQL (e.g. Neon) in normal/deployed setups; SQLite when `DJANGO_DEVELOPMENT_MODE=True`
- **Frontend:** ES modules + Semantic UI / jQuery in OBS browser sources and web pages
- **Production:** Vercel (WSGI via `multimedia/wsgi.py`)
- **Optional local containers:** Docker Compose (`Dockerfile`, `docker-compose.yml`)

## Requirements

- Python **3.10 or 3.11** (Django 4.0.1; prefer 3.11)
- Node.js **20+** only if you run the frontend test suite
- A Postgres URL **or** development mode with SQLite (see below)

## Quick start (local)

```powershell
git clone <repository-url>
cd multimedia-gkps-klender

py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1

pip install -r requirements-dev.txt
copy .env.example .env
```

Edit `.env`. For a quick local loop with SQLite:

```env
DJANGO_DEVELOPMENT_MODE=True
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
```

For a remote/Postgres database, set `DATABASE_URL` and keep
`DJANGO_DEVELOPMENT_MODE=False` (see comments in `.env.example`).

```powershell
python manage.py migrate
python manage.py runserver
```

App: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

Optional seed data (if you use it on this clone):

```powershell
python scripts/seeder.py
```

## Docker Compose

Uses your `.env` by default (handy for a shared remote DB):

```powershell
docker compose up --build
```

Isolated local Postgres:

```powershell
docker compose -f docker-compose.yml -f docker-compose.local.yml up --build
```

App: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## OBS browser sources

Point custom browser docks / sources at the local or deployed origin, for
example:

| Surface | Path |
|---------|------|
| Songs dock | `/obs/songs/dock` |
| Songs source | `/obs/songs/source` |
| Bible dock | `/obs/bible/dock` |
| Bible source | `/obs/bible/source` |
| Tatib dock | `/obs/tatib/dock` |
| Tatib source | `/obs/tatib/source` |
| Project source | `/obs/project/source` |
| Project settings | `/obs/project/settings` |

After a deploy or local static change, **hard-refresh / clear cache** on each OBS
browser source — OBS caches aggressively.

## Tests

This project uses TDD for behavior changes. See [`docs/TDD.md`](docs/TDD.md).

```powershell
# Python (Django) — SQLite in-memory via multimedia.settings_test
pytest

# JavaScript (Vitest + jsdom)
npm install
npm test
```

## Versioning and branching

- **Branching:** Git Flow — [`docs/GIT_FLOW.md`](docs/GIT_FLOW.md)
- **Versions:** single SemVer for the whole app (from **`0.5.0`**) —
  [`docs/VERSIONING.md`](docs/VERSIONING.md)
- **History:** [`CHANGELOG.md`](CHANGELOG.md)
- **Agent / contributor index:** [`AGENTS.md`](AGENTS.md)

Default integration branch is **`develop`**. Production deploys from **`main`**.

## Documentation

| Doc | Topic |
|-----|--------|
| [`docs/GIT_FLOW.md`](docs/GIT_FLOW.md) | Branches, PRs, release / hotfix |
| [`docs/VERSIONING.md`](docs/VERSIONING.md) | SemVer, changelog area labels |
| [`docs/TDD.md`](docs/TDD.md) | pytest + Vitest, red → green → refactor |
| [`CHANGELOG.md`](CHANGELOG.md) | Released and unreleased changes |
| [`.env.example`](.env.example) | Environment variables |
