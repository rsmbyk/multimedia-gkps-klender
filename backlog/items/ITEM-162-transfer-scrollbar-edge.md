---
id: ITEM-162
status: in-progress
title: 'The Transfers scrollbar floats inside the dialog and stops short of its bottom'
type: fix
priority: P2
effort: S
created: 2026-10-29
updated: 2026-10-29
spec: specs/152-transfer-scrollbar-edge/spec.md
branch: feat/152-transfer-scrollbar-edge
pr:
issue: 433
closed_at:
closed_reason:
bump:
release_version:
---

# ITEM-162: The Transfers scrollbar floats 22px inside the dialog

## Summary

The Transfers dialog's list is a plain child of the dialog, so it starts at the dialog's *content*
box: the dialog's `padding: 22px` and its 1px border stand between the list's edges and the dialog's
own, and the engine paints the app's 5px scrollbar against the list's edge. The bar therefore reads as
floating inside the dialog — 22px of canvas between its right edge and the dialog's border, and its
lane stopping 23px above the dialog's bottom border.

The bar moves to the dialog's right and bottom edges (owner, gate-1 revision: "also touches the
vertical edges ... bottom edge only"); the rows, the title, the age headings, the list's top and the
22px the last row keeps above the border at the end of the scroll stay exactly where they are today.

## Notes

- Owner report, with a screenshot of the Transfers dialog over `/media-library/`: "make the scrollbar
  touches the edge".
- Measured on the running app (headed Chromium, 1440×760, dpr 1, develop @ `24a6d6d2`, fifteen
  transfers): dialog border box x 430→1010, list box x 453→987, the bar's 5px lane x 982→986 —
  22px of canvas to the dialog's border. Rows run 453→982 (23px / 28px insets).
- The list is the scroll container since spec 149; this is the follow-on to that drawing fix, not a
  change to what scrolls.
- Headless Chromium paints overlay scrollbars here (0px lane, no thumb), so the E2E can measure the
  list's box but not the painted bar; the painted gap is measured by the preview's probe in a headed
  browser.

## Acceptance sketch

- With a list taller than the dialog, the bar's right edge sits against the dialog's right border —
  0px of canvas between them (was 22px) — and its lane ends at the bottom border (was 23px above it);
  the list's box reaches 1px inside the dialog's border box on the right and the bottom.
- The rows' content does not move: 23px from the dialog's left, 28px from its right with the bar and
  23px without it.
- The title, the age headings, the list's top and the 22px end-of-scroll gap are unchanged; the
  dialog clips its content to its 12px corner, so the bar cannot paint over it.
- Shown at 1440×760 and 420×820, light and dark, library-opened and rail-opened.

## Links

- Spec: [152](../../specs/152-transfer-scrollbar-edge/spec.md)
- Related items: ITEM-159 (spec 149 — the list became the scroll container), ITEM-070/ITEM-090
  (specs 067/087 — the bar's own drawing)
