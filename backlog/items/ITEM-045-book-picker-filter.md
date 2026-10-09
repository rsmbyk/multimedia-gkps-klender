---
id: ITEM-045
status: archived
title: 'Fix the passage modal book picker''s search filter'
type: fix
priority: P2
effort: S
created: 2026-10-08
updated: 2026-10-09
spec: specs/043-book-picker-filter/spec.md
branch:
pr:
archived_at: 2026-10-09
archive_reason: >
  Superseded by Spec 041 / ITEM-043, which implemented TB/SIM search and non-match hiding; its
  targeted E2E test passes.
bump: patch
release_version:
---

# ITEM-045: Fix the passage modal book picker's search filter

## Summary

Superseded by Spec 041 / ITEM-043: the picker already filters by both the TB and SIM names and
hides non-matches. Its E2E coverage passed locally and in CI. This item is retained as history, not a
pending implementation.

## Original request

The book picker's search box in the passage modal does not actually filter the list — typing leaves
every book visible. Fix it, and make it match both the TB and SIM names once the picker shows them
(ITEM-043 / spec 041).

## Notes

- **The filter runs but is invisible.** `wireScripture()` in `static/web/entries.js` binds
  `filter.addEventListener('input', filterBooks)`, and `filterBooks()` sets `option.hidden` for
  non-matches. But `.editor__songoption { display: block }` in
  `static/styles/design/components.css` beats the `hidden` attribute's UA `display: none`, so hidden
  options stay visible. The same trap was already handled for the menu
  (`.editor__picker-menu[hidden] { display: none }`) and the group
  (`.editor__picker-group[hidden]`), but not for the option itself.
- **The match key.** `filterBooks()` matches `option.dataset.bookName` (the option's
  `data-book-name` = `book.name`, the translation name). After spec 041 the picker shows a TB name
  and a SIM name, so the filter should match either.
- The groups and the "No matching books" hint already follow the option visibility.

## Open questions

- Match on explicit data attributes (`data-book-name` + a SIM one from spec 041) or on the option's
  rendered text?
- Should the filter also match the short book abbreviation?

## Acceptance sketch

- Typing in the book picker's search hides the non-matching books and shows only the matches.
- Clearing the search restores the full list.
- A query matching the SIM name (once the picker shows it) finds the book.

## Links

- Spec: [043 — Fix the passage modal book picker's search filter](../../specs/043-book-picker-filter/spec.md)
- Related items: ITEM-043 / spec 041 (TB/SIM names in the picker), ITEM-006 / spec 005 (entry modals)
