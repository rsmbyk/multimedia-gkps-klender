---
id: ITEM-211
status: in-review
title: 'A clicked service keeps its sidebar date'
type: fix
priority: P1
effort: S
created: 2026-11-19
updated: 2026-11-19
spec: specs/201-sidebar-date-focus/spec.md
branch: fix/201-sidebar-date-focus
pr: 537
issue: 536
closed_at:
closed_reason:
bump: patch
release_version:
---

# ITEM-211: A clicked service keeps its sidebar date

## Summary

Clicking a dated Tata Ibadah row leaves its link focused. The date-hide rule uses
`li[data-editor-kind]:focus-within`, so the date (and, on a Today row, the badge) stays hidden
after the pointer leaves, with no action controls revealed. It returns only when focus moves
elsewhere. The row controls themselves already avoid `:focus-within` for exactly this reason.

## Notes

- Cause: `static/styles/design/components.css:1440-1445` (spec 190's date rule, extended by spec 195's badge).
- Control reveal uses `.row-edit:focus-visible` / `.row-delete:focus-visible` at lines 487-505.
- Reproduced live on base `92edc752`: at rest `block`, hover `none`, clicked + pointer away `none`
  with `:focus-within` true, clicked elsewhere `block`.
- Capability: `reading/R41` (date) and `reading/R9` (Today badge) both describe the reveal and need
  the same clarification.

## Acceptance sketch

- Click a service row, move the pointer off it: the date is painted again.
- Hover still hides the date; keyboard focus on pencil/trash still hides it.
- The Today badge follows the same states; accessible label and row geometry never change.

## Links

- Spec: [201](../specs/201-sidebar-date-focus/spec.md)
- Related items: ITEM-194 (spec 190, row actions), the spec 195 hotfix batch (Today badge)
