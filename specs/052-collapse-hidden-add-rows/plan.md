# Plan 052: Collapse the hidden add rows and tighten the section break

- **Status:** Draft
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-054
- **Bump:** patch

## Why

The pane reserves space for controls it hides. Every `.entry__add` row keeps its full height while
`opacity: 0` (~45px at a normal window width, ~71px when the five buttons wrap at ~1280px), and
`.tatib__eos` adds `margin: 34px 0 34px`. Above the first entry the two stack — measured on
`/tatib/142/` at 1280px: start bar ends, then a 2px rule with 34px margins, then a 71px invisible
row, before the first passage — ~115px of apparent emptiness, plus ~45–71px between every pair of
entries. The reservation exists so a hidden row stays hittable (comment at
`components.css:1467-1473`); reveal-on-hover can keep that property without keeping the height.

## Scope / edges

**In:**

- Hidden `.entry__add` rows collapse to zero height and expand when revealed (item hover/focus,
  own hover/focus, `is-revealed`).
- Coarse-pointer / no-hover devices: rows shown outright.
- `.tatib__eos` margins 34px → 16px.
- E2E expectations in `test_tatib_entry_controls.py` that assume always-reserved rows.

**Out:**

- Add actions, endpoints, reorder, projection, other panes.
- The start bar (`spec 030`): always visible, unchanged.
- Item highlight / floating controls (specs 033, 034).

## Approach

- Collapse with `display: grid; grid-template-rows: 0fr` on the row and `1fr` when revealed, one
  child with `min-height: 0; overflow: hidden` — animates to the row's real (variable) height with
  no JS measurement and no `pointer-events` change. Reveal triggers stay exactly as now: the
  adjacent-sibling CSS rules, `:hover`, `:focus-within`, and the `is-revealed` toggling in
  `entries.js` (`revealNeighbours`), which needs no change.
- Keep the existing 220ms hide delay so crossing the item's edge onto the row cannot blink it
  closed; the expanded row must remain enterable for its whole transition-out (grid 0fr collapse
  keeps the box until the transition ends, so the pointer path stays open).
- `@media (hover: none) and (pointer: coarse)`: show the rows outright, mirroring the existing
  `.entry__acts` touch rule at `components.css:1512`.
- Reduce `.tatib__eos` margin to `16px 0 16px`; the rule and its diamond dot stay untouched
  (spec 035's look).
- Adjust the E2E assertions in `test_tatib_entry_controls.py` that read the rows' resting geometry
  (e.g. the "no overlap" box comparison) to the collapsed resting state; the reveal/hide
  expectations (`opacity`) stay valid and gain height checks.

## TDD

- Domain/app tests: N/A (no server data).
- E2E (Playwright via `LiveServerTestCase`): `tests/e2e/test_tatib_entry_controls.py` — rest state
  reserves no space; hover/focus expands both rows; a revealed row stays enterable; touch media
  shows rows; `tests/e2e/test_entries.py` and `tests/e2e/test_reorder.py` regressions for the rows
  they click through.

## Risks

- **Collapsed row unreachable on the way out.** If the row collapses instantly on mouseout, the
  pointer that was travelling onto it lands on the next entry, which then reveals *its* rows — a
  flicker chase. Mitigated by keeping the hide transition (the box exists until it ends).
- **Focus landing invisibly.** Tabbing into a still-collapsed row's button must expand the row
  before focus is read; `:focus-within` covers it, but the E2E must assert it.
- **Wrapped buttons.** At narrow widths the row wraps to two lines (~71px); the grid collapse
  handles any height, but visual confirmation at both widths is part of the tasks.
