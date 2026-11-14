---
id: ITEM-068
status: done
title: 'Hold the service entry highlight while its modal is open'
type: fix
priority: P2
effort: S
created: 2026-10-12
updated: 2026-10-12
spec: 065
branch: fix/065-entry-modal-origin-highlight
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/318
archived_at:
archive_reason:
bump: patch
release_version: 1.6.3
---

# ITEM-068: Hold the service entry highlight while its modal is open

## Summary

Clicking an entry's Preview, Edit, or Delete control drops the entry's highlight
as soon as the modal opens, because the backdrop takes the hover and the dialog
takes focus. Keep the origin entry's fill and controls until the modal closes.

## Notes

- Owner chose to hold both the fill and the floating controls (2026-10-12).
- Owner approved the state preview on 2026-10-12; spec 065 accepted on 2026-10-12.
- After-close behaviour stays as spec 061 defines it.

## Acceptance sketch

- While any entry modal is open, only its origin entry shows the hover fill and
  controls, whether opened by pointer or keyboard.
- Closing by any route releases it; spec 061 then governs the resting state.

## Links

- Spec: [065](../../specs/065-entry-modal-origin-highlight/spec.md)
- Preview: [state preview](../../specs/065-entry-modal-origin-highlight/preview.html)
- Related items: ITEM-063, ITEM-036
