# Implementation Plan: a checkout made on Windows starts the stack

**Spec**: `specs/216-windows-checkout-start/spec.md` (Accepted, Gate 1 2026-11-21)
**Branch**: `fix/216-windows-checkout-start`
**Bump**: `patch` (D005; shown at Gate 2)
**Preview**: `n/a — the launcher's terminal transcript and the image's entrypoint; no product surface, markup or stylesheet changes (spec §UI/UX)`

## Technical Context

| Field | Value |
| --- | --- |
| Language / version | `Dockerfile` (image build), POSIX `sh` (`docker/entrypoint.sh`, `docker/up.sh`), Windows PowerShell 5.1 (`docker/up.ps1`), Python 3.12 for the guard tests |
| Primary dependencies | none new — `sed` is in `python:3.12-slim-trixie`'s base, `git` is already required by every checkout |
| Existing patterns | `tests/test_docker_compose.py` pins compose-file rules with `yaml`; `tests/test_launcher_fonts.py` drives `up.sh` through a real shell with a stubbed `docker` on `PATH` and records that `up.ps1` is inspection-only |
| Storage | none — one build step, one attribute line, two report paths |
| Testing | new `tests/test_entrypoint_line_endings.py`; `tests/test_launcher_fonts.py` extended for the report path |
| Target platform | the operators' computers: Docker Desktop on Windows (the failing case) and macOS, Docker Engine on Linux |
| Project type | Django app with a local Docker Compose stack |
| Performance goals | none — the strip is one `sed` over a 597-byte file at build time |
| Constraints | the suite must stay runnable without a Docker daemon (CI has none), and no licensed font may enter the image (`local-stack/R2`) |
| Scale / scope | 3 files changed, 1 file added, ~5 tests |

## Constitution Check

No `CONSTITUTION.md` exists in this repository, so there are no principles to check against (SDD-01
makes it optional and it is never auto-created). Run before Phase 0 — nothing to check.
Re-checked after Phase 1: unchanged, still nothing to check.

## Phase 0 — Research

See `research.md`. **Unknowns remaining: 0.** Six decisions: where the strip lives (D001), the
`.gitattributes` width (D002), how the launcher's check tells a dead companion from an empty mount
(D003), that the check is advisory (D004), the bump (D005), the verification split (D006).

## Phase 1 — Design

- `data-model.md` — explicitly none: no entities, no stored state.
- `contracts/none.md` — explicitly none: the launchers keep their arguments, default command and exit
  status.
- `quickstart.md` — the commands that demonstrate every traceability row, and the one that cannot run
  here.

### Design notes

- **The strip.** `Dockerfile`, between `COPY . .` and `RUN chmod +x docker/entrypoint.sh`:
  `RUN sed -i 's/\r$//' docker/entrypoint.sh`. It reads as part of the same step that makes the file
  executable, and a file with no CR is unchanged.
- **The pin.** A new repo-root `.gitattributes` with one rule, `*.sh text eol=lf`, and a comment
  saying why `*.ps1` is absent. Nothing else in the tree is pinned (D002).
- **The check, `up.sh`.** The inner command becomes
  `sh -c 'n=$(fc-list 2>/dev/null | grep -c "/usr/share/fonts/host/"); printf "%s" "$n"; exit 0'`, so
  a non-zero `docker compose exec` status means the container, not the grep. The captured status is
  read before the output is used; a non-zero status or empty output prints the not-running line, and
  a `0` count prints the existing File-Sharing line.
- **The check, `up.ps1`.** Same command, same three branches, with `$ErrorActionPreference =
  'Continue'` around the block (PowerShell 5.1 turns a native command's stderr into a terminating
  error under `Stop`, which is what the report's trace shows) and the previous value restored
  afterwards. `$LASTEXITCODE` is read immediately after the call.
- **Neither launcher changes its exit status.** `$status` / `$?` from the compose invocation is what
  the script exits with, on every path (D004).

## Traceability

| Requirement | Component / file | Verified by | Notes |
| --- | --- | --- | --- |
| FR-001 (entrypoint runs whatever the context's line endings) | `Dockerfile` strip step | `test` → `tests/test_entrypoint_line_endings.py::test_a_crlf_entrypoint_runs_after_the_build_strip` | the test applies the Dockerfile's own `sed` to a CRLF fixture and runs `/bin/sh` on the result |
| FR-001 (placement) | `Dockerfile` | `test` → `tests/test_entrypoint_line_endings.py::test_the_strip_sits_between_the_copy_and_the_chmod` | order asserted by line number, not by presence |
| FR-002 (`*.sh` pinned, `*.ps1` not) | `.gitattributes` | `test` → `tests/test_entrypoint_line_endings.py::test_shell_scripts_are_pinned_to_lf_and_powershell_is_not` | reads `git check-attr eol`, not the file's text |
| FR-003 (the strip is in the image, not a launcher) | `Dockerfile` | `inspection` — no launcher writes `docker/entrypoint.sh`; look for `grep -rn entrypoint.sh docker/` and the `RUN` line in the `Dockerfile` | the `sed` is a build step, so plain `docker compose up` gets it |
| FR-004 (`up.ps1` reports instead of aborting) | `docker/up.ps1` | `inspection` — read the check block: `$ErrorActionPreference = 'Continue'` is set before the call, restored after, `$LASTEXITCODE` is read, the message names `docker compose logs media` | no PowerShell on this machine (D006) |
| FR-005 (a running companion with no mounted font still warns) | `docker/up.sh`, `docker/up.ps1` | `test` → `tests/test_launcher_fonts.py::LauncherPostStartCheckTests::test_a_running_companion_with_no_mounted_font_keeps_the_file_sharing_message` | `up.ps1` half by inspection in the same row's notes |
| FR-006 (`up.sh` behaves identically) | both launchers | `test` → `tests/test_launcher_fonts.py::LauncherPostStartCheckTests::test_a_companion_that_is_not_running_is_reported` | `up.ps1` half by inspection |
| FR-007 (the check never changes the exit status) | both launchers | `test` → `tests/test_launcher_fonts.py::LauncherPostStartCheckTests::test_a_failed_check_keeps_the_start_status` | the stub's `up` exits 0 while `exec` fails; the launcher must exit 0 |
| SC-001 (a CRLF checkout starts, end to end) | built image | `manual` — convert `docker/entrypoint.sh` to CRLF, `docker compose build media && docker compose up -d media`, `docker ps` shows `media` `Up` | the test row proves the strip; this proves the image |
| SC-002 (attributes) | `.gitattributes` | `test` → the FR-002 test | `lf`, `lf`, `unspecified` |
| SC-003 (a dead companion no longer kills the launcher) | `docker/up.ps1` | `inspection` — same block as FR-004; the trace's `NativeCommandError` cannot be raised | |
| SC-004 (the launchers still agree) | both launchers | `test` → the whole `tests/test_launcher_fonts.py` module stays green | |
| US1/AC1 (a CRLF checkout starts the stack) | `Dockerfile` | `manual` — the SC-001 row | |
| US1/AC2 (a `core.autocrlf=true` checkout holds LF scripts) | `.gitattributes` | `test` — the FR-002 row | |
| US1/AC3 (plain `docker compose up` still starts) | `Dockerfile` | `inspection` — the FR-003 row | |
| US2/AC1 (a restarting companion is named, status kept) | `docker/up.ps1` | `inspection` — the FR-004 row | |
| US2/AC2 (the empty-mount warning is unchanged) | `docker/up.sh` | `test` — the FR-005 row | |
| US2/AC3 (a failed start runs no check) | both launchers | `test` → `tests/test_launcher_fonts.py::LauncherPostStartCheckTests::test_a_failed_start_runs_no_check` | asserts the stub saw no `exec` |
| Edge: a checkout that predates the pin | `Dockerfile` | `test` — the FR-001 row (the fixture is CRLF whatever the repo holds) | no re-clone needed |
| Edge: `*.ps1` keeps its CRLF | `.gitattributes` | `test` — the FR-002 row (`unspecified`) | |
| Edge: `up.sh` under Git Bash | `.gitattributes` | `test` — the FR-002 row (`lf`) | |
| Edge: the exec fails for another reason | `docker/up.sh` | `test` — the FR-007 row (any non-zero status reports) | |
| Edge: a genuinely empty mount is not reported as dead | `docker/up.sh` | `test` — the FR-005 row | |

**Verification split**: `12 test · 5 inspection · 2 manual`.

## Complexity Tracking

| Violation | Why needed | Simpler alternative rejected because |
| --- | --- | --- |
| — | — | — |

## Project Structure

### Documentation

```
specs/216-windows-checkout-start/
  spec.md  plan.md  research.md  data-model.md  quickstart.md  tasks.md  analysis.md
  converge.md  fold.md
  contracts/none.md
  checklists/requirements.md
```

### Source

```
.gitattributes                     (new — *.sh text eol=lf)
Dockerfile                         (strip step before chmod +x)
docker/up.sh                       (report path, unambiguous exec status)
docker/up.ps1                      (same, without aborting under Stop)
tests/test_entrypoint_line_endings.py   (new)
tests/test_launcher_fonts.py       (extended: LauncherPostStartCheckTests)
docs/spec/local-stack.md           (Fold: R4, R5)
backlog/board.md, backlog/items/ITEM-231-windows-checkout-start.md
CHANGELOG.md, VERSION              (delivery commit)
```

### Structure Decision

No new directory: the tests join `tests/` beside the two guard modules they extend, the attribute
file sits at the repo root because `git` only honours it there, and the strip joins the `Dockerfile`
step that already makes the entrypoint executable. The launchers stay where spec 182 put them.
