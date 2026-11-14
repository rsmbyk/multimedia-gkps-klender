---
id: ITEM-020
status: done
title: 'Style Project and Stop projecting as primary and danger actions'
type: chore
priority: P2
effort: S
created: 2026-10-07
updated: 2026-10-08
spec: specs/018-project-button-styles/spec.md
branch: feat/026-live-projection-editing
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/275
issue:
closed_at: 2026-10-08
closed_reason: merged into develop (PR #275)
bump: patch
release_version: 1.0.0
---

# ITEM-020: Style Project and Stop projecting as primary and danger actions

## Summary

Use primary styling for the inactive Project action and danger styling for the active Stop projecting action.

## Notes

- Keep projection behavior, labels, and Update control behavior unchanged.
- Verify both states remain legible in light and dark themes.

## Acceptance sketch

- Styling follows the existing projection state: primary when inactive, danger when active.

## Links

- Spec: [018 — Style Project and Stop projecting as primary and danger actions](../../specs/018-project-button-styles/spec.md)
- Related items: ITEM-002 (projection controls)
