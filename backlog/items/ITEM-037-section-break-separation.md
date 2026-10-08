---
id: ITEM-037
status: in_review
title: 'Give the section break a clear separation in the Tata Ibadah pane'
type: chore
priority: P2
effort: S
created: 2026-10-08
updated: 2026-10-08
spec: specs/035-section-break-separation/spec.md
branch: chore/035-section-break-separation
pr:
archived_at:
archive_reason:
bump: patch
release_version: 1.3.3
---

# ITEM-037: Give the section break a clear separation in the Tata Ibadah pane

## Summary

A section break should read as an unmistakable divider between parts of the service. Today the two
forms of it look different and neither separates strongly: a legacy END_OF_SECTION draws a short
centred rule with a diamond, while a `section_break` entry renders as an ordinary item heading. Give
the section break one clear, consistent separation.

## Notes

- **Two shapes today.**
  - Legacy `TataIbadahItemType.END_OF_SECTION` renders `<div class="tatib__eos">` — a `min(220px,
    60%)` centred `1px` rule with a diamond `::after`, plus an optional dim uppercase note
    (`static/styles/design/components.css` §954–981).
  - A `ServiceEntry` of kind `section_break` renders as a normal `.tatib__item` whose label is its
    `h2` heading (`_tatib_stage()` in `multimedia/web/reading/views.py` sets `note` for it, and
    `multimedia/web/templates/reading/tatib.html` renders the section), so it carries no rule at all.
- **The goal.** One clear separation for a section break on the Tata Ibadah page — decide whether the
  legacy rule and the entry form converge on a single treatment.
- **Tokens.** Use the existing divider/ink tokens so light and dark both read.

## Open questions

- Full-width rule, or a wider centred one? How much contrast (weight/colour)?
- Does the separation show the break's label/note under the rule, or is it a bare divider?
- Do the legacy END_OF_SECTION rule and the `section_break` entry become one shared treatment?
- Any spacing change (the current rule sits in `34px` top/bottom margins)?

## Acceptance sketch

- A section break reads as a clear separation between the entries around it, in both themes.
- The legacy END_OF_SECTION and the `section_break` entry look consistent with each other.
- The change is confined to the pane's section-break rendering; other entries are untouched.

## Links

- Spec: [035 — Give the section break a clear separation](../../specs/035-section-break-separation/spec.md)
- Related items: ITEM-007 / spec 006 (service entries), ITEM-008 / spec 007 (the old rows)
