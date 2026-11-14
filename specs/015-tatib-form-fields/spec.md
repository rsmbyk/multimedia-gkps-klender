# Spec 015: Remove first-section and active controls from Tata Ibadah forms

- **ID:** 015
- **Status:** Accepted (owner, 2026-10-07)
- **Item:** ITEM-017
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** patch

## Intent

Simplify Tata Ibadah create/edit forms by removing the initial legacy-section inputs and activation control without changing activation behavior.

## Scope

### In scope

- Remove first-section title and text from the create form.
- Remove `is_active` from both create and edit forms.
- Ignore handcrafted POST values for omitted fields.
- Preserve the model's active default on create and the existing active value on edit.

### Out of scope

- Removing `is_active` from the model, database, API, admin, or public list filters.
- Changing service entry creation, date controls, or Tata Ibadah page presentation.

## Domain rules

- The Tata Ibadah sidebar form exposes only the model's name and date fields.
- No `first_title`, `first_text`, or `is_active` input is rendered, including hidden inputs.
- Extra POST values for omitted fields do not affect saved records.
- A new service uses `is_active=True` from the model default; edits retain their prior `is_active` value.
- Creating a service creates no legacy `TataIbadahItem`. Empty active services remain visible and can be populated by the existing service-entry controls.

## Acceptance scenarios

### Scenario: Create an empty service

- **Given** I open the Tata Ibadah create modal
- **Then** the form has no first-section or active field
- **When** I save a name and optional date, even if the request includes handcrafted first-section and active values
- **Then** an active service is created with no legacy item and is available in the Tata Ibadah list

### Scenario: Edit preserves activation

- **Given** an existing active or inactive Tata Ibadah
- **When** I edit its name or date, including a handcrafted `is_active` value
- **Then** the form has no active field and the stored activation value is unchanged

### Scenario: Fill an empty service

- **Given** a newly created empty active service
- **When** I open it and use the existing service-entry controls
- **Then** I can add its first entry without creating a legacy first section

## Traceability

- Domain/app tests: `multimedia/web/tests.py` (`EditorViewTests`).
- E2E: `tests/e2e/test_editor.py` (`EditorE2ETests`).
- Implementation: `multimedia/web/reading/editors.py` and focused service-create tests/fixtures.
