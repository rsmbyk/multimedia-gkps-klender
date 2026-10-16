# Plan 094: Targeted reading updates

- **Status:** Accepted
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-097
- **Bump:** patch

## Why

The delete POST resolves before `editor:saved` finishes its separate page fetch and DOM update. The confirmation dialog unlocks and closes at the POST response, leaving stale controls usable until the new view arrives. The reading shell also assigns `innerHTML` to the full stage and sidebar lists on navigation or refresh, detaching unchanged nodes and causing a visible flash.

## Scope / edges

**In:** Current and legacy service-entry deletion; the reading shell's server and saved-library in-page navigation/refresh; stage and both sidebar regions; edit-result toast timing; focus, scroll, filter, and reorder continuity.

**Out:** A new visual design, offline edit queuing, projector rendering, admin pages, and changing the service-order data model or write endpoint contract.

## Approach

- Give edit callers a completion signal for the shell's view update. Keep delete confirmation busy after the POST succeeds until the affected reading and sidebar rows have been reconciled. Guard duplicate deletion both in the dialog and in the action handler.
- Reconcile named reading regions against the arriving server or saved-library document. Preserve the live node when its identity and rendered content have not changed; patch, insert, move, or remove only changed elements. Replace a whole region only when its view type genuinely changes. Rebind behavior only where changed nodes require it.
- Keep first-level and second-level sidebars independent of the reading stage. Preserve operator-controlled sidebar open/mini state, filters, scroll, focus, and drag state when a response does not change those controls. Maintain the existing browser history and navigation rules.
- If the delete POST fails, keep the old view and unlock the dialog with the failure toast. If the POST succeeds but the follow-up read fails, remove the accepted entry locally from both visible lists, renumber and restore focus, and report that the latest view could not be verified. Do not present the accepted deletion as a failed write or leave the UI locked indefinitely.

## TDD and verification

- Add focused Playwright tests for a held delete response, a held follow-up read, duplicate activation, readback failure, changed-row updates, unchanged-node identity, and preserved sidebar/focus/scroll state.
- Run the touched reading, entry, reorder, editor-feedback, and offline-library E2E modules locally only as needed for the affected paths; CI performs the broader matrix at the pushed head.

## Risks

- Partial reconciliation must preserve event delegation and rebinding for genuinely new controls, including Tata Ibadah mode/add/reorder controls and Bible translation links.
- A stale response must not overwrite a newer navigation or edit; the completion signal must correspond to the requesting action and current view.
- A successful delete followed by a failed read is a successful write with an unverified view. Its message and local recovery must reflect that distinction.
