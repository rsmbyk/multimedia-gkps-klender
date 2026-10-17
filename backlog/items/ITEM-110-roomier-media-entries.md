---
id: ITEM-110
status: in_review
title: 'Give Tata Ibadah media entries more breathing room'
type: fix
priority: P2
effort: S
created: 2026-10-17
updated: 2026-10-17
spec: specs/110-roomier-media-entries/spec.md
branch: fix/108-roomier-media-entries
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/359
archived_at:
archive_reason:
bump: patch
release_version: 1.14.5
---

# ITEM-110: Give Tata Ibadah media entries more breathing room

## Summary

Increase the height and vertical padding of media rows on the Tata Ibadah page so the file icon, title, and details do not feel cramped beside text and break entries.

## Notes

The owner accepted the [spacing preview](../../specs/110-roomier-media-entries/preview.html) on 2026-10-17. It uses an 80 px media row and 12 px between sample entries.

## Acceptance sketch

- Media rows have enough vertical space to separate the icon, title, and file details from neighboring rows.
- Text rows and break rows keep their current dimensions.
- Long filenames and narrow screens remain usable without horizontal overflow.

## Links

- Spec: [110](../../specs/110-roomier-media-entries/spec.md)
- Related items: [ITEM-103](./ITEM-103-local-media-library.md), [ITEM-109](./ITEM-109-media-ui-polish.md)
