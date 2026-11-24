# Analysis — spec 241

**Date**: 2026-11-24
**Artifacts read**: `spec.md` `2562c9be5eb2`, `plan.md` `e846d9a4fea1`, `tasks.md`
`810b4fc1a368`, `checklists/requirements.md` `bfae4deba7bf`, `research.md`, `data-model.md`,
`contracts/README.md`, `docs/spec/reading.md` (`R11`, `R14`, `R57`).

**Metrics**: 8 functional requirements · 4 success criteria · 3 user stories (12 scenarios) ·
22 traceability rows (18 test · 4 inspection · 0 manual) · 19 tasks · 10 checklist items ·
0 `[NEEDS CLARIFICATION]` markers · 0 unknowns.

## Findings

| ID | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| A1 | MEDIUM | `US1/AC4`, `US3/AC1` and `FR-004` are verified by inspection of the gesture's lifecycle, not by a test that asserts a single POST. | Accepted — the E2E tests assert the written order and the reload; the captured call stacks are recorded in `research.md`. Adding an event-counter test would test structure, not behaviour. |
| A2 | LOW | `FR-008` (legacy rows, choices and their options) is inspected against the service 151 shape rather than asserted in a new E2E case. | Accepted — `applyPaneOrder()` only moves pks named by `what`, and `what` comes from top-level TOC rows; the existing 32 reorder cases cover the common shapes. |
| A3 | LOW | The preview uses scratch service 322, whose break row has no stage section, so the two lists differ by one row. | Accepted — the four-entry fixture gives the clean `3,1,2,4` / `3,1,2` measurement in `preview/README.md`; the scratch page shows the real shapes. |
| A4 | INFO | One previously-red E2E case (`test_dialog_defers_sidebar_idle_collapse_then_restarts`) turns green with the sorter fix. | Recorded as a side benefit; no new requirement, no spec change. |
| A5 | INFO | `multimedia.web.tests` keeps one failure and `test_reading.py` / `test_entries.py` keep their known reds; all reproduce on unmodified `develop`. | Accepted — the full reorder module and all six song-sort tests are green on this branch. |

No CRITICAL findings. Traceability coverage is 100%: every `FR-###`, `SC-###` and story scenario
appears in the plan's table with a declared verification method.

## History

- 2026-11-24 — first pass: 5 findings, 0 CRITICAL, 100% coverage; accepted with the dispositions above.
