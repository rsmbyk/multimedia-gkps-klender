# Feature Specification: the live entry header pins at the top when its block is above the view

**Slice**: `specs/242-dock-top-pin`
**Branch**: `feat/242-dock-top-pin`
**Created**: 2026-11-25
**Status**: Accepted at gate 1, 2026-11-25 (the preview below preceded the pack; see Assumptions)
**Input**: the owner's request, 2026-11-25 — "can you make the entry headers to stay pinned at
the top when the entry is off-screen just like the bottom pin?" Scope confirmed the same day
through the question tool: **live entry header only, mirroring the bottom pin**; a header that
loses liveness has no pin.

The runner's live header is `position: sticky; top: -4px`, but sticky cannot leave its own `li`.
It holds the top edge while the entry's block straddles the scrollport and is carried away with
the block once that block is wholly above the edge. The bottom half of the pair was completed in
spec 208 (`dock/R18`) with a faithful header clone in a list-level sticky slot. This slice adds
the mirror at the front of the list: the same clone, the same geometry read, the same click act,
so the live label stays at the top for as long as its entry is off-screen above.

## User Scenarios & Testing

### US1 — The live header stays at the top once its block passes above (P1)

**Why this priority**: the operator can be browsing above the live entry while it stays on air;
the current screen's identity should not vanish just because its block scrolled past the top.

**Independent Test**: with a deep entry live in the long service, scroll the list to its bottom
so the live block is entirely above the scrollport. A faithful copy of the live header stands
flush at the top edge — one visible header, not a second band.

**Acceptance scenarios**

1. **Given** a live entry whose block is entirely above the scrollport **When** the list rests
   **Then** a clone of its header (number + name + verse subtitle + chevron, selected face) stands
   with its top at the scrollport edge, flat top corners (0 px) and round bottom corners (9 px),
   and the real header is not drawn a second time.
2. **Given** that pin is up **When** the header is still off above **Then** no other header pin
   shows at the bottom; the NEXT band keeps its unchanged spec 208 behaviour.
3. **Given** `prefers-reduced-motion: reduce` **When** the block goes above the edge **Then** the
   pin paints in that same paint, with no stale frame.

### US2 — The pin gives way to the real header on the same frame (P1)

**Why this priority**: a second header beside the in-flow one reads as a duplicate entry, the
same fault the owner rejected for the bottom pin in spec 208.

**Independent Test**: click the pinned copy, or scroll back by hand; on every sampled frame the
pin's visibility equals the block's geometry, and the copy is gone once the block reaches the
fold.

**Acceptance scenarios**

1. **Given** the pin is up **When** the block's bottom reaches the scrollport's top edge
   **Then** the pin is gone on that frame.
2. **Given** a hand scroll back to the live entry **When** its header is in view again **Then**
   the native sticky header alone owns the top edge — no clone above it.
3. **Given** a crossing to another live entry **When** the old block is above and the new one is
   in view **Then** only the new header's geometry governs; the old clone is gone in that paint.

### US3 — Clicking the pin is the centre control's act (P2)

**Why this priority**: the bottom pin already has one ruled interaction; the top pin must not
invent a second way to change what is on air.

**Independent Test**: click the pinned copy while a deep screen is live; the list glides back to
the live row, the display state is byte-identical, and following returns.

**Acceptance scenarios**

1. **Given** the top pin is up **When** the operator clicks it **Then** the live row glides back to
   the centre, the current screen stays on air, and following returns — no screen write.
2. **Given** a go to is on air **When** the list is scrolled **Then** no service top pin appears;
   the go to's `.offstrip` is unchanged.

### Edge Cases

- **When** the live entry is the first in the service and the list is at rest **Then** no pin
  shows; the header is in flow exactly as before.
- **When** the live entry has no inner block (a break or an empty header) **Then** the clone is
  still a faithful copy of that header; no chevron is invented.
- **When** the window resizes **Then** the pin's visibility re-reconciles with the new fold.
- **When** the whole list fits the viewport **Then** the pin is never shown — the block cannot be
  above the edge.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | A list-level sticky slot SHALL lead the runner list and hold a faithful clone of the live entry's header — number, name, verse subtitle, chevron, selected face — whenever that entry's whole block is above the scrollport's top edge (`li.bottom <= box.top + 0.5`). The clone SHALL stand flush at the edge with a flat top (0 px) and the header's 9 px bottom radius. A header that loses liveness SHALL lose its pin in the same paint. | `dock/R19` (new) |
| FR-002 | The pin's state SHALL be re-evaluated on every path that moves or resizes the list: scroll frames, state sync, centring glides (including the first paint of a click), crossing and toggle morphs, their landings, and window resize. The NEXT band's motion guard SHALL NOT suppress it. Under reduced motion the state SHALL paint in the same frame. | `dock/R19` (new) |
| FR-003 | Before the block passes above the edge the native sticky header SHALL keep its own top-pin and corner state (spec 208, R17); no clone SHALL be shown alongside it. When the pin takes over it SHALL cover the departing header rather than add a second band's height. | `dock/R17` (unchanged), `dock/R19` |
| FR-004 | Clicking the top pin SHALL re-centre the live row, keep the current screen and return to following — the centre control's own act (R15) — and SHALL NOT write a different screen to the display state. | `dock/R15` (unchanged), `dock/R19` |
| FR-005 | The bottom pin, the always-visible NEXT band, the go to's `.offstrip`, the header wash (R14) and the entry/block anatomy (spec 198) SHALL be unchanged. | `dock/R18`, `dock/R3`, `dock/R14` (unaffected) |

### Success Criteria

| ID | Criterion | Verification |
| --- | --- | --- |
| SC-001 | With the live block entirely above the fold, the top pin is visible, its top is 0 px from the scrollport edge, its radius is `0px / 9px`, and its label matches the live header. Before: no pin at all. | new E2E `test_the_top_pin_stands_when_the_live_block_is_above` + `preview/probe_top.py` |
| SC-002 | The visibility equals the geometry on every sampled frame of the glide home — 0 mismatched frames. | new E2E `test_the_top_pin_tracks_the_block_per_frame` + probe |
| SC-003 | Scrolling back leaves the native sticky header alone and the pin gone. | new E2E `test_the_real_header_takes_over_when_the_block_returns` |
| SC-004 | Clicking the pin glides the live row to centre (≤1 px off), leaves the display state byte-identical and returns following. | new E2E `test_clicking_the_top_pin_performs_the_centre_act` |
| SC-005 | Reduced motion paints the pin in the same paint. | new E2E `test_the_top_pin_lands_instantly_under_reduced_motion` |
| SC-006 | Existing dock E2E modules stay green except the recorded machine-local red ITEM-220. | `tests/e2e/test_obs_dock.py`, `test_dock_stuck_corner.py`, `test_dock_open_reset.py` |

## UI/UX

`live preview at http://127.0.0.1:8793/obs/dock` — the worktree's own code with the change
applied, served by `specs/242-dock-top-pin/preview/serve.sh` against the real compose DB. The
unchanged build answers on `http://127.0.0.1:63404/obs/dock`. The change is state on a live list,
so a static replica cannot show it. Measured by `preview/probe_top.py`, dark mode at 1×,
420 × 860, first service, entry 26 live (a long block):

| State | Build | Pin visible | Pin top | Radius (top/bottom) | Label |
| --- | --- | --- | --- | --- | --- |
| Header in view, list at top | develop | no | — | — | — |
| Header in view, list at top | slice | no | — | — | — |
| Live block wholly above, list at bottom | develop | **no** | — | — | — |
| Live block wholly above, list at bottom | slice | yes | 0 px from scrollport edge | 0 px / 9 px | `26 Entri 26` — exact match with the real header |

- Bottom pin at the top-of-list state: visible on both builds (unchanged). At the above-fold
  state: hidden on both — the two pins never compete.
- Click on the slice's pin: **25 sampled frames, 0 mismatched** between visibility and the
  block's geometry; display state byte-identical; live row **0.48 px** from the centre; following
  `true`. Develop has no pin to click; its centre control gives the same landing.
- Screenshots: `preview/shots/before/`, `preview/shots/after/`.

## Assumptions

- **Live entry only.** The owner chose this over every-header variants when asked. A non-live
  header keeps its normal flow; only the live label gets a pin.
- **"Off-screen" means the whole block above the edge.** The native sticky header already holds
  the edge while any of its block is on screen; the clone exists only for the range sticky cannot
  reach. This is the exact mirror of spec 208's bottom half, not a second sticky on the same row.
- **Faithful clone, not a caption band.** The slot holds `cloneNode(true)` of the live `.entryrow`,
  re-cloned only when the source node changes. It drops `aria-current`/`aria-controls`: it is a
  pinned representation, not a second current row or toggle.
- **The slot is zero-height with an absolutely positioned clone.** Toggling its visibility must
  not change the list's flow: a 56 px in-flow slot re-showed itself by pushing the block back
  above the fold (measured feedback during the E2E glide), so the pin is drawn without taking
  space. This is a paint-only change to the slot, not to the header's own geometry.
- **Click act borrowed from the bottom pin** (spec 208, FR-010; owner ruling): re-centre, keep the
  screen, return to following. The click never writes the display state.
- **The extra `updatePins()` at the start of a centring glide** is paint-only reconciliation for a
  list the click or sync clamp may already have moved; it changes no layout and no motion curve.
- **No new dependency, endpoint, migration or template change** — vanilla JS and the dock's own
  stylesheet. The spec pack is written after the live preview edit (live-preview-first chronology);
  the change stayed uncommitted until Fold.
- **Spec number 242, card ITEM-257 and branch `feat/242-dock-top-pin`** were checked against
  `develop`, `origin/develop`, all unmerged local branches and untracked worktree packs; all were
  free at the time of writing. `bump` is declared at Plan, not here.

## Revision

- **2026-11-25 — scope settled before Specify.** The owner's question was answered through the
  native question tool: live entry only. No other revision; the spec has no open clarification
  markers.
