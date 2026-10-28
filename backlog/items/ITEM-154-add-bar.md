---
id: ITEM-154
status: in-review
title: 'The add bar opens over the seam, and nothing moves'
type: chore
priority: P1
effort: M
created: 2026-10-28
updated: 2026-10-28
spec: specs/143-add-bar/spec.md
branch: feat/143-add-bar
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/414
issue: 413
closed_at:
closed_reason:
bump: patch
release_version:
---

# ITEM-154: The add bar opens over the seam, and nothing moves

## Summary

Hovering a service entry reveals the two add rows around it, and each one buys 43.6px from the page:
the entry under the pointer drops 31.6px out from under it (13.6px more for the first entry), and a
sweep down eight entries accumulates 234.8px of movement. The script carries a `poised` guard whose
own comment names the cause; the guard survives the oscillation instead of removing it.

The rows keep their place in the flow — a 20px slot, the same gap the entries had — and their bar is
drawn on top of it: absolutely positioned, centred on the seam, with the seam line always hinted at
rest. Nothing above, below or under the pointer moves.

## Notes

- Owner report with a screenshot of `/tatib/142/`: "it makes it unpredictable when you hover one and
  it moved down or up. maybe something that pushes the other entries around it instead of itself".
- The bar floats rather than reserving space: reserving costs 892px of page on one 24-entry service,
  and moving the adds into the controls column costs a click and a popover. Both were built and shown
  in the comparison page before this was chosen.
- The start bar is the same object at the top of the service; the head's margin grows to 34px so the
  first seam measures the same 53px of white as the ones between entries.
- Eight E2E tests assert the replaced mechanism (0px at rest, 8px padding when open, the 13.6px
  start-bar shift). They are rewritten by this slice.

## Acceptance sketch

- Pointing at any entry moves nothing: 0.0px per entry across a sweep, page height unchanged.
- The bar is drawn over the seam, centred on the column, its hit area only as wide as its buttons.
- The seam paints at `.15` at rest and `.6` open; a hovered button is solid-bordered and opaque.
- Keyboard and touch both reach the buttons.

## Links

- Spec: [143](../specs/143-add-bar/spec.md)
- Depends on: 142 (the entries are bare, so the bar is the only surface on the stage)
- Replaces: the reveal model of specs 037 (ITEM-039), 052, 055
