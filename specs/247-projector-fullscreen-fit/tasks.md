# Tasks: refit the projector words when fullscreen changes the stage

**Spec**: `specs/247-projector-fullscreen-fit/spec.md`
**Plan**: `specs/247-projector-fullscreen-fit/plan.md`
**Verification split**: 10 test · 6 inspection · 1 manual

`[P]` means order-independent, not concurrent; one thread runs them in the order written. Every
new `test` row has a red and a green task. Inspection and manual rows produce no test task. The
production change is already in the worktree as the gate-1 preview: each red task temporarily
reverts that one file under a shell `trap` that restores it on exit, captures the wrong values, then
the green task runs with the change restored.

## Phase 1 — Setup

- [X] T001 Add a helper to `tests/e2e/test_projector.py` that opens a text screen at 1440×900,
      grows or shrinks `.projector__screen` by 200px, dispatches the named browser signal(s), and
      returns the active and neighbour line font sizes plus the URL and `data-current-screen`.
      No assertions yet; no production code touched.
- [X] T002 Verify `specs/247-projector-fullscreen-fit/preview/run_local.py` runs the targeted
      Django command with a throwaway `GKPS_DB` and prints no credential; record the command used
      in `quickstart.md`.

## Phase 2 — Foundational

- [X] T003 Revert only `static/web/projector.js` to the base file, run the helper, and record the
      red values: stage 804 → 1004 with the lines still at `42px` and the heading at `25.9574px`
      on the long-text fixture; the neighbour on service 1 stays at `125px`. Restore under the
      trap; no test file asserts an implementation detail.

## Phase 3 — US1 (P1) 🎯 MVP

**Goal**: a fullscreen signal that changes the stage re-fits the words, heading and neighbours, and
a repeat signal at the same stage does nothing.
**Independent test**: grow the stage by 200px, send the signal without a `resize`, and read sizes.

- [X] T004 [P] [US1] Red test for FR-001 / US1-AC1:
      `test_fullscreen_signal_refits_the_words_without_a_resize` — on the long-text service the
      stage grows 804 → 1004 without `resize`, the lines grow (base `42 → 42`, slice `42 → 49`),
      the heading keeps `size ÷ φ`, the key changes, and URL, index and body text are unchanged.
      The frozen `87 → 93` numbers stay in the live probe, not in the E2E assertion.
- [X] T005 [P] [US1] Red test for FR-003 / US1/AC2:
      `test_a_second_fullscreen_signal_does_not_change_the_fit` — a second identical signal leaves
      both computed sizes and the key unchanged.
- [X] T006 [P] [US1] Red test for FR-004:
      `test_fullscreen_signal_refits_the_neighbours` — the screen beside the active one is fitted
      to the new stage without being brought onto the stage.
- [X] T007 [P] [US1] Red test for US1/AC4:
      `test_a_fullscreen_signal_with_an_unchanged_stage_does_not_resize_words` — dispatching both
      signals with no stage change writes no new size.
- [X] T008 [US1] Restore the preview edit in `static/web/projector.js`: a `syncFullscreenFit()`
      that chooses the detour when up, otherwise `screens()[current]`, calls `fit(node, true)` and
      `fitNeighbours()` inside `requestAnimationFrame`, and is registered on `fullscreenchange`.
      Make T004–T007 green without touching `fit()` or `setSize()`.

## Phase 4 — US2 (P2)

**Goal**: the browser's own fullscreen and a resize-driven transition settle on the same sizes, and
the rest of the projector is untouched.
**Independent test**: dispatch the display-mode `change` signal, then replay a viewport change
with CDP.

- [X] T009 [P] [US2] Red test for FR-002 / US2/AC2:
      `test_display_mode_signal_refits_for_browser_fullscreen` — a `change` on
      `(display-mode: fullscreen)` with no `document.fullscreenElement` and no `resize` still
      refits the words.
- [X] T010 [P] [US2] Red test for SC-003 / US2/AC1:
      `test_resize_driven_fullscreen_still_settles_at_87_and_109` — CDP viewport 1440×900 →
      1920×1080 → back grows the active fit and returns it to the original size and key. Green on
      the unmodified base too: a characterisation guard, not a new behaviour.
- [X] T011 [US2] Register the display-mode listener with `addEventListener` and an `addListener`
      fallback; make T009 and T010 green and confirm the audio/video fullscreen takeover is
      unchanged.
- [X] T012 [US2] Inspect the diff for FR-005, FR-006, SC-004 and US2/AC3: no edits to the fit
      walk, `setSize()`, CSS, templates, key/click handlers or the cue; URL, screen index and body
      text unchanged in every probe reading.

## Phase 5 — Polish

- [X] T013 [manual] US1/AC3: open a passage Go To on the live preview, press `f`, read the
      detour's `.screen__lines` computed size before and after, press `f` again, and record the
      three readings in `converge.md`.
- [X] T014 Run the targeted module with `GKPS_DB=gkps247` (`tests.e2e.test_projector`) and report
      the named new cases; leave the full browser suite for the push step.
- [X] T015 Write `analysis.md` (zero CRITICAL, 100% coverage) and `converge.md` pass 1 against the
      plan's traceability rows; mark each row with its declared method.
- [X] T016 Fold the modified `projector/R14` block into `docs/spec/projector.md`, update the
      capability header, and write `fold.md` with the before/after counts. This is the first commit.

## Phase 6 — Delivery (owner's words only)

- [X] T017 Open card `ITEM-264` with `bump: patch`, add its board row and set the card's `spec:`;
      this is the pre-merge delivery commit alongside the version and changelog line.
- [X] T018 On `push`: push the branch, open the draft PR, then move `ITEM-264` to `In review` as
      its own commit with `status` and `pr:`; run the full browser suite and compare failures with
      the base when red.
- [X] T019 On `merge`: apply the version `1.37.5` and changelog line, close the card as `Done` with
      `closed_at`, `closed_reason` and the board's `develop via [#N]` row in the pre-merge delivery
      commit, update the PR body in place, then squash-merge with that same body.
