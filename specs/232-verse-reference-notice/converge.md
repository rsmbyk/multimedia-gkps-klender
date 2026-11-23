# Convergence — spec 232

**Pass**: 1
**Date**: 2026-11-23
**Checked**: every row in `plan.md`'s traceability table, by the method it declared.
**Commands**: `tests.e2e.test_verse_reference_notice` 12/12 green;
`tests.e2e.test_verse_modal_header` + `tests.e2e.test_add_verse_header` +
`tests.e2e.test_song_verse_script_boot` 12/12 green.

| Requirement | Status | Method | Evidence |
| --- | --- | --- | --- |
| FR-001 | satisfied | test | `test_note_leads_the_action_row` — note is the row's first child with the exact copy |
| FR-002 | satisfied | test | `test_note_type_and_glyph_use_existing_tokens` — 15px glyph, 12px/18px, 700 numeral, token inks |
| FR-003 | satisfied | test | `test_desktop_row_keeps_its_height` — row 38px, note 18px at 1366×900 |
| FR-004 | satisfied | test | `test_disabled_delete_is_neutral` — opacity 1, rail-bg/divider/head-ink |
| FR-005 | satisfied | test | `test_narrow_row_wraps_the_note_above_the_buttons`, `test_narrow_buttons_keep_their_row` |
| FR-006 | satisfied | test + inspection | `test_unreferenced_editor_has_no_note`, `test_other_editors_have_no_reference_note`; every new selector either requires `.editor__refnote` or `.editor__delete` |
| FR-007 | satisfied | test | `test_delete_is_still_refused`, `test_count_tracks_the_guard`; `views.py`/`verses.py` untouched |
| FR-008 | satisfied | test | `test_button_is_described_by_the_note` — `aria-describedby` resolves to the note id |
| SC-001 | satisfied | test | note-leads test |
| SC-002 | satisfied | test | desktop-row test |
| SC-003 | satisfied | test | neutral-button test |
| SC-004 | satisfied | test | one-service note text and three-service fragment assertion |
| SC-005 | satisfied | test | 420×900 note on one full-width line, 18px tall, row 66px, no overflow. The spec's `352px` was the preview's scrollbar-free number; the product measures 346–352 depending on the scrollbar, so the test compares the note to the row's own width rather than to a literal. |
| SC-006 | satisfied | test + inspection | unreferenced and other-editor tests; diff touches only two source files |
| US1/AC1–AC5 | satisfied | test | row order, count, neutral button, unreferenced case, other editors |
| US2/AC1–AC3 | satisfied | test | narrow wrap and buttons, both themes |

**Findings**: 0 missing · 0 partial · 0 contradicts · 0 unrequested.
**Outcome**: Converged on pass 1. No accepted gaps.
