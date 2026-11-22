# Phase 0 Research: a text screen arrives as fast as the entries beside it

**Spec**: `specs/219-projector-fit-cost/spec.md`
**Unknowns remaining**: 0

## D001 — The fitting keeps walking the sizes from 200 px down

**Decision**: the search stays what it was — 200 px downwards, one pixel at a time, the first size
that fits. What changes is *when* it runs, not how it searches.

**Rationale**: halving the range was implemented first and measured wrong. The refusal is not
monotone in the size: a real screen of one line is refused at 101–105 px (the line is wider than the
box) and fits again from 106 px to 137 px (the words re-wrap onto two narrower lines). A halved search
settled on 90 px where the screen allows 137 px — 53 of 126 screens came out smaller than the
one-pixel walk, some by half. The walk is what makes "the largest size that fits" true, and R14 keeps
that promise.

**Alternatives rejected**:
- *Halve the range*: wrong on 53 of 126 screens (above).
- *Halve, then walk up a bounded window*: the refused band here is 37 px wide, so no bounded window
  reaches the size above it.
- *Make the refusal monotone by letting words break*: `overflow-wrap: break-word` on the lines would
  stop the width refusal and make a halved search exact, but it changes how words are broken on
  screen — a rendering decision for the owner, not a performance one.

**Provenance**: measured in the browser on the local service `Ibadah Minggu` (screen 121: refused at
101–105 px, fitting at 106–137 px); the halved build's sizes were compared screen by screen against
develop's.

## D002 — The fit measures the screen at rest

**Decision**: `render()` fits the arriving screen *before* it adds the arrival morph's classes, so the
screen is measured where it comes to rest rather than 14 px below it.

**Rationale**: the morph is `screenIn`, `translateY(14px)` to none over 240 ms, and the fit ran after
the class was added. `getBoundingClientRect` includes transforms, so every vertical question the fit
asked was answered about a box that was still moving — and how far it had moved depended on how long
the fit had been running. The consequence is visible without any timing at all: on develop the same
screen is fitted to 131 px on an advance and 135 px after a resize (53 of 126 screens disagree with
themselves), and a slow fit was punished twice — once for taking the time, once for measuring a box
that had drifted.

**Alternatives rejected**:
- *Fit against the untransformed box by subtracting the offset*: the offset is an animation value
  read from the DOM per probe; moving one block of code is simpler and exact.
- *Fit after the morph finishes (a `transitionend`/timer)*: the words would be shown at a stale size
  and then jump.

**Provenance**: `preview/verify_sizes.py` — develop's advance disagrees with its own resize on 53 of
126 screens; the slice's advance agrees with develop's resize on all 126.

## D003 — The screens either side are fitted in idle time

**Decision**: after every render, the screens at `current ± 1` are fitted in a `requestIdleCallback`
(falling back to a 60 ms timer), and the fit is skipped on arrival when the screen is already fitted
for this stage and this body.

**Rationale**: the fit is the only part of an advance that depends on what a screen holds — 130–280
layout reads for a screen of words, none for a section break — and it is what stands between the key
and the paint. Moving it off the arrival is the only way to make a text screen arrive as fast as the
entries beside it without giving up the exact size (D001). Measured: 135.6 → 1.0 layout reads per
advance, 16.4 → 3.7 ms median.

**Alternatives rejected**:
- *Fit every screen once at load*: ~1 s of idle work for a service this size, and a jump still needs
  the on-arrival fit; the neighbours are the screens an advance can actually ask for.
- *Fit only the next screen in the advance's direction*: the operator goes back as often as forward,
  and a second fit is cheap.
- *Defer the fit to after the paint and correct it*: the words would pop from one size to another a
  frame later — worse than the delay it removes.

**Provenance**: `preview/probe.py`, paced run.

## D004 — A fitted screen is remembered by stage size and body

**Decision**: `dataset.fitted` holds `stage width x height | header text | row count | text length`;
the fit is skipped while that key matches, and every key is deleted when the bundled faces arrive.

**Rationale**: the idle fit has to survive until the screen is shown, and a bare "fitted" flag would
survive a resize or a header change it must not. The four parts are exactly what the fit depends on.
The bundled faces change the metrics without changing any of them, so they are handled explicitly by
clearing every key and re-fitting.

**Alternatives rejected**:
- *A `WeakMap` of screen to size*: no cheaper, and it hides the invalidation in a second place.
- *Re-fit on every render and rely on the idle work being fast enough*: that is the defect.

**Provenance**: the resize, fonts-ready and translation paths in `static/web/projector.js`.

## D005 — The single-screen cut halves instead of stepping

**Decision**: the rows a single-screen text keeps are found by halving the row count, and the
characters trimmed from the last row by halving the character count.

**Rationale**: both loops were linear with a layout per step; a 400-row body took 2 992 ms on arrival.
The cut is the same — 116 rows, 10 711 characters, 2 px on both builds — in 81.5 ms.

**Alternatives rejected**: leaving it — it is the worst case of the same defect and it is on the
arrival path of exactly the entries the owner named.

**Provenance**: measured on both builds with the same 400-row body.

## D006 — Layout containment on `.screen` was tried and dropped

**Decision**: no CSS change.

**Rationale**: an isolated probe suggested `contain: layout size` made a layout read 6.8× cheaper
(32.1 → 4.7 ms per 100 reads), but measured through the real advance it changed nothing (8.3 ms median
contained against 7.8 ms without) — the cost is the screen's own text layout, not the other screens.
A CSS containment change that buys nothing is risk without a reason.

**Provenance**: `preview/probe.py` with the rule injected and removed, same page.

## D008 — A move that arrives mid-morph cuts

**Decision**: `render()` tracks a 260 ms morph window. A move inside that window settles the screen
leaving at once (no transition, no animation) and paints the arriving screen whole; a move after it
morphs as before.

**Rationale**: each move starts a 240 ms crossfade and a held key sends one every ~35 ms, so a
crossfade is always still running when the next move arrives. Restarting it stacks the part-faded
screens: measured **7 painted at once** and **64 frames of 122** carrying more than one screen on
develop. Cutting is what a held key should do — the operator is running down a list, not watching a
transition.

**Alternatives rejected**:
- *Shorten the crossfade when moves come fast*: the screens still overlap, just less.
- *Queue the moves and play them one at a time*: the display would lag behind the key by seconds.
- *Keep the crossfade and let it finish before the next move*: same lag, and a held key would feel
  stuck.

**Provenance**: `preview/hold_probe.py` — 34 repeats at 35 ms, sampled every frame: 7 → 1 screens
painted at once, 64 → 1 frames with an overlap.

## D007 — The bump is a patch

**Decision**: `patch` — 1.36.4 → 1.36.5.

**Rationale**: no requirement is removed, no interface changes, and the behaviour a reader of the
spec would notice (which size a screen shows) moves to the size the display already gave after a
resize. Repo convention: a fix is a patch.

**Provenance**: `docs/PROCESS.md` (versioning part) and the previous fix slices (216, 217, 218).
