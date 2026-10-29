# Research: The Transfers scrollbar sits at the dialog's edges

**Spec**: `specs/152-transfer-scrollbar-edge/spec.md` (revision 2)
**Unknowns remaining**: 0

## D001 — The list takes the dialog's padding as a negative margin, and pads its own content back

- **Decision**: one rule beside the existing list rule in `static/styles/design/components.css` —
  `.media-transfers__list { margin: 0 -22px -22px; padding: 0 22px 22px; }`.
- **Rationale**: the bar is painted by the engine against the scroll container's border box, so the
  only way to move it without moving the content is to move the *box* and re-inset the content. The
  dialog's `padding: 22px` and its 1px border are what stand between the list's box and the dialog's
  edge; a negative margin equal to that padding on the right and the bottom puts the box's right and
  bottom edges on the dialog's inner border, and the same value as `padding` puts every child back on
  the x and y it already has. Measured on the live app (headed Chromium, 1440×760): the list's box
  moves 453→987 to 431→1009 and its bottom 683.8 → 705.8, the rows stay at 453→982 and the list's top
  at 117.2, and the painted gap between the bar and the dialog's right border goes 22px → 0px.
- **Alternatives considered**: (a) move the dialog's `padding` onto the list and give the dialog
  `padding: 0` — the title would have to be re-inset by hand, and the dialog would lose the padding
  every other child leans on; (b) `margin-right` only — leaves the bar stopping 23px short of the
  bottom border, which is the half of the report revision 2 added; (c) a negative margin on the
  `::-webkit-scrollbar` pseudo element — it has no box model, so there is no margin to set;
  (d) paint a fake bar as a `position: sticky` element — re-implements the engine's thumb, its hover
  state and its scroll coupling.
- **Provenance**: research

## D002 — The right and bottom edges move; the top does not

- **Decision**: the list's top margin and padding stay `0`. The bar keeps starting 14px under the
  `Transfers` title.
- **Rationale**: reaching the dialog's top border means the scroll area has to cover the title — the
  title would move inside the scroll container and become a pinned (sticky) line, which changes what
  spec 149 fixed and what the dialog's markup is. Asked at gate 1 and settled by the owner: "Bottom
  edge only — the bar still starts under the title, but reaches the dialog's bottom border."
- **Alternatives considered**: `margin-block: -22px` on both ends — measured on the live app, the
  list's box then starts at y 95.2, 8px *above* the title's bottom, so the lane would run beside the
  title's last line; rejected. The full-height variant (title inside the scroll area, pinned) is the
  option the owner did not take.
- **Provenance**: `owner decision`, gate 1 revision, 2026-10-29

## D003 — No reserved gutter

- **Decision**: `scrollbar-gutter: stable` is **not** added.
- **Rationale**: today the rows sit at 982 (28px from the dialog's right border) while the list
  scrolls and at 987 (23px) while it does not — the 5px the classic bar takes. Reserving the gutter
  would give both states 982, at the cost of moving the short list's rows 5px inwards, which is more
  than the report asks. Measured on the preview's two-row state: with the gutter, the row's right edge
  is 28px from the dialog's border; without it, 23px — today's number.
- **Alternatives considered**: `scrollbar-gutter: stable` (rejected as above); `overflow-y: scroll`
  (draws a disabled track on a short list, and spec 149 chose `auto` deliberately).
- **Provenance**: research

## D004 — The bar's own drawing is untouched

- **Decision**: the slice sets no `::-webkit-scrollbar*` property and no `scrollbar-width` /
  `scrollbar-color`. It relies on spec 087's global rules.
- **Rationale**: those two mechanisms must not both be in play (spec 087's finding: in Blink the
  standard properties win and the platform's 10px bar with stepper glyphs is painted instead). The
  bar this slice moves is already the app's 5px `--scroll-thumb` bar; moving the box moves it too.
- **Alternatives considered**: a dialog-specific bar width — would fragment the app's one bar style.
- **Provenance**: research

## D005 — The dialog clips its content to its rounded border

- **Decision**: `.media-transfers__dialog { overflow: clip; }` joins the dialog's own rule block.
- **Rationale**: the list is a rectangular child inside a 12px-radius dialog. With its box now
  reaching the bottom-right corner, the bar's last pixels painted *over* the radius — photographed on
  the live app before the clip: the thumb ran straight through the curve and out past it. `overflow:
  clip` clips descendant painting to the rounded padding box without creating a scroll container, so
  the corner is clean and the dialog cannot be scrolled programmatically by a focus move. Measured
  after: the dialog reports `overflow: clip`, `scrollHeight − clientHeight` stays 0, and the thumb's
  tip is cut by the curve.
- **Alternatives considered**: `overflow: hidden` (same clipping, but turns the dialog into a scroll
  container — verified to work, `scrollHeight − clientHeight` 0, but it invites a future focus scroll
  that `clip` forbids); a smaller corner radius (changes the dialog's shape); stopping the lane 12px
  short of the bottom (fails the report).
- **Provenance**: research

## D006 — The list's `padding-bottom` carries spec 149's end-of-scroll gap

- **Decision**: the 22px that keeps the last row clear of the dialog's bottom border at the end of the
  scroll moves from "the dialog's padding outside the list" to "the list's own `padding-bottom`".
- **Rationale**: the list's box now ends at the dialog's inner border, so the dialog's bottom padding
  is no longer between the last row and the border. A scroll container's bottom padding is part of its
  scrollable area, so it restores the same 22px at the end of the scroll. Measured: the last row's
  bottom at the end of the scroll is 684.2 inside a list whose box ends at 705.8 — 21.6px of padding,
  and 22.6px above the dialog's border, identical to develop's number. The scroll thumb's length
  changes by the same 22px of extra scroll extent, which is not measurable at this row count.
- **Alternatives considered**: leaving the gap out (spec 149's contract breaks and the last row's
  border lands on the dialog's border — the fault spec 149 fixed).
- **Provenance**: research

## D007 — The E2E asserts the box and the lane, not the paint

- **Decision**: the Playwright tests (headless, as the suite runs) assert the list's box against the
  dialog's border box, the row's insets, the short-list state and the unmoved frame. The painted gap
  is measured by `preview/probe.py` in a **headed** Chromium and recorded in `converge.md`.
- **Rationale**: headless Chromium on this machine paints overlay scrollbars — measured on the same
  page: `offsetWidth − clientWidth` is **0** headless and **5** headed, and no thumb is painted at all
  in the screenshot. A headless test therefore cannot see the bar, and a test that asserted "the bar
  is at the edge" there would be asserting nothing. What a test *can* pin is the mechanism: the
  container's box reaches the dialog's inner border, and the lane (when the engine takes one) is the
  outermost part of that box. The painted outcome is verified by the probe, quoted with its columns.
- **Alternatives considered**: launching the suite's browser non-headless for these tests — would
  make the module depend on a display server and change how every other test in it runs; a
  screenshot-diff fixture — the paint is fully determined by the box and the lane arithmetic the DOM
  assertions already read.
- **Provenance**: research

## D008 — The rules sit beside the rules they amend, and nothing else changes

- **Decision**: the list's rule joins the existing `.media-transfers__list` line and the clip joins
  `.media-transfers__dialog` in `components.css`; no template, JavaScript, class or markup change.
- **Rationale**: spec 149 already gave the element its class and its `overflow-y: auto`; the slice
  corrects its box and the dialog's painting. Keeping the declarations on the same lines is what lets
  the next reader see the whole of the dialog's drawing in one place. `git diff --stat` should show one
  file outside the spec pack and the test module.
- **Alternatives considered**: a new wrapper element — a template change for a box that already
  exists.
- **Provenance**: research

## Open

<!-- empty: Phase 0 finished, nothing blocks Phase 1 -->
