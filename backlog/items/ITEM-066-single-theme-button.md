---
id: ITEM-066
status: done
title: 'Restore the single theme button'
type: chore
priority: P2
effort: S
created: 2026-10-12
updated: 2026-10-12
spec: 063
branch: chore/063-single-theme-button
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/317
archived_at:
archive_reason:
bump: patch
release_version: 1.6.2
---

# ITEM-066: Restore the single theme button

## Summary

Replace the three theme buttons in the public reading rail with one button styled like the original theme switcher. Keep System, Dark, and Light modes and show the active mode in the icon and tooltip.

## Notes

- Follows [spec 062](../../specs/062-system-theme/spec.md).
- Owner approved the revised single-button preview in this task conversation before Draft 063.

## Acceptance sketch

- The rail has one theme button in the original position and style.
- Each click cycles System → Dark → Light → System.
- Icon, tooltip, and accessible name identify the active mode.
- The stored preference, System default, and live device-theme following continue to work.

## Links

- Spec: [../../specs/063-single-theme-button/spec.md](../../specs/063-single-theme-button/spec.md)
- Related items: [ITEM-065](./ITEM-065-system-theme.md)
