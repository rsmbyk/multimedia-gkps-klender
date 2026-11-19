---
id: ITEM-201
status: done
title: 'Copy as template stands in the edit modal header'
type: fix
priority: P1
effort: S
created: 2026-11-15
updated: 2026-11-15
spec: 195
branch: fix/195-hotfix-batch
pr: 523
issue: 518
closed_at: 2026-11-15
closed_reason: merged into develop (PR #523)
bump: patch
release_version: 1.32.1
---

# ITEM-201: Copy as template stands in the edit modal header

## Summary

The Edit Tata Ibadah modal renders the Copy as template button in its header, but no product stylesheet carries the header or button rules (spec 167's preview had them; `components.css` never received them), so the button falls below the title as an unstyled element — reading as broken on production (2026-11-15).

## Notes

- Spec 167 UI/UX: the button sits in the modal's header, right of the title, 137.8×34, no note under it.
- The click handler and confirmation layer work; this is the header layout and the button's own style.

## Acceptance sketch

- The Edit modal's title and the button share one header row; the button is right-aligned, 34px tall.
- The header carries the hairline rule the preview drew; the button matches the preview's hover and focus states.

## Links

- Spec:
- Related items:
