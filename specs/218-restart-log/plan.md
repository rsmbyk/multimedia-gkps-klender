# Implementation Plan: a dead companion says why

**Spec**: `specs/218-restart-log/spec.md`
**Branch**: `fix/218-restart-log`
**Bump**: `patch` (`1.36.3` → `1.36.4`)
**Preview**: `n/a — the launcher's terminal transcript; no product surface`

## Technical Context

| Field | Value |
| --- | --- |
| Language / version | POSIX `sh` (`docker/up.sh`), Windows PowerShell 5.1 (`docker/up.ps1`), Python 3.12 for the tests |
| Primary dependencies | none new — `docker compose logs` is already used by the operator |
| Existing patterns | `tests/test_launcher_fonts.py` drives `up.sh` through a stubbed `docker` on `PATH`; `up.ps1` is verified by inspection |
| Storage | none |
| Testing | `tests/test_launcher_fonts.py::LauncherPostStartCheckTests`, two new tests |
| Constraints | the check is advisory (`local-stack/R5`): it never changes the start's exit status |
| Scale / scope | 2 launchers, ~6 lines each, 2 tests |

## Constitution Check

No `CONSTITUTION.md` — nothing to check (SDD-01).

## Phase 0 — Research

Decision: read the companion's own last log line instead of comparing the image's age against the
`Dockerfile`. Rationale: `docker image inspect` timestamps differ from filesystem mtimes in format and
timezone, and converting them needs GNU `date -d` (absent on macOS) or a PowerShell parse — a
three-shell fragility for a guess. The log line is the failure itself. Alternative rejected: `up -d
--build` by default, which puts a LibreOffice install in front of every start.

**Unknowns remaining: 0.**

## Phase 1 — Design

- `data-model.md` · `contracts/none.md` — explicitly none.
- `quickstart.md` — the commands that demonstrate each row.

### Design notes

- `up.sh`: the not-running branch fetches the line inside the same guarded block, so `set -e` cannot
  abort on a failed `logs`, and prints it with a `gkps: its last line: ` prefix.
- `up.ps1`: both calls run under the existing `$ErrorActionPreference = 'Continue'` window, which is
  extended to cover the `logs` call; `Select-Object -Last 1` takes the line.
- The hint text is shared verbatim: `gkps: see docker compose logs media; if the image predates your
  checkout, docker compose build`.

## Traceability

| Requirement | Component / file | Verified by | Notes |
| --- | --- | --- | --- |
| FR-001 (the companion's last line) | `docker/up.sh`, `docker/up.ps1` | `test` → `tests/test_launcher_fonts.py::LauncherPostStartCheckTests::test_a_companion_that_is_not_running_shows_its_own_last_line` | `up.ps1` half by inspection in the same row |
| FR-002 (names `docker compose build`) | both | `test` → same function | |
| FR-003 (empty log omits the line) | `docker/up.sh` | `test` → `…::test_a_companion_that_is_not_running_is_reported` (stub answers no log) | asserts the message without a stray blank line |
| FR-004 (no log when healthy or when the start failed) | both | `test` → `…::test_a_running_companion_is_not_asked_for_its_log`, `…::test_a_failed_start_runs_no_check` | |
| FR-005 (exit status unchanged) | both | `test` → `…::test_a_failed_check_keeps_the_start_status` | |
| FR-006 (the launchers agree) | both | `inspection` — read the two blocks side by side; the three lines are identical | |
| SC-001..003 | the module | `test` — the rows above | |
| SC-004 (the command is valid) | real stack | `manual` — `docker compose logs --no-color --tail 1 media` answers one line | run against the running stack |
| Edge: long line | both | `inspection` — the line is printed whole, no truncation | |
| Edge: empty-mount path untouched | `docker/up.sh` | `test` → `…::test_a_running_companion_with_no_mounted_font_keeps_the_file_sharing_message` | |

**Verification split**: `6 test · 3 inspection · 1 manual`.

## Complexity Tracking

| Violation | Why needed | Simpler alternative rejected because |
| --- | --- | --- |
| — | — | — |

## Project Structure

```
docker/up.sh        (the not-running branch reads and prints the companion's last line)
docker/up.ps1       (same, inside the Continue window)
tests/test_launcher_fonts.py   (stub gains a logs answer; two tests)
docs/spec/local-stack.md       (Fold: R5 modified)
backlog/board.md, backlog/items/ITEM-233-stale-image-signal.md
CHANGELOG.md, VERSION
```