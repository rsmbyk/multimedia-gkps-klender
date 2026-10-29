---
id: ITEM-157
status: backlog
title: 'The media-entry spacing E2E pins a 12px gap the row no longer has'
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

# ITEM-157: The media-entry spacing E2E pins a 12px gap the row no longer has

## Summary

`tests/e2e/test_media_library.py::MediaLibraryE2ETests::test_media_entry_has_roomy_spacing_and_wraps_on_narrow_screen`
asserts that the next entry's top sits 12 ± 1px below a media entry's bottom. On an unmodified
`develop` at `05379336` it measures **19.85px**, and on `feat/148-media-library-refresh-flicker`
(which does not touch that surface) **19.67px** — the same failure, so the assertion is what went
stale, not the row.

The 20px difference is the slot spec 143's add bar reserves in the flow, which the row now carries
below it. The number to pin is the one the row actually holds; either the assertion moves to 20px or
it measures that slot explicitly, which is a decision for whoever takes this card.

## Notes

- Proven on `develop` in the main checkout: `manage.py test
  tests.e2e.test_media_library.MediaLibraryE2ETests.test_media_entry_has_roomy_spacing_and_wraps_on_narrow_screen
  --keepdb` → `AssertionError: 19.8453369140625 != 12 within 1 delta`.
- Nothing else in `tests.e2e.test_media_library` fails on `develop`.

## Acceptance sketch

- The case passes on `develop` unchanged, or its expectation is corrected and it passes on the branch
  that corrects it.
- No product behaviour changes: the row's rendered gap is what it is today.

## Links

- Spec: —
- Related items: ITEM-154 (spec 143, the add bar's 20px slot), ITEM-156 (the slice that found it)
