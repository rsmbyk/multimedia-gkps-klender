# Plan 041: Show TB/SIM book names in the passage modal's book picker

- **Status:** Accepted
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-043
- **Bump:** patch

## Why

The book picker in the passage modal shows only the translation name of each `BookTranslation` row,
unlike the sidebar, which shows the TB name with the SIM name dimmed at the right. Make the picker's
items read the same way.

## Scope / edges

**In:**

- The book picker (add and edit passage) shows each Bible book once, TB as the main label, SIM as the
  dimmed secondary on the right.
- The picker's filter matches either name.
- The stored value stays a `BookTranslation` that resolves chapters and verses.
- Editing an existing passage keeps its saved translation until a book is explicitly chosen; a new choice stores that book's primary translation.

**Out:**

- The chapter / from-verse / to-verse selects.
- The song picker.
- The sidebar itself.

## Approach

- `multimedia/web/reading/entries.py` — rebuild `scripture_books()` from
  `search_lib.bible_book_index()`: one row per `Book`, with `display` (TB), `other` (SIM),
  `testament_label`, `chapters`, and an `id` that is the **primary (TB) `BookTranslation`** so the
  stored FK still resolves.
- `multimedia/web/templates/reading/_entry_form.html` — render the option as two spans
  (`.book__n`-like main, `.book__s`-like secondary) and keep `data-chapters` / `data-book-name`; keep
  the hidden `<select name="book_translation">` consistent (same values, same labels).
- `static/styles/design/components.css` — a two-span layout for the picker option, mirroring
  `.book__n` / `.book__s` (secondary dimmed, pushed to the right).
- `static/web/entries.js` — the picker filter should match on both names (the option's text already
  carries both, so mostly a matter of not filtering on a single attribute).

## TDD

- Domain/app tests: `multimedia/web/tests.py` — `scripture_books()` returns one row per book with
  TB/SIM names and the primary translation id; a book with two translations does not duplicate.
- E2E: `tests/e2e/test_entry_pickers.py` — the option shows both names, TB main and SIM right.

## Risks

- **Stored translation.** Choosing the wrong `BookTranslation` breaks chapter/verse resolution; use
  the primary/TB one the sidebar treats as `display`.
- **Books without a TB verse set.** A SIM-only book may need the translation that actually holds the
  verses; verify against the data.
- **Deduping.** The picker today can list a book twice (once per translation); collapsing to one row
  is a deliberate change.
