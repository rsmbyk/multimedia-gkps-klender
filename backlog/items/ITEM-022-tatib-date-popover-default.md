---
id: ITEM-022
status: in_progress
title: 'Use a date popover with a Sunday default'
type: feat
priority: P1
effort: S
created: 2026-10-07
updated: 2026-10-07
spec: specs/020-tatib-date-popover-default/spec.md
branch:
pr:
archived_at:
archive_reason:
bump: patch
release_version:
---

# ITEM-022: Use a date popover with a Sunday default

## Summary

Show the Tata Ibadah date calendar as a dropdown beneath its field and preselect the nearest Sunday when creating a service.

## Notes

- If the form opens on Sunday, select today.
- Editing a dated or undated service preserves its existing date value.
- Keep clearing, keyboard support, and ISO submission.

## Acceptance sketch

- Create defaults to today's Sunday or the next upcoming Sunday; the calendar opens as a popover beneath the field.
- Existing edit dates and blank recurring-service dates are preserved.

## Links

- Spec: [020 — Use a date popover with a Sunday default](../../specs/020-tatib-date-popover-default/spec.md)
- Related items: ITEM-018 (custom Tata Ibadah date picker)
