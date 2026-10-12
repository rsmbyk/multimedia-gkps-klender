# Spec: System theme as the default appearance mode

- **ID:** 062
- **Status:** Accepted
- **Item:** ITEM-065
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** minor

## Intent

The public reading site offers Light, Dark, and System appearance choices. System is the default for readers without a saved choice and follows their device's current appearance.

## Scope

### In scope

- A clearly labeled three-mode control on public reading pages.
- Theme choice retained in browser storage across reading pages and reloads.
- Reuse the existing Light and Dark palettes for the public reading design language.
- Responsive system mode using `prefers-color-scheme`.

### Out of scope

- Editor, OBS docks and sources, server-side preference storage, and account synchronization.

## Domain rules

- The stored preference is one of `system`, `light`, or `dark`.
- Missing, unreadable, or unrecognized storage values resolve to `system`.
- Light and Dark overrides ignore system changes until the reader chooses System.
- System reacts to system-theme changes without a page reload.
- The control indicates the selected preference, including System when the resulting palette is light or dark.

## Acceptance scenarios

### Scenario: First visit follows the device

- **Given** I have no saved theme preference
- **When** I open a public reading page with a light or dark device theme
- **Then** System is selected and the page uses the matching palette before visible content appears

### Scenario: Explicit choice persists

- **Given** I select Light or Dark
- **When** I reload or navigate to another public reading page
- **Then** my choice remains selected and its palette stays applied regardless of the device theme

### Scenario: System updates live

- **Given** I select System
- **When** the device theme changes
- **Then** the page changes to the matching palette without a reload

### Scenario: Invalid or unavailable storage

- **Given** the stored preference is invalid or browser storage is unavailable
- **When** I open a public reading page
- **Then** the page remains usable with System behavior

## Traceability

- Domain/app tests: N/A, browser presentation behavior.
- E2E: `tests/e2e/test_reading.py` — `test_system_theme_is_default_and_follows_os_changes`, `test_system_mode_can_be_restored_after_manual_override`, `test_invalid_theme_storage_defaults_to_system`, `test_unavailable_theme_storage_defaults_to_system`, plus existing dark-theme checks.
- Implementation: `multimedia/web/templates/reading/base.html`, `static/web/reading.js`, `static/styles/design/components.css`.

## Verification

- Four new theme scenarios and the existing dark-mode persistence test passed locally.
- Fifteen related browser tests passed, including existing dark-theme styling checks.
- The editor date-picker browser test passed at its 360 px tall viewport after compacting the rail controls for short screens.
- The full reading E2E module ran 38 tests; 37 passed. `test_bible_language_highlight_slides_without_reflow` fails on an exact header geometry comparison. The same failure was reproduced on untouched `develop` at `89ce7c5`, so it is pre-existing.
