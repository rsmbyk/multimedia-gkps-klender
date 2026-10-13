# Spec 083: Give the translation switch the same hover as the screen-mode switch

- **ID:** 083
- **Status:** Accepted
- **Item:** ITEM-086
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** patch

## Intent

Every Bible translation switch answers the pointer the way the Text screen-mode switch does, so the two
segmented controls in the reading UI behave identically.

## Scope

### In scope

- `.read__lang` wherever it renders: the reading header (TB/SIM anchors) and the entry form's passage
  translation switch (TB/SIM buttons).

### Out of scope

- The Multi-line / Single-screen screen-mode switch and its Preview footer variant.
- The switches' size, radius, track, thumb, selected fill, typography, and focus outline.
- The legacy OBS dock and its own controls.

## Domain rules

- N/A — presentation only. No stored value, endpoint, or default changes.

## UI details

- **Visual reference:** [Switch comparison preview](./preview.html) — hover the TB/SIM switch with
  "Current build" off; the fill matches the screen-mode switch beside it.
- **Size / spacing / position:** unchanged. Options keep `min-width: 52px`, `height: 30px`,
  `padding: 0 12px`, and the 3px track padding with a 9px radius.
- **Colors / typography:** an unselected option under the pointer takes `background: var(--icon-hover-bg)`
  (`rgba(31, 31, 29, .08)` light, `rgba(255, 255, 255, .09)` dark) and `color: var(--ink)` — exactly the
  screen-mode hover. The selected option's `--active-bg` / `--active-ink` and the `--rail-bg` track are
  unchanged; the option under the pointer is never filled when it is the selected one.
- **States:** hover only. Keyboard focus keeps its current treatment; the switch's own focus ring is
  unchanged, and disabled/pending states keep their existing styles.
- **Responsive behavior:** unchanged; below 420px the switch keeps its current sizing and the hover fill
  follows the option's box.
- **Motion:** the fill uses the existing `--ease` (200ms cubic-bezier(.32, .72, .28, 1)) together with
  the colour, matching the screen-mode hover. Under `prefers-reduced-motion` the shell's existing
  clamp applies as it does today.

## Acceptance scenarios

### Scenario: Hovering an unselected translation

- **Given** the reading header shows TB selected and SIM not selected
- **When** the pointer rests on SIM
- **Then** SIM takes the same background fill and text colour that an unselected screen-mode option
  takes under the pointer, and TB is visually unchanged.

### Scenario: Hovering the selected translation

- **Given** TB is the selected translation
- **When** the pointer rests on TB
- **Then** TB keeps its selected fill and no hover fill is painted over the thumb.

### Scenario: The modal switch matches

- **Given** the passage picker is open in the entry form
- **When** the pointer rests on the unselected translation
- **Then** it fills exactly as the header switch does, with the fill fading in over the same duration.

### Scenario: Both switches side by side

- **Given** a Text create form showing the Multi-line / Single-screen switch
- **When** the pointer is moved between the two switches' options
- **Then** the hover treatment is indistinguishable between them.

## Traceability

- Domain/app tests: N/A — CSS only.
- E2E: `tests/e2e/test_reading.py` (header switch) and `tests/e2e/test_entry_pickers.py` (modal switch).
- Implementation: `static/styles/design/components.css` (the `.read__lang` hover and transition rules).
