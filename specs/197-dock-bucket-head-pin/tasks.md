# Tasks: The dock's bucket head owns the strip above its label

**Spec**: `specs/197-dock-bucket-head-pin/spec.md`
**Plan**: `specs/197-dock-bucket-head-pin/plan.md`
**Verification split**: 5 test · 2 inspection · 1 manual

## Phase 1 — Setup

- [X] T001 [P] Create `tests/e2e/test_dock_bucket_head.py` — a `StaticLiveServerTestCase` with Playwright, its
  fixtures two dated services in two age buckets (one dated today, one about 60 days back), and helpers
  `_open_dock(context)` and `_geometry(page)` that return the scroller's box, the head's box, the label's box
  and the topmost element at scroller top + 2px.

## Phase 2 — Foundational

None: the slice is one stylesheet and one test module, and no shared prerequisite sits between the stories.

## Phase 3 — US1 (P1) 🎯 MVP

**Goal**: the pinned bucket head owns the strip above its label, at the same place at rest and pinned, with
nothing below it moved.
**Independent test**: scroll the picker past the first bucket; the strip above the label holds the head, and
the label is 14px under the divider at rest and pinned alike.

- [X] T002 [P] [US1] Write the failing test `test_a_pinned_bucket_head_leaves_no_row_above_it` — red on
  develop's stylesheet, where the head's top is 4px below the scroller and the hit test returns a
  `.servicerow`.
- [X] T003 [US1] Make T002 pass in `static/styles/design/obs-dock.css`: `#pickBody { padding-top: 0 }` and
  `.group__head { padding: 14px 6px 7px }`.
- [X] T004 [P] [US1] Write the failing test `test_the_label_holds_its_place_between_rest_and_pinned`.
- [X] T005 [P] [US1] Write the failing test `test_nothing_below_the_head_moves` — the first row's top equals
  the head's foot, at rest and pinned.

## Phase 4 — US2 (P2)

**Goal**: the keyboard cursor still parks below the pinned head, the head's foot having not moved.
**Independent test**: walk the cursor up through a boundary; every parked row is fully visible.

- [X] T006 [P] [US2] Write the failing test `test_the_cursor_still_parks_below_the_head`.
- [X] T007 [US2] Confirm no stylesheet change is needed — `scroll-padding-top` stays 37px because the head's
  foot does not move (inspection of the declaration and of the head's foot); T006 goes green with T003.

## Phase 5 — US3 (P2)

**Goal**: consecutive buckets are separated by 12px of air that never enters the pin.
**Independent test**: the next label sits 26px below the previous group's last row and 14px below the divider
when pinned.

- [X] T008 [P] [US3] Write the failing test `test_consecutive_buckets_keep_their_air`.
- [X] T009 [US3] Add `#pickBody section + section { padding-top: 12px }` to `static/styles/design/obs-dock.css`.

## Phase 6 — Polish

- [X] T010 Write the board row's `pr:` and move the card to `In review` once the PR exists.
- [X] T011 `CHANGELOG.md` under `## [Unreleased]` (Fixed) and `VERSION` 1.32.1 → 1.32.2, in the pre-merge
  commit that also closes the card.
- [X] T012 Fold `docs/spec/reading.md` R33 (modified) and record `fold.md`.

## Phase 7 — Convergence

**Pass 1** — every traceability row checked by its declared method; no missing, partial, contradicts or
unrequested gap. One observed consequence recorded (the picker's empty-state line sits 4px higher because it
shares the scroll body; no requirement names it). Suite: 5 + 19 tests green. Outcome: **converged** — see
`converge.md`.