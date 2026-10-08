# Plan 015: Remove first-section and active controls from Tata Ibadah forms

- **Status:** Accepted (owner, 2026-10-07)
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-017
- **Bump:** patch

## Why

The sidebar create form should create an empty Tata Ibadah, and neither create nor edit should expose activation management.

## Scope / edges

**In:** Remove the first-section title/text fields from create; remove `is_active` from create/edit; preserve the model's active default and existing edit state.

**Out:** Removing `is_active` from model, API, admin, or list filters; changing how empty services are filled; changing date controls or header presentation.

## Approach

Keep the form to name and date. Remove the first-section `ModelForm` fields and the `save_form` code that creates a legacy item from them. Excluding `is_active` from the edit form preserves the instance value; new records use the model default. Add endpoint tests for create defaults, absence/ignored POST fields, and editing inactive services; add focused E2E form assertions.

## TDD

- Domain/app tests: `multimedia/web/tests.py` (`EditorViewTests`).
- E2E: `tests/e2e/test_editor.py` (`EditorE2ETests`).

## Risks

An empty active service must remain listed and fillable through the existing service-entry editor; verify that path remains unchanged.
