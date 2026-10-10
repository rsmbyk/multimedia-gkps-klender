# Spec 053: Give each entry the height of its floating controls

- **ID:** 053
- **Status:** Draft
- **Item:** ITEM-055
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** patch

## Intent

Preview / Edit / Delete float over an entry's top-right corner (spec 033), so on an entry without a
title they sit on the first line of its text and on a titled entry they crowd the title. Make the
entry's own height include the controls: each entry with controls reserves a quiet top band for
them, and its words always begin below that band.

## Scope

### In scope

- An entry that renders Preview / Edit / Delete reserves a top band equal to the controls' height
  plus their offset (~44px today); its title or first line starts below it.
- The controls keep their position, hover/focus reveal, touch behavior, and look (specs 033/034).
- The hover highlight covers the whole item including the band (spec 034).

### Out of scope

- The section break's own controls (`tatib__eos` is a rule, not a text block).
- The add rows and section-break margins (spec 052).

## UI details

Approved preview: the live session screenshots of 2026-10-10 (before / after) the owner OKed with
"accept both".

- **Size / spacing:** band = `padding-top: 44px` on `.tatib__item--acts` (controls offset 8px +
  measured height 36px); no other padding or margin changes.
- **Position / layout:** the controls keep `position: absolute; right: 8px; top: 8px` inside the
  item; the band pushes the title/first line below them.
- **Colors / typography:** unchanged — the existing `.entry__acts` backing and `.entry__ctrl` style.
- **States:** hidden (`opacity: 0`) still occupies the band — the band is the item's height, not a
  reveal; shown on hover / focus, always on touch (unchanged from spec 033).
- **Responsive behavior:** the band is a fixed 44px at every width; the controls never wrap.
- **Motion:** none added — the controls keep the existing `opacity` transition (spec 033).

## Domain rules

- **The item owns the controls' height.** An entry carrying Preview / Edit / Delete reserves a top
  band for them; no word of its title or text ever sits under the controls, at any width.
- **The reveal is unchanged.** Controls still show on hover and keyboard focus, and outright on
  touch devices; only the overlap goes away (amends spec 033: no longer "over the words").
- **Only where the controls exist.** The band is tied to the controls' own condition in the
  template: an item reserves it exactly when it emits `.entry__acts` (in practice every entry
  does; the section break does not).
- **One hovered row.** The band is part of the item, so the highlight and the hover fill include it
  (spec 034); the band is never a separate strip.

## Acceptance scenarios

### Scenario: An entry without a title

- **Given** an entry whose first content is a line of text
- **When** the pane renders, and when I hover the entry
- **Then** the controls sit in the reserved band above the text and never overlap its words

### Scenario: A titled entry

- **Given** an entry with a title
- **Then** the title starts below the band, and the controls sit above it, not beside it

### Scenario: Reveal behavior is untouched

- **Given** an entry with hidden controls
- **When** I hover it or focus something inside it
- **Then** the controls appear in the band; on a touch device they are always visible

### Scenario: Only where the controls are

- **Given** the pane
- **Then** every entry that renders Preview / Edit / Delete carries the band; the section break —
  which floats its controls over the rule, not over words — reserves none

### Scenario: Highlight coherence

- **Given** a hovered entry with a band
- **Then** the hover fill covers the band and the text as one row

## Traceability

- Domain/app tests: N/A (pane layout; no server data).
- E2E: `tests/e2e/test_tatib_entry_controls.py`.
- Implementation: `multimedia/web/templates/reading/tatib.html`,
  `static/styles/design/components.css`.
- Amends: spec 033 (the controls no longer float over the words).
- Pairs with: spec 052 (the pane's resting vertical space).
