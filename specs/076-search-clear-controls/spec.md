# Spec 076: Make reading search clear controls consistent

- **ID:** 076
- **Status:** Accepted
- **Item:** ITEM-079
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** patch

## Intent

Give every existing reading-shell search/filter clear button the same slightly larger, centered cross.

## Scope

### In scope

- Home search field, first-sidebar `bookFilter`, and second-sidebar `songFilter` in the new reading UI.
- Light, dark, system-selected, focused, hovered, empty, and filled states.

### Out of scope

- Picker search fields that currently have no separate clear control, date clearing, and legacy UI.

## Domain rules

- A clear button appears only while its field has text. Activating it empties the field, reapplies that field's current filter/search behavior, and returns focus to the field.
- The clear button retains its accessible, field-specific label. The native browser search cancel decoration remains suppressed so only one cross is shown.

## UI details

- **Approved preview:** [Sidebar follow-ups interactive preview](../072-sidebar-idle-collapse/preview.html), search/filter fields in the Tata Ibadah and menu-switch scenarios.
- **Size / spacing:** Every clear button has a 26 × 26px circular hit area; the centered cross SVG is 14 × 14px with its current 1.8px stroke. Keep an 8px right inset inside sidebar fields and the current 58px home-search offset from the right edge to leave room for Search. Increase input right padding as needed so typed text never sits beneath the button.
- **Position / layout:** Vertically center the button in its own field. No field height change.
- **Colors / typography:** Resting icon uses `--head-ink`; hover uses `--ink` on `--icon-hover-bg`; focus outline uses `--focus`.
- **States:** Empty fields hide the button entirely. Hover and focus backgrounds are circular and aligned across all three fields. No extra visible label.
- **Responsive behavior:** Keep the same 26px geometry on narrow screens and preserve the home Search button's own hit area.
- **Motion:** Existing color transition only.

## Acceptance scenarios

### Scenario: Three matching clear controls

- **Given** text in the home search and each of the two sidebar filters
- **When** each clear button is shown
- **Then** all three use equal 26 × 26px circles with centered 14 × 14px crosses and no text overlap.

### Scenario: Clearing

- **Given** a nonempty filter
- **When** the operator activates its clear button with pointer or keyboard
- **Then** the value becomes empty, the unfiltered results return, the button hides, and focus returns to that field.

### Scenario: Themes and narrow width

- **Given** light, dark, or system appearance and a narrow viewport
- **When** a clear button is hovered or focused
- **Then** its icon, circular background, and focus outline remain visible and aligned without overlapping the Search submit action.

## Traceability

- Domain/app tests: N/A.
- E2E: `tests/e2e/test_reading.py` checks shared geometry, input clearance, pointer and keyboard clearing, and focus return.
- Implementation: `static/styles/design/components.css`; existing markup and behavior in `multimedia/web/templates/reading/base.html` and `static/web/reading.js`.
