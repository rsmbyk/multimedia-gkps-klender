# Plan 002: Local Docker Compose stack

- **Status:** Accepted
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-003
- **Bump:** none

## Why

Local development has no containerized path. Running this project means
providing Python 3.12, a reachable PostgreSQL, and the pinned dependencies by
hand, then exporting `DATABASE_URL` yourself (Django settings require it unless
`DJANGO_DEVELOPMENT_MODE` is set). Onboarding a volunteer machine, or starting a
second checkout, is fiddly and easy to get wrong.

This repository previously shipped exactly this capability on another line of
history — tag `v0.5.2`, branch `archive/legacy-develop`
(`specs/018-local-compose-ports`, `ITEM-011`). The repo later started a fresh
`main`, and the Compose files are absent from the current tree, so
the capability is missing today. This slice re-introduces it on the current
line, with ports chosen to avoid the crowded well-known range.

## Scope / edges

**In:**

- `docker-compose.yml` — `web` (Django) + `db` (PostgreSQL 16) services, with
  `web` published on a random high host port and `db` likewise, both
  overridable through `.env`.
- `Dockerfile` — Python 3.12 slim base, project dependencies, entrypoint.
- `docker/entrypoint.sh` — optional `migrate` / `collectstatic` before the
  service command, gated by `RUN_MIGRATIONS` / `COLLECT_STATIC`.
- `.dockerignore` and `.env.example`.
- README quick start naming the real app URL.
- A regression test that pins the compose port rules.

**Out:**

- Production / Vercel configuration. `vercel.json` stays the deploy path; nothing
  in Docker is deployed.
- CI.
- Auto-detecting a free port at run time. Published ports are constants in the
  compose file; `.env` is the override.
- Container-internal ports. `web` keeps `8000`, Postgres keeps `5432`.
- Any change to the in-network `DATABASE_URL` (`…@db:5432/…`).

## Approach

Re-use the recovered Compose design (it was reviewed and merged once), adapted
to this line:

1. **`docker-compose.yml`** — publish `"${WEB_PORT:-63404}:8000"` and
   `"${DB_PORT:-59075}:5432"`. Compose reads the project `.env` for
   interpolation, so these defaults also make a fresh clone work with no
   `.env`. Make `env_file: .env` **optional** (`required: false`) so the stack
   still starts without the file, while a present `.env` still wins. Force the
   in-network `DATABASE_URL` in `environment:` so a stray production URL cannot
   hijack local development. Add a `db` healthcheck and `depends_on:
   condition: service_healthy`. Run Django's dev server (`runserver
   0.0.0.0:8000`) with the project bind-mounted for autoreload.
2. **`Dockerfile`** — `python:3.12-slim-bookworm` (matches `.python-version`;
   the recovered file used 3.11 and is updated here), install `libpq5`, install
   the pinned requirements, copy the tree, and run through the entrypoint.
3. **`docker/entrypoint.sh`** — run `migrate` when `RUN_MIGRATIONS=true` and
   `collectstatic` when `COLLECT_STATIC=true`, then `exec "$@"`.
4. **`.dockerignore`** — keep the build context small and never copy `.env` or
   `db.sqlite3`.
5. **`.env.example`** — document `WEB_PORT` / `DB_PORT`, the app URL, and the
   collision escape hatch. Adjust the recovered comments (the referenced
   `docs/DEPLOY.md` does not exist on this line; point at
   [`docs/ARCHITECTURE.md`](../../docs/ARCHITECTURE.md)).
6. **`README.md`** — a short "run locally with Docker" section.

Routing and Django settings are untouched: the stack supplies `DATABASE_URL`
and the `DJANGO_*` variables the app already reads.

## TDD

- **Domain/app tests:** `tests/test_docker_compose.py` (Django test runner,
  `python manage.py test`) — parse `docker-compose.yml` with `PyYAML` (already a
  dependency) and assert the port rules: both published ports are in
  `49152`-`65535`, neither is `8000` or `5432`, the container ports stay
  `8000` / `5432`, and `.env.example` documents the same defaults.
- **E2E (Playwright):** N/A — declared out of scope. The real proof is
  `docker compose config` with `.env` removed, then `docker compose up --build`
  and an HTTP request to the published `WEB_PORT`.

## Risks

- **Port collision is still possible.** Random high ports lower the odds; they
  do not remove them. `WEB_PORT` / `DB_PORT` in `.env` are the escape hatch and
  must be obvious in the docs.
- **Django 4.0.1 on Python 3.12.** The project already runs this combination on
  Vercel (`python3.12`) and `.python-version` pins `3.12`, but Django 4.0
  predates official 3.12 support. The image mirrors what production runs; if the
  build fails on an incompatibility, fall back to `python:3.11-slim` and record
  it in the spec.
- **Host bind-mount permissions / CRLF.** The recovered history had a fix to run
  the entrypoint via `/bin/sh` on Windows-shared folders; keep that shape.
- **Stale port references.** The recovered docs mention the old ports; only the
  files this line actually has are updated, and the regression test is the
  guard.

## Owner decision

Resolved at Accept: reuse the recovered low-conflict ports `63404` (web) and
`59075` (db), matching the local `.env`.
