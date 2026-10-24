# Tasks: A song page cites its songbook by its short name

**Spec**: `specs/126-songbook-short-header/spec.md`
**Plan**: `specs/126-songbook-short-header/plan.md`
**Verification split**: 19 test · 1 inspection · 0 manual

## Phase 1 — Setup

- [x] T001 [P] `n/a — no project, dependency or toolchain is added: both files exist, and the venv, the
      local database and the Playwright Chromium build are already in place.`

## Phase 2 — Foundational

- [x] T002 `n/a — nothing is shared beyond Phase 3's pins: the header has one producer per renderer and no
      other surface reads it.`

## Phase 3 — US1 (P1) 🎯 MVP

**Goal**: a hymn song's header names the song by its short reference — `PKJ 4`, `KJ 24A`, `HAL 101`, and the
tab names it the same way.
**Independent test**: T003 alone — open a hymn song page and read the header paragraph.

- [x] T003 [US1] Add `test_song_detail_header_cites_the_short_songbook_reference` to
      `multimedia/web/tests.py::ReadingViewTests`: request the song route and assert the rendered paragraph
      `<p class="read__eyebrow" id="readEyebrow">NKB 12</p>` (the *paragraph*, not a bare `assertContains`
      of `NKB 12`, which the sidebar row satisfies too). **Red today**: `Nyanyikanlah Kidung Baru 12`.
- [x] T004 [US1] Add `test_a_sub_number_follows_the_short_reference` to the same class: create
      `Song(book=nkb, number=12, sub_number='b')` and assert `NKB 12B`. **Red today**:
      `Nyanyikanlah Kidung Baru 12B`.
- [x] T005 [US1] Add `test_an_unnumbered_hymn_song_shows_the_reference_alone`: a hymn song with
      `number=None` asserts `NKB` and no trailing space. **Red today**: `Nyanyikanlah Kidung Baru`.
- [x] T006 [US1] Add `test_song_detail_tab_title_uses_the_short_reference` (FR-005): assert
      `response.context['page_title']` is `NKB 12 — GKPS Klender`. **Red today**:
      `Nyanyikanlah Kidung Baru 12 — GKPS Klender`.
- [x] T007 [US1] Add `test_song_detail_header_falls_back_to_the_full_songbook_name`: a hymn book with
      `short_name=''` and a numbered song asserts `Nyanyikanlah Kidung Baru 12`. **Guard** — green before and
      after; it fails if the new code reads `short_name` without the fallback (which would render ` 12`).
- [x] T008 [US1] Make T003–T006 pass: in `multimedia/web/reading/views.py` `SongDetailView.get_context_data`,
      compute the hymn reference as `book.short_name or book.name`, appending
      `f' {song.number}{song.sub_number.upper()}'` only when the song has a number; keep `book.name` for a
      non-hymn songbook. `page_title` already reads `citation`, so T006 follows. *(already in the preview
      build; confirmed unchanged as the implementation)*
- [x] T009 [US1] Re-run T003–T007 green, together with `test_song_detail_shows_lyrics_and_citation` and
      `test_hymn_songs_are_ordered_by_number_then_casefolded_sub_number`.

## Phase 4 — US2 (P2)

**Goal**: an ordinary songbook's page is unchanged, with or without a short name set.
**Independent test**: T010 and T011 — open an ordinary songbook's song page and read the header.

- [x] T010 [US2] Add `test_an_ordinary_songbook_header_keeps_its_full_name` using the class's `harian` fixture
      (`Kidung Harian`, blank short name): the header paragraph reads `Kidung Harian`. **Guard** — green today.
- [x] T011 [US2] Add `test_an_ordinary_songbook_with_a_short_name_still_shows_its_full_name`: create a book
      `name='Kidung Harian Baru', short_name='KH'` with one song, and assert `Kidung Harian Baru`.
      **Guard** — green today; it fails for a uniform `short_name or name` rewrite, which is the tempting
      simplification this requirement rules out.
- [x] T012 [US2] Re-run T010 and T011 plus `test_song_rows_carry_last_modified_and_an_az_key_without_the_number`
      and `test_book_detail_lists_its_songs`; inspect `/songs/1013/` for the surfaces listed in US2/AC2
      (sidebar heading and rows, songbook panel, filter placeholder, stage title) — record what was seen.

## Phase 5 — US3 (P2)

**Goal**: the saved page carries the same header and the same title as the server page.
**Independent test**: T013 — with the library synced, render the hymn song route and compare the header.

- [x] T013 [US3] Add the hymn eyebrow case to `tests/e2e/test_saved_render_parity.py::SavedRenderParityTests::
      test_saved_documents_use_route_specific_labels_and_markup` — `(f'/songs/{self.hymn_song.pk}/', 'eyebrow',
      'HT 7')`. **Red today**: the saved renderer writes `Hymn Test 7`.
- [x] T014 [US3] Add `test_header_and_title_agree_between_saved_and_server`: for the hymn song and the ordinary
      song routes, assert the saved header and the server header both equal the expected text (`HT 7`,
      `Ordinary Test`) and that both documents' titles are equal. **Red today** on the hymn leg.
- [x] T015 [US3] Make T013–T014 pass: apply the same rule in `static/web/offline-render.js` `songPage()`.
      *(already in the preview build; confirmed unchanged)*
- [x] T016 [US3] Re-run the whole `tests.e2e.test_saved_render_parity` class and
      `tests.e2e.test_offline_library` green.

## Phase N — Delivery

- [x] T017 Write `backlog/items/ITEM-127-songbook-short-header.md` and its `backlog/board.md` row.
- [x] T018 Add the spec's row to `specs/README.md` (and the four rows it was missing, 122–125, so the index
      stops claiming the tree ends at 101).
- [x] T019 Bump `VERSION` 1.20.3 → 1.20.4 and add the `[Unreleased]` changelog entry.
- [x] T020 Write `converge.md` and `fold.md`, and apply Fold's delta: create `docs/spec/reading.md` with
      `R1` (the song header cites the short songbook name) and `R2` (a saved reading page matches its server
      route's header and title), its header recording `last folded`/`slices` and that earlier slices were
      never folded. Tick this list and fill `analysis.md`'s dispositions.
- [ ] T021 Commit the slice. **Committed** as `b4641759` on `feat/126-songbook-short-header`; the draft PR
      into `develop` is not open — it needs the push, which waits on the owner's word.

## Dependency graph

```
T001,T002 (n/a) → T003..T007 (pins) → T008 (view) → T009
                                     → T010,T011 (guards) → T012
T009 → T013,T014 (pins) → T015 (renderer) → T016
T016 → T017..T020 → T021
```

Phase 3 delivers the MVP on its own; Phases 4 and 5 are guards and parity, and their pins touch different
files with no shared fixture, so they can be written alongside Phase 3's.

## Verified

- `multimedia.web.tests.ReadingViewTests`: **41 tests green** (7 new). **Red evidence before the view change**:
  4 failures — `'Nyanyikanlah Kidung Baru 12' != 'NKB 12'`, `'Nyanyikanlah Kidung Baru 12B' != 'NKB 12B'`,
  `'Nyanyikanlah Kidung Baru' != 'NKB'`, `'Nyanyikanlah Kidung Baru 12 — GKPS Klender' != 'NKB 12 — GKPS Klender'`.
- `tests.e2e.test_saved_render_parity.SavedRenderParityTests`: **6 tests green** (1 new case, 1 new test).
  **Red evidence before the renderer change**: 2 failures — `'Hymn Test 7' != 'HT 7'`.
- `multimedia.web` + `tests.e2e.test_offline_library` + `tests.e2e.test_saved_render_parity`: **331 tests**,
  one error in `test_saved_content_and_projector_survive_disconnection` (`ERR_INTERNET_DISCONNECTED`), which
  reproduces on the untouched `develop` checkout and is therefore pre-existing and environmental.
- `tests.e2e.test_reading`: **78 tests, one failure** — spec 123's style-parity pin had also asserted the old
  header text (`Nyanyikanlah Kidung Baru 12`), which this slice shortens; the pin now reads `NKB 12` and both
  spec-123 tests pass. On the re-run of the whole class one unrelated test flaked
  (`test_bible_edition_preference_returns_after_unavailable_chapter`, a 5 s visibility wait on a Bible page's
  Simalungun text); it passes alone in 4.1 s and no Bible code path is in this slice.
