---
id: ITEM-012
status: in_review
title: 'Sort hymn book songs by number and sub-number'
type: fix
priority: P1
effort: S
created: 2026-10-06
updated: 2026-10-06
spec: specs/011-hymn-song-order/spec.md
branch: fix/011-hymn-song-order
pr: 270
archived_at:
archive_reason:
bump: patch
release_version: 0.11.3
---

# ITEM-012: Sort hymn book songs by number and sub-number

## Summary

Show each hymn book’s songs in numeric song-number order, with sub-number variants grouped beneath their base number. This restores the ordering already promised for hymn books in the public Kidung reading experience.

## Notes

- Keep the change scoped to the public hymn-book song list.
- Preserve non-hymn song-list sorting and its toggle.
- Use the separate numeric `number` and text `sub_number` fields; do not sort a rendered citation as text.

## Acceptance sketch

- Hymn songs appear by ascending numeric number, then ascending sub-number, with a blank sub-number before lettered variants.
- Non-hymn song lists keep their existing default and alphabetical sort behavior.
- Hymn books continue to have no sort toggle.

## Links

- Spec: [`specs/011-hymn-song-order/spec.md`](../../specs/011-hymn-song-order/spec.md)
- Related item: ITEM-005
