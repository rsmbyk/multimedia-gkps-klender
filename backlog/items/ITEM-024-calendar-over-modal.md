---
id: ITEM-024
status: done
title: 'Let the Tata Ibadah date picker overlap the editor modal'
type: fix
priority: P1
effort: S
created: 2026-10-07
updated: 2026-10-08
spec: specs/022-datepicker-over-modal/spec.md
branch: feat/026-live-projection-editing
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/275
issue:
closed_at: 2026-10-08
closed_reason: merged into develop (PR #275)
bump: patch
release_version: 1.0.0
---

# ITEM-024: Let the Tata Ibadah date picker overlap the editor modal

## Summary

The open calendar is clipped by the Tata Ibadah editor's scrollable content. Let it overlap the modal form while staying anchored to the date field, so all dates remain visible and clickable.

## Notes

- Keep the calendar below its trigger and within the viewport.
- Do not change the Sunday default, selected date, optional/clear behavior, or ISO submission.
- Preserve keyboard navigation and modal dismissal behavior.

## Acceptance sketch

- Opening the picker does not increase the form height.
- The calendar stays visible and interactive beyond the modal content's clipping edge and remains within the viewport.

## Links

- Spec: [022 — Let the Tata Ibadah date picker overlap the editor modal](../../specs/022-datepicker-over-modal/spec.md)
- Related items: ITEM-018 (custom date picker), ITEM-022 (Sunday default and dropdown)