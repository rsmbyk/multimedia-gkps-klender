# Converge: the runtime entrypoint survives the bind mount

**Slice**: `specs/217-entrypoint-shadowed` · **Run**: 2026-11-21

## Pass 1

### What was checked

Every row of Plan's traceability table, by the method it declared.

| Row | Method | Evidence | Outcome |
| --- | --- | --- | --- |
| FR-001 (entrypoint outside `/app`) | `test` | `tests/test_runtime_entrypoint.py::RuntimeEntrypointPathTests::test_the_runtime_entrypoint_lives_outside_the_mounted_tree` — the `COPY` target is `/usr/local/bin/gkps-entrypoint.sh`, does not begin `/app/`, and is the path the strip names | matched |
| FR-002 (strip + chmod on that copy) | `test` | `…::RuntimeEntrypointStripTests::test_the_copied_entrypoint_fails_before_the_strip` (exit 2) and `…_runs_after_the_strip` (`reached`, exit 0) | matched |
| FR-003 (`ENTRYPOINT` names it, nothing in the tree is required) | `test` | `…::test_the_image_starts_from_that_path_and_no_other` — exactly one absolute path besides `/bin/sh` | matched |
| FR-004 (`media` and `web` both start) | `manual` | image run with the CRLF checkout at `/app`: `OK`, exit 0; without the mount: `OK`, exit 0 | matched for the shape; `media`'s own start was evidenced by the operator (see A-01) |
| SC-001 (the bind-mounted shape runs) | `manual` | `docker run --rm -v <crlf-ctx>:/app gkps217-proof echo OK` → `OK`, exit 0 (the pre-fix image: exit 2, `set: Illegal option -`) | matched |
| SC-002 (path outside the mount) | `test` | the FR-001/FR-003 rows | matched |
| SC-003 (both services `Up`) | `manual` | not runnable here — port conflict with the running stack; `media` was confirmed by the operator after `--build`, `web`'s shape is the row above | **not executed on this machine**, recorded in analysis A-01 |
| US1/AC1–2 | `manual` | the SC-001 row | matched |
| US1/AC3 (an LF checkout unchanged) | `test` | `…::test_the_strip_leaves_an_lf_entrypoint_untouched` | matched |
| Edge: no bind mount | `manual` | `docker run --rm gkps217-proof echo OK` → `OK` | matched |
| Edge: a Linux checkout | `inspection` | `git check-attr eol` still answers `lf`, `lf`, `unspecified` (the narrowed module, green) | matched |
| Edge: the path inside the container | `manual` | inside the container: `/usr/local/bin/gkps-entrypoint.sh` holds 0 CR bytes while `/app/docker/entrypoint.sh` holds 19 | matched |
| Edge: contents and order unchanged | `inspection` | `git diff 0198a3c8 -- docker/entrypoint.sh` is empty | matched |

### Findings

| ID | Type | Finding | Evidence | Outcome |
| --- | --- | --- | --- | --- |
| C-01 | `partial` | SC-003 cannot be run here; its two halves are covered by the operator's report (`media`) and the bind-mount row (`web`). | analysis A-01 | **Accepted gap, declared.** Recorded in `fold.md` as not folded? No — the requirement is folded, its *evidence* is weaker than the criterion asks. Named here so the reader sees it. |
| C-02 | `unrequested` | `tests/test_entrypoint_line_endings.py` lost four tests (its `Dockerfile`-placement and strip tests) and kept only the `*.sh` pin. | T007; TDD-07 — the behaviour those tests asserted no longer exists | **Kept.** Replaced, not removed: the strip's behaviour is now asserted in `tests/test_runtime_entrypoint.py` against its new target. |

No `missing` and no `contradicts` rows.

### Outcome

Pass 1: **converged**, with SC-003's end-to-end execution left to the operator's machine and named as
such. No tasks appended; no pass 2.