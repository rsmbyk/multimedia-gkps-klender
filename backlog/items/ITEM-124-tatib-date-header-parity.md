---
id: ITEM-124
status: in_review
title: 'Match the Tata Ibadah date header to the songbook header'
type: fix
priority: P1
effort: S
created: 2026-10-24
updated: 2026-10-24
spec: specs/123-tatib-date-header-parity/spec.md
branch: fix/123-tatib-date-header-parity
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/372
issue:
closed_at:
closed_reason:
bump: patch
release_version: 1.20.2
---

# ITEM-124: Match the Tata Ibadah date header to the songbook header

## Summary

A service page's date is the same header element as a song page's songbook name, but it renders at 11px
with .08em tracking — the size spec 112 left behind when it put the Project button and the media controls
on that row. Restore the shared eyebrow style and let the row wrap when the stage is too narrow for both.

## Notes

- The 11px override arrived in `7ffd243a` (spec 112) and contradicts spec 102's recorded 16.5px / .12em for
  the same element. This slice supersedes the size/tracking half of that override only.
- The saved/offline render needs no change: `static/web/offline-render.js` writes the same classes.

## Acceptance sketch

- The date's computed style equals the songbook header's on the running pages.
- At a narrow stage the Project action wraps beneath the date, the date keeps its size, and the page does
  not scroll sideways.

## Links

- Spec: [123](../../specs/123-tatib-date-header-parity/spec.md)
- Related items: ITEM-102 (spec 102, the eyebrow's recorded style), ITEM-112 (spec 112, the override's origin),
  ITEM-019 (spec 017, the long date)
