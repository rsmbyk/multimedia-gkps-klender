# Spec 071: Scroll Preview text with arrow keys

- **ID:** 071
- **Status:** Accepted
- **Item:** ITEM-074
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** patch

## Intent

Let a reader scroll a long Preview modal with the arrow keys after clicking its text.

## Scope

### In scope

- The shared Preview dialog used by Text, Single-screen Text, passage, and song entries.
- Focus behavior for non-interactive text and preserved focus for interactive controls.
- Native keyboard scrolling of the modal body and existing dismissal behavior.

### Out of scope

- Changes to the Preview's content, break controls, footer layout, or projector.
- A new scroll speed, custom key handler, or page-level keyboard shortcut.
- The separate unified Text-entry and three-way footer-switch proposal.

## Domain rules

- The Preview body is the scroll container and can receive keyboard focus.
- Clicking non-interactive content inside it focuses that scroll container without changing its current scroll position.
- Clicking an interactive descendant keeps focus on that control. Arrow keys keep their normal control behavior where applicable.
- When the Preview body is focused, ArrowDown and ArrowUp scroll it through the browser's native behavior if content overflows. The fixed footer stays in place. At the body edge, the key that cannot move it is canceled so the page behind the dialog does not scroll.
- Escape and backdrop clicks dismiss Preview; focus returns to its opener according to the existing pointer and keyboard restoration rules.

## UI details

The approved behavior preview is recorded in [the plan](./plan.md): a browser-only trial of the current app with focus applied to the scroll body. There is no new visible control.

- **Size / spacing:** Keep the current `min(44rem, 100vw - 32px)` dialog width, `100vh - 48px` maximum height, 22px body padding, and 12px by 22px footer padding.
- **Position / layout:** The Preview body alone scrolls; the footer remains at the bottom of the dialog.
- **Colors / typography:** Retain existing theme tokens, text styles, divider colors, and scrollbar styles. Keyboard focus on the body uses the existing focus token; pointer focus adds no persistent outline.
- **States:** Non-interactive text clicks focus the body. Buttons, tabs, links, and form controls keep their own focus and focus feedback. When content fits, arrow keys do not create extra movement.
- **Responsive behavior:** The behavior works at narrow heights and widths where Preview content overflows; no modal dimension changes.
- **Motion:** Use native browser scrolling while the body can move, with no added animation or timed transition.

## Acceptance scenarios

### Scenario: Scroll a long Preview after clicking text

- **Given** a Preview body taller than its visible area
- **When** a reader clicks a text line and presses ArrowDown
- **Then** the Preview body scroll position increases while its footer remains visible
- **When** the reader presses ArrowUp
- **Then** the Preview body scroll position decreases.

### Scenario: Keep controls usable

- **Given** a Preview with a break button or song tab
- **When** the reader clicks that control
- **Then** it retains focus and its existing pointer and keyboard behavior.

### Scenario: Preserve dismissal and page position

- **Given** the reader has clicked Preview text and scrolled it with arrow keys
- **When** they press Escape or click the backdrop
- **Then** Preview closes and focus returns to its opener
- **And** the page behind the dialog has not moved because of those arrow keys.

### Scenario: Short Preview

- **Given** a Preview body whose content fits
- **When** the reader clicks its text and presses ArrowDown
- **Then** the dialog and the page behind it remain in place.

## Traceability

- Domain/app tests: N/A; no domain or application rule changes.
- E2E: `tests/e2e/test_entry_preview.py`.
- Implementation: `multimedia/web/templates/reading/_preview_modal.html`, `static/web/preview.js`, and Preview focus styles only if needed.
