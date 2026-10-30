# Feature Specification: the dock fills whatever panel it is given

**Slice**: `specs/164-dock-fluid-width`
**Branch**: `fix/164-dock-fluid-width`
**Created**: 2026-10-29
**Status**: Accepted (owner, gate 1, 2026-10-29)
**Input**: the owner's report — *"the dock view does not fill the entire width. you never know the size of the dock"* — and *"keep the one column for picker"* after the first pass.

## What the page does today

`.dock` is the dock page's only panel (`multimedia/web/templates/reading/obs_dock.html:50`), and it
carries a phone-width cap with a centring margin:

```css
.dock { display: flex; flex-direction: column; width: 100%; max-width: 560px; height: 100%;
        margin: 0 auto; background: var(--rail-bg); overflow: clip; }
```

(`static/styles/design/obs-dock.css:29–39`). At 560px and below the cap is invisible; above it the
panel stops growing and floats in the middle of the page. Measured on develop (1.23.1, compose `web`,
`/obs/dock`, height 900):

| viewport | panel box | panel at x | picker row |
| --- | --- | --- | --- |
| 420 | 420 × 900 | 0 | 404 |
| 560 | 560 × 900 | 0 | 544 |
| 700 | 560 × 900 | 70 | 544 |
| 900 | 560 × 900 | 170 | 544 |
| 1200 | 560 × 900 | 320 | 544 |
| 1440 | 560 × 900 | 440 | 544 |
| 1920 | 560 × 900 | 680 | 544 |

The cap is the only width rule in the sheet — no other element carries a `max-width`, so everything
below it (head, rows, transport) is already fluid and simply inherits the panel's width. The comment
at the top of the same file says the dock *"IS the panel, so it fills the viewport"*; the cap
contradicts it.

An OBS dock panel is a browser window whose viewport **is** the panel, and its size is whatever the
operator drags: a narrow column beside the scene list in one layout, half a monitor in another, the
full browser window when the dock is reviewed outside OBS. The page therefore has no width to guess.

## User Scenarios & Testing

### US1 — The panel is the page, at every dock size (P1)

**Why this priority**: it is the reported defect; a capped panel wastes the dock's width, and the
wasted strip is where the operator expects rows, dates and the scrollbar.

**Independent Test**: open `/obs/dock` at 320, 420, 560, 900, 1440, 1920 and 2560 wide and read the
panel's box: it equals the viewport at every size, sits at x = 0, and the document reports no
horizontal overflow.

**Acceptance scenarios**

1. **Given** the dock at any viewport from 320px to 2560px, **When** the picker is open, **Then** the
   panel's width equals the viewport's width and its left edge is the viewport's left edge.
2. **Given** a viewport wider than 560px, **When** the page lays out, **Then** no strip of bare
   background is left beside the panel.
3. **Given** any of those widths, **When** the page is measured, **Then** `scrollWidth` equals
   `clientWidth` — the fill never produces a horizontal scrollbar.

### US2 — The picker stays one column, and that column fills the panel (P1)

**Why this priority**: the fill must not be bought by fanning the bucket list into columns — the
owner rejected that pass — and a one-column list that is capped again would reintroduce US1.

**Independent Test**: at 1440 and 1920, read the picker body: `display: block`, every bucket section
at the same x, the first row's width equal to the body's content width and, at 1440, 1424px of a
1440px viewport; the date right-aligned at the row's right padding.

**Acceptance scenarios**

1. **Given** the dock at 1440, **When** the picker lays out, **Then** the buckets are stacked (one
   column), and each service row spans the panel from its 8px side padding to the other.
2. **Given** a row in that column, **When** it is painted, **Then** its name starts at the row's left
   padding and its date ends at the row's right padding; the gap between them is the panel's width,
   not a fixed measure.
3. **Given** the picker scrolled, **When** a bucket head reaches the top of the scroller, **Then** it
   still sticks there — one heading band, as at 560px.

### US3 — A narrow dock is unchanged (P2)

**Why this priority**: the dock's normal home is a narrow OBS panel; the fix must be invisible there.

**Independent Test**: open `/obs/dock` at 320, 420 and 560 and compare every measured box with
develop's — they are identical, because the cap never applied below 560.

**Acceptance scenarios**

1. **Given** a 420px dock, **When** the picker paints, **Then** the panel, rows, badges and dates sit
   exactly where 1.23.1 put them.
2. **Given** a 320px dock, **When** the runner opens, **Then** its entries, head and transport keep
   their sizes and positions.

## Requirements

**FR-001** `.dock` SHALL take the viewport's full width and height at every viewport width from
320px up: `width: 100%`, `height: 100%`, no `max-width`, and no horizontal auto margin.

**FR-002** The dock page SHALL NOT scroll horizontally at any width: `scrollWidth` equals
`clientWidth`.

**FR-003** The picker SHALL stay a single column at every width: its body keeps block layout, every
bucket section paints at the same x, and no responsive layout may break the list into columns.

**FR-004** Each picker row SHALL span the picker body's content width — the panel's width less the
body's 8px side padding — with the name at the row's left padding and the date right-aligned at its
right padding.

**FR-005** A bucket head SHALL keep sticking to the top of the picker's scroller at every width.

**FR-006** No other measured thing SHALL move: the head's padding, the row's 40px minimum height and
10px padding, badge sizes, the transport's 40px arrows, the 5px scrollbar, and every box at widths of
560px and below keep their 1.23.1 values.

## Success Criteria

**SC-001** The panel's width equals the viewport's at 320, 420, 560, 720, 900, 1440, 1920 and 2560,
within 0.5px, with its left edge at 0 at every one.

**SC-002** No horizontal overflow at any of those widths (`scrollWidth - clientWidth == 0`).

**SC-003** At 1440 the first picker row is 1424px wide (viewport − 16px) and at 1920 it is 1904px;
at 560 both row and panel are unchanged at 544px.

**SC-004** The picker body's computed `display` is `block` at every measured width, and all bucket
sections share one x.

**SC-005** `tests.e2e.test_obs_dock` and `multimedia.web.test_obs_dock` pass with the two width tests
in place, and both width tests fail against 1.23.1's stylesheet for the width reason, not an import
error.

## Assumptions

- **A1 — The dock page's viewport is the panel.** OBS hosts the page in a browser dock whose window
  is the panel, so "fill the dock" is "fill the viewport". No container query is kept: an earlier
  pass carried `container: dock / inline-size` for a layout that was rejected, and a containment
  context with nothing querying it is dead weight.
- **A2 — "Fills the width" is the panel's box, not a text measure.** No `max-width` or
  `max-inline-size` is introduced on rows, heads or the body to keep line length comfortable; the
  date moving to the panel's right edge is the intended reading of the ask.
- **A3 — One column is the owner's decision (2026-10-29).** A bucket-per-column layout at 760px and
  up was built, measured (three 468px columns at 1440, three 628px at 1920) and shown; the owner
  asked for the one column instead. The requirement is recorded so the variant is not rebuilt from
  the same complaint.
- **A4 — The runner is not re-flowed.** It already fills the panel; its entries are a sequence, so
  they keep one column and the full-width row. Nothing in this slice changes the runner's layout.
- **A5 — Regression guard, not a breakpoint.** The CSS gains no media query and no breakpoint: the
  sheet has one width rule fewer than it had, which is the whole change.

## Preview

Live at `http://127.0.0.1:8799/obs/dock` — `manage.py runserver` from this slice's worktree against the
compose database, so the picker, the runner, the theme switch and the keyboard are the real code
paths. Resize the window; the dock answers at every size.

## UI/UX

| | today (1.23.1) | this slice |
| --- | --- | --- |
| panel, 1920 viewport | 560 × 900 at x 680 | 1920 × 900 at x 0 |
| panel, 1440 viewport | 560 × 900 at x 440 | 1440 × 900 at x 0 |
| panel, 900 viewport | 560 × 900 at x 170 | 900 × 900 at x 0 |
| panel, 560 viewport | 560 × 900 at x 0 | 560 × 900 at x 0 (unchanged) |
| picker row, 1440 | 544 | 1424 |
| picker row, 1920 | 544 | 1904 |
| picker row, 320 | 304 | 304 (unchanged) |
| picker columns | 1 | 1 (never more) |
| bucket head, sticky | yes | yes |
| horizontal overflow, 320–2560 | 0 | 0 |
| row height, font, badge, transport | mockup metrics | unchanged |

Every state reachable by hand on the live preview: picker and runner, light and dark, 320 through
2560, with the bucket head pinned while the list scrolls.
