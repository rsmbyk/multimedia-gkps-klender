---
id: ITEM-099
status: in_review
title: 'Keep Bible translation selection across menu switches'
type: fix
priority: P2
effort: M
created: 2026-10-16
updated: 2026-10-16
spec: 099
branch: fix/099-bible-edition-across-menus-runtime
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/349
archived_at:
archive_reason:
bump: patch
release_version: 1.13.1
---

# ITEM-099: Keep Bible translation selection across menu switches

## Summary

Remember the reader's TB/SIM choice while the same page visit moves through other reading menus. When the reader returns to Bible and opens a chapter, restore the chosen translation. Start fresh on a page refresh or in a separate tab.

## Acceptance sketch

- A deliberate TB or SIM choice survives in-page switches among Bible, Kidung, and Tata Ibadah, including returning to a Bible chapter from the sidebar.
- The choice is per tab and lasts only while that page remains loaded; refresh and a new tab start from the route's usual initial edition.
- If a chapter lacks the selected translation, the existing fallback remains and the choice returns on a later compatible chapter.
- The behavior matches in online and saved-copy reading.

## Links

- Spec: [099](../../specs/099-bible-edition-across-menus/spec.md)
- Related items: ITEM-095 (offline public reading shell)
