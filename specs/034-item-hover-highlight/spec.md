# Spec 034: Highlight a whole service entry item on hover

- **ID:** 034
- **Status:** Draft
- **Item:** ITEM-036
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** patch

## Intent

Make the hovered service entry obvious by highlighting the whole item, the way the sidebars
highlight a row.

## Scope

### In scope

- A hover background on the item (`--icon-hover-bg`, theme-aware), including legacy `.tatib__eos`
  rows.
- The same highlight when the item holds keyboard focus.
- No layout movement when the highlight appears.

### Out of scope

- Sidebar selected tints, and the other reading panes.
- Item contents, order, or data.

## Domain rules

- **The row reads as one. ** Hovering an entry highlights the whole item as a single row, not a
  fragment of it.
- **Nothing moves.** Showing the highlight never shifts the text.
- **Theme-aware.** The highlight uses the shared hover token so light and dark both read.
- **Keyboard included.** Focusing within the item highlights it as hovering does.
- **No stale state.** Moving the pointer away, or using a control, leaves no lingering highlight or
  outline (spec 025).

## Acceptance scenarios

### Scenario: Hovering an item

- **Given** an entry in the Tata Ibadah pane
- **When** I hover it
- **Then** the whole item is highlighted as one row

### Scenario: No layout shift

- **Given** an entry
- **When** the hover highlight appears and disappears
- **Then** the text does not move

### Scenario: Keyboard

- **Given** I tab into an item's controls
- **Then** the item is highlighted

### Scenario: Both themes

- **Given** the light theme, and the dark theme
- **Then** the highlight is legible in each

## Traceability

- Domain/app tests: N/A (visual state; no server data change).
- E2E: `tests/e2e/test_tatib_hover.py`.
- Implementation: `static/styles/design/components.css`.
- Related: spec 033 (floating controls, same hover), spec 025 (quiet focus).
- Amended by: spec 036 (the add bar is outside the item's hover).
