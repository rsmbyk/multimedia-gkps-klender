---
id: ITEM-274
status: backlog
title: 'Projector follows service changes without losing the live place'
type: feat
priority: P1
effort: L
created: 2026-11-28
updated: 2026-11-28
spec:
branch:
pr:
issue:
closed_at:
closed_reason:
bump:
release_version:
---

# ITEM-274: Projector follows service changes without losing the live place

## Summary

The projector SHALL detect a behind service version by a 10 s poll and by the existing same-browser update message, then apply identity-aware rules: keep the current entry when an add/reorder happens; keep the screen for a title-only edit; reset content changes to the entry's first screen, with the passage and song verse refinements the owner specified; and fall back to the previous projectable entry at its first screen when the current one is gone.

## Notes

- Depends on ITEM-271.
- The current entry must be matched by stable ID, not screen index.
- The browser compares old and new entry payloads field by field; measured at ~0.02 ms for the largest local service.
- Skip dividers and unfilled slots when choosing the previous applicable entry.

## Acceptance sketch

- A reorder leaves the live entry on screen and advances to the new next entry.
- A title-only text edit keeps the screen; a lyric edit resets to the verse start.
- A deleted current entry falls back to the previous projectable entry's first screen.

## Links

- Spec:
- Related items: ITEM-271, ITEM-275
