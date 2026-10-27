---
id: ITEM-149
status: speccing
title: 'The landing search field sits 49px below the window''s middle'
type: fix
priority: P2
effort: S
created: 2026-10-27
updated: 2026-10-27
spec: specs/139-home-search-center/spec.md
branch: feat/139-home-search-center
pr:
issue:
closed_at:
closed_reason:
bump:
release_version:
---

# ITEM-149: The landing search field sits 49px below the window's middle

## Summary

The landing page centres the logo and the search field as one block, so the field — the page's only
control — lands half the logo block below the window's middle. Measured +49px at 1440×900 (field centre
499, window 450) and +85px on a 390×844 phone, where the section is also 36px taller than the space the
stage leaves it. The owner's report: "center the search bar vertically", with a screenshot of the field
below the middle.

## Notes

- The block is already centred (399–577 in a 1000px window, ±5px), so the report can only be about the
  field; that measurement replaces a Clarify question.
- Two offsets compose: 61px — half the 96px logo plus its 26px gap — and 12px, the stage's asymmetric
  padding (40 above, 64 below) pushing the section's own middle above the window's.
- The phone layout adds a third: `min-height` subtracts `--pad-top` (40) while the stage pads 76 for the
  toolbar, so the section is 36px taller than its space and its middle sits 18px low.
- CSS only: `.stage` states its two vertical paddings as tokens, `.search-home__inner` becomes a
  three-row grid so the field is the middle row, and the logo hangs in the top row.

## Acceptance sketch

- The field's box centre equals the window's middle within 1px from 320px to 1920px wide.
- The logo stays fully above the field with its 26px gap, and the landing page stays one window tall.
- The results bar (field top 46 / 82, results 128 / 164) and the reading page do not move.

## Links

- Spec: [139](../specs/139-home-search-center/spec.md)
- Related items: ITEM-005 (spec 004 — the search-first home), ITEM-148 (spec 138 — the phone toolbar
  whose padding this slice makes measurable)
