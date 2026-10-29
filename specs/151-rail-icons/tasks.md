# Tasks: the rail says what each section is, and its marks are the stage's own

**Spec**: `specs/151-rail-icons/spec.md`
**Plan**: `specs/151-rail-icons/plan.md`
**Verification split**: 7 test · 5 inspection · 2 manual

## Phase 1 — Setup

- [ ] T001 Confirm the shipped state before touching anything: open
  `specs/151-rail-icons/preview/preview.html` and read the **Now — develop** column at 1:1 — the rail's
  open book, the stage's single flagged note, the audio chip's beamed pair, the panel's page-with-lines.
  No setup task exists: no dependency, no ignore-file change, no route.

## Phase 2 — Foundational

All seven cases live in one new file because they all read the same page; they are written and run
**red** before the markup changes (TDD-01).

- [ ] T002 [P] Write `tests/e2e/test_rail_marks.py::RailMarksE2ETests` with the fixtures the stage needs
  — a Bible edition with a book and verses, a hymn book with a song, a Tata Ibadah service carrying a
  scripture entry, a song entry and an **audio** media entry — plus a second, empty service for the
  add tiles. Helpers: `rail_paths()` (destination → its `d` strings), `kind_path(kind)`,
  `tile_path(label)`, `family_path(family)` (via `window.gkpsMediaIcon`).
- [ ] T003 [P] [US1] Write `test_the_rail_bible_and_a_passage_draw_one_path`: the rail's Alkitab path,
  the passage row's kind mark and the Add Passage tile are string-identical, and the path carries the
  cross (`M12 2.6v4.6M10.1 4.5h3.8`).
- [ ] T004 [P] [US2] Write `test_the_rail_service_is_a_clipboard`: the rail's Tata Ibadah svg holds two
  `rect`s and the three rules, carries no page path, and its total path set differs from
  `gkpsMediaIcon('pdf')`.
- [ ] T005 [P] [US3] Write `test_the_rail_note_and_a_song_draw_one_path` (rail Kidung = song kind mark =
  Add Song tile) and `test_an_audio_file_is_a_waveform_in_every_place_it_is_drawn` (the waveform path
  equals `gkpsMediaIcon('audio')` and the stage's audio chip; `image`, `video`, `pdf`, `slides` and
  `missing` still equal the strings this slice ships with).
- [ ] T006 [P] [US4] Write `test_the_five_rail_marks_are_five_shapes_and_none_is_a_media_family`
  (five buttons in order, five distinct path sets, no string in common with the family map),
  `test_the_marks_keep_their_boxes` (44 × 44 button, 24 × 24 glyph at the same x; kind mark 20 × 20 at
  row + 24 with the title at +64; chip 42 × 42 with a 23 × 23 glyph; row heights 56 and 80) and
  `test_the_marks_keep_their_ink_in_both_themes` (each mark's computed `color` equals its own element's
  colour token, no `fill`, `aria-hidden="true"`).
- [ ] T007 Run all seven against the **unmodified** templates and record the red output in
  `analysis.md`'s History: the rail still draws the old open book, the song row the single note, the
  audio family the beamed pair — each case failing on its own assertion, not on an import or a selector.

## Phase 3 — US1 (P1) 🎯 MVP · the Bible

**Goal**: one Bible drawing in the rail, on a passage row and on the Add Passage tile.
**Independent test**: T003 green.

- [ ] T008 [US1] `multimedia/web/templates/reading/base.html:88-92` — the rail's Alkitab mark becomes
  BIBLE; the `<svg>` keeps its attributes and its button untouched.
- [ ] T009 [US1] `base.html:256-261` — the panel's empty-state Bible mark becomes BIBLE.
- [ ] T010 [US1] `multimedia/web/templates/reading/_entry_kind_icon.html:4` — the `scripture` branch
  becomes BIBLE; the `{% else %}`/`song` branch is not touched in this phase.
- [ ] T011 [US1] `multimedia/web/templates/reading/tatib.html:200` and `static/web/entries.js:65` — the
  Add Passage tile and `EMPTY_ADD_ICONS.scripture` become BIBLE.
- [ ] T012 [US1] Re-run T003: green.

## Phase 4 — US2 (P1) · the service order

**Goal**: the rail's Tata Ibadah mark stops reading as a file.
**Independent test**: T004 green.

- [ ] T013 [US2] `base.html:119-123` (rail) and `base.html:251-256` (panel empty state) become
  CLIPBOARD.
- [ ] T014 [US2] Re-run T004: green.

## Phase 5 — US3 (P1) · songs and audio

**Goal**: one note wherever a song is drawn, and an audio file that is not a note.
**Independent test**: T005 green.

- [ ] T015 [US3] `_entry_kind_icon.html:4` — the `song` branch becomes SONG (the pair); its comment is
  unchanged.
- [ ] T016 [US3] `static/web/media-stage.js:6` — `paths.audio` becomes AUDIO (the waveform); the
  `missing` path and `renderRow` are untouched.
- [ ] T017 [US3] `$PY manage.py collectstatic --noinput`, restart the dev server, then re-run T005:
  green.

## Phase 6 — US4 (P2) · nothing else moves

**Goal**: every box and every ink is the shipped one.
**Independent test**: T006 green, and `tests.e2e.test_stage_kind_marks` still green untouched.

- [ ] T018 [US4] Re-run T006; then run `tests.e2e.test_stage_kind_marks` in full — spec 144's geometry
  and contrast cases must pass against the new paths without a single edit to that file.
- [ ] T019 [US4] `inspection` — the diff adds no `fill`, `style`, `width`, `height`, `tabindex` or event
  attribute, and no stylesheet line changed.
- [ ] T020 [US4] `manual` — at 1440px, both themes: the rail's five marks, a stage row's kind mark on
  hover, and an audio chip in its available, missing and unavailable states. Then 1024px (64px rail,
  20px marks) and 425px (the menu drawer beside the section names).
- [ ] T021 [US4] `manual` — a stage holding both a song and an audio file: the two silhouettes are told
  apart at 1:1.

## Phase 7 — Polish

- [ ] T022 Regenerate the preview (`build_preview.py`) so it draws the implemented paths, and replace
  its `GLYPHS` table with the shipped strings.
- [ ] T023 `inspection` — `docs/spec/reading.md` R25 and the new R27 are folded (Converge → Fold), with
  the capabilities' before/after counts in `fold.md`.
- [ ] T024 `VERSION` minor bump, `CHANGELOG.md` entry, board card `ITEM-…` closed by its own PR, and the
  slice's PR body written from the spec.
