---
id: ITEM-053
status: done
title: 'Search songs by songbook reference and title'
type: fix
priority: P2
effort: S
created: 2026-10-09
updated: 2026-10-10
spec: specs/051-song-picker-reference-search/spec.md
branch: fix/051-song-picker-reference-search
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/302
archived_at:
archive_reason:
bump: patch
release_version: 1.3.17
---

# ITEM-053: Search songs by songbook reference and title

## Summary

The New song picker matches free-text queries against song title, number, and hymn songbook names. Extend book filtering to short/full names and substrings; parse combined references as a hymn-book-name substring plus a number prefix, optionally followed by one-letter sub-number and title text, in both add and edit song pickers.

## Notes

- The picker endpoint is `multimedia/web/reading/views.py::entry_song_options`.
- The public cross-corpus search already resolves both abbreviated and full songbook references, but the entry picker uses a separate query path.
- Keep existing title, number, and abbreviation searches; this item extends matching rather than replacing free-text search.
- Owner accepted the hymn-books-only name filter and the unchanged 200-song limit. For references, the book phrase is substring-matched (`kj` can match KJ and PKJ); the number is prefix-matched (`kj 12` can find KJ/PKJ 12 and 123), with an optional letter matching the exact sub-number. Accepted on 2026-10-10.

## Acceptance sketch

- `kj`, `kidu`, `maat`, and `kidung jemaat` list the songs of every matching hymn book, alongside any song whose title matches; non-hymn book names remain title-only.
- `kj 12` finds KJ/PKJ song numbers 12 and 123, and any KJ 12A/12B variants; it does not find number 130.
- `kj 12a` finds KJ 12A but not KJ 12B; `kidung jemaat 235` matches the full-name reference, with optional title suffixes such as `KJ 123 <song title>`.
- Behavior is the same in add and edit forms; existing 200-result limit, grouping, order, labels, and verse loading stay unchanged.

## Links

- Spec: [051 — Search songs by songbook reference and title](../../specs/051-song-picker-reference-search/spec.md)
- Related item: ITEM-052 / spec 050 (song picker short-name search)
