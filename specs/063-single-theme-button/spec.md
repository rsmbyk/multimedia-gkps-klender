# Spec: Restore the single theme button

- **ID:** 063
- **Status:** Accepted
- **Item:** ITEM-066
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** patch

## Intent

The public reading rail uses one theme button, styled like its original two-mode switcher, to select System, Dark, or Light. The icon and tooltip identify the current preference.

## Scope

### In scope

- One theme button in the rail in place of the three buttons from spec 062.
- A fixed click cycle: `system → dark → light → system`.
- Current-mode icon, tooltip, and accessible name.
- Persistence and System behavior from spec 062.

### Out of scope

- Palette colors, projector appearance, editor and OBS pages, server-side preferences.

## Domain rules

- System remains the default when the stored preference is missing, invalid, or unreadable.
- The button cycles based on the **selected mode**, not the currently resolved light/dark palette.
- Explicit Dark and Light choices stay fixed when the operating system theme changes.
- System follows operating system changes without reloading.
- The stored preference continues to use `gkps-theme` with `system`, `dark`, or `light`.

## UI details

The owner approved the revised single-button preview in this task conversation: the original plain rail button, with its icon and tooltip showing the **active** mode.

- **Size / spacing:** Use the existing `--btn` size: 44 × 44 px by default and 40 × 40 px at viewport widths at or below 560 px. Icon artwork is 24 × 24 px. Do not add visible text beside the icon.
- **Position / layout:** The button is the sole child of the rail footer, centered horizontally and anchored at the bottom. Retain the rail's existing vertical padding. Remove the compact-height sizing rule that was added only to accommodate three theme buttons.
- **Colors / typography:** Plain transparent button with `--icon` stroke, matching other inactive rail buttons. Keep existing hover `--icon-hover-bg`, focus `--focus`, and tooltip token colors. No selected-mode fill.
- **States:** Active System shows a monitor icon and tooltip `System mode`; Dark shows a moon and `Dark mode`; Light shows a sun and `Light mode`. The accessible name also identifies the current mode. Hover and keyboard focus expose the same current-mode tooltip.
- **Responsive behavior:** One bottom button at desktop and narrow widths; no overlap with navigation tiles at 360 px viewport height.
- **Motion:** Reuse the original icon opacity/rotation transition driven by `--ease` (200 ms). Respect existing reduced-motion rules.

## Acceptance scenarios

### Scenario: Default System display

- **Given** I have no saved theme preference
- **When** I open a public reading page
- **Then** the one theme button shows the System icon and `System mode` tooltip
- **And** the page palette follows the device theme

### Scenario: Cycle through all modes

- **Given** System is selected
- **When** I click the button three times
- **Then** the selections are Dark, Light, and System in that order
- **And** after each click the button icon, tooltip, and accessible name show the selected mode

### Scenario: Retain preference across navigation

- **Given** I select Dark or Light
- **When** I reload or navigate to another public reading page
- **Then** the selected preference and matching icon/tooltip remain

### Scenario: System reacts while open

- **Given** I have returned to System mode
- **When** my operating system theme changes
- **Then** the page palette changes without a reload
- **And** the button continues to show System mode

### Scenario: Short viewport remains usable

- **Given** a 360 px tall viewport
- **When** I use the Tata Ibadah rail navigation and theme button
- **Then** neither control overlaps or blocks the other

## Traceability

- Domain/app tests: N/A, browser presentation behavior.
- E2E: `tests/e2e/test_reading.py` — theme cycle, current labels/icons, original button size and transparent fill, System default/following, storage fallback; `tests/e2e/test_editor.py` — date-picker layout at 360 px height.
- Implementation: `multimedia/web/templates/reading/base.html`, `static/web/reading.js`, `static/styles/design/components.css`.

## Verification

- The theme cycle test failed before implementation because the old button remained labeled `Dark theme`.
- The theme cycle, System default/following, storage fallback, original button style, and 360 px editor test passed after implementation (6 targeted browser tests).
- Sixteen existing related browser tests passed, including dark-mode persistence, palette styling, and Tata Ibadah hover behavior.
