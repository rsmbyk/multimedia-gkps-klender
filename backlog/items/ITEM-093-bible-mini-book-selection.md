---
id: ITEM-093
status: done
title: Keep the Bible book sidebar mini when selecting a book
type: fix
priority: P1
effort: S
created: 2026-10-14
updated: 2026-10-14
spec: ../../specs/090-bible-mini-book-selection/spec.md
branch: fix/090-bible-mini-book-selection
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/345
archived_at:
archive_reason:
bump: patch
release_version: 1.10.11
---

# ITEM-093: Keep the Bible book sidebar mini when selecting a book

## Summary

Clicking another Bible book while the book sidebar is mini opens the full sidebar. Keep the mini state while showing the selected book's chapters.

## Notes

The book tile used the `lists` navigation kind. Its arriving Bible page has `data-nav="open"`, and `applyPage()` copied that value to the live shell. Spec 080 preserved mini mode for chapter clicks but did not cover book selection.

## Acceptance sketch

- Selecting another Bible book from mini mode leaves the first sidebar mini, selects that book, and shows its chapter list.
- Clicking the selected book continues to toggle its chapter list without expanding the first sidebar.
- The explicit expand control still opens the first sidebar.

## Links

- Spec: [../../specs/090-bible-mini-book-selection/spec.md](../../specs/090-bible-mini-book-selection/spec.md)
- Related items: ITEM-083 (spec 080), ITEM-091 (spec 088)
