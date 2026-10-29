---
id: ITEM-173
status: in-review
title: 'A small image or a PDF page fills the projector stage'
type: feat
priority: P1
effort: S
created: 2026-10-29
updated: 2026-10-29
spec: specs/158-projector-media-fit/spec.md
branch: feat/158-projector-media-fit
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/455
issue: https://github.com/rsmbyk/multimedia-gkps-klender/issues/437
closed_at:
closed_reason:
bump: minor
release_version:
---

# ITEM-173: A small image or a PDF page fills the projector stage

## Summary

The projector paints an image at its own pixel size and a PDF page at its own page size: `182×277` on a
`1856×1104` stage for `images.jpeg`, `612×792` for a Letter page. Both are legible on the operator's
laptop and unreadable from the room. Media smaller than the stage should be enlarged to the fit that
shows all of it — the smaller of the width and height ratios — and `T` should switch between fit width
and fit height, with the shortcut listed for images and PDFs.

## Notes

Measured on the compose page (1920×1200 window, stage 1856×1104): `images.jpeg` paints 182×277 at
(829, 445.5); the Receipt PDF page paints 612×792 at (654, 188). `media-pdf.js:48` clamps its scale
with `Math.min(1, …)`, and `.screen__image` (`max-width/max-height: 100%`) never enlarges.

## Acceptance sketch

- A portrait image smaller than the stage paints at the stage's height, whole, with its width in
  proportion — 725×1104 for `images.jpeg` at 1920×1200.
- `T` fills the stage's width instead (1856×2824, cut 860 above and below); `T` again returns to the
  fit. The cut part is reached by dragging the page or rolling the wheel, clamped at its edges.
- A PDF page follows the same rule (853×1104 for a Letter page).
- The shortcut sheet lists `T` under a group naming images and PDFs, and the sheet still fits a
  1280×720 window.

## Links

- Spec: [158](../specs/158-projector-media-fit/spec.md)
- Related items: ITEM-116 (video display), ITEM-117/118 (PDF and PowerPoint display, specs 117/118)
