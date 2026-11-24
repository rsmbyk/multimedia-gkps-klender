---
id: ITEM-253
status: in progress
title: 'Passage entry uses the song search dropdown'
type: feat
priority: P2
effort: M
created: 2026-11-24
updated: 2026-11-24
spec: 238-passage-search-pickers
branch: feat/238-passage-search-pickers
pr:
issue:
closed_at:
closed_reason:
bump: patch
release_version:
---

# ITEM-253: Passage entry uses the song search dropdown

## Summary

The song entry's picker is a search field — type to filter, Arrow/Enter to choose, Escape to
dismiss — while Add Passage's Book, Chapter and From verse are chevron buttons, with the book
filter hidden inside its menu and no filter at all on chapter or verse. Make those three fields
the same search combobox as the song picker, without changing the saved value, the cascade or
the To verse control.

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
