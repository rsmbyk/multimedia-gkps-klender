# Plan 044: Add a TB/SIM toggle to the passage modal book picker

- **Status:** Draft
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-046
- **Bump:** patch

## Why

The passage modal offers the Bible books with one translation's names; the operator may want the other
translation. Add the reading page's TB/SIM toggle so the picker can be flipped in place, without
leaving the modal and without a new field.

## Scope / edges

**In:**

- A TB/SIM toggle in the add and edit passage modals, mirroring the reading page's control.
- Toggling swaps the main and secondary names in the book dropdown at once and points the picker at
  that translation's `BookTranslation`.
- The stored `book_translation` is the selected translation's translation.

**Out:**

- A new form field; the existing `book_translation` stores the choice.
- The chapter and verse controls, which do not change with the toggle.
- The song modal and the other editors.

## Approach

- `multimedia/web/templates/reading/_entry_form.html` — add the toggle to the scripture branch,
  reusing the reading page's `.read__lang` markup/`data-edition` shape; the book options need both
  translations' ids and names (spec 041 supplies them).
- `static/web/entries.js` `wireScripture()` — read the toggle state; on change, swap each option's
  main/secondary name and repoint its value at the selected translation's `BookTranslation`, then
  re-letter the trigger label. Keep the filter matching both names (spec 043).
- `static/styles/design/components.css` — the toggle's chrome, reusing the `.read__lang` styles or a
  close variant inside the modal.

## TDD

- Domain/app tests: `multimedia/web/tests.py` — the modal renders the toggle (add and edit); the
  fragment carries both translations' names/ids per book.
- E2E: `tests/e2e/test_entry_pickers.py` — toggling swaps the main and secondary names; the selected
  book stores the switched translation; the chapter / verse controls are unchanged.

## Risks

- **Stored translation.** The picker's value must follow the toggle, or the entry stores the wrong
  translation.
- **Missing verses.** A book/chapter without verses in the switched-to translation needs a defined
  outcome (the open question).
- **Both names everywhere.** The filter (spec 043) and the trigger label must keep working whichever
  side is primary.
