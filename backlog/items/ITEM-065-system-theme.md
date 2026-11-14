---
id: ITEM-065
status: done
title: 'System theme as the default appearance mode'
type: feat
priority: P2
effort: S
created: 2026-10-12
updated: 2026-10-12
spec: 062
branch: feat/062-system-theme
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/315
archived_at:
archive_reason:
bump: minor
release_version: 1.6.0
---

# ITEM-065: System theme as the default appearance mode

## Summary

Let readers choose Light, Dark, or System. Use System when no preference has been saved.

## Notes

The current `develop` branch has a light/dark switcher on the public reading site. This slice adds System as a selectable mode and makes it the default.

## Acceptance sketch

- A new reader sees the current system theme and System selected.
- A reader can choose Light or Dark regardless of the system theme.
- System follows changes to the operating system theme without reloading.
- A saved Light or Dark selection remains unchanged.

## Links

- Spec: [../../specs/062-system-theme/spec.md](../../specs/062-system-theme/spec.md)
- Related items:
