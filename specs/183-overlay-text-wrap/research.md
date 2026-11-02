# Research: the overlay's text wraps inside the box that owns it

**Spec**: `specs/183-overlay-text-wrap/spec.md`

## D001 — `overflow-wrap: break-word`, not `anywhere`

**Decision**: the rule is `overflow-wrap: break-word`.

**Rationale**: both values break an unbreakable run when it does not fit. They differ in what they
contribute to intrinsic sizing: `anywhere` lets the affected text's *min-content* shrink to a single
character, `break-word` leaves min-content alone and only breaks when the line box would otherwise
overflow. Measured on the live page, applying each to every panel in turn produced byte-identical
boxes, row counts and zero spill on all six states (`scratch/ab-wrap.py` run: `same_box: true`), so the
choice is not decided by these numbers — it is decided by what the declaration may do to a box that
does size itself. The plate is `width: fit-content`, and a future flex or grid child would inherit
`anywhere`'s min-content collapse silently; `break-word` cannot move a box.

**Alternatives**: `anywhere` — the dock's own rule (`obs-dock.css:296`), rejected here for the
intrinsic-sizing side effect; `word-break: break-all` — breaks between any two characters even when a
better break exists, so `Kasih` could split mid-word; `hyphens: auto` — hyphenation, not wrapping,
and the language is not declared on the page.

**Provenance**: CSS Text Level 3 (`overflow-wrap`); spec 137's own decision for `.read`; the
projector's `overflow-wrap: break-word` at `projector.css:227` and `:255`; the A/B measurement above.

## D002 — One declaration on the stage

**Decision**: `.obs-overlay__stage { overflow-wrap: break-word; }`, and nothing on the plates, the rows
or the caption.

**Rationale**: the property inherits, so one declaration reaches every text the surface paints — the
plate's body rows and its `.obs-overlay__words` column, its `.kicker` and `.title`, and the song's
`.caption` — without a second rule per element. A speaker's mark is the exception and keeps its own
`white-space: nowrap`.

**Revised 2026-11-02, at gate 2**: this decision was first taken as `.obs-overlay__line` alone, on an
owner answer that scoped the slice to the plate's body. The owner then widened it — *"do the word-break
on the song captions and the panel's header/title as well"* — and the declaration moved up to the stage.
The narrow version is recorded as the superseded one in `spec.md`'s clarifications rather than dropped,
because the first answer is what the earlier preview and test set were built against.

**Alternatives**: the body row only (the first pass, superseded by the wider scope); each text element
(four declarations for one behaviour, and the words column would be missed when a mark is present).

**Provenance**: owner instruction, 2026-11-02 (gate 2); `obs-overlay.css`'s own class anatomy; the
`test_the_rule_is_inherited_from_the_stage` assertion that the stage, the plate, the kicker, the row and
the words column all compute `break-word`.

## D003 — No clamp, no scroll, no maximum height

**Decision**: a body that wraps to more rows makes the plate taller; nothing limits its height.

**Rationale**: the panel is anchored at `bottom: 5%` and grows upward, which is how it already behaves
for a long verse (spec 180's five-row verse measures 1728×342). The surface's answer to too much text
is the operator's screen breaks — the projector splits a body into screens — not a clamp that hides
words from the congregation. The report asks for wrapping, not for truncation.

**Alternatives**: `max-height` with a scroll — the overlay has no pointer and no controls, so a
scroller cannot be driven by anyone; `-webkit-line-clamp` — hides words that the operator put on air.

**Provenance**: spec 180's measured states; `docs/spec/overlay.md` R3 ("the card takes the frame's
90 % measure before it grows taller"); the surface's `pointer-events: none`.

## D004 — The test reads ink, not boxes

**Decision**: the acceptance test compares the right edge of the row's **ink** (`Range.getClientRects`)
with the plate's **content** edge, at three frame sizes.

**Rationale**: the element's border box is the full content width, so `element.scrollWidth` is a weaker
signal — a row whose ink overflowed by 710px reported the same box. The ink rects are what the
congregation sees. The content edge (the plate's right edge less its `23.40px` padding) is the line the
words may not cross; measuring against the border edge would let the text sit in the padding.

**Alternatives**: `scrollWidth > clientWidth` on the row (misses nothing today, but a box that is
itself too wide scores zero); a screenshot diff (no numbers to assert, and the frame behind the plate
is a video still); comparing against a hard-coded pixel (breaks with any type change).

**Provenance**: the same technique spec 137's preview used; the measurement bug found while probing
this slice (the first pass compared ink with the *row's* box less the *plate's* padding, which
reported a false 23.4px spill on the control).

## D005 — "Unchanged" is measured, not asserted from memory

**Decision**: the control case is verified by taking the declaration away on the live page
(`overflow-wrap: normal !important` on the rows) and re-measuring the same rows.

**Rationale**: nothing records the pre-slice box of a control state, so a hard-coded number would be a
guess that rots with the type scale. Removing the rule on the same DOM, in the same paint, isolates the
change to exactly what the slice adds — and the assertion is that the box, the rows and the width are
identical with and without it.

**Alternatives**: a golden snapshot of the control states (a number to maintain, no proof of cause);
trusting the rule to be inert because `normal` and `break-word` "only differ on long words" — the
premise of the slice is that nobody checked.

**Provenance**: the probe's `--normal` mode; spec 137's `before-*.html` pages built the same way.

## D006 — The fixture's shapes

**Decision**: 120-character run in a body, a 140-character pasted URL after the mark `L.`, and two
control entries; screens chosen by the projector's own order (each text entry paints one content screen
followed by its rest).

**Rationale**: the run must exceed the plate's 90 % cap (1728px at 1080p, ~96 characters at 36px) or the
plate simply grows and nothing overflows — a shorter run would pass without the fix and prove nothing.
The driver projects by entry index through the dock, which is how an operator does it, so the test
exercises the real state path rather than writing `localStorage` by hand.

**Alternatives**: setting `localStorage` directly (skips the dock's own write path); a 60-character run
(reproduces at 960 only, not at the frame the report came from).

**Provenance**: the report's own screenshot; the measured table in `spec.md`.

## D007 — The kicker's own row cannot outgrow the plate

**Decision**: no separate treatment for `.obs-overlay__kicker`; it inherits the rule like every other
text, and its measured state is asserted as unchanged rather than as wrapping.

**Rationale**: the kicker is set at `.5em` — 18px at 1080p — and its column is the entry title's 64
characters, or a Bible reference. A 64-character run at that size measures ~916px inside a 1,681px
content box, so the plate's own `fit-content` measure always absorbs it: the state has one row with and
without the rule, and a plate of 963.44 × 139.94 in both builds. The rule still covers the kicker for
the case where the plate is holding a longer row; it just cannot be *demonstrated* with a kicker alone.
Recorded because the first version of the test asserted a second row and failed — the number, not the
premise, was wrong.

**Alternatives**: force a break by shrinking the viewport (the surface's type is in container units, so
the ratio never changes — measured at 1280 and 960: still one row); raise the kicker's size (a design
change, not this slice's).

**Provenance**: the probe's `text-long-kicker` state at three frames; the red run recorded in
`converge.md`.

**Unknowns remaining: 0.**
