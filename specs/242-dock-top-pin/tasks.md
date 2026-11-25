# Tasks — spec 242

**Order**: one agent, one thread. `[P]` means order-independent, not concurrent; the order below
is the order used. Product edit predates the pack under live-preview-first; it stays uncommitted
until Fold, and each new E2E pin is proven red on unmodified `develop` before it is made green.

## Setup

- [X] T001 Create `specs/242-dock-top-pin/preview/run-tests.sh` from spec 208's runner with the
  throwaway database `gkps242`; paths: `specs/242-dock-top-pin/preview/run-tests.sh`.

## Foundational

- [X] T002 [P] [US1] Write a failing E2E for a faithful top pin when the live block is wholly
  above the fold (`test_the_top_pin_stands_when_the_live_block_is_above`); prove it red on base;
  paths: `tests/e2e/test_dock_top_pin.py`.
- [X] T003 [P] [US1] Make T002 pass: `topBandSlot` in `renderList()`, `updateTopBand()` in
  `updatePins()`, `.topband-slot` CSS; paths: `static/web/obs-dock.js`,
  `static/styles/design/obs-dock.css`.

## US1 — the pin stands when the block is above

- [X] T004 [US1] Write a failing E2E for the reduced-motion instant pin
  (`test_the_top_pin_lands_instantly_under_reduced_motion`); paths: `tests/e2e/test_dock_top_pin.py`.
- [X] T005 [US1] Make T004 pass by keeping the reduced-motion branch on the same `updatePins()`
  path; paths: `static/web/obs-dock.js`.

## US2 — the pin yields, per frame

- [X] T006 [US2] Write a failing E2E for per-frame geometry tracking on the glide home
  (`test_the_top_pin_tracks_the_block_per_frame`); paths: `tests/e2e/test_dock_top_pin.py`.
- [X] T007 [US2] Make T006 pass: `updatePins()` at the head of `glideRow()` and on every existing
  geometry path; paths: `static/web/obs-dock.js`.
- [X] T008 [US2] Write a failing E2E for hand scroll and crossing give-way
  (`test_the_real_header_takes_over_when_the_block_returns`); paths: `tests/e2e/test_dock_top_pin.py`.
- [X] T009 [US2] Make T008 pass: hide the slot when the block reaches the fold and on liveness
  change (go to included); paths: `static/web/obs-dock.js`.

## US3 — the click is the centre act

- [X] T010 [US3] Write a failing E2E for the click (centre row, unchanged display state,
  following returns) (`test_clicking_the_top_pin_performs_the_centre_act`); paths:
  `tests/e2e/test_dock_top_pin.py`.
- [X] T011 [US3] Make T010 pass via the shared `.liveband-slot, .topband-slot` click branch;
  paths: `static/web/obs-dock.js`.
- [X] T012 [US3] Run the new module and the three regression modules declared in SC-006 with
  `run-tests.sh`; record results and compare any red name against unmodified base; paths:
  `specs/242-dock-top-pin/preview/run-tests.sh`.

## Polish and delivery

- [X] T013 [P] Inspection: diff `obs-dock.js` / `obs-dock.css` against `develop` and confirm the
  bottom pin, NEXT band, `.offstrip` and header wash are byte-identical (FR-005).
- [X] T014 Write `converge.md` with the traceability comparison and typed gaps; paths:
  `specs/242-dock-top-pin/converge.md`.
- [X] T015 Fold: add `dock/R19` to `docs/spec/dock.md`, move the header date, write `fold.md`;
  paths: `docs/spec/dock.md`, `specs/242-dock-top-pin/fold.md`.
- [X] T016 Commit the converged pack, code, board row and capability delta on
  `feat/242-dock-top-pin` (first commit; green suite required); Conventional Commit subject.
- [X] T017 On the owner's `push` word, push and open the draft PR, then move `ITEM-257` to
  `In review` with `pr:` in its own commit and mark the PR ready; paths: `backlog/board.md`,
  `backlog/items/ITEM-257-dock-top-pin.md`.
- [X] T018 Pre-merge delivery commit: `VERSION` 1.36.27 → 1.37.0 (`minor`), one `CHANGELOG.md`
  `## [Unreleased]` line, card `Done` with `closed_at`/`closed_reason` and board row
  `develop via [#N]`; paths: `VERSION`, `CHANGELOG.md`, board and card.
- [ ] T019 On the owner's `merge` word, squash-merge with the PR title and body as the squash
  message; do not delete the local branch or worktree.
