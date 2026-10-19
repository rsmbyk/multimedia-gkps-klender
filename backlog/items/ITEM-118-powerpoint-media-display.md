---
id: ITEM-118
status: speccing
title: 'Display PowerPoint slides in Preview and projector'
type: feat
priority: P1
effort: L
created: 2026-10-19
updated: 2026-10-19
spec: specs/118-powerpoint-media-display/spec.md
branch: feat/118-powerpoint-media-display
pr:
archived_at:
archive_reason:
bump: minor
release_version:
---

# ITEM-118: Display PowerPoint slides in Preview and projector

## Summary

Let operators inspect and project locally available PPT/PPTX entries slide by slide. Keep the original library file and use a private, disposable display conversion so it remains one immutable service reference.

## Notes

The owner approved the static-slide visual preview on 2026-10-19. Conversion and UI behavior remain Draft until the owner explicitly accepts Spec 118.

## Acceptance sketch

- Preview displays a whole slide with previous/next and a count.
- Projector navigation moves through slides before adjacent service entries.
- Missing or failed conversion leaves no stale projector content.
- Derived display data is not shared or counted as another Media Library file.

## Links

- Spec: [118](../../specs/118-powerpoint-media-display/spec.md)
- Related items: [ITEM-117](./ITEM-117-pdf-media-display.md), [ITEM-103](./ITEM-103-local-media-library.md)
