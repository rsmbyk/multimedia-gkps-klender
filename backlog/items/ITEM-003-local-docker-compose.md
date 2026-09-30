---
id: ITEM-003
status: in_review
title: Local Docker Compose stack on low-conflict ports
type: chore
priority: P1
effort: S
created: 2026-09-30
updated: 2026-10-01
spec: ../specs/002-local-docker-compose/spec.md
branch: chore/002-local-docker-compose
pr: 258
archived_at:
archive_reason:
bump: none
release_version:
---

# ITEM-003: Local Docker Compose stack on low-conflict ports

## Summary

There is no containerized way to run this project locally. Starting it by hand
means installing Python 3.12, a reachable PostgreSQL, and the pinned
dependencies, then supplying `DATABASE_URL` yourself. This slice adds a
`docker compose` stack — `web` (Django) plus `db` (PostgreSQL 16) — that boots
on a fresh clone with no manual `.env` copy.

The published host ports are random high numbers from the IANA dynamic range
(`49152`-`65535`), so the stack does not fight the well-known `8000` / `5432`
that other local apps and a native Postgres commonly hold. Both are overridable
per clone through `WEB_PORT` / `DB_PORT` in `.env`.

## Notes

- This capability already exists on another line of history: tag `v0.5.2`,
  branch `archive/legacy-develop` (`specs/018-local-compose-ports`,
  `ITEM-011`). It is **not** on the current `main` (the repo re-adopted
  vexbook onto a fresh line), so it is being re-introduced here, adapted to
  this line.
- Ports: `WEB_PORT=63404`, `DB_PORT=59075` (verified in the dynamic range;
  the same values already sit in the local, gitignored `.env`).
- Container-internal ports stay conventional — `web` listens on `8000`,
  Postgres on `5432`; only the published host side changes.
- `bump: none` — developer tooling only; the Vercel deploy path is unchanged.
- Recovered files (to adapt): `Dockerfile`, `docker-compose.yml`,
  `.dockerignore`, `.env.example`, `docker/entrypoint.sh`.

## Acceptance sketch

- `docker compose config` resolves on a fresh clone with no `.env`.
- `docker compose up --build` starts `db` and `web`, applies migrations, and
  answers over HTTP on the published `WEB_PORT`.
- Both published ports are in `49152`-`65535` and neither is `8000` nor `5432`.
- A collision is recoverable via `WEB_PORT` / `DB_PORT` in `.env`, with no edit
  to tracked files.

## Links

- Spec: [`specs/002-local-docker-compose/spec.md`](../specs/002-local-docker-compose/spec.md)
- Related items: ITEM-000 (process adoption)
- Related history: `specs/018-local-compose-ports` @ `v0.5.2` (archived line)
