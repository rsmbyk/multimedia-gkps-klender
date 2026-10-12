---
id: ITEM-070
status: in_progress
title: Consistent scrollbars across app views
type: feat
priority: P2
effort: S
created: 2026-10-12
updated: 2026-10-12
spec: ../../specs/067-consistent-scrollbars/spec.md
branch: feat/067-consistent-scrollbars
pr:
archived_at:
archive_reason:
bump: patch
release_version: 1.6.6
---

# ITEM-070: Consistent scrollbars across app views

## Summary

Use the attached Tata Ibadah sidebar scrollbar as the visual reference for scrollable areas in the new app UI.

## Notes

- The reference has a narrow, rounded, subdued thumb and an unobtrusive track on a dark surface.
- Include page and panel scrolling, preview modals, dropdown menus, and multiline text fields in the new UI.
- Exclude the legacy web and OBS dock/source pages.
- Preserve scrollbar visibility and usable contrast on light surfaces.

## Acceptance sketch

- Scrollable panels, previews, menus, text fields, and pages in the new UI use one coherent thin scrollbar treatment.
- Dark and light surfaces remain legible; scrolling, keyboard access, and touch behavior still work.

## Links

- Spec: [Spec 067](../../specs/067-consistent-scrollbars/spec.md)
