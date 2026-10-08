---
id: ITEM-023
status: archived
title: 'Hide the projection-lock explanation'
type: fix
priority: P1
effort: S
created: 2026-10-07
updated: 2026-10-08
spec: specs/021-hide-projection-lock-note/spec.md
branch:
pr:
archived_at: 2026-10-08
archive_reason: Superseded by accepted Spec 026 / ITEM-028, which removes the projection lock entirely.
bump: patch
release_version:
---

# ITEM-023: Hide the projection-lock explanation

## Summary

Superseded by Spec 026 / ITEM-028: projecting no longer blocks entry editing, so no projection-lock explanation can be shown. This item's original request is retained below for historical context; it is not a pending implementation.

## Original request

Keep entry editing blocked during projection, but remove the explanatory lock text below the projection controls.

## Notes

- Preserve Project/Stop behavior and Update behavior.
- Preserve independent status feedback for projector lifecycle and Update actions.

## Acceptance sketch

- Attempting an entry edit while projecting remains blocked without displaying the lock explanation.

## Links

- Spec: [021 — Hide the projection-lock explanation](../../specs/021-hide-projection-lock-note/spec.md)
- Related items: ITEM-020 (projection button styles)
