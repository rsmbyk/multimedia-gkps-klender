# Plan 079: One Text entry with a selectable default screen mode

- **Status:** Accepted
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-082
- **Bump:** minor

## Why

Tata Ibadah stores Multi-line Text and Single-screen Text as different entry kinds even though both have the same title, body, editing form, Preview rows, and manual break controls. The kind currently decides only the default projection. The owner asked for one Text entry, a default screen-mode choice on creation, and a three-state switch in Preview so the result is visible while changing it. PR #323 delivered manual breaks for both existing kinds, but did not deliver this consolidation.

The previously shown [Create/Edit form preview](./preview-form-light.png) and [light](./preview-footer-light.png) and [dark](./preview-footer-dark.png) Preview footer mockups are the visual reference. The last form revision keeps the two-way choice on Create and removes it from Edit.

## Scope / edges

**In:**

- One active Text entry kind with a stored default mode: Multi-line or Single-screen. Custom is derived from saved break positions, not a third stored default.
- Migrate existing Text and Single-screen Text rows to that one kind without losing their order, content, mode, custom breaks, or projector behavior.
- Keep one Add Text action. The Create modal has the icon-labeled two-way mode switch; the Edit modal has Title and Text only.
- Replace Reset breaks and the mode badge in Preview with the three-state footer switch. Choose either default there and confirm before discarding a custom arrangement.
- Preserve the current break-line interaction, live projector refresh, keyboard scrolling, and read-only Preview behavior for viewers.

**Out:**

- Songs, Scripture, section breaks, legacy TataIbadahItem rows, and old OBS docks and web sources.
- Text rewriting, song verse grouping, and changing the existing default line-pair or single-screen fitting algorithms.

## Approach

Add a default screen-mode field to ServiceEntry. In a data migration, set Single-screen for former kind 4 rows and Multi-line for former kind 0 rows, then normalize both to the Text kind. Leave custom break arrays intact. Update validation, the form/URL mapping, Preview payload, screen-break endpoint, and projector grouping to use the new field. Existing rows must produce the same screens before and after migration.

Keep the existing two gap-click algorithms: first Multi-line custom action uses its two-line cadence (or removes one default break), while first Single-screen custom action adds only the selected boundary. Later actions toggle only one boundary. The middle Custom segment is status only. Clicking a default while Custom opens the in-app confirmation shown in the preview; confirmation clears breaks and saves the chosen default atomically. A canceled or failed save keeps the custom state. Switching between defaults saves immediately, without confirmation.

Use the current editor-saved event to refresh the page and any open projector after a successful change. Reject stale Preview writes when the text or current mode/break state changed in another editor.

## TDD

- Domain/app tests: multimedia/tatib/tests.py for model validation and migration; multimedia/web/tests.py for Create/Edit, mode writes, break rules, and unchanged projector output.
- E2E: tests/e2e/test_unified_text_screen_mode.py for the Create switch, Preview footer states, confirmation/cancel, single-screen first break, keyboard access, and live projector refresh.

## Risks

- Existing kind 4 rows must migrate to Text without changing their IDs or custom break semantics.
- The Single-screen boundary rule permits breaks across blank paragraph rows; Multi-line does not. Validation must follow the saved default mode.
- A stale Preview must not overwrite a newer mode or break change.
