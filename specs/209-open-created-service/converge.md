# Convergence: a newly created service opens on the reading stage

**Spec**: `specs/209-open-created-service/spec.md` · **Plan**: `specs/209-open-created-service/plan.md`
**Date**: 2026-11-21 · **Base**: `989347f2`

## Phase 1: Convergence

Checked every row in the plan's traceability table by the method it declared.

| Row | Method | Evidence | Type |
| --- | --- | --- | --- |
| FR-001 / SC-001 | `test` | `test_a_created_service_opens_on_the_stage` — red on base with `url='/tatib/'`, `name=''`, `current=None`; green after the change with URL, heading, current row and empty actions all matching | complete |
| FR-002 / SC-002 | `test` | `test_an_open_from_create_does_not_reload_the_document` — marker `alive`, `performance.timeOrigin` and `data-nav` unchanged; green baseline on base, kept green | complete |
| FR-002 | `test` | `test_a_created_service_opens_its_contents_pane` — red on base (`ch='closed'`), green after (`ch='open'`) | complete |
| FR-003 | `test` | `test_an_open_from_create_keeps_the_panel_state` — `data-nav='mini'` survives; green baseline on base, kept green | complete |
| FR-004 | `test` | `test_a_template_create_keeps_the_stage`, `test_an_edit_keeps_the_stage` — both green baseline and after | complete |
| FR-004 | `inspection` | read `static/web/editors.js` dispatch and the unchanged handlers in `entries.js:222`, `display.js:460`, `media-stage.js:55`, `generate.js:384`; only `reading.js` branches on the two new fields | complete |
| FR-005 / SC-004 | `test` | `test_a_refused_create_keeps_the_stage`, `test_a_failed_create_keeps_the_stage` — green baseline and after; the branch runs only on a 200 response | complete |
| FR-006 | `test` | `test_a_fill_in_and_a_choice_settle_then_create`, `test_copy_as_template_asks_and_copies` green in the final module run | complete |
| US1/AC1 | `inspection` | `test_add_empty_active_tatib` now selects the row by `[data-name]`; it passed in the final run | complete |

**Findings**

- **F1 — partial (fixed mechanically)**. The first implementation navigated on create but dropped
  the quiet focus restoration that spec 025 pins: `test_sidebar_save_restores_focus_to_the_matching_kind_row`
  failed at its Tata Ibadah create assertion after passing on the base worktree. Cause:
  `restoreRequestedFocus` runs only for the `lists`/`refresh` kinds, while this navigation uses
  `service`. Fixed in `static/web/reading.js` by calling the same helper after `navigate()` resolves;
  T007 was amended to record it. The test then passed.
- **F2 — accepted, not this slice**. The final two-module run had five errors out of 66 tests. The
  same five methods were run on a clean worktree at base `989347f2` with the same command, database
  mode, venv and browser: the identical five errors, zero failures. Four are date-picker E2E errors
  in the `ITEM-144` family (`test_date_picker_cells_are_square_across_widths_and_month_lengths` at
  two viewports, `test_tatib_date_picker_loads_saved_date_and_clears_on_edit`,
  `test_tatib_date_picker_selects_clears_and_supports_keyboard`); one is
  `test_pointer_closed_editor_does_not_leave_its_row_control_visible`, which has no card on the board
  and is reported for carding rather than fixed here. No red test was deleted or quarantined.

**Outcome**: 1 partial fixed, 1 accepted pre-existing gap. Re-run for pass 2.

## Phase 2: Convergence

- Re-read `multimedia/web/reading/views.py:184-188` and `static/web/reading.js:2033-2052`: the guard
  is `kind === 'tatib' && created && record_kind === 0`; no other listener consumes the new fields.
- Re-ran the nine focused tests (the eight new scenarios plus the spec-025 focus test): **9 OK**.
- Re-ran both focused modules after the last edit: **66 tests, 0 failures, 5 errors**, all five proven
  on base under the same command. No `missing`, `contradicts` or `unrequested` gaps remain.

**Outcome**: Converged — zero blocking findings, one accepted pre-existing gap (F2).
