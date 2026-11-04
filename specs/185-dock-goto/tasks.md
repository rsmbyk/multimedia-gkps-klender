# Tasks: the dock's Go To

**Spec**: `specs/185-dock-goto/spec.md`
**Plan**: `specs/185-dock-goto/plan.md`
**Verification split**: 36 test · 3 inspection · 0 manual

TDD is in force: every row declared `test` arrives as a failing test first and a task that makes it
pass, in that order. Ordering inside a task is TDD's; ordering between tasks is this file's.

## Phase 1 — Setup

- [x] T001 Confirm the branch and the worktree: `git branch --show-current` is `feat/185-dock-goto`,
  `VERSION` reads `1.26.2`, and `git status --short` shows only the pack. No dependency, migration or
  env var is added by this slice (FR-013), so setup has nothing to install.

## Phase 2 — Foundational

Shared by every story: the state's shape and verbs, and the readers that carry the field.

- [x] T002 [Foundational] Add `goto` to `static/web/display.js`'s `read()` and `write()` with the
  shape `contracts/display-state.md` pins, including the unparseable-go-to path.
- [x] T003 [Foundational] Add the verbs `goTo(goto)`, `stepGoto(position)` and `back()` to
  `static/web/display.js`, extend `flip()` to name whatever is on air, and end a goto from `show()`,
  `moveTo()` and `release()`.
- [x] T004 [Foundational] Post `{type: 'goto', goto}` from every goto write, and update the module's
  header comment so the message list matches the code.
- [x] T005 [Foundational] Teach `static/web/projector.js` and `static/web/obs-overlay.js`'s
  `readState()` to carry `goto` (both keep their own fixed-shape copy), without painting it yet.

## Phase 3 — US1 (P1) 🎯 The dock puts a passage or a song on air

**Goal**: `G` in the runner opens a band over the dock; a reference puts that passage or song on air;
the dock shows it as the list's live block; the layer closes on three gestures.
**Independent test**: open `/obs/dock` for a service, press `G`, type `NKB 43`, press Enter — the
block names the song, the projector paints its first lyric, and the service's own rows are gone.

- [x] T006 [P] [US1] Write the failing tests in `tests/e2e/test_dock_goto.py`:
  `test_g_opens_the_band_and_the_picker_has_no_goto` (FR-004, US1/AC1),
  `test_typing_makes_no_request` (FR-005, SC-001, US1/AC2),
  `test_no_match_says_so_and_enter_does_nothing` (US1/AC5),
  `test_the_same_lookup_answers_both_surfaces` (SC-006).
- [x] T007 [US1] Make T006 pass: the runner's head gains the Go To control (`.iconbtn`, 38 px, `G`),
  `openFind()` injects `static/web/projector-library.js` on first use and `load()`s the index,
  `refreshFind()` answers from page memory and paints `n / n`, the picker view never offers it, and
  the labels and order for a fixed set of queries are the projector's own (SC-006).
  Files: `multimedia/web/templates/reading/obs_dock.html`, `static/web/obs-dock.js`.
- [x] T008 [P] [US1] Write the failing test `test_choosing_fetches_once_and_steps_stay_local` in
  `tests/e2e/test_dock_goto.py` (FR-006, SC-001, US1/AC3).
- [x] T009 [US1] Make T008 pass: `chooseFind()` fetches one chapter or song, writes the goto at its
  first screen or verse, and steps inside the loaded chapter make no request. Same files as T007.
- [x] T010 [P] [US1] Write the failing test `test_the_block_replaces_the_service_rows` in
  `tests/e2e/test_dock_goto.py` (FR-007, FR-017, US3/AC2, US3/AC3).
- [x] T011 [US1] Make T010 pass: `renderBlock()` draws the pinned header (label, `Back`) and the
  goto's rows — song bait heads + screens, passage verses — full-bleed from the list's 8 px padding,
  with the live row tinted; `renderList()` draws nothing of the service while the block is up; no
  row wears an `On screen` pill. Files: `static/web/obs-dock.js`,
  `static/styles/design/obs-dock.css` (`.offblock`, `.offstrip`, `.offstrip__back`).
- [x] T012 [P] [US1] Write the failing test `test_the_layer_closes_on_escape_click_and_empty_backspace`
  in `tests/e2e/test_dock_goto.py` (FR-018, US1/AC4).
- [x] T013 [US1] Make T012 pass: `.findscrim` over the head and list in `--backdrop`, the foot band
  above it, a click anywhere on the layer closing the band, `Backspace` on an empty field closing it,
  the transport keys inert while it is open, and the 200 ms height morph between the transport row
  and the band. Files: `static/web/obs-dock.js`, `static/styles/design/obs-dock.css`
  (`.findband`, `.findfield`, `.findresult`, `.findcount`, `.bandswap`).

## Phase 4 — US2 (P1) One state, three surfaces

**Goal**: a goto started anywhere is on air everywhere, and a surface opened mid-goto catches up.
**Independent test**: start a goto from the projector's `G`; the dock shows its block, the overlay
paints its words, and the dock's arrows step all three.

- [x] T014 [P] [US2] Write the failing tests in `tests/e2e/test_goto_shared_state.py`:
  `test_the_three_surfaces_agree_at_every_step` (US2/AC1, SC-003),
  `test_a_surface_opened_mid_goto_catches_up` (FR-014, US2/AC3).
- [x] T015 [US2] Make T014 pass: `static/web/projector.js` renders the detour from the state
  (`detour` becomes the payload for the state's current goto), `static/web/obs-overlay.js` paints a
  song goto as the caption and a passage goto as the plate, and both paint it on their first load.
- [x] T016 [P] [US2] Write the failing test `test_the_dock_follows_a_goto_started_on_the_projector`
  in `tests/e2e/test_goto_shared_state.py` (FR-010, US2/AC4).
- [x] T017 [US2] Make T016 pass: the projector's `openDetour()` writes the state before it paints,
  its `leaveDetour()` calls `back()`, and the cue keeps its present look and its `back to …` label.
  File: `static/web/projector.js`.
- [x] T018 [P] [US2] Write the failing test `test_a_goto_stops_a_playing_recording` in
  `tests/e2e/test_goto_shared_state.py` (FR-012).
- [x] T019 [US2] Make T018 pass: a goto arriving over the channel while a recording owns the
  projector stops it and paints; the projector's own `G` stays refused while the recording plays.
  File: `static/web/projector.js`.

## Phase 5 — US3 (P1) Back restores the service exactly

**Goal**: Back lands on the screen and edition that stood before the goto, whatever happened during.
**Independent test**: service on screen 12 with SIM, step a goto and flip its edition, press Back —
screen 12 with SIM, the block gone, the cue naming the service entry.

- [x] T020 [P] [US3] Write the failing tests in `tests/e2e/test_dock_goto.py`:
  `test_back_restores_the_service_screen_and_edition` (FR-008, SC-002, US3/AC1),
  `test_the_transport_steps_the_goto_not_the_service` (FR-015, US2/AC2).
- [x] T021 [US3] Make T020 pass: `back()` clears the goto and every surface repaints the service;
  `stepUnit()`, `edgeOf()`, the bait chips and `flipEdition()` read and write the goto while one is
  up; `blankBtn` toggles `on` for what is on air. Files: `static/web/display.js`,
  `static/web/obs-dock.js`.
- [x] T022 [P] [US3] Write the failing test `test_a_block_row_moves_the_goto_and_show_ends_it` in
  `tests/e2e/test_dock_goto.py` (FR-009).
- [x] T023 [US3] Make T022 pass: a block row writes the goto's position instead of ending it, and a
  `show`/`moveTo` clears the goto before the service screen goes up. Files: `static/web/display.js`,
  `static/web/obs-dock.js`.
- [x] T024 [P] [US3] Write the failing test `test_switch_service_is_disabled_while_a_goto_is_up` in
  `tests/e2e/test_dock_goto.py` (FR-019).
- [x] T025 [US3] Make T024 pass: `sync()` disables `#switchBtn` while a goto is up (opacity .45, no
  hover fill, default cursor) and restores it the moment the goto ends. Files: `static/web/obs-dock.js`,
  `static/styles/design/obs-dock.css`.

## Phase 6 — US4 (P2) The go to lives exactly as long as the display state

**Goal**: the goto dies with the browser session, survives closing every surface, and takes
`hide`/`release` like a service screen.
**Independent test**: put a goto on air, reopen every surface in the session (still there); clear the
session marker (every surface idle).

- [x] T026 [P] [US4] Write the failing tests in `tests/e2e/test_goto_shared_state.py`:
  `test_restart_paints_no_goto` (FR-003, SC-004, US4/AC1),
  `test_release_ends_the_goto` (US4/AC2),
  `test_hide_during_a_goto_keeps_the_place` (US4/AC3).
- [x] T027 [US4] Make T026 pass: nothing new is stored — the goto rides the state's stamp; `release`
  clears it; `hide` keeps it at its place with `on: false` and every surface paints nothing.
  Files: `static/web/display.js`, `static/web/obs-dock.js`, `static/web/obs-overlay.js`.
- [x] T028 [P] [US4] Write the failing test `test_a_goto_can_start_with_nothing_on_air` in
  `tests/e2e/test_dock_goto.py` (FR-016).
- [x] T029 [US4] Make T028 pass: choosing with nothing on air adopts the browsed service at its
  first screen underneath the goto, so Back has a place to land. File: `static/web/obs-dock.js`.

## Phase 7 — Polish

- [x] T030 The dock at 320 and 520, and in the light theme: the block's header, the label's
  ellipsis and the `Back` control hold their boxes (the numbers are in `spec.md`'s `## UI/UX`).
  Files: `static/styles/design/obs-dock.css`.
- [x] T031 Remove the projector's private goto memory: `returnScreen` and any branch that treats
  `detour` as the source of truth, leaving one reader of the state. File: `static/web/projector.js`.
- [x] T032 Update the pack's preview README if any ported rule differs from what the probe prints,
  and re-run all three preview probes.
- [x] T033 Run the neighbouring E2E modules the slice touches — `tests.e2e.test_display_session`,
  `tests.e2e.test_entries` — and record any difference from the base in `converge.md`.
- [ ] T034 Delivery: board row and card state, `VERSION` 1.26.3 and the `## [Unreleased]` line, the
  PR title and body — in the same PR as the work, per the repo's chain.

## Phase N+1 — Convergence

<!-- written by Converge only; absent until it runs -->
