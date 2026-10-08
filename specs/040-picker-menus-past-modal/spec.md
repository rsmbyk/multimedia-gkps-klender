# Spec 040: Let the entry modal picker menus extend past the modal

- **ID:** 040
- **Status:** Draft
- **Item:** ITEM-042
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** patch

## Intent

The book and song dropdowns in the entry modals should be able to overlap the dialog's edge, capped
to the viewport, instead of being clipped inside the dialog's scroll area.

## Scope

### In scope

- The book picker (passage) and song picker (song) menus in the add and edit entry modals.
- A menu that overlaps the dialog, never leaves the window, flips up/down for room, and scrolls its
  options.

### Out of scope

- Native selects, the verses picker (unless extended), the date picker, other modals, the projector.

## Domain rules

- **Out of the dialog.** A picker menu may extend past the dialog's edge; it is capped to the
  viewport, not the dialog.
- **Always reachable.** The menu never leaves the window; when there is no room below, it flips above
  the trigger.
- **Options scroll.** The menu's options scroll within the available room.
- **Anchored.** The menu is positioned against its trigger and stays there while the dialog is used.
- **Add and edit alike.** Both the add and edit modals behave the same.

## Acceptance scenarios

### Scenario: A menu at the dialog edge

- **Given** the passage modal with the book picker near the dialog's bottom edge
- **When** I open the picker
- **Then** the menu extends past the dialog's edge and stays inside the window

### Scenario: No room below

- **Given** a picker with no room below it
- **When** I open it
- **Then** the menu opens above the trigger and its options scroll

### Scenario: The song picker

- **Given** the song modal
- **Then** the song picker behaves as the book picker does

### Scenario: Edit counterparts

- **Given** the edit passage and edit song modals
- **Then** their pickers behave the same as the add modals

## Traceability

- Domain/app tests: N/A (client behaviour; fragment markup unchanged).
- E2E: `tests/e2e/test_entry_pickers.py`.
- Implementation: `static/web/entries.js`, `static/styles/design/components.css`.
- Related: spec 022 (the date picker over the modal).
