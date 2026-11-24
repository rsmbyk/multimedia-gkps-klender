# Tasks: passage search comboboxes

**Spec**: `specs/238-passage-search-pickers/spec.md`
**Plan**: `specs/238-passage-search-pickers/plan.md`
**Verification split**: 10 test · 12 inspection · 0 manual

`[P]` means order-independent, not concurrent. Every `test` row is a red task and a green task.
Inspection rows produce no test task.

## Phase 1 — Setup

- [ ] T001 Create `tests/e2e/test_passage_search_pickers.py` with a `StaticLiveServerTestCase`
      fixture: one service holding a passage entry, plus a helper for the book → chapter → verse
      cascade. Use `@tag('e2e')`, `skipUnless` on Playwright and
      `override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')`.
      Add a 1440×900 page helper. No assertions yet.

## Phase 2 — US1 (P1) 🎯 MVP

**Goal**: Book is a type-to-filter search field.
**Independent test**: focus, type `mat`, get Imamat + Matius, choose one, cascade enables Chapter.

- [ ] T002 [P] [US1] Red: `test_book_field_is_a_search_combo` — Book is an
      `INPUT[type=search]`, focus opens the grouped menu and selects all, choosing a book
      stores the translation-aware id and enables Chapter.

- [ ] T003 [P] [US1] Green: implement via `wireSearchCombo` + `filterBooks(query)` +
      `pickBook()` in `entries.js`; keep the hidden selects as the value carriers.

- [ ] T004 [P] [US1] Red: `test_book_filter_matches_names_and_codes` — typing filters to
      matching books, shows the empty hint when nothing matches.

- [ ] T005 [P] [US1] Green: pass the field value through the debounced query; hide the in-menu
      filter input.

## Phase 3 — US2 (P1) 🎯 MVP

**Goal**: Chapter and From verse are search fields over the generated lists.

- [ ] T006 [P] [US2] Red: `test_chapter_filter_and_choice_reload_verses` — Chapter filters by
      number substring and choosing stores the chapter and reloads verses.

- [ ] T007 [P] [US2] Green: `filterByNumber()` + `setChapterValue()` over the hidden select.

- [ ] T008 [P] [US2] Red: `test_from_verse_filter_and_choice` — From verse filters and choosing
      refreshes the To verse list.

- [ ] T009 [P] [US2] Green: `setFromValue()` + `syncTo()`.

- [ ] T010 [P] [US2] Red: `test_empty_query_restores_all_options`.

## Phase 4 — US3 (P1) 🎯 MVP

**Goal**: stored values, translation toggle and the cascade stay intact.

- [ ] T011 [P] [US3] Red: `test_edit_shows_stored_values_in_all_three_fields`.
- [ ] T012 [P] [US3] Red: `test_translation_toggle_keeps_the_cascade`.

## Phase 5 — US4 (P2)

**Goal**: keyboard and dismissal match the song picker.

- [ ] T013 [P] [US4] Red: `test_keyboard_and_dismissal_match_the_song_picker`.

## Phase 6 — Regression

- [ ] T014 `test` — `tests.e2e.test_song_entry_pickers` (10 tests, 9 pass / 1 known-red on base).
      Green task: keep it green; red task: none expected beyond the known-red.
- [ ] T015 inspection — migrate the three stale selectors in `tests/e2e/test_entry_pickers.py`
      (`#entry-book-trigger`, `#entry-chapter-trigger`, `#entry-verse_start-trigger`, and the
      `[data-picker-trigger]` usages for those three pickers). No red task.

## Phase 7 — Delivery (per repo practice)

- [ ] T016 bump `VERSION` patch (origin/develop `1.36.23` → `1.36.24`), add `CHANGELOG.md`
      line, create `ITEM-253`, close the card pre-merge on the slice PR.

## Phase 8 — Converge / Fold

- [ ] T017 Converge: run the new module, the song module and the manual state walk.
- [ ] T018 Fold: add `reading/R59` and the slice id to `docs/spec/reading.md`; record in the
      vault.
