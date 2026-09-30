# Tasks 018: Local Compose ports

- **Status:** Accepted
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Failing test first → implement → green. Check off in order. -->

## Checklist

- [x] Spec Accepted by the project owner
- [x] Branch from the current base (`feat/018-local-compose-ports`)
- [x] Red — `tests/test_toolchain.py`: assert the DSN port equals the shared
  `multimedia.env.DEFAULT_DB_HOST_PORT` (fails: constant does not exist yet)
- [x] Green — `multimedia/env.py`: add `DEFAULT_DB_HOST_PORT` +
  `DEFAULT_TEST_DATABASE_URL`
- [x] Green — `conftest.py` and `multimedia/settings_test.py`: import the shared
  default instead of repeating the literal DSN
- [x] Green — `tests/test_toolchain.py`: honor an explicit `TEST_DATABASE_URL`
  override in the assertion
- [x] `docker-compose.yml`: publish `"${WEB_PORT:-63404}:8000"` and
  `"${DB_PORT:-59075}:5432"`; make `env_file: .env` optional
- [x] `docker-compose.yml`: add a `DJANGO_ALLOWED_HOSTS` default that `.env`
  still overrides
- [x] `.env.example`: document `WEB_PORT` / `DB_PORT` and the app URL
- [x] Red — E2E: N/A (out of scope in spec)
- [x] Green — E2E: `docker compose config` resolves with `.env` removed, then
  `docker compose up --build` serves HTTP on the published `WEB_PORT`
- [x] `README.md`: quick start prints the real app URL
- [x] `docs/TDD.md`: update the test DSN and correct the Windows `docker-vm`
  tunnel numbers; state that this host still needs a 3.10/3.11 interpreter
- [x] `specs/015-deploy-local/`: additive note that `DEPLOY-LOCAL-AC4`'s
  `127.0.0.1:8000` is superseded by spec 018 (preserve the migrated EARS body)
- [x] `specs/README.md`: index row for 018
- [x] Fill Traceability in `./spec.md`
- [x] Re-grep the repo for stale `5433` / `8000` / `5432` references
- [x] Set `bump` on the ITEM and spec header
- [x] Bump is `patch`: `VERSION` `0.5.1` → `0.5.2`, add `CHANGELOG.md`
  `## [0.5.2]`, and set `release_version` on ITEM-011 — all in **this PR**
- [x] Update ITEM + [`backlog/board.md`](../../backlog/board.md) in **this PR**
  (In review while open; Done before merge)
- [x] Conventional Commit + draft PR linking `./spec.md` (same PR; extra commits
  fine)

## Done when

- [x] All acceptance scenarios in spec.md hold
- [x] `pytest` and `npm test` green
- [x] Stack verified up on the published ports with and without `.env`
- [x] Board, tasks, and version are complete in this PR
