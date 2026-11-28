# Research: earlier top pin for the live header

**Spec**: `specs/248-dock-top-pin-early/spec.md`
**Unknowns remaining**: 0

## D001 — The takeover boundary

- **Decision**: the clone takes over when the live header's *natural* top reaches the scrollport's
  top edge: `li.getBoundingClientRect().top <= box.top + 0.5`, with the real header already clamped
  by sticky (`row.top <= box.top + 0.5`). R19's `li.bottom <= box.top + 0.5` is superseded.
- **Rationale**: the owner chose "as soon as the header itself starts to be clipped by the top edge,
  the clone takes over from the sticky header at that exact point, mirroring the bottom pin". The
  probe on 63404 showed the sticky header at 0 px from scrollTop 1056 while the clone waited until
  1164 — a 108 px stretch where the header was at the edge but no pinned representation existed.
- **Alternatives considered**: keep the whole-block boundary (rejected by the owner); trigger on
  any part of the block crossing the fold while the header is still fully in view (would duplicate
  the header before sticky engages). R18's bottom trigger is the named mirror.
- **Provenance**: owner decision; `preview/before-boundary.json` (490 frames, 420 × 860, dark 1×).

## D002 — The clone's pinned position

- **Decision**: the clone stands at 0 px from the scrollport edge (`top: 0` in the zero-height slot),
  unchanged from spec 242.
- **Rationale**: a first build used `top: -4px` to match the header's *constrained* position late in
  the straddle (scrollTop 1128: headerTop -4.31). The probe showed that at the actual takeover
  (scrollTop 1056) the sticky header holds at 0 px, so -4 px produced a 4 px hop. Reverting to 0
  made pinTop = headerTop = 0 on the takeover frame.
- **Alternatives considered**: -4 px (measured 4 px hop, rejected); animate the 4 px (unrequested
  motion on a boundary that should read as one header).
- **Provenance**: research — `preview/after-boundary.json`, 28 straddle frames re-measured.

## D003 — One painted header

- **Decision**: while the clone owns the edge, the real header carries `visibility: hidden`; the
  clone drops that class when copied. The covering wrapper is tracked so a crossing or a re-render
  clears the old row in the same paint.
- **Rationale**: `visibility` keeps the sticky box in flow, so covering it shifts no geometry (the
  spec 242 feedback loop with an in-flow slot applies with equal force here). An opaque clone at
  exactly the same box would hide it visually but leave two accessible headers; hiding the source
  keeps one painted and one announced header.
- **Alternatives considered**: `display: none` (removes the sticky box and moves the list); overlay
  only (duplicate accessible header); no clone until fully off-screen (the behaviour being fixed).
- **Provenance**: research, following the spec 242 feedback finding and the spec 208 "never a second
  band" ruling.

## D004 — Reconciliation paths and reduced motion

- **Decision**: reuse `updatePins()` and every call site already established in spec 242 — scroll
  frames, sync, the first paint and each frame of a centring glide, morphs and their landings, resize
  — and add no new listener.
- **Rationale**: the pin is paint-only state; a new event path would be a second source of truth.
  Under reduced motion the same synchronous reconciliation paints in the same frame.
- **Alternatives considered**: a `ResizeObserver` or a dedicated scroll handler (duplicate paths);
  hiding the pin behind the NEXT band's motion guard (spec 242 explicitly forbids it).
- **Provenance**: code inspection of `static/web/obs-dock.js` `updatePins()` call sites; spec 242
  FR-002/FR-008.

## D005 — Record numbers

- **Decision**: `ITEM-265` (next free card id on develop and in worktrees), `bump: patch`, applied in
  the pre-merge delivery commit; re-checked before delivery because sibling slices can take either
  number.
- **Rationale**: repo conventions (BRD-01, VER-03, C-SDD-VER); a user-visible pin boundary is a fix.
- **Alternatives considered**: `bump: none` (a visible behaviour change is notable); claiming a new
  capability number (R19 is *modified*, not replaced).
- **Provenance**: repo docs `docs/PROCESS.md`, `git log`, worktree scan on 2026-11-28.

## D006 — The Go To exception carried over from spec 242

- **Decision**: this slice does not add a Go To suppression; the carried-over scenario is narrowed
  to "the `.offstrip` is unchanged", and the older "no service pin appears" wording is kept as a
  retraction in the spec.
- **Rationale**: `preview/check_goto.py` put a service entry live, started a real Go To through the
  `G` band, scrolled to the fold, and read both builds: develop (63404) `goto: true`,
  `topPinHidden: false`, `offBlockShown: true`, 21 off rows; slice (8793) the same, with the expected
  new `is-covered` class on the service header. The service pin during a Go To is pre-existing, not
  introduced here; only its boundary moved earlier.
- **Alternatives considered**: add a Go To suppression (out of scope and would change accepted
  behaviour); silently delete the scenario (loses the record of a false claim).
- **Provenance**: manual check, 2026-11-28, `preview/check_goto.py` on both builds.

## Open

<!-- empty: Phase 0 finished with zero unknowns -->
