---
id: ITEM-075
status: in_progress
title: Collapse an idle matching sidebar
type: feat
priority: P2
effort: M
created: 2026-10-13
updated: 2026-10-13
spec: ../../specs/072-sidebar-idle-collapse/spec.md
branch: feat/072-sidebar-idle-collapse
pr:
archived_at:
archive_reason:
bump: minor
release_version: 1.8.0
---

# ITEM-075: Collapse an idle matching sidebar

## Summary

Let a matching first sidebar collapse after 60 seconds without rail or first-panel activity, using Bible mini mode and the existing other-section collapse states.

## Notes

- The owner accepted the interactive sidebar follow-ups preview and Spec 072 on 2026-10-13.

## Acceptance sketch

- Only a sidebar matching the reading page auto-collapses after the idle interval.
- Rail or first-panel interaction restarts the interval; active controls and modal work are not interrupted.
- Bible enters mini mode; a rail click reopens the panel with the page unchanged.

## Links

- Spec: [Spec 072](../../specs/072-sidebar-idle-collapse/spec.md)
