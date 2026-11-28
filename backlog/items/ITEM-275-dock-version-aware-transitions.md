---
id: ITEM-275
status: backlog
title: 'OBS dock follows service changes with the same rules'
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

# ITEM-275: OBS dock follows service changes with the same rules

## Summary

The dock SHALL apply the same identity-aware transitions as the projector, keeping its active row and bait list in step with a changed service while preserving its changed-rows-only painting and its 10 s re-read.

## Notes

- Depends on ITEM-271 and ITEM-274 for the shared transition rules.
- The dock already skips dividers when resolving an active entry.

## Acceptance sketch

- An add or reorder keeps the dock's active entry and updates the entry list.
- A content edit resets the active entry as the projector does.
- A deleted current entry falls back to the previous projectable entry.

## Links

- Spec:
- Related items: ITEM-271, ITEM-274
