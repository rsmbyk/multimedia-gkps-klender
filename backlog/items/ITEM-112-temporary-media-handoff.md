---
id: ITEM-112
status: in_progress
title: 'Temporarily share and acquire Media Library files'
type: feat
priority: P1
effort: L
created: 2026-10-17
updated: 2026-10-18
spec: specs/112-temporary-media-handoff/spec.md
branch: feat/112-temporary-media-handoff
pr:
archived_at:
archive_reason:
bump: minor
release_version: 1.15.0
---

# ITEM-112: Temporarily share and acquire Media Library files

## Summary

Let operators share individual local media files online for seven days, then acquire missing online files for future services on another computer. Configure the private R2 bucket and server credentials in this same slice. Show progress/history from the local companion in Media Library, Tata Ibadah, and a temporary sidebar button.

## Notes

The owner accepted the revised Draft on 2026-10-18 after adding protected local copies for today/future services and indefinite bounded retry for automatic downloads.

## Acceptance sketch

- Individual SHA-256 identities can be shared online once, expire after seven days, and never appear available before verified upload completion.
- Today/future services acquire missing online files automatically; past and undated services offer manual download.
- Companion transfers and history survive browser closure and are visible through the agreed UI states.
- Files needed by today/future services resist manual and automatic deletion; failed automatic downloads retry with bounded backoff while eligible and online.

## Links

- Spec: [112](../../specs/112-temporary-media-handoff/spec.md)
- Related items: [ITEM-103](./ITEM-103-local-media-library.md)
