# Tasks: the overlay reads by kind

**Spec**: `specs/180-overlay-text-styles/spec.md` · **Plan**: `specs/180-overlay-text-styles/plan.md`

Ordering is SDD's; `[P]` marks order-independent work, not concurrency — one agent runs these in order. Every row the
plan declares `test` appears twice, once as the failing test and once as the change that makes it pass
(`C-SDD-TDD`).

## Phase 1 — Setup

- [X] T001 Verify the ignore files still cover the tree this slice touches — `.gitignore` hides `_static/` and the
      local database artefacts, so `git status` before and after a `collectstatic` shows no new noise.
- [X] T002 Confirm the static pipeline the overlay depends on: `DJANGO_DEBUG=False` + `collectstatic` serve
      `static/styles/design/obs-overlay.css` and `static/web/obs-overlay.js` from `_static/` (a stale tree is the most
      likely reason a change looks absent on the live page).

## Phase 2 — Foundational

- [X] T003 Write the failing payload test for the speaker column: a voiced line carries `mark` and `words` beside the
      full `text` — `multimedia/web/tests.py`, `test_a_voiced_line_carries_its_mark_and_words_apart` (FR-010).
- [X] T004 Make it pass by carrying `mark` and `words` through `_screen_lines()` in
      `multimedia/web/reading/views.py` (FR-010).
- [X] T005 Read the entry list and screen model in `static/web/obs-overlay.js` — fetch the projector page once per
      service, cache both islands, and expose `modelFor(displayState)` returning `{kind, header, lines}` or `null`.
      No painting yet (FR-001).
- [X] T006 Give the stage a `data-kind` attribute in `static/web/obs-overlay.js::paint` so the stylesheet can branch
      on the kind without a second class per element (FR-001, FR-004a).

## Phase 3 — US1: a passage is a quotation

- [X] T007 Write the failing test: a passage screen paints a plate whose kicker is the reference and whose title is the
      verse's own title, with no caption and a non-transparent fill —
      `tests/e2e/test_obs_overlay.py::test_a_passage_wears_a_plate_naming_its_reference_and_title` (FR-001, FR-003,
      SC-003).
- [X] T008 Make it pass: `plate()` in `static/web/obs-overlay.js` builds kicker, title, hairline and body from the
      screen header and lines (FR-003, FR-007).
- [X] T009 Add the passage's card in `static/styles/design/obs-overlay.css` — centred, `fit-content` between
      `min-width: 34%` and `max-width: 90%`, `.32em` corner, `.42em .65em .44em` padding (FR-005, FR-006).
- [X] T010 Write the failing test that a song screen never grows a heading —
      `test_a_song_screen_does_not_repeat_the_entry_title` (FR-002).
- [X] T011 Make it pass by keeping the caption path free of the heading (FR-002).
- [X] T012 Write the failing test that `T` repaints the plate's heading and body together —
      `test_the_translation_flip_repaints_the_plate_heading` (FR-007, SC-006).
- [X] T013 Make it pass: `paint()` prefers the shown edition's header and line when the screen carries one (FR-007).

## Phase 4 — US2: a liturgy is a script

- [X] T014 Write the failing test: a text screen paints a left-aligned panel with a leading bar, its title as the
      kicker, and a leader line quieter than the assembly's —
      `test_a_liturgy_text_wears_a_plate_with_its_title_and_quieter_leader_lines` (FR-004, FR-004a, SC-004).
- [X] T015 Make it pass: the `[data-kind="liturgy"]` block in `obs-overlay.css` — no centring, `.08em` corner,
      `.105em` bar, `1.05em` left padding — and `is-leader` · `is-assembly` · `is-join` ink (FR-004a, D007).
- [X] T016 Write the failing test for the speaker column: a wrapped liturgy line hangs under its words, and the marks
      of one screen share one column — `test_a_wrapped_speaker_line_hangs_under_its_words` (FR-010).
- [X] T017 Make it pass: `.obs-overlay__line.has-mark` as a two-column grid plus `applySpeakerColumn()` sizing
      `--speaker-col` to the widest mark on the screen (FR-010).
- [X] T018 Confirm the untitled case and the single-answer case against the preview (states 6 and 7): no empty kicker,
      no orphan hairline, and the panel keeps its 34 % floor instead of collapsing to a chip (FR-003, US2/AC4).

## Phase 5 — US3: it arrives, it leaves, it morphs

- [X] T019 Write the failing test for the panel's motion: `overlay-plate-in` at 180 ms on arrival and
      `overlay-plate-out` at 120 ms on blank, stage empty afterwards —
      `test_a_panel_enters_and_leaves_with_a_short_motion` (FR-011, SC-007).
- [X] T020 Make it pass: the two keyframe pairs and the `is-entering` / `is-leaving` classes in `obs-overlay.css`,
      with `animateIn` / `animateOut` in `obs-overlay.js` and a 600 ms settle for a throttled tab (FR-011, D005).
- [X] T021 Write the failing test for the caption's motion: the same clock with the caption's shorter travel —
      `test_a_caption_enters_and_leaves_with_the_same_clock` (FR-012).
- [X] T022 Make it pass: `overlay-caption-in` / `overlay-caption-out`, and the caption animating only when a song
      starts or ends, never between its own screens (FR-012).
- [X] T023 Write the failing test for the morph: a second screen of one passage changes the panel's measure with
      `is-resizing` and no re-entry — `test_a_second_screen_morphs_the_panel_box` (FR-013).
- [X] T024 Make it pass: `resizePlate()` pins the old width and height, releases them to the new measure on the shared
      curve, and resolves the words at 110 ms (FR-013, D006).
- [X] T025 Add the reduced-motion branch so all three motions fall back to a cut (FR-011, FR-012, FR-013).

## Phase 6 — Polish

- [X] T026 Write the failing test that the surface stays listen-only and clears on hide —
      `test_hide_empties_the_overlay_and_nothing_is_focusable` (FR-008, FR-009, SC-005).
- [X] T027 Make it pass and keep media, break and blank screens painting nothing (FR-008).
- [X] T028 Adapt `tests/e2e/test_obs_dock.py` to the exit animation: the stage is empty when the exit ends, so the
      assertion waits instead of sampling the same frame (FR-011).
- [X] T029 Build the review surfaces: `preview/overlay-preview.html` (15 states, navigable, motion on navigation),
      `preview/overlay-motion.html` (1× / ¼× / ⅛×) and `preview/overlay-sequence.html` with its walkthrough recording.
- [X] T030 Record the measured numbers into `spec.md`'s `## UI/UX` and the traceability table in `plan.md`; run
      `test_obs_overlay` + `test_obs_dock` + `web.test_obs_dock` and keep the tree green.

## Delivery

- [ ] T031 Bump `VERSION` 1.23.3 → 1.24.0 against `origin/develop` (declared `minor`), add the `CHANGELOG.md` line
      under `## [Unreleased]`, and carry the card to Done in the pre-merge commit (C-SDD-VER, BRD-07).
