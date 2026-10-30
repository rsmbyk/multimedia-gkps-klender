# Research: the dock fills whatever panel it is given

**Spec**: `specs/164-dock-fluid-width/spec.md`

## D001 — Remove the width cap; do not raise it

**Decision**: `.dock` drops `max-width: 560px` and `margin: 0 auto` and takes `margin: 0`.

**Rationale**: the panel's width is decided by the operator dragging an OBS dock, and the same page
opens as a full browser window when the dock is reviewed outside OBS. Any number left in the sheet is
a guess about a size the page cannot know. The sheet's own header comment already claimed the panel
"IS the panel, so it fills the viewport" — the cap was the one line contradicting it, and it is the
only `max-width` in `obs-dock.css` (checked: one occurrence, line 33).

**Alternatives**: raise the cap to 900px or 1200px — still a guess, and the strip returns above it;
keep the cap and centre a comfortable column — this is the look the owner rejected ("does not fill
the entire width"); `width: clamp(...)` — the same guess, written longer.

**Provenance**: the owner's report of 2026-10-29 and the measured table in `spec.md` (panel held at
560 at every viewport ≥ 700).

## D002 — No container query

**Decision**: the slice keeps no `container-type` on `.dock`.

**Rationale**: an earlier pass of this same slice carried `container: dock / inline-size` to drive a
bucket-per-column grid. The grid was rejected (D003), so nothing would query the dock any more, and
`container-type: inline-size` is not inert: it applies inline-size containment and makes the element a
containing block for absolutely positioned descendants. Dead weight with a trap is worse than no
declaration.

**Alternatives**: keep it "for later" — a layout rule with no consumer; use media queries — the
viewport and the panel are the same box for this page, and the sheet needs no breakpoint at all.

**Provenance**: the working tree's own first pass, removed 2026-10-29 when the one column was chosen.

## D003 — One column, recorded as a requirement

**Decision**: the picker stays a single column at every width (FR-003).

**Rationale**: the bucket-per-column layout was built and measured — three columns of 468px at 1440,
628px at 1920, two columns with the third bucket wrapped below between 760 and 1100 — and the owner
asked for the one column instead. Written as a requirement, the variant cannot be rebuilt from the
same complaint.

**Alternatives**: bucket-per-column (rejected by the owner); two columns only above 1100px (still
fans out, still not asked for).

**Provenance**: owner decision, 2026-10-29 ("keep the one column for picker").

## D004 — A fill, not a text measure

**Decision**: no `max-width` / `max-inline-size` is introduced on the rows, the heads or the body.

**Rationale**: the ask is the panel's box. With one column, the row's own anatomy already carries the
structure — the name is the flexible first item and the date the last — so at 1440 the row is 1424px
and the date lands at the row's right padding. That is the reading of "fills the entire width" that
does not reintroduce the cap in another form.

**Alternatives**: cap rows at 720–760px and centre them (the rejected look); right-align a text block
inside a full-width row (invents an inset the mockup never had).

**Provenance**: `spec.md`'s measured table; the row measurements in this slice's probe.

## D005 — Two E2E cases at fixed viewports, no new fixture

**Decision**: the acceptance tests set the viewport with `page.set_viewport_size()` on the dock page
the suite already opens, and read boxes with `getBoundingClientRect` / `clientWidth`.

**Rationale**: the behaviour is geometric and lives entirely in CSS; the existing module already opens
`/obs/dock` at 1440 and needs no service it does not create. Resizing one page across four widths
covers the range without four page loads, which matters because the module runs a real browser.

**Alternatives**: a per-width context (four loads, slower, no extra coverage); a computed-style test
(`max-width: none`) — asserts the declaration, not the box the operator sees.

**Provenance**: `tests/e2e/test_obs_dock.py`'s existing helpers; the red/green runs recorded in
`converge.md`.

## D006 — The runner is out of scope

**Decision**: no change to the runner view beyond what the panel's width already does to it.

**Rationale**: it already filled the panel (its rows are `width: 100%`), and its entries are a
sequence — numbered in running order — so a second column would break the order the operator steps
through. Nothing in the report names it.

**Provenance**: `obs-dock.css` `.entryrow { width: 100% }`; the owner's report names the view, not the
runner.

**Unknowns remaining: 0.**
