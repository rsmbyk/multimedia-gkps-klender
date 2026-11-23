---
id: ITEM-239
status: ready
title: 'An empty song paints Add verse twice'
type: fix
priority: P2
effort: S
created: 2026-11-23
updated: 2026-11-23
spec: 224-empty-song-add-verse-row
branch: fix/224-empty-song-add-verse-row
pr:
issue: 590
closed_at:
closed_reason:
bump:
release_version:
---

# ITEM-239: An empty song paints Add verse twice

## Summary

On a song with no live verses the stage draws the normal after-the-last-verse `Add verse` row
even though there is no last verse, and then the empty invitation draws a second identical
button. Measured on `/songs/1731/` at 1440×900: two `[data-add-verse]` buttons, the stray row
520×38 at y=167.9 directly above the 520×128 invitation. The invite already says "Add the first
verse", so the extra control has no verse to follow and no job to do.

## Notes

- The gate is `verse_rows` in `reading/song.html` — the same list `SongDetailView` already
  passes, filtered to `is_deleted=False`.
- The invitation's button is the one to keep; the row's own button is byte-identical markup.
- Out of scope: verse write endpoints, permissions, hymn pages, invitation copy and button styling.

## Acceptance sketch

- An empty editable song paints exactly one `Add verse`, inside the empty invitation.
- A song with verses keeps its one after-the-last-verse row in the same box.
- Saving the first verse from the invitation swaps the invitation for verse 1 plus one row,
  without a reload.
- The empty invitation's title sits at the same height as the Tata Ibadah empty title:
  y=253.9 vs 253.5 at 1440×900, y=199.0 vs 198.6 at 900×700.

## Links

- Spec: [224-empty-song-add-verse-row](../../specs/224-empty-song-add-verse-row/spec.md)
- Related items: ITEM-193 (song verse editing), ITEM-170 (empty song in the entry picker)
