---
id: ITEM-016
status: done
title: 'Clear stale row-edit visibility after modal close'
type: fix
priority: P1
effort: M
created: 2026-10-07
updated: 2026-10-08
spec: specs/014-editor-focus-cleanup/spec.md
branch: feat/026-live-projection-editing
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/275
issue:
closed_at: 2026-10-08
closed_reason: merged into develop (PR #275)
bump: patch
release_version: 1.0.0
---

# ITEM-016: Clear stale row-edit visibility after modal close

## Summary

Pointer-closing a create/edit modal can leave the affected song or songbook's edit action visible even when the pointer is not over the row. Trace and correct the shared focus/hover lifecycle, then check the other sidebars and reading-pane modals without losing keyboard focus indicators.

## Notes

- Keep genuine pointer hover and keyboard `:focus-visible` behavior.
- Audit songbook, song, Tata Ibadah, service-entry, legacy-item, and confirmation modals.

## Acceptance sketch

- Pointer-driven close/save leaves no row edit action stuck visible when the pointer is away.
- Genuine hover reveals the action; keyboard focus remains visible and operable.
- Other modal/sidebar close paths do not strand controls in a revealed state.

## Links

- Spec: [014 — Clear stale row-edit visibility after modal close](../../specs/014-editor-focus-cleanup/spec.md)
- Related items: ITEM-006 (sidebar editors), ITEM-007 (service entries)
