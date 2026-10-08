---
id: ITEM-047
status: speccing
title: 'Make the passage modal''s chapter/verse dropdowns custom'
type: refactor
priority: P2
effort: M
created: 2026-10-08
updated: 2026-10-08
spec: specs/045-custom-chapter-verse-dropdowns/spec.md
branch:
pr:
archived_at:
archive_reason:
bump: patch
release_version:
---

# ITEM-047: Make the passage modal's chapter/verse dropdowns custom

## Summary

The passage modal is inconsistent: the book is a custom picker, but chapter, from-verse and to-verse
are native `<select>`s. Rebuild those three as the same custom dropdown so the modal feels of a
piece.

## Notes

- **Where.** `_entry_form.html`'s scripture branch renders `<select name="chapter">`,
  `<select name="verse_start">` and `<select name="verse_end">` (the last inside
  `.editor__end-wrap` with its disabled-hover tip).
- **Driven by JS.** `wireScripture()` in `static/web/entries.js` fills them: `fillChapters()` writes
  the chapter options, `loadVerses()` the verse options, `syncTo()` trims the to-verse list and
  toggles its disabled state.
- **The component to reuse.** The book/song picker: `.editor__picker` with `[data-picker-trigger]`,
  `.editor__picker-menu`, `[data-picker-options]`, `[data-picker-label]`, and the JS in
  `wirePickerMenus()`.
- **The value must still POST.** Each custom control needs a hidden input (or the existing select
  kept hidden) carrying the value, so the form posts `chapter` / `verse_start` / `verse_end`
  unchanged.
- **The to-verse tip.** Its "No verses available after the start verse" note (`.editor__end-wrap`
  `[data-empty]`) must survive.
- Applies to the add and edit passage modals (shared fragment).

## Open questions

- Scope: only the passage modal's chapter/verse controls, or every native select in the editor modals
  (songbook, song, Tata Ibadah forms)?
- Keep a native select as a no-JS fallback, or rely on the custom control?
- Preserve the disabled to-verse tip's exact behaviour?

## Acceptance sketch

- Chapter, from-verse and to-verse are custom dropdowns, styled like the book picker.
- They still update with the chosen book/chapter and still post their values.
- The to-verse still disables with its note when no verse can end the range.
- The add and edit modals both use them.

## Links

- Spec: [045 — Make the passage modal's chapter/verse dropdowns custom](../../specs/045-custom-chapter-verse-dropdowns/spec.md)
- Related items: ITEM-042 (picker menus past the modal), ITEM-043 (the book picker),
  ITEM-046 (the translation toggle), ITEM-006 / spec 005 (entry modals)
