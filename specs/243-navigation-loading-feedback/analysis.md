# Analysis — spec 243

**Date**: 2026-11-25
**Artifacts read**: `spec.md` `70d039634f16`, `plan.md` `318fb54d650e`, `tasks.md`
`4c265278861e`, `checklists/requirements.md` `d42045318208`, `research.md` `3d0110ad1d6f`,
`data-model.md` `037aa7bb7597`, `contracts/README.md` `73251dbb46c0`, `quickstart.md`
`eb57de61cdd3`; code read: `static/web/reading.js` (`navigate()`, rail/panel/chapter click
handlers), `static/styles/design/components.css` (shell layout and `read__*` rules),
`multimedia/web/templates/reading/base.html`, `tests/e2e/test_navigation_freshness.py`.

**Metrics**: 10 functional requirements · 3 user stories (14 acceptance scenarios) ·
16 traceability rows (11 test · 8 inspection · 0 manual verification methods) ·
25 tasks · 22 checklist items · 0 `[NEEDS CLARIFICATION]` markers · 0 unknowns.

## Findings

| ID | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| A1 | MEDIUM | Replacing `pendingNavigation` queueing with cancel/coexist changes an existing client behaviour that no current E2E test pins. | Accepted — T009/T010 add the missing tests before T017 changes the queue. `tests/e2e/test_navigation_freshness.py` keeps the rail-to-page path green as a sibling guard. |
| A2 | LOW | Search and history traversal inherit the pending state, but their individual write/list classification is an assumption rather than a separate scenario. | Accepted — recorded in `spec.md` §Assumptions and §Scope; FR-010 names `navigate()` as the single choke point. A future slice can refine classification without changing this mechanism. |
| A3 | LOW | The stage is `pointer-events: none` while busy; if focus is already inside the stage, a write leaves a focused control under a disabled region. | Covered — T016 asserts the status announcement does not move focus, and T008 checks settlement clears `aria-busy` before the new content is used. If a live run shows a focus trap, it is a new finding, not a silent change to this spec. |
| A4 | LOW | The full-page fallback rule (leave the bar up until unload) is inspection-only. | Accepted — an E2E test cannot reliably observe the unload handoff; the inspection row in `plan.md` records the exact `navigate()` line to check. |
| A5 | INFO | `plan.md` and checklist CHK020 declared 12 test / 7 inspection but the table actually yields 11 test / 8 inspection across 16 rows. | Corrected in both artifacts during Analyze; no requirement or scope changed. |
| A6 | INFO | No app code, board, VERSION or CHANGELOG has been changed by this slice so far. | Expected — Analyze is read-only and implementation is gated at gate 2. |

No CRITICAL findings. Traceability coverage is 100%: every `FR-###`, every user story and all
14 acceptance scenarios appear in `plan.md`'s traceability table with a declared verification
method.

## History

- 2026-11-25 — first pass: 6 findings, 0 CRITICAL, 100% coverage; A5 corrected in place.
