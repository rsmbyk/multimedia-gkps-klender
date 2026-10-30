---
id: ITEM-117
status: done
title: 'Display PDF pages in Preview and projector'
type: feat
priority: P1
effort: L
created: 2026-10-19
updated: 2026-10-19
spec: specs/117-pdf-media-display/spec.md
branch: feat/117-pdf-media-display
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/365
issue:
closed_at: 2026-10-19
closed_reason: merged into develop (PR #365)
bump: minor
release_version: 1.18.0
---

# ITEM-117: Display PDF pages in Preview and projector

## Summary

Let operators inspect and project a locally available PDF one page at a time at its Tata Ibadah entry. A missing or unreadable file must leave no stale projected content.

## Notes

The owner compared page-by-page and scrollable previews and chose page-by-page on 2026-10-19.

## Acceptance sketch

- Preview shows one complete page with previous/next controls and a page count.
- Projector navigation moves through PDF pages before crossing to adjacent service entries.
- The original SHA-256 reference remains immutable; other media behavior is unchanged.

## Links

- Spec: [117](../../specs/117-pdf-media-display/spec.md)
- Related items: [ITEM-103](./ITEM-103-local-media-library.md), [ITEM-114](./ITEM-114-image-media-display.md)
