# Feature Specification: A long transfer name ellipsizes instead of moving the row

**Slice**: `specs/147-transfer-icon-column`
**Branch**: `feat/147-transfer-icon-column`
**Created**: 2026-10-28
**Status**: Accepted (owner, gate 1, 2026-10-28)
**Input**: "why do some items alignments are off from the others" — owner report with a screenshot of the Transfers dialog on `/media-library/`, two of nine rows sitting left of the rest

## What the page does today

The Transfers dialog (`#mediaTransfersDialog`, `multimedia/web/templates/reading/base.html:456`)
draws one row per transfer. `static/web/media-handoff.js` builds each row as
`div.media-transfers__row > span.media-transfers__mark (the direction glyph) + div.media-transfers__main
(strong name + status label)`.

`static/styles/design/components.css:2752-2753` lays the row out as a flex line with a 12px gap, and
gives the mark a `width: 32px`. The mark is a **flex item**, so that 32px is a preferred width, not a
column: it defaults to `flex: 0 1 auto` and its automatic minimum is the 21px SVG inside it. When a
name is too long for the row, the line is short by exactly that overflow and the mark absorbs it.

Measured on the owner's own list (nine rows, 580px dialog at a 1920px window):

| Row | Mark box | Glyph left | Name + status left |
| --- | --- | --- | --- |
| the seven names that fit the column | 32px | 702.5 | 741.0 |
| `side-view-silhouette-african-elephant-…` (1133px of text) | **21px** | **697.0** | **730.0** |
| `Sujud & Terima Kasih - JCC Worship […]` (691px of text) | **22.75px** | **697.9** | **731.8** |

The two long names are not shifted by their own length; the *icon column* has been squeezed, and
everything after it starts sooner. The glyph moves only half as far as the text because
`text-align: center` re-centres the 21px SVG inside the narrowing box — which is why the column reads
as ragged by 5.5px while the words read as ragged by 11px.

`main` keeps its `nowrap` name and ellipsizes correctly; nothing is wrong with the truncation. What is
wrong is that the fixed-looking icon column is what pays for it.

## User Scenarios & Testing

### US1 — Every row's icon sits on one vertical line (P1)

**Why this priority**: this is the report. The dialog is the surface an operator reads to answer "did
every file go through?"; a ragged left edge reads as rows belonging to different lists, and the two
ragged rows are exactly the long names — the ones that most need to be scanned.

**Independent Test**: open the Transfers dialog on a list that holds both short and long names, and
measure the glyph and the text: one value each, across every row.

**Acceptance scenarios**

1. **Given** a list mixing names that fit the text column with names that do not, **When** the dialog
   draws, **Then** every row's glyph box is 32px wide and every glyph's left edge has the same x.
2. **Given** the same list, **When** the dialog draws, **Then** every row's name and status label start
   at the same x, 12px right of the 32px mark column.
3. **Given** a name wider than the text column, **When** the row draws, **Then** the name ends in an
   ellipsis inside the column and the row's height is unchanged (72px).

### US2 — The column survives the dialog narrowing (P2)

**Why this priority**: the dialog is `min(580px, 100vw - 32px)`. On a narrow window the text column
shrinks to almost nothing, and the same squeeze would reappear at exactly the size where the rows have
the least room.

**Independent Test**: at a 420px window, open the dialog on the same list and re-measure: one glyph x,
one text x, names still ellipsized.

**Acceptance scenarios**

1. **Given** a window narrower than 612px, **When** the dialog draws, **Then** the mark column is still
   32px and the text column takes what is left.
2. **Given** a window narrow enough that no name fits, **When** the dialog draws, **Then** every name
   ellipsizes and no row overflows the dialog horizontally.

### Edge Cases

- **When** every name fits, or every name is long **Then** the rows keep the same two x values — the
  column is not a function of the list's contents.
- **When** a transfer is active and its label is a percentage instead of `Completed` **Then** the row
  keeps the same geometry; the label's width does not affect the mark.
- **When** the list is empty, disconnected or still loading **Then** the empty paragraph keeps its
  place and this slice changes nothing about it.
- **When** the dialog is drawn from the rail's session list rather than the library button **Then**
  it is the same rows and the same geometry.
- **When** the browser is at 200% zoom **Then** the column is 32 CSS px and the constraints are the
  same ones the viewport rules already state.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | A transfer row's direction glyph occupies a column of exactly 32px, and no content in the row may narrow it. | `new: reading` → R20 |
| FR-002 | A name wider than the text column is ellipsized inside the column; it does not change the row's width, the mark's width or the row's height. | `new: reading` → R20 |
| FR-003 | Every row's name and status label share one left edge: the mark column plus the row's 12px gap. | `new: reading` → R20 |
| FR-004 | The dialog keeps its `min(580px, 100vw - 32px)` width, and the text column absorbs all narrowing. | `new: reading` → R20 |
| FR-005 | Nothing else about the list changes: the rows drawn, their order, their height, the divider between them, and the rail's own behaviour. | `new: reading` → R20 |

### Key Entities

- **Transfer row** — one job from the local companion: `direction` (upload or download, which chooses
  the glyph), `name` (rendered in one ellipsized line), `status` (rendered as `Completed`,
  `Cancelled`, `Failed`, or a percentage while active). No field is added, removed or re-shaped by
  this slice.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | In a nine-row list holding both short and long names, the spread between the smallest and largest glyph left edge is 0.0px. | E2E: `getBoundingClientRect().left` of every `svg` in `#mediaTransfersList` |
| SC-002 | The same list shows a 0.0px spread on the name/status left edge. | E2E: `getBoundingClientRect().left` of every `strong` and every status `span` |
| SC-003 | Both long names still truncate: `scrollWidth > clientWidth` on their `strong`, and the row's height stays 72px. | E2E: same run |
| SC-004 | At a 420px window the two spreads are still 0.0px and no row's right edge passes the dialog's. | E2E: same run at a narrow viewport |

## UI/UX

**Static preview at `specs/147-transfer-icon-column/preview/preview.html`** (regenerate with
`build_preview.py`). Two columns of the real dialog markup: **Now**, drawn from the stylesheet frozen
at `05379336`, and **Fixed**, the same markup with the proposed declaration. Both columns carry a live
readout of the two left edges; the numbers below are that readout at a 1920px window.

- **Layout / position**: row is a flex line, `padding: 13px 4px`, `gap: 12px`; mark column 32px;
  text column 482px in a 580px dialog (`534 − 8 − 32 − 12`). On the live page Now draws glyph x
  `702.5 / 697.0 / 697.9` and text x `741.0 / 730.0 / 731.8`; Fixed draws `702.5` and `741.0` on
  every row. In the preview (dialogs flush left, so its x values differ by the panel offset) the
  readout is: Now `mark column 32 / 21 / 22.75px`, glyph spread `5.5px`, name and label spread
  `11.0px`; Fixed `mark column 32px`, both spreads `0.0px`. At a 382px dialog (a 420px window —
  the app's `min(580px, 100vw - 32px)` is 388px there, and Chrome's own dialog
  `max-width: calc(100% - 6px - 2em)` caps the rendered box at 382px): Now `32 / 21px` with the same
  5.5px and 11.0px spreads and three names truncating; Fixed `32px` and `0.0px`.
- **Size / spacing**: mark box `32 × 33` (row 72px tall), glyph `21 × 21` centred in it; underline
  unchanged at `1px` `--divider`; the gap between the name and the status label stays `3px`.
- **Colour / typography**: unchanged — glyph `--focus`, name 16px `--ink`, status `--head-ink` 12px.
- **States**: the row has no hover, focus, active or disabled state of its own, before or after. The
  long-name state and the all-short state must both be reachable in the preview; the empty,
  disconnected and active-percentage rows are drawn by the same list and are shown by the live page.
- **Motion**: unchanged; nothing animates on load or resize.
- **Responsive**: `min(580px, 100vw - 32px)`, rendered as 580px at a 1440px window and 382px at a
  420px one; the text column goes 482 → 284px and the two x values are unchanged. At 200% zoom the
  column stays 32 CSS px.

## Assumptions

- **The 32px column is the thing to keep, not the 21px glyph.** The fix pins the box the glyph is
  centred in; the glyph keeps its authored 21px and its centring. Widening the glyph, or setting the
  box to `width: 21px`, would move every row's text 5.5px left of where it is today — a second change
  nobody asked for.
- **Only the Transfers dialog changes.** The service-media status dialog draws its rows as a grid with
  a fixed 38px column (`components.css:2760`), so it has no such collapse; touching it would be
  `unrequested` work.
- **The list is not otherwise re-shaped.** No row cap, no reordering, no change to the rail, the
  library button, or the companion API.
- **The name column keeps `nowrap` + `ellipsis`.** The alternative — wrapping long names — costs row
  height, which the reported list shows is not what the operator wants: every row reads at one glance.
- **No data or API change.** The fix is CSS plus whatever a test needs to count as evidence.

## Clarifications

### Session 2026-10-28

- No open items. The request named the symptom and the surface; the mechanism was measured before
  Specify, and every default taken is listed under Assumptions. Zero `[NEEDS CLARIFICATION]` markers
  remain.
