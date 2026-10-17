---
id: ITEM-104
status: done
title: 'Restrict the search page to the listed content fields'
type: fix
priority: P1
effort: M
created: 2026-10-17
updated: 2026-10-17
spec: [104](../../specs/104-search-field-scope/spec.md)
branch: fix/104-search-field-scope
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/355
archived_at:
archive_reason:
bump: patch
release_version: 1.13.5
---

# ITEM-104: Restrict the search page to the listed content fields

## Summary

The public search page matches container names, references, numbers, dates, and labels — `Kidung
Jemaat` returns 814 song rows, `KJ 152` returns the hymn, `Matius 5:13` returns the passage — none
of which the owner listed as searchable. Entry rows are not indexed at all: a service built only
from `ServiceEntry` rows never appears under its own name or its entries' titles and bodies.

## Notes

- Owner request, 2026-10-17: "make the search page only match the following fields: verse texts
  and titles / song titles / song lyrics / tataibadah titles / entry titles / text entries text".
- Owner corrections: songbook references stop resolving; Bible references stop resolving; the
  home hint `Try Yoh 3:16 or HAL 411` is removed entirely.
- The Go To is frozen ("do not touch anything on goto. only search page"), and the owner asked
  for the two search functions to be separated to avoid future conflicts. The page gets its own
  `search_page()`; the legacy `search()` stays as the Go To's fallback, byte-identical.
- Spec 105 replaces this spec's ranking ladder with token coverage and order once accepted.

## Acceptance sketch

- `Kidung Jemaat` lists no songbook row and no song for membership alone; `152`, `KJ 152`,
  `Kidung Jemaat 152`, and `HAL 411` list no song.
- `Matius 5:13`, `Matius 5`, and `Yoh 3:16` list no passage; `Matius` lists no book row, while
  verses whose text or title contain it still match.
- Verse text/title, song title/lyrics, service name, row title, and text-entry body still match;
  an entry-only service appears under its name and each entry links `#ti-e<pk>`.
- Dates, section labels, end-of-section notes, and song-entry bodies list nothing.
- The saved copy matches the same fields after a refresh.
- The Go To behaves exactly as today.

## Links

- Spec: [104](../../specs/104-search-field-scope/spec.md)
- Plan: [104](../../specs/104-search-field-scope/plan.md)
- Related items: [ITEM-064](./ITEM-064-public-site-revamp.md) (spec 004 — the search shell),
  [ITEM-007](./ITEM-007-service-entries.md) (spec 006 — entries), ITEM-105 (the query grammar)
