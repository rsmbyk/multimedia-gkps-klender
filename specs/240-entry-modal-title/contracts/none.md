# Contracts: none

**Spec**: `specs/240-entry-modal-title/spec.md`

No external interface is added or changed. No endpoint, request/response shape, model
field, event name, stored format or script API is touched. Interfaces read but not
changed by the verification:

- `_entry_form.html`'s `#editorTitle` and `[data-editor-size="large"]` (read only);
- the fetched entry-form route used by `+ Text`, a text row's Edit and `+ Media` (read only);
- `tests/e2e/test_entry_modal_frame.py` and `tests/e2e/test_verse_modal_header.py`
  measurement scripts (read only).
