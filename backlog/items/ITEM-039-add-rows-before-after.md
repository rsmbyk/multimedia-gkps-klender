---
id: ITEM-039
status: in_review
title: 'Reveal the add rows before and after a hovered item'
type: chore
priority: P2
effort: M
created: 2026-10-08
updated: 2026-10-08
spec: specs/037-add-rows-before-after/spec.md
branch: chore/037-add-rows-before-after
pr:
archived_at:
archive_reason:
bump: patch
release_version: 1.3.5
---

# ITEM-039: Reveal the add rows before and after a hovered item

## Summary

Hovering a service entry should reveal the add row immediately **above** it and the one immediately
**below** it, so the operator can insert on either side of the item under the pointer. Today only
the row after the item is revealed.

## Notes

- The pane renders one `.entry__add` bar after each item (in `tatib.html`), each carrying
  `data-entry-after="…"`; CSS reveals only the following one
  (`.tatib__item:hover + .entry__add`).
- So a bar already exists above every item except the first — that one is the leading start bar
  (ITEM-032). The row above item N is the row that inserts after item N-1, which is the same
  position as "before item N".
- **CSS cannot reach a preceding sibling**, so revealing both needs a small JS toggle (a visibility
  class on the item's adjacent bars) on item hover **and** keyboard focus, or a DOM restructure.
- Must stay consistent with ITEM-038 / spec 036: hovering or focusing a bar shows only that bar and
  does not highlight the item above; only hovering the item reveals the pair.

## Acceptance sketch

- Hovering an item reveals the add row above it and the add row below it.
- The first item's "above" row is the start bar (ITEM-032); the last item's "below" row is its own
  trailing bar.
- Keyboard focus within an item reveals the same pair.
- Hovering a bar itself reveals only that bar, with no item highlight (spec 036).

## Links

- Spec: [037 — Reveal the add rows before and after a hovered item](../../specs/037-add-rows-before-after/spec.md)
- Related items: ITEM-032 (add at start), ITEM-038 (the add bar is outside the item hover),
  ITEM-035 / ITEM-036 (item hover: controls and highlight)
