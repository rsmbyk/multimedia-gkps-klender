# Feature Specification: the live entry header's corners follow its pin state

**Slice**: `specs/208-dock-stuck-corner`
**Branch**: `fix/208-dock-stuck-corner`
**Created**: 2026-11-20
**Status**: Accepted (fix stories at gate 1; bottom pin and the band/corner rulings folded into this
slice before gate 1 and accepted through the same gate; see Revision)
**Input**: the owner's report, 2026-11-20 — "sometimes the entry headers get into the following
states: pinned entry headers but the top is not flat; unpinned entry headers but flat top"
(two screenshots of the runner: a pinned HAL 5 header with rounded top corners, and an in-flow
header with square ones). Follow-up the same day: "can you also do the same when the live-entry
headers going partially out of screen at the bottom (pin it to the bottom)" — folded into this
slice as US4 (ITEM-221).

The live entry's header pins flush at the scrollport's top edge (`position: sticky; top: -4px`,
mockup v39) and squares its top corners while stuck — the `.is-stuck` class, the only place the
flat top comes from (`static/styles/design/obs-dock.css:418`). That class is toggled in exactly one
place: inside `updateBand()` (`static/web/obs-dock.js:903`), behind the NEXT band's motion guard
(line 893: `glideFrame || morphFrame || performance.now() < bandHoldUntil`). The guard exists for
the band — re-parenting it mid-glide shifts the row being centred — but the corner class is
paint-only and moves nothing. Three consequences, all measured on `develop` at `c385a194`:

1. Every scroll event a glide or crossing morph generates is swallowed by the guard, and nothing
   re-runs `updateBand()` after the 300 ms hold expires. When the motion lands and the list rests,
   no further event fires, so the class stays stale until the next hand scroll.
2. On a crossing, `sync()` measures the *new* live header against the *old* scroll position. A
   header far above the fold reads as "stuck" (`top − boxTop ≤ 0.5` is true for any row scrolled
   out above) and gets the class before the morph has moved anything; the guard then blocks every
   correction.
3. Height-only changes — a hand block-toggle, a browsing morph — never fire a scroll event, so
   they never re-measure at all.

Reproduced on the live dock (compose `web`, 63404; 420 × 860, dark, 1×; HAL 1, 21 screens):

| State | Header top vs list top | `.is-stuck` | Painted top radius |
| --- | --- | --- | --- |
| Advance to bait 7, at rest | 0 px — pinned | absent | 9 px — **rounded while pinned** |
| One hand scroll (control) | 0 px — pinned | present | 0 px — correct |
| Ctrl+Home to entry 1, at rest | 4 px — in flow | present | 0 px — **flat while unpinned** |

The control proves the toggle itself works; the bug is when it runs and what it measures.

## User Scenarios & Testing

### US1 — A pinned header always wears a flat top (P1)

**Why this priority**: the first reported state. The flat top is the visual cue that the header is
docked against the list's edge; a pinned header with rounded corners reads as a floating card and
shows slivers of the rows passing behind its notches.

**Independent Test**: on the live dock with a long song on air, advance deep into it and let the
list rest without a hand scroll; the header's top is at the scrollport edge and its top corners are
square.

**Acceptance scenarios**

1. **Given** a long song is live and the dock is following **When** the operator advances to a
   screen deep enough that the header pins and the list comes to rest **Then** the header wears
   `.is-stuck` and its painted top radius is 0 px — with no hand scroll after the advance.
2. **Given** the header is pinned **When** the operator scrolls by hand **Then** the state stays
   correct (the existing scroll path, unchanged).
3. **Given** `prefers-reduced-motion: reduce` **When** an advance lands the header pinned
   **Then** the flat top is painted in the same instant paint, not a frame later.

### US2 — An in-flow header always keeps round corners (P1)

**Why this priority**: the second reported state. A header sitting in normal flow with square top
corners wears the pinned treatment while visibly detached from the edge.

**Independent Test**: from a pinned header, cross back to an entry whose header lands in flow and
let the list rest; the header's top corners are rounded.

**Acceptance scenarios**

1. **Given** the live header is pinned and stuck **When** a crossing (e.g. `Ctrl+Home`) lands the
   new live header in flow and the list rests **Then** it has no `.is-stuck` and its painted top
   radius is 9 px.
2. **Given** the live header is pinned **When** the operator opens a closed block above it by hand
   and the expansion pushes the header below the pin line **Then** the corners round without any
   scroll event — the height change alone reconciles them.
3. **Given** a header was stuck on an earlier visit **When** it becomes live again **Then** it
   wears the state its current geometry says, never the one it kept from before.

### US3 — The corners track the pin line through every motion (P2)

**Why this priority**: the owner's motion rule — expand, collapse and scroll read as ONE continuous
action (R15). A corner that pops square 300 ms after the motion lands is a second phase; the state
must flip on the frame the geometry crosses the pin line.

**Independent Test**: sample the header's offset and class each frame during a centring glide; on
every frame the class equals the geometry's verdict.

**Acceptance scenarios**

1. **Given** a glide or crossing morph is running **When** the header's top crosses the pin line
   mid-motion **Then** `.is-stuck` flips on that same frame, in both directions.
2. **Given** any crossing **When** the old header loses liveness **Then** it loses `.is-stuck` in
   the same paint — only the live header may wear the state.
3. **Given** the NEXT band's own motion guard **When** this slice lands **Then** the band's
   reparenting, yield rule and 300 ms hold are unchanged — only the corner toggle leaves the guard.

### US4 — The live label pins to the bottom when the header would be cut (P2)

**Why this priority**: the owner's follow-up ask — the pin model completed at the other edge.
When the operator scrolls above the live entry (browsing) or projects a far-down entry without
re-centring, the live header sits cut at the bottom edge; the live label should stay fully
visible there, wearing the same treatment the top pin wears: flat edge while pinned, round in
flow.

**Mechanism finding** (measured against the DOM): the header node itself cannot bottom-pin — a
sticky element pins only toward room inside its containing block, and the header is the entry's
first child (an upward shift would leave the li, which sticky forbids). The NEXT band, the last
child, is why a list-level slot with `bottom:0` (and `margin-top:auto` for the no-scroll case)
works for it. The feasible shape is a list-level sticky slot holding
a **faithful clone of the live header**, clipping exactly when the header's bottom reaches the
NEXT band's top — the clone sits precisely over the real header at that boundary (bottom at the
band's top, one header-height tall), so it takes over rather than adding a second band's height.
Both pinned elements are
list-level slots at the list's end: the NEXT band at the edge, the pin abutting directly above it
(owner: "make the NEXT bar always sticky and make the bottom pin above that"). The header clone is
shown from that staging point onward; NEXT is always shown whenever a next entry exists.

**Independent Test**: with a tall live block, scroll the list above the live entry until the
header's bottom reaches the NEXT band's top; the clone stands precisely over the real header with
flat bottom corners, abutting NEXT, and stays as the header passes off; scroll back until the whole
header is in view and the pin is gone, per frame, no hand scroll needed to reconcile.

**Acceptance scenarios**

1. **Given** the live header's bottom touches the NEXT band's top **When** the list rests **Then** a
   faithful clone of the header (number + name + verse subtitle + chevron, selected face) stands
   flush at the scrollport's bottom edge, directly above the NEXT band, bottom corners flat (0 px),
   top corners round (9 px), covering the real header with no added height, tracked per frame on the
   same paths as the top state.
2. **Given** the pin is up **When** the header scrolls fully back into view **Then** the pin is
   gone on that same frame. While it is up it covers the departing header — one visible header,
   never a second band above it (no doubling).
3. **Given** the pin is up **Then** it abuts directly above the always-sticky NEXT band (FR-009),
   no gap or overlap; with no NEXT entry it takes the edge itself.
4. **Given** the pin is up **When** the operator clicks it **Then** the live row glides back
   to the centre, the current screen stays on air, and following returns — the centre control's
   act.
5. **Given** `prefers-reduced-motion: reduce` **When** the header starts to go off below **Then**
   the pin paints instantly, no frame of stale state.

### Edge Cases

- **When** the live block's end scrolls past the header and the header slides out above the top
  edge **Then** it keeps the flat top while any part of it is still at the edge, and loses the
  class once the whole block is above the edge (nothing of it is visible then).
- **When** the list is clamped at an end and a centring cannot move it **Then** the corners still
  match the geometry they land with.
- **When** a go to is on air **Then** its `.offstrip` header is untouched — it has no corner state.
- **When** the window resizes **Then** the corners re-reconcile with the reflowed geometry.
- **When** the live entry is a go to's block **Then** the bottom pin does not apply — the go to
  strip (`.offstrip`) has its own anatomy and no corner state (FR-006).
- **When** the live block's end is in view at the bottom **Then** the NEXT band is still shown and
  pinned flush at the edge (FR-011); the bottom strip's own rule is the header's visibility, not
  the block's end.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | The live entry's header SHALL wear square top corners (`.is-stuck`, painted top radius 0 px) **if and only if** it is pinned: its top at the scrollport's top edge within 0.5 px **and** its block still reaching below that edge. A header scrolled out of view above the list is not pinned; at rest in flow the top radius is 9 px. | `dock/R17` (new) |
| FR-002 | The corner state SHALL be re-evaluated on every path that moves or resizes the list: scroll frames, state sync, every frame of a centring glide, a crossing morph and a hand block-toggle morph, each of their landings, and window resize. The NEXT band's motion guard SHALL NOT suppress it. | `dock/R17` (new) |
| FR-003 | Only the live entry's header SHALL wear `.is-stuck`; a header that loses liveness SHALL lose the class in the same paint, so a later re-liveness never inherits a stale state. | `dock/R17` (new) |
| FR-004 | The NEXT band's click (project its own screen), label text and truncation are unchanged; its placement is now a list-level slot (FR-011) with no yield rule. Its 300 ms motion guard on the **label** stays. | `dock/R15` (click/label unchanged), `dock/R18` (placement) |
| FR-005 | Under reduced motion the instant paint SHALL reconcile the corners in the same paint, with no frame of stale state. | `dock/R17` (new) |
| FR-006 | The pin geometry itself (sticky `top: -4px`, flush at the edge, z-index), the header wash and tint rules (R14), and the go to's `.offstrip` SHALL be unchanged. | `dock/R14`, `R3` (unaffected) |
| FR-007 | The bottom pin SHALL clip **exactly when the live header's bottom touches the NEXT band's top** (`row.bottom > bandRect.top`), not a row-height early — staging early added a second header-height of chrome while the header was still clear ("it gets too tall", owner). At that boundary the clone sits precisely over the real header (its bottom at the band's top, one header-height tall), so it takes over with no added height. It is a faithful clone (number + name + verse subtitle + chevron, selected face), flat bottom corners (0 px), round top corners (9 px), pinned directly above the always-visible NEXT band (FR-011), abutting its top; when no NEXT band exists it takes the edge itself. The header's own top-pin state SHALL be unchanged. (Owner rulings 2026-11-20: "only clip right when the bottom part of the entry headers is touching the next band"; "make the NEXT bar always sticky and make the bottom pin above that".) | `dock/R18` (new) |
| FR-008 | The strip's pinned state SHALL be tracked per frame on the same paths as the top state (FR-002); the header scrolling back into full view SHALL remove the strip and restore round corners on that same frame; reduced motion SHALL paint it instantly. | `dock/R18` (new) |
| FR-009 | The TWO pinned slots stack at the bottom edge: the NEXT band holds the edge (FR-011) and the live header's pin abuts directly above its **measured top**, with no gap or overlap. When no NEXT entry exists the band is hidden and the pin takes the edge itself. (Owner ruling 2026-11-20: "make the NEXT bar always sticky and make the bottom pin above that" — restores the stack with the band now always present.) | `dock/R18` (new), `dock/R15` (band click/label unchanged) |
| FR-010 | Clicking the bottom strip SHALL **re-centre the live row, keep the current screen, and return to following** — the centre control's own act (R15); it SHALL NOT write a different screen to the display state. (Owner ruling, 2026-11-20: "Re-centre the live row, keep the current screen, return to following".) | `dock/R18` (new), `dock/R15` (following) |
| FR-011 | The NEXT band SHALL be **always visible** while a next entry exists — regardless of whether that row is on screen (owner) — via a list-level sticky slot at the end of `#entryList`, so it is never caged by its live block. To pin even when all entries fit the viewport, `#entryList` is `min-height:100%` and a flex column with the slots at its flow bottom (`margin-top:auto`), and `#runBody` has no bottom padding: the band lands flush at the edge (band bottom 0) in both scroll and no-scroll states. Its click and label (FR-004) are unchanged. | `dock/R18` (new), `dock/R15` (band click/label) |

### Success Criteria

| ID | Criterion | Verification |
| --- | --- | --- |
| SC-001 | After advancing deep into a long song and resting (no hand scroll), the pinned header has `.is-stuck` and top radius 0 px. Before: delta 0 px, class absent, 9 px. | `tests/e2e/test_dock_stuck_corner.py::test_a_pinned_header_wears_a_flat_top_after_advancing` (new) |
| SC-002 | After a crossing lands the new live header in flow and rests, it has no class and top radius 9 px. Before: delta 4 px, class present, 0 px. | `…::test_an_in_flow_header_keeps_round_corners_after_a_crossing` (new) |
| SC-003 | A hand-opened block above the pinned header rounds its corners with no scroll event. | `…::test_a_hand_toggle_above_the_live_header_reconciles_the_corners` (new) |
| SC-004 | During a glide, every sampled frame's class equals the geometry's verdict (pinned ⇒ stuck, in flow ⇒ not). | `…::test_the_corners_track_the_pin_line_during_a_glide` (new) + `preview/probe.py` |
| SC-005 | The old live row loses `.is-stuck` on the crossing paint. | `…::test_only_the_live_header_wears_the_stuck_state` (new) |
| SC-006 | Reduced motion lands the flat top instantly. | `…::test_the_flat_top_lands_instantly_under_reduced_motion` (new) |
| SC-007 | The existing dock E2E modules stay green (band, toggle, open-reset, follow, wrap), except the recorded pre-existing machine-local red ITEM-220 (the chevron-eligibility pointer race), reproduced identically on the unmodified base. | `tests/e2e/test_obs_dock.py`, `test_dock_open_reset.py`, `test_obs_dock_follow.py`, `test_dock_text_wrap.py` |
| SC-008 | With the live header fully off below and the list at rest, a faithful clone of the header stands flush at the edge — exact text match, 0 px bottom radius, 9 px top radius, no LIVE caption; the header's top state is untouched. | `tests/e2e/test_dock_stuck_corner.py::test_the_bottom_pin_is_the_header_pinned_when_fully_off` (new) |
| SC-009 | The pin's visibility equals the geometry (header top past the bottom edge) on every sampled frame of the glide home. | `…::test_the_bottom_pin_tracks_the_header_visibility_per_frame` (new) |
| SC-010 | The ruled click act lands: re-centre the live row, keep the current screen, return to following. | `…::test_clicking_the_bottom_pin_performs_the_ruled_act` (new) |
| SC-011 | Reduced motion paints the pin instantly. | `…::test_the_bottom_pin_lands_instantly_under_reduced_motion` (new) |
| SC-012 | The pin clips exactly when the header's bottom touches the NEXT band's top — not a row early — and at that boundary the clone covers the real header with no added height, faithful and abutting NEXT. | `…::test_the_bottom_pin_starts_as_soon_as_the_header_goes_off` (new) |
| SC-013 | The NEXT band is always visible while a next entry exists and pinned flush at the edge (band bottom ≈ 0) even when the whole list fits (1920×1200) — never caged, never dangling. | `…::test_the_next_band_is_always_visible_even_when_the_list_fits` (new) |

## UI/UX

`live preview at http://127.0.0.1:8767/obs/dock` — the real dock served from this worktree with the
fix applied (the change is state tracking on the live list, so a static replica cannot show it).
Develop's unchanged build answers on 63404 for the before/after comparison. Measured by
`preview/probe.py`, dark mode at 1×, 420 × 860:

- **At rest, after advancing to bait 7 with no hand scroll** — develop: header pinned
  (Δ 0 px), class absent, top radius **9 px**; slice: pinned, class present, **0 px**.
- **At rest, after Ctrl+Home crosses to entry 1** — develop: header in flow (Δ 4 px), class
  present, top radius **0 px**; slice: in flow, class absent, **9 px**.
- **Per frame during the advance** (class vs geometry's verdict): develop **328 of 328 pinned
  frames mismatched** (404 sampled); slice **0 of 328** (405 sampled) — the corners flip on the
  frame the header crosses the pin line, in both directions.
- **Control** (one hand scroll while pinned): both builds class present, 0 px — the toggle
  itself was never broken.
- **In flow at the first screen** (before any advance): both builds Δ 172 px, no class, 9 px —
  the resting state is unchanged.
- Fixture: the team's own 1 November service, **HAL 1** (7 baits, 21 screens); raw screenshots
  in `preview/shots/before/` and `preview/shots/after/`.

### The bottom pin (US4) — measured by `preview/probe_clone.py` + the E2E fixture on the live dock

- **The stack** (HAL 5 live, two blocks hand-open above; header bottom 764 px > edge 727.9 px,
  header top 708 px): the NEXT band holds the bottom edge (**692.7–727.9 px**) and the live
  header's pin abuts directly above it (**636.7–692.7 px**) — `abuts: true`, `copyExact: true`,
  text `11 HAL 5 Bait 4`, bottom radius 0 px, top radius 9 px. One live header, no doubling.
  Pinned by `test_the_bottom_pin_starts_as_soon_as_the_header_goes_off` and
  `test_the_bottom_pin_is_the_header_pinned_when_fully_off`.
- **NEXT band, list-level and always pinned**: measured at 1920×1200 (whole list fits, no scroll)
  the band sits flush at the bottom edge — band top **1033 px**, bottom **1068 px** = the scrollport
  edge — and at 420×860 it pins at **693–728 px**. Always visible while a next entry exists.
  Pinned by `test_the_next_band_is_always_visible_even_when_the_list_fits`.
- **The pin click** (the centre control's act): per-frame visibility equals geometry on every
  sampled frame of the glide home; the display state byte-identical before/after; the live row
  glides back to the centre; following returns; the pin is gone once the header is back in view.
- **Reduced motion**: the pin paints instantly (E2E pin).
- Screenshot: `preview/shots/bottom/stack-next-and-pin.png`.

## Assumptions

- **The corners track the motion live, not just at landing.** R15 and the owner's one-motion rule
  make a post-landing corner pop a second phase; per-frame reconciliation is the same cost as the
  morph's existing per-frame rect reads.
- **"Pinned" excludes a header scrolled out above.** The block's bottom above the scrollport edge
  means nothing of the header is visible; the class comes off so the state is honest, and the
  crossing measurement (root cause 2) stops reading a far-above row as stuck.
- **The 0.5 px tolerance stays** — the value mockup v39 settled and the current code uses.
- **Dock service list only.** `.is-stuck` exists nowhere else (searched): the go to's `.offstrip`
  and the reading page's pinned header (spec 085) carry no corner state.
- **The band's 300 ms hold stays for the band alone.** It prevents layout shift mid-glide; the
  corner class shifts no layout, so it has no reason to wait.
- **The fixture songs are synthetic** (12–14 verses); the report's HAL 5 / HAL 1 are the same
  mechanism — a block taller than the scrollport, a header pinned while a deep screen is centred.
- **The NEXT band is a list-level slot always at the edge.** The band used to be the live li's last
  child with a yield rule and a sticky cage. It now lives in `li.nextband-slot` at the end of
  `#entryList`, always shown while a next entry exists (regardless of the next row's position).
  `#entryList` is `min-height:100%` and a flex column with the slots at its flow bottom
  (`margin-top:auto`) and `#runBody` has no bottom padding — so with no scroll (sticky inert) the
  band still sits flush at the edge, not dangling after the last row; with scroll, sticky bottom:0
  pins it. Its click/label are unchanged. The pin's slot follows it and its inset is measured from
  the band's **rendered top** (`box.bottom - bandRect.top`), so the two abut with no gap.
- **The bottom pin is a faithful clone of the live header, not a caption band.** The slot
  (`li.liveband-slot`, the last child of `#entryList`) is the sticky element — its containing
  block is the whole list. It holds a `cloneNode(true)` of the live `.entryrow` (number + name +
  verse subtitle + chevron), re-cloned only when the source header node changes. The clone drops
  `aria-current`/`aria-controls` (it is not a second "current" row and not a toggle); CSS
  `.liveband-slot .entryrow` gives it the selected face, static position, flat bottom corners
  (0 px) and the row's 9 px top corners — mirroring the top pin. It stands as soon as the header's
  bottom passes the edge, directly above the NEXT band.
- **The pin is a pinned representation, not a second live header** — the real header keeps its own
  state and geometry; the pin stands while any of the header is off the bottom and covers it, and
  clicking it acts on the live row (re-centre), never projects a different screen by itself.

## Revision

- **2026-11-20 — the bottom pin folded in before gate 1 (owner).** Gate 1 accepted the fix
  stories (US1–US3) as presented; the same answer instructed ITEM-221 ("pin it to the bottom")
  folded into this slice before gate 1. Per SDD-25 the pack re-enters Specify: US4, FR-007..010
  and SC-008..011 are added, three design points go to Clarify (trigger scope, band interaction,
  click act), and the combined pack awaits a fresh gate-1 showing. The fix stories' acceptance
  stands — their text and evidence are unchanged. The slice's bump moves from `patch` to
  `minor` (a new capability, `dock/R18`), declared at Plan. ITEM-221 joins ITEM-219 on this spec
  (card ≠ slice; two cards, one spec pack).
- **2026-11-20 — the bottom-pin trigger corrected to the band's top (owner-reported boundary).**
  Live review found the strip missing when the live header's bottom was *inside* the scrollport
  edge but under the pinned NEXT band — the band paints over the header's lower half, so it is not
  fully visible even though it has not passed the edge. The edge-only trigger missed this
  band-height gap. FR-007 now measures the header against the **band's top** when the band holds
  the edge (else the scrollport edge); SC-012 and
  `test_the_bottom_strip_stands_while_the_band_covers_the_header` pin the boundary, and the
  per-frame sampler + the full-in-view pin now use the same line. Reproduced at 1920×1200
  (header bottom 1065, edge 1067.9, band top 1032.7): strip hidden before, stands after. 12/12 in
  the module.
- **2026-11-20 — the bottom pin redesigned to a faithful header clone, fully-off only (owner;
  supersedes the two bottom-pin rulings above).** Live review: "can you not make it double? make
  it like the top pin" — the "LIVE · label" strip was a second, separate-looking band, and it
  showed alongside the partly-visible header ("the strip and the live entry headers both are
  showing"). Ruling: the bottom pin must be the header's own face pinned (like the top pin), and
  only when the header is fully off-screen below, never alongside a partly-visible one.
  Implemented as a `cloneNode(true)` of the live `.entryrow` in the list-level slot, shown only
  while `header.top > scrollport.bottom`. The band-top trigger and the "stack above the NEXT
  band" ruling above are superseded — under the fully-off trigger the band is caged off-screen
  with its block, so the pin holds the edge alone. FR-007/FR-009, US4 and SC-008..012 rewritten;
  5 bottom pins (faithful copy, no-doubling, per-frame, click act, reduced motion). 11/11 in the
  module.
- **2026-11-20 — bottom pin starts as soon as the header goes off, like the top pin (owner;
  latest, supersedes the fully-off-only trigger above).** Live review: "the headers should start
  pinning as soon as it is starting to go off-screen (just like the top)". The trigger moves back
  to the scrollport edge — `header.bottom > scrollport.bottom` — so the clone stands while the
  header is still partly visible. No-doubling is kept by making the clone sit flush at the edge
  and cover the departing header (its top at/above the header's top) rather than appear as a
  separate band above it; one header is ever visible. FR-007/FR-009, US4, SC-008..012 rewritten;
  11/11 in the module. Measured partial state: header top 708 / bottom 764 vs edge 727.9, clone
  671.9–727.9 with `coversHeader: true`, `copyExact: true`.
- **2026-11-20 — NEXT band always sticky, pin above it (owner; latest).** "can you make the NEXT
  bar always sticky instead and make the bottom pin above that?" The NEXT band moved from the live
  li (where a yield rule hid it when the block's end was in view, and sticky caged it off-screen
  when the block was wholly below) into a list-level `li.nextband-slot` — it now holds the edge at
  every scroll position while a next entry exists (FR-011), its click/label unchanged (FR-004).
  The pin's slot follows it in the list and its inset is measured from the band's rendered top so
  the two abut (FR-007/FR-009). The "pin holds the edge alone / covers the band" arrangement is
  superseded. E2E RED first (4 failures: band caged 781 px, hidden, no abut), then green; 12/12
  module and 67/67 full dock regression. Measured stack: NEXT 692.7–727.9, pin 636.7–692.7,
  `abuts: true`.
- **2026-11-20 — NEXT band always visible + pinned even when the list fits; header pin staged early (owner; superseded by the latest).** Live review:
  "the NEXT band is always visible regardless the next entry position is on-screen or not" and
  "i think you should pre-pinned right before any part of the live entry headers going off-screen".
  Native-UI choice: stage while the header is still fully visible, within ~one row-height (≈56 px)
  of the edge. The NEXT band's yield rule is removed — it shows whenever a next entry exists.
  To make it pin with no scroll, `#entryList` is `min-height:100%` and a flex column with the slots
  at its flow bottom (`margin-top:auto`), and `#runBody` loses its bottom padding; the band lands
  flush at 0 in both scroll and no-scroll states (measured 1033–1068 at 1920×1200, 693–728 at
  420×860). The pin trigger moves to `row.bottom > box.bottom - row.height - 0.5`. The pin's inset
  drops the stale `-10` (padding removed), now `box.bottom - bandRect.top`. FR-004/FR-007/FR-011,
  SC-012/SC-013, UI/UX, assumptions and CHK014 updated; the yield test becomes
  `test_the_next_band_is_always_visible_even_when_the_list_fits`. 12/12 module.
- **2026-11-20 — NEXT band yields when the whole list fits (owner; superseded by the latest).**
  1920×1200: the band showed "NEXT Jadi SpertiMu" directly under row 12 "Jadi SpertiMu" with empty
  space below — it had no edge to pin to (the list fits the viewport), so it sat in flow after the
  last row and duplicated it. The band stays list-level (never caged) but its show condition is the
  live block actually reaching past the fold (`liveEntry.bottom > box.bottom + 6`); when the whole
  list fits it yields. E2E RED then green; 12/12 module, 66/67 full regression (the one error is
  the known ITEM-220 chevron settle-wait race, at line 914, unrelated). Verified: 1920×1200 band
  hidden, list ends cleanly at row 12; 420×860 band pinned at the edge, pin abuts above.
- **2026-11-20 — pin clips at the NEXT band's top, not a row early (owner; latest, supersedes the
  staged-early trigger above).** Live review: "it gets too tall. maybe only clip right when the bottom
  part of the entry headers is touching the next band." Staging one row-height early added a second
  header's height of chrome while the header was still clear. The trigger moves to the band's own
  top — `row.bottom > bandRect.top` (or the scrollport edge when no band) — and reuses that band
  measurement for the inset. At that boundary the clone sits exactly over the real header (one
  header-height, bottom at the band's top), so it takes over with no added height. The per-frame
  sampler's boundary and the staged test follow the band top. FR-007/SC-012, mechanism finding,
  US4 acceptance, README updated; 12/12 module, 67/67 full dock regression.
