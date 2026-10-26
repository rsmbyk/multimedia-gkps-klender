---
id: ITEM-143
status: in-review
title: 'Keep reading views current after sidebar edits'
type: fix
priority: P1
effort: M
created: 2026-10-26
updated: 2026-10-26
spec: specs/134-sidebar-save-freshness/spec.md
branch: feat/134-sidebar-save-freshness
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/398
issue: 397
closed_at:
closed_reason:
bump: patch
release_version:
---

# ITEM-143: Keep reading views current after sidebar edits

## Summary

After a successful sidebar edit, keep the current Tata Ibadah, song, and songbook rows, active reading
view, document title, and search results consistent with saved server values without reloading or
reopening a sidebar.

## Notes

- The browser audit confirmed stale active-section sidebar rows and stale search results after saves.
- The unrelated-stage case updates the selected sidebar while preserving the open Bible chapter.
- This card is the demand for `specs/134-sidebar-save-freshness/spec.md` and carries its declared patch bump.

## Acceptance sketch

- Editing a Tata Ibadah, song, or songbook updates every matching visible reading representation in place.
- Search results and group counts reflect the saved title while the current query remains active.
- Sidebar state and unrelated stage content remain in place after a save.

## Links

- Spec: [134](../../specs/134-sidebar-save-freshness/spec.md)
- Related items: ITEM-006 (sidebar editors), ITEM-122 (saved reading parity), ITEM-119 (consistent reading navigation)
