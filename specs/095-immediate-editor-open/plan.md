# Plan 095: Immediate editor opening during form loads

- **Status:** Accepted
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Approved preview:** [./preview.html](./preview.html) (loading spinner above the text, centered together)
- **Item:** ITEM-098
- **Bump:** patch

## Why

Sidebar and service-entry Add/Edit controls fetch form HTML before opening their shared modal. On a slow connection, repeated clicks can start several requests and make the control appear unresponsive. Responses that arrive after the modal is closed can reopen it or replace a newer form.

## Scope / edges

**In:** Public-reading Add/Edit form loading for songbooks, songs, Tata Ibadah, current service entries, and legacy rows; slow, failed, and offline reads; cancellation and stale-response handling; focus; and the existing load-failure toast.

**Out:** Delete confirmation and write requests, edit-option requests made inside an already-open form, offline edit queuing, unrelated admin editors, and new toast styling.

## Approach

- Open the existing editor modal on the initiating click and render a centered loading state immediately. The approved preview puts the 18px spinner on its own row above the 14px “Loading editor…” label, with 10px between them. Keep Cancel in the modal and support Esc and backdrop dismissal.
- Coordinate the sidebar and service-entry editor paths through one active-load identity. Ignore repeated opens while a load is active. When the user closes the loading modal, abort the request when supported and always invalidate its identity so its response cannot reopen or alter another editor.
- On success, replace the loading content in the same modal and focus the first usable form control. On failure, close the loading modal and use the existing “Could not load editor” toast. A canceled/stale request produces no failure toast. A new click after closure or failure can retry.
- Preserve the loaded form's existing save behavior.

## TDD

- Domain/app tests: none; this is browser-side request and modal coordination.
- E2E: add focused coverage in `tests/e2e/test_immediate_editor_open.py` for sidebar and service-entry editors, held responses, dismissal, stale responses, failure, retry, and focus.

## Risks

- Sidebar and service-entry modules currently initiate loads independently while sharing editor UI. A common identity must prevent either response from replacing the other's active form.
- Cancellation and request failure both need to release loading state, but only a real active-load failure should show the existing toast.
