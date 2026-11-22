# Research: a checkout made on Windows starts the stack

**Spec**: `specs/216-windows-checkout-start/spec.md`
**Unknowns remaining**: 0

## D001 — The CRLF strip lives in the image, before the entrypoint is made executable

- **Decision**: `Dockerfile` gains one step between `COPY . .` and `RUN chmod +x
  docker/entrypoint.sh`: `RUN sed -i 's/\r$//' docker/entrypoint.sh`. The file is then made
  executable as today.
- **Rationale**: The failure is in the build context, so the cure has to be in the build. Measured on
  the running `media` container of the real image, a CRLF copy of the repo's own entrypoint prints
  `set: Illegal option -` and exits 2 — `set -e` becomes `set -e\r`, so `/bin/sh` stops on line 2 and
  `restart: unless-stopped` (spec 191) turns the crash into a loop. A no-CR file is unchanged by the
  command, so it is safe on every platform. `sed` is present in `python:3.12-slim-trixie`'s base.
- **Alternatives considered**: rewriting the file from a launcher — rejected, `local-stack/R1` makes
  the launcher optional, and FR-003 requires plain `docker compose up` to work; `.gitattributes`
  alone — rejected as the *only* fix, because a checkout made before the pin exists still holds CRLF
  and would need a re-clone; an `ENTRYPOINT` of `sh -c 'tr -d "\r" …'` — rejected, it hides the file
  behind a wrapper instead of fixing it, and breaks the `exec "$@"` contract `entrypoint.sh` relies on.
- **Provenance**: research (measured in the running container).

## D002 — `.gitattributes` pins `*.sh`, and only `*.sh`

- **Decision**: a repo-root `.gitattributes` carrying `*.sh text eol=lf`. `*.ps1` is deliberately
  absent.
- **Rationale**: Git for Windows' default `core.autocrlf=true` rewrites text files on checkout, and
  nothing in this repo overrode it — `git ls-files --eol docker/` reports an empty `attr/` column for
  every file. `eol=lf` on `*.sh` makes the working tree LF whatever the platform's setting is, which
  removes the cause rather than surviving it. PowerShell is the one consumer that wants CRLF, and a
  `.ps1` with LF is the kind of surprise that shows up as a broken `if` block later.
- **Alternatives considered**: `* text=auto eol=lf` repo-wide — rejected: it rewrites every text file
  in an existing Windows checkout, so the fix arrives as a whole-tree `git status` on the machine it
  is meant to help, and it would touch Markdown, Python and CSS in one slice; pinning nothing and
  relying on D001 — rejected as the only fix, because it leaves the working tree wrong for anything
  else that runs a shipped script (Git Bash running `docker/up.sh`).
- **Provenance**: `owner decision` (asked at Clarify, 2026-11-21); research for the mechanism.

## D003 — The launcher's check makes "exec failed" unambiguous, then reports instead of aborting

- **Decision**: both launchers run the count through a command that always exits 0 —
  `sh -c 'n=$(fc-list 2>/dev/null | grep -c "/usr/share/fonts/host/"); printf "%s" "$n"; exit 0'` —
  and treat a non-zero `docker compose exec` status (or empty output) as *the companion is not
  running*, printed as one line naming `docker compose logs media`. A zero count with a zero status
  keeps the existing File-Sharing message. `up.ps1` runs that block with
  `$ErrorActionPreference = 'Continue'` so PowerShell 5.1 does not turn the native stderr into a
  terminating `NativeCommandError`.
- **Rationale**: the current command is ambiguous — `grep -c` exits 1 both when it matched nothing
  *and* when the container is gone, so the launcher cannot tell a dead companion from a companion
  with no mounted font, which is exactly the distinction the two messages exist for. Making the inner
  command succeed always moves the exit status back to where it belongs: compose. The PowerShell
  abort is reproducible from the report itself — the trace names `NativeCommandError` at the `exec`
  line, so the check ran with `$ErrorActionPreference = 'Stop'` in force and threw.
- **Alternatives considered**: keeping the command and parsing compose's stderr for
  "is restarting" — rejected: string-matching a daemon message, in two launchers, in two shells;
  `try { … } catch { … }` alone — rejected: it catches the PowerShell error but still cannot tell a
  zero count from a dead container, so the File-Sharing message would fire on a dead companion;
  dropping the check — rejected, it is the only evidence that a mount is real (spec 182).
- **Provenance**: research (report trace + `grep -c` exit-status semantics), owner decision on the
  advisory shape.

## D004 — The check never changes the start's exit status

- **Decision**: `up.sh` and `up.ps1` keep `$status` / `$?` from the compose invocation and `exit`
  with it; the check's own status is discarded.
- **Rationale**: the check exists to tell the operator something they cannot see from outside the
  container. A start Docker reported as successful is successful; a check that fails to *look* is not
  evidence the start failed, and turning it into a non-zero exit would make `up.sh && next-step`
  scripts stop on a font warning.
- **Alternatives considered**: failing the start on a dead companion — rejected by the owner at
  Clarify (2026-11-21); the crash that motivated this slice would then still be reported as a failure,
  but by a launcher that has already started the stack.
- **Provenance**: `owner decision` (Clarify, 2026-11-21).

## D005 — Bump: `patch`

- **Decision**: `1.36.1` → `1.36.2`.
- **Rationale**: a defect that stops the stack starting on one platform, fixed with no new capability
  for the operator and no interface change (`VER-10`). The two capability requirements it adds are
  statements of behaviour that already had to hold.
- **Alternatives considered**: `minor` — rejected: nothing new is offered to a user who already had a
  working stack.
- **Provenance**: research. `VERSION` read `1.36.0` when the plan was written; spec 214's slice merged
  into `develop` while this one was open and took `1.36.1`, so the number was re-read before the
  delivery commit and moved to the next free patch — the collision the versioning rules exist for.

## D006 — Verification split: the image is tested by command, the `.ps1` by inspection

- **Decision**: FR-001/002/003 and the `up.sh` half of FR-005/006/007 are `test`; the `up.ps1` half is
  `inspection`; the built-image run of SC-001 is `manual`.
- **Rationale**: PowerShell is not installed on the development machine (`command -v pwsh` finds
  nothing), and the suite must stay runnable — `tests/test_launcher_fonts.py` already records exactly
  this split for `up.ps1` ("verified by inspection"). The Dockerfile strip can be proven without a
  daemon by applying the same `sed` to a CRLF fixture in a temporary directory and running `/bin/sh`
  on the result, which is the behaviour, not the line's presence. CI has no Docker daemon, so a
  build-and-run test would be a test that never runs.
- **Alternatives considered**: a test that builds the image — rejected, no daemon in CI and a
  LibreOffice build per run; asserting only that the `sed` line exists — rejected as too weak on its
  own, so the placement assertion and the behaviour assertion are both present.
- **Provenance**: research (`command -v pwsh`, the existing launcher test's docstring).

## Open

<!-- empty — Phase 0 finished -->
