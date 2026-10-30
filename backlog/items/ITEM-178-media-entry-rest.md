---
id: ITEM-178
status: in_progress
title: 'A media entry ends on a rest like every other entry'
type: feat
priority: P1
effort: S
created: 2026-10-29
updated: 2026-10-29
spec: specs/165-media-entry-rest/spec.md
branch: feat/165-media-entry-rest
pr:
issue:
closed_at:
closed_reason:
bump: patch
release_version: 1.23.3
---

# ITEM-178: A media entry ends on a rest like every other entry

## Summary

Every entry kind but one ends its projector screens on a built-in rest: a text row, a passage, each
song verse, and a section break (which is one). A media entry — image, audio, video, PDF or slide deck —
builds its one screen and stops, so `_projector_data` runs a picture straight into the next entry, and a
service that ends on a picture has no rest to leave the display on.

## Notes

- The media branch (`multimedia/web/reading/views.py:1234`–`1252`) is the only group built without
  `_blank_screen()`; the rule that asks for the rest (spec 058) was written before media screens
  existed and was never extended to them.
- Measured on `develop` `59182b12`: service 149 (1 legacy text + 4 images) builds 6 screens — four
  pictures with nothing between them, and its last screen is the fourth picture. Service 144's video,
  image, PDF and audio entries are one screen each, beside song rows that rest after every bait.
- In the dock the same gap is a row: a media entry's inner list holds `IMAGE` alone (a 37.8px body)
  where the text entry above it holds its line and `Rest` (69.7px).

## Acceptance sketch

- A media entry with a file is its media screen then one rest, for all five families; with no file it is
  its one rest.
- The rest is the built-in blank — not a row, not stored, no payload and no bait fields.
- The dock lists it under the media row and the transport steps onto it.
- Nothing else changes: the media screens, the fit and pan, the audio/video lock, the stage, the editors.

## Links

- Spec: [164 — a media entry ends on a rest like every other entry](../specs/165-media-entry-rest/spec.md)
- Related items: ITEM-060 (spec 058, the built-in blank this extends), ITEM-117 / ITEM-118 (the media
  screens that were never given one), ITEM-119 (the dock's step list)
