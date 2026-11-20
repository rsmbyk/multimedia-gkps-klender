# Tasks — spec 205 (dock centre pace)

Ordered by user story. `[P]` = order-independent. TDD active: a `test` row is two tasks (write failing,
make pass). The code change already landed as preview work; Implement proves it red-on-base then green.

## Setup

- [X] T001 [P] Confirm the fixture service "Ibadah Pace Probe" (60 entries) and the slice server on
  8765 + develop on 63404 are serving — `specs/205-dock-centre-pace/preview/README.md`.

## Foundational

- [X] T002 [P] Add the shared pace constant `CENTRE_MS = 200` and switch `glideScroll`, `glideRow`
  and `startMorph` to it; replace `ease` with the plain sine in-out — `static/web/obs-dock.js`.
  *(Landed as preview; re-verified here.)*

## US1 — Fast advancing keeps the live row near the middle

- [X] T003 [US1] Write the failing pace test
  `test_the_centring_glide_runs_at_the_shared_pace` (single-move duration ≤ 280 ms) —
  `tests/e2e/test_obs_dock_follow.py`.
- [X] T004 [US1] Prove it red on the base: stash the `obs-dock.js` change, run the test (400 ms fails
  the ≤ 280 ms assertion), pop the change.
- [X] T005 [US1] Make it pass: run the test on the slice (200 ms) — green.
- [X] T006 [US1] Run the regression guards green: `test_the_centring_decelerates_into_its_target`,
  `test_reduced_motion_jumps_instead_of_gliding` — `tests/e2e/test_obs_dock_follow.py`.

## US2 — The single move stays smooth; the hand toggle is untouched

- [X] T007 [US2] Inspection: `startToggleMorph` keeps 230 ms `easeInOut`; `glideScroll` end-clamp and
  the wheel/pointerdown cancel are unchanged; `startMorph` carry uses `CENTRE_MS` and `ease` —
  `static/web/obs-dock.js` diff.
- [X] T008 [US2] Run the header-toggle regression green:
  `test_the_header_toggles_its_block_and_never_projects`,
  `test_the_toggle_swaps_instantly_under_reduced_motion` — `tests/e2e/test_obs_dock.py`.

## Polish

- [X] T009 [P] Run `preview/probe.py` before/after; confirm the UI/UX numbers (single-move steps,
  rapid mean_off / max_step) and record raw frames in `preview/shots/`.
- [X] T010 Delivery: bump `VERSION` 1.34.2 → 1.34.3, append the `## [Unreleased]` changelog line,
  set card `bump: patch`, move the card to Done before the merge and the board row to
  `develop via [#PR]` — `VERSION`, `CHANGELOG.md`, `backlog/items/ITEM-214-dock-centre-pace.md`,
  `backlog/board.md`. *(Runs at the pre-merge commit, after the owner's push/merge word.)*