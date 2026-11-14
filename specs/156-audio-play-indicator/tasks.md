# Tasks: The audio projector screen shows its play/pause control

**Spec**: `specs/156-audio-play-indicator/spec.md`
**Plan**: `specs/156-audio-play-indicator/plan.md`
**Verification split**: 11 test · 5 inspection · 0 manual

## Phase 1 — Setup

- [X] T001 Cut the slice: `git worktree add ../multimedia-gkps-klender-156 -b feat/156-audio-play-indicator develop`; spec 156 was free across the open branches. The card number was not: slice 155 claimed ITEM-164 while this slice was in flight, so the card was renumbered to **ITEM-169** at delivery.
- [X] T002 Write the card `backlog/items/ITEM-169-audio-play-indicator.md`, its `Speccing` row in `backlog/board.md`, and the `specs/README.md` index row.

## Phase 2 — Foundational

- [X] T003 `static/styles/design/projector.css`: give `.screen__audio-box` `position: relative; z-index: 3; pointer-events: none` so the screen's own content can sit above `.mouse-zones` (research D002). Blocks both stories.

## Phase 3 — US1 (P1) 🎯 MVP — the control shows the state and hides with the chrome

**Goal**: a painted 48×48 play/pause control whose mark follows the audio and whose visibility follows the chrome.
**Independent test**: open the live route at the audio entry; pause → triangle; play → bars; wait 3.5 s → control gone, bar dimmed; move the pointer → control back with bars.

- [X] T004 [P] [US1] Write the failing test `test_projector_audio_control_hides_as_the_chrome_settles_and_returns` in `tests/e2e/test_audio_display.py` — red on the base code: `::before` `border-left` reads `0px` where `12px` is asserted.
- [X] T005 [US1] `projector.css`: the control's box, radius, colours, cursor, glyphs (D004) and the idle rule restored (D005) — make T004 pass.
- [X] T006 [US1] `projector.css`: `pointer-events: auto` on the control so the pointer can reach it at all once the box is inert.

## Phase 4 — US2 (P1) — a click reaches the control

**Goal**: clicking the control toggles playback on the projector, including its first click in a windowed page.
**Independent test**: click the control once in a windowed projector: the audio plays, the page stays windowed.

- [X] T007 [P] [US2] Write the failing test `test_projector_audio_control_is_painted_and_toggles` in `tests/e2e/test_audio_display.py` — red on the base code: the element is reported hidden (0×0) before any click.
- [X] T008 [US2] `projector.js:909–921`: return early when the click's target is inside `[data-audio-play]`, so the fullscreen gesture does not consume it (D003) — make T007 pass.

## Phase 5 — Polish

- [X] T009 `specs/156-audio-play-indicator/preview/measure.py`: read the control, bar, times and player boxes in paused / playing / idle / returned at 1920×1200, 1280×800 and 640×480; record them in `plan.md` and the spec's `## UI/UX`.
- [X] T010 Run `manage.py test tests.e2e.test_audio_display` on a throwaway database (`gkps156`) and record that `test_untitled_preview_and_projector_idle_display_off` is red on `develop` too (ITEM-140).
- [X] T011 Inspection rows from `plan.md`: FR-006 (diff scope), SC-004 (geometry table re-read), ended, reduced motion, 1280/640.
- [X] T012 Fold `projector/R4` into `docs/spec/projector.md` (header, requirement, five scenarios) and write `fold.md`.
- [ ] T013 Delivery, after the push: `VERSION` 1.22.10 → 1.22.11, one `## [Unreleased]` changelog line, the card `done` with `bump: patch` and its board row moved, then the PR body.

## Phase 6 — Convergence

<!-- written by Converge only; absent until it runs -->
