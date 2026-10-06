---
id: ITEM-009
title: 'Softer selected-item tint in reading sidebars'
status: done
type: chore
priority: P2
effort: S
spec: specs/008-sidebar-selection-tint/spec.md
branch: feat/008-sidebar-selection-tint
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/264
archived_at:
archive_reason:
bump: patch
release_version: 0.11.1
created: 2026-10-05
updated: 2026-10-06
---

# ITEM-009: Softer selected-item tint in reading sidebars

## Summary

Use a slightly softer, lighter selected-row tint for Bible books, Bible chapters, songbooks, songs,
and Tata Ibadah services, with readable text in light and dark themes.

## Notes

- Keep the accent hue but blend it into the rail surface for these sidebar rows only.
- Preserve all other active, hover, focus, and drag destination-slot styling.

## Acceptance sketch

- All five selected sidebar row types use the same theme-specific softer tint.
- Selected text remains at least 4.5:1 contrast in both themes.
- Unrelated states and selection behavior are unchanged.

## Links

- Spec: [`specs/008-sidebar-selection-tint/spec.md`](../../specs/008-sidebar-selection-tint/spec.md)
- Related items: ITEM-005, ITEM-006, ITEM-007
