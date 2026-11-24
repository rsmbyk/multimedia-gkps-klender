---
id: ITEM-256
status: done
title: 'A Tata Ibadah reorder loses entries after a save'
type: fix
priority: P1
effort: M
created: 2026-11-24
updated: 2026-11-24
spec: 241-tatib-reorder-kept
branch: fix/241-tatib-reorder-kept
pr: 620
issue: 619
closed_at: 2026-11-24
closed_reason: merged into develop (PR #620)
bump: patch
release_version:
---

# ITEM-256: A Tata Ibadah reorder loses entries after a save

## Summary

After adding, editing or deleting an entry, the service's contents list and stage stop agreeing:
the break row jumps to the top, a section can vanish from the stage, and a drag to the top writes
the pre-drag order. Measured at 1440×900 on the base commit: an edit paints `[4, 1, 2, 3]` where
the server holds `[1, 2, 3, 4]`; an add-then-drag leaves the stage with `[5, 3, 1, 2]` and the
sidebar with `[4, 5, 1, 2, 3]`.

## Notes

- `applySongOrder()` (spec 233) treats every `.songrow` as a song, including the contents rows,
  and its `appendChild` moves them to the end of the shared list.
- `endDrag()` rewrites the pane while the gesture is live; the rewrite raises a cancel that
  restores the pre-drag order, and `applyPaneOrder()`'s stale node cache drops a section.
- The server already renders and accepts the right order; the fix is client-side.
- Capability: `reading/R57` modified (sorter scope), `reading/R58` added (one write, both lists agree).

## Acceptance sketch

- An edit leaves the contents in the server's order.
- A drop after an edit writes the dropped order once; the stage and the contents show the same
  entries in the same order, and a reload keeps it.
- An add-then-drag keeps every entry on the stage.
- The retained song sort and the chapter order stay as they are.

## Links

- Spec: [241-tatib-reorder-kept](../specs/241-tatib-reorder-kept/spec.md)
- Related items: ITEM-247 (spec 233 introduced the shared re-sort), ITEM-007 (service entries)
