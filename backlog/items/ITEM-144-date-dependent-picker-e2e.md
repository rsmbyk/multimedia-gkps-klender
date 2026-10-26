---
id: ITEM-144
status: backlog
title: 'Five date-picker E2E tests fail when the nearest Sunday falls in the next month'
type: fix
priority: P1
effort: S
created: 2026-10-26
updated: 2026-10-26
spec:
branch:
pr:
issue:
closed_at:
closed_reason:
bump:
release_version:
---

# ITEM-144: Five date-picker E2E tests fail when the nearest Sunday falls in the next month

## Summary

`EditorE2ETests._fill` reaches a date by clicking the calendar's next/prev control the number of months
between **today** and the target, assuming the calendar opens on today's month. The Tata Ibadah form's
picker opens on the date it defaults to — the nearest Sunday — so when that Sunday is in the following
month the extra click lands a month too far and `[data-date="<value>"]` is not rendered.

## Notes

- Reproduced today (Monday 2026-10-26, nearest Sunday 2026-11-01) on both this branch and `develop`
  `4de3b3b1`, same command, database and browser: identical five errors. It is a test-side flaw, not a
  product regression, and it only surfaces on the days when the default Sunday crosses a month boundary.
- Failing tests, all in `tests/e2e/test_editor.py::EditorE2ETests`:
  `test_add_empty_active_tatib`, `test_sidebar_save_restores_focus_to_the_matching_kind_row`,
  `test_tatib_date_picker_selects_clears_and_supports_keyboard`,
  `test_tatib_date_picker_submits_iso_date`, `test_tatib_date_picker_survives_validation_rerender`.
- `_fill` steps from `date.today()`, while `static/web/date-picker.js` opens on
  `addDays(today, (7 - today.getDay()) % 7)` whenever the field has no value.

## Acceptance sketch

- The helper steps from the month the calendar actually opened on, or sets the field directly instead of
  walking the grid.
- The five tests pass on a Monday whose nearest Sunday is in the next month, pinned either way so the run
  does not depend on the calendar day.

## Links

- Spec: —
- Related items: ITEM-018, ITEM-022, ITEM-024 (the Tata Ibadah date picker)
