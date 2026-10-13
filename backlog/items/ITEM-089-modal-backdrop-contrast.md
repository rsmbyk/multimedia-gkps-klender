---
id: ITEM-089
status: in-review
title: Separate the modals from the page behind them
type: chore
priority: P2
effort: S
created: 2026-10-13
updated: 2026-10-13
spec: ../../specs/086-modal-backdrop-contrast/spec.md
branch: chore/086-modal-backdrop-contrast
pr:
archived_at:
archive_reason:
bump: patch
release_version: 1.10.7
---

# ITEM-089: Separate the modals from the page behind them

## Summary

Both dialogs dim the page with the same hard-coded `rgba(31, 31, 29, .38)` scrim in both themes, and in
dark mode that is barely darker than the canvas beneath it — the owner can hardly tell the dialog from
the page behind it.

## Notes

- Fix: theme tokens `--backdrop` (light `rgba(20, 20, 18, .52)`, dark `rgba(0, 0, 0, .68)`) and
  `--shadow-dialog`, plus a 1px `--divider` edge on both dialogs; `.preview__confirm-layer` follows the
  same scrim.
- Deliberately no blur: spec 065 keeps the origin entry's highlight readable behind the scrim.
- Draft only — no implementation until the owner accepts Spec 086.

## Acceptance sketch

- In dark mode the page behind is clearly dimmed and the dialog reads as the front plane.
- Light mode is deeper than 38% but the page stays legible.
- The origin entry's highlight is still discernible; dialogs' size and behaviour are unchanged.

## Links

- Spec: [Spec 086](../../specs/086-modal-backdrop-contrast/spec.md)
- Preview: [backdrop comparison](../../specs/086-modal-backdrop-contrast/preview.html)
- Related items: ITEM-068 (origin highlight behind the backdrop)
