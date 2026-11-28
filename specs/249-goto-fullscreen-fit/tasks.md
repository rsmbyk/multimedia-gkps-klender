# Tasks: refit the Go To detour on a stage resize

**Spec**: `specs/249-goto-fullscreen-fit/spec.md`
**Plan**: `specs/249-goto-fullscreen-fit/plan.md`
**Verification split**: 8 test · 4 inspection · 0 manual

`[P]` means order-independent, not concurrent; one thread runs them in the order written. Every new
`test` row has a red and a green task. The production change is already in the worktree as the
gate-1 preview; red tasks revert that one file under a trap that restores it on exit.

## Phase 1 — Setup

- [X] T001 Add a helper to `tests/e2e/test_projector.py` that opens a passage Go To with
      `_open_matius_5()`, reads the detour's computed font size and fit key, changes the viewport
      with CDP to 1920×1080 and back, and optionally dispatches `fullscreenchange` first.
      No assertions yet; no production code touched.
- [X] T002 Verify `preview/run_local.py` runs the targeted Django command with a throwaway
      `GKPS_DB` and prints no credential.

## Phase 2 — Foundational

- [X] T003 Revert only `static/web/projector.js` to the base file under the trap, run the helper,
      and record the red values: detour `87px` with key `1376x804|…` at a stage of 1856×984 in both
      orderings. Restore under the trap.

## Phase 3 — US1 (P1) 🎯 MVP

**Goal**: the detour's words follow a stage resize, whichever order the signals arrive in.
**Independent test**: open a Go To, grow the viewport, read the detour's font size.

- [X] T004 [P] [US1] Red test for FR-001 / FR-003 / US1-AC1, AC2:
      `test_a_goto_detour_refits_on_a_resize` — detour `87 → 109 → 87`, key
      `1376x804|… → 1856x984|… → 1376x804|…`, detour still active, URL unchanged.
- [X] T005 [P] [US1] Red test for FR-002 / US1-AC3:
      `test_a_fullscreen_signal_before_resize_still_fits_the_detour` — the same sizes when
      `fullscreenchange` is dispatched before the viewport changes.
- [X] T006 [US1] Restore the preview edit in `static/web/projector.js`: the `resize` listener calls
      `syncFullscreenFit()` after `render(true)`. Make T004 and T005 green without touching
      `render()`, `fitNeighbours()` or `fit()`.
- [X] T007 [P] [US1] Guard test for FR-004 / US1-AC4:
      `test_a_resize_without_a_detour_keeps_service_screens` — a resize with no detour settles the
      active and neighbour screens exactly as before; green on the base too.

## Phase 4 — Polish

- [X] T008 Run the three named cases with `GKPS_DB=gkps249` and report the targeted result; leave
      the full browser suite for the push step.
- [X] T009 Inspect the diff for FR-004 and FR-005: no edits to `render()`, `fitNeighbours()`, CSS,
      templates, endpoints or the cue; the `document.fonts.ready` gap stays as recorded.
- [X] T010 Write `analysis.md` (zero CRITICAL, 100% coverage) and `converge.md` pass 1 against the
      plan's traceability rows.
- [X] T011 Fold the `projector/R14` regression note into `docs/spec/projector.md`, update the
      capability header, and write `fold.md` with before/after counts. First commit.

## Phase 5 — Delivery (owner's words only)

- [ ] T012 On `push`: push the branch, open the draft PR, move `ITEM-265` to `In review` in its own
      commit with `status` and `pr:`, run the full browser suite and compare failure names with the
      base.
- [ ] T013 On `merge`: apply version `1.37.6` and the changelog line, close `ITEM-265` as `Done`
      with `closed_at`, `closed_reason` and the board's `develop via [#N]` row in the pre-merge
      delivery commit, update the PR body in place, then squash-merge with that same body.
