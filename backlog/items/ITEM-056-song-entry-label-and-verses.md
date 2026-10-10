---
id: ITEM-056
status: speccing
title: 'Label song entries by their short hymn reference and show the selected verses'
type: chore
priority: P2
effort: S
created: 2026-10-10
updated: 2026-10-10
spec: specs/054-song-entry-label-and-verses/spec.md
branch:
pr:
archived_at:
archive_reason:
bump: patch
release_version:
---

# ITEM-056: Label song entries by their short hymn reference and show the selected verses

## Summary

On the Tata Ibadah stage a hymn song still reads `Haleluya 3` (long book name), and the preview
modal's header reads `Haleluya — Sai puji Naibata`, while the section sidebar and the pickers
already use the short reference. The stage and the modal should read `HAL 3 — Sai puji Naibata`.
Separately, a song entry that keeps only some of a song's verses shows no hint of the selection;
the stage should show `Bait 1, 3` under the heading when the entry does not include every verse.

## Notes

- Owner asked for both while reviewing the live `/tatib/142/` page on 2026-10-10 (screenshot);
  the approved preview settled the choices: serial **with title**, **em dash**, verse line
  `Bait 1, 3` (no “dari N”).
- Spec 039 moved the sidebar label to the short form; this extends the same treatment to the
  stage heading and the modal header, and leaves the sidebar's form untouched.
- The heading comes from `ServiceEntry.citation()` (`multimedia/tatib/models.py`), changed for
  numbered hymn songs; the modal's header is built separately in `_entry_preview()` and reuses
  that string for those songs so the two can never drift. A non-hymn song's or an unnumbered
  hymn's header stays as today.
- The stage template already has the `read__sub` hook (`tatib.html`); the verse line needs the
  view data and its CSS rule, not new template markup.
- Spec-006-era assertions encoding `Kidung Jemaat 152` are updated deliberately (listed in
  `tasks.md`).

## Acceptance sketch

- A hymn song entry's stage heading reads `KJ 152 — Ada Kuasa dalam DarahNya`; the same string
  is the preview modal's header (other songs' headers unchanged).
- A partial selection shows `Bait 1, 3` under the heading; a full selection shows nothing.
- The sidebar row keeps `HAL 3 Sai puji Naibata`; the projector and the pickers are unchanged.

## Links

- Spec: [054 — Label song entries by their short hymn reference and show the selected verses](../../specs/054-song-entry-label-and-verses/spec.md)
- Related items: ITEM-041 / spec 039 (the sidebar's short form), ITEM-034 / spec 032 (the entry
  preview modal), ITEM-007 / spec 006 (service entries)
