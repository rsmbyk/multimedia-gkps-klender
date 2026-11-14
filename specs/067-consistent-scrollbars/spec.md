# Spec: Consistent scrollbars

- **ID:** 067
- **Status:** Accepted
- **Item:** ITEM-070
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** patch

## Intent

Make scrollbars throughout the new app UI visually consistent with the slim, rounded scrollbar shown in the attached Tata Ibadah sidebar.

## Scope

### In scope

- Page scrollbars; sidebars, lists, result areas, and detail panels in the new UI.
- Preview modals and other scrollable dialog bodies.
- Scrollable dropdowns, popovers, and search suggestion lists, including content rendered in a portal.
- Multiline text fields and editors that use native scrollbars.
- Document-level scrolling on the reading and Tata Ibadah pages, and horizontal scrolling in preview tabs if they overflow.
- Dark and light surface variants with subdued tracks and visible thumbs.
- Browser-supported styling with native fallback.

### Out of scope

- Legacy web pages and OBS docks/sources.
- Scrolling mechanics, layout, or content changes.
- Browser UI outside the app page.
- Collapsed mini rail scrollbars that are deliberately hidden and represented by scroll chevrons.

## Domain rules

- None; this is a visual style change.

## Visual details

- Scrollbar width and height: 6px where the browser supports WebKit scrollbar styling; `thin` in browsers supporting the standard property.
- Track: transparent. Thumb: fully rounded.
- Light thumb: `#AAA59B`, hover `#827D73`; dark thumb: `#514D45`, hover `#777268`.
- The active theme selects the thumb color, including system theme changes.
- Collapsed mini rails retain hidden scrollbars and their existing scroll chevrons.

## Acceptance scenarios

### Scenario: Dark surface

- **Given** a dark app panel with content that overflows
- **When** the panel is scrolled
- **Then** its scrollbar is narrow, rounded, and subdued like the reference sidebar, with a visible thumb.

### Scenario: Light surface

- **Given** a light app page or panel with content that overflows
- **When** the page or panel is scrolled
- **Then** its scrollbar follows the same shape and width, with a thumb that remains visible against the light surface.

### Scenario: Scrollable components

- **Given** a new UI page with overflowing sidebar/list/detail content, a preview modal, a dropdown or popover, and a multiline text field
- **When** each component is scrolled
- **Then** each uses the shared scrollbar treatment wherever the browser permits styling.

### Scenario: Legacy views

- **Given** a legacy web page or OBS dock/source
- **When** this spec is implemented
- **Then** its stylesheets and scrollbar appearance remain unchanged.

### Scenario: Scroll behavior

- **Given** a restyled scrollbar
- **When** a user scrolls with a pointer, keyboard, or touch input
- **Then** the content remains reachable and scrolling behavior remains unchanged.

## Traceability

- Domain/app tests: N/A; CSS only.
- E2E: Local Chromium inspection of `/home/` and `/tatib/142/` in light and dark themes. Computed `scrollbar-width` and `scrollbar-color` matched on the page, sidebar, preview, editor, dropdown options, and textarea; `.ch__body` remained `none`. The sidebar scrolled by mouse wheel (500px), PageDown (to 998px), and a simulated touch swipe (to 425px). The existing 22 preview/picker E2E tests ran in Docker but were skipped because Chromium was unavailable there.
- Implementation: `static/styles/design/tokens.css`, `static/styles/design/components.css`.
