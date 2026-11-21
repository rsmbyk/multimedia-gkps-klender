# Research: a slot states the kind it resolves to

**Spec**: `specs/213-slot-kind-badge/spec.md`
**Unknowns remaining**: 0

## D001 — Where the badge's markup lives

- **Decision**: a new partial `multimedia/web/templates/reading/_slot_kind_badge.html`, included from
  `_slot_mark.html`, which `tatib.html` already includes for a slot row.
- **Rationale**: `_slot_mark.html` is already the one place a slot's mark is drawn, and it already
  branches on the row's own kind (`fill_in` / `choice`). Adding the badge there keeps one include site
  and one file to read. `tatib.html` already passes `item.slot_kind` (the resolved kind, lowercased)
  into the row's `data-slot` attribute, so it needs one added argument and nothing else.
- **Alternatives considered**: (a) inline the badge in `tatib.html`'s row template — puts SVG path data
  in an already-dense one-line template; (b) extend `_entry_kind_icon.html` with the four slot kinds —
  that partial is spec 144's *entry* mark, drawn in the 24-unit stroke language at 20px, and a slot's
  badge is a different size and seat; sharing it would force one of the two to compromise.
- **Provenance**: research (`grep -n "slot__mark\|slot_kind" multimedia/web/templates/reading/*.html
  multimedia/web/reading/views.py`).

## D002 — Server-rendered, from the row's resolved kind

- **Decision**: the badge is drawn by the template from `fill_kind`; no script injects it.
- **Rationale**: `views.py` already resolves the slot's kind for the row (`slot_kind`, used for
  `data-slot` and the `Fill-in · Song` label). The kind is a fact at render time, so a script would be
  a second source that can disagree with the label beside it. Spec 144 made the same call for its kind
  marks, and the media chip's script exists only because a media family is a client-side fact.
- **Alternatives considered**: a client script keyed on `data-slot` — rejected: it would leave the
  badge absent until script runs, and the row already carries the value.
- **Provenance**: research (`multimedia/web/reading/views.py:1407-1409`, `:1468`).

## D003 — The four glyphs, and why they are redrawn rather than reused

- **Decision**: four glyphs on a **12-unit** viewBox at `stroke-width: 1.6`:
  song `M4.5 8.7V2.8l5.1-1v5.8` + two r1.2 noteheads · scripture an open book
  (`M6 4.8c-.8-.65-1.9-.95-3.45-.85v5.2c1.55-.1 2.65.2 3.45.85.8-.65 1.9-.95 3.45-.85V3.95c-1.55-.1-2.65.2-3.45.85z`
  + `M6 4.8v5.2`) · media a rounded frame with a play mark
  (`rect 1.6 2.6 8.8 6.8 rx1.2` + `M5.1 4.7v2.6l2.2-1.3z`) · text three rules
  (`M2.4 3.4h7.2M2.4 6h7.2M2.4 8.6h4.3`).
- **Rationale**: the product's own marks are 24-unit viewBoxes drawn at 20px, i.e. 1.8 stroke at 0.833
  scale. Scaled to a 10px box the same geometry strokes at **0.75 device px** — under a pixel, so every
  glyph greys out into a smudge. Redrawing on a 12-unit grid keeps the stroke at 1.6 units of a box
  that renders at 10px, i.e. **1.33 device px**, which still resolves. The three non-song glyphs reuse
  the product's existing shapes at that grid: the song note and the text lines are the add-bar's own
  glyphs (`tatib.html` empty-state tiles), and the media frame-and-play is the **Add Media** tile's
  glyph — not the media chip's per-family glyphs, because a media slot resolves to a *family*, not to
  one file.
- **The book drops the cross it carries at full size.** `_entry_kind_icon.html`'s scripture glyph has a
  cross above the panels (`M12 2.6v4.6M10.1 4.5h3.8`). At 10px that cross is ~1.6px of stroke in a
  1.3px-wide space: it merges into the spine and reads as a blob. The two panels plus the spine are
  what make a book at this size.
- **Alternatives considered**: (a) reuse `_entry_kind_icon.html`'s paths verbatim — measured, strokes
  fall under a pixel; (b) a 24-unit grid with `vector-effect: non-scaling-stroke` — that pins the
  stroke to device pixels but leaves the *geometry* scaled, so the note's two noteheads collapse into
  each other; (c) letters (`S`, `P`, `M`, `T`) — the repo has no letter-mark precedent and a letter is
  not a kind mark.
- **Provenance**: research (`multimedia/web/templates/reading/_entry_kind_icon.html`,
  `static/styles/design/components.css:2081-2087` (`.entry__kind-icon`),
  `multimedia/web/templates/reading/tatib.html:145-160` (the empty-state tile glyphs)).

## D004 — The disc's fill, and the row's fill states

- **Decision**: the disc paints `--canvas` at rest, and repaints the row's own `--icon-hover-bg` over
  it in the row's four fill states (`:hover`, `.is-modal-origin`, `:focus:not(.focus-restore-quiet)`,
  `:has(:focus:not(.focus-restore-quiet))`) as a `linear-gradient` background-image.
- **Rationale**: the badge sits *on* the mark, which sits inside the row, so whatever is behind the
  badge is the row's own background. A disc of plain `--canvas` on the row's 8–9 % tint reads as a
  hole punched through the row — seen at 8× on the real page, in both themes. Re-laying the same
  `--icon-hover-bg` over the canvas makes the two composite to the same value by construction, rather
  than by a second hand-matched colour that drifts when the token moves. A `linear-gradient` is the
  only way to stack a second background over `background-color` without touching the colour the
  contrast check reads.
- **Alternatives considered**: (a) leave the disc transparent and let the frame show through — the
  dashed frame would run under the glyph and turn it to noise; (b) `color-mix` the canvas toward the
  tint — a second colour to keep in step; (c) `background: inherit` — the row's background is
  `--icon-hover-bg` only in those states and `transparent` at rest, and a transparent disc on the
  canvas is the same picture, but it also inherits *nothing* of the mark's stacking context, so the
  frame would show through.
- **Provenance**: research — measured on the live page in both themes; the hole is visible in
  `preview/shots/hover-<theme>-8x.png` before the fix and gone after.

## D005 — The frame's own sizing rule must not catch the badge

- **Decision**: `#read .slot__mark svg` becomes `#read .slot__mark > svg`.
- **Rationale**: that rule stretches the mark's frame to the full 20px box. As a descendant selector it
  also matched the badge's own `<svg>` — which sits *inside* `.slot__mark` — and would have blown the
  10px glyph up to 20px, filling the 13px disc and spilling past it. The child combinator keeps the
  frame's rule on the frame and leaves the badge's own `width/height` in charge.
- **Alternatives considered**: `:not(.slot__badge) > svg` — same effect, noisier; sizing the badge's svg
  with `!important` — hides the collision instead of removing it.
- **Provenance**: research (`static/styles/design/generate.css`, the `#read` block; the collision was
  found by reading the cascade, and the corrected selector is what the preview and the page both run).

## D006 — The glyph's paint is declared on the template, not only in CSS

- **Decision**: the badge's `<svg>` carries `fill="none" stroke="currentColor" stroke-linecap="round"
  stroke-linejoin="round"` as attributes, like `_slot_mark.html`'s frame.
- **Rationale**: this is a defect found on the live page, not a preference. The first implementation
  declared the paint only in the preview's own stylesheet and not in the product's rule, so the shipped
  badge's `<svg>` fell back to `fill: rgb(0,0,0)` / `stroke: none` — a black blob on a near-black disc,
  i.e. **invisible**, while the preview page (which carried its own rule) looked correct. Measured
  `getComputedStyle(svg)` on the live page before the fix: `{fill: rgb(0,0,0), stroke: none}`; after:
  `{fill: none, stroke: rgb(156,154,145)}`. Attributes on the element make the glyph's paint
  independent of which stylesheet happens to load.
- **Alternatives considered**: rely on the CSS rule alone — the state that shipped the bug.
- **Provenance**: research — `preview/probe_adopted.py`'s paint readout, and the pixel maps in
  `preview/shots/glyph-*.png`.

## D007 — No new test module; the badge is covered by the existing stage suites

- **Decision**: no new E2E module. The badge is asserted inside the existing template-page coverage,
  and one new E2E test in `tests/e2e/test_tatib_templates.py` proves the behaviour that is new.
- **Rationale**: the repo's browser suite already has `test_tatib_templates.py` for this page and
  `test_stage_kind_marks.py` for the mark rail (spec 144). A third module would duplicate the fixture
  (a template with slots) a third time. The new behaviour — a badge per slot, four distinct glyphs, the
  mark unchanged — is one test with several assertions, plus a unit test for the legacy no-`fill_kind`
  row that the local data cannot produce.
- **Alternatives considered**: a `test_slot_kind_badge.py` module — rejected as a third copy of the
  same fixture.
- **Provenance**: research (`tests/e2e/test_tatib_templates.py` fixtures `open_rich`/`_template_with_slots`;
  `tests/e2e/test_stage_kind_marks.py`).

## Open

<!-- empty: Phase 0 finished, zero unknowns -->
