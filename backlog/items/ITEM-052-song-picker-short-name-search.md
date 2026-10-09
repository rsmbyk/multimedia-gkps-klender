---
id: ITEM-052
status: done
title: 'Search and label songs by songbook abbreviation'
type: fix
priority: P2
effort: S
created: 2026-10-09
updated: 2026-10-09
spec: specs/050-song-picker-short-name-search/spec.md
branch: fix/050-song-picker-short-name-search
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/301
archived_at:
archive_reason:
bump: patch
release_version: 1.3.16
---

# ITEM-052: Search and label songs by songbook abbreviation

## Summary

The New song picker does not reliably find songs by their songbook's short name. Include the abbreviation in search so typing `KJ` can find songs even when their titles and numbers do not contain it. Keep the hymn-book reference visible in the selected label instead of showing only the title.

## Notes

- The picker endpoint is `multimedia/web/reading/views.py::entry_song_options`; it currently searches song title and number but not `book.short_name`.
- The shared `multimedia/songs/search.py::search_songs` helper already includes the book short name; the picker uses a separate endpoint.
- Result options already show a hymn's short name and number, but the selected and edit-prefilled picker labels show only `song.title`.
- Apply the behavior to both add and edit song-entry forms, which use the same picker endpoint.

## Acceptance sketch

- A case-insensitive abbreviation query finds songs through their songbook's `short_name`, even when title and number do not match.
- Selecting or editing a hymn-book song shows its short name, number/sub-number, and title; non-hymn labels remain title-only.
- Existing title/number search, grouping, order, result limit, and verse loading remain unchanged.

## Links

- Spec: [050 — Search and label songs by songbook short name](../../specs/050-song-picker-short-name-search/spec.md)
- Related items: ITEM-044 / spec 042 (song picker labels and ordering)
