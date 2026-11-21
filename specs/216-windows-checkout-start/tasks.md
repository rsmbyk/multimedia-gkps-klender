# Tasks: a checkout made on Windows starts the stack

**Slice**: `specs/216-windows-checkout-start` · **Created**: 2026-11-21 · Ordering per SDD-16; `[P]`
means order-independent, not concurrent.

## Setup

- No task — the branch (`fix/216-windows-checkout-start`), the worktree and the spec pack were cut at
  the change request per C-SDD-GIT.

## US1 — The stack starts from a checkout made on Windows

**Goal**: a CRLF `docker/entrypoint.sh` in the build context still reaches `exec "$@"`, and the
repository pins its shell scripts so a Windows checkout holds LF in the first place.

**Independent test**: build `media` from a working tree whose `docker/entrypoint.sh` has CRLF
endings, start it, and see `Up` rather than `Restarting`.

- [x] T001 [US1] Write the failing test `test_a_crlf_entrypoint_runs_after_the_build_strip` in `tests/test_entrypoint_line_endings.py`: build a CRLF copy of `docker/entrypoint.sh` in a temp dir, apply the `sed` command the `Dockerfile` carries, run `/bin/sh <file> true`, assert exit 0 and the marker reached the command. Fails today — the `Dockerfile` carries no strip step to read (C-SDD-TDD handoff for FR-001/SC-001).
- [x] T002 [US1] Make it pass: add `RUN sed -i 's/\r$//' docker/entrypoint.sh` to `Dockerfile`, between `COPY . .` and `RUN chmod +x docker/entrypoint.sh`.
- [x] T003 [P] [US1] Write the failing test `test_the_strip_sits_between_the_copy_and_the_chmod` in the same module: the strip line's number is greater than `COPY . .`'s and smaller than `chmod +x docker/entrypoint.sh`'s (FR-001 placement, FR-003).
- [x] T004 [P] [US1] Write the failing test `test_shell_scripts_are_pinned_to_lf_and_powershell_is_not` in the same module: `git check-attr eol` reports `lf` for `docker/entrypoint.sh` and `docker/up.sh`, `unspecified` for `docker/up.ps1` (FR-002, SC-002).
- [x] T005 [US1] Make it pass: add the repo-root `.gitattributes` carrying `*.sh text eol=lf` and a comment saying why `*.ps1` is absent.
- [x] T006 [US1] `inspection` — FR-003/US1-AC3: confirm nothing in `docker/` rewrites `docker/entrypoint.sh` (`grep -rn entrypoint.sh docker/`) and that the strip is a `RUN` step, so plain `docker compose up` carries it.
- [x] T007 [US1] `manual` — SC-001/US1-AC1 end to end: convert `docker/entrypoint.sh` to CRLF in the working tree, `docker compose build media && docker compose up -d media`, `docker ps` shows `media` `Up`; restore the file afterwards.

## US2 — A launcher start reports a companion it cannot inspect

**Goal**: a failed post-start check prints one line naming the companion, and never changes the exit
status of the start it follows.

**Independent test**: run `up.sh` against a stub whose `up` succeeds and whose `exec` fails; one line,
exit 0.

- [x] T008 [P] [US2] Write the failing test `test_a_companion_that_is_not_running_is_reported` in `tests/test_launcher_fonts.py::LauncherPostStartCheckTests`: the stub answers `up` with 0 and `exec` with 125 plus a daemon error; assert the launcher prints the not-running line naming `docker compose logs media` and does not print the File-Sharing line (FR-004, FR-006).
- [x] T009 [US2] Make it pass: in `docker/up.sh`, run the count through a command that always exits 0, capture the `exec` status before using the output, and branch three ways (dead companion · zero fonts · at least one font).
- [x] T010 [P] [US2] Write the failing test `test_a_running_companion_with_no_mounted_font_keeps_the_file_sharing_message` in the same class: `exec` answers 0 with `0`; assert the existing File-Sharing message and no not-running line (FR-005, edge case).
- [x] T011 [P] [US2] Write the failing test `test_a_failed_check_keeps_the_start_status`: `up` answers 0 while `exec` fails; assert the launcher exits 0 (FR-007).
- [x] T012 [P] [US2] Write the failing test `test_a_failed_start_runs_no_check`: `up` answers 1; assert the launcher exits 1 and the stub logged no `exec` call (FR-007, US2-AC3).
- [x] T013 [US2] Mirror the same three branches in `docker/up.ps1`, with `$ErrorActionPreference = 'Continue'` around the block and `$LASTEXITCODE` read immediately after the call.
- [x] T014 [US2] `inspection` — FR-004/SC-003/US2-AC1: read the `up.ps1` check block and confirm the `NativeCommandError` of the report cannot be raised, that the restored preference is `Stop`, and that `exit $status` still uses `up`'s status.

## Polish

- [x] T015 [Polish] Fold: add `R4` and `R5` to `docs/spec/local-stack.md` as typed `added` deltas with their scenarios; write `fold.md` (capabilities touched, operations, before/after counts).
- [x] T016 [Polish] First commit at Fold — spec pack, `.gitattributes`, `Dockerfile`, both launchers, both test modules, card and board row together, targeted suite green (`tests.test_entrypoint_line_endings tests.test_launcher_fonts`; the full suite runs before the push per the owner's standing practice).
- [x] T017 [Polish] Delivery: PR opened as a draft with the owner's word to deliver (push is GIT-07's, not assumed); card to `In review` in a commit after the PR number exists; `VERSION` → `1.36.2` and the `CHANGELOG.md` Fixed line in the pre-merge commit; `bump: patch` on the card.

## Convergence

<!-- written by Converge only; absent until it runs -->
