---
id: ITEM-054
status: in_review
title: 'Collapse the hidden add rows and tighten the section break'
type: chore
priority: P2
effort: S
created: 2026-10-10
updated: 2026-10-10
spec: specs/052-collapse-hidden-add-rows/spec.md
branch:
pr:
archived_at:
archive_reason:
bump: patch
release_version: 1.3.18
---

# ITEM-054: Collapse the hidden add rows and tighten the section break

## Summary

Every hidden `.entry__add` row reserves its full height (~45px, ~71px when wrapped) while `opacity: 0`,
and the section break adds 34px margins — together ~115px of apparent emptiness above the first entry and
~45–71px between every pair of entries. Collapse hidden rows to zero height (expand on reveal, as now)
and reduce the break's margins to 16px.

## Notes

- The reservation exists so a hidden row stays hittable (comment in `components.css:1467-1473`); the
  grid 0fr/1fr collapse keeps the box through the hide transition, so the pointer path stays open.
- Reveal triggers (spec 036/037) are unchanged: adjacent-sibling CSS, `:hover`, `:focus-within`,
  and `is-revealed` from `entries.js`.
- Touch (coarse pointer, no hover) shows the rows outright, mirroring the `.entry__acts` rule.
- Amends spec 035 (break margins) and specs 036/037 (resting height only; reveal rules intact).
- Owner saw the space in a full-width screenshot of `/tatib/142/` on 2026-10-10.

## Acceptance sketch

- At rest no add row is visible; consecutive entries sit a few pixels apart.
- Hovering or focusing an entry expands the rows above and below it without moving the entry; a
  revealed row keeps only itself shown and never highlights the entry above.
- Tabbing onto a collapsed row's button expands that row; a no-hover device shows all rows.
- The section break keeps its rule and dot with 16px margins; the start bar stays always visible.

## Links

- Spec: [052 — Collapse the hidden add rows and tighten the section break](../../specs/052-collapse-hidden-add-rows/spec.md)
- Related items: ITEM-037 / spec 035 (break separation), ITEM-038 / spec 036 (add bar outside item hover), ITEM-039 / spec 037 (rows before and after)
