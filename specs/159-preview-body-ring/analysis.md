# Analysis: a preview's play shortcut paints nothing on the dialog's edge

**Date**: 2026-10-29 · **Gate**: opens at zero CRITICAL and 100% coverage.

**Artifacts read** (sha256, first 12):

| Artifact | Digest |
| --- | --- |
| `spec.md` | `873649dc85ca` |
| `plan.md` | `b4d1256c33f3` |
| `research.md` | `b1851af9ead4` |
| `data-model.md` | `6a723238b505` |
| `contracts/none.md` | `6605924c0296` |
| `quickstart.md` | `a6a38d64b471` |
| `tasks.md` | `48b84d917bac` |
| `checklists/requirements.md` | `3c1b7030eac2` |

**Metrics**: 4 requirements · 4 success criteria · 6 story scenarios · 5 edge cases (19 traceability
rows) · 16 tasks, six of them test work — a fixture (T001), two writing tasks (T002, T003) and three
runs (T004, T009, T010) · coverage **14/14 = 100%** · CRITICAL **0**.

The coverage figure is read from the traceability table, not re-derived from the task list: every
`FR-###`, `SC-###` and `USn ACn` in `spec.md` appears as a row in `plan.md`. No mechanical fix was
needed, so there is no before/after delta to report.

## Findings

| # | Class | Finding | Disposition |
| --- | --- | --- | --- |
| F1 | **medium** | SC-001's *How it is measured* cell reads "`:focus-visible` false and computed outline `none 0px`". Under the adopted mechanism the body keeps focus (FR-003 depends on it), so `:focus-visible` stays true and only the paint changes — the first half of that cell cannot be produced by any correct fix (`research.md` D003). | **Owner decision at gate 2.** Recommended: narrow the cell to the painted outline, which is what the criterion's own words ("shows no focus indicator") describe. The alternative is to restate SC-001 at Specify and re-enter the loop, which voids this plan (SDD-25). |
| F2 | **low** | `test_tab_brings_the_ring_back_after_a_space_press` and `test_the_next_preview_gets_its_ring_back` were planned as guards — expected green before the fix. **They are not:** each one pre-asserts the suppressed state after the space press, so all five cases are red on the unmodified page (History, run 1). | Corrected in place rather than deleted: the pre-assertion is what makes the guard test a state the fix produces, so the tests are right and the earlier claim about them was wrong. |
| F3 | low | T005–T008 make both guards go red mid-slice: T006 sets the class before the open/close clears and the Tab branch exist. | Accepted — that is the red-green cycle working, and the task list says so at T006 rather than leaving a reviewer to discover it. |
| F4 | note | The `specs/README.md` index row was written at gate 1 (Accept), not in Polish as the plan's structure implies. | Recorded in T012. The row's content is the same either way; only its timing differs from 150's. |
| F5 | low | The two `manual` rows (SC-001, SC-004) cannot be measured on the branch: compose serves `develop`, and a worktree server is refused by the companion's origin allow-list, so no audio or video preview can load its media. | Accepted, as specs 148 and 150 recorded the same limitation. The commands and the expected reading are in `quickstart.md`; the row is T016. |
| F6 | none | The capability number R27 is provisional — `reading` folds through R26 at 2026-10-28 and other slices are in flight. | Recorded at Fold (T013); if a sibling claims R27 first, this slice takes the next free number and the spec's Assumptions are corrected in the same commit. |
| F7 | low | Task coverage of the `manual` rows rests on one task (T016) carrying both SC-001 and SC-004. | Accepted: they are one act on one screen — open a preview, press space, Tab, screenshot — and splitting them would produce two tasks that cannot fail independently. |

## History

- 2026-10-29 — first run, pack as of the digests above: coverage 14/14, CRITICAL 0, one medium finding
  (F1) held for gate 2, six notes and lows recorded. Gate 2 may open once F1 is decided.
- 2026-10-29 — after implementation. `tests.e2e.test_preview_body_ring` run three times green
  (7 cases, 23.8 s / 20.2 s / 23.8 s); the same module against the unmodified product files — both
  reverted with `git checkout` — **5 of 5 failed** on `'2px solid rgb(28, 92, 60) offset -2px' != 'none'`,
  which is the red run F2 corrects. Two cases were added during convergence for FR-003, because its
  planned evidence (`test_entry_preview`) errors on develop; see `converge.md`.
- 2026-10-29 — F1's disposition, as delivered: the owner authorised delivery with *"push and merge"*,
  which accepts the recommendation rather than reopening Specify. `SC-001`'s measurement moved to the
  painted outline in the traceability row and in the test; the criterion's wording is unchanged.
