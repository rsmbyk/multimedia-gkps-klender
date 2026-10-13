---
id: ITEM-083
status: in-review
title: Keep the first-level sidebar state when a page opens from a second-level list
type: fix
priority: P1
effort: M
created: 2026-10-13
updated: 2026-10-13
spec: ../../specs/080-sidebar-state-on-item-open/spec.md
branch: fix/080-sidebar-state-on-item-open
pr:
archived_at:
archive_reason:
bump: patch
release_version: 1.10.1
---

# ITEM-083: Keep the first-level sidebar state when a page opens from a second-level list

## Summary

Opening a page from a second-level list re-opens the first-level sidebar the operator had collapsed —
reported three times, once per section: the Tata Ibadah panel springs open when an entry is added to the
open service, the songbook panel when a song is opened, and the Bible book panel when a chapter is
opened.

## Notes

- Root cause: `applyPage` copies the arriving page's `data-nav` over the live one for every
  stage-swapping navigation, and every reading page is rendered with `nav="open"`.
- The post-save `refresh` is a stage-swapping navigation too, which is why adding an entry triggers it.
- Fix scope is the four stage-only kinds (`chapter`, `song`, `service`, `refresh`); main-menu switches
  and the search paths keep their current behaviour.
- Draft only — no implementation until the owner accepts Spec 080.

## Acceptance sketch

- A collapsed first panel stays collapsed while the stage swaps from a second-level item click.
- A mini Bible panel stays mini.
- A main-menu switch still opens the arriving section's panel.

## Links

- Spec: [Spec 080](../../specs/080-sidebar-state-on-item-open/spec.md)
- Preview: [state preview](../../specs/080-sidebar-state-on-item-open/preview.html)
- Related items: ITEM-078 (mode-switch continuity), ITEM-075 (idle collapse)
