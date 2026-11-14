---
id: ITEM-041
status: done
title: 'Show the short full title for a hymn song in the service sidebar'
type: chore
priority: P2
effort: S
created: 2026-10-08
updated: 2026-10-08
spec: specs/039-hymn-song-sidebar-title/spec.md
branch: chore/039-hymn-song-sidebar-title
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/291
archived_at:
archive_reason:
bump: patch
release_version: 1.3.7
---

# ITEM-041: Show the short full title for a hymn song in the service sidebar

## Summary

In the Tata Ibadah sidebar (the service's contents list), a song entry from a hymn book should read
as its **short full title** — the short hymn-book reference plus the song's title, e.g.
`KJ 435 Marolopolop Tondingki` — instead of the long book name it shows today.

## Notes

- **What the sidebar shows.** `_tatib_stage()` in `multimedia/web/reading/views.py` labels an entry
  with `row.resolve()[0]`, which for a song is `ServiceEntry.citation()` — `f'{book.name}
  {number}{sub_number}'`, e.g. "Kidung Jemaat 435" (`multimedia/tatib/models.py`).
- **What we want.** `Song.book_number` already yields the short reference (`f'{book.short_name}
  {number}{sub_number.upper()}'` → "KJ 435") and `Song.title` yields the title; the sidebar label
  should combine them.
- **Hymn books only.** The change is for songs whose `Book.is_hymn_book` is true; other songbooks
  keep their current label.
- **Scope.** This is the sidebar label. Whether the pane's entry heading and other places adopt the
  same wording is an open question.
- The sidebar's filter text (`txt`) should include the new wording so filtering still matches.

## Open questions

- Sidebar only, or the pane heading too?
- A hymn song with no title (`is_untitled`): fall back to just the short reference?
- Should the short title also feed the TOC's `aria-label`/grip label (it uses `item.label` already)?

## Acceptance sketch

- The Tata Ibadah sidebar shows `KJ 435 Marolopolop Tondingki` for a hymn song (short name, number,
  title).
- A non-hymn song keeps its current label.
- Filtering the sidebar still matches on the shown words.

## Links

- Spec: [039 — Show the short full title for a hymn song in the service sidebar](../../specs/039-hymn-song-sidebar-title/spec.md)
- Related items: ITEM-007 / spec 006 (service entries), ITEM-008 / spec 007 (the old rows)
