# Tasks: A Go To still names itself with no service under it

## Setup

None — the worktree and the slice branch already exist.

## Foundational

None — no new entity, interface or dependency.

## US1 — The cue belongs to the Go To, not the service beneath it

- [X] T001 [US1] Write a failing E2E for a passage Go To with no service under it, asserting the
      prefix, translation flip and Back in `tests/e2e/test_goto_shared_state.py`.
- [X] T002 [US1] Write a failing E2E for a song Go To over a service with no entries, asserting the
      prefix and one bait button per bait in `tests/e2e/test_goto_shared_state.py`.
- [X] T003 [US1] Make both pass by checking `detour` before the empty-entries early return in
      `static/web/projector.js` `renderCue()`.

## Polish

- [X] T004 Fold the new empty-cue scenario into `docs/spec/projector.md` `R2` and write
      `specs/227-goto-cue-empty-service/fold.md`.
- [X] T005 Write the card, board row, changelog line and version bump; record convergence.
