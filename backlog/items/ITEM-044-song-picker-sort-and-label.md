---
id: ITEM-044
status: in_progress
title: 'Sort and label the add-song picker like the hymn books'
type: chore
priority: P2
effort: S
created: 2026-10-08
updated: 2026-10-08
spec: specs/042-song-picker-sort-and-label/spec.md
branch: chore/042-song-picker-sort-and-label
pr:
archived_at:
archive_reason:
bump: patch
release_version: 1.3.10
---

# ITEM-044: Sort and label the add-song picker like the hymn books

## Summary

In the add / edit song modal's dropdown: order a hymn book's songs by their number and a non-hymn
book's songs alphabetically; put the hymn songbooks first, ordered by songbook id, then the non-hymn
songbooks by name; and label a hymn option as its short reference plus title (e.g.
`HAL 123 Some Title`) while a non-hymn option shows just the title.

## Notes

- **Today.** `entry_song_options()` in `multimedia/web/reading/views.py` orders songs by
  `book__name, number, title`, builds groups in encounter order (so groups follow the book name), and
  `_entry_song_options.html` renders each option as `{{ number }} — {{ title }}` for every kind of
  book.
- **The songbooks.** `Haleluya` (`HAL`), `Kidung Jemaat` (`KJ`), `Pelengkap Kidung Jemaat` (`PKJ`),
  `Nyanyikanlah Kidung Baru` (`NKB`) — see `raw/songs/books.json`; `Book.is_hymn_book` marks the
  hymnals and `Book.short_name` gives the reference. `Song.book_number` is already
  `f'{short_name} {number}{sub_number.upper()}'`.
- **What to change.**
  - Order: hymn books' songs by number (sub-number as tiebreak); non-hymn books' songs
    alphabetically by title.
  - Group order (owner's decision): hymn songbooks first, ordered by songbook **id**; then non-hymn
    songbooks ordered by **name**.
  - Label: a hymn option shows `HAL 123 Some Title`; a non-hymn option shows only its title.
- **Selected label.** `entries.js` uses `data-song-title` for the closed control; keep that plain-title
  behavior while open hymn options show the short reference plus title.
- The picker's filter (`q`) still matches title and number.

## Decisions

- The closed picker keeps its current title-only label; the full reference is shown in open hymn options.
- Numberless hymns appear after numbered ones, ordered by title, and use the short book name plus
  title without a `None` placeholder.

## Acceptance sketch

- A hymn book's group lists its songs by number; a non-hymn book's group lists them A–Z.
- The hymn songbooks appear first, ordered by songbook id; the non-hymn songbooks follow by name.
- A hymn option reads `HAL 123 Some Title`; a non-hymn option reads just the title.
- Unnumbered hymns follow numbered ones in title order and show the short reference plus title.
- The closed selected label remains the title alone.

## Links

- Spec: [042 — Sort and label the add-song picker like the hymn books](../../specs/042-song-picker-sort-and-label/spec.md)
- Related items: ITEM-043 (the book picker's names), ITEM-041 (hymn short title in the sidebar)
