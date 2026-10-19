---
id: ITEM-116
status: speccing
title: 'Display Video entries in Preview and projector'
type: feat
priority: P1
effort: M
created: 2026-10-19
updated: 2026-10-19
spec: specs/116-video-media-display/spec.md
branch: feat/115-116-audio-video-display
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/364
archived_at:
archive_reason:
bump: minor
release_version: 1.17.0
---

# ITEM-116: Display Video entries in Preview and projector

## Summary

Let operators inspect a locally available Video entry and show it directly at its position in the Tata Ibadah projector sequence. Projection should start paused and stop when the operator leaves the entry.

## Notes

The owner approved the [interactive Video preview](../../specs/116-video-media-display/preview.html) on 2026-10-19. Its 12-second generated demo recording and sample Tata Ibadah entries are preview data; the product uses the entry's referenced local Media Library file.

The owner requested this slice on the same branch as Audio, so branch `feat/115-116-audio-video-display` carries both concerns in separate numbered specs.

## Acceptance sketch

- Video entries can be previewed and projected without changing their stored file reference.
- Playback starts manually; projector playback enters fullscreen when allowed, and pausing returns to the normal projector view.
- Only the fullscreen projector shows the progress bar and timer; they hide after two seconds of inactivity. Left/right navigation is suppressed while fullscreen video is playing.
- Space toggles Audio/Video playback in context; the projector shortcut sheet explains this alongside Show/Hide Words for other entries.
- Landscape and portrait videos fit without cropping. Missing, disconnected, or undecodable video shows a readable operator state and a quiet Video-specific projector icon.

## Links

- Approved preview: [116](../../specs/116-video-media-display/preview.html)
- Draft spec: [116](../../specs/116-video-media-display/spec.md)
- Related items: [ITEM-115](./ITEM-115-audio-media-display.md), [ITEM-103](./ITEM-103-local-media-library.md)
