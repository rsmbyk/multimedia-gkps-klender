---
id: ITEM-007
title: Service entries — a Tata Ibadah holds texts, scriptures and songs
status: speccing
type: feat
priority: P1
effort: L
spec: specs/006-service-entries/spec.md
branch:
pr:
bump: minor
release_version:
created: 2026-10-03
updated: 2026-10-03
---

# ITEM-007: Service entries

## Summary

Let one Tata Ibadah hold everything a service needs — plain texts, Bible passages, songs and
section breaks — so one surface drives a whole service instead of three docks prepared and
toggled separately. Editing happens in the content pane, with a modal per kind: the scripture
modal cascades book → chapter → verse (resetting to 1), the song modal offers a searchable,
songbook-grouped pick and a verse checklist that starts with everything included. Entries
reorder by drag, holding changes until Save or Discard and confirming before leaving with
unsaved ones.

## Compatibility

Additive only. The current OBS dock, sources, projection and API are not touched — the new
system gets its own projector, its own overlay, its own pages and its own sync channel — and
existing `TataIbadahItem` rows and endpoints keep working as they are. Migrating the old rows is
a separate, later slice the owner triggers.

## Notes

- Drafted from the owner's description of how services are prepared today (three lists, one dock
  talking to the display at a time) and the display rules the operator relies on (two lines per
  body, font fitting on the projector, box growth on the overlay, blank line as the pause).
- Blocked on the owner's Accept of spec 006, and on the open questions in it (model name, what
  drives the new display, its stack, its URLs).
