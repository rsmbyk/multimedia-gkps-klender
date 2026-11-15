# Feature Specification: the runner snaps its live entry back into view at the edge it left

**Slice**: `specs/196-dock-live-entry-snap`
**Branch**: `feat/196-dock-live-entry-snap`
**Created**: 2026-11-15
**Status**: Draft
**Input**: *"when the current entry is out of the screen in dock, it should snap the same way as
the long entry being seen whether they are far off the top or bottom of the screen … the entry 3
should snap just like the image 2 while it is off screen at the top … also the same things when it
is off screen at the bottom (image 3). it should snap at the bottom (above the next bar)."*

## What the runner does today

Every state notice reaches `sync()` (`static/web/obs-dock.js:1034`). With a service live and no
crossing morph, it calls `scheduleCenter()` (`:1140`), which on the next frame runs `centerRow()`
on the live row (`:530-535`) — the live screen row, or the entry's label row when the screen has
no row of its own. The target is the row's layout top minus half the scroller's free height
(`:513-517`), reached by `glideScroll()` — a 190 ms ease-out glide, clamped to the list's real
ends (`:470`), instant under reduced motion. A crossing runs as one 230 ms morph instead, and
`finishMorph()` re-centres when it lands (`:591`).

Two things follow from that code:

- The snap-back-to-live exists, but its target is *centre*. A live entry that has left the screen
  entirely returns centred, not edge-aligned, and a long entry that is being scrolled through pins
  its row at the top edge (`position: sticky; top: -4px`,
  `static/styles/design/obs-dock.css:377-387`) — the look the request's image 2 shows.
- A hand on the list cancels any pending centring or glide (`wheel` / `pointerdown` →
  `cancelPendingCenter`, `:611-619`), which is deliberate: browsing between notices is free. So an
  operator who scrolls away from the live entry leaves it off-screen, and nothing brings it back
  until the next state notice — the state image 1 shows.

The centring rule spec 119 pinned ("Navigation recenters the current row vertically on every move,
190 ms ease-out, clamped at the ends") was never folded into `docs/spec/dock.md`; this slice folds a
complete rule for where the runner parks the live entry, citing spec 119.

## The rule this slice adds

When the runner re-settles and the live entry is **entirely** out of the scroll area, it glides to
an edge, not to the middle:

- entirely above the top → the entry row flushes to the list's top edge, pinned like a long entry,
  its block open beneath it;
- entirely below the bottom → the entry's foot rests just above the sticky NEXT band at the list's
  bottom edge, the band still visible and naming the next entry.

A live entry that is even partly in view keeps today's centring. The hand still wins mid-gesture.

## User Scenarios & Testing

### US1 — The live entry is entirely off the top; the runner snaps it flush to the top (P1)

**Why this priority**: this is the request's first case (image 1 → image 2). The operator must
always be able to see which entry is on air, and the pinned-row look is the one the product already
teaches with long entries.

**Independent Test**: open the runner with a service on air, scroll the list so the live entry is
entirely above the top edge, then let any state notice arrive (step the service). The list glides
up until the live entry's row sits flush at the list's top edge, its block open beneath it.

**Acceptance scenarios**

1. **Given** the live entry's whole box is above the scroller's top edge **When** the runner
   re-settles from a state notice **Then** the entry's row sits flush at the scroller's top edge
   (the pinned row's own `-4px` treatment), the entry's block is open beneath it, and the live
   screen row is visible.
2. **Given** the live entry is entirely above and the operator has scrolled away by hand **When**
   the next state notice re-settles the runner **Then** the same edge-aligned position results;
   the gesture's own settle does not fire it (Q1).
3. **Given** the operator prefers reduced motion **When** the snap fires **Then** the list jumps
   there without the 190 ms glide.

### US2 — The live entry is entirely off the bottom; the runner snaps it above the NEXT band (P1)

**Why this priority**: the request's second case (image 3). An entry that has run off the bottom
is as invisible as one off the top, and the NEXT band is the landmark the operator reads the
service against.

**Independent Test**: scroll the list so the live entry is entirely below the bottom edge, then
let a state notice arrive. The list glides down until the entry's foot rests just above the sticky
NEXT band, which stays visible and names the next entry.

**Acceptance scenarios**

1. **Given** the live entry's whole box is below the scroller's bottom edge **When** the runner
   re-settles **Then** the entry's foot rests just above the NEXT band, the band still pinned at
   the scroller's bottom edge and still visible, still naming the next entry.
2. **Given** the live entry is the service's last entry **When** the snap fires **Then** the foot
   rests flush at the scroller's bottom edge, with the band hidden — `updateBand` already hides
   it when no next entry exists (`obs-dock.js:623-646`).
3. **Given** the operator prefers reduced motion **When** the snap fires **Then** it is instant.

### US3 — A partly visible live entry keeps today's centring (P2)

**Why this priority**: the request asks for the snap when the entry is *out of the screen*; an
entry the operator can still see needs no snap, and changing its parking would move a target the
morphs and the refresh paths already agree on.

**Independent Test**: scroll so the live entry straddles an edge, then let a state notice arrive.
The list glides to today's centred position, not to an edge.

**Acceptance scenarios**

1. **Given** any part of the live entry is inside the scroller **When** the runner re-settles
   **Then** the live row lands at the centred target `layoutTop(node) − (clientHeight −
   offsetHeight) / 2`, exactly as today.
2. **Given** the live row is already at that centred position **When** the runner re-settles
   **Then** nothing moves.

### US4 — A browse in progress is not fought (P2)

**Why this priority**: the cancel-on-wheel rule exists so an operator can look around the list; the
snap must not turn every scroll into a rubber band.

**Independent Test**: with the live entry off-screen, scroll the list by hand; the list stays where
the hand left it for as long as the hand is on it.

**Acceptance scenarios**

1. **Given** a snap glide is running **When** the operator wheels or presses on the list **Then**
   the glide is cancelled, as today.
2. **Given** the operator is mid-gesture with the live entry off-screen **When** the gesture
   continues **Then** no snap starts; a later state notice is what fires it, not the gesture's
   own settle (Q1).

### Edge Cases

- **When** the live entry is taller than the scroller (a long entry, or a very short OBS panel)
  **Then** it can never be entirely out of view, so the snap never fires and the pinned-row look
  of image 2 is exactly what the operator already gets.
- **When** the live entry is a section-break row (a divider) **Then** there is no live entry to
  park, and the runner does nothing, as today.
- **When** the dock reloads with the live entry off-screen **Then** the first paint re-settles it
  edge-aligned, the same notice path as any other sync.
- **When** a go to is on air **Then** the runner keeps today's behaviour for the go to (no
  re-centring at all), as Q2 confirms.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | When the runner re-settles with the live entry's whole box above the scroller's top edge, it SHALL glide the scroller so the entry's row sits flush at the top edge (the pinned row's `-4px` treatment), with the entry's block open beneath it | `new: dock/R13` |
| FR-002 | When the runner re-settles with the live entry's whole box below the scroller's bottom edge, it SHALL glide so the entry's foot rests just above the sticky NEXT band, the band remaining visible and naming the next entry | `new: dock/R13` |
| FR-003 | With no next entry, FR-002's target SHALL be the entry's foot flush at the scroller's bottom edge, with the band hidden | `dock/R13` |
| FR-004 | A live entry at least partly inside the scroller SHALL keep today's centred target | `dock/R13` |
| FR-005 | The snap SHALL fire at the moments today's centring fires — every state notice with a live service and no morph, the morph's finish, the first paint after load — firing only when the live entry is entirely out of view (Q1 closed) | `dock/R13` |
| FR-006 | A snap glide SHALL be cancelled by `wheel` and `pointerdown`, and none SHALL start while a gesture is in progress | `dock/R13` |
| FR-007 | Under `prefers-reduced-motion: reduce` the snap SHALL be instant, reusing `glideScroll`'s existing path | `dock/R13` |
| FR-008 | The NEXT band's own show/hide and `is-stuck` rules SHALL be unchanged | `dock/R13` |
| FR-009 | With no measurable live row (no live service, or a go to on air, which keeps today's behaviour per Q2) the runner SHALL do nothing, as today | `dock/R13` |

### Key Entities

- **The live entry** — the `entryli` whose `data-live="true"` marks the entry on air; its box is
  measured through its non-sticky parent `.entryli` (`layoutTop`, `:505-511`), never through the
  pinned row's own `offsetTop`.
- **The scroll area** — `#runBody` (`.dock__body`, `obs-dock.css:209-227`), `position: relative;
  overflow-y: auto`, the element whose `clientHeight` is the view and whose `scrollTop` the snap
  drives.
- **The NEXT band** — `.nextband`, `position: sticky; bottom: -10px` inside the live `entryli`
  (`obs-dock.css:551-570`), hidden by `updateBand` when the entry's own end is in view; the bottom
  snap's floor is its top edge.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | A live entry entirely above the top re-settles with its row flush at the scroller's top edge | Playwright E2E: row rect top vs scroller rect top (±1 px) |
| SC-002 | A live entry entirely below the bottom re-settles with its foot just above the NEXT band | E2E: li bottom vs band top (±1 px), band not `hidden` |
| SC-003 | A partly visible live entry still lands centred | E2E: row rect top equals today's centre formula (±1 px) |
| SC-004 | A hand mid-gesture is never snapped | E2E: wheel during a pending snap leaves scrollTop where the gesture parked it |
| SC-005 | Reduced motion snaps without animation | E2E with `emulateMedia({reducedMotion: 'reduce'})`: position jumps, no glide frames |
| SC-006 | The dock's other scroll behaviour (picker cursor, morph curve, band rules) is unchanged | inspection of the diff + the existing dock suites stay green |

## UI/UX

`n/a` is not claimed — the dock's list moves differently. Numbers from the preview
(`specs/196-dock-live-entry-snap/preview/index.html`):

- **Layout / position**: the runner list in a 400 × 520 dock panel; the pinned live row sits flush
  at the scroller's top edge (`top: -4px` over the body's 4 px padding); the bottom snap parks the
  live entry's foot at the NEXT band's top edge, the band (`padding: 7px 10px 9px`, 1 px top
  border, ~35 px tall) pinned at the scroller's bottom.
- **Size / spacing**: entry row `min-height: 38px` + `padding: 9px 10px`; screen row 28.8 px;
  `entryli + entryli` margin 4 px; body padding `4px 8px 10px`.
- **Colour / typography**: unchanged — the live row keeps `--sidebar-selected-bg` and the pinned
  row's existing fill.
- **States**: hover, focus, active, disabled, empty, error, loading unchanged; the snap adds no
  state of its own.
- **Motion**: the snap reuses `glideScroll` — 190 ms, ease-out cubic `1 − (1 − t)³`, clamped to the
  list's real ends, cancelled by `wheel` / `pointerdown`; instant under reduced motion. The 230 ms
  crossing morph is untouched.
- **Responsive**: the rule is relative to the scroller's box, so it holds at the dock's 320 / 400 /
  520 widths and any OBS panel height; an entry taller than the scroller can never be entirely out
  of view and keeps today's behaviour.

## Assumptions

- The top-snap target is the pinned-long-entry look from image 2: row flush at the top edge, block
  open below. The bottom target is image 3's: foot just above the band, band visible. (The request's
  words; the exact edges are confirmed in Q3.)
- "Entirely out of view" is measured on the live entry's whole `entryli` box against the scroller's
  `clientHeight`, using the non-sticky parent for layout position, never the pinned row's
  `offsetTop`.
- A long entry (taller than the scroller) is never entirely out of view; the snap cannot fire on
  it.
- Reduced motion inherits `glideScroll`'s existing instant path; no new flag.
- A crossing morph keeps its own curve; `finishMorph`'s re-centre is unchanged — the arriving block
  is on screen by then.
- The snap re-targets where the runner parks the live entry only: no new storage key, channel
  message, endpoint or persistent timer. [Q1's settle debounce, if accepted, adds a one-shot
  `requestAnimationFrame`/timeout on scroll, no state.]

## Clarifications

### Session 2026-11-15

| Question | Answer |
| --- | --- |
| Q1 — Scroll-settle trigger | Fire **only** when the live entry is fully off-screen (entirely above top or entirely below bottom); partially visible entries keep today's centring. The snap fires at today's centring moments (every state notice with a live service and no morph, the morph's finish, the first paint after load). No separate scroll-settle debounce: the trigger is the next sync after an off-screen state, not a gesture's end. |
| Q2 — Go-to-on-air scope | Edge-snap applies **only** to service entries. A go-to block keeps today's behaviour (no re-centring at all). |
| Q3 — Edge / partial-visible boundary | "Entirely out of view" is measured against the scroller's **clientHeight** (the viewport), ignoring the body's 4 px top/bottom padding — matching `glideScroll`'s existing clamp and `updateBand`'s visibility measure. |

Answers lock the rule: **off-screen → edge flush (top) or foot just above the NEXT band (bottom); anything visible → centre today**.
