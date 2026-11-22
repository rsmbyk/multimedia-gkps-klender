---
id: ITEM-227
status: done
title: 'Revamp the song entry pickers'
type: feat
priority: P1
effort: M
created: 2026-11-21
updated: 2026-11-21
spec: specs/210-song-verse-picker/spec.md
branch: feat/210-song-verse-picker
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/561
issue:
closed_at: 2026-11-21
closed_reason: merged into develop (PR #561)
bump: patch
release_version: 1.36.6
---

# ITEM-227: Revamp the song entry pickers

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
- Review round on the shipped build: the section reads as the preview's bordered panel with a rule
  under the summary line and another under the helper/All-Clear row; its summary is display text, not
  a control; a tile draws its focus ring for keyboard focus only; the tiles are never clipped once the
  reveal settles; the Verses label hides with its section; a server-rendered checklist comes back as
  the same tile grid; the Edit form no longer takes focus into the Song field; and the field selects
  its text on focus so typing starts a new query.
- Numbers now read `Bait` with collapsed ranges (`Bait 1–2, 4–5`) in the summary and in every printed
  verse reference — the stage and contents `Bait` lines, generate rows and option previews — through one
  shared formatter, which also collapses a pair.
- Three E2E failures and eight unit-lane failures reproduce on unmodified `develop`; they are recorded
  on their own cards and are not attributed to this slice.

## Acceptance sketch

- Opening "+ Song" puts focus in the search field; typing over the stored label replaces it, and the
  grouped result list may run past the dialog's bottom edge without resizing it.
- Picking a song reveals an inline, bordered Verses section whose summary states `Bait` ranges.
- A click ticks or unticks one tile; a held drag previews a range and writes verse IDs only on release.
- No song or a no-verses song collapses the section and its label; a one-verse song leaves one muted tile.
- An Edit form opens without focus in the search field and keeps its saved verses.

## Links

- Spec: [210 — Revamp the song entry pickers](../../specs/210-song-verse-picker/spec.md)
- Preview: [static preview](../../specs/210-song-verse-picker/preview/index.html)
