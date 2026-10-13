# Spec 087: Slimmer, softer scrollbars with no stepper buttons

- **ID:** 087
- **Status:** Accepted
- **Item:** ITEM-090
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** patch

## Intent

Make the reading UI's scrollbars quiet, thin indicators: no end buttons, a lighter touch against the
surface, and the same look in both themes.

## Scope

### In scope

- The shared scrollbar block used by every scroller in the reading UI, the dialogs, the pickers, and the
  textareas.
- The scrollbar thumb tokens in light and dark.

### Out of scope

- The scrollers that deliberately hide the scrollbar (Bible mini panel, Tata Ibadah entry list).
- Scroll behaviour and the Bible mini panel's scroll-indicator chevrons.
- The legacy OBS docks and the projector page.

## Domain rules

- N/A — presentation only.

## UI details

- **Visual reference:** [Scrollbar comparison preview](./preview.html) — the same two scrollable panes,
  current beside proposed, in light and dark; the browser draws the real scrollbars.
- **Size / spacing / position:** the scrollbar track goes from 6px to **5px** in both axes; the thumb
  keeps `border-radius: 999px` and a transparent track.
- **Which path each engine takes:** the standard properties (`scrollbar-width: thin`,
  `scrollbar-color: var(--scroll-thumb) transparent`) are applied **only** where the custom
  pseudo-element is unsupported:

  ```css
  @supports not selector(::-webkit-scrollbar) {
    :root, :root * { scrollbar-width: thin; scrollbar-color: var(--scroll-thumb) transparent; }
  }
  ```

  Blink and WebKit match `selector(::-webkit-scrollbar)`, so they never see the standard properties and
  draw the `::-webkit-scrollbar` bar (5px, no steppers); engines without the pseudo-element keep the
  standard thin coloured bar. Applying both at the top level is what puts the platform's stepper buttons
  on screen — a browser that understands the standard properties takes the native path and ignores the
  pseudo-elements, and measured on Chromium 145 that native bar is 10px with a visible stepper glyph.
- **Colors / typography:** the resting thumb moves closer to its surface and the hover state stays
  clearly distinguishable, per theme:

  | token | now | proposed |
  | --- | --- | --- |
  | `--scroll-thumb` (light) | `#AAA59B` (2.25:1) | `#B4B0A6` (1.99:1) |
  | `--scroll-thumb-hover` (light) | `#827D73` (3.76:1) | `#948F85` (2.95:1) |
  | `--scroll-thumb` (dark) | `#514D45` (2.21:1) | `#45413A` (1.83:1) |
  | `--scroll-thumb-hover` (dark) | `#777268` (3.89:1) | `#65615A` (3.02:1) |

  Ratios are against that theme's canvas (`#F7F5F1` light, `#14130F` dark). Text tokens are untouched.
- **States:** stepper buttons are suppressed on both paths — by never entering the native path in
  Blink/WebKit, and by `::-webkit-scrollbar-button { display: none; width: 0; height: 0; }` with a
  transparent `::-webkit-scrollbar-corner` for engines that draw them on the custom path. The thumb's
  hover fill still changes to `--scroll-thumb-hover`, and a scroller with nothing to scroll is
  unchanged.
- **Responsive behavior:** unchanged — the same 5px bar at every width, and the mini-panel and entry-list
  scrollbars stay hidden as they are today.
- **Motion:** none; the existing hover colour transition on the thumb is untouched.

## Acceptance scenarios

### Scenario: No stepper buttons

- **Given** any scrollable region of the reading UI in Chromium
- **When** it renders with more content than fits
- **Then** the bar's top and bottom ends carry no up/down glyph: the thumb runs from the track's end,
  with no button between it and the edge.

### Scenario: The custom path is the one in use

- **Given** the same region
- **When** it is measured
- **Then** the space the scrollbar takes (`offsetWidth - clientWidth` minus the element's borders) is
  5px and the element's computed `scrollbar-width` is `auto` — proof that the native thin bar, the one
  that brings the steppers, is not being drawn.

### Scenario: The slimmer bar

- **Given** the same region
- **When** its scrollbar is measured
- **Then** it is 5px wide, the thumb is fully rounded, and the track is transparent.

### Scenario: Both themes

- **Given** the app in light and in dark mode
- **When** the thumb's resting colour is read
- **Then** it is the theme's softer `--scroll-thumb`, and hovering it takes
  `--scroll-thumb-hover` and reads clearly against the surface.

### Scenario: Hidden scrollbars stay hidden

- **Given** the Bible mini panel or the Tata Ibadah entry list
- **When** their content overflows
- **Then** no scrollbar is drawn, exactly as today.

### Scenario: Dialogs and pickers inherit

- **Given** the entry Preview, an editor dialog, a picker menu, or a textarea with overflow
- **When** a scrollbar appears
- **Then** it uses the same 5px, button-free, softer bar.

## Traceability

- Domain/app tests: `tests/test_design_scrollbars.py` (new) — the standard properties appear only inside
  the `@supports not selector(::-webkit-scrollbar)` block and nowhere else, the custom bar is 5px, the
  stepper buttons are suppressed, the track and corner are transparent, the two deliberately hidden bars
  stay hidden, and the four thumb tokens sit in the intended contrast band. `tests/test_design_tokens.py`
  keeps passing (it does not assert the scrollbar tokens).
- E2E: `tests/e2e/test_reading.py::ScrollbarE2ETests` — the panel scroller's occupied width (5px) and
  its computed `scrollbar-width: auto`, in light and dark, with the native path forced as a control
  (10px, `thin`); and a pixel check that the bar's top end is bare track rather than a stepper button,
  again with the native path as the control. The browser is launched with `ignore_default_args=
  ['--hide-scrollbars']`: Playwright hides scrollbars by default, which would measure 0px on both paths
  and prove nothing.
- Implementation: `static/styles/design/components.css`, `static/styles/design/tokens.css`.
