# Spec: Polish media picker layout and tab feedback

- **ID:** 107
- **Status:** Accepted (2026-10-17)
- **Item:** ITEM-107
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** patch

## Intent

Keep the New media modal's tall, steady layout when the local library is empty, and make the Upload tab's supported-files line use a consistent text size.

## Scope

### In scope

- The connected local library's empty state in the Media Library tab of the Tata Ibadah New media modal.
- Consistent create-modal geometry when switching between Upload and Media Library, including the connected-empty state.
- The “Supported files:” label and supporting text in the Upload tab.
- The hover appearance of the Upload and Media Library tabs.
- Responsive layout, internal scrolling, and accessible status text for the empty state.

### Out of scope

- The top-level Media Library page, including its own empty and filtered-result states.
- Upload, library selection, save, or file-reference behavior beyond preserving their current states.
- A new empty-state action button, API, storage, companion behavior, or modal motion.

## Domain rules

- Show the empty state only after the local companion is connected and confirms that the library contains no files.
- If the companion is unavailable, retain the existing unavailable message; do not present the library as empty.
- With no file selected, Save remains disabled regardless of the optional entry title.
- Switching tabs, entering a title, or displaying the empty state does not select or import a file.
- Switching between Upload and Media Library does not change the create modal's outer dimensions for the same viewport.
- Hovering an unselected tab gives it the app's normal switch hover cue; hovering the selected tab does not cover or change its selected appearance.

## UI details

The approved quiet empty-state concept is [preview.png](./preview.png). The Upload-tab typography reference is [upload-typography-preview.png](./upload-typography-preview.png). The inactive-tab hover reference is [tab-hover-preview.png](./tab-hover-preview.png). Keep the icon and copy quiet, with generous space around them.

- **Dialog size:** For media-entry creation, set the dialog height to `min(760px, calc(100dvh - 32px))`; retain the existing width `min(840px, calc(100vw - 32px))`. This matches the tall Upload layout while respecting short viewports. Keep the existing 14 px dialog radius, canvas surface, divider outline, and dialog shadow.
- **Layout:** Keep the title at the top, centered two-tab switch below it, the active panel filling remaining vertical space, and the entry-title/actions footer at the bottom. Keep Upload's drop area and the Media Library panel the same height when their tabs are active. Only the active panel may scroll; do not let the page behind the dialog scroll. Preserve the existing 26 px desktop side insets and 18 px insets at widths up to 650 px.
- **Empty panel:** Preserve the existing thin divider at the top and bottom of the library area. Center an empty-state group horizontally and vertically, with a maximum width of 440 px, 12 px gaps, and at least 32 px of free space around the group on desktop. Use a 52 px green outline media icon with no separate icon card or badge, followed by the heading “No media in this library yet” and helper “Upload a file to add it to this computer’s Media Library.” Do not add a CTA, search, file count, drop area, or file rows.
- **Typography and colors:** Use the app's system sans-serif stack. The empty heading is 17 px semibold in `--ink`; its helper is 13 px in `--head-ink` with 1.45 line-height. The icon uses `--focus`. For the Upload tab, set the full supported-files paragraph to 12 px; keep “Supported files:” semibold but make its font size inherit from the paragraph. Keep the larger 17 px treatment only for the main “Drop a file here” instruction.
- **Tab states:** Use `--rail-bg` for the tab-track background, as on the app's other segmented switches. The selected tab stays `--active-bg` with `--active-ink`. On hover, only an unselected tab gets `--icon-hover-bg` and `--ink`; the selected tab remains unchanged. Transition background and text color using the existing `var(--ease)` timing. Preserve the tabs' existing keyboard-focus behavior and `aria-selected` state.
- **Empty-state states:** Expose the empty copy as a polite status. It has no hover, active, or focus state because it has no control. Preserve disabled Save styling and Cancel behavior. Keep the current unavailable-library message distinct from the connected-empty state.
- **Responsive behavior:** Retain the existing narrow dialog width and 18 px horizontal insets at widths up to 650 px. The dialog height remains capped by the viewport formula above; the active content panel scrolls internally on short viewports while the modal title, tabs, entry-title field, Save, and Cancel remain reachable without horizontal overflow.
- **Motion:** No motion for the empty content itself; preserve current dialog open/close motion and reduced-motion behavior.

## Acceptance scenarios

### Scenario: Connected library is empty

- **Given** the local companion is connected and returns an empty file list
- **When** the operator opens the Media Library tab while creating a media entry
- **Then** the tall modal remains the same size as it was on the Upload tab for that viewport
- **And** the library panel shows the centered icon, heading, and helper with relaxed surrounding space and no CTA
- **And** the top and bottom panel dividers, entry-title field, and Cancel action remain available
- **And** Save remains disabled until a file is selected

### Scenario: Supported-files line uses consistent text size

- **Given** the Upload tab is active
- **When** the supported-files paragraph is displayed
- **Then** “Supported files:” and the adjacent text use the same 12 px font size
- **And** the label remains semibold while “Drop a file here” keeps its larger instruction size

### Scenario: Inactive media-source tab is hovered

- **Given** either Upload or Media Library is selected
- **When** the pointer hovers the unselected tab
- **Then** that tab receives the app switch's subtle hover fill and primary text color
- **And** the selected tab keeps its active fill and active text color
- **And** the hover fill and text color transition using the existing app easing

### Scenario: Local library is unavailable

- **Given** the local companion cannot be reached
- **When** the operator opens the Media Library tab
- **Then** the existing unavailable message appears instead of the empty-state copy

### Scenario: Empty state on a narrow or short viewport

- **Given** the New media modal is open on a narrow or short viewport
- **When** the Media Library tab has no files
- **Then** the empty-state content remains centered without horizontal overflow
- **And** the active panel can scroll while the modal title, entry title, Save, and Cancel remain reachable

## Traceability

- Domain/app tests: N/A
- E2E: `tests/e2e/test_media_library.py`
- Implementation: `multimedia/web/templates/reading/_entry_form.html`, `static/web/media-entry.js`, `static/styles/design/components.css`
