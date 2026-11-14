---
id: ITEM-114
status: done
title: 'Display Image entries in Preview and projector'
type: feat
priority: P1
effort: M
created: 2026-10-18
updated: 2026-10-18
spec: specs/114-image-media-display/spec.md
branch: feat/114-image-media-display
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/362
archived_at:
archive_reason:
bump: minor
release_version: 1.16.0
---

# ITEM-114: Display Image entries in Preview and projector

## Summary

Show a locally verified Image service entry in the existing Preview dialog and directly on the Tata Ibadah projector page. Fit the complete image within each surface and keep missing-file feedback quiet for the congregation.

## Notes

The owner accepted the interactive visual preview and Draft spec on 2026-10-18. The implementation and exact-head CI are complete; the owner authorized the merge.

## Acceptance sketch

- Image entries gain Preview, and one fitted projector screen appears at the entry's sequence position.
- Missing/unavailable/undecodable images show a clear operator Preview state and a muted projector icon without leaving prior content visible.
- Escape/backdrop dismissal, morph animation, local SHA-256 identity, and existing navigation/display-off behavior are preserved.
- Audio, video, PDF, and slides stay outside this slice.

## Links

- Spec: [114](../../specs/114-image-media-display/spec.md)
- Related items: [ITEM-103](./ITEM-103-local-media-library.md), [ITEM-112](./ITEM-112-temporary-media-handoff.md)
