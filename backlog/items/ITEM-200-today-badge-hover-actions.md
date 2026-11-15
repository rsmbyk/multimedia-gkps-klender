---
id: ITEM-200
status: done
title: 'The Today badge sits under the revealed row actions'
type: fix
priority: P1
effort: S
created: 2026-11-15
updated: 2026-11-15
spec: 195
branch: fix/195-hotfix-batch
pr: 523
issue: 517
closed_at: 2026-11-15
closed_reason: merged into develop (PR #523)
bump: patch
release_version: 1.32.1
---

# ITEM-200: The Today badge sits under the revealed row actions

## Summary

Hovering a dated Tata Ibadah row reveals the edit and delete controls on the row's trailing edge — exactly where the Today badge is painted, so the controls land on top of the badge (seen on production, 2026-11-15). The badge should step aside the same way the row's date already does while the actions are revealed.

## Notes

- Spec 190 already hides `.book__s` (the date) on hover for this exact reason; the badge needs the same rule.
- The badge must stay in the accessible label — it is why the row leads Upcoming (spec 132).

## Acceptance sketch

- Hovering a Today row hides the badge while the controls are up; leaving the row brings it back.
- At rest the badge is unchanged (position, colours, size).

## Links

- Spec:
- Related items:
