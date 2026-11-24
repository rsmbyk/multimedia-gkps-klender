# Feature Specification: center the service-entry kind mark in the contents row

**Slice**: `specs/237-sidebar-mark-centering`
**Branch**: `fix/237-sidebar-mark-centering`
**Created**: 2026-11-24
**Status**: Draft — Gate 1 pending
**Input**: "center the icon in service entry sidebar vertically just like the entry numbers"
**Demand**: `ITEM-252` (new card)
**Capability**: `reading/R49` (modified)
**Preview**: live preview at `http://127.0.0.1:8776/tatib/151/` — from `/`, click the Tata Ibadah rail, then the service `111ojo`; run `python ~/.hermes/cache/scratch/gkps237/run.py runserver 0.0.0.0:8776 --noreload` from `~/Projects/multimedia-gkps-klender-237` if the server is down.

The Tata Ibadah contents row is a flex line with `align-items: baseline`. Spec 063
centred the order number with `align-self: center` under
`:root[data-section="tatib"] #chList` (and on the drag copy). Spec 214 later added
`.songrow__mark` to the same row, but that span kept the row's baseline alignment:
its 16px box sits level with the first line of the label, while the number sits at the
row's vertical middle. On a two-line song row the two columns are 11.5px apart.

The change gives the mark the same centring declaration as the number. No markup,
colour, size, spacing, label or behaviour changes.

## User Scenarios & Testing

### US1 — The mark shares the number's vertical centre (P1)

**Why this priority**: this is the reported surface. The number and icon are two
columns of one rail; when the label wraps, the icon drifting to the first line breaks
that rail.

**Independent Test**: on a service with one-line and multi-line entries, measure each
row's number and mark box centres against the row box; both read 0px.

**Acceptance scenarios**

1. **Given** a service with a passage, a song with a `Bait` line, a media file and a
   text entry **When** its contents list is shown **Then** every mark's centre equals
   its row's centre within 1px, as the number's already does.
2. **Given** the same rows in light or dark theme, hovered or selected **When** they
   are measured **Then** the mark stays centred and keeps its existing colour.

### US2 — The rest of the row does not move (P2)

**Why this priority**: centring a flex item must not shift the columns it sits between,
change row heights, or alter the label's three-line clamp.

**Independent Test**: compare mark x, label x, row height and line count before and
after at 1440px, 1024px and 390px viewports.

**Acceptance scenarios**

1. **Given** a 38px one-line row and a 53px two-line song row **When** the mark is
   centred **Then** the mark's left edge stays 42px from the row, the label's 66px,
   and both row heights stay as they were.
2. **Given** a 390px window where the song row wraps to 74px **When** it is measured
   **Then** its mark is still centred at 0px and the label still clamps at three lines.

### US3 — Drag copy and slot badge keep their seats (P2)

**Why this priority**: spec 063 centred the drag copy's number as well as the live
row's, and spec 213's corner badge is positioned against the mark box. Both must follow
the mark rather than stay behind at the old baseline.

**Independent Test**: on a fill-in row, measure the badge's offset from the mark and
from the row; then inspect a `.reorder__ghost` copy of a multi-line row.

**Acceptance scenarios**

1. **Given** a fill-in row **When** the mark is centred **Then** its corner badge stays
   on the mark's bottom-right corner (11px box at `right: -3px; bottom: -2px`) and
   moves with it, 9px above the row's bottom edge instead of 13px.
2. **Given** a row being dragged **When** the `.reorder__ghost` copy paints **Then** its
   mark is centred on the copy just as its number is.

### Edge Cases

- A section-break row paints no number and no mark; it is untouched.
- The songbook sidebar shares `.songrow` but renders no `.songrow__mark`; its number
  keeps baseline alignment as spec 063 requires.
- A three-digit order number widens its 24px box; the gap stays 8px and the mark's x
  is unchanged.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | The Tata Ibadah contents kind mark SHALL be vertically centred on its row, matching the order number, for every row of every line count. | `reading/R49` |
| FR-002 | The mark's size, horizontal seat, colour, pointer behaviour and accessibility SHALL NOT change; the label's clamp, wrap and position SHALL NOT change. | `reading/R49` |
| FR-003 | The drag copy's mark SHALL be centred on the copy, as its number already is. | `reading/R49` |
| FR-004 | No surface outside the Tata Ibadah contents list and its drag copy SHALL change. | `reading/R49` |

### Key Entities

- **`.songrow__mark`** — the 16px decorative span introduced by spec 214 inside
  `#chList a.songrow`, server-rendered and `aria-hidden`.
- **`.songrow__c`** — the order-number span already centred by spec 063; the rule to
  mirror.
- **`.reorder__ghost`** — the detached copy of a dragged row, stamped from the row's
  own markup.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | Every mark centre is at the row centre | browser readout of mark box centre minus row box centre, within ±1px, across 12 rows |
| SC-002 | Nothing else moves | mark x 42px, label x 66px, row heights 38/53/74px, badge offset 9px, all unchanged except the badge's vertical move with the mark |
| SC-003 | Drag copy follows | computed `align-self: center` on `.reorder__ghost .songrow__mark` |
| SC-004 | Both themes and all widths hold | same readout in light and dark at 1440px, 1024px and 390px |

## UI/UX

Measured on the live worktree server (`http://127.0.0.1:8776/tatib/151/`, service
`111ojo`), 1440×900 unless stated, `device_scale_factor: 1`, both themes. "Before" is
the same page with the new declaration reverted on the mark's inline style; the
shipped page has it applied.

| Row / state | Mark centre vs row | Number centre | Mark x | Label x | Row height |
| --- | --- | --- | --- | --- | --- |
| 38px one-line row — before | −4px | 0px | 42px | 66px | 38px |
| 38px one-line row — after | 0px | 0px | 42px | 66px | 38px |
| 53px song row (`HAL 1 … / Bait 1–7`) — before | −11.5px | 0px | 42px | 66px | 53px |
| 53px song row — after | 0px | 0px | 42px | 66px | 53px |
| 74px song row at 390px window — before | −22px | 0px | 42px | 66px | 74px |
| 74px song row at 390px window — after | 0px | 0px | 42px | 66px | 74px |

The 12 rows on the fixture hold these values in both themes. The slot mark's corner
badge moves with its mark: its bottom edge goes from 13px above the row bottom to 9px,
keeping its 11px box at `left: 50px` relative to the row. The mark is 16×16px, the
number box 24px, the gap 8px and the label's three-line clamp unchanged.

States reachable by hand: light/dark via the theme control, hover and selected by
pointing at rows, narrow widths by resizing to 1024px and 390px, and the drag copy by
dragging a row by its grip. No motion is added.

## Assumptions

- The drag copy is included, because the number's centring already covers it and the
  request says "just like the entry numbers"; the copy is made from the live row's
  markup, so its mark must match.
- The fix is two selectors in `static/styles/design/components.css`, sharing one
  declaration with spec 063's number rule; no template, script or endpoint changes.
- The songbook sidebar has no kind marks, so its rows are outside this change.
- The fix was applied to the worktree before gate 1 under the live-preview-first
  practice, so you could review it on the real page; the "before" numbers are that
  same page with only the new declaration reverted. The E2E module comes after the
  spec and is run red against the base rule before the edit is restored.
- `bump: patch` is expected for a user-visible fix; the level is declared at Plan and
  reviewed at gate 2, not fixed here.
- The card is new (`ITEM-252`); the owner promotes it to `Ready` after gate 1.
