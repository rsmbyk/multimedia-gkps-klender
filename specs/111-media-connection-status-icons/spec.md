# Spec: Show distinct connection icons in the Media Library status row

- **ID:** 111
- **Status:** Accepted (2026-10-17)
- **Item:** ITEM-111
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** patch

## Intent

Help operators scan the local Media Library connection state in the status popover without implying that an unavailable companion is in an error state.

## Scope

### In scope

- A distinct inline icon for Connected and Unavailable in the status popover's Connection row.
- Updating the icon when the existing connection state changes.
- Keeping the text state label as the accessible, authoritative state.

### Out of scope

- The Media Library status-button dot or its color/state behavior.
- Companion health checks, connection detection, polling, or error handling.
- File count and total-size rows, including their existing hidden state while unavailable.
- Any other Media Library or service-entry presentation.

## Domain rules

- The existing connection response continues to determine whether the row says Connected or Unavailable.
- Connected and Unavailable each show only their matching icon; a state change must not leave the previous icon visible.
- Icons are decorative (`aria-hidden="true"`); the visible text remains exactly Connected or Unavailable and is available to assistive technology.
- Unavailable is a neutral state, not a danger or error indication.

## UI details

The owner accepted the [Media Library preview](./preview.html) on 2026-10-17. It shows the connection icons inside the existing status popover.

- **Size / spacing:** Each inline SVG is 17 px by 17 px, does not shrink, and sits 7 px before the state label. Preserve the current Connection row height, value font, weight, and right alignment.
- **Position / layout:** Keep the existing Connection label on the left and the state value right-aligned. Align the icon and state text vertically in one inline row; do not resize or reposition the popover or its status button.
- **Colors / typography:** Connected uses a 1.8 px green outline (`#17804d`) check-circle. Unavailable uses a 1.8 px `var(--head-ink)` outline (the app's theme-aware muted text token): a 14 px rounded square with 4 px corner radius and a centered horizontal dash. This matches the muted `--muted` icon in the approved preview. Keep the existing state text typography and foreground color. Do not apply danger colors to Unavailable.
- **States:** Connected displays the check-circle and Connected text; Unavailable displays the neutral square-minus and Unavailable text. On a state refresh, switch both the text and icon together. No new hover, focus, active, or disabled state is introduced.
- **Responsive behavior:** Keep the icon fixed-size and adjacent to its text within the current status-row layout; preserve the existing responsive popover width and avoid horizontal overflow.
- **Motion:** No new animation. Preserve the existing popover animation and reduced-motion behavior.

## Acceptance scenarios

### Scenario: Connected state is shown calmly and distinctly

- **Given** the local companion responds with a connected status
- **When** the operator opens the Media Library status popover
- **Then** the Connection row shows a green outlined check-circle before Connected
- **And** the icon is decorative to assistive technology
- **And** the existing file count and total-size rows remain visible as before

### Scenario: Unavailable state does not imply an error

- **Given** the local companion is unavailable
- **When** the operator opens the Media Library status popover
- **Then** the Connection row shows a muted rounded-square-minus before Unavailable
- **And** the icon does not use danger styling
- **And** the existing file count and total-size rows remain hidden

### Scenario: The icon follows a refreshed connection state

- **Given** the Connection row currently shows either state
- **When** the existing status refresh reports the other state
- **Then** the label and icon update together
- **And** only the icon matching the latest state is visible

## Traceability

- Domain/app tests: N/A; no connection or persistence rules change.
- E2E: `tests/e2e/test_media_library.py::MediaLibraryE2ETests.test_disconnected_library_hides_local_inventory_details`, `test_connected_library_shows_file_and_status_details`, and `test_connection_icon_tracks_status_refresh`.
- Implementation: `multimedia/web/templates/reading/media_library.html`, `static/web/media-library.js`, and `static/styles/design/components.css`; release metadata in `VERSION` and `CHANGELOG.md`.
