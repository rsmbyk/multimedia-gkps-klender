---
id: ITEM-222
status: in-review
title: 'A newly created service opens on the reading stage'
type: fix
priority: P1
effort: S
created: 2026-11-21
updated: 2026-11-21
spec: specs/209-open-created-service/spec.md
branch: feat/209-open-created-service
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/554
issue:
closed_at:
closed_reason:
bump: patch
release_version:
---

# ITEM-222: A newly created service opens on the reading stage

## Summary

Saving a new dated Tata Ibadah from the sidebar currently refreshes the list but leaves the reading
stage where it was, so the operator has to find and click the new row. The save should open that
service on the stage in place, without a document reload.

## Notes

- Owner decision: the reading stage opens the service; the OBS dock and projector are untouched.
- Only a Normal (dated) service opens. Template creates, edits and other record saves keep their
  present list-refresh behaviour; generate and copy-as-template already navigate.
- The five E2E errors in the two focused modules were reproduced identically on the base commit;
  four belong to the ITEM-144 date-picker family and one (the pointer-closed row control) is reported
  for its own card. None was deleted or quarantined.

## Acceptance sketch

- After one sidebar create, the URL is `/tatib/<id>/`, the stage names the saved service, its row is
  current, and its empty-service actions are visible — with no second click.
- The in-page marker, `performance.timeOrigin`, `data-nav` and other list selections are unchanged.
- A Template create, an edit, a validation refusal or a failed request leaves the stage put.

## Links

- Spec: [209 — A newly created service opens on the reading stage](../../specs/209-open-created-service/spec.md)
- Related items: ITEM-144 (date-picker E2E errors on base)
