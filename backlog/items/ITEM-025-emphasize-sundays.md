---
id: ITEM-025
status: done
title: 'Make Sundays more prominent in the Tata Ibadah date picker'
type: chore
priority: P2
effort: S
created: 2026-10-07
updated: 2026-10-08
spec: specs/023-emphasize-sundays/spec.md
branch: feat/026-live-projection-editing
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/275
issue:
closed_at: 2026-10-08
closed_reason: merged into develop (PR #275)
bump: patch
release_version: 1.0.0
---

# ITEM-025: Make Sundays more prominent in the Tata Ibadah date picker

## Summary

Emphasize Sunday dates in the Tata Ibadah calendar so they are easier to spot when choosing a date for weekly services.

## Notes

- Keep the treatment theme-aware.
- Preserve the selected-date and today indicators, Sunday defaults, and date submission behavior.

## Acceptance sketch

- Sunday dates and the Sunday weekday heading stand out from other days in light and dark themes.
- Sunday styling does not obscure selected-date or today states.

## Links

- Spec: [023 — Make Sundays more prominent in the Tata Ibadah date picker](../../specs/023-emphasize-sundays/spec.md)
- Related items: ITEM-018 (custom Tata Ibadah date picker), ITEM-022 (Sunday default and dropdown)