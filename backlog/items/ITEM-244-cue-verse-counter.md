---
id: ITEM-244
status: speccing
title: 'A passage cue does not say where it stands in the passage'
type: feat
priority: P2
effort: S
created: 2026-11-23
updated: 2026-11-23
spec: 229-cue-verse-counter
branch: feat/229-cue-verse-counter
pr:
issue:
closed_at:
closed_reason:
bump: patch
release_version:
---

# ITEM-244: A passage cue does not say where it stands in the passage

## Summary

The projector's corner cue names the passage and its edition but gives no read-out of the verse on
screen. A service passage's reference never changes as the operator steps; a chapter Go To follows
the verse but says nothing about the chapter's length. Add a `current/end` counter after the
reference so both cases read `3/5` or `1/3`.

## Notes

- Owner chose the slash form on 2026-11-23: `Yoh 3:16-18 · 16/18 · TB` and `Yoh 3:16 · 16/132 · TB`.
- Service passages take the entry's `verse_end` (or `verse_start` when absent); a Go To takes the
  last verse of the chapter currently loaded.
- Only scripture cues gain it; songs, texts, breaks and media stay as they are.

## Acceptance sketch

- A service passage's counter follows the verse and holds the passage's end number.
- A chapter Go To's counter follows the verse and the end number changes with the chapter.
- A dock- or reading-started Go To reads the same as one started on the projector.
- The cue's 24px band, centre alignment, centre dots and translation flip are unchanged.

## Links

- Spec: [229](../specs/229-cue-verse-counter/spec.md)
- Related items: ITEM-242 (the Go To's cue with no service), ITEM-243 (Back's cue reset)
