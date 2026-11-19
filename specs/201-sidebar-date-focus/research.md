# Research: a clicked service keeps its date

**Spec**: `specs/201-sidebar-date-focus/spec.md`
**Unknowns remaining**: 0

## D001 — Which focus hides the date and the Today badge

- **Decision**: hide them when the row is hovered, or when `.row-edit:focus-visible` /
  `.row-delete:focus-visible` matches — the exact reveal the two controls use at
  `static/styles/design/components.css:487-505`.
- **Rationale**: the report is a click on the row's link. That focus makes `li:focus-within` true
  while no control is revealed, which is why the date disappears with nothing up to explain it.
  The control rules already reject `li:focus-within` for the mirrored problem (comment at lines
  484-486). The capability tree's wording — "focused for that reveal" (`reading/R41`) and "its
  actions take focus" (`reading/R9`) — means action focus, not link focus.
- **Alternatives considered**: keep `li:focus-within` and clear focus on click in `reading.js`
  (a script change for a CSS state, and it would break keyboard navigation); use
  `.row-edit:focus-visible ~ .book .book__s` (the buttons come *after* the link in the DOM, so a
  following-sibling combinator cannot reach it); track a class in JS on every focus/blur (new state
  to keep in sync).
- **Provenance**: research — base `92edc752`, `components.css:471-505,1435-1445`, the accepted
  preview (`preview/probe.py`) and the live reproduction.

## D002 — How to express "an action button is focused" in CSS

- **Decision**: `li[data-editor-kind]:has(> .row-edit:focus-visible, > .row-delete:focus-visible)`
  as a second selector beside `li[data-editor-kind]:hover`.
- **Rationale**: `:has()` with a selector list is already used in this stylesheet
  (`#panelBody li:has(> .row-delete)`, line 3237), so the feature is established in the product's
  browser targets. The list covers either control without duplicating the declaration block.
- **Alternatives considered**: two separate `:has()` selectors (same result, longer); putting a
  marker class on the `li` from JS (unnecessary state).
- **Provenance**: research — stylesheet inspection at base `92edc752`.

## D003 — How to test a `@media (hover: hover)` rule in headless Playwright

- **Decision**: the E2E reads the shipped selector from the same-origin stylesheet and asserts
  the proposed selectors are present and `:focus-within` is absent, then injects those same
  selectors outside the media guard so real pointer hover and real keyboard focus can be driven
  and the computed `display` asserted.
- **Rationale**: on this machine the app's HTTP origin reports `(hover: hover)` as false in
  headless Chromium while a `file://` page reports true, so the guarded rule never applies in a
  LiveServerTestCase browser; an E2E that only reads computed style would pass before the fix.
  Injecting the selector text keeps the behavioural assertion on the real DOM states.
- **Alternatives considered**: skip the browser test and check the CSS text only (would not prove
  click, hover or focus behaviour); launch Chromium with blink hover flags (tried, no effect on
  the app's HTTP origin).
- **Provenance**: research — Playwright probe matrix, 2026-11-19 (see spec preview `probe.py`).

## Open

<!-- empty when Phase 0 is finished -->
