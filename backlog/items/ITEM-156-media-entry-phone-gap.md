---
id: ITEM-156
status: backlog
title: 'The gap above a media entry is 19.9px at the phone width, not the 12px its test asserts'
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
bump: patch
release_version:
---

# ITEM-156: The gap above a media entry is 19.9px at the phone width, not the 12px its test asserts

## Summary

`test_media_entry_has_roomy_spacing_and_wraps_on_narrow_screen` asserts that the text row below a media
entry sits **12px ± 1** under it at a 390px viewport. On `develop` as it stands the measured gap is
**19.89px**, so the test fails without any change beside it.

## Notes

- Measured twice: 19.89px on unmodified `develop` at `05379336`, 19.75px on `feat/145-media-size-precision`.
- Identical on `develop` — the spacing rule the test encodes was changed by an earlier slice (the entry
  surface and add-bar slices both moved the block gaps) and the assertion was not brought with it.
- Found by slice 145's Converge, which ran the media E2E file; recorded here rather than fixed there.

## Acceptance sketch

- The media entry's gap above its next block reads the value the page actually draws, and the test
  asserts that value at 390px.

## Links

- Test: `tests/e2e/test_media_library.py::test_media_entry_has_roomy_spacing_and_wraps_on_narrow_screen`
- Found by: [145](../specs/145-media-size-precision/spec.md)
