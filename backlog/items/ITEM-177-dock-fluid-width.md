---
id: ITEM-177
status: in-review
title: 'The dock fills whatever panel it is given'
type: fix
priority: P2
effort: S
created: 2026-10-29
updated: 2026-10-29
spec: specs/164-dock-fluid-width/spec.md
branch: fix/164-dock-fluid-width
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/464
issue:
closed_at:
closed_reason:
bump: patch
release_version:
---

# ITEM-177: The dock fills whatever panel it is given

## Summary

The dock page caps itself at `560px` and centres with `margin: 0 auto` (`obs-dock.css:29–39`), so an
OBS dock the operator has widened keeps a 560px panel with a strip of bare background on each side:
measured on develop (1.23.1), the panel is 560 × 900 at x 170 in a 900px window and at x 680 in a
1920px one, while the picker's rows stay 544px at every width above 560. The panel should fill the
dock at every size — the dock's viewport *is* the panel — with the picker staying one column and its
rows running with the width.

## Notes

The sheet's own header comment already claimed the panel "fills the viewport"; the cap was the one
line contradicting it, and it is the only `max-width` in `obs-dock.css`. Everything below the panel
was already fluid (the head is a flex row, the body a block scroller with 8px side padding, the rows
`width: 100%`), so the fix is two declarations.

A bucket-per-column layout at 760px and up was built and measured first (three columns of 468px at
1440, 628px at 1920, a wrapped third bucket between 760 and 1100) and rejected: the picker stays one
column at every width, recorded as FR-003 so the variant is not rebuilt from the same report.

## Acceptance sketch

- At 320, 420, 560, 720, 900, 1440, 1920 and 2560 the panel's width equals the viewport's, its left
  edge is 0, and the page reports no horizontal overflow.
- At 1440 the first picker row is 1424px wide (viewport − 16) with its date on the row's right
  padding; at 1920, 1904px; at 560, 544px — unchanged from 1.23.1.
- The picker body stays `display: block` with all four buckets at one x, and the bucket head still
  computes `sticky` at every width.
- The runner is untouched; a 420px dock paints exactly as it did.

## Links

- Spec: [164](../specs/164-dock-fluid-width/spec.md)
- Related items: ITEM-119 (the dock, spec 119)
