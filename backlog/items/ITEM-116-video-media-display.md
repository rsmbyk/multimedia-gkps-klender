---
id: ITEM-116
status: speccing
title: 'Display Video entries in Preview and projector'
type: feat
priority: P1
effort: M
created: 2026-10-19
updated: 2026-10-19
spec:
branch: feat/115-116-audio-video-display
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/364
archived_at:
archive_reason:
bump: minor
release_version:
---

# ITEM-116: Display Video entries in Preview and projector

## Summary

Let operators inspect a locally available Video entry and show it directly at its position in the Tata Ibadah projector sequence. Projection should start paused and stop when the operator leaves the entry.

## Notes

The [interactive Video preview](../../specs/116-video-media-display/preview.html) is proposed for owner review. It uses a small demo recording and the existing Tata Ibadah shell; the eventual product would use the referenced local Media Library file.

The owner requested this slice on the same branch as Audio, so branch `feat/115-116-audio-video-display` carries both concerns in separate numbered specs.

## Acceptance sketch

- Video entries can be previewed and projected without changing their stored file reference.
- The video fits within the existing modal and projector safe area, including a portrait recording.
- Playback starts manually, can be paused and sought, and stops on navigation or display-off.
- Missing, disconnected, or undecodable video has an operator unavailable state and a quiet projector icon.

## Links

- Proposed preview: [116](../../specs/116-video-media-display/preview.html)
- Related items: [ITEM-115](./ITEM-115-audio-media-display.md), [ITEM-103](./ITEM-103-local-media-library.md)
