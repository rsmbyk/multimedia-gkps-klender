---
id: ITEM-011
status: done
title: 'Local Compose on random low-conflict ports'
type: chore
priority: P1
effort: S
created: 2026-09-30
updated: 2026-09-30
spec: 018-local-compose-ports
branch: feat/018-local-compose-ports
pr: 253
archived_at:
archive_reason:
bump: patch
release_version: 0.5.2
---

# ITEM-011: Local Compose on random low-conflict ports

## Summary

The local Compose stack publishes `web` on `8000` and `db` on `5432` — the two
most contended ports on a developer machine. This host already runs other
Compose projects, and a Windows-native Postgres commonly owns `5432`, so the
stack fails to start on a conflict with no remedy short of editing a tracked
file.

Move both published ports to random values from the IANA dynamic range
(`49152`-`65535`), overridable per clone via `WEB_PORT` / `DB_PORT` in `.env`.
Two related defects get fixed in the same pass: `.env` is currently a hard
requirement (so a fresh clone cannot start the stack at all), and the host
pytest DSN points at a port the stack never published.

## Notes

- Chosen after verifying both are free on this host (no listening sockets, no
  other container publishing them): web `63404`, db `59075`.
- Container-internal ports are unchanged — `web` still listens on `8000`,
  Postgres on `5432`, and the in-network `DATABASE_URL` still uses `db:5432`.
- The shared DSN default lives in `multimedia/env.py`, which is already
  importable before Django settings load, so `conftest.py` and
  `multimedia/settings_test.py` can read the same constant.
- Fixing the DSN drift means host-side `pytest` works on Linux with no SSH
  tunnel; the Windows `docker-vm` instructions in `docs/TDD.md` stay valid with
  corrected numbers.
- Spec: [018](../../specs/018-local-compose-ports/spec.md).

## Acceptance sketch

- `docker compose config` resolves on a fresh clone with no `.env`.
- Both published ports are in `49152`-`65535`, neither is `8000` or `5432`, and
  the app answers over HTTP on the published `WEB_PORT`.
- A collision is fixable via `WEB_PORT` / `DB_PORT` in `.env`, with no edit to
  tracked files.
- The default host pytest DSN port equals the published `DB_PORT`, from one
  shared constant.
- `pytest` and `npm test` pass.

## Links

- Spec: [018](../../specs/018-local-compose-ports/spec.md)
- Related items: ITEM-004 (CI for pytest and npm test — will consume the same
  published port)
- Related specs: [015](../../specs/015-deploy-local/spec.md) (`DEPLOY-LOCAL-AC4`
  names the old `127.0.0.1:8000`), [017](../../specs/017-test-coverage/spec.md)
  (`TEST-COV-AC1` defers the host port to `docs/TDD.md`)
