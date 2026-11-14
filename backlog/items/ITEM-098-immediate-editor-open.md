---
id: ITEM-098
status: done
title: 'Open editors immediately during form loads'
type: fix
priority: P1
effort: M
created: 2026-10-16
updated: 2026-10-16
spec: [095](../../specs/095-immediate-editor-open/spec.md)
branch: feat/092-offline-library-sync
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/347
archived_at:
archive_reason:
bump: patch
release_version: 1.13.0
---

# ITEM-098: Open editors immediately during form loads

## Summary

Sidebar and service-entry Add/Edit controls fetch their forms before opening the shared modal. On a slow connection, repeated clicks start multiple reads; late responses can reopen the modal after it was closed. Show the modal immediately with a cancellable loading state and ensure only the active request may populate it.

## Acceptance sketch

- A single click opens the modal immediately with a loading state, even while the form request is pending.
- Repeated activation cannot queue another form open. Closing the loading modal cancels or invalidates its request, so its late response cannot reopen the modal.
- A failed or offline form read closes the loading modal and shows the existing editor-load failure toast.
- Sidebar songbook, song, and Tata Ibadah forms and current/legacy service-entry forms follow the same behavior.

## Links

- [Draft spec](../../specs/095-immediate-editor-open/spec.md)
- [Interactive preview](../../specs/095-immediate-editor-open/preview.html)
- Related item: [ITEM-096](./ITEM-096-edit-request-feedback.md)
