# Analysis: reopening the projector window

**Date**: 2026-10-27 · **Gate**: opens at zero CRITICAL and 100% coverage.
**Artifacts read** (sha256, first 12):

| Artifact | Digest |
| --- | --- |
| `spec.md` | `d4f65ebbb8f2` |
| `plan.md` | `90d832b5714b` |
| `research.md` | `1e16167482bd` |
| `data-model.md` | `c0026502675e` |
| `contracts/none.md` | `d0d5d6a4d1e8` |
| `quickstart.md` | `51eb9ecdc979` |
| `tasks.md` | `ea8b13619520` |
| `checklists/requirements.md` | `bfc7e1794440` |

**Metrics**: 6 requirements · 6 success criteria · 9 story scenarios · 6 edge cases (12
traceability rows) · 13 tasks (4 of them writing tests) · coverage **100%** · CRITICAL **0**.

## Findings

| # | Class | Finding | Disposition |
| --- | --- | --- | --- |
| F1 | note | FR-002 and SC-001 both land on `test_reopening_returns_the_window_to_the_screen_on_air`: the screen is the requirement, so one command observes both. | Kept: two statements, one command. Recorded so a reader does not look for a second test. |
| F2 | note | FR-005 is an `inspection` row while its phone half is a test (SC-006). The box, glyph and accessible name are static; the drawn/not-drawn state is what a browser can assert. | Kept: the split says which half is which. |
| F3 | low | Three edge cases have no command of their own: a blocked popup, the projector open as an ordinary tab, and the shell/deep-link path. The first is a `window.open` returning null (a browser policy), the second needs a second surface, and the third is spec 119's `shell:page` re-sync, already exercised by `test_the_display_works_on_the_path_a_person_clicks_through`. | Accepted as inspection for the first two, and as coverage by the existing test for the third; recorded here rather than dressed up as red-first tests. |
| F4 | low | The preview carries a copy of the proposed stylesheet rules, because it is a static page; `components.css` is the authority once implemented. | Expected: the preview is the design record, and Converge re-measures the running app (T011) against `spec.md` §UI/UX. |
| F5 | none | `docs/spec/reading.md` has no requirement for the reopen act yet, and its R14 names only the Project control. | Not a defect: Fold adds them (T012); the spec cites `new: reading` and `reading/R14`. |
| F6 | fixed | **First run:** US1.5 (a second tab hears the start and draws the control) and the "pressed twice" edge case had no task behind them. Coverage read 92%: two spec statements with no step. | Mechanical fix applied before re-running: T004 gained the second-tab assertion and T005 the double press; the digests above are the corrected files' and the metrics line refreshed. |

No other mechanical fixes were needed: terminology is stable (`control`, `group`, `pane`, `on air`),
every path the plan names exists in the worktree (`multimedia/web/templates/reading/tatib.html`,
`static/web/display.js`, `static/styles/design/components.css`, `tests/e2e/test_projector.py`), and
the requirement IDs are unique.

## History

- **2026-10-27 — first run**, on the accepted spec and the plan: 0 CRITICAL, coverage 92% — two
  statements had no task (F6). The task list was corrected, the digests recomputed, and the run
  repeated.
- **2026-10-27 — second run**, on the corrected artifacts: 0 CRITICAL, 100% coverage, six findings —
  two notes about one command serving two statements, one low about three untested edge cases, one
  low about the preview's copy of the rules, one none about the capability delta awaiting Fold, and
  the fixed finding above.
