---
id: ITEM-079
status: done
title: Make reading search clear controls consistent
type: fix
priority: P2
effort: S
created: 2026-10-13
updated: 2026-10-13
spec: ../../specs/076-search-clear-controls/spec.md
branch: fix/076-search-clear-controls
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/330
archived_at:
archive_reason:
bump: patch
release_version: 1.9.2
---

# ITEM-079: Make reading search clear controls consistent

## Summary

Unify and slightly enlarge the existing clear buttons in the home search and both reading sidebar filters.

## Notes

- The owner accepted the interactive sidebar follow-ups preview on 2026-10-13.
- The Draft in Spec 076 controls implementation after explicit owner acceptance.

## Acceptance sketch

- All three clear controls use a 26px circle and centered 14px cross.
- Their hover/focus states align in light and dark themes.
- Clearing restores full results and returns focus to the field.

## Links

- Spec: [Spec 076](../../specs/076-search-clear-controls/spec.md)
- PR: [#330](https://github.com/rsmbyk/multimedia-gkps-klender/pull/330)
- CI: [full browser and fast checks](https://github.com/rsmbyk/multimedia-gkps-klender/actions/runs/38369485965) passed on `6d800ad` after rerunning one unrelated search-scroll assertion.
