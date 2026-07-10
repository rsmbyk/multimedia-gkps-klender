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
- **Database:** PostgreSQL (Docker Compose locally; Neon/`DATABASE_URL` in production)
- **Frontend:** ES modules + Semantic UI / jQuery in OBS browser sources and web pages
- **Production:** Vercel (WSGI via `multimedia/wsgi.py`)
- **Local app runtime:** Docker Compose only (`web` + local Postgres)

## Requirements

- **Docker** (local app) — on this machine use the VirtualBox `docker-vm` context, not Docker Desktop
- **Python 3.10 or 3.11** only if you run the pytest suite on the host (prefer 3.11)
- **Node.js 20+** only if you run the frontend test suite

## Quick start (local Docker)

```powershell
git clone <repository-url>
cd multimedia-gkps-klender

copy .env.example .env
docker compose up --build
```

App: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

Compose always injects a local `DATABASE_URL` for the `db` service. Do **not**
point local development at production Neon.

Optional seed data (inside the running `web` container, if you use it on this
clone):

```powershell
docker compose exec web python scripts/seeder.py
```

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

Host Python is for the test suite; the app itself runs in Docker.

```powershell
# Python (Django) — SQLite in-memory via multimedia.settings_test
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
pytest

# JavaScript (Vitest + jsdom)
npm install
npm test
```

## Versioning and branching

- **Branching:** Git Flow — [`docs/GIT_FLOW.md`](docs/GIT_FLOW.md)
- **Versions:** single SemVer for the whole app (from **`0.5.0`**) —
  [`docs/VERSIONING.md`](docs/VERSIONING.md)
- **Production deploy:** Vercel + `main` — [`docs/DEPLOY.md`](docs/DEPLOY.md)
- **History:** [`CHANGELOG.md`](CHANGELOG.md)
- **Agent / contributor index:** [`AGENTS.md`](AGENTS.md)

Default integration branch is **`develop`**. Production deploys from **`main`**.

## Documentation

| Doc | Topic |
|-----|--------|
| [`docs/GIT_FLOW.md`](docs/GIT_FLOW.md) | Branches, PRs, release / hotfix |
| [`docs/VERSIONING.md`](docs/VERSIONING.md) | SemVer, changelog area labels |
| [`docs/DEPLOY.md`](docs/DEPLOY.md) | Vercel production runbook and landmines |
| [`docs/TDD.md`](docs/TDD.md) | pytest + Vitest, red → green → refactor |
| [`docs/SDD.md`](docs/SDD.md) | Spec-Driven Development and Spec IDs |
| [`docs/BACKLOG.md`](docs/BACKLOG.md) | In-repo backlog and tracker (`BL-*`) |
| [`CHANGELOG.md`](CHANGELOG.md) | Released and unreleased changes |
| [`.env.example`](.env.example) | Local Docker environment variables |
