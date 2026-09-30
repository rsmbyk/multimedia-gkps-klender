---
id: ITEM-001
status: in-review
title: Public song reading + design foundation
type: feat
priority: P0
effort: M
created: 2026-09-30
updated: 2026-09-30
spec: ../specs/001-public-songs-reading/spec.md
branch: feat/001-public-songs-reading
pr: 257
archived_at:
archive_reason:
bump: minor
release_version: 0.6.0
---

# ITEM-001: Public song reading + design foundation

## Summary

Make the website worth opening outside streaming. First slice: a shared design
foundation and a public, server-rendered song-reading experience — browse
songbooks, read lyrics, search — with the editor relocated under `/manage/`.

## Notes

- Spec pack: [`specs/001-public-songs-reading/`](../specs/001-public-songs-reading/spec.md).
- Part of the owner's vision: the website becomes the product (see
  [`docs/PRODUCT.md`](../../docs/PRODUCT.md) → Vision).
- `bump: minor`: `VERSION` is `0.5.2` (highest shared tag), so this slice lands
  as `0.6.0` in the release PR.
- E2E: Playwright (Python) via Django `LiveServerTestCase`.
- Design language defined from scratch (no Semantic/Fomantic on public pages); palette drawn from
  the GKPS logo's green and blue.

## Acceptance sketch

- Home shows search + books; book page lists songs; song page reads lyrics.
- Search works server-side; unknown ids 404.
- Legacy `/songs/books*` paths redirect to `/manage/...`.
- Reading pages render content without JS and without Fomantic.

## Links

- Spec: [`specs/001-public-songs-reading/spec.md`](../specs/001-public-songs-reading/spec.md)
- Related items:
