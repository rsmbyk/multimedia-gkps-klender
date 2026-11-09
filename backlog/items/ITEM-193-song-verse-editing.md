---
id: ITEM-193
status: speccing
title: 'An ordinary song''s verses are added, edited, removed and reordered on its own page'
type: feat
priority: P2
effort: L
created: 2026-11-05
updated: 2026-11-05
spec: specs/189-song-verse-editing/spec.md
branch: feat/189-song-verse-editing
pr:
issue:
closed_at:
closed_reason:
bump:
release_version:
---

# ITEM-193: An ordinary song's verses are added, edited, removed and reordered on its own page

## Summary

A song of an ordinary songbook has no live editor for its verses. The song page renders the lyrics and
nothing else; the only verse writer is the REST resource `/api/songs/verses/`, and the management
screen that used it (`/manage/songs/songs/<id>/`) still loads `static/web/songs/verses/index.js`, a
file this repo does not contain. The request: add, edit, remove and reorder those verses from the song
page itself.

## Notes

- Measured on the local library: 281 ordinary songs hold live verses, all numbered `1…n` with no gap;
  seven hold none. 448 service entries name a verse of an ordinary song (433 exactly one, 12 two, 3
  three) and 1,655 ordinary verses are named by at least one entry; 829 setlist items name an ordinary
  song.
- The verse number is a reference key, not only a label: `ServiceEntry.verses` and
  `SongBookmarkItem.verse` both store numbers, so a reorder that renumbers has to answer what happens
  to a prepared service's selection.
- Hymn songs and their verses are read-only by decision (spec 005), and this slice keeps that rule.
- `songs.Verse` is soft-deleted and its `unique_together` covers deleted rows too, so renumbering into
  a soft-deleted verse's number needs the constraint narrowed to live rows.

## Acceptance sketch

- On an ordinary song's page: `Add verse` appends; each verse edits in place; a grip drags (and takes
  the arrow keys) to reorder; delete asks once, naming what else uses the song.
- After every verb the page reads `1…n` and the lyrics sit in the written order, without a reload.
- A service entry that named verse `k` still projects the same lyric after a reorder.
- A hymn song's page draws no verse control and every endpoint refuses the write.

## Links

- Spec: [189](../specs/189-song-verse-editing/spec.md)
- Related items: ITEM-170 (spec 162, the verse-less song), ITEM-192 (spec 188, the bookmarks that
  became services)
