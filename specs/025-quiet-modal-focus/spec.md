# Spec 025: Avoid automatic row outlines after modal close

- **ID:** 025
- **Status:** Accepted
- **Item:** ITEM-027
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** patch

## Intent

Closing or saving an editor must not leave a created/edited item outlined solely because focus was automatically restored. Keyboard navigation must still have a visible focus indicator.

## Scope

### In scope

- Songbook, song, and Tata Ibadah create/edit modals in the reading shell.
- Service-entry create/edit/delete and legacy-item edit/delete modal paths.
- Audit any unsaved-order confirmation for the same outline or stale-action symptom. Spec 026 removes that dialog entirely; only the remaining modal paths need focus restoration.
- Focus restoration after cancellation and asynchronous post-save DOM replacement.
- Normal keyboard focus in the Alkitab, songbook, song, Tata Ibadah, and contents sidebars must remain unaffected.

### Out of scope

- Blanket outline removal, intentionally discarding DOM focus, or hidden focus sinks.
- Changing the selected-row fill, genuine hover behavior, date-picker focus indicators, forms, permissions, reorder semantics, or legacy admin/Fomantic pages.

## Domain rules

- Automatic focus restoration after closing/saving a modal does not draw an outline on the item, edit action, or restored opener.
- Focus remains on a predictable visible target: a sidebar row's primary link, the corresponding surviving pane control, or the nearest sensible surviving control after a save/delete.
- Tab/Shift+Tab or other deliberate keyboard navigation restores normal visible focus immediately; no permanent marker suppresses it.
- An idle row edit action is not revealed just because a modal or refresh restored focus.
- Post-save row lookup distinguishes record kind as well as ID and does not confuse a sidebar record with a service entry/legacy item sharing the same ID.
- These rules refine Spec 014: automatic close/save restoration is now visually quiet, while intentional keyboard focus and reachability remain required.

## Acceptance scenarios

### Scenario: Keyboard closes sidebar create/edit modals

- **Given** I start at home and open a songbook, song, or Tata Ibadah create/edit modal
- **When** I cancel with Escape or press Enter on Cancel
- **Then** the modal closes without leaving a restored row/opener outlined
- **And** its sidebar stays open and idle row actions stay hidden when not hovered
- **And** focus remains usable at a predictable target

### Scenario: Saving does not reintroduce outlines after refresh

- **Given** I create or edit a songbook, song, or Tata Ibadah in the home shell
- **When** I save using Enter on a supported form or the Save button
- **Then** the record is saved and its lists/stage refresh in place
- **And** the intended surviving primary row/control is used, not an edit action or a different-kind record with the same ID
- **And** the settled refresh leaves no automatic outline or idle edit action
- **And** the saved row remains discoverable through the existing reveal/flash behavior

### Scenario: Deliberate keyboard focus remains visible

- **Given** a modal has just closed with visually quiet focus restoration
- **When** I use Tab/Shift+Tab or normal keyboard navigation through the sidebars
- **Then** the reached control has its normal visible focus indicator
- **And** returning to the original item by keyboard also shows normal focus
- **And** keyboard users can still open/edit the item without using a pointer

### Scenario: Other reading-shell modals do not strand outlines or controls

- **Given** I open a service-entry editor, legacy-item editor, or delete confirmation
- **When** I close through its supported Escape, Enter, or pointer action
- **Then** automatic restoration leaves no unwanted outline or unrelated revealed row action
- **And** supported saves/deletes keep a usable surviving focus target
- **And** genuine hover controls and deliberate keyboard focus still work

Spec 026 removes the unsaved-order confirmation altogether; after a reorder there is no modal to close and no pending focus restoration.

## Traceability

- Isolated view tests (passed 2026-10-08): `EditorViewTests.test_new_song_form_carries_its_songbook_id_to_save` and `EditorViewTests.test_create_songbook_ignores_hidden_metadata_and_forged_language` cover the supporting save payload/response.
- Focus E2E (passed 2026-10-08): sidebar create/edit saves across songbooks, songs, and Tata Ibadah; Escape/Enter cancellation; quiet restored outlines with normal Tab focus; pointer close; date-picker keyboard and validation-rerender behavior; service-entry create/edit/cancel/delete; legacy-item save/cancel/delete. Coverage is in `tests/e2e/test_editor.py`, `tests/e2e/test_entries.py`, and `tests/e2e/test_old_rows.py`.
- The unsaved-order modal is absent from the current worktree: reordering now writes immediately under accepted Spec 026. Its old modal-close path is not applicable; the current direct-save/no-prompt behavior is covered by `test_an_arrow_move_is_written_at_once` and `test_leaving_for_another_tata_ibadah_does_not_ask_and_keeps_the_order`.
- Implementation: `static/web/focus.js`, `static/web/editors.js`, `static/web/reading.js`, `static/web/entries.js`, `static/styles/design/components.css`, `multimedia/web/templates/reading/base.html`, `multimedia/web/templates/reading/tatib.html`, `multimedia/web/templates/reading/_editor_form.html`, and `multimedia/web/reading/views.py`.
- Full browser suite remains deferred to push; no production data was used for save-path tests.
