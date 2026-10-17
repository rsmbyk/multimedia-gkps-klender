---
id: ITEM-104
status: in_review
title: 'Polish media picker layout and tab feedback'
type: chore
priority: P2
effort: S
created: 2026-10-17
updated: 2026-10-17
spec: specs/104-media-picker-layout/spec.md
branch: feat/104-media-picker-layout
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/354
archived_at:
archive_reason:
bump: patch
release_version: 1.14.1
---

# ITEM-104: Polish media picker layout and tab feedback

## Summary

Keep the New media modal at its tall layout when the connected Media Library is empty, with a quiet, spacious empty state. Make “Supported files:” bold at the same size as the adjacent supported-types text, and add the existing switch hover treatment to the inactive media-source tab.

## Notes

- The owner selected the quiet visual concept and requested more relaxed space around it on 2026-10-17.
- The owner requested the empty-library preview retain the taller New media modal size and the Upload tab's supported-files label match the adjacent text size.
- The owner requested the inactive Upload/Media Library tab get hover feedback matching other app switches.
- The owner accepted Spec 104 on 2026-10-17; implementation is on `feat/104-media-picker-layout`, stacked on Spec 103 while its media-picker implementation is under review.
- Draft PR [#354](https://github.com/rsmbyk/multimedia-gkps-klender/pull/354) targets `feat/103-local-media-library`; retarget it to `develop` after PR #353 merges.
- The connected-empty preview is [preview.png](../../specs/104-media-picker-layout/preview.png); the upload typography preview is [upload-typography-preview.png](../../specs/104-media-picker-layout/upload-typography-preview.png); the tab-hover preview is [tab-hover-preview.png](../../specs/104-media-picker-layout/tab-hover-preview.png).
- The change is limited to the New media modal's connected-empty state, supported-files typography, and source-tab hover state.

## Acceptance sketch

- A connected library with no files shows the quiet, centered empty state and preserves the same tall modal dimensions as the Upload tab.
- The supported-files label is 12 px like the rest of its line, while remaining semibold.
- Hovering the unselected source tab gives it the same subtle background and ink-color change used by the app's other switches; the selected tab remains visually unchanged.
- A disconnected library retains its existing unavailable message.
- Save stays disabled until a file is selected, and the title and Cancel controls remain reachable on short screens.

## Links

- Spec: [104](../../specs/104-media-picker-layout/spec.md)
- Related items: [ITEM-103](./ITEM-103-local-media-library.md)
