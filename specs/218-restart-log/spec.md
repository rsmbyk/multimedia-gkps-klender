# Feature Specification: A dead companion says why

**Slice**: `specs/218-restart-log`
**Branch**: `fix/218-restart-log`
**Created**: 2026-11-21
**Status**: Draft
**Input**: "go" — proceed with `ITEM-233`, the stale-image trap that made a correct fix look broken.

## User Scenarios & Testing

### US1 — A start whose companion is dying prints the companion's own line (P1)

**Why this priority**: Two failures in a row reached the operator as `Container … is restarting`, a
message that names nothing. The launcher already knows the companion is unreachable; the reason was
one command away (`docker compose logs --tail 1 media`), and it is the difference between "the stack is
broken" and "`set: Illegal option -`, rebuild".

**Independent Test**: Drive the launcher with a stub whose `up` succeeds, whose `exec` fails, and whose
`logs` answers the entrypoint's line; observe that line in the launcher's output.

**Acceptance scenarios**

1. **Given** a start that succeeded and a companion that is not running, **When** the check runs,
   **Then** the launcher prints the not-running line, the companion's last log line, and a line naming
   `docker compose build`.
2. **Given** the companion prints nothing (it never started), **When** the check runs, **Then** the
   launcher omits the log line and still prints the other two.
3. **Given** a companion that answers the check, **When** the launcher finishes, **Then** it asks for
   no log and prints nothing extra.

### Edge Cases

- **When** the start itself failed, **Then** no check and no log are requested, and the start's status
  is what the launcher exits with.
- **When** the log line is long, **Then** it is printed as one line, unmodified — truncating it would
  remove the end of the message, which is where the cause usually sits.
- **When** the companion is running and sees no mounted font, **Then** the existing File-Sharing
  message is unchanged and no log is requested.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | When the post-start check cannot reach the companion, both launchers SHALL print the companion's last log line (`docker compose logs --no-color --tail 1 media`), prefixed so it is distinguishable from the launcher's own lines. | `local-stack/R5` |
| FR-002 | The launchers SHALL name `docker compose build` in that report, because an image older than the checkout reproduces the previous failure exactly. | `local-stack/R5` |
| FR-003 | An empty log SHALL omit that line rather than print a blank one. | `local-stack/R5` |
| FR-004 | The log SHALL NOT be requested when the check succeeds or when the start failed. | `local-stack/R5` |
| FR-005 | The report SHALL NOT change the exit status of the start (unchanged from `R5`). | `local-stack/R5` |
| FR-006 | `up.sh` and `up.ps1` SHALL behave identically. | `local-stack/R5` |

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | The companion's line reaches the operator | `tests/test_launcher_fonts.py::LauncherPostStartCheckTests::test_a_companion_that_is_not_running_shows_its_own_last_line` — the stubbed line and `docker compose build` both appear in stderr |
| SC-002 | A healthy companion is not asked | `…::test_a_running_companion_is_not_asked_for_its_log` — no `logs` call in the stub's log |
| SC-003 | A failed start still runs nothing | `…::test_a_failed_start_runs_no_check` stays green |
| SC-004 | The command is valid against the real stack | `docker compose logs --no-color --tail 1 media` answers a line on the running stack |

## UI/UX

`n/a — the launcher's terminal transcript only; no product surface changes. The transcript is asserted by tests/test_launcher_fonts.py.`

## Assumptions

- The stale-image case is not detected by timestamp — that comparison is fragile across macOS, Linux
  and PowerShell, and it would be a guess. The companion's own log line is exact evidence and covers
  every cause, not only this one.
- The log line is printed verbatim, including compose's `media-1  |` prefix: rewriting it would be the
  launcher implying what it saw rather than showing it.
- One line, not the whole log: the operator has `docker compose logs media` named on the same screen.
- The hint names the rebuild rather than performing it, because a build costs the LibreOffice install
  and the operator may be starting a stack they did not pull.

## Clarifications

### Session 2026-11-21

- Q: Should the stale-image case be detected (image age vs `Dockerfile`) rather than inferred from a
  dead companion? → A: no — the timestamp comparison is fragile in three shells; the log line is
  exact and covers every cause. Recorded as the first assumption.
- Gates 1 and 2 were presented together at the owner's "go", which authorised this small slice
  end to end; the record of that is this section rather than two separate acceptances.

No `[NEEDS CLARIFICATION]` markers remain.