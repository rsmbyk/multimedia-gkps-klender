---
id: ITEM-081
status: in_progress
title: Keep the open Tata Ibadah in view across list modes
type: fix
priority: P1
effort: M
created: 2026-10-13
updated: 2026-10-13
spec: ../../specs/078-tatib-mode-switch-continuity/spec.md
branch: fix/078-tatib-mode-switch-continuity
pr:
archived_at:
archive_reason:
bump: patch
release_version: 1.9.4
---

# ITEM-081: Keep the open Tata Ibadah in view across list modes

## Summary

Switch between dated orders and templates while retaining the open page and service-entry sidebar, reselecting the exact open order and scrolling it into view.

## Notes

- The owner accepted the interactive sidebar follow-ups preview on 2026-10-13.
- The Draft in Spec 078 controls implementation after explicit owner acceptance.

## Acceptance sketch

- The service-entry sidebar and stage stay open through either mode switch.
- The exact open Tata Ibadah row is selected and visible; an opposite-mode service appears as one contextual row.
- Returning to the matching mode selects the ordinary row without a duplicate.

## Links

- Spec: [Spec 078](../../specs/078-tatib-mode-switch-continuity/spec.md)
