# Data Model: passage search comboboxes

**Spec**: `specs/238-passage-search-pickers/spec.md`

## Entities

No persisted entity is added, removed or changed. No model, migration, form class,
serialiser or endpoint is touched. The slice edits one Django template fragment, one
JavaScript file and one stylesheet.

## Existing state the combos rely on

| State | Carrier | Role in this slice |
| --- | --- | --- |
| Selected book translation | hidden `<select name="book_translation">` | remains the posted value; the search field is display only |
| Selected chapter | hidden `<select name="chapter">` | rebuilt by `fillChapters()`; keeps `data-initial` on edit |
| Start verse | hidden `<select name="verse_start">` | rebuilt by `loadVerses()`; keeps `data-initial` on edit |
| End verse | hidden `<select name="verse_end">` | unchanged button picker, refreshed by `syncTo()` |
| Translation edition | `[data-entry-translation-toggle]` `data-edition` | TB/SIM labels and book ids; unchanged |
| Book options | `[data-book]` buttons with `data-book-name-tb/sim`, `data-book-code-tb/sim`, `data-chapters` | the local filter source for Book |
| Chapter / verse options | `[data-picker-option]` with `data-value` | the local filter source for Chapter, From verse and To verse |
| Menu visibility | `.editor__picker-menu[hidden]` | opened/closed by the combos and `closeMenus()` |
| Active option | `.is-active` on a visible option | keyboard cue, now tinted by one shared CSS rule |

**Relationships**: Book → Chapter → From verse → To verse is the existing cascade. The
combos choose an option, set the hidden select and dispatch its `change` event; the existing
listeners reload the next list. **Validation**: server-side, through the unchanged hidden
selects. **State transitions**: none added beyond the menu open/closed and active-option
highlight; those are UI-only.

## Invariants

- The hidden selects, not the search fields, are posted (FR-006, SC-002).
- An option that is `hidden` or `disabled` is never chosen by click, Enter or Arrow keys.
- The Book field's label is always the active edition's name for the selected book.
- Chapter and From verse stay disabled until the preceding list is loaded, as before.
- To verse's "No ending verse" state and hover note are byte-identical (FR-007).
