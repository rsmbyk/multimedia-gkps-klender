# Implementation Plan: the add bar opens over the seam, and nothing moves

**Spec**: `specs/143-add-bar/spec.md`
**Branch**: `feat/143-add-bar` (rebased on `develop` @ `38507a35`; implementation commit `77f36a3c`)
**Bump**: `patch`
**Preview**: live — `/tatib/142/`, `/tatib/144/` (see `preview/README.md`; the change is motion)

## Technical Context

| Field | Value |
| --- | --- |
| Language / version | CSS (`static/styles/design/components.css`) and ES5-style JS (`static/web/entries.js`); no Python, template or migration change |
| Primary dependencies | none added — the existing tokens (`--focus`, `--divider`, `--ink`, `--canvas`) and the existing `.entry__add` / `.entry__start` class names |
| Storage | none |
| Testing | Playwright (Python) E2E via `StaticLiveServerTestCase`: `tests/e2e/test_tatib_entry_controls.py` (the 11 tests that encode the reveal model), `tests/e2e/test_tatib_hover.py` (the start-bar shift) |
| Target platform | every width the Tata Ibadah stage draws at, both themes, plus touch (no hover) |
| Project type | server-rendered Django web app, no build step |
| Performance goals | no request; the bar is one absolutely positioned element per row, no extra selector depth over 250 nodes |
| Constraints | the entry's own controls keep the right-hand column (spec 140) and must stay hit-testable; the rows must stay keyboard-reachable; the section break's rule is the only rule in the service that means something |
| Scale / scope | 1 stylesheet block, 1 JS function, 12 E2E tests rewritten |

## Constitution Check

No `CONSTITUTION.md` exists (SDD-01: optional, never auto-created), so the check is not applicable.
The repo's constraints — the `stage-pane` container query that reserves the controls' column, the
`(hover: none)` exemption for touch, `prefers-reduced-motion`, and the design tokens rather than
literals — are honoured in the design below.

Re-checked after Phase 1: pass. The slice adds no route, no stored value, no dependency; it removes
a layout shift and keeps every existing surface's behaviour.

## Phase 0 — Research

See `research.md`. **Unknowns remaining: 0.**

## Phase 1 — Design

- `data-model.md` — the three objects this slice defines: the row (a 20px slot), the seam line, and
  the bar (34px, `max-content`, centred on the slot).
- `contracts/` — `none` (no endpoint, payload, template variable or stored value).
- `quickstart.md` — the live server, the states to click, and the E2E command.

The design in one paragraph: `.entry__add` and `.entry__start` become `position: relative` boxes with
`height: 20px` and no padding, so the space they occupy is exactly the gap the entries already had;
their `.entry__add-inner` / `.entry__start-inner` becomes `position: absolute; left: 50%; top: 50%;
transform: translate(-50%, -50%); width: max-content; height: 34px`, revealed by opacity only. The
1px seam line moves from the bar to the row's `::before`, so it spans the column while the bar's hit
area stays as wide as its buttons. `entries.js` keeps revealing the rows above and below an item —
the only script change is that the start bar is a neighbour again after being briefly excluded.
Twelve E2E tests that encode the in-flow reveal are rewritten to assert the new contract.

## Traceability

| Requirement | Component / file | Verified by | Notes |
| --- | --- | --- | --- |
| FR-001 | `components.css` (row + bar rules) | `test` → `test_tatib_entry_controls.py::…::test_opening_a_row_moves_nothing` (new, replaces `test_a_revealed_row_keeps_equal_gaps_above_and_below`) | sweep of eight entries, 0.0px each, page height unchanged |
| FR-002 | `components.css` | `test` → `…::test_the_row_keeps_its_slot_and_the_bar_floats_over_it` (replaces `test_at_rest_the_rows_and_the_bar_reserve_nothing`) | slot 20px, bar absolute, 34px |
| FR-003 | `components.css` (`::before` rules) | `test` → `…::test_the_seam_is_a_hint_at_rest_and_brightens_when_opened` | computed opacity .15 / .6, colour `rgb(141,165,147)` |
| FR-004 | `components.css` (bar width + line on the row) | `test` → `…::test_the_bar_does_not_cover_the_entry_controls` | `elementFromPoint` at the Edit button's top edge and middle |
| FR-005 | `entries.js` (`neighboursOf`), `components.css` (`:hover`, `:focus-within`) | `test` → `…::test_hovering_an_item_reveals_the_add_rows_around_it`, `…::test_tabbing_into_a_collapsed_row_expands_it` (both rewritten), `test_tatib_hover.py::…::test_the_start_bar_opens_with_the_first_entry` | keyboard and pointer both reach every row |
| FR-006 | `components.css` (button rules) | `test` → `…::test_a_hovered_button_is_solid_and_opaque` | computed `border-style: solid`, `background-color: rgb(230,228,224)` |
| FR-007 | `components.css` (row height, head margin, break margin) | `test` → `…::test_the_first_seam_matches_the_others` (replaces `test_the_start_bar_collapses_and_reveals_with_equal_gaps`) | 53px ink both sides, 20px gaps, 8px break margin |
| FR-008 | `components.css` (`.tatib__eos` rule) | `test` → `…::test_the_divider_takes_the_same_box` (rewritten for the muted colour) | `rgb(228,226,219)`; box, rule and diamond otherwise unchanged |
| SC-001…SC-006 | — | the tests above, one per criterion | see `spec.md` §Success Criteria |

**Verification split**: 8 test · 0 inspection · 0 manual

## Complexity Tracking

No violation to justify. The slice removes a `.is-revealed` layout transition and a pointer-coordinate
guard's reason to exist; it adds one absolutely positioned element per row, which is the cheapest
form of "drawn over" available without a second stacking context.
