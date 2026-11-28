# Convergence — spec 255

Date: 2026-11-28

## Pass 1

Checked every traceability row against the code and the named test, by the method each row declares
(all `test`). 69 E2E tests pass across the three modules: the new module 16/16, spec 253's 15/15 and
the template module 38/38, zero console errors.

| ID | Gap type | Evidence |
| --- | --- | --- |
| US1/AC1 | none | persistent profile relaunch; `test_progress_survives_a_new_browser_session` |
| US1/AC2 | none | `liveRecord` removes an expired key; `test_an_expired_record_is_ignored_and_removed` |
| US1/AC3 | none | `save` rewrites `savedAt`; `test_a_save_on_day_six_restarts_the_clock` |
| US1/AC4 | none | per-template keys; `test_two_templates_keep_separate_clocks` |
| US2/AC1 | none | `paintMark`; `test_the_button_marks_a_live_draft` |
| US2/AC2 | none | `test_the_button_has_no_mark_without_a_draft` |
| US2/AC3 | none | `test_the_mark_appears_after_the_first_save` |
| US2/AC4 | none | `test_the_mark_is_gone_after_create` |
| FR-001 | none | localStorage, `v: 2`, `savedAt`; `test_the_record_is_stored_locally_with_a_timestamp` |
| FR-002 | none | every write path calls `save`; `test_every_change_refreshes_the_timestamp` |
| FR-003 | none | 168 h on read and in the sweep; `test_an_expired_record_is_ignored_and_removed` |
| FR-004 | none | restore + stale-id filter; `test_reopening_restores_slots_step_name_and_date` and spec 253's stale-id test |
| FR-005 | none | `clearSaved` on success; `test_the_mark_is_gone_after_create` |
| FR-006 | none | dot geometry; `test_the_button_marks_a_live_draft`, `test_the_mark_does_not_change_the_button_width` |
| FR-007 | none | `paintMark` sets and removes the name; `test_the_mark_names_the_saved_draft`, `test_the_button_has_no_mark_without_a_draft` |
| FR-008 | none | live appear/clear; the two mark tests |
| FR-009 | none | `test_the_template_is_byte_identical_after_create` |
| FR-010 | none | `test_storage_failure_does_not_break_the_modal` |
| FR-011 | none | confirmation copy; `test_the_leave_confirmation_names_the_seven_day_lifetime` |
| SC-001…SC-006 | none | the tests named in the plan's SC rows |

Findings during implementation, applied:

- The rendered inset is **4px from the border box**, not 3px: `top/right: 3px` sits inside the
  button's 1px border. FR-006, UI/UX and the test now say 4px; the dot is unchanged.
- The leave confirmation's copy said “saved in this browser session”, which the new lifetime makes
  false. It now reads “saved on this browser for seven days” (FR-011), and spec 253's assertion was
  updated with it.
- Spec 253's module still read `sessionStorage` and asserted `v: 1`; both were updated to
  `localStorage` / `v: 2`, since this slice supersedes that store.
- Five new tests initially clicked Next with a choice slot unsettled. That was a test-fixture error,
  not a product gap; they now settle every slot before advancing.

Outcome: **Converged** — 0 missing, 0 partial, 0 contradicts, 0 unrequested. Accepted gaps: none.