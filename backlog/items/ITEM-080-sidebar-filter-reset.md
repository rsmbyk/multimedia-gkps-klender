---
id: ITEM-080
status: in_review
title: Clear sidebar filters on main-menu switches
type: fix
priority: P2
effort: S
created: 2026-10-13
updated: 2026-10-13
spec: ../../specs/077-sidebar-filter-reset/spec.md
branch: fix/077-sidebar-filter-reset
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/331
archived_at:
archive_reason:
bump: patch
release_version: 1.9.3
---

# ITEM-080: Clear sidebar filters on main-menu switches

## Summary

Empty first- and second-sidebar filters when the operator selects another main rail menu, so returning lists are not stale.

## Notes

- The owner accepted the interactive sidebar follow-ups preview on 2026-10-13.
- The Draft in Spec 077 controls implementation after explicit owner acceptance.

## Acceptance sketch

- Changing main menus clears both sidebar filters and their clear buttons.
- Returning to a menu shows its full lists.
- Same-menu navigation and the global search query retain their established behavior.

## Links

- Spec: [Spec 077](../../specs/077-sidebar-filter-reset/spec.md)
- PR: [#331](https://github.com/rsmbyk/multimedia-gkps-klender/pull/331)
