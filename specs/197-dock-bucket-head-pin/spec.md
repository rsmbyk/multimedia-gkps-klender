# Feature Specification: The dock's bucket head owns the strip above its label

**Slice**: `specs/197-dock-bucket-head-pin`
**Branch**: `fix/197-dock-bucket-head-pin`
**Created**: 2026-11-16
**Status**: Accepted (Gate 1, 2026-11-16)
**Input**: "the pinned date group headers are not perfectly pinned to the toolbar (there is a small gap between it and the toolbar)" — reported on the dock picker with a 449×604 screenshot of `/obs/dock` in responsive mode (2026-11-16) — then, on the first preview, "there is a slight difference of the pinned header when the list is fully scrolled to the top and when it is not", and "can you also increase the gap between the date groups slightly?".

## User Scenarios & Testing

### US1 — A bucket head owns the strip above its label (P1)

**Why this priority**: the operator reads the top of the picker to know which age bucket the rows in view
belong to. Today the row above the pinned head keeps painting in a 4px band between the dock's head and the
bucket's label, so two things occupy that edge at once and the label reads as floating rather than pinned.
The defect is on the list's most-frequented surface — every scroll of the picker passes through it.

**Independent Test**: open `/obs/dock`, scroll the picker past the first bucket's rows, and look at the edge
under the toolbar divider: only the bucket head paints there.

**Acceptance scenarios**

1. **Given** the picker scrolled so a bucket head is at the top, **When** the strip between the scroller's
   top edge and the label is probed, **Then** it holds no row — the head's box starts at the scroller's top
   edge (0.0px) and a hit test at scroller top + 2px returns the head.
2. **Given** the same scroll position, **When** the row above the group is half-scrolled out, **Then** none
   of it paints above the head.
3. **Given** the picker at `scrollTop` 0, **When** it is painted, **Then** the label sits at the same
   distance under the divider as it does pinned — nothing moves when the scroll begins.
4. **Given** the runner, **When** its current entry pins at the top and the next band pins at the foot,
   **Then** both keep their accepted positions: this slice moves the picker's bucket head only.

### US2 — The keyboard cursor still parks clear of the head (P2)

**Why this priority**: the picker is driven by `↑`/`↓` from the dock's own focus, and the scroller reserves
a strip at its top so a row scrolled into view is not hidden. The head's pinned foot — the line the reserve
is derived from — must not move, or a keyboard-scrolled row lands under it.

**Independent Test**: walk the picker's cursor through a group boundary; every row it lands on is fully
visible below the head.

**Acceptance scenarios**

1. **Given** the cursor moves up through a pinned head, **When** a row is scrolled into view, **Then** its
   top edge is at or below the head's bottom edge — never underneath it.
2. **Given** the cursor moves down, **When** it scrolls a row in at the foot, **Then** the parking is
   unchanged from today.

### US3 — The buckets are separated by air, not only by their labels (P2)

**Why this priority**: the picker draws no rule between buckets, so the only thing marking the boundary is
the label and the space above it. At 10px above the label the next bucket reads as a continuation of the
rows, not a new group. This is a look change, taken on the owner's word during review ("can you also
increase the gap between the date groups slightly?"), and it must not disturb the pin US1 fixes.

**Independent Test**: scroll to a group boundary; the space between the previous group's last row and the
next label is 26px, and the pinned head above it is unmoved.

**Acceptance scenarios**

1. **Given** two consecutive buckets, **When** the boundary is measured, **Then** the label sits 26px below
   the previous group's last row (10px on develop, 14px with US1 alone).
2. **Given** the same boundary, **When** the next head pins, **Then** it pins at the scroller's top edge with
   its label 14px below the divider — the extra air scrolls away with its section and never enters the pin.
3. **Given** the first bucket, **When** the picker is at rest, **Then** the label is still 14px below the
   divider: the air is between groups only, not above the list.

### Edge Cases

- **When** a group ends and the next head is still in the content, **Then** no head is at the top and the
  edge keeps showing the rows in flight — that is the group boundary, not this defect.
- **When** a head is crossing the top edge, **Then** the label travels with it until the head is fully there;
  that is the head arriving, not the rest-versus-pinned difference US1 scenario 3 rules out.
- **When** the dock is narrower or wider than 449px, **Then** the fix holds: it is vertical, and the head
  spans the body's content width at every width (spec 164's fluid width).
- **When** the strip holds a row's *padding* rather than its glyphs, **Then** the strip still paints — the
  row is there whether or not its letters are — which is why the probe counts pixels and hit-tests the
  element, not the glyphs.
- **When** the theme is light, **Then** the head's background and the row's are still distinct colours, so
  the same fix applies with no colour rule of its own.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | The dock picker's bucket head covers the strip above its label: its box starts at the scroller's top edge, so no row paints between the dock's head and the bucket's label, whether the head is at rest or pinned. | `reading` (R33, modified) |
| FR-002 | The label's distance under the divider is the same at rest and pinned — no jump when the scroll begins. | `reading` (R33) |
| FR-003 | The head's pinned foot does not move: the scroll reserve stays 37px, so a row scrolled into view parks exactly where it does today. | `reading` (R33) |
| FR-004 | Nothing else moves: the head's bottom edge (100.52px), the first row's top (100.52px), the row box, the runner's pinned entry and its strip, and the next band's foot pin keep their values. | `dock` (R3's live block, no change) |
| FR-005 | Consecutive buckets are separated by 12px of air, carried by the section, so the label of the next bucket sits 26px below the previous group's last row; the first bucket's label stays 14px below the divider. | `reading` (R33, modified) |

### Key Entities

- **Bucket head** — the `h3.group__head` above each age bucket in the dock picker; sticky, 36.52px tall at
  449px once its own 14px top padding carries the sky above the label.
- **Picker scroller** — `.dock__body#pickBody`; its padding box is the scrollport the head pins to, and it
  carries no top padding so the head can start at the edge.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | At every scroll offset where a head is at the top, the strip above the label is empty of row pixels. | 4× screenshots of the strip at 514 offsets: 0 non-background pixels (was up to 9,715 at `scrollTop` 98). |
| SC-002 | The hit test at the scroller's top + 2px returns the head at every such offset. | `document.elementFromPoint` — `H3.group__head` (was `BUTTON.servicerow`). |
| SC-003 | The label's offset under the divider is one number in both states. | 14.00px at rest and at 1,564 of 1,600 scroll offsets, the rest being fractional frames as a head crosses the edge; 14.00px on `develop` too, so the invariant is preserved rather than introduced. |
| SC-004 | The cursor-parked row is never under the head, and the head's foot does not move. | head bottom 100.52px at every pinned offset, unchanged; clearance measured at every cursor step ≥ 0px. |
| SC-005 | Nothing below the head moves. | first row top 100.52px at rest on both branches; row, badge and separator boxes identical. |
| SC-006 | The air between buckets is measurable and does not disturb the pin. | label 26.0px below the previous group's last row (10.0px on develop); pinned head still at 0.0px with its label 14.0px below the divider. |

## UI/UX

Measured on `/obs/dock` at 449×604, dark theme, `device_scale_factor` 1 and 4:

- **Layout / position**: the picker's scrollport top is 64.00px from the viewport top. Before, the head's box
  started at 68.00px — 4px of `.dock__body` top padding sat above it and the row showed through — and its
  32.52px box put the label at 78.00px. After, the picker body carries no top padding, the head's box starts
  at 64.00px and its own padding carries the same sky: the label is at 78.00px in both states and the head's
  foot is still at 100.52px.
- **Size / spacing**: head 36.52px tall, padding `14px 6px 7px` (from `10px`; the +4px is exactly the strip
  it now owns), 11.5px/650 type at `.10em` tracking; **12px of air between consecutive buckets, carried by the
  section** (`#pickBody section + section { padding-top: 12px }`), which puts the next label 26.00px below the
  previous group's last row — 10.00px on develop, 14.00px with the strip change alone. That is the dial for
  "slightly": 0px removes it, 12px is the accepted value. Row 40px minimum, 10px padding, unchanged; picker
  body `0 8px 10px`, runner body `4px 8px 10px` untouched; `scroll-padding-top` 37px, unchanged.
- **Colour / typography**: no colour rule added. The head paints `--rail-bg` (`#232019` dark) over the strip.
- **States**: rest (`scrollTop` 0) head box 64.00px, label 78.00px · pinned head box 64.00px, label
  78.00px, strip empty · group boundary (no head at the top) unchanged · both themes identical in geometry ·
  320–2560px widths identical in geometry.
- **Motion**: none; the head is sticky, not animated.

Preview: `specs/197-dock-bucket-head-pin/preview/index.html` (static — the real picker markup and
`obs-dock.css`, two panes differing only in these three numbers, with a live readout of the head's offset,
the strip's topmost element and the air above the next label). Live: `python manage.py runserver
127.0.0.1:8767 --noreload` in the slice worktree, `/obs/dock`, scrolled past the first bucket; the developed
page answers the same route on `:63404`.

## Assumptions

- The 14px between the divider and the label is the accepted look, so it is the fixed point: the strip's
  ownership moves to the head instead of the head moving. The runner keeps the body's 4px because its own
  pins compensate for it with `top: -4px`; the picker does not need that compensation any more.
- The strip is silent at most offsets because a row's padding is the same `--rail-bg` as the head; it shows
  only where a row's glyphs or a badge cross it. Both cases are the same defect and the same fix.
- Nothing below the head depends on where the head's *top* is: the reserve is derived from its foot, which
  does not move, so the keyboard path needs no second number.

## Clarifications

### Session 2026-11-16

- The first shape of this slice pinned the head with `top: -4px` and dropped `scroll-padding-top` to 33px.
  On the first preview the owner observed "there is a slight difference of the pinned header when the list is
  fully scrolled to the top and when it is not": that shape kept the label at 78.00px at rest and moved it to
  74.00px when pinned. **Retracted** — the head's `top` stays 0, the picker body loses its top padding
  instead, and the head's own padding carries the sky, so the label is at 78.00px in both states and the
  reserve returns to 37px with the head's foot.
- The owner then asked for "the gap between the date groups" to grow slightly, and after seeing 8px asked for
  slightly more. **12px** is the accepted value, carried by the section so it never enters the pin (boundary
  10.00px → 26.00px from the previous group's last row). It is one number and can be dialled without touching
  anything else. Accepted by the owner at the revised gate 1 (2026-11-16); gate 2 was already accepted.
  No `[NEEDS CLARIFICATION]` markers remain.