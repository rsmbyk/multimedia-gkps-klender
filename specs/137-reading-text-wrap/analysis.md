# Analysis: a reading page's text wraps at its pane

**Date**: 2026-10-27 · **Gate**: opens at zero CRITICAL and 100% coverage.
**Artifacts read** (sha256, first 12):

| Artifact | Digest |
| --- | --- |
| `spec.md` | `e019317b8327` |
| `plan.md` | `2f3cefdfce36` |
| `research.md` | `6ac7c86ba58f` |
| `data-model.md` | `734f1abaea76` |
| `contracts/none.md` | `c6fb8d6e5c0b` |
| `quickstart.md` | `b73978609936` |
| `tasks.md` | `d14cf213b926` |
| `checklists/requirements.md` | `ba455bbf2e8a` |

**Metrics**: 9 requirements · 7 success criteria · 11 story scenarios · 6 edge cases (33
traceability rows) · 17 tasks (7 of them test-writing) · coverage **100%** · CRITICAL **0**.

## Findings

| # | Class | Finding | Disposition |
| --- | --- | --- | --- |
| F1 | note | FR-007 and the TB/SIM-toggle edge case resolve to the same test (`test_the_title_keeps_its_box_and_the_toggle_its_line`): the toggle's line is how the width's stability is observed. | Kept: two statements, one command. Recorded so the reader does not look for a second test. |
| F2 | note | FR-009 and the one-character edge are `inspection` rows, discharged by assertions inside test functions rather than by a command of their own. | Kept: the inspection is real (`plan.md` Design quotes the three selectors, and T003 asserts the computed value on a nested span); it is visible where the behaviour is measured. |
| F3 | note | The rule already exists in the tree, because the live preview serves it (SDD-06). T006, T009 and T011 confirm it rather than author it. | Expected: the preview is a live page, not a mock. Recorded so the implementer does not go looking for a missing edit — and so T003's red run still comes first. |
| F4 | low | `quickstart.md`'s E2E command is marked not-yet-runnable: `tests/e2e/test_text_wrap.py` is written in Implement (T002–T012). | Expected ordering under TDD; the module and function names are fixed here so the red run needs no invention. |
| F5 | low | US3.2 (a media filename stays one line) has no browser test: the suite holds no media fixture, and the declaration is not touched by this slice. | Accepted as `inspection` — the declaration is unchanged and the preview shows the same one-line row. Stated in `plan.md`'s Risks rather than carried as an untested claim. |
| F6 | none | The capability file has no `R13` yet. | Not a defect: Fold adds it (T015); the spec cites `new: reading` for the new requirement and `reading/R12` for what it must not unclip. |
| F7 | low | Two rows are `test` but cannot be shown red under this slice: `test_a_short_title_is_unchanged` (T004) and `test_a_truncating_row_still_truncates` (T012) assert behaviour the change does not alter. T012 has a mutation that proves it is wired (drop `.book__n`'s `nowrap`); T004 has none — it is a regression guard against a future type or flow change. | Kept as `test`, and stated as a guard in `tasks.md` rather than dressed up as red-first. Cost of leaving it: a reviewer must take one row on trust that its guard is meaningful, which the stated mutation covers for T012 and the spec's own UI/UX numbers cover for T004. |
| F8 | fixed | **First run:** the plan's traceability named `test_no_reading_route_scrolls_sideways` and `test_a_short_title_is_unchanged`, but no task wrote either — FR-005, FR-008, SC-001 and SC-003 had no task behind them. | Mechanical fix applied before re-running: `tasks.md` rewritten to 17 tasks (T004 and T007 added, the rest renumbered), and this file's metrics refreshed. |

No other mechanical fixes were needed: terminology is stable (`run`, `spill`, `root`, `truncating
surface`), and every path the plan names exists in the worktree
(`static/styles/design/components.css`, `multimedia/web/templates/reading/base.html`,
`_preview_modal.html`, `tests/e2e/test_reading.py`, `tests/e2e/test_song_label_typography.py`,
`tests/e2e/test_media_library.py`).

## History

- **2026-10-27 — first run**, on the accepted spec and the plan above: 0 CRITICAL, coverage 97% on
  the first pass — two requirements and two success criteria had no task (F8). The task list was
  corrected, the digests refreshed, and the run repeated.
- **2026-10-27 — second run**, on the corrected artifacts: 0 CRITICAL, 100% coverage, eight findings
  — two notes about one command serving two statements, one note about the live preview, two low,
  one none, one low about guard tests. None fixed silently.
