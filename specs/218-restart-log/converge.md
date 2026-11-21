# Converge: a dead companion says why

**Slice**: `specs/218-restart-log` · **Run**: 2026-11-21

## Pass 1

| Row | Method | Evidence | Outcome |
| --- | --- | --- | --- |
| FR-001 (the companion's last line) | `test` | `LauncherPostStartCheckTests::test_a_companion_that_is_not_running_shows_its_own_last_line` — stubbed line appears in stderr | matched |
| FR-002 (names `docker compose build`) | `test` | same function | matched |
| FR-003 (empty log omits the line) | `test` | `…::test_a_companion_that_is_not_running_is_reported` — stub answers no log, message set is complete without a blank line | matched (see analysis A-01) |
| FR-004 (no log when healthy or failed) | `test` | `…::test_a_running_companion_is_not_asked_for_its_log` (no ` logs ` call), `…::test_a_failed_start_runs_no_check` | matched |
| FR-005 (exit status unchanged) | `test` | `…::test_a_failed_check_keeps_the_start_status` — exec 125, launcher exits 0 | matched |
| FR-006 (launchers agree) | `inspection` | `docker/up.sh:126–138` and `docker/up.ps1:79–97` print the same three lines; the PowerShell block runs both calls inside the saved `'Continue'` window | matched |
| SC-001..003 | `test` | the rows above | matched |
| SC-004 (the command is valid) | `manual` | `docker compose logs --no-color --tail 1 media` on the running stack → one line, `media-1  | 172.20.0.1 …` | matched |
| Edge: long line | `inspection` | the value is interpolated whole; no truncation exists in either launcher | matched |
| Edge: empty-mount path untouched | `test` | `…::test_a_running_companion_with_no_mounted_font_keeps_the_file_sharing_message` | matched |

### Findings

| ID | Type | Finding | Outcome |
| --- | --- | --- | --- |
| C-01 | `unrequested` | The log line is printed with compose's own `media-1  |` prefix rather than stripped. | **Kept.** The spec's assumption says the launcher shows what it saw; stripping would be the launcher guessing at formatting. |

No `missing`, no `contradicts`. Pass 1 converged; no pass 2.

## Outcome

**Converged** in one pass, one accepted MEDIUM (analysis A-01).