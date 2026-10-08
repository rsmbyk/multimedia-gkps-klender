---
id: ITEM-043
status: speccing
title: 'Show TB/SIM book names in the passage modal''s book picker'
type: feat
priority: P2
effort: M
created: 2026-10-08
updated: 2026-10-08
spec: specs/041-picker-book-names/spec.md
branch:
pr:
archived_at:
archive_reason:
bump: patch
release_version:
---

# ITEM-043: Show TB/SIM book names in the passage modal's book picker

## Summary

In the add / edit passage modal, each item in the Bible-books dropdown should read like a sidebar
book row: the **TB** (Indonesian) translation as the main text and the **SIM** (Simalungun)
translation as the secondary, dimmed, on the right.

## Notes

- **The sidebar already does this.** `_books_panel.html` renders `.book__n` (`display`, the TB name)
  and `.book__s` (`other`, the SIM name), built by `_books_groups()` from
  `search_lib.bible_book_index()` (`multimedia/web/reading/search.py`), which maps each `Book` to
  `display` (primary, TB) and `other` (the second translation).
- **The picker does not.** `entry_forms.scripture_books()` (`multimedia/web/reading/entries.py`)
  builds a row per `BookTranslation` with `name = translation.translation`, and
  `_entry_form.html` renders `<button class="editor__songoption" data-book=…>{{ book.name }}</button>`
  with no secondary name.
- **What to change.** Build the picker's books from the same index — one row per **book**, TB as the
  main label and SIM as the right-hand secondary — while keeping the stored value the primary (TB)
  `BookTranslation` so chapter/verse lookups still resolve. Keep `data-chapters` and
  `data-book-name` for the chapter flow, and the hidden `<select name="book_translation">` in step.
- **Styling.** A two-span option mirroring `.book__n` / `.book__s` (secondary dimmed, pushed right).
- **Filtering.** The picker's own search should match either name.

## Open questions

- Confirm **one row per book** (today a book with both translations can appear twice) and that the
  stored translation is the primary/TB one.
- A book whose verses exist only in SIM: does choosing it (TB) still work, or should it store the
  translation that has the chapter's verses?

## Acceptance sketch

- A book with TB and SIM appears once, showing the TB name as the main text and the SIM name dimmed on
  the right.
- Selecting it resolves chapters and verses as before.
- The picker filter matches on either name.

## Links

- Spec: [041 — Show TB/SIM book names in the passage modal's book picker](../../specs/041-picker-book-names/spec.md)
- Related items: ITEM-006 / spec 005 (entry modals), ITEM-042 (picker menus past the modal)
