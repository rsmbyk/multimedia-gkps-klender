---
id: ITEM-046
status: speccing
title: 'Add a TB/SIM toggle to the passage modal book picker'
type: feat
priority: P2
effort: M
created: 2026-10-08
updated: 2026-10-08
spec: specs/044-passage-translation-toggle/spec.md
branch:
pr:
archived_at:
archive_reason:
bump: patch
release_version:
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
- **The picker.** After spec 041 the book options carry both names (TB and SIM) and one stored
  `BookTranslation`. The toggle decides which of the two is primary: with TB selected, TB is the main
  name and SIM the secondary; with SIM selected, they swap.
- **Not a new field.** No extra form field is added; the existing hidden
  `select[name=book_translation]` still carries the stored value, and the toggle changes which
  translation's `BookTranslation` the picker offers.
- **The rest stays.** The chapter and from/to-verse controls do not change with the toggle; they still
  follow the chosen book.
- **Filter.** The picker filter keeps matching both names (spec 043) whichever side the toggle puts
  them on.

## Open questions

- Editing an existing passage: does the toggle start on the stored translation's side?
- When the selected book has no verses in the switched-to translation, what happens to the chapter /
  verse lists?
- Should switching re-fetch chapters/verses, or only re-letter the picker?

## Acceptance sketch

- The passage modal (add and edit) shows a TB/SIM toggle.
- Toggling it swaps the book dropdown's main and secondary names immediately.
- Selecting a book stores that translation's `BookTranslation`.
- The chapter and verse controls are unchanged by the toggle.

## Links

- Spec: [044 — Add a TB/SIM toggle to the passage modal book picker](../../specs/044-passage-translation-toggle/spec.md)
- Related items: ITEM-043 / spec 041 (TB/SIM names in the picker), ITEM-045 / spec 043 (the filter),
  ITEM-042 (picker menus past the modal)
