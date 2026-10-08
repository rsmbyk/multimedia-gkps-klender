---
id: ITEM-038
status: in_review
title: 'Keep the add bar out of the item hover'
type: chore
priority: P2
effort: S
created: 2026-10-08
updated: 2026-10-08
spec: specs/036-add-bar-outside-item-hover/spec.md
branch: chore/036-add-bar-outside-item-hover
pr:
archived_at:
archive_reason:
bump: patch
release_version: 1.3.4
---

# ITEM-038: Keep the add bar out of the item hover

## Summary

With the entry controls now floating in the item's row (ITEM-035) and the item highlighting on hover
(ITEM-036), the add bar directly below an item must not count as part of that item. Hovering the add
buttons' space should show the add buttons and nothing else — no item highlight, no floating
controls.

## Notes

- The add bar is a sibling after the item and currently overlaps it by 4px:
  `.tatib__item + .entry__add { margin-top: -4px; padding-top: 4px }` in
  `static/styles/design/components.css`.
- Because of that overlap, the pointer in the add bar's top edge can still match `.tatib__item:hover`,
  revealing the item's controls (spec 033) and highlight (spec 034) when the operator only meant the
  add buttons.
- Hovering the item should still reveal its add bar (unchanged); the add bar keeps its own four `+`
  buttons.

## Acceptance sketch

- Hovering or focusing the add bar shows its buttons, and the item above is neither highlighted nor
  showing its controls.
- Hovering an item still reveals its add bar.
- The item and its add bar still read as one ("add after this item") without overlap.

## Links

- Spec: [036 — Keep the add bar out of the item hover](../../specs/036-add-bar-outside-item-hover/spec.md)
- Related items: ITEM-035 (floating entry controls), ITEM-036 (item hover highlight)
