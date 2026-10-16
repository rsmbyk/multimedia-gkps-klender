# Tasks 093: Edit request feedback

- **Status:** Accepted
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

## Checklist

- [x] Owner accepted this Draft; update plan/spec/tasks and ITEM statuses.
- [x] Add focused browser tests for toast lifecycle, timing/crowding, native-dialog layering, and form/non-modal pending guards in `tests/e2e/test_edit_request_feedback.py` (red).
- [x] Implement shared top-layer toast host/API and approved styles in the reading shell and `static/styles/design/components.css`; verify light/dark and reduced motion.
- [x] Route songbook/song/Tata Ibadah and service-entry form load/save/delete outcomes through the toast API. Keep 400 field errors and focus, block modal dismissal/edit while pending, and finalize locks on every response path.
- [x] Route non-modal break creation, reorder persistence, and custom-break add/remove/reset/mode writes through the same API. Preserve reorder queue/rollback and previously confirmed break state; lock only the initiating non-modal control.
- [x] Run focused browser/Django tests, inspect the real modal/overlay stacking, and update traceability.
- [x] Push a separate draft PR for Spec 093 after acceptance and required metadata/version updates.
- [x] Before merge, set ITEM Done, complete this checklist and the release metadata in that PR; verify required CI at its exact head.

## Done when

- [x] Every acceptance scenario in `spec.md` passes.
- [x] No generic red edit-request status remains in the covered views; field validation still identifies the bad input.
- [x] Toasts remain visible above native dialogs and all pending controls release correctly after every outcome.
