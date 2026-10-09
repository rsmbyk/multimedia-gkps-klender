---
id: ITEM-050
status: in_progress
title: 'Make passage book filtering hide non-matches'
type: fix
priority: P2
effort: S
created: 2026-10-09
updated: 2026-10-09
spec: specs/048-book-picker-filter/spec.md
branch: fix/048-book-picker-filter
pr:
archived_at:
archive_reason:
bump: patch
release_version: 1.3.14
---

# ITEM-050: Make passage book filtering hide non-matches

## Summary

Typing in the passage modal's book filter leaves non-matching books visible. Make the rendered list
follow the existing filter state, while preserving matching on both TB and SIM names.

## Notes

- `filterBooks()` in `static/web/entries.js` already sets `option.hidden` and updates the empty
  groups and no-match hint.
- Before the fix, `.editor__songoption--book { display: flex }` in
  `static/styles/design/components.css` overrode the browser's default hidden rule. An explicit
  `[hidden] { display: none }` override now ensures filter state controls visibility.
- Playwright's browser libraries are not in the app image, so a fresh local web container may skip
  the E2E test until those system dependencies are installed.
- The focused regression E2E was run red without the CSS override and green with it; the broader
  E2E suite was not run.

## Acceptance sketch

- Typing a TB or SIM name leaves only matching books visible.
- A query with no matches hides all options and shows the no-match hint.
- Clearing the query restores all books.

## Links

- Spec: [048 — Make the passage book search hide non-matching books](../../specs/048-book-picker-filter/spec.md)
- Related items: ITEM-043 / spec 041 (TB/SIM names in the picker), ITEM-045 / spec 043 (original
  filter requirement)
