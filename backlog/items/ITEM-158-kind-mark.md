---
id: ITEM-158
status: ready
title: 'A passage or a song carries its own kind mark'
type: feat
priority: P2
effort: S
created: 2026-10-28
updated: 2026-10-28
spec: specs/144-passage-song-icons/spec.md
branch: feat/144-passage-song-icons
pr:
issue:
closed_at:
closed_reason:
bump: patch
release_version:
---

# ITEM-158: A passage or a song carries its own kind mark

## Summary

On the Tata Ibadah stage only a media entry is marked: a 42px tinted chip at the row's left edge
carrying the file family's glyph. A passage and a song are plain text — their title, and for a song
its "Bait 1-3" line — so the stage's kinds cannot be told apart without reading them.

Give passage and song rows a mark of their own, in the media chip's visual language but visibly
different from it, so a media file is never mistaken for a passage or a song.

## Notes

- Owner request, 2026-10-28: "add some kind of icons for passage and songs just like the media
  entries, but make it kind of different so that you can distinguish between media and
  passage/songs entries."
- The stage's passage and song rows are compact 56px rows; the media row is 80px because its 42px
  chip sits inside the flow. A mark that fits the compact row is the constraint, not a preference.
- Scope is the stage. The sidebar's service list and the OBS dock's entry list keep their own
  anatomy.

## Acceptance sketch

- A passage row and a song row each paint a kind glyph at their left edge.
- The glyph is distinguishable from the media chip at a glance, and at the 400px reading pane a
  1440px window produces.
- Neither row's height nor its title's first-line position changes by more than the mark's own
  indent, and nothing else on the stage moves.
- The mark is decorative for assistive technology: the row already carries its kind in words.

## Links

- Spec:
- Related items: ITEM-151 (stage link affordance), ITEM-152 (entry surface), ITEM-154 (add bar)
