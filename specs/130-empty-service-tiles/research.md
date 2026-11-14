# Research: An empty Tata Ibadah is centred, and its five kinds are tiles

## D1 — Where "centred on the page" is measured

**Decision**: the block is centred between the header's bottom edge and the bottom of the window, and the
header's 30px bottom margin (22px below tablet width) plus the read body's 8px top margin are dropped in this
state only.
**Rationale**: measured at 1440×900, the reading body starts at 150.7px and the window ends at 900px; keeping
the two margins put the block 19px below the centre of the visual area, because both margins are the page's
header-to-content gap and neither has content to separate once the page is empty. With them dropped the gaps
measure 318.6px above and 318.7px below.
**Alternatives**: absolute positioning against the stage — takes the block out of flow and breaks the short
column case; a fixed `padding-top` — a magic number that fails at every other window height.
**Provenance**: `static/styles/design/components.css:1113` (`.read__body`), the running branch, measured with
`specs/130-empty-service-tiles/quickstart.md`.

## D2 — How the article gets the stage's leftover height

**Decision**: `.read` becomes `display: flex; flex-direction: column; min-height: 100%` and `.read__body`
takes `flex: 1` with the block centred inside it, scoped by `:has(.entry__empty)`.
**Rationale**: `.stage` already has a definite height (900px at 1440×900, stretched by the shell's `body`
flex row), so `min-height: 100%` resolves against its content box without a viewport unit, and the header
keeps its own height while the body absorbs the rest. Nothing needs to know the header's height.
**Alternatives**: `min-height: calc(100dvh - 150px)` — a magic number tied to this header; making `.stage`
itself a flex column — moves the search home and the results list too.
**Provenance**: measured `main.stage` 900px / `read` 860px on the branch; `components.css:1603` (`.stage`).

## D3 — Tile size and the row's behaviour

**Decision**: 52×52px tiles, 12px radius, 10px gap, a 22px glyph capped at 60% of the tile, in a five-column
grid that shrinks with the column; at or below 300px of reading column the grid becomes three and two at full
52px (`@container (max-width: 300px)`).
**Rationale**: 52px is the height of a service entry box in the same pane, so the row reads as the same
furniture; five full tiles need 300px of body (5 × 52 + 4 × 10 + 2 × 16 padding). Measured: 1440×900 → 52px
one row; 390×844 → 52px three and two; 1280×800 and 1024×700 (240px of body with both sidebars open) → 52px
three and two. Shrinking alone gave 33.6px and 29.1px tiles there, under the 44px target.
**Alternatives**: `flex-wrap` — wrapped 4 + 1, a ragged edge worse than 3 + 2; a viewport media query — the
constraint is the column, which the sidebars move independently of the window.
**Provenance**: `components.css:2215` region on the branch; the four-viewport probe in `quickstart.md`.

## D4 — Keeping the label when the text goes

**Decision**: each tile keeps its sentence in a `.sr` span and repeats it in `title`; the glyph is
`aria-hidden`.
**Rationale**: the existing `.sr` rule (1px, clipped) already carries hidden labels across this app, the
accessible name comes from the contents so no `aria-label` can drift from the sentence, and the `title` gives
a pointer user the same word. Playwright's text assertions keep matching the same labels, so the existing E2E
selectors stay honest rather than being rewritten to hide the change.
**Alternatives**: `aria-label` only — invisible to a sighted pointer user, who then has five anonymous glyphs.
**Provenance**: `components.css:1341` (`.sr`), `tests/e2e/test_offline_library.py:292`.

## D5 — The media glyph

**Decision**: a frame with a play triangle, in the same 24-unit viewBox and 1.6 stroke as the other four.
**Rationale**: `Add Media` covers image, audio, video, PDF and slides, so the glyph names the family rather
than a type; the family glyphs already exist per media entry but none of them fits five families at once.
**Alternatives**: reuse the PDF or play glyph — both name one type and lie about the others.
**Provenance**: `multimedia/web/templates/reading/tatib.html:208` (the tile had no glyph at all).

## D6 — Which tests move

**Decision**: the empty-state parity test now compares tiles by label, glyph count and square size instead of
by absolute position, and waits for the tiles before counting.
**Rationale**: the saved copy and the server route are drawn in differently wide reading columns, so absolute
coordinates were never evidence of parity — the previous version compared heights and vertical gaps, which
stopped meaning anything once the buttons stood in a row. Sizes, labels and glyph counts are the parts that
must match.
**Alternatives**: pin both renders to one width — the saved page's sidebar state is not the server page's, so
the width cannot be pinned from the test without navigating both the same way.
**Provenance**: `tests/e2e/test_saved_render_parity.py:88` on the branch; measured 3+2 versus 5-across between
the two renders at 1280×720.
