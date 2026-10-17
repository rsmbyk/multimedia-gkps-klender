---
id: ITEM-106
status: in_review
title: 'Keep media entries visible in saved Tata Ibadah pages'
type: fix
priority: P2
effort: M
created: 2026-10-17
updated: 2026-10-17
spec: specs/106-tatib-offline-media-rendering/spec.md
branch: fix/106-tatib-offline-media-rendering
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/359
archived_at:
archive_reason:
bump: patch
release_version: 1.14.3
---

# ITEM-106: Keep media entries visible in saved Tata Ibadah pages

## Summary

In-place navigation can use the saved-page renderer, which currently drops media entry icons
and media add actions. Keep saved and server-rendered Tata Ibadah pages consistent.

## Notes

- Diagnosis: `static/web/offline-render.js` omits media from `addButtons` and does not emit the
  media row icon or identifying attributes. `multimedia/web/reading/offline.py` also filters
  those fields out of the saved service chunk.
- The current server-rendered page already defines the intended appearance and behavior.
- Related accepted media slices: [Spec 103](../../specs/103-local-media-library/spec.md),
  [Spec 108](../../specs/108-media-navigation-feedback/spec.md).

## Acceptance sketch

- Opening a Tata Ibadah through in-place navigation shows media icons, media labels, and the
  same add-media actions as a full refresh.
- Existing saved offline chunks refresh when the media metadata shape changes.
- Other entry types, order, and projector behavior remain unchanged.

## Links

- Spec: [106](../../specs/106-tatib-offline-media-rendering/spec.md)
- Related items: [ITEM-103](./ITEM-103-local-media-library.md),
  [ITEM-108](./ITEM-108-media-navigation-feedback.md)
