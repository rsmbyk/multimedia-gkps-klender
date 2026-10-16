# Spec 093: Edit request feedback

- **ID:** 093
- **Status:** Accepted
- **Item:** ITEM-096
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** minor
- **Approved UI preview:** [v11](./preview-v11.html)

## Intent

Every edit action gives the operator one visible, reliable account of its request from pending through outcome. The operator cannot accidentally submit the same write twice or close an in-progress form, and a failed request is visible above all reading UI, including native modal overlays.

## Scope

### In scope

- Create/edit songbooks, songs, and Tata Ibadah; create/edit/delete current service entries and legacy rows; immediate add of section breaks; entry reorder; and custom Text screen-break add/remove/reset and mode saves.
- Loading of an editor form or edit-dependent options when failure currently appears as a generic red request error.
- Shared pending/success/failure toast lifecycle and pending-control locks on the public reading shell.

### Out of scope

- Queuing edits for offline replay; adding retry buttons; general reading, sync, or search notifications; projector HUD notifications; unrelated editor/admin pages.

## Behavior

- Start one toast lifecycle for each logical edit action. Delay showing its pending state by 180ms. If the request settles sooner, show its result directly; do not suppress the result. A visible pending toast stays until its own request settles. A settled toast retains the same position and morphs its mark, accent, title, and supporting text to success or failure; no separate result toast is created.
- Opening an editor or loading dependent picker data is preparatory, not an edit action: show a toast if that load fails, but no success toast when it loads normally.
- Successful completion means the server accepted the mutation and the existing UI refresh/update path was initiated. HTTP failure, rejection, network failure, malformed expected response, and server validation failure are failures. A 400 validation response re-renders field-level errors as before, while the toast gives a concise failure summary. Generic red status text in the issuing view/modal is removed; field-level validation and non-error explanatory notices remain.
- A failure toast uses the action-specific cause when safe and useful (for example, a server-provided custom-break error), otherwise a plain fallback. Do not expose raw response bodies or stack traces. A failed reorder still restores the last confirmed order. A failed custom-break write leaves the previous confirmed breaks/mode intact.
- Every pending modal write sets the dialog busy and prevents form input, resubmission, Cancel/Close, backdrop dismissal, and Esc dismissal until settlement. A validation failure leaves the dialog open and focuses the first invalid field after unlocking. A successful save follows its existing close/refresh behavior. A failed network/server write leaves the form open with entered values intact. Modal open/load requests that fail use a failure toast and do not leave a half-open dialog.
- A non-modal write disables only the action's initiating control while pending; other independent controls remain usable. Repeated activation of that control cannot start a duplicate request. For reorder, preserve its existing keyboard/drag debounce and queued-latest-order behavior; each actual persisted write has one toast and a queued write is reported only after its own response.
- Multiple toasts may coexist. Append new toasts at the bottom and push older ones up. Do not cap the count or hide pending toasts. Constrain the stack to the viewport and keep the newest in view when it overflows; its scrollbar is visually hidden. A toast may be dismissed manually after it settles. Do not allow manual dismissal of pending progress.
- Normally a success result closes 2,000ms after settlement and a failure result after 3,230ms. When four or more toasts are visible, use 1,000ms for success and 1,618ms for failure. On first reaching four visible toasts, update already-settled toasts to the shorter deadline measured from their original settlement times; close any whose shortened deadline has passed. Do not lengthen them if count later drops. Pending toasts remain until settlement.
- Toast display is best-effort presentation; failure to show it must not change the request outcome, lock duration, or existing rollback. Each request clears its pending lock on every settlement path.

## UI details

- Match the [approved v11 preview](./preview-v11.html). Fixed bottom-right overlay: 20px from viewport edges on desktop; 12px on narrow screens (740px and below). Maximum width 360px; minimum available width `viewport - 24px`; 10px vertical gap. Stack maximum height is `viewport - 40px` (or `viewport - 24px` narrow), with overflow scrollable and no visible scrollbar. Above all reading UI, native dialog/backdrop, and popovers.
- Each toast uses a 10px radius, 1px theme-divider border, 3px left state accent, theme canvas/background and ink, 13px top/bottom and 12–14px side padding, 11px mark-to-copy gap, and a quiet `0 1px 2px` shadow at about 9% black opacity. Loading accent is muted amber, success green, failure `--danger`; marks have a pale matching tint. Text: 14px semibold title, 12.5px supporting text, 18px mark. Use theme tokens or equivalent dark-theme values so contrast remains legible.
- A visible pending toast has a small 0.8s spinner. On settlement, the accent/mark color changes over 180ms and copy updates in place. A toast enters/exits with a 140ms opacity fade only, without position or scale motion. Reduced-motion users get no fades or spinner rotation. The stack reflows naturally as items enter/leave.
- A settled toast has a 24×24px dismiss button at top-right with hover fill and 2px focus outline. Pending toasts do not expose a dismiss action. Use a suitable live region for result announcements without causing every spinner frame to be announced; give each action an accessible status name. Busy modal controls expose disabled/busy state. Do not shift dialog layout when controls lock.

## Acceptance scenarios

### Fast and slow writes

- **Given** an edit action completes before 180ms, **when** its response arrives, **then** the single toast appears directly as the correct result and closes on its result timer.
- **Given** a slow edit action, **when** it starts and then settles, **then** one pending toast appears after 180ms, stays for the rest of the request, morphs into the outcome, and closes on the correct timer.

### Simultaneous actions and crowding

- **Given** several independent edit actions, **when** they run together, **then** each has its own bottom-appended toast and none of the pending toasts is discarded.
- **Given** four visible toasts, **when** the fourth appears, **then** already-settled toasts switch to the short deadline from their settlement time; pending ones stay, and subsequent results use the short timer while the count remains at least four.

### Modal and non-modal guard

- **Given** a modal form is submitting, **when** the operator edits a field, submits again, clicks Close/backdrop, or presses Esc, **then** the form and dialog remain unchanged until settlement. After failure they are editable/closable again; after success the existing close/refresh behavior runs.
- **Given** a non-modal delete or add control is submitting, **when** clicked again, **then** it sends no duplicate request; other independent controls remain operable and the original control unlocks after settlement.

### Error surfaces and rollback

- **Given** an editor 400 response, **when** validation returns, **then** field errors and invalid-field focus remain, the generic red request status is absent, and the action toast reports failure.
- **Given** a reorder or custom-break write fails, **when** the request settles, **then** its failure toast appears above any open modal/overlay and the last confirmed order or breaks are preserved.
- **Given** an editor or edit-option load fails, **when** the request settles, **then** a failure toast appears and no form is left busy or half-open.

## Traceability

- **Domain/app tests:** none; this is browser-side request/UI coordination.
- **E2E:** `tests/e2e/test_edit_request_feedback.py`.
- **Implementation:** shared toast module, reading-shell template/styles, `static/web/editors.js`, `entries.js`, `reorder.js`, `preview.js`.
