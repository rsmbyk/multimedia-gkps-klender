---
id: ITEM-105
status: in_review
title: 'Keep media navigation selection feedback in sync'
type: fix
priority: P2
effort: S
created: 2026-10-17
updated: 2026-10-17
spec: specs/105-media-navigation-feedback/spec.md
branch: feat/105-media-navigation-feedback
pr:
archived_at:
archive_reason:
bump: patch
release_version: 1.14.2
---

# ITEM-105: Keep media navigation selection feedback in sync

## Summary

Move the selected surface between Upload and Media Library like the app's other switches, and
clear the main-sidebar Media Library highlight when in-place navigation opens another
destination.

## Notes

- The owner accepted the interactive UI preview and Spec 105 Draft on 2026-10-17.
- The selected media-source tab uses the existing switch easing and theme tokens; the approved
  screenshot is [preview.png](../../specs/105-media-navigation-feedback/preview.png).
- The Media Library link must remain selected on direct loads and when browser history returns
  to that page. Other rail-menu `aria-expanded` and panel behavior remains unchanged.
- Implementation is on `feat/105-media-navigation-feedback`, based on the current Spec 104 media
  feature stack; `develop` is an ancestor of this branch.
- Targeted verification passed: all 16 tests in `tests.e2e.test_media_library`.

## Acceptance sketch

- Switching media tabs moves one active thumb in either direction and keeps the selected tab,
  visible panel, and accessible state aligned; reduced motion disables the animation.
- Navigating in place away from Media Library clears its stale current-page highlight; direct
  loads and Back / Forward restore the highlight for the destination actually shown.
- Existing rail menu expansion and panel state remain unchanged.

## Links

- Spec: [105](../../specs/105-media-navigation-feedback/spec.md)
- Related items: [ITEM-103](./ITEM-103-local-media-library.md),
  [ITEM-104](./ITEM-104-media-picker-layout.md)
