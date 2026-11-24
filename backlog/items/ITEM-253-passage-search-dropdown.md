---
id: ITEM-253
status: in review
title: 'Passage entry pickers use searchable dropdowns'
type: feat
priority: P2
effort: M
created: 2026-11-24
updated: 2026-11-24
spec: 238-passage-search-pickers
branch: feat/238-passage-search-pickers
pr: 618
issue:
closed_at:
closed_reason:
bump: patch
release_version:
---

# ITEM-253: Passage entry pickers use searchable dropdowns

## Summary

The song entry's picker is a search field — type to filter, Arrow/Enter to choose, Escape to
dismiss — while Add Passage's Book was a chevron button with a filter hidden inside its menu and
chapter/verse had no filter. Make Book the same search field; keep Chapter, From verse and To
verse as button popovers, but give each popover its own in-menu filter like the old book picker.

## Notes

"Same dropdown" was confirmed as the full search-combobox behaviour, not only the field styling.
Filtering runs over the option data already in the modal, so no endpoint is added. The hidden
selects stay the form's value carriers; To verse stays a button picker. Escape is prevented from
clearing a chosen label, a native behaviour of `input[type=search]`.

## Acceptance sketch

- Book, Chapter and From verse are search fields matching `#entry-song-search` chrome and menu.
- Type-to-filter, focus-select-all, one active option under Arrow keys, Enter chooses, Escape and
  outside-click close only the menu.
- Book → chapter → verse cascade, translation toggle, stored edit values and To verse unchanged.
- Song entry's picker and verse checklist unchanged.

## Links

- Spec: [238-passage-search-pickers](../specs/238-passage-search-pickers/spec.md)
- Related items: ITEM-174 (known-red backdrop race in the legacy picker module)