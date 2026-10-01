# Tasks 002: Local Docker Compose stack

- **Status:** Accepted
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Failing test first → implement → green. Check off in order. -->

## Checklist

- [x] Spec Accepted by the project owner
- [x] Branch from `develop` (`chore/002-local-docker-compose`)
- [x] Red — `tests/test_docker_compose.py`: port-rule assertions (fails: no
      compose file yet)
- [x] Green — `docker-compose.yml`: publish `"${WEB_PORT:-63404}:8000"` and
      `"${DB_PORT:-59075}:5432"`, optional `env_file`, forced local
      `DATABASE_URL`, `db` healthcheck, `runserver` command
- [x] Green — `Dockerfile` (Python 3.12 slim) + `docker/entrypoint.sh`
- [x] Green — `.dockerignore` + `.env.example`
- [x] Green — `tests/test_docker_compose.py` passes
- [x] Red — E2E: N/A (out of scope in spec)
- [x] Green — E2E: `docker compose config` resolves with `.env` removed, then
      `docker compose up --build` serves HTTP on the published `WEB_PORT`
- [x] `README.md`: quick start prints the real app URL
- [x] Fill Traceability in `./spec.md`
- [x] Set `bump` on the ITEM and spec header (`none`)
- [x] `bump` is `none`: `VERSION` unchanged; no tag
- [x] Update ITEM + [`backlog/board.md`](../../backlog/board.md) in **this PR**
      (In review while open; Done before merge)
- [x] Conventional Commit + draft PR linking `./spec.md` (same PR; extra
      commits fine)

## Done when

- [x] All acceptance scenarios in spec.md hold
- [x] `python manage.py test` green (E2E excluded by scope)
- [x] Stack verified up on the published ports with and without `.env`
- [x] Board, tasks, and version are complete in this PR
