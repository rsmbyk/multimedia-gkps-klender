---
id: ITEM-027
status: in progress
title: 'Avoid automatic row outlines after modal close'
type: fix
priority: P1
effort: M
created: 2026-10-08
updated: 2026-10-08
spec: specs/025-quiet-modal-focus/spec.md
branch: feat/026-live-projection-editing
pr:
archived_at:
archive_reason:
bump: patch
release_version: 0.12.0
---

# ITEM-027: Avoid automatic row outlines after modal close

## Summary

Do not leave created/edited songs or songbooks outlined after Enter/Escape closes a modal. Check the same focus issue across Tata Ibadah and other reading-shell modals/sidebars while preserving keyboard operation.

## Notes

- Live Escape reproduced focus rings on songbook, song, and Tata Ibadah links; Enter on Cancel reproduced the songbook ring.
- Automatic restoration now uses a temporary quiet marker; deliberate keyboard/pointer navigation removes it, so focus indicators remain usable.
- Saved-row targeting uses kind and ID; entry/legacy deletes choose a surviving row or the read region.
- Focused E2E covers sidebar create/edit saves, service-entry and legacy-item modals, delete confirmation, and deliberate Tab focus. Save paths use the isolated test database.
- The unsaved-order modal is absent in the current worktree because reordering now writes immediately under accepted Spec 026; direct-save/no-prompt reorder regressions pass.
- Shared with ITEM-026 and accepted ITEM-028 on `feat/026-live-projection-editing`; `release_version` is 0.12.0 because ITEM-028 carries the higher minor bump. Full browser suite deferred to push.

## Acceptance sketch

- Enter/Escape/pointer close and save do not leave an automatic outline or stale idle edit action.
- Focus survives DOM refresh predictably; normal Tab/Shift+Tab shows visible focus.
- Audit/fix the same issue across service-entry, legacy-item, delete-confirmation, and unsaved-order modals.

## Links

- Spec: [025 — Quiet modal focus restoration](../../specs/025-quiet-modal-focus/spec.md)
- Related items: ITEM-016 (row-edit visibility cleanup)
