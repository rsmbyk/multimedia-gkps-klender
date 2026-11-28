# Feature Specification: pin the live header at the top as soon as it goes off screen

**Slice**: `specs/248-dock-top-pin-early`
**Branch**: `feat/248-dock-top-pin-early`
**Created**: 2026-11-28
**Status**: Draft
**Input**: the owner's request — "can you make the live entry header to start pinning at the top as soon as it going off screen just like the it is at the bottom"

## Current behaviour (read, not assumed)

- `static/styles/design/obs-dock.css`: the live header is `position: sticky; top: -4px` inside its
  own `.entryli`, so it holds the top edge while that block straddles the scrollport (R17), and is
  carried away when the whole block passes above.
- `static/web/obs-dock.js` `updateTopBand()` (spec 242 / R19): a clone in a zero-height list-level
  `.topband-slot` shows only when the whole block is above (`li.bottom <= box.top + 0.5`).
- `updateLiveBand()` (spec 208 / R18): the bottom clone shows as soon as the header's bottom reaches
  the NEXT band's top (or the viewport bottom) — i.e. at the first sign of clipping, not once the
  whole block is below.

## User Scenarios & Testing

### US1 — The top pin starts at the requested boundary (P1)

**Why this priority**: the whole request is the boundary at which the pinned representation takes
over from the in-flow header.

**Independent Test**: with a deep entry live, scroll until the boundary is crossed and read the pin
visibility, its edge offset, and the real header's position in the same frame.

**Acceptance scenarios**

1. **Given** the live header approaches the top edge **When** the requested boundary is crossed
   **Then** one faithful copy of the header stands at the top edge and the real header is not drawn
   a second time.
2. **Given** the pin is up **When** scrolling returns the live header to full view **Then** the
   native header owns the edge on that frame with no clone beside it.
3. **Given** a go to is on air **When** the list scrolls **Then** the go-to's `.offstrip` is
   unchanged. *(Superseded wording: "no service top pin appears" — a manual check on 2026-11-28
   found the service pin present with a Go To on air on both develop and the slice; see research
   D006. The earlier wording is kept here as a retraction, not silently rewritten.)*

**Clarified (owner, 2026-11-28)**: the pin starts as soon as the live header itself starts to be
clipped by the top edge — the header's natural top crossing the scrollport edge, where CSS sticky
currently clamps it — and the clone takes over from the sticky header at that exact point, mirroring
R18's bottom boundary. The whole-block-above rule in R19 is superseded for this boundary.

### US2 — Existing dock pin behaviour is preserved (P2)

**Why this priority**: the bottom pin, the NEXT band, the go-to strip and the header corner state
are separate, already accepted behaviours (R14/R15/R17/R18/R19).

**Independent Test**: run the existing `tests/e2e/test_dock_top_pin.py`,
`test_dock_stuck_corner.py` and `test_dock_stuck_corner.py`-adjacent pin modules; unchanged states
stay byte-identical except where the new boundary deliberately moves the top pin.

**Acceptance scenarios**

1. **Given** the live block is wholly above the fold **When** the list rests **Then** the top pin
   still stands flush at the edge.
2. **Given** the bottom pin or NEXT band is in its own state **When** the top boundary changes
   **Then** neither changes.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | As soon as the live header's natural top crosses the scrollport's top edge (the point where sticky clamps it and clipping begins), a faithful clone in a list-level slot SHALL take over the edge, covering the native header in that same paint so exactly one header is visible. The whole-block-above boundary of R19 is superseded. | `dock/R19` (modified) |
| FR-002 | The pin's state SHALL be reconciled on every path that moves or resizes the list, including the first paint of a click and reduced motion. | `dock/R19` (modified) |
| FR-003 | Clicking the pin SHALL re-centre the live row, keep the screen and return to following, writing no display state. | `dock/R15` (unchanged) |
| FR-004 | The bottom pin, NEXT band, go-to strip, header wash and entry anatomy SHALL be unchanged. | `dock/R18`, `dock/R3`, `dock/R14` (unaffected) |

### Key Entities

- **Live header pin** — the list-level clone and its slot; the single state read by `updatePins()`.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | The pin appears at the agreed boundary, top offset 0 px from the scrollport edge, one header-height, faithful label. | new E2E + live probe |
| SC-002 | Pin visibility equals the agreed geometry on every sampled frame of a glide, 0 mismatches. | new E2E + frame sampler |
| SC-003 | Existing dock pin modules stay green except separately recorded machine-local reds. | targeted E2E modules |

## UI/UX

`live preview at http://127.0.0.1:8793/obs/dock` — the worktree's code with the change applied,
served by `specs/248-dock-top-pin-early/preview/serve.sh` against the real compose DB. The unchanged
build answers on `http://127.0.0.1:63404/obs/dock`. The change is state on a live list, so a static
replica cannot show it. Measured by `preview/probe_boundary.py`, dark mode at 1×, 420 × 860,
first service, entry 26 live, 490 frames stepped 4 px at a time:

| Reading | develop (before) | slice (after) |
| --- | --- | --- |
| First pin visible at scrollTop | 1164 | **1056** |
| Live block top at takeover | -110 px | **-2 px** |
| Live block bottom at takeover | -2.31 px | 105.69 px |
| Real header top at takeover | -40.31 px (already off) | **0 px** |
| Pin top / bottom | 0 / 38 px | 0 / 38 px |
| Pin label | `26Entri 26` | `26Entri 26` (exact) |
| Real header while pinned | visible, off-screen | **hidden while covered** |
| Boundary mismatches | 0 (old rule) | 0 (new rule) |
| Takeover hop | — | 0 px (pin top = header top) |

- The pin starts **108 px earlier** in scroll terms, at the header's own top edge rather than the
  block's bottom edge; its corners stay flat top (0 px) / round bottom (9 px).
- Radius and geometry after the block is fully above are unchanged from spec 242 (top 0 px, one
  header-height, faithful label); the bottom pin and NEXT band keep their own states.
- Every state is reachable by hand on the live URL; see `preview/README.md`.

## Assumptions

- Live entry header only, mirroring the bottom pin — carried over from spec 242's scope; the owner
  has not asked to pin any other header.
- **Live-preview chronology**: the pack was written first, then the uncommitted code/CSS edit was
  applied in the slice worktree and served live at the URL above before gate 1. No commit exists
  yet; per the repo's rule the first commit comes at Fold.
- **One visible header**: while the clone owns the edge the native header is hidden with
  `visibility: hidden` (not `display`), so its sticky box stays in flow and covering it moves no
  geometry. The clone drops that class when copied.
- **No new endpoint, dependency or migration** is expected: this is a boundary change in
  `updateTopBand()` and a paint-only CSS rule.

## Clarifications

### Session 2026-11-28

- Q: what boundary starts the top pin? → A: as soon as the live header itself starts to be clipped
  by the top edge; the clone takes over from the sticky header at that exact point, mirroring the
  bottom pin. (owner, native question UI)
