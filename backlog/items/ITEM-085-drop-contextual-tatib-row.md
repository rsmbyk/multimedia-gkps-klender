---
id: ITEM-085
status: done
title: Stop inventing a Tata Ibadah row for the open service
type: fix
priority: P1
effort: S
created: 2026-10-13
updated: 2026-10-13
spec: ../../specs/082-drop-contextual-tatib-row/spec.md
branch: fix/082-drop-contextual-tatib-row
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/336
archived_at:
archive_reason:
bump: patch
release_version: 1.10.3
---

# ITEM-085: Stop inventing a Tata Ibadah row for the open service

## Summary

When the open service is missing from the list mode on screen, the panel appends a synthetic
"· Currently open" card under a divider (the owner's screenshot). The list should show the mode's own
services only, and highlight the open service only when it is in them.

## Notes

- Supersedes the contextual row introduced with Spec 078 (ITEM-081); the rest of that slice stays.
- Touches `_tatib_groups()`, the `contextual` flag, the suffix copy, and the edit-control exemption
  built on that flag.
- Draft only — no implementation until the owner accepts Spec 082.

## Acceptance sketch

- Template mode lists templates; a dated open service adds no row and no "Currently open" text.
- Dated mode lists dated services; a template open service adds no row.
- An open service inside the shown list keeps its single highlighted row and its edit control.

## Links

- Spec: [Spec 082](../../specs/082-drop-contextual-tatib-row/spec.md)
- Preview: [Tata Ibadah list preview](../../specs/082-drop-contextual-tatib-row/preview.html)
- Related items: ITEM-081 (mode-switch continuity — part superseded)
