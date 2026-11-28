# Convergence — spec 253

Date: 2026-11-28

## Pass 1

Checked every traceability row in `plan.md` against the implemented code and the named test, by the
method each row declared. All 22 rows declare `test`; each was run in
`tests.e2e.test_use_template_progress` (15 tests, all passing, zero console errors).

| ID | Gap type | Evidence |
| --- | --- | --- |
| US1/AC1 | none | `editor:saved` and chooser pick call `save()`; `test_progress_is_keyed_by_template_id`, `test_settling_a_slot_writes_progress_for_that_template` |
| US1/AC2 | none | `open()` calls `reset(saved())`; `test_reopening_restores_slots_step_name_and_date` |
| US1/AC3 | none | `storageKey()` uses `data-generate-tatib`; `test_two_templates_hold_separate_progress` |
| US1/AC4 | none | `sessionStorage` lifetime; `test_a_new_browser_context_starts_empty` |
| US2/AC1 | none | Cancel, backdrop and `cancel` + document keydown all funnel through `attemptClose()`; `test_cancel_backdrop_and_escape_each_show_the_leave_confirm` |
| US2/AC2 | none | `data-leave-stay` hides the layer; `test_stay_keeps_the_modal_and_the_settled_rows` |
| US2/AC3 | none | `data-leave-accept` calls `close()` without clearing; `test_leave_closes_and_the_progress_survives` |
| US2/AC4 | none | `dirty()` gates the layer; `test_a_clean_modal_closes_without_a_confirm` |
| FR-001 | none | keyed per template; `test_progress_is_keyed_by_template_id` |
| FR-002 | none | save on slot, choice, name, date and step; `test_every_slot_name_and_date_change_rewrites_progress` |
| FR-003 | none | `{v, step, settled, name, date}`; `test_the_saved_record_holds_slots_step_name_and_date` |
| FR-004 | none | restore on open; `test_reopening_restores_slots_step_name_and_date` |
| FR-005 | none | stale slot ids filtered; `test_a_slot_removed_from_the_template_is_ignored_on_restore` |
| FR-006 | none | layer wording and three close paths; `test_cancel_backdrop_and_escape_each_show_the_leave_confirm` |
| FR-007 | none | Stay/Leave; `test_stay_keeps_the_modal_and_the_settled_rows` |
| FR-008 | none | `clearSaved()` on success only; `test_a_successful_create_clears_that_templates_progress` |
| FR-009 | none | no write path added; `test_the_template_is_byte_identical_after_close_and_create` |
| SC-001 | none | `test_two_templates_hold_separate_progress` |
| SC-002 | none | `test_a_reload_restores_progress` |
| SC-003 | none | `test_a_clean_modal_closes_without_a_confirm` |
| SC-004 | none | `test_cancel_backdrop_and_escape_each_show_the_leave_confirm` |
| SC-005 | none | `test_a_successful_create_clears_that_templates_progress` |

Findings during implementation, already applied:

- Escape did nothing when focus had returned to `body` after a slot form saved: a modal `<dialog>`
  fires `cancel` only while focus is inside it. A document-level keydown path was added with a flag
  so the following `cancel` cannot dismiss the layer it just opened. Covered by SC-004's test.
- The preview's layer was named after the Create confirm; it was renamed to `data-generate-leave` to
  match the shipped markup. `preview/probe.py` passes 10/10 and the chat-frame verifier passes.

Outcome: **Converged** — 0 missing, 0 partial, 0 contradicts, 0 unrequested. Accepted gaps: none.
