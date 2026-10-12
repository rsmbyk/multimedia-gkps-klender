---
id: ITEM-071
status: in_review
title: Subtle surface for Tata Ibadah entries
type: chore
priority: P2
effort: S
created: 2026-10-13
updated: 2026-10-13
spec: ../../specs/068-tatib-entry-surface/spec.md
branch: chore/068-entry-surface
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/322
archived_at:
archive_reason:
bump: patch
release_version: 1.6.7
---

# ITEM-071: Subtle surface for Tata Ibadah entries

## Summary

Give each entry in the right-hand Tata Ibadah service pane a quiet, theme-aware fill and outline so its containing area is visible without adding prominent decoration.

## Notes

- The owner iterated on a live `/tatib/142/` preview and chose the final fill, outline, and padding values recorded in Spec 068.
- Keep the existing hover, focus, modal-origin, and add-row behavior.
- Section-break boxes use the same surface treatment.

## Acceptance sketch

- Entries and section breaks show the approved subtle surface in light and dark modes.
- Each entry uses 8px top/right/bottom and 12px left padding; floating controls remain 8px from the top and right.
- Hover/focus still takes the established stronger fill, and narrow layouts remain usable.

## Links

- Spec: [Spec 068](../../specs/068-tatib-entry-surface/spec.md)
- Related: [ITEM-057](./ITEM-057-contained-entry-box.md), [ITEM-036](./ITEM-036-highlight-item-on-hover.md)
