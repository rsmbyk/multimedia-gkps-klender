---
id: ITEM-072
status: done
title: Manual screen breaks for multiline Text entries
type: feat
priority: P2
effort: M
created: 2026-10-13
updated: 2026-10-13
spec: ../../specs/069-manual-text-screen-breaks/spec.md
branch: feat/069-manual-text-screen-breaks
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/323
archived_at:
archive_reason:
bump: minor
release_version: 1.7.0
---

# ITEM-072: Manual screen breaks for multiline Text entries

## Summary

Let an editor choose how the lines of an ordinary Tata Ibadah Text entry are grouped on projector screens. The existing two-line and blank-line behavior remains the default.

## Acceptance sketch

- The preview modal shows one row per text line; hovering a gap previews a divider and clicking it adds a break.
- The modal shows default or custom mode, quieter default dividers, labeled hover feedback, clickable breaks, and a footer Reset breaks control.
- A saved entry can show a chosen line alone or keep more than two consecutive lines together.
- The reading pane, projector navigation, and existing entry content continue to work; entries without overrides still group in pairs.

## Links

- Spec: [Spec 069](../../specs/069-manual-text-screen-breaks/spec.md)
