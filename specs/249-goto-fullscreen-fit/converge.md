# Converge: refit the Go To detour on a stage resize

**Spec**: `specs/249-goto-fullscreen-fit/spec.md`
**Passes**: 1 of 3

## Pass 1 — 2026-11-27

**Checked**: the code against `plan.md`'s traceability table, row by row, with each row checked by
the method it declared. `test` rows are the three named cases run on throwaway `test_gkps249`;
`inspection` rows are the diff and the live probe readings.

| Requirement | Method | Result | Evidence |
| --- | --- | --- | --- |
| FR-001 | test | met | `test_a_goto_detour_refits_on_a_resize`: detour 42 → larger with stage 804 → 984, key updated; red on base with `42 not greater than 42` |
| FR-002 | test | met | `test_a_fullscreen_signal_before_resize_still_fits_the_detour`: signal first, then resize; red on base with the same wrong value |
| FR-003 | test | met | shared with FR-001: key returns to `1376x804|…` and the size returns to the original |
| FR-004 | test/inspection | met | `test_a_resize_without_a_detour_keeps_service_screens` green; `render()` and `fitNeighbours()` byte-identical in the diff |
| FR-005 | inspection | met | `git diff --name-only` shows only `static/web/projector.js`, `tests/e2e/test_projector.py` and the pack; no model, view, URL, CSS or template |
| SC-001 | inspection | met | `preview/probe.py`, resize-only: base `87 → 87 → 87`, slice `87 → 109 → 87`, stage 804 → 984 → 804 |
| SC-002 | inspection | met | same probe with `fullscreenchange` first: base flat, slice `87 → 109 → 87` |
| SC-003 | inspection | met | probe and cases keep detour `is-active`, URL `/projector?service=…` and service screens unchanged |
| US1/AC1 | test | met | shared with FR-001 |
| US1/AC2 | test | met | shared with FR-003 |
| US1/AC3 | test | met | shared with FR-002 |
| US1/AC4 | test | met | shared with FR-004 |

**Targeted run**: three named cases, `...`, 0 failures, 12.5 s. Full browser suite deferred to the
push step; no full-suite claim is made here.

**Findings**: none — `missing` 0 · `partial` 0 · `contradicts` 0 · `unrequested` 0.

**Outcome**: converged on pass 1. No convergence tasks were appended.

## Accepted gaps

None. The fonts-ready detour gap (analysis F002) is reported, not accepted as a requirement gap.

## Cap reached

Not applicable — converged before the cap.
