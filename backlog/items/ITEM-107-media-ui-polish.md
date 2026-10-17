---
id: ITEM-107
status: in_progress
title: 'Clarify Media Library controls and align media entry labels'
type: fix
priority: P2
effort: S
created: 2026-10-17
updated: 2026-10-17
spec: 107
branch: fix/107-media-ui-polish
pr:
archived_at:
archive_reason:
bump: patch
release_version: 1.14.4
---

# ITEM-107: Clarify Media Library controls and align media entry labels

## Summary

Give the Media Library sort control an order icon, represent the whole library in the main rail, center Tata Ibadah media entry labels beside their file icon, and clarify the supported upload formats and size limit.

## Notes

The owner accepted the preview and Draft on 2026-10-17. The service entry title inherited a 30 px top margin from the general Tata Ibadah heading rule, despite a narrower media-specific override. This branch corrects that cascade and awaits the parallel offline-entry integration before its final release check.

## Acceptance sketch

- The sort icon remains visible when the sort option changes.
- The Media Library rail pictogram represents files beyond images.
- Titled and untitled media entries align their text block vertically with the file icon.
- The upload hint uses `PPT/PPTX` and places the emphasized `Maximum 200 MB` limit on its own line.

## Links

- Spec: [107](../../specs/107-media-ui-polish/spec.md)
- Related items: [ITEM-103](./ITEM-103-local-media-library.md), [ITEM-104](./ITEM-104-media-picker-layout.md), [ITEM-105](./ITEM-105-media-navigation-feedback.md)
