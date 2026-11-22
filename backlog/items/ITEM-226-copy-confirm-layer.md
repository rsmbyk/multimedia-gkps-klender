---
id: ITEM-226
status: done
title: 'The Copy as template confirmation paints inline under the edit form'
type: fix
priority: P1
effort: S
created: 2026-11-21
updated: 2026-11-21
spec: 212
branch: fix/212-copy-confirm-layer
pr: 560
issue:
closed_at: 2026-11-21
closed_reason: merged into develop (PR #560)
bump: patch
release_version: 1.36.6
---

# ITEM-226: The Copy as template confirmation paints inline under the edit form

## Summary

Pressing **Copy as template** in the Edit modal should put a confirmation card over the form. It does
not: the confirmation renders as a block in the modal's own flow, under Save/Cancel, with no scrim, no
card, and its two answers left-aligned — the modal grows from 241px to 477px and carries two Save rows.
Reported from production with a screenshot (2026-11-21).

## Notes

- `components.css` carries `.editor__confirm` and a dead `.editor__confirm-title`, and nothing for
  `.editor__confirm-layer` or `.editor__confirm-actions`. The layer, the card and the right-aligned
  actions exist only in `generate.css`, scoped to `.generate__confirm-layer` / `.choose-layer`.
- Spec 167's preview styled `.confirm-layer` / `.confirm` — names that never reached the product, the
  same miss ITEM-201 fixed for the modal header.
- Measured on production (template 312, *Model C Indonesia*): layer `display: block`,
  `position: static`, transparent, `z-index: auto`; actions `justify-content: normal`; the form's Save
  still receives a click at its own position.

## Acceptance sketch

- One card over a dimmed form; the modal's height does not change when it opens.
- The two answers sit on the card's right edge, 8px apart, as the editor's own 38px buttons.
- Cancel restores the form; `hidden` still hides the layer.

## Links

- Spec: `specs/212-copy-confirm-layer/spec.md`
- Related items: ITEM-201 (the modal header, same class of defect)
