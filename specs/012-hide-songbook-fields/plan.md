# Plan 012: Hide short name and hymn-book fields in the songbook modal

- **Status:** Accepted (owner, 2026-10-06)
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-014
- **Bump:** patch

## Why

The songbook create/edit modal currently exposes `short_name` and `is_hymn_book`. The request is to remove both controls from the songbook form while keeping the modal usable and preserving existing songbook data.

## Scope / edges

**In:**

- Do not render the short-name or hymn-book controls in songbook create and edit forms.
- New songbooks use the model defaults for those fields: blank `short_name` and `is_hymn_book=False`.
- Editing a non-hymn songbook preserves its existing values for both fields, and submitted values for the omitted fields do not change them.
- Keep existing hymn-songbook read-only behavior unchanged.

**Out:**

- Removing or migrating either model field, changing songbook data, or changing other songbook surfaces.
- Changing the read-only rule for hymn songbooks or their songs.
- Changing songbook name/language validation or any other editor form.

## Approach

Limit the `SongbookForm` to the editable fields that remain visible (`name` and `lang`). Let model defaults initialize new records and let an edit's instance retain fields omitted from the form. Add Django tests for create/edit persistence and ignored POST values, plus a Playwright acceptance assertion that reaches the modal through the home page's Kidung navigation and sees neither input.

**To confirm:** for new songbooks, this uses the existing defaults (blank short name and not a hymn book); it does not derive a short name or provide another way to create a hymn book.

## TDD

- Domain/app tests: `multimedia/web/tests.py` (`EditorViewTests`).
- E2E (tool named after stack exists): `tests/e2e/test_editor.py` (`EditorE2ETests`), through the home-to-Kidung modal flow.

## Risks

- Song references may use `short_name`; new songbooks will have no abbreviation unless another workflow supplies one. Existing abbreviations must remain unchanged when editing.
- The hidden hymn-book flag is what distinguishes read-only hymn books. New songbooks will use the non-hymn default, while existing hymn books remain read-only and unchanged.