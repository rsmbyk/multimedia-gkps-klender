---
id: ITEM-134
status: done
title: 'Retire the Break service entry kind'
type: feat
priority: P1
effort: S
created: 2026-10-25
updated: 2026-10-25
spec: specs/131-retire-break-entry/spec.md
branch: feat/131-retire-break-entry
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/387
issue: https://github.com/rsmbyk/multimedia-gkps-klender/issues/386
closed_at:
closed_reason:
bump: patch
release_version: 1.20.9
---

# ITEM-134: Retire the Break service entry kind

## Summary

The **Break** service entry kind is retired: no surface offers it any more, no endpoint creates or edits one,
and the breaks already written keep rendering, projecting, reordering and deleting exactly as they do today.
The kind and its stored rows stay in the model — this is a retirement of the action, not a data migration.

## Notes

- Three surfaces offer creation and all three must agree: the server template (`tatib.html`), the in-place
  rebuild after a delete (`entries.js`), and the saved-page renderer (`offline-render.js`).
- The endpoint is closed with the surfaces: the save-new and save endpoints refuse the kind with `404`, so a
  stale page or a direct request cannot create one.
- Break rows already offer Delete only (spec 057). This slice makes the endpoint agree with the control.
- The legacy `END_OF_SECTION` `TataIbadahItem` row is a different table and is untouched.

## Acceptance sketch

- An add row and an empty service offer Passage, Song, Text and Media — no Break.
- A POST naming the Break kind answers `404` and creates nothing; a save or edit request on an existing Break
  answers `404` and changes nothing.
- An existing Break still draws its divider on the stage and in the sidebar, keeps its projector screen, and
  still deletes and reorders.

## Links

- Spec: [131](../../specs/131-retire-break-entry/spec.md)
- Related items: ITEM-059 (spec 057 — breaks are Delete-only), ITEM-133 (empty-service tiles, in flight)
