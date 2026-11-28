---
id: ITEM-273
status: backlog
title: 'Sidebars sync external changes without losing order or filter'
type: feat
priority: P1
effort: L
created: 2026-11-28
updated: 2026-11-28
spec:
branch:
pr:
issue:
closed_at:
closed_reason:
bump:
release_version:
---

# ITEM-273: Sidebars sync external changes without losing order or filter

## Summary

The songbook, song and service sidebars SHALL poll a small list-version endpoint every 10 s and, on a change, fetch the fresh fragment and reconcile by row ID: update changed rows, remove deleted rows, and animate a new row into its position under the current filter and sort.

## Notes

- Depends on ITEM-271.
- A template created while dated services are shown stays invisible; a new song sorts into its current order rather than the last-modified top.
- Filter text, sort choice, scroll offset and panel open/mini state are preserved.

## Acceptance sketch

- A row edited on another computer updates in place without a full page refresh.
- A new service row animates into its position in the current list.
- The open stage is untouched by sidebar-only changes.

## Links

- Spec:
- Related items: ITEM-271, ITEM-272
