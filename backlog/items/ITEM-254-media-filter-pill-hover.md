---
id: ITEM-254
status: speccing
title: 'Media Library filter pills have no hover feedback'
type: feat
priority: P2
effort: S
created: 2026-11-24
updated: 2026-11-24
spec: 239-media-filter-pill-hover
branch: feat/239-media-filter-pill-hover
pr:
issue:
closed_at:
closed_reason:
bump: patch
release_version:
---

# ITEM-254: Media Library filter pills have no hover feedback

## Summary

The six pills in the Media Library's filter row — five file types and Unused — keep
their transparent fill and divider border when pointed at, while the sort button and
the head icon buttons beside them change on hover. Give the unpressed pills the same
focus-border and hover-fill pair so the row answers the pointer; a pressed pill keeps
its accent fill.

## Notes

One CSS rule on `.media-library__chips button:not([aria-pressed="true"]):hover` in
`static/styles/design/components.css`. The pair matches the existing sort and icon
button hover and the dock's chip hover. No template, script, token or endpoint
change. The live preview and its before/after measurements are in the spec pack.

## Acceptance sketch

- Hovering any unpressed pill paints `--icon-hover-bg` over transparent and swaps
  `--divider` for `--focus`, in both themes.
- A pressed pill's fill, border and text stay at the accent values under the pointer.
- Pill boxes stay 63.36 × 30 px at 1440 px; focus-visible outline, dot separator,
  filter behaviour and the rest of the app are unchanged.

## Links

- Spec: [239-media-filter-pill-hover](../specs/239-media-filter-pill-hover/spec.md)
- Related items: —
