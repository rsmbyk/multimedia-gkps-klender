# Convergence: picker popout scrollbar edge

**Pass**: 1 · **Date**: 2026-11-26
**Spec**: `specs/244-picker-menu-scrollbar-edge/spec.md`
**Plan**: `specs/244-picker-menu-scrollbar-edge/plan.md` (19 traceability rows)

## What was checked

Every row was re-assessed against the code in this worktree by its declared method.

| Method | Rows | Evidence |
| --- | --- | --- |
| `test` (14) | FR-001, FR-003, FR-005, FR-006, SC-001, SC-002, SC-003, SC-004, US1/AC1, US1/AC2, US2/AC1, US2/AC2, US2/AC3, US2/AC4 | Focused module `tests/e2e/test_picker_menu_scrollbar_edge.py`: 4/4 green on the slice with `gkps244green`; on unmodified base `14af227a` with `gkps244red`, three behaviour tests fail `AssertionError: 9 != 1` (right and bottom edge) and the content-invariant test passes — red for the reported reason, not an import or fixture error. Sibling modules: `test_passage_search_pickers` 19/19 green; `test_song_entry_pickers` 11/12 with one pre-existing failure (below). |
| `inspection` (5) | FR-002, FR-004, FR-007, US1/AC3, US1/AC4 | Computed `.editor__picker-menu` overflow `clip`, 10px radius; `::-webkit-scrollbar` width `5px`; `--scroll-thumb` token unchanged; live preview corner clipped at the scrolled end; dark theme measured with right/bottom gaps `1/1`; flipped menu at 1440×300 (`data-flip="up"`, menu bottom 162.3, scrollport bottom 161.3) with gaps `1/1`. |
| `manual` (0) | — | none declared |

## Findings

| Type | Finding | Evidence | Disposition |
| --- | --- | --- | --- |
| `missing` | none | all 19 rows have an implementation and evidence | — |
| `partial` | none | edge, content invariance and non-overflow states each measured | — |
| `contradicts` | none | the CSS change matches the accepted `reading/R59` behaviour | — |
| `unrequested` | none | only two CSS rule sets, one E2E module and bookkeeping changed | — |

## Pre-existing red, not a slice regression

`tests.e2e.test_song_entry_pickers.py::SongEntryPickerE2ETests::test_hidden_and_muted_states`
fails with `22 != 0 within 1 delta` at line 201 on both the slice (`gkps244sib2`) and the
unmodified base (`gkps244sibbase`). The failure name and assertion are identical; the verse-panel
geometry it measures is not touched by this slice. It stays red on `develop` and is not counted as
a convergence gap. The other 18 sibling tests are green.

## Bookkeeping correction

The plan and tasks first named `ITEM-258`; that card was taken in flight by the navigation slice.
Before creating the card this slice re-checked every worktree and took `ITEM-259` instead. The
card and board row use `ITEM-259`; the retake is recorded here and in `fold.md`.

## Merge resolution (parallel slice)

`origin/develop` advanced with spec 243 after this branch was cut. The merge auto-applied code and
the board, and conflicted only on the capability header's `slices` line. Both IDs were kept, newest
first: `244-picker-menu-scrollbar-edge`, `243-navigation-loading-feedback`, then the existing list.
The R59 modification survived unchanged. The focused module was re-run on the merged tree with
`gkps244merge`: 4/4 green.

## Outcome

**Converged** — no accepted gaps. H1 and H2 from `analysis.md` were discharged by the live computed
style checks and the dark/flipped measurements above; the pre-existing sibling failure is recorded
rather than silently fixed.
