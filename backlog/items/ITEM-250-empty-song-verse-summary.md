---
id: ITEM-250
status: in-review
title: 'An empty song hides the whole Verses section instead of naming itself'
type: fix
priority: P2
effort: S
created: 2026-11-24
updated: 2026-11-24
spec: 235-empty-song-verse-summary
branch: fix/235-empty-song-verse-summary
pr: 612
issue: 611
closed_at:
closed_reason:
bump: patch
release_version:
---

# ITEM-250: An empty song hides the whole Verses section instead of naming itself

## Summary

Spec 210 chose to hide the entire Verses field when the picked song has no live verses. The
sentence `This song has no verses` is rendered inside that hidden panel, so the operator sees
the field disappear without an explanation until Save refuses the entry. The section should
be shown, collapsed to the summary row that names the song.

## Notes

- Reverses spec 210's answer to "what should a song with no verses show?"; the superseded note
  in `reading/R30` is updated rather than deleted.
- The label and the bordered panel stay; the helper/All–Clear row, tiles and readout do not.
- The summary's bottom separator is dropped in the empty state because nothing follows it.
- First paint is server-rendered: `SongEntryForm.song_has_no_verses` already carries the fact.
- No new animation phase; the empty ↔ populated swap changes in the same frame as the pick.

## Acceptance sketch

- Add and Edit song entry modals show `Verses` + a small panel whose only line is
  `This song has no verses`; no checkboxes, helper text or All/Clear buttons.
- No song picked still hides the whole section at 0 px.
- Songs with verses keep the 200 ms reveal, five-across tiles, first verse ticked, drag range
  and muted one-verse state unchanged.
- Both save refusals keep their exact wording.

## Links

- Spec: [235](../specs/235-empty-song-verse-summary/spec.md)
- Related items: ITEM-217 (spec 189's empty-song stage invitation, a different surface)
