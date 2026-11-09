# Tasks: song verse editing on the song page

**Spec**: `specs/189-song-verse-editing/spec.md`
**Branch**: `feat/189-song-verse-editing`

> Ordered by user story: Setup → Foundational → US1 → US2 → US3 → US4 → US5 → Polish.
> `[P]` = order-independent, not concurrent: one agent in one thread, and the run states the order it actually used.
> TDD: rows declared `test` become test-then-implement pairs (C-SDD-TDD); `inspection` rows produce no test tasks.

## Setup

- [X] T001 [P] Create `multimedia/web/reading/verses.py` and register `POST /editor/verse/new/save/`, `POST /editor/verse/<pk>/save/`, `POST /editor/verse/<pk>/delete/`, `POST /editor/verse/reorder/` in `multimedia/web/reading/urls.py` with CSRF + ordinary-book + live-song guards.

## Foundational

- [X] T002 Narrow `songs.Verse.unique_together` to live rows (partial unique on `(song, number)` where `is_deleted=False`) and add `multimedia/songs/test_migrations.py` coverage for tombstone collision.
- [X] T003 Write failing test `multimedia/tatib/tests.py::test_migration_maps_numbers_to_ids` for the number→ID migration (fixture of ten entries) and make it pass with `multimedia/tatib/migrations/xxxx_verse_refs_to_ids.py`.
- [X] T004 [P] Refactor `ServiceEntry.resolve()` (`multimedia/tatib/models.py`) and `multimedia/web/reading/views.py` `_verse_lines`/stage sites from `number__in` to `pk__in` ordered by `number`; update `multimedia/web/reading/entries.py` picker value→ID, label→current number, and summary `Verses 1, 3`.

## US1 — Add a verse on the song page

- [X] T005 [P] Write failing Playwright E2E `tests/e2e/test_song_verse_verbs.py::test_add_verse_appends` (fixture song → `Add verse` → save → fourth verse `#4`, no reload) and make it pass: `song.html` add row + endpoint `POST /editor/verse/new/save/`.

## US2 — Edit a verse on the song page

- [X] T006 [P] Write failing E2E + view test `tests/e2e/test_song_verse_verbs.py::test_edit_keeps_number` and `multimedia/web/reading/tests.py::test_edit_verse_keeps_number`, make pass: hover glyphs + gutter yield in `song.html`, edit modal titled `Edit verse n` prefilled, save replaces lyric only.

## US3 — Reorder the verses (ghost + frozen mids + live cursor)

- [X] T007 Write failing E2E `tests/e2e/test_song_verse_drag.py::test_slot_follows_live_cursor_not_origin` (current cursor crossing each frozen middle moves slot; origin anchoring fails the check), then implement `static/web/songs/verses.js` ported from `static/web/reorder.js`: `makeGhost`/`positionGhost`, frozen mids at grab, placeholder tint + hidden contents, others morph via CSS (160/60ms), 3px dead zone, edge auto-scroll, one last placement on release Y.
- [X] T008 [P] Write failing view test `multimedia/web/reading/tests.py::test_reorder_writes_order` and make pass: `POST /editor/verse/reorder/` renumbers live rows 1…n exactly; membership mismatch → whole refusal.

## US4 — Remove a verse, only when unreferenced

- [X] T009 Write failing tests `multimedia/web/reading/tests.py::test_delete_refused_when_referenced` and `::test_delete_soft_and_renumbers`, make pass: disabled Delete + count line in edit modal, confirm, soft-delete + renumber 1…n.

## US5 — A prepared service keeps its lyrics

- [X] T010 Write failing test `multimedia/tatib/tests.py::test_entry_survives_four_verbs` (add/edit/reorder all keep lyric text, label follows current number), make pass; covered partially by T003/T004.

## Polish

- [X] T011 [P] Endpoint hardening test `multimedia/web/reading/tests.py::test_verse_endpoints_enforce` (hymn 403 ×4, CSRF, permutation, song match, blank lyric) + `test_write_leaves_other_fields` + `test_numbers_stay_1_to_n_after_each_verb` + hymn-zero-controls render test.
- [X] T012 [P] SC-007 check `multimedia/tatib/tests.py::test_migration_maps_numbers_to_ids` already done in T003; SC-001/002/003 walked by `tests/e2e/test_song_verse_verbs.py` cases; measure live numbers: collapsed 44px, gutter 41.6, ghost `from→now` in 41.6px, seams exact, auto-scroll 72px.
