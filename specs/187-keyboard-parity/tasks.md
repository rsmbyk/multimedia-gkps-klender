# Tasks: one keyboard grammar for the dock and the projector

**Spec**: `specs/187-keyboard-parity/spec.md`
**Plan**: `specs/187-keyboard-parity/plan.md`
**Verification split**: 25 test · 2 inspection · 0 manual

Tasks are test-first: each story opens with its red test, then the code that turns it green. Nothing is
committed here — the first commit comes at Fold, on a green tree (C-TDD-GIT).

## Phase 1 — Setup

- [ ] T001 Create `tests/e2e/test_dock_keys.py` with the suite's fixtures copied from `test_dock_goto.py`
      (a service with a song and a text entry, a `StaticLiveServerTestCase`, one browser context).
- [ ] T002 Create `tests/e2e/test_projector_keys.py` with the projector's fixture (a service, the sheet
      button, a 1920 × 1080 context and a 1280 × 720 one).

## Phase 2 — Foundational

- [ ] T003 [P] Red test in `tests/e2e/test_goto_shared_state.py`:
      `test_a_picker_go_to_writes_no_service_and_back_idles` — `goTo` writes `{service: null, goto}`,
      `back` writes `{service: null, on: false, goto: null}`.
- [ ] T004 `static/web/display.js`: `gotoOf` accepts a goto with `service === null`; `goTo`, `stepGoto`,
      `hide`, `resume`, `flip` act on it; `back` writes the idle state (FR-003).
- [ ] T005 Make T003 green; assert the write count and the one channel message per verb.

## Phase 3 — US1 (P1) 🎯 MVP — the held `Esc`

**Goal**: a tap of `Esc` in the runner moves nothing; a 900 ms hold returns to the picker.
**Independent test**: dispatch keydown over the runner, wait 300 ms, keyup — the view is the runner;
hold 1000 ms — the picker shows and the service is still on air where it stood.

- [ ] T006 [P] [US1] `test_a_tap_of_escape_does_nothing_and_a_hold_returns_to_the_picker` in
      `tests/e2e/test_dock_keys.py` (SC-001).
- [ ] T007 [P] [US1] `test_escape_still_closes_the_band_and_the_sheet_on_the_tap` (US1/AC4-5).
- [ ] T008 [US1] `static/web/obs-dock.js`: replace the `Esc` branch with a 900 ms timer that is cancelled
      by keyup, window blur and any layer opening; the band and the sheet keep the tap (FR-001).

## Phase 4 — US2 (P1) — `G` on the picker, and a go to that stands alone

**Goal**: `G` opens the band over the picker; a chosen result goes on air with no service; `Back` idles
every surface and returns the dock to the picker.
**Independent test**: on the picker, `G`, type `NKB 43`, `Enter` — the song is on air, the state names
no service, the dock shows the block alone; `Back` — all three idle, the picker is back.

- [ ] T009 [P] [US2] `test_g_opens_the_band_on_the_picker` (FR-002, US2/AC1).
- [ ] T010 [P] [US2] `test_the_picker_go_to_stands_alone_and_back_returns_to_the_picker` (FR-004,
      US2/AC2-4).
- [ ] T011 [P] [US2] `test_the_picker_never_adopts_a_service` (US2/AC5) — no `show` is written.
- [ ] T012 [US2] `static/web/obs-dock.js`: the picker branch calls `openFind`; `chooseFind` writes the go
      to without adopting a service when the view is the picker; the runner shows the block alone and
      `Back` returns to the picker (FR-002, FR-004).
- [ ] T013 [US2] `static/web/projector.js` `renderDetour` and `static/web/obs-overlay.js` `sync`/`plate`:
      paint a go to with `service: null` (FR-011); `back` paints nothing.
- [ ] T014 [P] [US2] `test_the_overlay_paints_a_service_less_go_to` in `test_goto_shared_state.py`
      (SC-009).

## Phase 5 — US3 (P1) — the go to steps like the projector's

**Goal**: the dock's go-to chords are the projector's, with one fetch per crossing and none inside a
loaded chapter.
**Independent test**: from `Matius 5:3`, `Shift+→` fetches the next chapter once; `Ctrl+→` the next book
once; a plain step fetches nothing and lands on the same place the projector lands on.

- [ ] T015 [P] [US3] `test_the_go_to_steps_like_the_projectors_chords` (FR-005, US3/AC1-2).
- [ ] T016 [P] [US3] `test_a_chapter_crossing_fetches_once_and_a_verse_step_none` (SC-003).
- [ ] T017 [US3] `static/web/obs-dock.js`: a `requestPassage` twin over
      `GKPSProjectorLibrary.movePassage`/`fetchChapter`; `stepUnit` and `edgeOf` route plain/shift/ctrl
      to verse, chapter and book; a song go to keeps its bait step and ignores `Ctrl` (FR-005).
- [ ] T018 [US3] `static/web/display.js`: `stepGoto` accepts the position the dock computes after a
      crossing (no new field).
- [ ] T019 [US3] Extend `test_goto_shared_state.py`:
      `test_the_dock_and_the_projector_land_on_the_same_go_to_place` over six chords (SC-004).

## Phase 6 — US4 (P2) — the picker moves on `↑` and `↓` only

- [ ] T020 [P] [US4] `test_the_picker_moves_on_up_and_down_only` (FR-006, SC-005).
- [ ] T021 [US4] `static/web/obs-dock.js`: the picker branch accepts `↑`/`↓`, `Enter`, `G`; `←`, `→`,
      `PgUp`, `PgDn`, `Home`, `End` are inert.

## Phase 7 — US5 (P2) — `K` shows the dock's own shortcuts

- [ ] T022 [P] [US5] `test_k_opens_the_sheet_and_the_picker_group_rides_with_the_view` (FR-007,
      FR-008, SC-006).
- [ ] T023 [P] [US5] `test_the_sheet_is_a_layer_and_closes_on_its_frame` (FR-007, SC-006).
- [ ] T024 [US5] `multimedia/web/templates/reading/obs_dock.html`: the `.keysheet` section with its
      five groups, the picker group first and `data-keys="pick"`, every control `tabindex="-1"`;
      `static/web/obs-dock.js`: `setKeysOpen`, the `K` toggle, `Esc`/close/frame-click closing, the
      picker group's `hidden` following `data-view` (FR-007, FR-008).
- [ ] T025 [US5] `static/styles/design/obs-dock.css`: the sheet, its rows, caps, headings, scrollbar
      and the ␣ space cap, to the preview's measured numbers (`## UI/UX`).

## Phase 8 — US6 (P2) — no input changes what is on air while a go to fetches

- [ ] T026 [P] [US6] `test_no_key_changes_what_is_on_air_while_a_go_to_fetches` (FR-009, SC-007).
- [ ] T027 [US6] `static/web/obs-dock.js`: a `gotoBusy` raised around `fetchGoto` and the passage step,
      gating the key handler and the transport/row clicks; the header reads `Loading…` until it settles.

## Phase 9 — US7 (P2) — `⌘` is a modifier on the projector too

- [ ] T028 [P] [US7] `test_meta_and_control_are_the_same_modifier` (FR-010, SC-008).
- [ ] T029 [P] [US7] `test_meta_with_a_letter_keeps_the_browsers_shortcut` (US7/AC3).
- [ ] T030 [US7] `static/web/projector.js`: `ctrl = ctrlKey || metaKey` for the arrows and `Home`/`End`;
      the plain `metaKey` return moved so `⌘+letter` reaches the browser.

## Phase 10 — US8 (P2) — Home and End act on the unit on show

- [ ] T031 [P] [US8] `test_home_and_end_act_on_the_bait_or_entry` (FR-012, SC-010).
- [ ] T032 [P] [US8] `test_shift_home_does_nothing_on_a_text_entry` (US8/AC3).
- [ ] T033 [US8] `static/web/obs-dock.js` `edgeOf`/`stepUnit`: the plain chord takes the live bait's or
      entry's ends, `Shift` the live entry's baits and nothing on an entry without, `Ctrl`/`⌘` the
      service's entries; a blank trailing rest is skipped; between entries nothing moves.

## Phase 11 — US9 (P2) — one Display group and one Find group on both sheets

- [ ] T034 [P] [US9] `test_the_sheet_carries_one_display_group_and_one_find_group` in
      `test_projector_keys.py` (FR-013, US9/AC1-2).
- [ ] T035 [P] [US9] `test_the_sheet_orders_find_prev_next_open_empty_close` (US9/AC2).
- [ ] T036 [US9] `projector_controls.html`: display, find and fullscreen sections become one `Display`
      group; *While Finding* becomes `Find` and its rows take the new order; the dock's sheet keeps the
      same two groups (FR-013).

## Phase 12 — US10 (P2) — the media groups sit with the service

- [ ] T037 [P] [US10] `test_audio_and_video_are_one_group_in_the_left_column` (FR-014, SC-011).
- [ ] T038 [P] [US10] `test_the_sheet_grows_to_its_tallest_column_and_scrolls_at_720` (US10/AC4).
- [ ] T039 [US10] `projector_controls.html`: Audio and Video become one `Audio and Video` group with one
      `Play/Pause` row; it and `Image and PDF` move to the end of the first `.stack`.
- [ ] T040 [US10] `static/styles/design/projector.css`: `.sheet`'s frame follows its tallest column
      (835.5 px at 1080p) and scrolls at 720p instead of clipping.

## Phase 13 — US11 (P2) — the find band keeps the keyboard

- [ ] T041 [P] [US11] `test_the_band_keeps_the_keyboard_when_the_window_returns` (FR-015, SC-012).
- [ ] T042 [US11] `static/web/obs-dock.js`: `openFind` focuses the field; a window `focus` and a
      `visibilitychange` to visible refocus it while the band is open; the panel's `pointerdown` park
      and the outside-`focusin` park choose the field while the band is open; closing returns the panel;
      the field is focused only when enabled.

## Phase 14 — Polish

- [ ] T043 The dock's key table comment (`obs-dock.js:14-25`) is replaced by a pointer to the sheet,
      so the comment and the markup cannot drift.
- [ ] T044 Run the four dock/projector modules and the two extended ones together; fix the reds that
      belong to this slice (the known-red tests on `develop` stay listed in the board's Backlog).
- [ ] T045 Re-run `preview/probe.py`; the preview's numbers and the implemented sheet agree.

## Phase 15 — Convergence

<!-- written by Converge only; absent until it runs -->
