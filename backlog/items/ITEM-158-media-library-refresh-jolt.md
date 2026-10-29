---
id: ITEM-158
status: in-review
title: 'The Media Library list jumps while it refreshes'
type: fix
priority: P2
effort: S
created: 2026-10-28
updated: 2026-10-28
spec: specs/148-media-library-refresh-flicker/spec.md
branch: feat/148-media-library-refresh-flicker
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/424
issue: https://github.com/rsmbyk/multimedia-gkps-klender/issues/423
closed_at:
closed_reason:
bump:
release_version:
---

# ITEM-158: The Media Library list jumps while it refreshes

## Summary

Every action on `/media-library/` that ends in `refresh()` draws the list twice: the first pass
passes `uses = null`, so each file's `used by` line becomes the one-line `Service uses unavailable`
placeholder and the rows shrink from 119/101/123px to 97px. The list loses 68px, everything below the
first row jumps up 22px and back, and the action that shows it most is Share online.

## Notes

Reported from a screencast of `/media-library/` on `localhost:63404`: the list jolts twice, once per
upload click. Measured on the running page: row 2 top 377 → 355, row 3 478 → 452, row 4 653 → 601,
back to the start within 16–85ms.

Cause: `static/web/media-library.js:148` (`uses = null; … render()`) before the references request
resolves, then `:155` (`render()`) again with them. `render()` is `list.replaceChildren()` + a full
rebuild (`:94`).

## Acceptance sketch

- Clicking Share online, Remove-then-cancel, Save setting, and opening the page each leave every row
  at one position across the whole refresh, sampled every frame.
- A file whose references are known never shows `Service uses unavailable`.
- The first load paints the list once, complete, with its references.

## Links

- Spec: [148](../specs/148-media-library-refresh-flicker/spec.md)
- Related items: ITEM-145, ITEM-146, ITEM-147 (other slices touching this page); ITEM-156 is the
  media-entry spacing E2E this slice found red on develop
