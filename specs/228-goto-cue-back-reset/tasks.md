# Tasks: Back clears the Go To from the cue over an empty stage

## Setup

None — the worktree and slice branch already exist.

## Foundational

None — no new entity, interface or dependency.

## US1 — Leaving a Go To returns the cue to the empty stage

- [X] T001 [US1] Write a failing E2E for Back from a passage Go To with no service, asserting the
      cue has no label, flip or Back control in `tests/e2e/test_goto_shared_state.py`.
- [X] T002 [US1] Write a failing E2E for Back from a song Go To over a service with no entries,
      asserting no label and no baits remain in `tests/e2e/test_goto_shared_state.py`.
- [X] T003 [US1] Write a failing E2E for Back pressed on the dock with no service, asserting the
      projector's cue clears through the shared state.
- [X] T004 [US1] Make all three pass by clearing the cue's Go To DOM in the empty branch of
      `renderCue()` in `static/web/projector.js`.

## Polish

- [X] T005 Fold the clear-on-exit rule into `docs/spec/projector.md` `R2` and write `fold.md`.
- [X] T006 Write the card, board row, changelog line and version bump; record convergence.

## Revision (owner finding, same unpushed slice)

- [X] T007 [US2] Write failing E2E cases for the idle empty cue's separator, the inert mouse
      zones with fullscreen kept, and the visible cursor with working cue buttons.
- [X] T008 [US2] Mark the idle empty stage in `syncEmptyNotice()` and skip cursor auto-hide in
      `revealCursor()` in `static/web/projector.js`.
- [X] T009 [US2] Hide the separator and disable the mouse zones with two scoped rules in
      `static/styles/design/projector.css`.
- [X] T010 Re-fold `docs/spec/projector.md` `R2` with the idle HUD rules and amend the pack.
- [X] T011 [US2] Add `.cue-next[hidden] { display: none; }` so the lone right-arrow icon is not
      painted when the next control is hidden, and pin the computed display in two E2E cases.
