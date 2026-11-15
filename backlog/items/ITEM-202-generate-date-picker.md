---
id: ITEM-202
status: done
title: 'The date picker opens in the create-from-template dialog'
type: fix
priority: P1
effort: S
created: 2026-11-15
updated: 2026-11-15
spec: 195
branch: fix/195-hotfix-batch
pr: 523
issue: 519
closed_at: 2026-11-15
closed_reason: merged into develop (PR #523)
bump: patch
release_version: 1.32.1
---

# ITEM-202: The date picker opens in the create-from-template dialog

## Summary

Clicking the Date field in the New Tata Ibadah (create from template) dialog does nothing on production (2026-11-15). The picker markup is correct; the calendar never initializes.

## Notes

- `date-picker.js` initializes pickers once at load, and on `date-picker:initialize` scoped to `#editorContent` only. The generate dialog arrives with a stage swap (the reading shell replaces the page's main region), so its picker is never initialized.
- The dialog's own script already re-reads the document on every open for the same reason.

## Acceptance sketch

- Opening the dialog and clicking the Date field opens the calendar; choosing a day fills the field.
- A dialog reached by deep link (full page load) behaves as before.

## Links

- Spec:
- Related items:
