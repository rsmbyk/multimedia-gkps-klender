# Spec 056: Give the stage entry links a theme-aware colour

- **ID:** 056
- **Status:** Accepted
- **Item:** ITEM-058
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** patch

## Intent

On the Tata Ibadah stage the entry titles — `.entry__jump`, the song and passage links — are raw
anchors with no author colour, so they render in the browser's default blue `#0000EE` in both
themes. Measured, that is **1.98:1** contrast on the dark canvas (the theme's body text there is
16.8:1) and the only off-palette element in the reading surface; the owner finds them jarring
against the other text. Give the stage's entry links the theme's accent, quieted: forest green
`#1C5C3C` in light (7.29:1) and lifted royal blue `#7C9CF0` in dark (6.97:1), keeping the
underline.

## Scope

### In scope

- A `--link` token in both theme blocks of `tokens.css`: light `#1C5C3C`, dark `#7C9CF0`.
- One rule colouring `.entry__jump` from the token.
- The tokens contrast test covers the new pair; one E2E theme check.

### Out of scope

- Every other anchor (the rail logo is an image; sidebar/TOC rows are already styled).
- Visited styling; hover/focus decoration; the underline.

## UI details

Approved preview: the live `/tatib/142/` session of 2026-10-11 — a four-option colour grid in
both themes (default blue / sage / royal / quiet ink) and the chosen combo rendered full-page;
the owner picked green-light + blue-dark and OKed with "proceed".

- **Size / spacing:** none (colour only).
- **Position / layout:** none.
- **Colors / typography:** link colour `var(--link)` — light `#1C5C3C` on canvas `#F7F5F1`
  (7.29:1), dark `#7C9CF0` on `#14130F` (6.97:1); both clear the 4.5:1 AA floor (measured).
  Font and underline inherit as today (`text-decoration: underline`, colour follows the text).
- **States:** hover, focus and visited keep the colour; the focus outline is unchanged.
- **Responsive behavior:** none.
- **Motion:** none.

## Domain rules

- **The stage's entry links wear the theme's link colour.** `.entry__jump` renders
  `var(--link)`; `--link` is `#1C5C3C` (light) and `#7C9CF0` (dark).
- **The pair stays AA.** `--link` on `--canvas` is at least 4.5:1 in both themes (measured
  7.29 / 6.97).
- **The underline stays.** The link keeps its underline as the non-colour cue.
- **Scope is exact.** Only `.entry__jump` changes; every other anchor renders as today.

## Acceptance scenarios

### Scenario: Light theme

- **Given** the stage in light mode
- **Then** every entry title link is `#1C5C3C` on the canvas

### Scenario: Dark theme

- **Given** I toggle the theme on the stage
- **Then** every entry title link is `#7C9CF0` on the canvas

### Scenario: States and cue

- **Given** a link hovered or focused
- **Then** its colour is unchanged and its underline is still present

### Scenario: Everything else

- **Given** the rest of the page
- **Then** no other anchor's rendering changes

## Traceability

- Domain/app tests: `tests/test_design_tokens.py` (add `('--link', '--canvas')` to `TEXT_PAIRS`).
- E2E: `tests/e2e/test_reading.py` — `test_tatib_stage_entry_links_follow_the_theme`.
- Implementation: `static/styles/design/tokens.css`, `static/styles/design/components.css`.
- Amends: spec 004 (extends the token layer; the stage links were unstyled).
- Related: spec 054 (the entry heading these links render).
