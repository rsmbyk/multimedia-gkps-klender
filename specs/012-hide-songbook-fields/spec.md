# Spec: Hide short name and hymn-book fields in songbook forms

- **ID:** 012
- **Status:** Accepted (owner, 2026-10-06)
- **Item:** ITEM-014
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** patch

## Intent

Simplify the songbook create/edit form by removing the short-name and hymn-book controls while keeping existing songbook data intact.

## Scope

### In scope

- Omit `short_name` and `is_hymn_book` from the songbook form in both create and edit flows; they are absent from the rendered form, not CSS-hidden or rendered as hidden inputs.
- Keep existing stored values when editing a non-hymn songbook, even if a request manually supplies values for the omitted fields.
- New songbooks use the model defaults for omitted fields: blank `short_name` and `is_hymn_book=False`.
- Preserve all other form fields, validation, and the existing read-only rule for hymn songbooks and their songs.

### Out of scope

- Removing or migrating the model fields, changing stored songbook data, or changing other displays or APIs.
- Adding another way to set a short name or create a hymn book.
- Changing which songbooks or songs are editable.

## Domain rules

- The form does not accept user edits to `short_name` or `is_hymn_book`.
- Excluding these fields from the edit form must not clear or overwrite their existing database values.
- A new songbook has no abbreviation and is not a hymn book unless another workflow changes those values.

## Acceptance scenarios

### Scenario: Create a songbook without the two controls

- **Given** I open the songbook create modal
- **When** the form is shown
- **Then** there is no short-name or hymn-book field, including no hidden input for either
- **And** saving the remaining valid fields creates a songbook with a blank short name and `is_hymn_book=False`

### Scenario: Edit a songbook without changing its hidden values

- **Given** a non-hymn songbook has an existing short name
- **When** I open its edit modal
- **Then** there is no short-name or hymn-book field, including no hidden input for either
- **And** saving a change to its visible fields preserves its existing short name and hymn flag

### Scenario: Omitted fields cannot be changed by a handcrafted submission

- **Given** I submit the songbook form with extra `short_name` or `is_hymn_book` values
- **When** a new songbook is created or a non-hymn songbook is updated
- **Then** those extra values are ignored and the defaults or existing stored values remain unchanged

### Scenario: Hymn songbooks remain read-only

- **Given** a songbook is marked as a hymn book
- **When** I try to open its edit form
- **Then** the existing read-only response remains in effect

## Traceability

- Domain/app tests: `multimedia/web/tests.py` (`EditorViewTests`).
- E2E: `tests/e2e/test_editor.py` (`EditorE2ETests`), covering create and edit modals from the public reading flow.
- Implementation: `multimedia/web/reading/editors.py` (`SongbookForm`); the shared form fragment `multimedia/web/templates/reading/_editor_form.html` renders only fields declared by the form.
