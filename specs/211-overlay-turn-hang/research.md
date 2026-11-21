# Research: a speaker's turn hangs under its words

**Spec**: `specs/211-overlay-turn-hang/spec.md`
**Unknowns remaining**: 0

## D001 — The row builder owns the continuation decision

- **Decision**: in `plate()` (`static/web/obs-overlay.js:118-137`) pre-scan `model.lines` once for a
  painted mark (`line.mark && line.words`). A row with no mark and a non-empty voice gets
  `is-continuation` only when that screen-wide flag is true. No other file classifies a line.
- **Rationale**: `voices.voice_lines` already carries the voice across blank lines and screen
  breaks; `_screen_lines` hands the overlay `text`, `voice`, `mark` and `words` for each line
  (`multimedia/web/reading/views.py:1579-1588`). The row builder is the only place that knows both
  the per-line voice and which marks this screen actually paints.
- **Alternatives considered**: a server-side `continuation` flag would duplicate the voice
  contract in the projector payload and change a stable interface for a paint-only rule; asking
  the DOM after insertion (`querySelector('.obs-overlay__speaker')`) would couple the class to
  measurement order.
- **Provenance**: research (source read on base `7a0e7069`)

## D002 — An indent, not a second grid

- **Decision**: `static/styles/design/obs-overlay.css` gains one rule beside `.has-mark`:
  `.obs-overlay__line.is-continuation { padding-left: calc(var(--speaker-col, 0px) + .45em); }`.
  The text node and the `is-leader` / `is-join` class stay as they are.
- **Rationale**: `.has-mark` is `grid-template-columns: var(--speaker-col, max-content) minmax(0, 1fr)`
  with `column-gap: .45em` (lines 206-211), and `applySpeakerColumn` sets one `--speaker-col` on
  the body from the widest painted mark (lines 222-229). The same column plus the same gap gives
  the first glyph exactly the words x. `padding-left` needs no empty mark cell, so no span is added
  and the wrapped rows inherit the indent. The static preview approved at gate 1 uses this rule.
- **Alternatives considered**: copying the grid onto the continuation would need a dummy empty
  mark span (a DOM and screen-reader change for no visual gain); a fixed px indent would break the
  stage's cqw type scale; deriving the column in CSS with `:has()` would re-measure rather than
  reuse the sheet's single authoritative variable.
- **Provenance**: owner decision (rule shape, gate 1) + research

## D003 — No painted mark means no indent

- **Decision**: no `is-continuation` class when the screen has no mark with words; the CSS fallback
  is `0px`, so even an otherwise-classed row has no indent without a measured column.
- **Rationale**: a screen can begin mid-turn because voices are classified over the whole body
  before `_line_pairs` chunks it (`views.py:1591-1613`). With no mark there is no column to share;
  the plate's content edge is the correct x (FR-003, FR-004). `applySpeakerColumn` already sets the
  variable only when `widest` is non-zero, so both guards agree.
- **Alternatives considered**: indenting every voiced line by a fixed em — it would move ordinary
  text on mid-turn screens and cues' neighbours that the owner did not report.
- **Provenance**: owner decision (no-mark control in the approved preview) + research

## D004 — The seam is the existing overlay E2E module

- **Decision**: add focused Playwright tests to `tests/e2e/test_obs_overlay.py`. Add small TEXT
  fixtures to `setUp` and one helper that clicks the nth `.screenerow`, leaving the three existing
  entries and their screen indices untouched.
- **Rationale**: the outcome spans the projector payload, the row builder and the real stylesheet;
  only the live overlay proves the glyph x. The module already measures mark/words rectangles
  (`test_a_wrapped_speaker_line_hangs_under_its_words`) and runs at 1280×720. A third line on the
  first text would pair onto a second screen under MULTI_LINE, so the cases need their own entries;
  a single-screen fixture is needed where the new `J.` answer must share the first screen.
- **Alternatives considered**: a DOM-only JS unit test would not resolve `cqw` type or the grid;
  a new E2E module would duplicate the dock/overlay harness.
- **Provenance**: research

## D005 — Bump, board and Fold

- **Decision**: `bump: patch` (unchanged from the card). At Fold, modify `overlay/R5` in
  `docs/spec/overlay.md`: keep its existing scenarios and add the continuation rule and a scenario
  for the inline mark's continuing line. ITEM-223 stays in Speccing until the owner promotes it to
  Ready; ITEM-224 keeps the token-alone shape on the board.
- **Rationale**: a visible correction to an existing overlay behaviour, like the neighbouring
  overlay fixes; R5 already owns the mark column, so this is a modification rather than a new
  requirement (SDD-03).
- **Alternatives considered**: a new `overlay/R<n>` would split one column rule across two IDs;
  `none` would leave a user-visible change unversioned.
- **Provenance**: research

## D006 — Measurement timing is unchanged

- **Decision**: do not add a `document.fonts.ready` re-measure. `applySpeakerColumn` runs after
  `stage.replaceChildren(node)` on every paint and again on resize with the current plate
  (`obs-overlay.js:272-306, 437-442`).
- **Rationale**: the continuation reads the same variable the marked words already use; if the
  measure were stale, both would be wrong together and this slice would not introduce the fault.
  The existing E2E waits for the plate and the bundled faces, so the geometry under test is the
  painted one.
- **Alternatives considered**: re-running the measurement on font load would change an unrelated
  timing path and is not needed to make the two x values agree.
- **Provenance**: research

## Open

<!-- empty when Phase 0 is finished; anything here blocks Phase 1 -->
