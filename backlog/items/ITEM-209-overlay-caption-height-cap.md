---
id: ITEM-209
status: in-progress
title: 'The song caption type is bound to the stage height'
type: fix
priority: P1
effort: S
created: 2026-11-19
updated: 2026-11-19
spec: 202
branch: fix/202-overlay-caption-height-cap
pr:
issue:
bump: patch
release_version:
---

# ITEM-209: The song caption type is bound to the stage height

## Summary

The caption's font size is currently driven by the source's width, so it does not follow the height
the words have to live in. Bound it to the stage height instead: 5 % at rest, 2 % as the floor the
two-line fit cannot pass. At the floor the block may exceed two rows — the lyric was too long.

## Notes

- The owner's clarification: "the font size should not be bigger than 5 % of screen height and not
  smaller than 2 % while fitting into 2 lines."
- OBS caption only. The projector's `fit()` and the passage/liturgy plates keep their own scales.
- No truncation or ellipsis: the fit only changes `font-size`.

## Acceptance sketch

- At 1920×1080 the rest reads 54 px; at 1280×720 it reads 36 px.
- A wrapping lyric shrinks in 6 % steps, never below 21.6 px at 1080p.
- A lyric that cannot fit two rows at the floor stops there and lands as it lands.

## Links

- Spec: [202](../../specs/202-overlay-caption-height-cap/spec.md)
- Related items: ITEM-204 (the two-line fit this slice bounds)
