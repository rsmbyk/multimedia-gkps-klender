---
id: ITEM-103
status: in_review
title: 'Local Media Library and service media entries'
type: feat
priority: P1
effort: L
created: 2026-10-17
updated: 2026-10-17
spec: specs/103-local-media-library/spec.md
branch: feat/103-local-media-library
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/353
archived_at:
archive_reason:
bump: minor
release_version: 1.14.0
---

# ITEM-103: Local Media Library and service media entries

## Summary

Keep media bytes in a shared local computer folder rather than browser storage or Vercel. Add a Media Library view and immutable file references on Tata Ibadah media entries. Operators can add or reuse an image, audio, video, PDF, PPT, or PPTX file and see when its bytes are missing on their computer. File-content Preview and projector rendering remain blank in this first slice.

## Notes

- The owner approved the linked Library and entry-form visual previews on 2026-10-17.
- The owner accepted Spec 103 on 2026-10-17.
- A separate local companion is needed so Chrome and the OBS dock can use the same folder.
- Files are limited to 200 MB; content inspection determines type, and SHA-256 determines identity.
- Integration order assumes spec/ITEM 102 merges into `develop` before this item. Keep ID 103, then rebase before the implementation PR.

## Acceptance sketch

- A new media entry imports one verified local file or reuses a library file; editing can change only the title.
- The library lists local files, references, filters, date/size sort, connection status, removal, and per-computer unused cleanup.
- Missing local bytes never erase a service entry; a different file requires a new entry.
- Media Preview and projector content remain blank without leaving the previous projected item visible.

## Links

- Spec: [103](../../specs/103-local-media-library/spec.md)
- Visual previews: [Library](../../specs/103-local-media-library/preview-library.html), [entry form](../../specs/103-local-media-library/preview-entry.html)
- Related items: [ITEM-002](./ITEM-002-projection-controls.md)
