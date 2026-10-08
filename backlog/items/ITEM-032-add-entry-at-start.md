---
id: ITEM-032
status: speccing
title: 'Add a service entry at the beginning of a Tata Ibadah'
type: feat
priority: P2
effort: M
created: 2026-10-08
updated: 2026-10-08
spec: specs/030-add-entry-at-start/spec.md
branch:
pr:
archived_at:
archive_reason:
bump: minor
release_version:
---

# ITEM-032: Add a service entry at the beginning of a Tata Ibadah

## Summary

Entries can only be inserted **after** an existing row (or appended when the service is empty).
There is no way to insert one at the very **start** of the running order. Give the editor an
affordance to add an entry at the beginning, and the server the insertion logic to place it first.

## Notes

- **Today's flow.** The pane renders an add bar after each row carrying
  `data-entry-after="{{ item.after_marker|default:item.anchor }}"`
  (`multimedia/web/templates/reading/tatib.html`); the empty-state buttons carry no `after`.
  `static/web/entries.js` reads `[data-entry-after]`, and `newUrl()` appends `&after=` to the new-form
  URL.
- **Server insertion.** `editor_save` in `multimedia/web/reading/views.py` only places a new entry
  **after** a marker — `e<id>` (entry) or `l<id>` (legacy row) — shifting both tables; with no marker
  it appends via `next_order_number()`. `_compact_service_order()` normalizes legacy reorderings
  first.
- **The start case.** Add a marker/param meaning "at the beginning" and insert at order 1, shifting
  every existing `ServiceEntry` and legacy `TataIbadahItem` up by one so the shared order stays
  contiguous from 1 (ITEM-007/ITEM-008 invariant).
- **Carry it through the form.** The editor fragment passes `after` via GET and re-renders it on a
  400 (`_editor_fragment_context`, and the `after` read from `request.POST`); the start marker has to
  survive that round trip too.

## Open questions

- UI shape: a leading add bar mirroring the per-row bar (all four kinds), or a single "Add at start"
  action?
- Reuse the existing `after` plumbing with a sentinel (e.g. `after=start`), or a distinct parameter?

## Acceptance sketch

- From a Tata Ibadah that already has items, I can add an entry at the beginning.
- The new entry becomes order 1; the others shift and the order stays contiguous, spanning both old
  rows and entries.
- The reading pane and the projector both show the new entry first.

## Links

- Spec: [030 — Add a service entry at the beginning](../../specs/030-add-entry-at-start/spec.md)
- Related items: ITEM-007, ITEM-008 (service order editor), ITEM-028 (live projection editing)
