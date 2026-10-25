---
id: ITEM-133
status: in_progress
title: 'An empty Tata Ibadah quarter-centres its five add tiles'
type: fix
priority: P2
effort: S
created: 2026-10-25
updated: 2026-10-25
spec: specs/130-empty-service-tiles/spec.md
branch: fix/130-empty-service-stage
pr:
issue:
closed_at:
closed_reason:
bump: patch
release_version:
---

# ITEM-133: An empty Tata Ibadah quarter-centres its five add tiles

## Summary

An empty service drew its five add actions as full-width labelled buttons stacked under the date, so the
only content on the page sat in its top third and the rest was blank — the page read as unfinished rather
than as an invitation. The five labels also repeat what an operator learns once.

## Notes

- The block centres in the reading area the header leaves, not in the whole window: the header is furniture
  and centring through it would crowd the date.
- The tiles are square, icon-only, 52px, in one row; the sentence survives as the accessible name and the
  tooltip. `Add Media` gains the glyph it never had.
- Five full tiles need 300px of reading column. Narrower, they take three and two at full size rather than
  shrinking below a 44px target.
- Three renderers must agree: the server template, the saved renderer and the post-delete rebuild.
- A service that holds items keeps its header-to-body gap and top-aligned flow.

## Acceptance sketch

- An empty service shows one block a quarter of the way down the reading area: heading, hint, one row of
  five square tiles.
- The block's centre is on the quarter mark at 1440×900, 1280×800, 1024×700 and 390×844, clear of the header.
- Hovering a tile names it; keyboard focus keeps its ring; clicking one opens the same editor.
- Deleting the last entry leaves the same centered row, and the saved copy matches the server page.

## Links

- Spec: [`specs/130-empty-service-tiles/spec.md`](../../specs/130-empty-service-tiles/spec.md)
- Related items: ITEM-132 (the sidebars' empty states, the same session's other half)
