# Tasks: the dock fills whatever panel it is given

**Spec**: `specs/164-dock-fluid-width/spec.md` · **Plan**: `specs/164-dock-fluid-width/plan.md`

Order used: the order below, one thread. `[P]` marks a task that is order-independent, not one run
concurrently.

## Phase 1 — Setup

- [X] T001 [P] Confirm the worktree `../multimedia-gkps-klender-164-dock` is on `fix/164-dock-fluid-width` and that a throwaway database (`gkps164`) carries the suite, so no other worktree's test run collides — `specs/164-dock-fluid-width/quickstart.md`

## Phase 2 — US1: the panel is the page at every width

- [X] T002 [US1] Write the failing case: at 320, 420, 560, 720, 900, 1440, 1920 and 2560 the panel's width equals the viewport's, its x is 0, and `scrollWidth == clientWidth` — `tests/e2e/test_obs_dock.py` (`test_the_dock_fills_whatever_width_it_is_given`, with the `_panel()` helper)
- [X] T003 [US1] Make T002 pass: `.dock` loses `max-width: 560px` and `margin: 0 auto`; it takes `margin: 0` and keeps `width: 100%`, `height: 100%` — `static/styles/design/obs-dock.css`
- [X] T004 [US1] Record in the rule's comment why the panel is never capped: the dock's size is the operator's, not the page's — `static/styles/design/obs-dock.css`

## Phase 3 — US2: one column, and that column fills the panel

- [X] T005 [US2] Write the failing case: at 560, 900, 1440 and 1920 the picker body is `display: block`, every bucket section shares one x, the first row's width equals the body's content width and the viewport's width less 16px, and the bucket head computes `sticky` — `tests/e2e/test_obs_dock.py` (`test_a_wide_dock_keeps_the_picker_in_one_column`)
- [X] T006 [US2] Confirm the one column needs no rule of its own: `#pickBody` stays `display: block` and nothing in the sheet lays the buckets out side by side — `static/styles/design/obs-dock.css` (inspection; the bucket-per-column block from the earlier pass is gone)
- [X] T007 [US2] Confirm the row's anatomy carries the fill: the name is the flexible first item and the date the last, so the date lands on the row's right padding at every width — `static/styles/design/obs-dock.css` (`inspection`)

## Phase 4 — US3: a narrow dock is unchanged

- [X] T008 [US3] Read the probe at 320, 420 and 560 and compare every box with the spec's 1.23.1 column: panel and rows identical, no rule added below 560 — `specs/164-dock-fluid-width/probe/probe.py`

## Phase 5 — Polish

- [X] T009 [P] Re-run the probe and check every number in `spec.md`'s `## UI/UX` against it — `specs/164-dock-fluid-width/probe/probe.py`
- [X] T010 [P] Run the whole dock surface: the two width cases, the module's five existing cases and the unit file — `tests/e2e/test_obs_dock.py`, `multimedia/web/test_obs_dock.py`
- [X] T011 Converge against the traceability table, then Fold the new requirement into the capability file — `docs/spec/reading.md`, `specs/164-dock-fluid-width/converge.md`, `specs/164-dock-fluid-width/fold.md`
- [X] T012 Delivery: the spec's index row, `VERSION` 1.23.1 → 1.23.2 with the `## [Unreleased]` line, the card `ITEM-177` with its `branch` and `pr`, and the board rows — `specs/README.md`, `VERSION`, `CHANGELOG.md`, `backlog/items/ITEM-177-dock-fluid-width.md`, `backlog/board.md`

## Phase 6: Convergence

Pass 1 (2026-10-29): 19 rows checked by their declared method, no `missing`, no `partial`, no
`contradicts`, no `unrequested` — converged on the first pass. See `converge.md`; `reading/R33` folded
in `fold.md`. Delivery is PR #464, merged into `develop` as `6a1f6562`; the card closed on 2026-10-30.
