# Spec 073: Give song Preview verse tabs equal shapes

- **ID:** 073
- **Status:** Accepted
- **Item:** ITEM-076
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** patch

## Intent

Make every numbered song verse tab in the Tata Ibadah service-entry Preview modal the same circular shape.

## Scope

### In scope

- `.preview__tab` buttons in the song variant of the existing Preview modal.
- One- and two-digit verse numbers, selected and unselected states, keyboard focus, and narrow viewports.

### Out of scope

- Bible verse numbers, other Preview variants, song data, and verse selection order.

## Domain rules

- Choosing a tab still shows its corresponding song verse panel and preserves the existing roving keyboard focus behavior.
- The tab count and order come from the same saved song verse selection.

## UI details

- **Approved preview:** [Sidebar follow-ups interactive preview](../072-sidebar-idle-collapse/preview.html), “Song verse tabs” scenario.
- **Size / spacing:** Each numbered button has a fixed 30 × 30px border box and a 1px border. Keep the current 4px gap and 10px bottom margin.
- **Position / layout:** Center each digit horizontally and vertically. Fix width, height, min-width, and flex basis to 30px; do not stretch a button for a two-digit number. Keep one horizontally scrollable tab row at narrow widths.
- **Colors / typography:** Use current `--divider`, `--ink`, `--active-bg`, and `--active-ink` tokens. Keep 13px/1.2 sans-serif digits with tabular numerals.
- **States:** Resting, hover, selected, and keyboard-focus treatments remain token based. The selected circle has the existing active fill. An outline must remain visible on keyboard focus.
- **Responsive behavior:** The circles stay 30 × 30px on small screens and the tablist scrolls horizontally if needed.
- **Motion:** None added.

## Acceptance scenarios

### Scenario: Mixed digit widths

- **Given** a song Preview containing verse tabs 1 through 12
- **When** the modal opens
- **Then** all twelve buttons have equal 30 × 30px border boxes and circular outlines regardless of the number's width.

### Scenario: Selection and keyboard use

- **Given** a song Preview with several verses
- **When** the operator selects a tab with pointer or keyboard
- **Then** that tab uses the current selected colors and the corresponding verse panel appears without changing tab geometry.

### Scenario: Narrow modal

- **Given** more tabs than fit in the modal
- **When** the viewport narrows
- **Then** the row scrolls horizontally and no tab is clipped or distorted.

## Traceability

- Domain/app tests: N/A; this slice only changes tab geometry.
- E2E: `tests/e2e/test_entry_preview.py::EntryPreviewE2ETests.test_a_song_preview_tabs_between_its_verses` preserves verse selection and active-tab focus; `test_a_song_preview_verse_tabs_keep_equal_circles_and_scroll` verifies equal circle geometry, selected verse content, and horizontal scrolling at a narrow viewport.
- Implementation: `static/styles/design/components.css` fixes each song verse tab at 30 × 30px, centers the digits, keeps one horizontal scroll row, and adds a token-based visible keyboard focus outline.
