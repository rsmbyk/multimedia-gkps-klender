---
id: ITEM-046
status: in_progress
title: 'Add a TB/SIM toggle to the passage modal book picker'
type: feat
priority: P2
effort: M
created: 2026-10-08
updated: 2026-10-09
spec: specs/044-passage-translation-toggle/spec.md
branch: feat/044-passage-translation-toggle
pr:
archived_at:
archive_reason:
bump: patch
release_version: 1.3.11
---

# ITEM-046: Add a TB/SIM toggle to the passage modal book picker

## Summary

Add the reading page's TB/SIM toggle to the add and edit passage modals, so the operator can quickly
switch which translation the book picker offers. It is **not** a new form field — the existing
`book_translation` still stores the choice. The book dropdown reflects the switch at once: the main
and secondary book names swap places, and the other dropdowns (chapter, verses) stay as they are.

## Notes

- **The precedent.** The reading page already has the toggle: `.read__lang` with `#langTb` / `#langSim`
  and a thumb (`multimedia/web/templates/reading/base.html`,
  `static/styles/design/components.css`), switching the TB/SIM edition.
- **The picker.** After spec 041 the book options carry both names (TB and SIM). The toggle decides
  which is primary: TB selected means TB main/SIM secondary; SIM selected means SIM main/TB secondary.
- **Legacy fallback.** If neither TB nor SIM exists, keep the existing primary translation selectable
  on the default side.
- **Not a new field.** No extra form field is added; the existing hidden
  `select[name=book_translation]` carries the selected `BookTranslation`. Toggling updates it for the
  selected book, and choosing a book afterward stores the active translation.
- **Initial state.** A new passage starts on TB. An edit or validation-error form starts on the edition
  of its selected `BookTranslation`.
- **The rest stays.** Toggling does not reload or change chapter/from/to-verse options or selected
  values. Choosing a different book uses the existing cascade for the active translation.
- **Filter.** Spec 041 already matches both book names; spec 043 / ITEM-045 was superseded by spec 041.
  The filter must continue working whichever name is primary.

## Acceptance sketch

- The passage modal (add and edit) shows a TB/SIM toggle with correct initial state.
- Toggling it swaps the book dropdown's main and secondary names and updates the selected book's
  `BookTranslation` at once.
- Selecting a book stores the active translation's `BookTranslation`.
- The chapter and from/to-verse controls remain unchanged during a toggle; selecting another book
  loads the active translation's chapter/verse options through the existing cascade.
- Filtering either name works in either toggle state.

## Links

- Spec: [044 — Add a TB/SIM toggle to the passage modal book picker](../../specs/044-passage-translation-toggle/spec.md)
- Related: ITEM-043 / spec 041 (TB/SIM names and filter), ITEM-042 (picker menus past the modal).
  The former filter item ITEM-045 / spec 043 is archived as superseded by spec 041.
