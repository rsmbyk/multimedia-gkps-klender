---
id: ITEM-097
status: in-review
title: 'Keep reading updates targeted and entry deletion atomic'
type: fix
priority: P1
effort: L
created: 2026-10-16
updated: 2026-10-16
spec: 094
branch: feat/092-offline-library-sync
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/347
archived_at:
archive_reason:
bump: patch
release_version: 1.13.0
---

# ITEM-097: Keep reading updates targeted and entry deletion atomic

## Summary

Deleting a service entry releases its dialog while a separate reading refresh is still running. The operator can then act on stale rows. Reading updates also replace whole stage and sidebar regions, making unchanged content flash and losing live DOM state. Keep the delete pending through the visible update and update only components whose data changed.

## Acceptance sketch

- A delete confirmation accepts one click, stays busy through the resulting view update, and releases only after the deleted row is removed from the reading pane and service sidebar.
- An accepted delete never reports that the deletion itself failed merely because its follow-up read failed.
- In-page navigation and background refresh preserve unchanged stage and sidebar nodes, focus, filter values, and scroll positions while updating changed content.
- Changed sections, rows, controls, and metadata still update correctly for server and saved-library rendering.

## Links

- Spec: [094](../../specs/094-targeted-reading-updates/spec.md)
- Related items: [ITEM-096](./ITEM-096-edit-request-feedback.md)
