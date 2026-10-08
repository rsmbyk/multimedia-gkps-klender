# Spec 014: Clear stale row-edit visibility after modal close

- **ID:** 014
- **Status:** Accepted (owner, 2026-10-07)
- **Item:** ITEM-016
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** patch

## Intent

A pointer-driven close of a create/edit modal must not leave a sidebar or pane row's edit action visibly stuck when the pointer is elsewhere. Keyboard focus indicators remain available to keyboard users.

## Scope

### In scope

- Focus restoration and revealed row controls after create/edit modal cancellation, save, Escape, and backdrop close.
- The shared shell's sidebar row actions for songbooks, songs, and Tata Ibadah, plus service-entry and legacy-item actions in the content pane.
- Audit other modal close paths in the reading shell for the same stale-hover/focus symptom.

### Out of scope

- Changing hover affordances, row-control eligibility, modal designs, form behavior, or permissions.
- Removing focus-visible indicators or changing reorder behavior.

## Domain rules

- A row edit action is revealed while its row is actually hovered, or while the action is keyboard-focused with `:focus-visible`.
- Pointer-driven modal close/save does not leave the row action visible solely because focus was programmatically restored or because a refreshed row inherited focus.
- Keyboard users retain an intentional, visible focus target after modal close/save and can continue through the row controls with Tab/Shift+Tab.
- The same rule applies across sidebar and content-pane modal families; a specific modal must not require a one-off CSS exception.

## Acceptance scenarios

### Scenario: Pointer closes an edit modal with the pointer away from the row

- **Given** a song, songbook, or Tata Ibadah row edit action opened its modal by pointer
- **When** I close it with Cancel, Escape, the backdrop, or Save while the pointer is outside that row
- **Then** the row edit action is not visible after the modal closes and its refresh settles
- **And** it becomes visible again when I genuinely hover the row

### Scenario: Keyboard close preserves keyboard operation

- **Given** I open a row editor using the keyboard
- **When** I close it with Escape or Enter
- **Then** focus returns to the row's primary link, not its edit action
- **And** the edit action is not left visible just because it was the modal trigger
- **And** Tab and Shift+Tab continue to reach the row action with a visible focus indicator

### Scenario: Other reading modals do not strand row actions

- **Given** a service-entry editor, legacy-item editor, or unsaved-order confirmation is open
- **When** I close it through its supported pointer or keyboard path
- **Then** no unrelated sidebar or pane row action remains visibly revealed without hover or keyboard focus

### Scenario: Idle sidebars remain idle

- **Given** I close a sidebar or move away from a list row after modal close
- **When** no row is hovered or keyboard-focused
- **Then** songbook, song, and Tata Ibadah edit controls have computed opacity 0 and do not intercept pointer input

## Traceability

- E2E: `tests/e2e/test_editor.py` (songbook/song/Tata Ibadah), `tests/e2e/test_entries.py`, `tests/e2e/test_old_rows.py`, and `tests/e2e/test_projector.py` (shared sidebar behavior where suitable).
- Implementation: `static/web/editors.js`, `static/web/reading.js`, relevant delegated modal scripts, and `static/styles/design/components.css` after root-cause confirmation.
