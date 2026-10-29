# Tasks: A song with no verses is named, not mistaken for no song

**Spec**: `specs/162-song-verse-empty-state/spec.md`
**Plan**: `specs/162-song-verse-empty-state/plan.md`
**Verification split**: 17 test · 3 inspection · 0 manual

## Phase 1 — Setup

- [X] T001 `tests/e2e/test_entries.py` — add `self.verse_less` to `EntryModalE2ETests.setUp`: a hymn
      song (`KJ 901`, title `Kosong`) with no `Verse` row, so the modal's new state has a real pick.

## Phase 2 — Foundational

- [X] T002 `multimedia/web/reading/entries.py` — `SongEntryForm.song_has_no_verses`: true when a song
      is chosen and the verses field has no choices. Blocks T005–T006 (the template reads it).

## Phase 3 — US1 (P1) 🎯 MVP

**Goal**: the Verses field names a picked song that has no verses, and stays disabled.
**Independent test**: New song → pick `lagu kosong` → the field reads `This song has no verses`.

- [X] T003 [P] [US1] `tests/e2e/test_entries.py` — write the failing E2E
      `test_a_song_with_no_verses_is_named_and_cannot_be_saved` for US1/AC1, AC2 and SC-001–SC-003:
      the line before any pick, then after picking, then the trigger's disabled state and 38px box.
- [X] T004 [US1] `static/web/entries.js` — give `verseSummary` the chosen song and write
      `This song has no verses` in the no-boxes branch when one is picked; update the three call
      sites. Passes T003's FR-001/FR-003 assertions.
- [X] T005 [P] [US1] `multimedia/web/tests.py` — write the failing
      `test_an_edit_form_for_a_verse_less_song_states_it_in_the_markup` for FR-002 and US1/AC4: an
      entry created through the ORM (the model refuses one through the form), then the edit route's
      fragment.
- [X] T006 [US1] `multimedia/web/templates/reading/_entry_form.html` — the summary span renders the
      statement when `form.song_has_no_verses`, and `Pick a song first` otherwise. Passes T005.
- [X] T007 [P] [US1] `multimedia/web/tests.py` — write
      `test_an_edit_form_keeps_the_verses_an_entry_stored` for the edge case: stored numbers stay
      choices, so the no-verses line does not appear (already true; the test pins it).

## Phase 4 — US2 (P2)

**Goal**: a save refusal names the song when the song is the cause.
**Independent test**: pick `lagu kosong`, press Save → the field's error names the song.

- [X] T008 [P] [US2] `multimedia/tatib/tests.py` — write the failing
      `test_a_song_entry_with_no_verses_names_the_song` for FR-004 and US2/AC1; leave
      `test_a_song_entry_keeps_at_least_one_verse` untouched for US2/AC2.
- [X] T009 [US2] `multimedia/tatib/models.py` — split the `verses` refusal by cause in
      `ServiceEntry.clean`. Passes T008 and keeps T008's sibling green.
- [X] T010 [US2] `tests/e2e/test_entries.py` — extend T003's test with the Save assertion for SC-004:
      the field's error names the song and the dialog stays open.

## Phase 5 — Polish

- [X] T011 `specs/162-song-verse-empty-state/preview/` — rebuild `preview.html` from the implemented
      form and refresh `shots/`; re-read the 420px render.

## Phase 6 — Convergence

- [X] T014 [US1] `tests/e2e/test_entries.py` — open the menu of the disabled trigger by a JS click
      and assert `#entry-verses-menu` stays hidden (FR-003's note promised it; pass 1 found it
      unproven).

## Phase 7 — Polish after Converge

- [X] T012 The full verification run: the three targeted suites green (158 unit/web tests, 3 song
      E2Es), and `tests.e2e.test_entry_pickers` run as extra evidence — red on `develop` itself, see
      `converge.md`.
- [X] T013 `VERSION` 1.22.15 → 1.22.16 and the `## [Unreleased]` line in `CHANGELOG.md` (bump:
      patch), in the delivery commit with the card's move to In review (PR #453).
