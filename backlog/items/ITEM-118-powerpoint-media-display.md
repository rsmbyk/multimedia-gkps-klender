---
id: ITEM-118
status: in_review
title: 'Display PowerPoint slides in Preview and projector'
type: feat
priority: P1
effort: L
created: 2026-10-19
updated: 2026-10-20
spec: specs/118-powerpoint-media-display/spec.md
branch: feat/118-powerpoint-media-display
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/366
archived_at:
archive_reason:
bump: minor
release_version: 1.19.0
---

# ITEM-118: Display PowerPoint slides in Preview and projector

## Summary

Let operators inspect and project locally available PPT/PPTX entries slide by slide. Keep the original library file and use a private, disposable display conversion so it remains one immutable service reference.

## Notes

The owner accepted Spec 118. Implementation is in review in PR #366, stacked on the PDF display branch until its PR merges into develop.

## Acceptance sketch

- Preview displays a whole slide with previous/next and a count.
- Projector navigation moves through slides before adjacent service entries.
- Missing or failed conversion leaves no stale projector content.
- Derived display data is not shared or counted as another Media Library file.

## Links

- Spec: [118](../../specs/118-powerpoint-media-display/spec.md)
- Related items: [ITEM-117](./ITEM-117-pdf-media-display.md), [ITEM-103](./ITEM-103-local-media-library.md)
