---
id: ITEM-096
status: in-review
title: 'Unified feedback for edit requests'
type: feat
priority: P1
effort: M
created: 2026-10-16
updated: 2026-10-16
spec: 093
branch: feat/092-offline-library-sync
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/347
archived_at:
archive_reason:
bump: minor
release_version: 1.13.0
---

# ITEM-096: Unified feedback for edit requests

## Summary

Show one bottom-right toast per edit action from request start through success or failure. Replace scattered generic red request statuses, keep field-specific validation useful, and prevent duplicate or interrupted edits while a write is pending.

## Notes

The approved [interactive preview](../../specs/093-edit-request-feedback/preview-v11.html) establishes placement, stacking, states, timing, and modal/non-modal locks. Editor and preview dialogs use the browser top layer, so the live toast host must remain visible above them.

## Acceptance sketch

- An action's loading toast morphs into its own success or failure result and closes after the specified timer.
- Simultaneous pending actions retain separate toasts; new toasts enter at the bottom. Four or more visible toasts shorten settled-toast timers without hiding pending progress.
- Modal forms cannot change or close while submitting; a non-modal write disables only its initiating control until settlement.
- Songbook, song, Tata Ibadah, service-entry, reorder, and custom-break writes use the shared feedback.

## Links

- Spec: [093](../../specs/093-edit-request-feedback/spec.md)
- Related items: [ITEM-095](./ITEM-095-offline-library-sync.md)
