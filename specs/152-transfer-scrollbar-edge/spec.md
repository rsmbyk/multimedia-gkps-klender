# Feature Specification: The Transfers scrollbar sits at the dialog's edges

**Slice**: `specs/152-transfer-scrollbar-edge`
**Branch**: `feat/152-transfer-scrollbar-edge`
**Created**: 2026-10-29
**Status**: Accepted (owner, gate 1 revision 2026-10-29; gate 2, 2026-10-29 — all ten checklist items ticked)
**Input**: "make the scrollbar touches the edge" — with a screenshot of the Transfers dialog over
`/media-library/` — then, at gate 1, "can you make the scrollbar also touches the vertical edges of
the modal?", settled as **the bottom edge**: the bar keeps starting under the title and now runs down
to the dialog's bottom border.

## What the dialog does today

The Transfers dialog (`#mediaTransfersDialog`, `multimedia/web/templates/reading/base.html`) lists the
local companion's jobs. Its body is `<div id="mediaTransfersList" class="media-transfers__list">`, the
element that scrolls since spec 149 (`overflow-y: auto`). The list is a plain child of the dialog, so
it starts at the dialog's *content* box: the dialog's `padding: 22px` and its 1px border stand between
the list's box and the dialog's own edges on all four sides, and the engine paints the scrollbar
against the list's box — inside the padding.

Measured on the running app (headed Chromium, 1440×760, dpr 1, `develop` @ `24a6d6d2`, fifteen
completed transfers, opened from the Media Library's Transfers button):

- the dialog's border box is x 430→1010, y 53.2→706.8 (580 × 653.59, `border: 1px`,
  `padding: 22px`, `border-radius: 12px`, `max-height: min(86vh, 46rem)`);
- the list's box is x 453→987, ending at y 683.8 — 23px of dialog on every side (22px padding + 1px
  border);
- the app's 5px scrollbar (spec 087) paints in that box's last five columns, **982→986, leaving 22px
  of dialog canvas between the bar and the dialog's right border**, and its lane stops **23px above
  the dialog's bottom border** — the bar reads as floating inside the dialog rather than as the
  dialog's own edge;
- the rows' content runs 453→982: 23px from the dialog's left border edge and 28px from its right.

With a list short enough not to scroll (two rows) there is no bar, and the rows run 453→987.

## User Scenarios & Testing

### US1 — The scrollbar is the dialog's edge (P1)

**Why this priority**: this is the report. A 5px bar 22px inside a 580px panel, stopping 23px short of
the bottom border, reads as an inset scroll area rather than as the panel's edge.

**Independent Test**: open the dialog on a list taller than the dialog; scroll it to the end and look
at the bar's bottom-right end against the dialog's border: no canvas between them.

**Acceptance scenarios**

1. **Given** a transfers list taller than the dialog's `max-height`, **When** the dialog is opened,
   **Then** the scrollbar paints against the dialog's right border, with **0px** of canvas between the
   bar's right edge and the border (was 22px).
2. **Given** the same list, **When** the bar is measured against the dialog's box, **Then** the list's
   box reaches the dialog's inner edge — 1px (the border's own width) inside the dialog's border box
   on the right **and on the bottom** (was 23px on both).
3. **Given** the same list scrolled to its end, **When** the bar's bottom is measured, **Then** the
   thumb reaches the dialog's bottom border, its rounded tip cut by the dialog's 12px corner radius
   rather than painting over it (lane: 1px above the border, was 23px).
4. **Given** the dialog opened from the rail, from the Media Library's button, at a narrow viewport or
   in the dark theme, **When** the list overflows, **Then** both edges behave as above.

### US2 — Nothing but the bar moves (P2)

**Why this priority**: the report names the dialog's edges. A fix that also shifts the text, the
separators or the scroll's end position would be a redesign of the surface, not the report.

**Independent Test**: measure the first row's content box, the `Transfers` title, an age heading, the
gap between the title and the list, and the last row at the end of the scroll, before and after; every
number is identical.

**Acceptance scenarios**

1. **Given** the scrolling list, **When** the fix is in place, **Then** the rows' content box is
   unchanged: left edge 23px from the dialog's left border edge, right edge 28px from its right
   (23px + the 5px bar) — and each row's separator line still ends at that right edge.
2. **Given** a list short enough not to scroll, **When** the dialog is opened, **Then** no bar is
   drawn, no lane is reserved, and every row sits where it does today (right edge 23px from the
   dialog's right).
3. **Given** any state, **When** the dialog is measured, **Then** the `Transfers` title and an age
   heading are still 23px from the dialog's left border edge, the list's top is still 14px below the
   title, and at the end of the scroll the last row's border still sits the dialog's 22px bottom
   padding above the dialog's bottom border.
4. **Given** the dark theme, **When** the dialog is opened, **Then** the bar is `--scroll-thumb`
   (`#45413A`) at the edges and every distance is the same as in the light theme.

### Edge Cases

- **When** the list holds one row **Then** no bar is drawn and the row is where it is today.
- **When** the window narrows so the dialog takes `calc(100vw - 32px)` **Then** the bar still sits at
  both edges and the content keeps its 23px / 28px insets.
- **When** the dialog is opened while a transfer is active (the rail's progress view) **Then** the
  list draws no age headings and the bar meets both edges exactly as in the history view.
- **When** the list is scrolled **Then** the bar tracks as it does today; at the end of the scroll its
  bottom meets the dialog's border, and its rounded tip is clipped by the corner radius — nothing
  paints outside the dialog's border.
- **When** the dialog is closed **Then** nothing is drawn and no layout changes.
- **When** a keyboard user pages through the list **Then** the keyboard path is unchanged — the slice
  touches the drawing only.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | The Transfers list's scroll container SHALL span the dialog's full inner box: its right and bottom edges SHALL each be 1px (the dialog's border) inside the dialog's border box, and its left edge 1px inside the left. | `media-library/R1` |
| FR-002 | A scrollbar painted by that container SHALL occupy the outermost part of its box, so the bar's right edge sits against the dialog's border with **0px** of dialog canvas between them (22px today), and its lane ends at the dialog's inner bottom edge (23px above it today). | `media-library/R1` |
| FR-003 | The rows' content box SHALL NOT move: its left edge SHALL stay 23px from the dialog's left border edge and its right edge 23px + the bar's width (28px with the 5px bar, 23px without it) from the dialog's right border edge. | `media-library/R1` |
| FR-004 | The `Transfers` title and an age heading SHALL stay 23px from the dialog's left border edge; the list's top SHALL stay 14px below the title; and at the end of the scroll the last row's border SHALL stay the dialog's 22px bottom padding above the dialog's bottom border. | `media-library/R1` |
| FR-005 | A list that does not overflow SHALL draw no bar, SHALL reserve no lane, and SHALL keep every row where it is today. | `media-library/R1` |
| FR-006 | The bar SHALL keep spec 087's drawing: 5px wide, `--scroll-thumb` (hover `--scroll-thumb-hover`), rounded, no stepper buttons, transparent track. | `media-library/R1` |
| FR-007 | The dialog SHALL clip its content to its rounded border, so nothing — the bar included — paints over the 12px corners. | `media-library/R1` |

### Key Entities

- **Transfer list** — the dialog's scroll container (`#mediaTransfersList.media-transfers__list`).
  Today its box stops at the dialog's padding edge on all four sides; this slice widens it to the
  dialog's border edge on the right and the bottom, and insets its content back by the dialog's own
  22px.
- **Scrollbar** — the engine-painted 5px lane at the inline-end of that container. It has no DOM, so
  the slice constrains the container's box and the lane follows.
- **Row content** — the `.media-transfers__row` box inside the list's padding. It is the anchor every
  existing measurement of this dialog uses (spec 147's icon column, spec 149's pitch and its 22px
  end-of-scroll gap); it must not move, and neither must the scroll's end position.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | No canvas between the bar and the dialog's right border, and the lane reaches the bottom border | painted columns between the bar's right edge and the border: 22px → 0px; the bar's lane bottom against the border: 23px → 1px |
| SC-002 | The list's box reaches the dialog's inner edges | dialog border-box right − list box right: 23px → 1px; dialog border-box bottom − list box bottom: 23px → 1px |
| SC-003 | The content is where it was | first row's content left: 23px → 23px; right: 28px → 28px with the bar, 23px → 23px without it |
| SC-004 | The frame and the scroll's end are where they were | title 23px, age heading 23px, title→list 14px, last row at the end 22px above the bottom border — identical before and after |
| SC-005 | Every state keeps SC-001 to SC-004 | the same numbers at 1440×760 and 420×820, light and dark, rail-opened and library-opened |
| SC-006 | Nothing paints outside the dialog | no bar pixel outside the border's curve at any scroll position |

## UI/UX

Measured on the live app (headed Chromium — headless paints overlay scrollbars and shows no bar at
all, so it cannot be the instrument here) at 1440×760, dpr 1, `develop` @ `24a6d6d2`, and on
`preview/preview.html` for the two states side by side. The dialog is 580px wide, `max-height`
653.59px at this viewport.

| | Today | After |
| --- | --- | --- |
| dialog border box | x 430 → 1010, y 53.2 → 706.8 | unchanged |
| list box | x 453 → 987, bottom 683.8 | x 431 → 1009, bottom 705.8 |
| scrollbar lane | x 982 → 986, ends 23px above the bottom border | x 1004 → 1008, ends 1px above it |
| canvas between the bar and the right border | **22px** | **0px** |
| thumb's bottom at the end of the scroll | 24.4px above the bottom border | 2.4px (its rounded tip clipped by the 12px corner) |
| first row's content | x 453 → 982 | x 453 → 982 |
| age heading | x 453 | x 453 |
| title | x 453 → 987 | x 453 → 987 |
| title bottom → list top | 14px | 14px |
| last row at the end of the scroll | 22.6px above the bottom border | 22.6px |

- **Layout / position**: the list's box moves 22px rightward and 22px downward at its edges only — its
  left edge and its top stay put, so the bar still starts under the title and now runs to the bottom
  border. The content box does not move at all.
- **Size / spacing**: unchanged everywhere the eye reads it — row padding `13px 4px`, 72px pitch, 22px
  dialog padding, `margin: 0 0 14px` under the title, age headings at `20px 0 2px`, and the 22px the
  last row keeps above the bottom border at the end of the scroll (now the list's own `padding-bottom`
  rather than the dialog's).
- **Colour / typography**: unchanged. The bar keeps `--scroll-thumb` (`#B4B0A6` light, `#45413A`
  dark) and `--scroll-thumb-hover`; no new token.
- **States**: fifteen rows (the report's overflow) · two rows (no bar, no lane) · fifteen rows
  rail-opened (no age headings) · narrow (382px dialog) · light and dark · scrolled to the start, the
  middle and the end · hovered bar · the corner clip at the bottom-right radius.
- **Motion**: none added. The dialog's 190ms open animation and its scroll behaviour are untouched.
- **Responsive**: no new breakpoint. Below 612px the dialog is `calc(100vw - 32px)` and the list keeps
  its 22px inset on every side; measured at 420×820 the bar meets both edges as at 1440.

## Assumptions

- **The right and bottom edges; not the top.** The bar keeps starting 14px under the title, because
  reaching the top edge would mean the scroll area covers the title too (the title would become a
  pinned line inside it). Asked at gate 1 and settled: bottom edge only. — *(owner decision, gate 1
  revision, 2026-10-29)*
- **No reserved gutter.** The lane is not held open with `scrollbar-gutter: stable`: that would move
  every row 5px inwards in the short-list state, which is more than the report asks. Today's 5px
  difference between the scrolling and the non-scrolling states stays exactly as it is. —
- **The dialog's padding stays the source of the inset.** The list takes a negative margin equal to
  the dialog's own `22px` on the right and the bottom, and pads its content back by the same amount;
  if that padding ever changes, the two move together. —
- **The dialog clips its content.** `overflow: clip` on the dialog, so the bar's bottom end is cut by
  the 12px corner instead of painting over it. The dialog has no scrollable content of its own, so
  clipping changes nothing else. —
- **The Media Library's own page list and the service-media dialog are out of scope** — the report
  shows the Transfers dialog, and neither of those surfaces has a scrollbar at rest. —
- **Engine**: the fix is plain box geometry (`margin`, `padding`, `overflow`) and holds in the engines
  that paint the custom bar and in those that use `scrollbar-width: thin` (spec 087's split); nothing
  new is depended on. —

## Clarifications

### Session 2026-10-29

- Q: none asked before gate 1 — the report named the surface and the number is measurable; the open
  points are the assumptions above.
- Q (gate 1 revision): "can you make the scrollbar also touches the vertical edges of the modal?" →
  A: **the bottom edge only**; the bar keeps starting under the title. Sent back to Specify as
  revision 2: FR-001/002 gained the bottom, FR-004 kept the 22px end-of-scroll gap, FR-007 (the corner
  clip) is new, and the preview's After column now carries both rules.
