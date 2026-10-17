# Spec: Keep media navigation selection feedback in sync

- **ID:** 108
- **Status:** Accepted (2026-10-17)
- **Item:** ITEM-108
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** patch

## Intent

Make the New media modal's Upload / Media Library selection move like the app's other
segmented switches, and ensure the main-sidebar Media Library highlight is removed when the
operator navigates to another page without a full reload.

## Scope

### In scope

- The Upload / Media Library tab switch inside the Tata Ibadah New media form.
- The main-sidebar Media Library link's current-page state during direct and in-place page
  navigation, including back and forward history navigation.
- Reduced-motion and keyboard-accessible behavior for the tab switch.

### Out of scope

- Changes to tab order, labels, panel contents, media selection persistence, upload behavior, or
  saving a media entry.
- Changes to the layout, open/mini/closed behavior, or `aria-expanded` state of the Bible,
  Songs, and Tata Ibadah rail menus.
- Changes to any selected-state treatment outside these two controls.

## Domain rules

- The Upload tab remains selected by default when the New media form opens.
- A tab's `aria-selected` value, visible panel, and active-thumb position always identify the
  same selection.
- The Media Library rail link has `aria-current="page"` only while the Media Library page is
  the active destination. A client-side page swap must not leave it current for another route.
- The existing rail menu expansion and panel-state behavior remains unchanged.
- Reduced motion disables the thumb transition, but never the tab selection or route change.

## UI details

The approved visual reference is [preview.png](./preview.png). Keep the media tabs' existing
outer geometry and labels; add a moving selected surface rather than changing the switch size.

- **Size / spacing:** Keep the tab track at `min(320px, calc(100% - 36px))`, centered with its
  current 15 px vertical margin, 3 px inner padding, 1 px divider border, and 9 px corner
  radius. Keep two equal-width 36 px-high tab buttons with 6 px corner radii. The active thumb
  sits 3 px from the track's top and left, is `calc((100% - 8px) / 2)` wide, and is 36 px high.
- **Position / layout:** The track is the positioning context. Place one decorative thumb behind
  the two buttons. Its default position is behind Upload at the left. When Media Library is
  selected, translate it exactly one half-track (`translateX(100%)`) to the right. Do not change
  the track's dimensions or cause content reflow.
- **Colors / typography:** Use `--rail-bg` for the track, `--active-bg` for the thumb,
  `--active-ink` for the selected label, and `--head-ink` for the inactive label. Keep the
  existing 600-weight, 13 px system-sans tab labels. Retain the previous spec's inactive-tab
  hover fill (`--icon-hover-bg`) and `--ink` text color; the selected tab's active colors remain
  visible while hovered. Colors follow the app's light and dark theme tokens.
- **States:** Upload is selected on open; Media Library becomes selected on click or keyboard
  activation and vice versa. Update `aria-selected` and the visible `tabpanel` together with the
  thumb. The thumb is decorative (`aria-hidden="true"`). Keep existing keyboard focus styling.
  On the main rail, retain the server-rendered current marker on a direct Media Library load;
  clear it from that link when navigation lands on another destination, and restore it when
  navigation returns to Media Library. Other rail-menu expansion states continue using their
  existing `aria-expanded` state.
- **Responsive behavior:** Do not change the current centered track width or the dialog layout.
  The track remains within its existing responsive width on narrow screens and does not
  introduce horizontal overflow.
- **Motion:** Move the thumb with `transform var(--ease)`, using the app's existing
  `200ms cubic-bezier(.32, .72, .28, 1)` timing. Transition tab text/background colors with the
  same `--ease` value. Under `prefers-reduced-motion: reduce`, remove these transitions while
  preserving immediate state updates.

## Acceptance scenarios

### Scenario: Switch between media sources

- **Given** the New media form is open with Upload selected
- **When** the operator activates Media Library
- **Then** the Media Library panel becomes visible and its tab has `aria-selected="true"`
- **And** the active thumb moves from behind Upload to behind Media Library
- **And** returning to Upload moves the thumb back and restores the Upload panel and selected
  state
- **And** the existing media selection behavior remains unchanged

### Scenario: Respect reduced motion

- **Given** the system requests reduced motion
- **When** the operator switches between Upload and Media Library
- **Then** the panel and accessible selection update immediately
- **And** no animated thumb transition runs

### Scenario: Navigate away from Media Library in place

- **Given** Media Library is open and its main-sidebar link is marked
  `aria-current="page"`
- **When** the operator navigates in place to Bible, Songs, or Tata Ibadah
- **Then** the Media Library link no longer has `aria-current="page"` or its current-page
  highlight
- **And** the chosen menu follows its existing `aria-expanded` and panel behavior

### Scenario: Return to Media Library through navigation history

- **Given** the operator navigated in place from Media Library to another main destination
- **When** browser Back returns to Media Library, or browser Forward leaves it again
- **Then** the Media Library link's current-page state follows the destination shown in the
  reading shell
- **And** no stale current-page highlight remains on the other destination

### Scenario: Load Media Library directly

- **Given** the operator opens or reloads the Media Library URL directly
- **When** the page is rendered
- **Then** its main-sidebar link is marked as the current page

## Traceability

- Domain/app tests: N/A
- E2E: `tests/e2e/test_media_library.py`
- Implementation: `multimedia/web/templates/reading/_entry_form.html`,
  `multimedia/web/templates/reading/base.html`, `static/styles/design/components.css`, and
  `static/web/reading.js`
