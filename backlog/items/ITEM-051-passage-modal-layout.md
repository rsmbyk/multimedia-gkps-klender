---
id: ITEM-051
status: in review
title: 'Fix passage modal control placement and overflow'
type: fix
priority: P2
effort: S
created: 2026-10-09
updated: 2026-10-09
spec: specs/049-passage-modal-layout/spec.md
branch: fix/049-passage-modal-layout
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/300
archived_at:
archive_reason:
bump: patch
release_version: 1.3.15
---

# ITEM-051: Fix passage modal control placement and overflow

## Summary

Center the TB/SIM switch over the book picker and keep the Chapter, From verse, and To verse
controls inside the passage modal at narrow widths. The current row extends beyond the modal,
creating horizontal overflow and clipping the To verse control.

## Notes

- The switch, Book label, and book picker are rendered in `multimedia/web/templates/reading/_entry_form.html`.
- The chapter/from/to controls share a fixed three-column row in `static/styles/design/components.css`.
- Preserve the existing TB/SIM selection, book, chapter, and verse behavior; this item is layout-only.

## Acceptance sketch

- The TB/SIM switch is centered above the Book label, which remains above the book dropdown.
- Chapter has its own row; From verse and To verse sit together as a range pair below it.
- At 320px, stack the range pair if needed; all controls stay inside the modal without horizontal scrolling.
- Save and Cancel stay reachable if the modal content needs vertical scrolling.
- Add and edit passage forms retain their current values and save behavior.

## Links

- Spec: [049 — Center the TB/SIM switch and contain passage number pickers](../../specs/049-passage-modal-layout/spec.md)
- Related items: ITEM-046 / spec 044 (TB/SIM toggle); ITEM-047 / spec 045 (custom chapter and verse pickers)
