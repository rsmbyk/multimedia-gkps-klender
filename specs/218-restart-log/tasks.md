# Tasks: a dead companion says why

**Slice**: `specs/218-restart-log` · **Created**: 2026-11-21 · `[P]` means order-independent.

## Setup

- No task — the branch and worktree were cut at the change request (C-SDD-GIT).

## US1 — A start whose companion is dying prints the companion's own line

- [x] T001 [US1] Write the failing test `test_a_companion_that_is_not_running_shows_its_own_last_line` in `tests/test_launcher_fonts.py`: the stub answers `up` 0, `exec` 125 and `logs` with the entrypoint's line; the launcher must print that line and `docker compose build` (C-SDD-TDD handoff for FR-001/FR-002).
- [x] T002 [US1] Make it pass: in `docker/up.sh`'s not-running branch, fetch `docker compose … logs --no-color --tail 1 media` inside the guarded block and print it, then the rebuild hint (FR-003/FR-004 hold by construction).
- [x] T003 [P] [US1] Write `test_a_running_companion_is_not_asked_for_its_log`: a healthy companion produces no `logs` call and no extra output (FR-004).
- [x] T004 [US1] Mirror the block in `docker/up.ps1` inside the `'Continue'` window, with `Select-Object -Last 1` (FR-006).
- [x] T005 [US1] `inspection` — FR-006 and the long-line edge: the two blocks print the same three lines, and the log line is passed through whole.
- [x] T006 [US1] `manual` — SC-004: `docker compose logs --no-color --tail 1 media` on the running stack answers one line.

## Polish

- [x] T007 [Polish] Fold: modify `local-stack/R5` — the report now shows the companion's own last line
  and names the rebuild.
- [ ] T008 [Polish] Delivery: PR, card `In review`, `VERSION` → `1.36.4` with the changelog line, card
  `Done`.
