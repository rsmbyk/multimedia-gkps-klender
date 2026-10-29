---
id: ITEM-164
status: in review
title: 'The rail names its sections with the marks the stage draws'
type: feat
priority: P2
effort: S
created: 2026-10-29
updated: 2026-10-29
spec: specs/151-rail-icons/spec.md
branch: feat/151-rail-icons
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/441
issue: https://github.com/rsmbyk/multimedia-gkps-klender/issues/439
closed_at:
closed_reason:
bump: patch
release_version:
---

# ITEM-164: The rail names its sections with the marks the stage draws

## Summary

The rail drew the Bible as a plain open book, the service order as a page with three rules — the shape
the product also gives a PDF — and Kidung with the same beamed pair the audio media family drew, so a
media file and a hymn were the same drawing told apart only by their box. A song row, meanwhile, wore a
single flagged note that neither the rail nor the Add Song tile drew.

Now one mark per section, drawn wherever the product repeats it: the Bible is an open book with a Latin
cross (rail, Alkitab panel empty state, passage row, Add Passage tile); the beamed pair is the note on
the rail, a song row and the Add Song tile; Tata Ibadah is a clipboard. Audio files move to a five-bar
waveform, so no rail mark is a media family mark any more.

## Notes

The three open books in the product collapse to one drawing; the two notes to one. Every box is the
shipped one — 44px rail button with a 24px glyph, 20px kind mark at row + 24, 42px chip with a 23px
glyph — and no stylesheet line changed.

The cross is a Latin cross (3.8-unit bar on a 4.6-unit stem): an equal-armed cross reads as a plus at
24px, which the first contact sheet showed.

## Acceptance sketch

- The rail's five marks are five shapes, and none of them is a media family's.
- The rail's Bible, a passage row and the Add Passage tile draw the same path; likewise the rail's
  note, a song row and the Add Song tile.
- An audio file draws the waveform in the stage chip, the Media Library, the service-media dialog and
  the upload preview, and the other four families and `missing` are untouched.
- Every measured box is unchanged, in both themes.
