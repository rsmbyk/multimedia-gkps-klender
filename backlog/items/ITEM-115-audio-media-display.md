---
id: ITEM-115
status: in_progress
title: 'Play Audio entries in Preview and projector'
type: feat
priority: P1
effort: M
created: 2026-10-19
updated: 2026-10-19
spec: specs/115-audio-media-display/spec.md
branch: feat/115-audio-media-display
pr:
archived_at:
archive_reason:
bump: minor
release_version: 1.17.0
---

# ITEM-115: Play Audio entries in Preview and projector

## Summary

Let an operator hear a locally available Audio service entry in Preview and play it directly from its position in the Tata Ibadah projector sequence. The audio player must leave existing navigation shortcuts usable and show a quiet missing-file state.

## Notes

The owner accepted the interactive [audio preview](../../specs/115-audio-media-display/preview.html) on 2026-10-19. Its generated demo clip is prototype data only; the delivered player uses the referenced local Media Library file.

## Acceptance sketch

- Audio entries gain a playable Preview modal and one manual-play projector screen at their current service position.
- Space plays/pauses an available audio entry in Preview and on the projector; the projector shortcuts sheet documents it.
- Projector navigation pauses audio; returning to the entry resets playback to the start. Existing non-audio Space behavior remains.
- While playing, projector controls fade to an unobtrusive idle state after inactivity and reappear on operator activity; paused controls remain visible.
- Missing, disconnected, or undecodable audio never plays a substitute file.

## Links

- Spec: [115](../../specs/115-audio-media-display/spec.md)
- Related items: [ITEM-103](./ITEM-103-local-media-library.md), [ITEM-112](./ITEM-112-temporary-media-handoff.md), [ITEM-114](./ITEM-114-image-media-display.md)
