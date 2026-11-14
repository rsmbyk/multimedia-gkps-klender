# Spec: Keep media entries visible in saved Tata Ibadah pages

- **ID:** 106
- **Status:** Accepted (2026-10-17)
- **Item:** ITEM-106
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** patch

## Intent

Make a Tata Ibadah opened through in-place/saved-page navigation show the same media entry
identity and add actions as a full server-rendered page.

## Scope

### In scope

- Serialize a media service entry's kind, fingerprint, and family in the offline service chunk.
- Render media rows with the existing type icon, filename/title, and missing/unavailable state
  behavior when the saved renderer applies a Tata Ibadah page.
- Render the existing `+ Media` add action in the start bar and after-entry rows.
- Render the existing `Add Media` action for an empty service when editing is enabled in the
  saved shell.
- Keep offline chunk revisions sensitive to these serialized fields so existing saved copies
  refresh.

### Out of scope

- Uploading, downloading, storing, deleting, or recovering files.
- Displaying media contents in Preview or on the projector.
- Changing the service-entry form, control appearance, add order, or editor save behavior.
- Adding editor functionality when the saved shell does not already expose editing.

## Domain rules

- A media entry keeps the same fingerprint and family in both server and saved-page rendering.
- Offline service chunks contain media metadata only; file bytes and companion tokens are never
  included.
- Local availability remains computer-specific. After a saved-page swap, the existing media
  status check distinguishes available, missing, and unavailable as it does after a full load.
- Other entry types and their order remain unchanged.

## UI details

This restores the existing Tata Ibadah page UI; it introduces no new design or layout.

- **Position / layout:** Place the media type icon at the left of its service entry, as in
  `multimedia/web/templates/reading/tatib.html`. Keep `+ Media` alongside the existing add
  actions and `Add Media` alongside the other empty-service actions.
- **Colors / typography:** Reuse the current icon, row, and button classes and theme tokens from
  the server-rendered view.
- **States:** Preserve the existing available, missing, and local-library-unavailable states.
  Keep the add actions only when the saved shell already includes the editor modal.
- **Responsive behavior:** Match the server-rendered Tata Ibadah layout at all viewport sizes.
- **Motion:** No new motion.

## Acceptance scenarios

### Scenario: Open a service with media through in-place navigation

- **Given** the browser has a saved Tata Ibadah service containing a media entry
- **And** the operator opens Tata Ibadah from the main rail and selects that service
- **When** the saved-page renderer applies the service page
- **Then** the media entry shows the same file-type icon and title/subtitle as a full page load
- **And** the entry retains its media fingerprint and family for the local availability check
- **And** the corresponding `+ Media` add actions are present wherever the other add actions are
  shown

### Scenario: Open an empty service through in-place navigation

- **Given** the browser has a saved empty Tata Ibadah and the saved shell includes editing
- **When** the operator opens that service through the main rail
- **Then** the empty-service actions include `Add Media` with the other add actions
- **And** activating it opens the existing New media form when online

### Scenario: Refresh saved service data after media metadata changes

- **Given** an existing offline service chunk was saved before the media metadata was added
- **When** the offline library synchronizes the service again
- **Then** the changed chunk revision causes the new media metadata to be saved
- **And** the saved renderer can show the same media row as the server page

### Scenario: Preserve other entry rendering

- **Given** a service contains media and non-media entries
- **When** it is rendered from a saved chunk
- **Then** every entry remains in the same order with its existing content and controls

## Traceability

- Domain/app tests: `tests/test_offline_sync.py`
- E2E: `tests/e2e/test_offline_library.py`
- Implementation: `multimedia/web/reading/offline.py`, `static/web/offline-render.js`,
  `tests/test_offline_sync.py`, and `tests/e2e/test_offline_library.py`
