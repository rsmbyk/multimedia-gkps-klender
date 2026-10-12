---
id: ITEM-059
status: in_review
title: Built-in blank after each entry and each song verse
type: feat
priority: P1
effort: M
created: 2026-10-12
updated: 2026-10-12
spec: ../specs/057-built-in-projection-breaks/spec.md
branch: feat/057-built-in-projection-breaks
pr: 311
archived_at:
archive_reason:
bump: minor
release_version: 1.4.0
---

# ITEM-059: Built-in blank after each entry and each song verse

## Summary

The projector should show a blank screen after every content entry, and after
every verse of a song, without storing that blank as a section break. The blank
is not a row, so it cannot be moved or deleted.

## Notes

Agreed in chat on 2026-10-12 before this Draft. A stored section break stays an
operator-placed blank. A content entry followed by one shows two blanks.

## Acceptance sketch

- Text, single-screen text, scripture, and legacy text rows end on one blank screen.
- Each selected song verse ends on one blank; the last verse does not get a second blank.
- The editor order is unchanged.

## Links

- Spec: [057](../specs/057-built-in-projection-breaks/spec.md)
- Related items: ITEM-031 (single-screen text), service-entry projector (spec 006)
