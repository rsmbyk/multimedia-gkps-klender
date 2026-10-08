---
id: ITEM-015
status: in_review
title: 'Remove songbook language and merge duplicate songbooks'
type: feat
priority: P1
effort: L
created: 2026-10-07
updated: 2026-10-07
spec: specs/013-songbook-language-removal/spec.md
branch: feat/026-live-projection-editing
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/275
archived_at:
archive_reason:
bump: major
release_version: 1.0.0
---

# ITEM-015: Remove songbook language and merge duplicate songbooks

## Summary

Remove language from the songbook model and API, consolidate existing songbooks with the same exact name, and preserve every song, lyric verse, and song-based reference. When a merge creates a song-number collision, assign the moved song the next available integer while preserving its sub-number.

## Notes

- Owner decision: remove `Book.lang` and the now-unused `songs.Language` model/table, not only the form control.
- Owner decision: keep all songs; merge into the lowest-ID active songbook (or lowest ID if all duplicates are soft-deleted); keep the keeper's metadata.
- Owner decision: for number/sub-number collisions, allocate max+1 and preserve sub-number.
- This changes the book API shape and is a major bump. Rehearse the data migration on a backup before production.

## Acceptance sketch

- Songbook language is absent from models, forms, admin, search/order consumers, and songbook API payloads.
- Exact-name duplicates consolidate without losing songs, verses, IDs, or song-based references.
- Colliding moved songs receive deterministic available numbers; global book-name uniqueness prevents duplicates returning.

## Links

- Spec: [013 — Remove songbook language and merge duplicate songbooks](../../specs/013-songbook-language-removal/spec.md)
- Related items: ITEM-006 (sidebar editors), ITEM-014 (songbook form fields)
