# Converge: a checkout made on Windows starts the stack

**Slice**: `specs/216-windows-checkout-start` · **Run**: 2026-11-21

## Pass 1

### What was checked

Every row of Plan's traceability table, by the method it declared.

| Row | Method | Evidence | Outcome |
| --- | --- | --- | --- |
| FR-001 (the entrypoint runs whatever the context's line endings) | `test` | `tests/test_entrypoint_line_endings.py::EntrypointLineEndingTests::test_a_crlf_entrypoint_runs_after_the_build_strip` — the fixture exits 2 before the strip and reaches the command after it | matched |
| FR-001 (placement) | `test` | `…::test_the_strip_sits_between_the_copy_and_the_chmod` — `COPY . .` < strip < `chmod +x` by line number | matched |
| FR-002 (`*.sh` pinned, `*.ps1` not) | `test` | `…::CheckoutLineEndingTests::test_shell_scripts_are_pinned_to_lf_and_powershell_is_not` — `git check-attr eol` answers `lf`, `lf`, `unspecified` | matched |
| FR-003 (the strip is in the image) | `inspection` | `grep -rn entrypoint.sh docker/ Dockerfile tests/` — the only writer is `Dockerfile:42 RUN sed -i …`; no launcher names the file; `ENTRYPOINT ["/bin/sh", "docker/entrypoint.sh"]` at line 49 consumes it | matched |
| FR-004 (`up.ps1` reports instead of aborting) | `inspection` | `docker/up.ps1:76–90` — `$ErrorActionPreference` saved, set to `'Continue'` before the call, restored after; `$LASTEXITCODE` read immediately; the message names `docker compose logs media`; `exit $status` at the end | matched |
| FR-005 (a running companion with no mounted font still warns) | `test` | `tests/test_launcher_fonts.py::LauncherPostStartCheckTests::test_a_running_companion_with_no_mounted_font_keeps_the_file_sharing_message`; the `up.ps1` half read in the same inspection as FR-004 (its `elseif` branch prints the same two lines) | matched |
| FR-006 (`up.sh` behaves identically) | `test` | `…::test_a_companion_that_is_not_running_is_reported`, `…::test_a_companion_that_sees_a_mounted_font_says_nothing` | matched |
| FR-007 (the check never changes the status) | `test` | `…::test_a_failed_check_keeps_the_start_status` (exec 125, launcher exits 0), `…::test_a_failed_start_runs_no_check` (up 1, launcher exits 1, no `exec` logged) | matched |
| SC-001 (a CRLF checkout starts, end to end) | `manual` | built the image from a CRLF context — `git archive HEAD` + the slice's `Dockerfile`, `docker/entrypoint.sh` rewritten to CRLF (19 CR bytes), `docker build -t gkps216-crlf-proof .`; inside it `grep -c $'\r' /app/docker/entrypoint.sh` → `0`, and `docker run --rm gkps216-crlf-proof echo …` → exit 0, the command ran. Counterfactual: the same context with the strip line removed (`Dockerfile.nostrip`) builds to `gkps216-crlf-nostrip`, whose `docker run … echo reached` prints `docker/entrypoint.sh: 2: set: Illegal option -` and exits 2 — the report, reproduced | matched |
| SC-002 (attributes) | `test` | the FR-002 row | matched |
| SC-003 (a dead companion no longer kills the launcher) | `inspection` | the FR-004 row: no native command runs outside the `'Continue'` block, so the `NativeCommandError` in the report's trace cannot be raised | matched |
| SC-004 (the launchers still agree) | `test` | `manage.py test tests.test_entrypoint_line_endings tests.test_launcher_fonts` → 13 tests, OK | matched |
| US1/AC1 (a CRLF checkout starts the stack) | `manual` | the SC-001 row | matched |
| US1/AC2 (`core.autocrlf=true` checkout holds LF scripts) | `test` | the FR-002 row | matched |
| US1/AC3 (plain `docker compose up` still starts) | `inspection` | the FR-003 row — the strip is a `RUN` step in the image, so any compose invocation gets it | matched |
| US2/AC1 (a restarting companion is named, status kept) | `inspection` | the FR-004 row | matched |
| US2/AC2 (the empty-mount warning is unchanged) | `test` | the FR-005 row | matched |
| US2/AC3 (a failed start runs no check) | `test` | `…::test_a_failed_start_runs_no_check` | matched |
| Edge: a checkout that predates the pin | `test` | the FR-001 row — the fixture is CRLF whatever the repo holds, so no re-clone is needed | matched |
| Edge: `*.ps1` keeps its CRLF | `test` | the FR-002 row (`unspecified`) | matched |
| Edge: `up.sh` under Git Bash | `test` | the FR-002 row (`lf` for `docker/up.sh`) | matched |
| Edge: the exec fails for another reason | `test` | the FR-007 row — any non-zero status takes the not-running branch | matched |
| Edge: a genuinely empty mount is not reported as dead | `test` | the FR-005 row — `exec` 0 with `0` takes the File-Sharing branch | matched |

### Findings

| ID | Type | Finding | Evidence | Outcome |
| --- | --- | --- | --- | --- |
| C-01 | `unrequested` | The launcher tests now share a `LauncherTestCase` base (stub writing, log parsing, `run_launcher`), which the spec does not ask for. | `tests/test_launcher_fonts.py:26–58` — two classes needed the same three helpers; duplicating them would have put the stub's `exec` behaviour in two places. | **Kept, no task.** A test-support refactor that adds no behaviour; the module stays green (SC-004). |
| C-02 | `partial` | FR-005's `up.ps1` half is verified by inspection only, as declared — the row is satisfied by the method it named, not by a run. | D006; `command -v pwsh` finds nothing. | **Matched as declared.** The gap is the one already recorded in analysis A-03. |
| C-03 | `unrequested` | The strip's comment block in the `Dockerfile` runs five lines, longer than the neighbouring comments. | `Dockerfile:37–41` | **Kept.** It names the failure mode and why the strip is not in a launcher — the next reader will otherwise move it. |

No `missing` and no `contradicts` rows: every requirement, success criterion, scenario and edge case
has a matching artifact verified by the method it declared.

### Outcome

Pass 1: **converged.** 12 `test` rows green, 5 `inspection` rows read and matched, 2 `manual` rows
executed (the image proof and its counterfactual). No tasks were appended, so there is no pass 2.
