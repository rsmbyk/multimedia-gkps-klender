---
id: ITEM-040
status: speccing
title: 'Remove the label from section-break entries'
type: chore
priority: P2
effort: S
created: 2026-10-08
updated: 2026-10-08
spec: specs/038-drop-section-break-label/spec.md
branch:
pr:
archived_at:
archive_reason:
bump: patch
release_version:
---

# ITEM-040: Remove the label from section-break entries

## Summary

A `section_break` entry currently carries a **label** (stored in the shared `title` field, edited via
the form's "Label" input). Drop it: a section break is just a break, with no label.

## Notes

- **Where the label lives.** `ServiceEntry.title` is shared by kinds; for a `section_break` it *is*
  the label. `multimedia/web/reading/entries.py` `SectionBreakEntryForm.Meta.fields` includes
  `title`, and `TITLES['section_break']` drives the modal's wording.
- **Where it is read.** `ServiceEntry.resolve()` returns `(self.title, '')` for a section break, and
  `_tatib_stage()` in `multimedia/web/reading/views.py` uses `row.title` as the block's title and its
  `note`.
- **The legacy row is different.** `TataIbadahItem` END_OF_SECTION keeps its own note text (a
  liturgist's cue, shown small under the rule); this item is about `ServiceEntry` breaks only.
- **Interacts with ITEM-037 / spec 035**, which planned a shared divider showing "the break's
  label/note under the rule". With no label on entry breaks, only the legacy note remains.
- **The model column stays.** `title` is still used by text entries; the break simply never sets it.
  The projector's blank section-break screen is unaffected.

## Open questions

- Labels already stored on existing breaks: left in place (unused) or cleared on next save?
- The TOC label for a break falls back to the kind display ("Section break") — acceptable?

## Acceptance sketch

- The section-break editor offers no label input.
- A saved section break stores no label, and none is shown in the pane.
- Existing text entries keep their title control; the legacy END_OF_SECTION note is untouched.

## Links

- Spec: [038 — Remove the label from section-break entries](../../specs/038-drop-section-break-label/spec.md)
- Related items: ITEM-037 (section-break separation), ITEM-007 / spec 006 (service entries)
