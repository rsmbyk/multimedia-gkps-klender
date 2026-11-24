# Implementation Plan: passage search comboboxes

**Spec**: `specs/238-passage-search-pickers/spec.md`
**Branch**: `feat/238-passage-search-pickers`
**Bump**: `patch` — origin/develop is `1.36.23` at Plan; applied pre-merge and re-checked then
**Preview**: `specs/238-passage-search-pickers/preview/README.md` (live worktree page)

## Technical Context

| Field | Value |
| --- | --- |
| Language / version | Python 3.12 + Django 4.0 server; vanilla JS, CSS and Django templates |
| Primary dependencies | none added; Playwright (Python) already supplies user-visible E2E |
| Storage | PostgreSQL for fixtures only; no model, migration, form or endpoint change |
| Testing | Django test runner; Playwright E2E through `StaticLiveServerTestCase` with a throwaway database |
| Target platform | The passage entry modal in Tata Ibadah, desktop and narrow viewports, light and dark themes |
| Project type | Server-rendered Django fragment + progressively enhanced vanilla JS in `static/web/entries.js` |
| Performance goals | local filtering only; no request added on keystroke |
| Constraints | Hidden selects remain the value carriers; To verse, the translation toggle and the song picker's own code are unchanged |
| Scale / scope | 66 book options, up to 150 chapter and verse numbers; one modal fragment |

## Constitution Check

No `CONSTITUTION.md` exists at the base commit — the constitution is optional and never
auto-created (SDD-01), so the table is empty by absence, not by waiver.

Re-checked after Phase 1: pass — no new dependency, endpoint, persisted entity or external
interface; the change is contained in one template, one script and one stylesheet.

## Phase 0 — Research

See `research.md`. **Unknowns remaining: 0.**

## Phase 1 — Design

- `data-model.md` — the hidden selects and option data the combos read; no new entity.
- `contracts/README.md` — `none` for external interfaces; the internal trigger-attribute
  change is named explicitly.
- `quickstart.md` — live preview, probe, targeted E2E commands, all runnable.

## Traceability

| Requirement | Component / file | Verified by | Notes |
| --- | --- | --- | --- |
| US1/AC1 | `#entry-book-search` in `_entry_form.html`; `wireSearchCombo` in `entries.js` | `test` → `test_book_field_is_a_search_combo` | field is search input, focus selects, two Testament groups |
| US1/AC2 | `filterBooks()` / `wireSearchCombo.query` | `test` → `test_book_filter_matches_names_and_codes` | `mat` → Imamat + Matius; empty hint |
| US1/AC3 | `pickBook()` / `bookId()` | `test` → `test_choosing_a_book_keeps_the_translation_id_and_cascade` | hidden id, field label, Chapter enabled |
| US2/AC1 | `filterByNumber()` / `setChapterValue()` | `test` → `test_chapter_filter_and_choice_reload_verses` | `1` → 12 options; hidden chapter and verse reload |
| US2/AC2 | `setFromValue()` / `syncTo()` | `test` → `test_from_verse_filter_and_choice` | hidden start verse, To verse list refreshed |
| US2/AC3 | `wireSearchCombo.runQuery` | `test` → `test_empty_query_restores_all_options` | empty query shows every option |
| US3/AC1 | first paint in `wireScripture()` | `test` → `test_edit_shows_stored_values_in_all_three_fields` | stored values in fields and hidden selects |
| US3/AC2 | `renderEdition()` / `setEdition()` | `test` → `test_translation_toggle_keeps_the_cascade` | TB/SIM labels and translation-aware id |
| US4 | `wireSearchCombo` keydown + `closeMenus()` | `test` → `test_keyboard_and_dismissal_match_the_song_picker` | one active option, Enter, Escape, outside click |
| FR-001 | `_entry_form.html` three trigger replacements | `inspection` — diff shows three `INPUT[type=search]` and no in-menu book filter | no chevron left on the three |
| FR-002 | `filterBooks(query)`, `filterByNumber()` | `test` → `test_book_filter_matches_names_and_codes`, `test_chapter_filter_and_choice_reload_verses`, `test_from_verse_filter_and_choice` | 140ms debounce preserved |
| FR-003 | `wireSearchCombo` focus/input/keydown | `test` → `test_book_field_is_a_search_combo`, `test_keyboard_and_dismissal_match_the_song_picker` | select-all verified 6/6 chars |
| FR-004 | `pickBook()`, `renderEdition()`, `fillChapters()`, `loadVerses()` | `test` → `test_choosing_a_book_keeps_the_translation_id_and_cascade`, `test_translation_toggle_keeps_the_cascade` | unchanged cascade body |
| FR-005 | `setChapterValue()`, `setFromValue()`, `renderRangeControl()` | `test` → `test_chapter_filter_and_choice_reload_verses`, `test_from_verse_filter_and_choice` | hidden selects dispatch `change` |
| FR-006 | hidden `<select>` elements in the fragment | `inspection` — diff leaves all four selects and the server form unchanged | payload and validation identical |
| FR-007 | verse_end block in `_entry_form.html` | `inspection` — diff has no hunk in that block; button, hover note and "No ending verse" stay | out of scope by owner's wording |
| FR-008 | `placeMenu()`, `closeMenus()` | `inspection` — `preview/parity.py` readouts: 436px menu, 10px radius, 6px gap, viewport cap | shared with song picker |
| SC-001 | `preview/parity.py` + new E2E module | `inspection` — field/menu numbers match `#entry-song-search` exactly | numbers frozen at Gate 1 |
| SC-002 | hidden selects + server form | `inspection` — no `views.py`, form or URL diff; hidden values checked by the E2E module | no server change |
| SC-003 | file list in the slice diff | `inspection` — no endpoint added; only template/JS/CSS/spec files changed | no fetch on keystroke |
| SC-004 | `wireSongPicker()` in `entries.js` | `test` → `tests.e2e.test_song_entry_pickers` (10 tests) | 9 pass, 1 known-red identically on base `88b300bf` |
| Edge cases | disabled books, empty lists, last verse | `inspection` — `option.disabled`/`hidden` filtered in `wireSearchCombo.refresh()` and `list` click guard | see spec Edge Cases |

**Verification split**: 20 test · 12 inspection · 0 manual

## Complexity Tracking

| Violation | Why needed | Simpler alternative rejected because |
| --- | --- | --- |
| A new local interaction helper duplicates ~60 lines of the song picker's key handling | Keeps the green spec-210 path untouched while the three passage fields get the same contract | Extracting a shared helper for all four pickers rewires a passing path with fetch and verse-checklist side effects; no user-visible benefit |

## Project Structure

### Documentation

- `specs/238-passage-search-pickers/spec.md` — accepted at Gate 1.
- `specs/238-passage-search-pickers/research.md`, `data-model.md`, `contracts/README.md`,
  `quickstart.md`, `tasks.md`, `analysis.md`, `converge.md`, `fold.md`.
- `docs/spec/reading.md` — Fold adds `reading/R59` and prepends the slice id.

### Source

- `multimedia/web/templates/reading/_entry_form.html` — three search fields and empty hints.
- `static/web/entries.js` — `wireSearchCombo`, cascade integration, `closeMenus` aria reset.
- `static/styles/design/components.css` — `.is-active` tint and disabled search-field tone.

### Tests

- `tests/e2e/test_passage_search_pickers.py` — new acceptance module for US1–US4.
- `tests/e2e/test_entry_pickers.py` — migrate the three stale trigger selectors.

### Delivery

- `VERSION` patch bump, `CHANGELOG.md` line, `ITEM-253` card, same-PR board close.
