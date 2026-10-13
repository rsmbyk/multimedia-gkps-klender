---
id: ITEM-084
status: done
title: Renumber the dragged row while it is being reordered
type: fix
priority: P2
effort: S
created: 2026-10-13
updated: 2026-10-13
spec: ../../specs/081-reorder-index-while-dragging/spec.md
branch: fix/081-reorder-index-while-dragging
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/335
archived_at:
archive_reason:
bump: patch
release_version: 1.10.2
---

# ITEM-084: Renumber the dragged row while it is being reordered

## Summary

`renumber()` keeps the list's numbers in step during a drag but never reaches the drag copy, so the row
in the operator's hand keeps showing the index it had when it was picked up.

## Notes

- `#chList li.is-dragging > *` hides the real row's paint, so the number on screen while dragging is the
  ghost's — stamped once in `makeGhost()` and never updated.
- The keyboard arrow move has no copy and already behaves.
- Draft only — no implementation until the owner accepts Spec 081.

## Acceptance sketch

- The copy in hand counts 1, 2, 3 … as it passes the other rows, and matches the final position.
- A section break advances the count without painting a number.
- Cancel and no-op presses leave every number as it was.

## Links

- Spec: [Spec 081](../../specs/081-reorder-index-while-dragging/spec.md)
- Preview: [renumbering preview](../../specs/081-reorder-index-while-dragging/preview.html)
- Related items: ITEM-064 (number centering), ITEM-077 (whole-row drag)
