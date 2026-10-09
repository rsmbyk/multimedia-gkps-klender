# Plan 044: Add a TB/SIM toggle to the passage modal book picker

- **Status:** Accepted
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
- Each book option carries both translations' IDs and names. A new passage starts on TB; an edit or
  validation re-render reflects the form's currently selected `BookTranslation`.
- When neither TB nor SIM exists for a book, retain its existing primary fallback on the default side.
- Toggling swaps the main and secondary names and updates the selected book's hidden
  `book_translation` value to the same book in the active translation.
- The two-name filter continues matching either name in both toggle states (the behavior is already
  implemented by spec 041; spec 043 was superseded by spec 041).
- Toggling does not reload or change the chapter/verse controls or their current values. Picking a
  different book continues to use the existing cascade for the active translation.

**Out:**

- A new form field; the existing `book_translation` stores the choice.
- Re-fetching chapter/verse options solely because the toggle changed.
- The song modal and the other editors.

## Approach

- `multimedia/web/reading/entries.py` — expose explicit TB/SIM IDs and names per book while retaining
  the current selected translation for edit/error forms.
- `multimedia/web/templates/reading/_entry_form.html` — add the toggle to the scripture branch,
  reusing the reading page's `.read__lang` markup/`data-edition` shape; include both translations in
  the hidden select and both names in each picker option.
- `static/web/entries.js` `wireScripture()` — initialize from the stored translation (TB for a new
  form); on change, swap each option's main/secondary name and update the selected book's value, but
  leave chapter/verse controls and values untouched. Keep the filter matching both names.
- `static/styles/design/components.css` — style the toggle using the reading page's `.read__lang`
  treatment inside the modal.

## TDD

- Domain/app tests: `multimedia/web/tests.py` — both add and edit fragments expose both translation
  IDs/names; add defaults to TB and an existing SIM selection remains SIM.
- E2E: `tests/e2e/test_entry_pickers.py` — toggling swaps names and the selected book's stored ID;
  chapter/verse values and options remain unchanged during the toggle; selecting another book follows
  the active edition; a book with neither TB nor SIM keeps its existing primary fallback selectable.

## Risks

- **Stored translation.** The edit/error form's active side must follow its selected
  `BookTranslation`, or it can silently save the other edition.
- **Verse lists.** The accepted behavior is to preserve the current chapter/verse controls on a toggle;
  selecting another book uses the existing translation-specific cascade, including its empty state.
- **Both names everywhere.** The filter must continue searching both names even though their visual
  positions swap.
