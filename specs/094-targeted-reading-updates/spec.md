# Spec 094: Targeted reading updates

- **ID:** 094
- **Status:** Accepted
- **Item:** ITEM-097
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** patch

## Intent

An accepted service-entry deletion should remain one pending action until the operator sees the updated order. In-page reading updates should preserve unchanged components so the page does not flash, lose focus, or reset sidebars.

## Scope

### In scope

- Deleting current service entries and legacy service rows from the public reading page.
- Reconciling the reading stage, first-level list, second-level list, and their dependent toolbar controls during in-page navigation, edit refresh, saved-library rendering, and server refresh.
- Maintaining the existing toast, dialog, navigation, filter, focus, scroll, and reorder behavior while those updates complete.

### Out of scope

- New notification styling, new loading overlays, offline edit replay, projector-page DOM updates, and changes to unrelated admin screens.

## Behavior

- Treat delete as one action from its first activation through the visible view update. The confirmation button is disabled synchronously before the POST begins; later clicks, Enter presses, or repeated handler calls cannot send a second POST. The dialog remains open and busy after an accepted POST while its view update is in progress. Its controls, Cancel, Esc, and backdrop cannot dismiss it during that interval, so stale page editing and reordering remain inaccessible.
- On accepted POST and completed view update, remove the deleted row from the reading pane and second-level service list, update affected numbering and adjacent add controls, restore focus to the nearest surviving item as the current behavior intends, close the dialog, and settle the action toast as success. Do not settle it when merely starting the follow-up read.
- On POST failure, keep the old view, leave entered state intact, unlock the confirmation, and settle the toast as a failed deletion.
- On accepted POST followed by a failed read, apply the deletion locally to the visible stage and service list, update numbering and focus, then unlock/close the dialog. Give a truthful settled warning that the deletion succeeded but the latest server view could not be verified. Do not send the delete request again automatically.
- An in-page update compares incoming and live components by stable identity. Reuse nodes whose content and relevant attributes are unchanged. Patch only changed stage sections, entry/song/book/chapter/sidebar rows, toolbar controls, and metadata; insert or remove nodes for additions/deletions; move existing nodes for order changes. A change of page/view type may replace that changed view's root, but must not rebuild unrelated sidebars or the main rail.
- Preserve live filter text, sidebar open/mini states, scroll offsets, focus, selection, and active drag/reorder state whenever their owning component is unchanged. When the selected content itself changes, keep the current navigation and focus rules. Server-rendered and saved-library documents use the same reconciliation path; newer navigation/edit responses take precedence over older in-flight reads.
- The existing result toast timing, colors, typography, position, and disabled-control appearance from Spec 093 remain the visual source of truth. No new overlay or spacing is introduced. A pending delete toast remains pending through the view update; an accepted delete with readback failure uses the existing failure/warning presentation with explicit success-of-write wording.

## Acceptance scenarios

### Delete stays pending through the visible update

- **Given** a service-entry delete POST and its follow-up read are delayed independently, **when** the operator activates Delete repeatedly or attempts to close the confirmation, edit another entry, or reorder, **then** exactly one delete POST is sent, the confirmation stays busy, and no stale action runs until both the POST and view reconciliation complete.
- **Given** the server accepts a deletion, **when** the follow-up view update completes, **then** the deleted row is absent in the reading pane and service sidebar before the dialog closes and the single toast changes to success.
- **Given** the delete POST fails, **when** it settles, **then** the old rows remain, the dialog unlocks, and the toast reports a failed deletion.
- **Given** the POST succeeds but the follow-up read fails, **when** the local deletion is applied, **then** both visible lists and numbering agree, focus lands on a surviving target, the dialog unlocks, and the toast says the deletion succeeded but the latest view could not be verified.

### Targeted page and sidebar updates

- **Given** a response whose first-level list is unchanged, **when** a chapter, song, or service content changes, **then** existing first-level row nodes remain mounted and its filter, scroll, focus, and sidebar state remain intact.
- **Given** one service entry changes or is deleted, **when** the reading refresh arrives, **then** only affected stage and service-list nodes change; unaffected row nodes and the main rail remain mounted, with no full-stage or full-list flash.
- **Given** a section, mode, or route changes the actual sidebar contents, **when** the update arrives, **then** the relevant rows and toolbar controls change while unrelated stage/sidebar components keep their current nodes and behavior.
- **Given** a saved-library view later receives a newer server response, **when** that response is applied, **then** changed content updates through the same targeted path without restoring stale data or discarding in-tab sidebar state.

## Traceability

- **Domain/app tests:** existing delete/reorder endpoint tests in `multimedia/web/tests.py` if the endpoint contract needs adjustment.
- **E2E:** `tests/e2e/test_targeted_reading_updates.py`, plus focused regressions in `tests/e2e/test_reading.py`, `test_entries.py`, `test_reorder.py`, `test_edit_request_feedback.py`, and `test_offline_library.py`.
- **Implementation:** `static/web/reading.js`, `entries.js`, and any small shared reconciliation/feedback helper needed by the accepted behavior.
