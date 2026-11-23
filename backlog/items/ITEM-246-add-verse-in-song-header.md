---
id: ITEM-246
status: ready
title: 'Add verse sits beside Project in the song header'
type: fix
priority: P2
effort: S
created: 2026-11-23
updated: 2026-11-23
spec: 231-add-verse-in-header
branch: fix/231-add-verse-top
pr:
issue: 603
closed_at:
closed_reason:
bump: patch
release_version:
---

# ITEM-246: Add verse sits beside Project in the song header

## Summary

On a song with verses, the Add verse control sits at the foot of the lyric column while the
Project action lives in the header. Move Add verse into the header group immediately left of
Project, keeping its dashed identity and gating it on edit permission plus at least one live
verse. A song with no verses keeps only the centred invitation button.

## Notes

- Measured before, 1440×900 on `/songs/1880/`: Project 96×34 at x=1276, y=42; dashed add row
  1291×38 at x=80, y=846 with its button 112×38 at x=124.
- Measured after: header group 214×34 at x=1157, y=42 holding Add verse 111×34 then Project
  96×34, 8px gap; no dashed row. Empty song `/songs/1909/` unchanged.
- The moved control keeps `[data-add-verse]`; exactly one such node per state is required by the
  reorder write in `songs_verse.js`.

## Acceptance sketch

- A song with verses shows Add verse left of Project, both 34px tall, 8px apart.
- Clicking it opens `New verse` without a reload.
- A song with no verses shows no header actions and one centre Add verse.
- Hymn and read-only songs show no header actions.

## Links

- Spec: [231-add-verse-in-header](../../specs/231-add-verse-in-header/spec.md)
- Related items: ITEM-239 (empty song Add verse), ITEM-245 (verse script boot)
