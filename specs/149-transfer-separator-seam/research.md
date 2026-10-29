# Research: The Transfers list draws each boundary once

**Spec**: `specs/149-transfer-separator-seam/spec.md`
**Unknowns remaining**: 0

## D001 — The duplicate line is removed from the row, not from the divider

- **Decision**: the row above the divider drops its own border —
  `.media-transfers__row:has(+ .media-transfers__divider) { border-bottom-width: 0; }` — and the
  `<hr class="media-transfers__divider">` stays the seam's only line, at its existing 2px and
  `margin: 9px 0`.
- **Rationale**: the divider's *existence* is decided in `static/web/media-handoff.js` from the
  session state (`52-57`); keeping the element and removing the row's border leaves that script
  untouched and puts the drawing fix in the stylesheet that draws. `:has()` is already used by this
  stylesheet (`.editor[open]:has([data-entry-form="media"])`), so no new platform requirement is
  introduced. Measured on the preview: two painted lines 10.5px apart → one 2px line.
- **Alternatives considered**: (a) a JavaScript class on the row above the divider — moves a drawing
  decision into the script, which would then have to know its own sibling's styling; (b) delete the
  `<hr>` and give the first unseen row `border-top: 2px` — the preceding row's 1px border would then
  touch it (3px together) and still need suppression, and a top border cannot carry the 9px of
  breathing space without extra padding; (c) make the divider 1px and keep both — still two lines.
- **Provenance**: research

## D002 — The list becomes the scroll container; the dialog keeps its `max-height`

- **Decision**: `.media-transfers__dialog { display: flex; flex-direction: column; }` and
  `.media-transfers__list { min-height: 0; overflow-y: auto; }`.
- **Rationale**: the dialog's own `max-height: min(86vh, 46rem)` and `padding: 22px` are unchanged, so
  the title stays put and the list's box ends exactly at the padding edge. Measured: the list ran
  19px past that edge at nine rows and 451px at fifteen; with the two rules it is 0px in both, and
  the list carries 18px / 450px of scroll. `min-height: 0` is what lets a flex child shrink below its
  content height.
- **Alternatives considered**: `overflow: auto` on the dialog — the title would scroll away with the
  rows, and the dialog's own padding would still be overrun; a fixed pixel height on the list — the
  dialog is sized in `vh`/`rem`, so a pixel height would drift at other viewports.
- **Provenance**: research

## D003 — The seam keeps its 2px weight

- **Decision**: the seam is one 2px `--divider` line, not a 1px separator equal to the row borders.
- **Rationale**: the divider marks transfers that finished after this session started; at 1px it would
  be indistinguishable from every row boundary and the grouping would be lost with the second line.
  The gap (9px either side) is what carries the break; the weight keeps it legible.
- **Alternatives considered**: a plain 1px line (offered at gate 1 and not taken).
- **Provenance**: `owner decision; research inconclusive` — the owner accepted the drafted 2px at gate 1.

## D004 — The list takes a class; the `id` stays the script's hook

- **Decision**: add `media-transfers__list` to `<div id="mediaTransfersList">` in
  `multimedia/web/templates/reading/base.html` and style the class.
- **Rationale**: this stylesheet styles classes; the id remains what `media-handoff.js` queries
  (`$('mediaTransfersList')`). A rule on `#mediaTransfersList` would work but couples the stylesheet to
  an identifier the script owns.
- **Alternatives considered**: `#mediaTransfersList` selector; styling `#mediaTransfersDialog > div`
  (breaks as soon as a second child is added).
- **Provenance**: research

## D005 — Verification runs through the existing fake-companion E2E harness

- **Decision**: four Playwright tests in `tests/e2e/test_media_library.py`, reusing its
  `page.route('http://127.0.0.1:63174/**', companion)` fake and the rail button.
- **Rationale**: the behaviour is DOM and CSS; the seam only exists when the client's session state
  says so, which a template test cannot produce and a unit test would only restate as a selector
  string. The harness already serves `/status`, `/transfers` and `/files` from a mutable dict, so
  flipping one job from `active` to `completed` is enough to create the session and its divider.
- **Alternatives considered**: a pixel-diff assertion on a screenshot (the paint is fully determined by
  the border widths and boxes the DOM assertions read, so it would add a fixture, not evidence);
  `test_design_tokens.py` (no new token is introduced).
- **Provenance**: research

## D006 — When the divider exists is not part of this slice

- **Decision**: the `session` / `viewed` / `separated` logic in `media-handoff.js` is not touched.
- **Rationale**: the report is a drawing fault. Changing which transfers the divider separates would
  change the meaning of the list, which the spec keeps out of scope.
- **Alternatives considered**: dropping the divider entirely (loses the grouping the owner's earlier
  request asked for).
- **Provenance**: research

## Open

<!-- empty: Phase 0 finished, nothing blocks Phase 1 -->
