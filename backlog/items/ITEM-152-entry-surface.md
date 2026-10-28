---
id: ITEM-152
status: done
title: 'A service entry draws no box until it is pointed at'
type: chore
priority: P2
effort: S
created: 2026-10-28
updated: 2026-10-28
spec: specs/142-entry-surface/spec.md
branch: feat/142-bare-entry-surface
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/412
issue: https://github.com/rsmbyk/multimedia-gkps-klender/issues/411
closed_at: 2026-10-28
closed_reason: merged into develop (412)
bump: patch
release_version:
---

# ITEM-152: A service entry draws no box until it is pointed at

## Summary

Every service entry wears a resting surface since spec 068: a fill at 1.2% ink and a 1px inset ring.
Measured, the fill is 3 of 255 levels over the canvas (1.027 : 1) — invisible — so the ring carries the
whole signal and a 24-entry service reads as 24 faint rectangles. The box was also standing in for
spacing: the rule meant to separate entries never matches while the add rows sit between them.

The entries keep their box — the padding, the 56px floor, the reserved controls column, the media
tile, the section break's rule — and lose the paint. Hover, deliberate focus and an open modal still
fill the row with `--icon-hover-bg`, and that fill is now the only surface on the page.

## Notes

- Owner request with a screenshot of `/tatib/142/`: "i dont feel like the border and a slight fill
  there"; then "try bare as default, then filled when being hovered"; then, shown on all five kinds in
  `/tatib/144/`, "leave all kinds bare — media reads fine up close".
- Four candidates were weighed in a static comparison built from the live markup — bare, hairline
  rules, a hanging `L :`/`J :` gutter, and a visible 4% fill without the ring. The gutter lost because
  the entries' left margin is not where the problem was; the rules lost because the section break's
  2px rule is the only divider that means anything.
- Supersedes the visual detail of spec 068; the tokens it introduced are deleted, and the two E2E
  tests that read them now assert the canvas instead.

## Acceptance sketch

- At rest nothing is painted: `rgba(0, 0, 0, 0)` and `box-shadow: none`, light and dark.
- Hover, deliberate focus and modal-origin fill with `--icon-hover-bg`; quiet restoration does not.
- The box is unchanged: 8/8/8/12 padding, 56px floor, 106/264px controls column, 9px radius.
- Media keeps its 64px tile column and 80px height; the section break keeps its rule and diamond.
- No other surface moves.

## Links

- Spec: [142](../specs/142-entry-surface/spec.md)
- Supersedes: [068](../specs/068-tatib-entry-surface/spec.md) (ITEM-071)
- Related: ITEM-036 (the hover fill this now carries alone), ITEM-151 (the other thing this stage
  wore at rest)
