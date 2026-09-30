---
id: ITEM-001
status: speccing
title: Public song reading + design foundation
type: feat
priority: P0
effort: M
created: 2026-09-30
updated: 2026-09-30
spec: ../specs/001-public-songs-reading/spec.md
branch: feat/001-public-songs-reading
pr:
archived_at:
archive_reason:
bump: minor
release_version:
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
- `bump: minor` is intent only; `VERSION` is `0.4.6` on `main` while tags
  `v0.5.0`–`v0.5.2` exist on the `develop` line. Resolve before versioning.
- E2E tool is still unchosen (deferred in spec).

## Acceptance sketch

- Home shows search + books; book page lists songs; song page reads lyrics.
- Search works server-side; unknown ids 404.
- Legacy `/songs/books*` paths redirect to `/manage/...`.
- Reading pages render content without JS and without Fomantic.

## Links

- Spec: [`specs/001-public-songs-reading/spec.md`](../specs/001-public-songs-reading/spec.md)
- Related items:
