# Research: dock live entry snap

**Spec**: `specs/196-dock-live-entry-snap/spec.md` · **Date**: 2026-11-15

## D001 — Measurement: entry's whole `entryli` box vs scroller's `clientHeight`

- **Decision**: "Entirely out of view" is true when the live entry's entire non-sticky parent box (`.entryli`) lies above the scroller's top edge or below the scroller's bottom edge. The visible area is `runBody.clientHeight` (the viewport), ignoring the body's 4 px top/bottom padding — the same element `glideScroll` already uses for its clamp (`static/web/obs-dock.js:485`) and `updateBand` uses for its visibility check (`:632,:645`).
- **Rationale**: The pinned row's `offsetTop` is its pinned position, not its flow position (`layoutTop` exists precisely because of that: `:501-510`). Measuring the `.entryli` against `clientHeight` is the one primitive that already works in the code — it is how `centerRow` computes its target and how `updateBand` decides to hide the band. Using `scrollHeight` or `getBoundingClientRect()` against the padding box would disagree with both by the 4 px margin.
- **Alternatives considered**: (a) `getBoundingClientRect()` on the `.entryli` vs the scroller's rect — rejected: layout shifts during morphs make rects transient, and the code already clamps against `clientHeight`. (b) Including the 4 px body padding in the visible area — rejected: the padding is inert spacing, not content; the spec's clarifications resolved this.
- **Provenance**: owner decision (Q3), 2026-11-15; corroborated by existing code at `obs-dock.js:485,520-526,633`.

## D002 — Snap targets: flush at top / foot just above NEXT band

- **Decision**: 
  - Off-top: scroll so the entry's `.entryrow` sits at the scroller's top edge with its `-4px` sticky treatment (the same look as a scrolled-through long entry); the entry's block is open beneath it.
  - Off-bottom: scroll so the entry's `.entryli` bottom rests just above the sticky NEXT band's top edge; the band remains visible, pinned at the scroller's bottom edge, naming the next entry.
  - If no next entry exists (`updateBand` hides it): the foot rests flush at the scroller's bottom edge.
- **Rationale**: The request's own wording — "it should snap just like the image 2 while it is off screen at the top … also the same things when it is off screen at the bottom (image 3). it should snap at the bottom (above the next bar)." An operator who has scrolled far away needs the live entry back at a *known* edge, not a centred position that changes as the block opens/closes during a crossing.
- **Alternatives considered**: (a) Always centre — rejected: the request is explicitly about *edge* snapping; centring is today's behaviour. (b) Snap to the scroller's physical edges (0 / scrollHeight) — rejected: would cover the NEXT band and lose the pinned-row look; rejected by the request's own "above the next bar".
- **Provenance**: owner decision (the request itself), reinforced by the gate-1 verification against the preview; the `updateBand` show/hide rule supplies the no-next-entry floor.

## D003 — Trigger: the same moments today's centring fires

- **Decision**: The snap fires at today's centring moments — every state notice with a live service and no morph (`sync()` when `live && !morphing`), the morph's finish (`finishMorph`), and the first paint after load. No separate scroll-settle debounce: the trigger is the *next sync* after an off-screen state, not a gesture's end.
- **Rationale**: `sync()` is the single funnel for every state change (all steps, seeks, blank/resume, bait jumps, service switches, the picker's own `openService`). Adding a scroll listener that snaps on gesture-end would rubber-band every manual browse and duplicate the cancel-on-wheel rule. The gesture is already the operator's own act; the snap restores the *view* of the thing on air, once the tool is told to re-settle.
- **Alternatives considered**: (a) Scroll-settle debounce (listen to `scroll`, snap after 300 ms idle) — rejected: fights the "a hand on the list wins" rule and creates unpredictable jumps. (b) Fire on every `scroll` immediately — rejected: same rubber-band problem.
- **Provenance**: owner decision (Q1), 2026-11-15.

## D004 — Reduced motion: instant, reusing `glideScroll`

- **Decision**: Under `prefers-reduced-motion: reduce`, the snap is instant. `glideScroll` already checks `reduceMotion.matches` and jumps (`obs-dock.js:492`). No new flag, no new code path.
- **Rationale**: The rest of the dock's motion system treats reduced-motion as "set scrollTop, done". Adding the snap as a special case would either duplicate the path or diverge from the existing token.
- **Alternatives considered**: (a) A separate `snapScroll` function — rejected: duplicates the clamp logic and the flag. (b) Disabling the snap entirely under reduced-motion — rejected: reduced-motion is about *not animating*, not about *not going there*.
- **Provenance**: research (the existing `reduceMotion` path at `obs-dock.js:481,492`); owner decision (Q3 boundary clarification).

## D005 — Go-to scope: service entries only

- **Decision**: Edge-snap applies only to the dock's service entries (the `entryList` flow). A go-to block keeps today's behaviour (no re-centring at all), as spec 185 designed.
- **Rationale**: The go-to block is a detached, transient view of a passage/song; its own rows are stepped with ↑/↓ and the block is centred when chosen. Spec 185 explicitly designed no centring for the go-to (`obs-dock.js:1084-1095` returns early). Adding an edge-snap there would introduce a new behaviour for a view that was never asked for it.
- **Alternatives considered**: (a) Apply snap to go-to live rows too — rejected: would change spec 185's contract and the go-to's own acceptance criteria; not asked for.
- **Provenance**: owner decision (Q2), 2026-11-15; spec 185 FR-004/FR-005 and `obs-dock.js:1084` supply the boundary.

## D006 — Hand wins: cancel on `wheel` / `pointerdown`

- **Decision**: The snap glide is cancelled by `wheel` and `pointerdown`, and none starts while a gesture is in progress, reusing `cancelPendingCenter` (`obs-dock.js:626-634`).
- **Rationale**: The dock already has this exact rule for the existing glide and the morph: an operator who scrolls or presses the list is looking around; nothing should yank the view back underneath them. The snap is a *re-settle* (after a state notice), not a *during-gesture* intervention.
- **Alternatives considered**: (a) No cancel (snap always wins) — rejected: contradicts the existing product behaviour and the request's "while it is off screen" does not imply fighting a manual scroll. (b) Cancel only on `wheel`, not `pointerdown` — rejected: would let a touch/click interrupt less reliably than the existing path.
- **Provenance**: research (existing `cancelPendingCenter` path); the request's own emphasis on the live entry being *out of the screen* implies the re-settle restores it, not the gesture.

## Open

None. All decisions traceable; zero unknowns remain.
