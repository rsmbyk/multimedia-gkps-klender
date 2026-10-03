---
id: ITEM-007
title: Service entries — a Tata Ibadah holds texts, scriptures and songs
status: in-progress
type: feat
priority: P1
effort: L
spec: specs/006-service-entries/spec.md
branch: feat/006-service-entries
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
- The owner's answers (2026-10-03) are folded into spec 006: `ServiceEntry`; a project button
  opening the new projector in a new tab with previous/next/toggle; hand-written pages on the
  public design tokens; new `/obs/service/...` URLs; display mode held on the server so every tab
  shares it, with entry writes refused while a Tata Ibadah is displaying; soft deletion for songs,
  songbooks and verses with a deleted-target warning on the entry; jump-to-it controls on
  scripture and song entries.
- One reading to confirm: "always sync with the songs" is taken to mean *exclusions* are stored
  (a verse added later shows; an unchecked one stays out) rather than a frozen verse list.
- Blocked on the owner's Accept of spec 006 (and that one confirmation).
