---
id: ITEM-225
status: speccing
title: 'Revamp the song entry pickers'
type: feat
priority: P1
effort: M
created: 2026-11-21
updated: 2026-11-21
spec: specs/210-song-verse-picker/spec.md
branch: feat/210-song-verse-picker
pr:
issue:
bump: patch
release_version:
---

# ITEM-225: Revamp the song entry pickers

## Summary

The Add/Edit song modal asks for a second click before its song search can be typed in, and its
Verses field is a dropdown of small checkboxes that all start ticked. The picker should be usable
from the modal's first frame: live song search, then an inline verse grid where one click ticks a
verse and a held drag previews a range before committing it.

## Notes

- Owner decisions from the preview review: tiles five across; a plain click ticks one; a held drag
  previews and commits on release with no leftover mark; the summary line lives inside the Verses
  section with a separator; no-verses and no-song songs hide the section; a one-verse song mutes it.
- Editing an existing entry preserves its saved verses; only a fresh pick defaults to verse 1.
- The existing query grammar, hymn-first ordering, short-reference labels, 200-result cap and the
  verse-ID submission contract are unchanged.
- Three E2E failures and three unit-lane failures reproduce on unmodified `develop`; they are
  recorded on their own cards and are not attributed to this slice.

## Acceptance sketch

- Opening "+ Song" puts focus in the search field; typing narrows the grouped result list, which
  may run past the dialog's bottom edge without resizing it.
- Picking a song reveals an inline Verses section with the summary inside it and five tiles per row.
- A click ticks or unticks one tile; a held drag previews a range and writes verse IDs only on release.
- No song or a no-verses song collapses the section; a one-verse song leaves one muted tile.

## Links

- Spec: [210 — Revamp the song entry pickers](../../specs/210-song-verse-picker/spec.md)
- Preview: [static preview](../../specs/210-song-verse-picker/preview/index.html)
