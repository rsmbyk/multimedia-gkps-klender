# Tasks: Stack Restart Policy

**Slice**: `specs/191-compose-restart` · **Created**: 2026-11-14 · Ordering per SDD-16; `[P]`
means order-independent, not concurrent.

## Setup

- No task — the branch (`feat/191-compose-restart`) and the spec pack were cut at the change
  request per C-SDD-GIT; nothing remains to set up.

## US1 — The stack returns after a machine restart

- [x] T001 [US1] Write the failing test `DockerComposeRestartPolicyTests.test_web_and_db_restart_on_daemon_restart` in `tests/test_docker_compose.py`: it asserts `web` and `db` declare `restart: unless-stopped` and fails today because neither service carries the key (C-SDD-TDD handoff for FR-001/FR-002).
- [x] T002 [US1] Make it pass: add `restart: unless-stopped` to the `web` and `db` service blocks in `docker-compose.yml`, placed as `media` places its own.
- [x] T003 [US1] `manual` — US1/SC-001 proof: restart the Docker daemon (Docker Desktop restart or reboot); `docker ps` shows web/db/media `Up` and the site answers `200` on the published web port (quickstart step 3).

## US2 — A deliberately stopped stack stays stopped

- [x] T004 [US2] `manual` — US2 proof: `docker compose stop`, restart the daemon, no service starts itself (quickstart step 4).

## Polish

- [x] T005 [Polish] Fold: add R3 to `docs/spec/local-stack.md` as a typed `added` delta with its scenarios; write `fold.md` (capabilities touched, operations, before/after counts).
- [x] T006 [Polish] First commit at Fold — spec pack, `docker-compose.yml`, test, card and board row together, targeted suite green (`tests.test_docker_compose`; full suite runs before the push per the owner's standing practice).
- [x] T007 [Polish] Delivery: PR opened as a draft with the owner's word to deliver (push is GIT-07's, not assumed); card to `In review` in a commit after the PR number exists; `VERSION` → 1.29.1 and the `CHANGELOG.md` Fixed line in the pre-merge commit; `bump: patch` on the card.
