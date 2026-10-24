---
id: ITEM-131
status: in-review
title: 'Separate the hymn songbooks from the rest of the Kidung panel'
type: feat
priority: P2
effort: S
created: 2026-10-24
updated: 2026-10-24
spec: specs/128-songbook-hymn-separator/spec.md
branch: feat/128-songbook-hymn-separator
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/380
issue:
closed_at:
closed_reason:
bump: patch
release_version:
---

# ITEM-131: Separate the hymn songbooks from the rest of the Kidung panel

## Summary

The Kidung panel is one flat column, so nothing tells an operator where the four hymn collections end and the
locally kept songbooks begin. Put the hymn books first, draw the panel's own divider once, and let the
ordinary songbooks read A–Z below it — with no heading on either side.

## Notes

- The separator is the panel's existing group rule (`.group + .group`), the same one Alkitab uses between
  testaments, so the slice adds a second `section.group` and no new element.
- "Alphabetical" is a folded ordinal key (`search_lib.normalize` on the server, `normalized()` in the saved
  renderer), not the database collation and not `localeCompare`.
- A group the filter empties drops its separator; the same guard reaches a filtered testament or Tata Ibadah
  month.
- The Kidung panel has no mini-rail state — `#panelCollapse` and the idle collapse send it to `closed`; mini
  belongs to Alkitab.

## Acceptance sketch

- `/songs/` shows the hymn books, one `2px` divider, then the ordinary songbooks A–Z, no heading.
- Filtering to an ordinary book leaves the surviving group flush, with no floating rule.
- A songbook page, a song page and the saved copy of each draw the same two groups.

## Links

- Spec: [128](../../specs/128-songbook-hymn-separator/spec.md)
- Related items: ITEM-125 (saved song sort parity), ITEM-129 (site name in the tab)
