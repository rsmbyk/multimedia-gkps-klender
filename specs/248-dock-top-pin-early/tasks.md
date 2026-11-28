# Tasks: earlier top pin for the live header

**Spec**: `specs/248-dock-top-pin-early/spec.md`
**Plan**: `specs/248-dock-top-pin-early/plan.md`
**Verification split**: 9 test · 4 inspection · 1 manual

## Phase 1 — Setup

- [X] T001 Build the live preview harness on the real dock: `specs/248-dock-top-pin-early/preview/{serve.sh,probe_boundary.py,README.md}` and the frozen before/after JSON (done before gate 1; recorded in the spec's Assumptions).
- [X] T002 Add the throwaway-database runner `specs/248-dock-top-pin-early/run-tests.sh` with the `gkps248` database and no credential in the file.

## Phase 2 — Foundational

- [X] T003 Confirm the base build's boundary with `preview/probe_boundary.py` against 63404 (first pin 1164, blockTop -110) and keep the JSON as the before evidence.
- [X] T004 Read `updatePins()` call sites and agree that no new listener is needed (research D004).

## Phase 3 — US1 (P1) 🎯 MVP

**Goal**: the pinned copy takes over at the header's own top edge, with one painted header and no hop.
**Independent test**: scroll a deep live entry until its header reaches the fold; the pin stands at 0 px while the native header is still at the edge, and only one is painted.

- [X] T005 [P] [US1] Write a failing E2E case `test_the_top_pin_takes_over_when_the_header_is_clipped` in `tests/e2e/test_dock_top_pin.py`, and prove it red on unmodified develop.
- [X] T006 [P] [US1] Write a failing E2E case `test_only_one_header_is_painted_while_the_pin_owns_the_edge` in the same module; assert the source is hidden and the clone is not, with identical boxes on the takeover frame.
- [X] T007 [US1] Move the boundary in `static/web/obs-dock.js` `updateTopBand()` to `li.top <= box.top + 0.5` and track the covered row (preview edit already applied before gate 1).
- [X] T008 [US1] Add `.entryrow.is-covered` and the clone's class removal in `static/styles/design/obs-dock.css`; keep the clone at `top: 0` (preview edit already applied).
- [X] T009 [P] [US1] Re-point `test_the_top_pin_tracks_the_block_per_frame` to the new boundary and keep 0 mismatched frames on the glide home.
- [X] T010 [US1] Keep `test_the_top_pin_lands_instantly_under_reduced_motion` green; same-paint reconciliation.

## Phase 4 — US2 (P2)

**Goal**: every other dock pin state stays as accepted.
**Independent test**: run the named regression modules and read the focused diff.

- [X] T011 [P] [US2] Keep `test_clicking_the_top_pin_performs_the_centre_act` green — display state byte-identical, following returns.
- [X] T012 [US2] Verify by inspection that `updateLiveBand()`, `updateBand()`, `.offstrip` and the entry anatomy are untouched.
- [X] T013 [US2] Manually check that a Go To on air keeps its `.offstrip` unchanged; the service pin is present on both builds (D006) and its earlier boundary is the only change.

## Phase 5 — Polish

- [X] T014 Re-collectstatic and restart the 8793 server after the final CSS/JS state, then re-run the boundary probe and confirm the live URL serves the change.
- [X] T015 Run the targeted modules with `run-tests.sh` and record the result; defer the full browser matrix to the push step.

## Phase N+1 — Convergence

<!-- written by Converge only; absent until it runs -->
