# Implementation Plan: the song entry's pickers

**Spec**: `specs/210-song-verse-picker/spec.md`
**Branch**: `feat/210-song-verse-picker`
**Bump**: `patch` — a change to two existing pickers, not a new capability or a break.
**Preview**: `specs/210-song-verse-picker/preview/` (accepted at gate 1)

## Technical Context

| Field | Value |
| --- | --- |
| Language / version | Python 3.12, Django 4.0, DRF; vanilla ES5-style JS in `static/web/` |
| Primary dependencies | Django forms, Playwright (Python), no new packages |
| Storage | Existing `Song`, `Verse`, `ServiceEntry` rows; no migration in this slice |
| Testing | Django `manage.py test` plus `tests/e2e/` Playwright over `StaticLiveServerTestCase`; classicist, real collaborators |
| Target platform | Chromium on Linux and the deployed reading shell, dark and light themes, 560px–960px widths |
| Project type | Server-rendered Django templates with progressive vanilla JS |
| Performance goals | The song query stays capped at 200 options; no extra round trip on focus, click or drag |
| Constraints | Keep verse IDs as submitted values, keep the query grammar and ordering, keep the fixed viewport-capped menu, no framework or icon library |
| Scale / scope | One form fragment, one JS module, one CSS block, one new E2E module; capability `reading` only |

## Constitution Check

No `CONSTITUTION.md` exists in this checkout, so there are no project principles to test
against. Nothing to justify; the Complexity Tracking table is empty.

Re-checked after Phase 1: pass — no new dependency, no new model, no backend interface change.

## Phase 0 — Research

See `research.md`. **Unknowns remaining: 0.**

## Phase 1 — Design

- `data-model.md` — no persistent entity changes; the ephemeral picker state is described.
- `contracts/` — `none`: the existing endpoints and their payloads are unchanged.
- `quickstart.md` — local verification commands and their current runnability.

## Traceability

| Requirement | Component / file | Verified by | Notes |
| --- | --- | --- | --- |
| FR-001 | `static/web/entries.js` `wireSongPicker` + `_entry_form.html` `data-entry-mode` | `test` → `tests/e2e/test_song_entry_pickers.py::test_search_is_focused_on_open`, `::test_edit_does_not_grab_the_song_search` | focus on the Add form's first paint only |
| FR-002 | `static/web/entries.js` `placeMenu` + `components.css` `.editor__picker-menu` | `test` → `tests/e2e/test_song_entry_pickers.py::test_results_overlay_may_pass_dialog_bottom` | geometry at 960×900 |
| FR-003 | `multimedia/web/reading/views.py` `entry_song_options` | `inspection` — diff contains no query/order/cap change | guard FR |
| FR-004 | `static/web/entries.js` song results handlers | `test` → `tests/e2e/test_song_entry_pickers.py::test_keyboard_and_touch_pick` | arrows, Enter, Escape, tap |
| FR-005 | `_entry_form.html` hidden `song`; `entries.js` `wireSongPicker` | `test` → `tests/e2e/test_song_entry_pickers.py::test_pick_writes_hidden_id_and_label` | |
| FR-006 | `_entry_form.html` Verses field + `components.css` | `test` → `tests/e2e/test_song_entry_pickers.py::test_summary_lives_inside_section` | no chevron/menu |
| FR-007 | `components.css` tile grid | `test` → `tests/e2e/test_song_entry_pickers.py::test_tile_grid_geometry_and_helper_position` | computed geometry, equal columns |
| FR-008 | `entries.js` `renderVerses` + `SongEntryForm` | `test` → `tests/e2e/test_song_entry_pickers.py::test_fresh_pick_and_edit_state` | |
| FR-009 | `entries.js` tile click handler | `test` → `tests/e2e/test_song_entry_pickers.py::test_click_ticks_one_verse` | |
| FR-010 | `entries.js` drag preview/commit | `test` → `tests/e2e/test_song_entry_pickers.py::test_drag_previews_until_release` | values unchanged while held |
| FR-011 | `entries.js` carrier + `multimedia/web/reading/entries.py` `SongEntryForm` + `reading/widgets/verse_checkbox*.html` | `test` → `tests/e2e/test_song_entry_pickers.py::test_a_failed_save_keeps_the_tile_grid`, `multimedia/web/tests.py::ServiceEntryViewTests::test_a_server_rendered_verses_list_is_already_the_tile_grid` | IDs still submitted, `{id, number}` payload unchanged |
| FR-012 | `entries.js` `verseSummary` + `reading/formatting.py` `format_verses` | `test` → `tests/e2e/test_song_entry_pickers.py::test_summary_inside_section_and_quick_states`, `multimedia/web/tests.py::FormatVersesTests`, `::ServiceEntryViewTests::test_the_stage_and_sidebar_verse_lines_agree` | one `Bait …` form everywhere |
| FR-013 | `entries.js` quick actions | `test` → `tests/e2e/test_song_entry_pickers.py::test_summary_inside_section_and_quick_states` | |
| FR-014 | `_entry_form.html` + `components.css` + `entries.js` | `test` → `multimedia/web/tests.py::test_no_song_and_no_verses_hide_field` | server fragment first |
| FR-015 | `entries.js` + `components.css` | `test` → `tests/e2e/test_song_entry_pickers.py::test_single_verse_section_is_muted` | |
| FR-016 | `components.css` reveal rule | `test` → `tests/e2e/test_song_entry_pickers.py::test_reveal_is_one_reduced_motion_curve` | emulated reduced motion |
| SC-001 | `_entry_form.html` + `entries.js` | `test` → `tests/e2e/test_song_entry_pickers.py::test_search_is_focused_on_open` | |
| SC-002 | `entries.js` drag handler | `test` → `tests/e2e/test_song_entry_pickers.py::test_drag_previews_until_release` | |
| SC-003 | `entries.js` carrier sync | `test` → `tests/e2e/test_song_entry_pickers.py::test_drag_previews_until_release` | same pin |
| SC-004 | `components.css` + `entries.js` `placeMenu` | `test` → `tests/e2e/test_song_entry_pickers.py::test_results_overlay_may_pass_dialog_bottom` | |
| SC-005 | `_entry_form.html` + `components.css` | `test` → `multimedia/web/tests.py::test_no_song_and_no_verses_hide_field` | |
| US1/AC1 | `_entry_form.html` | `test` → `test_search_is_focused_on_open` | |
| US1/AC2 | `entry_song_options` + result renderer | `inspection` — same groups, labels, order, cap | |
| US1/AC3 | `wireSongPicker` | `test` → `test_pick_writes_hidden_id_and_label` | |
| US1/AC4 | song results keydown | `test` → `test_keyboard_and_touch_pick` | |
| US1/AC5 | result renderer | `test` → `test_results_overlay_may_pass_dialog_bottom` | |
| US2/AC1 | `renderVerses` fresh default | `test` → `test_fresh_pick_and_edit_state` | |
| US2/AC2 | tile click | `test` → `test_click_ticks_one_verse` | |
| US2/AC3 | drag preview | `test` → `test_drag_previews_until_release` | |
| US2/AC4 | drag commit | `test` → `test_drag_previews_until_release` | |
| US2/AC5 | quick actions | `test` → `test_all_and_clear_disable_at_ends` | |
| US2/AC6 | edit render | `test` → `test_fresh_pick_and_edit_state` | |
| US3/AC1 | `_entry_form.html` | `test` → `multimedia/web/tests.py::test_no_song_and_no_verses_hide_field` | |
| US3/AC2 | server fragment + save guard | `test` → `multimedia/tatib/tests.py` existing refusal pins | unchanged error text |
| US3/AC3 | `renderVerses` single verse | `test` → `test_single_verse_section_is_muted` | |
| US3/AC4 | reveal CSS | `test` → `test_reveal_is_one_reduced_motion_curve` | |
| US3/AC5 | reduced motion | `test` → `test_reveal_is_one_reduced_motion_curve` | |
| US4/AC1 | `_entry_form.html` + `components.css` | `test` → `test_summary_lives_inside_section` | |
| US4/AC2 | soft-trigger handler | `test` → `test_soft_trigger_collapses_tiles_only` | |
| US4/AC3 | panel CSS | `inspection` — no chevron rule or fixed verse menu remains | |
| Edge: verse fetch fails | `loadVerses` | `test` → `tests/e2e/test_song_entry_pickers.py::test_verse_fetch_failure_keeps_state` | |
| Edge: stale saved numbers | `SongEntryForm` | `test` → `multimedia/web/tests.py` existing stale-verse pin | unchanged |
| Edge: same-tile drag | drag handler | `test` → `test_click_ticks_one_verse` | treated as click |
| Edge: no result | result renderer | `test` → `tests/e2e/test_song_entry_pickers.py::test_no_match_keeps_dialog_height` | |

**Verification split**: 41 test · 3 inspection · 0 manual (FR-011 moved from inspection to test when
the server-rendered tile grid gained its pins). Dark/light review at 1× remains a
manual owner check after implementation, but no requirement depends on it alone.

## Complexity Tracking

| Violation | Why needed | Simpler alternative rejected because |
| --- | --- | --- |

## Project Structure

### Documentation

```
specs/210-song-verse-picker/
  spec.md  plan.md  research.md  data-model.md  quickstart.md  tasks.md
  contracts/none.md  checklists/requirements.md  preview/
```

### Source

```
multimedia/web/templates/reading/_entry_form.html   (form field structure)
static/web/entries.js                               (picker behaviour)
static/styles/design/components.css                 (section, tiles, overlay)
tests/e2e/test_song_entry_pickers.py                (new acceptance pins)
```

### Structure Decision

No new app or package: both pickers live in the one modal fragment that already renders them,
and the behavior stays in `entries.js` beside its existing picker wiring. The new E2E module
is separate from `test_entry_pickers.py`, whose base-level backdrop race is already on the
board, so this slice's pins are not mixed with known-red tests.
