# Research: song entry modal scrollbar

**Spec**: `specs/236-song-modal-scrollbar/spec.md`
**Unknowns remaining**: 0

## D001 — Where the fix belongs

- **Decision**: change the shared `.editor` rule in `static/styles/design/components.css` to
  `overflow: clip`; leave templates, scripts and endpoints untouched.
- **Rationale**: the measured overflow is on the `<dialog>` (`clientHeight 246`, `scrollHeight 256`,
  `offsetWidth - clientWidth = 5px`), while `.editor__content` is already `246/246` and
  `overflow-y: auto`. The dialog is the wrong scrollport; removing it as one fixes the reported
  surface without moving scrolling into the form.
- **Alternatives considered**: hiding the collapsed verse panel with `display: none` would break
  the deliberate `grid-template-rows: 0fr` reveal animation; hiding the scrollbar with
  `scrollbar-width: none` leaves a programmatically scrollable dialog and does not fix the cause.
- **Provenance**: research — live measurement on the base commit and the CSS rule at
  `components.css:2720-2733`.

## D002 — `clip` over `hidden`

- **Decision**: use `overflow: clip`, not `overflow: hidden`.
- **Rationale**: `clip` makes the dialog a non-scrollport with no programmatic `scrollTop`, while
  `hidden` still creates a scroll container; the requirement is that the dialog never scrolls.
- **Alternatives considered**: `hidden` passes a screenshot but leaves the underlying fault and
  can still be scrolled by script or focus; `visible` would paint clipped descendants outside the
  rounded corner.
- **Provenance**: research — browser readout in the static preview: after `clip`, gutter `0px`,
  computed `overflow-y: clip`, `scrollHeight` still `256px`.

## D003 — Verification depth before the push step

- **Decision**: one targeted E2E module measures the new/edit geometry and tall-form scrolling;
  the full browser suite is deferred to the push step.
- **Rationale**: a one-declaration CSS change has a narrow blast radius; the owner asks for
  targeted verification between pushes and heavy suites at push.
- **Alternatives considered**: running the whole E2E suite now would repeat unrelated red tests
  already recorded on `develop` and would not add evidence for this rule.
- **Provenance**: owner decision; research inconclusive.

## D004 — Preview shape and the chat frame

- **Decision**: keep the static preview and make it one self-contained HTML file; verify it with
  the chat-frame reproduction script before using `::preview`.
- **Rationale**: the chat frame sets the file text on a sandboxed `srcdoc` iframe with an opaque
  origin, so relative `<link>` and `<script src>` never resolve. The first build linked four CSS
  files and parsed zero rules there; inlining them yields one parsed stylesheet and a PASS.
- **Alternatives considered**: a live preview would need a dev server and would not be portable
  inside the chat frame; a screenshot is not a preview.
- **Provenance**: research — frame verifier FAIL before, PASS after inlining.

## Open

None.
