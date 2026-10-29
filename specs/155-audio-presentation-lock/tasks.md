# Tasks: a playing recording owns the projector screen until it pauses

**Spec**: `specs/155-audio-presentation-lock/spec.md`
**Plan**: `specs/155-audio-presentation-lock/plan.md`
**Verification split**: 16 test · 1 inspection · 0 manual

## Phase 1 — Setup

- [x] T001 `backlog/items/ITEM-164-audio-presentation-lock.md`, its Backlog row in `backlog/board.md`
      and the `specs/README.md` row — written with the Draft pack, before any code.
- [x] T002 `specs/155-audio-presentation-lock/preview/README.md` and `preview/probe_lock.py` — the live
      preview's run recipe and the harness that reads every requirement back off the route.

## Phase 2 — Foundational

- [x] T003 [P] Eight cases in the existing `AudioDisplayE2ETests` class of
      `tests/e2e/test_audio_display.py`, written red-first:
      `test_projector_playing_audio_locks_navigation`,
      `test_projector_playing_audio_ignores_pointer_navigation`,
      `test_projector_playing_audio_keeps_go_to_shut`,
      `test_projector_playing_audio_enters_fullscreen`,
      `test_projector_pausing_audio_returns_the_screen`,
      `test_projector_escape_leaves_fullscreen_and_pauses_audio`,
      `test_projector_audio_end_returns_the_screen`,
      `test_projector_refused_fullscreen_still_locks_audio`.
- [x] T004 Run the module against the base and record the red output: each case fails on the behaviour
      it names (a screen that moved, a fullscreen that never happened), not on a missing symbol.

## Phase 3 — US1 (P1) 🎯 MVP

**Goal**: a playing recording cannot be stepped off, from either input family.
**Independent test**: play, press every key and click every zone and cue control, and read
`data-current-screen`: it stays on the audio screen while `data-playing` stays `true`.

- [x] T005 [US1] `static/web/media-audio.js` — `onPlayRequest` in `toggle()` before `audio.play()`, and
      `pause()` on the returned handle (D002).
- [x] T006 [US1] `static/web/projector.js` — `audioPlaying()`, `requestAudioFullscreen`,
      `exitAudioFullscreen`, `syncAudioFullscreen` beside the video's three (D001).
- [x] T007 [US1] `static/web/projector.js:1266` — the keydown guard after the video fullscreen guard:
      arrow/page/home/end swallowed, `g`/`j` swallowed (FR-001, FR-003).
- [x] T008 [US1] `static/web/projector.js` — the mouse-zone handler at `:938` and the four cue handlers
      (`cueService`, `cueNext`, `baitList`, `chooseEntryList`) return while `audioPlaying()` (FR-002).
- [x] T009 [US1] `static/styles/design/projector.css` — `.screen__audio-box:fullscreen` at `100vw ×
      100vh`, `#171613` (FR-004, SC-003).
- [x] T010 [US1] Green: the four lock cases, `test_video_display.py`'s
      `test_projector_fullscreen_play_pause_and_navigation_guard` unchanged, and the existing
      `test_untitled_preview_and_projector_idle_display_off` still stopping and releasing the
      recording on a display-off (FR-009).

## Phase 4 — US2 (P2)

**Goal**: the screen comes back by itself, paused, at the same place.
**Independent test**: pause with `Space`, hold `Escape`, and let a recording end — three times back on
the normal screen.

- [x] T011 [US2] `static/web/projector.js` — `onPlayback` fanning out to `audioActivity()` and
      `exitAudioFullscreen()`, and `syncAudioFullscreen` registered on `fullscreenchange` (FR-005,
      FR-006, FR-007).
- [x] T012 [US2] Green: `test_projector_pausing_audio_returns_the_screen`,
      `test_projector_escape_leaves_fullscreen_and_pauses_audio`,
      `test_projector_audio_end_returns_the_screen`.

## Phase 5 — US3 (P3)

**Goal**: a browser that refuses fullscreen is not the one place a stray key kills a recording.
**Independent test**: deny `Element.prototype.requestFullscreen`, play, press the keys and click the zones.

- [x] T013 [US3] Green: `test_projector_refused_fullscreen_still_locks_audio`, with the guards keyed on
      `audioPlaying()` rather than on the fullscreen element (D003, FR-008).

## Phase 6 — Polish

- [x] T014 `VERSION` 1.22.10 → 1.22.11 and the `CHANGELOG.md` line, in the same commit as the card's
      `bump: patch`.
- [x] T015 `backlog/items/ITEM-164-audio-presentation-lock.md` — `status: in review`, `pr:` once the PR
      number exists; board row moved to `In review` with the PR link.
- [x] T016 FR-010 read back by inspection: the keydown guard lists no `c` or `t`, and both handlers sit
      below it reading nothing from the audio state.

## Phase 7 — Convergence

- [x] T018 Read every requirement back: `tests/e2e/test_audio_display.py` (12 of its 13 cases green;
      the 13th is ITEM-140's pre-existing stop-broadcast red), `tests/e2e/test_video_display.py`
      (6 of 7; the failing one is the same ITEM-140 case, proven on the base), and
      `preview/probe_lock.py` 14/14 against the live route. See `converge.md`.

## Phase 8 — Fold

- [x] T017 `docs/spec/projector.md` — `R3 — A playing recording owns the projector screen until it
      pauses`, `added`, source slice 155.
