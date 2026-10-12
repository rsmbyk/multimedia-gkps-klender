---
id: ITEM-062
status: in-review
title: 'Distinct song label typography'
type: fix
priority: P2
effort: S
created: 2026-10-12
updated: 2026-10-12
spec: '060'
branch: fix/059-song-label-typography
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/313
archived_at:
archive_reason:
bump: patch
release_version: 1.5.1
---

# ITEM-062: Distinct song label typography

## Summary

Distinguish the hymn book and song number, song title, and second-line lyric verse selection in the service-order sidebar shown in the owner's screenshot.

## Notes

Hierarchy: 12px semibold hymn reference, 14px regular title, and 12px verse selection on the second line. Dark mode uses primary text color for the smaller verse label to retain readable contrast.

## Acceptance sketch

- Three separately styled text regions with preserved two-line grouping and 8px between reference and title.
- Readable selected rows in both themes, wrapping titles, and reference-free songs.
- Existing interactions and other service item styles preserved.

## Links

- Spec: [060](../../specs/060-song-label-typography/spec.md)
