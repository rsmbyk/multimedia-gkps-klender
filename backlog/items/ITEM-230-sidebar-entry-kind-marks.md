---
id: ITEM-230
status: done
title: 'A service entry''s sidebar row marks its kind'
type: feat
priority: P2
effort: S
created: 2026-11-21
updated: 2026-11-21
spec: 214
branch: feat/214-sidebar-entry-kind-marks
pr: 569
issue: 565
closed_at: 2026-11-21
closed_reason: merged into develop (PR #569)
bump: patch
release_version:
---

# ITEM-230: A service entry's sidebar row marks its kind

## Summary

The Tata Ibadah contents list — the second sidebar column, `#chList` — prints each entry's order number
and then its label. It carries no kind mark of any sort: the stage's passage/song glyphs (spec 144),
the media family chip and the slot badges (spec 213) all stop at that surface's edge. The request: add a
column after the order number that carries the corresponding icon or mark of the entry, so the order can
be scanned by kind without reading each label.

## Notes

- Spec 144 FR-008 and spec 213's sidebar edge case explicitly kept `#chList` on its own anatomy. This
  card is the owner's reversal of that boundary for the contents list; the stage and dock keep theirs.
- The entry kinds a service can hold are passage, song, text, media and section break, plus fill-in and
  choice on a template, plus the legacy `TataIbadahItem` row. The mark set has to say what each of them
  is, including the kinds that carry no glyph on the stage today.
- The mark is decorative: the row already names its entry in words, so the icon takes no pointer and is
  hidden from assistive technology.
- The contents list is rebuilt in place after an entry is saved or deleted; the column has to survive
  that rebuild as well as the first server render.

## Acceptance sketch

- Every contents row paints its kind's mark in a dedicated column immediately after the order number.
- The marks are told apart at a glance, in both themes, at the full sidebar and drawer widths.
- The column adds no height to a row and does not break the three-line label cap (spec 135).
- A row whose label wraps, a deleted target and a legacy row all keep their mark.

## Links

- Spec: `specs/214-sidebar-entry-kind-marks/spec.md`
- Related items: ITEM-160 (passage and song kind marks, spec 144), ITEM-228 (slot kind badge, spec 213),
  ITEM-145 (the contents row's three-line cap, spec 135)
