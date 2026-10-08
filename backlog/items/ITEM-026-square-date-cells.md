---
id: ITEM-026
status: in progress
title: 'Make Tata Ibadah calendar date cells square'
type: chore
priority: P2
effort: S
created: 2026-10-08
updated: 2026-10-08
spec: specs/024-square-date-cells/spec.md
branch: feat/026-live-projection-editing
pr:
archived_at:
archive_reason:
bump: patch
release_version: 0.12.0
---

# ITEM-026: Make Tata Ibadah calendar date cells square

## Summary

Give all date-picker day cells equal width and height while keeping Sunday accents, selected/today indicators, and top-layer placement.

## Notes

- Confirmed interpretation: 1:1 proportions, retaining the existing 8 px corner radius.
- CSS uses the seven-column width, `aspect-ratio: 1`, and zero minimum height/padding; no picker logic changed.
- Focused E2E passes across desktop, mobile, narrow, and short viewports; 4-, 5-, and 6-week months; Sunday themes and date-picker behavior.
- The active branch also carries accepted ITEM-028 (minor); `release_version` is therefore 0.12.0 rather than a standalone patch release.
- Full browser suite deferred to push; no commit or push requested.

## Acceptance sketch

- Day buttons and blank slots are square at desktop and narrow widths.
- Months with different row counts remain usable inside the viewport.
- Existing calendar behaviors and Sunday emphasis remain intact.

## Links

- Spec: [024 — Square date cells](../../specs/024-square-date-cells/spec.md)
- Related items: ITEM-024 (calendar overlap), ITEM-025 (Sunday emphasis)
