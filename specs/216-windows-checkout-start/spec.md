# Feature Specification: A checkout made on Windows starts the stack

**Slice**: `specs/216-windows-checkout-start`
**Branch**: `fix/216-windows-checkout-start`
**Created**: 2026-11-21
**Status**: Draft
**Input**: "when i run the ./docker/up.sh1 on windows, i got the following error (fresh docker): … Container e1cbb130… is restarting, wait until the container is running … at up.ps1:60 … exec -T media sh -c 'fc-lis…'"

## User Scenarios & Testing

### US1 — The stack starts from a checkout made on Windows (P1)

**Why this priority**: Every Windows computer builds the image from its own working tree. If git
hands that tree a CRLF copy of the entrypoint, `/bin/sh` refuses it, both `web` and `media` exit
with status 2, `restart: unless-stopped` loops them, and the first start on a fresh machine never
reaches the app. Nothing on Linux reproduces it, so it can only be fixed by making the image and the
checkout independent of how git wrote the file.

**Independent Test**: Build the image from a working tree whose `docker/entrypoint.sh` has CRLF line
endings, start the stack, and observe `web` and `media` running (not restarting) with the site
answering on the published port.

**Acceptance scenarios**

1. **Given** a checkout whose `docker/entrypoint.sh` carries CRLF line endings, **When** the image is
   built and the stack started, **Then** the entrypoint runs to its `exec "$@"` and the `web` and
   `media` services stay up.
2. **Given** a checkout made with `core.autocrlf=true` (Git for Windows' default), **When** the files
   are inspected, **Then** the shell scripts in `docker/` are LF, because the repository pins them.
3. **Given** the same checkout, **When** `docker compose up` is run without the launcher, **Then** the
   stack still starts — the fix is not carried by `up.ps1` alone.

### US2 — A launcher start reports a companion it cannot inspect (P2)

**Why this priority**: The post-start font check is the launcher's only evidence that the mounts are
real. Today it runs under `$ErrorActionPreference = 'Stop'`, so when the companion is not running the
launcher dies with a `NativeCommandError` trace instead of its own message — the operator reads a
PowerShell stack trace where the answer ("the companion is restarting") should be.

**Independent Test**: Point the launcher at a stack whose `media` container is restarting and observe
one line naming the likely cause, with the launcher's exit status still `up`'s.

**Acceptance scenarios**

1. **Given** a start that succeeded and a `media` container that is restarting, **When** the launcher
   reaches its post-start check, **Then** it prints a line naming the companion as not running and
   pointing at `docker compose logs media`, and exits with the status `up` returned.
2. **Given** a start that succeeded and a running companion with no visible mounted font, **When** the
   check runs, **Then** the existing File-Sharing message is printed, unchanged.
3. **Given** a start that failed, **When** the launcher finishes, **Then** no check runs and the
   failing status is what it exits with.

### Edge Cases

- **When** a checkout predates the new `.gitattributes` rule and already holds a CRLF
  `docker/entrypoint.sh`, **Then** the image still starts, because the strip happens at build time —
  no re-clone is required.
- **When** the file is `docker/up.ps1`, **Then** its CRLF line endings are correct and the pin does
  not touch it.
- **When** `docker/up.sh` is run from Git Bash on Windows, **Then** it is LF and runs, the same pin
  covering it.
- **When** the post-start check's `exec` fails for a reason other than the container restarting,
  **Then** the launcher still prints its one line and still exits with `up`'s status.
- **When** the companion is running and the mount is genuinely empty, **Then** the empty-mount
  warning is not replaced by the not-running message.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | `docker/entrypoint.sh` SHALL execute under `/bin/sh` whatever line endings the build context carries: the image strips `\r` from it before making it executable, so a CRLF checkout cannot produce a container that exits at `set -e`. | `local-stack/R4` |
| FR-002 | The repository SHALL pin LF for the shell scripts it ships — `*.sh` — in a `.gitattributes` at the repo root, so a checkout made with `core.autocrlf=true` still produces LF copies. `*.ps1` SHALL NOT be pinned. | `local-stack/R4` |
| FR-003 | The strip SHALL be in the image, not in a launcher: plain `docker compose up` on a CRLF checkout SHALL start every service, with no launcher involved. | `local-stack/R4` |
| FR-004 | `docker/up.ps1`'s post-start font check SHALL NOT abort the launcher: a failed `docker compose exec` prints one line naming the companion as not running and pointing at `docker compose logs media`, and the launcher exits with the status `up` returned. | `local-stack/R5` |
| FR-005 | The check SHALL keep its present behaviour when the `exec` succeeds: a companion that sees no mounted font prints the File-Sharing message, and a companion that sees at least one mounted font prints nothing. | `local-stack/R5` |
| FR-006 | `docker/up.sh` SHALL behave identically to `docker/up.ps1` on both branches of the check — the two launchers keep one command contract. | `local-stack/R5` |
| FR-007 | The post-start check SHALL never change the exit status of the start it follows: a failed check is a report, and a start that failed exits with its own failing status because no check runs after it. | `local-stack/R5` |

### Key Entities

None — the change is a build step, a repository attribute file and the two launchers' report path.
No models, no stored state.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | A CRLF `docker/entrypoint.sh` in the build context reaches `exec "$@"` | In the built image: `sh -c 'printf "x\r\nset -e\r\nexec "$@"" …'` — the shipped file is copied to `/tmp/e.sh` with CRLF endings and run with `sh /tmp/e.sh true`, exiting 0 (today: exit 2, `set: Illegal option -`) |
| SC-002 | The shell scripts are pinned to LF | `git check-attr eol -- docker/entrypoint.sh docker/up.sh` reports `eol: lf` for both, and `git check-attr eol -- docker/up.ps1` reports `unspecified` |
| SC-003 | A dead companion no longer kills the launcher | `pwsh`-free inspection of the check block: the `exec` is invoked so a non-zero status is captured, the message names `docker compose logs media`, and `exit $status` uses the status of `up` |
| SC-004 | The launchers still agree | `tests/test_launcher_fonts.py` passes, and the two launchers' check blocks differ only in syntax |

## UI/UX

`n/a — the slice changes the launcher's terminal transcript and the image's entrypoint; no screen changes. The transcript itself is asserted by tests/test_launcher_fonts.py rather than previewed.`

## Assumptions

- Git for Windows' default `core.autocrlf=true` is what produced the CRLF file in the report; a
  checkout made with `core.autocrlf=input` or `false` already holds LF, and neither fix changes
  anything there.
- The strip belongs in the `Dockerfile` rather than in a launcher because the launcher is optional by
  `local-stack/R1` — a computer without the script is not a broken computer.
- The attribute pins `*.sh` only. Pinning the whole tree (`* text=auto eol=lf`) would rewrite every
  file in an existing Windows checkout, so the fix would arrive as a thousand-file diff in `git
  status` on the machine it is meant to help.
- The post-start check stays advisory: its purpose is to tell the operator something they cannot see
  from outside the container, never to fail a start that Docker reported as successful.
- The two failure messages are distinguished because they send the operator to different places:
  `docker compose logs media` for a container that is not running, Docker's File-Sharing settings for
  a running container whose mount is empty.
- `local-stack/R2` owns *what* the post-start check says about an empty mount; `R5` owns only that the
  message is reachable — that a check which cannot run reports instead of aborting the launcher.
- The reported checkout predates `spec 192`'s launcher (the check sits at `up.ps1:60`); the slice
  fixes the launchers as they stand on `develop`, and the operator's older checkout picks the fix up
  by pulling.

## Clarifications

### Session 2026-11-21

- Q: Does the launcher's post-start check stay advisory, or should a companion that is not running
  fail the start? → A: advisory — it reports and never changes `up`'s exit status (FR-004, FR-007).
- Q: Should `.gitattributes` pin the whole tree to LF or only the shell scripts? → A: `*.sh` only;
  `*.ps1` keeps its CRLF (FR-002).

No `[NEEDS CLARIFICATION]` markers remain.
