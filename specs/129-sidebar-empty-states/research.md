# Research: The sidebars say which nothing they show

**Spec**: `specs/129-sidebar-empty-states/spec.md`

## D001 — The empty line is a flex child, which is why it sits at the bottom

**Decision**: take the block out of the column's flow and centre it over the list pane.

**Rationale**: `.panel` and `.chapters` are fixed flex columns; the old `<p class="panel__empty">` /
`<p class="ch__empty">` were the last in-flow children, so they landed under the scroller — the
bottom-left corner in every screenshot. Centring them as flex items would fight the scroller for the
remaining height; `position: absolute; inset: 0` on the pane places the block on the rows' area with no
height arithmetic, and `pointer-events: none` leaves the list's wheel and drags alone.

**Alternatives considered**: (a) `flex: 1` + `display: grid` on the paragraph, rejected — it splits the
pane's height with the scroller, so the block centres on the bottom half; (b) centring in the whole column,
rejected — the ~63px filter strip then biases it upward, and the spec asks for the list's centre.

**Provenance**: `static/styles/design/components.css:277` (`.panel`), `:1485` (`.ch__wrap`),
`multimedia/web/templates/reading/base.html:218,304` — read on `develop` at 2990c3ae.

## D002 — Two states, typed by counting rows, not by trusting the filter

**Decision**: the block is typed `empty` when the list holds no rows at all and `filter` when it holds rows
but none match; the filter's own emptiness never implies "no data".

**Rationale**: `applyFilter`/`applySongFilter` already counted a hit per row; counting all rows is one extra
increment, and it makes the empty case independent of the query. A section whose list is empty therefore
keeps the empty copy even while a query is typed — the query did not empty it.

**Alternatives considered**: a server-set `data-empty` flag, rejected — the count changes without a reload
(after an entry is deleted, after an in-page navigation), so the browser has to decide anyway.

**Provenance**: `static/web/reading.js:873-897` (panel filter), `:908-929` (list filter) on `develop`.

## D003 — The copy lives on the element, not in the script

**Decision**: `data-empty-title`, `data-empty-hint`, `data-filter-title`, `data-filter-hint`; the script only
picks one pair.

**Rationale**: the copy is per section and per column, and the server already owns those strings in
`PANEL_META`/`CH_META` (`views.py:58-71`). Keeping them in one place means the in-page swap can copy the
arriving page's attributes instead of re-deriving section names in JavaScript, which is where the old
three-branch ternary lived and drifted.

**Alternatives considered**: a JS map keyed by `root.dataset.section`, rejected — it duplicates six strings
per section into the browser and would have to be kept in step with the views.

**Provenance**: `multimedia/web/reading/views.py:58-104`, `static/web/reading.js:890-894` on `develop`.

## D004 — A page can arrive empty, and nothing repainted it

**Decision**: paint both blocks once at boot, before any input.

**Rationale**: measured on the branch before the fix: `/tatib/<empty>/` and `/songs/book/<empty>/` left the
block hidden until a keystroke, because `applyFilter`/`applySongFilter` only ran on `input`, after a
navigation, or after an entry delete. The server cannot decide it either — the block's state depends on
counting the rows that made it into the DOM.

**Alternatives considered**: painting server-side with `{% if %}` around the list, rejected — every page
already renders the list either way, and the in-page navigation replaces the rows without a server render of
the block.

**Provenance**: probe run on `fix/129-sidebar-empty-states` before the boot paint:
`#chEmpty.hidden = true` on both empty pages.

## D005 — The saved renderer must re-label and re-glyph, because its shell is the home page

**Decision**: `offline-render.js` carries the six strings and two glyph paths per section and writes them
into both blocks before painting.

**Rationale**: `loadShell()` parses the cached `/home/` page (`offline-render.js:34-40`), whose blocks are
the Bible's. The renderer already re-labels the panel title, the filter labels and the list heading for the
section it rebuilds; the empty blocks join that list. Without it, an offline Kidung or Tata Ibadah page
would show `No books yet.` under a book glyph.

**Alternatives considered**: (a) one neutral glyph and one neutral sentence for every list, rejected — it
would lose the section's own name, which is the point of the fix; (b) fetching the destination route's
markup for its labels, rejected — the offline path must not need the network.

**Provenance**: `static/web/offline-render.js:300-354,815-897` on `develop`.

## D006 — The collapsed panel hides the block

**Decision**: `[data-nav="mini"] .panel .listempty { display: none; }`.

**Rationale**: the mini panel is ~80px wide and hides its filter (`:352`), so the block could only ever be
the empty copy, squeezed into a rail. The rail's job is to show where the section is, not to explain it.

**Alternatives considered**: a glyph-only mini variant, rejected — a 38px glyph in an 80px rail reads as a
broken row.

**Provenance**: `components.css:297-361` (mini panel), measured: `display: none` in the probe's mini step.
