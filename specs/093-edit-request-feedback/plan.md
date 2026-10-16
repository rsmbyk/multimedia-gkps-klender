# Plan 093: Edit request feedback

- **Status:** Draft
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-096
- **Bump:** minor

## Why

Edit failures currently surface as small red text inside whichever pane or dialog issued the request. A failure can be hidden by another modal, and several actions present inconsistent progress and duplicate-click behavior. Operators need a consistent, visible result without losing an in-progress form.

## Scope / edges

**In:** One shared toast system for public-reading editor requests and service-order writes: songbook/song/Tata Ibadah create and edit, entry and legacy-row create/edit/delete, section-break add, entry reorder, and custom screen-break add/remove/reset or mode save. Include edit-form and edit-dependency load failures. Preserve server field-level validation and existing successful refresh/focus behavior.

**Out:** Offline write queue, retries, public reading/content-fetch status, projector navigation, unrelated server-rendered admin forms, and success toasts for read-only navigation.

## Approach

- Mount one toast host in the public reading shell. Use a nonmodal browser top-layer surface so it can render above native editor/preview dialogs and their backdrops; prove stacking in a browser test. Give each logical action its own handle from start to settle, with an initial 180ms loading delay and a result toast even when the request settles before that delay.
- Adopt the approved [v11 preview](./preview-v11.html): 360px maximum width, bottom/right 20px (12px narrow), new at bottom, quiet border/shadow, no visible stack scrollbar, opacity-only entry, and state color changes. Store settlement time per toast. When visible count reaches four, shorten timers for all settled toasts from their original settlement time; keep pending toasts until settlement.
- Replace generic request-status lines in `editors.js`, `entries.js`, `reorder.js`, and `preview.js` with shared toast calls. Keep field-specific validation next to fields; a 400 response also settles the action toast as a failure summary. Preserve reorder rollback and queue behavior, and custom-break rollback/refresh behavior.
- Make each modal submission a single pending transaction: disable its form controls and all close paths, including Cancel, backdrop, and Esc, until the response settles. For non-modal writes, disable only the initiating button until settlement. Keep independent actions available elsewhere.
- Ensure pending state is cleared in a finalization path for success, validation failure, authorization failure, network failure, malformed response, and unexpected exception. An unavailable toast host must not leave controls locked.

## TDD and verification

- Add focused browser tests in `tests/e2e/test_edit_request_feedback.py` using delayed and failed responses. Cover success/failure, modal and non-modal locks, top-layer stacking, simultaneous toasts and timer compression, reorder rollback, and custom breaks.
- Run targeted Django/E2E tests locally. Full browser matrix and other required checks run in CI at the pushed PR head.

## Risks

- Native `<dialog>` outranks ordinary `z-index`; use and verify a top-layer toast host, including dialogs opened after an existing toast.
- Reorder already queues writes. Keep that behavior while associating each persisted write with the correct toast and never reporting a queued failure as success.
- Server 400 validation fragments are re-rendered. The pending lock must release onto the new fields without discarding their error messages or focus target.
