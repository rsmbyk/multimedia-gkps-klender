# Feature Specification: The Transfers list draws each boundary once

**Slice**: `specs/149-transfer-separator-seam`
**Branch**: `fix/149-transfer-separator-seam`
**Created**: 2026-10-28
**Status**: Accepted (owner, gate 1, 2026-10-28; gate 2, 2026-10-28 — all eight checklist items ticked)
**Input**: "why is there multiple consecutive separators here? (i opened it from tranfers button in main rail after uploading)"

## What the dialog does today

The Transfers dialog (`#mediaTransfersDialog`, `reading/base.html`) lists jobs the local companion
has run, newest first, drawn from `static/web/media-handoff.js`. Each row carries its own
`border-bottom: 1px solid var(--divider)` (`components.css:2752`); the script also inserts an
`<hr class="media-transfers__divider">` before the first transfer that finished after this session's
first transfer started, and that rule carries `border-top: 2px` with `margin: 9px 0`
(`components.css:2757`) — so at that seam the two are stacked 9px apart and read as two separators.

The same list has no scroll container: the dialog carries `max-height: min(86vh, 46rem)` and
`overflow` stays `visible`, so a list taller than the dialog runs over the dialog's own bottom
padding. With the nine rows of the report the list's box ends 19px past the dialog's inner bottom
edge and the last row's border paints 4px above the dialog's bottom border — a second doubled
separator, at the dialog's edge. With fifteen rows the same list paints 451px outside the dialog,
over the page behind it.

Measured on the static preview (`preview/preview.html`, 1920×1200, dpr 1): the seam's two lines sit
10.5px apart, 1px and 2px wide; the row separators elsewhere are single 1px lines 72px apart.

## User Scenarios & Testing

### US1 — The seam between this session's transfers and the older ones is one line (P1)

**Why this priority**: this is the report. A boundary drawn twice reads as a rendering fault, not as
grouping.

**Independent Test**: open the dialog from the rail on a list whose first two transfers finished
after this session's first transfer started; count the lines where the groups meet — one.

**Acceptance scenarios**

1. **Given** a completed list of nine transfers with the two newest in this session, **When** the
   dialog is opened from the rail, **Then** the boundary between them is a single 2px line in
   `--divider` and no second line sits within 20px of it.
2. **Given** the same list, **When** the seam is inspected, **Then** the line sits 9px below the text
   above it and 9px above the text below it, and no other row's separator has moved.
3. **Given** a list whose every shown transfer is older than this session, **When** it renders,
   **Then** the divider is the first thing under the title and still draws exactly one line.
4. **Given** a dialog opened from the media library's own Transfers button, or one holding an active
   transfer, **When** it renders, **Then** there is no divider and every boundary is the single 1px
   row border, unchanged.

### US2 — The list scrolls inside the dialog instead of painting over it (P2)

**Why this priority**: it is the same fault seen at the dialog's edge — a boundary and the dialog's
own border 4px apart — and it becomes a real spill as soon as the list outgrows the dialog.

**Independent Test**: open a dialog holding fifteen completed transfers; scroll the list to its end
and find the last row's border 22px above the dialog's bottom border, with nothing painted outside
the dialog at any scroll position.

**Acceptance scenarios**

1. **Given** more transfers than the dialog's `max-height` holds, **When** the dialog opens, **Then**
   the list itself scrolls and no row paints outside the dialog's border.
2. **Given** that scrolling list, **When** it is scrolled to its end, **Then** the last row's border
   sits the dialog's 22px bottom padding above the dialog's own border.
3. **Given** the same dialog, **When** the list is scrolled at all, **Then** the `Transfers` title
   stays in place above the list.
4. **Given** a list short enough to fit, **When** it renders, **Then** the dialog takes its natural
   height, no scrollbar appears, and every row is exactly where it was before this slice.

### Edge Cases

- **When** the list holds a single transfer **Then** it draws one row, one border, no divider, and
  the dialog is its natural height.
- **When** the only unseen transfer is the first row **Then** the divider sits directly under the
  title with its two 9px margins, and the row below still has no border stacked on it.
- **When** a transfer failed or was cancelled **Then** its row's text and its border are unchanged.
- **When** a name is longer than the row **Then** the ellipsis and the row height are unchanged.
- **When** the window is narrower than 612px **Then** the dialog narrows by `calc(100vw - 32px)` as
  today and the list keeps scrolling; no new breakpoint is introduced.
- **When** the theme is dark **Then** every line keeps using `--divider` (`#3A362F`) and nothing else
  changes.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | At the boundary between transfers that finished in the current session and older ones, the list SHALL draw exactly one horizontal line: 2px, `--divider`. | `new: media-library` |
| FR-002 | That line SHALL sit 9px from the content above it and 9px from the content below it. | `new: media-library` |
| FR-003 | Every other row boundary SHALL keep its current 1px `--divider` border, at its current position. | `new: media-library` |
| FR-004 | When the rows are taller than the dialog's `max-height`, the list SHALL be the element that scrolls, and the `Transfers` title SHALL stay above it. | `new: media-library` |
| FR-005 | The list's painted box SHALL NOT extend past the dialog's inner bottom edge; at the end of its scroll the last row's border SHALL sit the dialog's 22px bottom padding above the dialog's border. | `new: media-library` |
| FR-006 | A list that fits SHALL keep the dialog's natural height and show no scrollbar. | `new: media-library` |

### Key Entities

- **Transfer row** — one companion job: a direction glyph, a name, a status (`Completed`, a
  percentage while active, `Cancelled`, `Failed`). Identity is the job id; the list is ordered by
  `ended_at` descending with active jobs first.
- **Session seam** — the divider marking where the transfers that finished after this session's
  first transfer started end. It exists only in a rail-opened dialog with no active transfer; it is
  drawn once, as the `<hr class="media-transfers__divider">`.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | The seam paints one line where the report showed two | count the painted lines within 20px of the seam on the rendered dialog: 2 → 1 |
| SC-002 | No boundary is drawn twice anywhere in the dialog | the distance from the lowest visible boundary to the dialog's bottom border: 3.5px → at least 22px |
| SC-003 | Nothing in the list paints outside the dialog | the list's box past the dialog's inner bottom edge: 19px (9 rows) and 451px (15 rows) → 0px |
| SC-004 | A short list is unchanged | the same nine rows with the divider removed: identical row count, pitch (72px) and border width (1px) before and after |

## UI/UX

Measured on `preview/preview.html` at 1920×1200, dpr 1, in both themes. The dialogs in the preview
take the product's own width and `max-height`, so the numbers are the shipped ones.

- **Layout / position**: the dialog keeps `width: min(580px, calc(100vw - 32px))`,
  `max-height: min(86vh, 46rem)` (736px at this viewport), `padding: 22px`, `border: 1px solid
  var(--divider)`, `border-radius: 12px`. The title keeps `margin: 0 0 14px`. The list becomes the
  scroll container; its box ends exactly at the dialog's padding edge (0px past it, was 19px at nine
  rows and 451px at fifteen).
- **Size / spacing**: a row keeps `padding: 13px 4px` and a 72px pitch (row box 71px + its 1px
  border). At the seam the row above loses its 1px border, so the one line sits 9px above and 9px
  below the neighbouring text; the two rows' content boxes stand 20px apart (9 + 2 + 9). The gap was
  21px across two lines (1px border, 9px, 2px, 9px) before.
- **Colour / typography**: the seam's line is `--divider` — `#D9D6CD` light, `#3A362F` dark — at 2px;
  row separators stay 1px in the same token. Row names keep weight 650, statuses 12px in `--head-ink`.
  No new colour or token is introduced.
- **States**: nine rows (the report) · fifteen rows (the overflow state) · light and dark · an empty
  list (`No transfers yet.`) unchanged · an active upload unchanged · the divider absent (library
  view) unchanged. The list's scrollbar is the app's existing thin one (spec 087's rules); it
  appears only when the list overflows, and `overflow-y: auto` is used rather than `scroll` so a
  short list shows none.
- **Motion**: none added or removed. The dialog's open animation is untouched.
- **Responsive**: no new breakpoint. Below 612px the dialog narrows by `calc(100vw - 32px)` and the
  list keeps absorbing the overflow; the title stays above it.

## Assumptions

- The seam keeps a **heavier** line (2px) instead of becoming a plain 1px separator, because it marks
  "finished while you were not looking" and would otherwise be indistinguishable from the row
  borders. —
- The seam's 1px of removed border is not kept as spacing: 9px above and below, not 10px above and
  9px below. —
- The list scrolls with `overflow-y: auto`; the dialog keeps its own `max-height`, so the title is
  fixed and only rows move. —
- The 22px bottom padding is the scroll end — no extra inner padding is added to the list. —
- When the divider appears is **not** part of this slice: the rule in `media-handoff.js` stays as it
  is. —
- The empty state, the active-transfer view and the media library's own page list are out of scope;
  they draw no divider today and are unchanged. —

## Clarifications

### Session 2026-10-28

- Q: none asked — the report named the surface and the preview reproduced it, so every open point is
  recorded as an assumption above and can be vetoed at the gate.
