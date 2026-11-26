---
id: ITEM-259
status: in-review
title: 'Picker popout scrollbars sit at the menu edge'
type: fix
priority: P2
effort: S
created: 2026-11-26
updated: 2026-11-26
spec: 244-picker-menu-scrollbar-edge
branch: fix/244-picker-menu-scrollbar-edge
pr: 625
issue:
closed_at:
closed_reason:
bump: patch
release_version:
---

# ITEM-259: Picker popout scrollbars sit at the menu edge

## Summary

The entry modal's Book search and Chapter/verse popouts paint their 5px scrollbar inside the menu's
8px padding, so the bar floats in the panel instead of belonging to its edge. Move the scrollport to
the menu's inner border with compensating content padding and clip its last pixels at the corner.

## Notes

- Measured at 1440×900: scrollport right/bottom 929/883 against a menu edge of 938/892; after the
  fix 937/891. The first option and the in-menu filter keep their boxes.
- CSS-only change in `static/styles/design/components.css` with a focused Playwright E2E module.
- The card ID was retaken from ITEM-258 after the navigation slice claimed that number in flight.

## Acceptance sketch

- The bar's right and bottom edges meet the menu's 1px border with no canvas between.
- The option rows, group headings and filter stay where they were; a one-option menu draws no bar.
- Filtering, highlight, Tab commit and scroll-follow keep their accepted behaviour.

## Links

- Spec: [244-picker-menu-scrollbar-edge](../specs/244-picker-menu-scrollbar-edge/spec.md)
- Related items: ITEM-251 (the dialog's own edge), ITEM-253 (searchable passage pickers)
