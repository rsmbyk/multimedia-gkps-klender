---
id: ITEM-156
status: backlog
title: 'The media-entry spacing E2E measures 19.98px where 12px is asserted'
type: fix
priority: P1
effort: S
created: 2026-10-28
updated: 2026-10-28
spec:
branch:
pr:
issue:
closed_at:
closed_reason:
bump:
release_version:
---

# ITEM-156: The media-entry spacing E2E measures 19.98px where 12px is asserted

## Summary

`tests/e2e/test_media_library.py::MediaLibraryE2ETests::test_media_entry_has_roomy_spacing_and_wraps_on_narrow_screen`
asserts that a text row sits `12px ± 1` below the media row above it. It measures 19.98px on
`feat/147-transfer-icon-column` and 19.71px on unmodified `develop` at `05379336` — identical on
develop, so the spacing tests of specs 142–143 are unproven rather than broken by any slice in flight.

## Notes

- Found while running the media library E2E module for slice 147 (spec 147 does not touch entry
  spacing; its Converge records this as an observation, not a gap).
- 19.7–20px is the add-row slot shipped by spec 143, not the 12px gap the test still expects — likely
  a test that was not rewritten by that slice.

## Acceptance sketch

- The test and the shipped spacing agree; either the assertion is rewritten to the add row's slot or
  the slot is changed, and the decision is recorded in the card before the change.

## Links

- Found in: [147](../../specs/147-transfer-icon-column/converge.md)
- Related: spec 142 (entry surface), spec 143 (add bar)
