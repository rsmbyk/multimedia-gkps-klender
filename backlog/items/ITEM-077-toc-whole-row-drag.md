---
id: ITEM-077
status: in_progress
title: Drag service entries from the whole sidebar row
type: feat
priority: P2
effort: M
created: 2026-10-13
updated: 2026-10-13
spec: ../../specs/074-toc-whole-row-drag/spec.md
branch: feat/074-toc-whole-row-drag
pr:
archived_at:
archive_reason:
bump: minor
release_version: 1.9.0
---

# ITEM-077: Drag service entries from the whole sidebar row

## Summary

Start desktop pointer reordering from the number, text, or blank space of a movable service-entry row while keeping the grip as a cue and keyboard/touch control.

## Notes

- The owner accepted the interactive sidebar follow-ups preview on 2026-10-13.
- The Draft in Spec 074 controls implementation after explicit owner acceptance.

## Acceptance sketch

- Whole-row mouse/pen drag saves the new order on drop.
- A click still jumps to the entry; a completed drag does not activate the link.
- The visible grip continues to support touch and keyboard movement.

## Links

- Spec: [Spec 074](../../specs/074-toc-whole-row-drag/spec.md)
