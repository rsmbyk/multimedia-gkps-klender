Book in Add Passage is now the same type-to-filter search combobox as the song picker. Chapter, From verse and To verse keep their button popovers, but each menu gained a filter above its options. Every search dropdown highlights the stored (or first visible) option on open, follows the highlight with its own scroll box, and commits it with Enter or Tab without submitting or closing the dialog. The cascade, hidden form values, translation toggle and To verse's optional state are unchanged.

- Spec: `specs/238-passage-search-pickers/spec.md`
- Verification: 21 test · 12 inspection; passage module 19/19 green, song module 11/12 (one failure reproduces on unmodified base).
- Board: `ITEM-253` — In review at push, Done before merge.
- Bump: patch (1.36.27)

Refs ITEM-253
