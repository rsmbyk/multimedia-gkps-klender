---
id: ITEM-061
status: in-progress
title: 'Distinct song label typography'
type: fix
priority: P2
effort: S
created: 2026-10-12
updated: 2026-10-12
spec: '059'
branch: fix/059-song-label-typography
pr:
archived_at:
archive_reason:
bump: patch
release_version: 1.3.24
---

# ITEM-061: Distinct song label typography

## Summary

Distinguish the hymn book and song number, song title, and second-line lyric verse selection in the service-order sidebar shown in the owner's screenshot.

## Notes

Hierarchy: 12px semibold hymn reference, 14px regular title, and 12px verse selection on the second line. Dark mode uses primary text color for the smaller verse label to retain readable contrast.

## Acceptance sketch

- Three separately styled text regions with preserved two-line grouping and 8px between reference and title.
- Readable selected rows in both themes, wrapping titles, and reference-free songs.
- Existing interactions and other service item styles preserved.

## Links

- Spec: [059](../../specs/059-song-label-typography/spec.md)
