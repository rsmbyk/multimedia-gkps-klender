# Spec: Give Tata Ibadah media entries more breathing room

- **ID:** 110
- **Status:** Accepted (2026-10-17)
- **Item:** ITEM-110
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** patch

## Intent

Make media entries on the Tata Ibadah page easier to scan by giving the file icon, title, and details more vertical room.

## Scope

### In scope

- Height and vertical padding of media rows in the Tata Ibadah service page.
- Consistent 12 px vertical spacing between service rows shown in the approved preview.
- Responsive behavior for long filenames and narrow viewports.

### Out of scope

- Text-entry or break-entry dimensions, file icons, content, actions, file storage, and projector rendering.

## Domain rules

- Only media rows receive the larger minimum height and vertical padding.
- A media row continues to display its existing file icon, title, subtitle, and actions with their current behavior.
- Text and break entries retain their existing dimensions and content.

## UI details

The owner accepted [preview.html](./preview.html) on 2026-10-17. It shows media rows among text and break entries on a Tata Ibadah page.

- **Size / spacing:** Media rows have `min-height: 80px`, with `16px` vertical padding, `16px` right padding, and `64px` left content offset. Keep the file icon at `42px × 42px`, positioned `12px` from the row's left edge and centered vertically. Keep `12px` between consecutive rows, matching the preview.
- **Position / layout:** Keep the icon in its existing absolute-positioned slot. Vertically center the title and subtitle block in the row. The title and subtitle remain together and wrap when needed. Do not apply the media sizing rule to text or break entries.
- **Colors / typography:** Preserve current row surface, border, radius, icon colors, title font, and muted subtitle styling. The spacing change adds no new color or typography treatment.
- **States:** Keep existing hover and keyboard-focus surfaces and controls in their current locations and states. The taller card must not hide or disable Edit/Delete actions.
- **Responsive behavior:** At widths up to `520px`, keep the row within the viewport, retain the existing `60px` left offset and `12px` right padding, and allow long titles to wrap without horizontal overflow.
- **Motion:** No new animation; preserve the current row transition and reduced-motion behavior.

## Acceptance scenarios

### Scenario: Media rows have more vertical room

- **Given** a Tata Ibadah contains media entries alongside text and break entries
- **When** the service page displays the entries
- **Then** each media row is at least 80 px tall with 16 px vertical padding
- **And** the icon stays vertically centered beside the title and subtitle
- **And** text and break rows retain their existing dimensions

### Scenario: Media rows fit narrow screens

- **Given** the Tata Ibadah page is viewed at 520 px wide or narrower
- **When** a media filename is long
- **Then** the title wraps within the media row
- **And** no horizontal page overflow is introduced
- **And** the icon and title remain separated and readable

### Scenario: Existing actions remain available

- **Given** a media row is hovered, focused, or opened for editing
- **When** the row uses its taller geometry
- **Then** its existing action controls remain visible and usable in the same states as before

## Traceability

- Domain/app tests: N/A, no rules change.
- E2E: `tests/e2e/test_media_library.py::MediaLibraryE2ETests.test_media_entry_has_roomy_spacing_and_wraps_on_narrow_screen` checks the 80 px media row, padding, centered icon, wrapping, responsive insets, 12 px rhythm, and unchanged text/break dimensions.
- Implementation: `static/styles/design/components.css` and the relevant Tata Ibadah E2E module.
