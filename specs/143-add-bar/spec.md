# Feature Specification: the add bar opens over the seam, and nothing moves

**Slice**: `specs/143-add-bar`
**Branch**: `feat/143-add-bar` (rebased onto `develop` after 142's merge; carries one commit, `77f36a3c`)
**Created**: 2026-10-28
**Status**: Accepted (owner, gate 1, 2026-10-28)
**Input**: "reduce the moving parts when the cursor is moving in and out of the service entry areas … the entry needs to be pushed down for the add row to appear" — then "keep the row above … but keep the entry still", then "make the add buttons background solid", "make the divider a bit more muted", "add the same gaps above the first", "make it softer and more muted on rest", "center the buttons horizontally"

## What the page does today

Hovering an entry reveals the two add rows around it (spec 037). Each row is in the flow and
expands from nothing to 43.6px — 8px of padding above and below a 27.6px button — so the page
reflows under the pointer:

| measured on `/tatib/142/` | value |
| --- | --- |
| the row, at rest → revealed | 0px → **43.6px** |
| the entry below it | pushed **+45.2px** |
| the entry under the pointer | pushed **+31.6px** (the row above it opened), **+13.6px** for the first entry (the start bar) |
| a sweep of the pointer down eight entries | **234.8px** of accumulated movement |

`static/web/entries.js` carries a `poised` guard — pointer coordinates compared between `mouseover`
and `mouseout` — whose comment names the cause: *"the row above it expands in flow and pushes a short
item out from under a stationary pointer."* The guard survives the oscillation; it does not remove it.

## User Scenarios & Testing

### US1 — The entry under the pointer never moves (P1)

**Why this priority**: this is the report. Every other story is about how the bar looks while it
does that.

**Independent Test**: point at entries 1–8 in turn and measure each one's own top before and after:
every delta is 0.0px, while both surrounding rows are open.

**Acceptance scenarios**

1. **Given** a stage at rest, **When** the pointer enters any entry, **Then** that entry's own top
   does not change, nor does any other entry's, and the page's scroll height is unchanged.
2. **Given** an entry is hovered and its two rows are open, **When** the pointer moves to the row
   it just opened, **Then** nothing moves: the row is already where the pointer went.
3. **Given** the first entry is hovered, **When** the start bar opens above it, **Then** the first
   entry does not move — the bar is drawn in the head's own margin.
4. **Given** a hover ends, **When** the rows close, **Then** nothing shifts back.

### US2 — The bar is usable where it is drawn (P1)

**Why this priority**: a bar that floats over the page must not steal the entry's own controls, and
must still be reachable by keyboard.

**Independent Test**: with a row open, hit-test the entry's Preview/Edit/Delete buttons at their top
edge and at their middle — both land on the button — and Tab into the row's first button: it opens.

**Acceptance scenarios**

1. **Given** a row is open, **When** the pointer reaches the entry's own controls, **Then** they are
   hit-testable at every point, because the bar's hit area is only as wide as its buttons.
2. **Given** a row is closed, **When** its band takes focus by Tab, **Then** the row opens and its
   buttons are reachable.
3. **Given** a row is open and the pointer leaves both the entry and the row, **When** the closing
   transition runs, **Then** the buttons are no longer clickable.
4. **Given** a touch screen, where nothing hovers, **Then** the rows are drawn open and their buttons
   remain reachable.

### US3 — The seam is legible without being loud (P2)

**Why this priority**: the bar sits on a line; if the line is invisible at rest the bar appears from
nowhere, and if it is strong the page grows a second rule competing with the section break.

**Independent Test**: on `/tatib/142/` at rest, the seam reads as a faint hairline; pointed at, the
same line brightens and the bar appears on it, centred.

**Acceptance scenarios**

1. **Given** a stage at rest, **When** it is drawn, **Then** each seam paints a 1px line at
   `opacity: .15` of `color-mix(--focus 40%, --divider)`.
2. **Given** a row is open, **When** it is drawn, **Then** the line is the same colour at `.6`.
3. **Given** a row is open, **When** it is drawn, **Then** its bar is centred horizontally on the
   column, and its buttons sit centred on the line.
4. **Given** a button is hovered, **Then** its border is solid and its fill opaque, so the line does
   not read through it.

### Edge Cases

- **When** the reading pane is narrow enough that the four buttons would overflow the column
  **Then** the bar wraps or shrinks inside the column; it never crosses the pane's edge.
- **When** an entry is short — a section break at 56px — **Then** the bars around it still clear its
  rule, because they are centred on the seams above and below.
- **When** `prefers-reduced-motion` is set **Then** the line and the bar appear without the 140ms
  fade.
- **When** a modal is opened from an entry **Then** the entry keeps its hover fill and the bars stay
  where they were.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | Opening a row SHALL NOT change the layout: no entry's top, no block's position and no scroll height SHALL move when a row opens or closes, on hover, focus or modal-origin. | `new: reading` |
| FR-002 | The bar SHALL be drawn over the seam: `.entry__add` and `.entry__start` SHALL keep a 20px slot in the flow and their bar SHALL be absolutely positioned, centred on that slot. | `new: reading` |
| FR-003 | Each seam SHALL paint a 1px line at rest at `.15` opacity of `color-mix(--focus 40%, --divider)`, and at `.6` while its row is open. | `new: reading` |
| FR-004 | An open bar's hit area SHALL be no wider than its buttons, so an entry's Preview / Edit / Delete remain hit-testable at every point. | `new: reading` |
| FR-005 | A row SHALL open from the entry above it, from its own band's hover, or from keyboard focus inside it; the start bar SHALL open from the first entry's hover as well. | `new: reading` |
| FR-006 | An add button SHALL keep its resting style (canvas fill, dashed `--divider` border, `--head-ink` label) and SHALL take a solid `--focus` border and an opaque `color-mix(--ink 8%, --canvas)` fill when hovered. | `new: reading` |
| FR-007 | The gap between two blocks SHALL be 20px, the first seam SHALL measure the same 53px of white between the title's words and the first line as between two entries, and the section break SHALL take 8px of its own above and below. | `new: reading` |
| FR-008 | The section break's rule and diamond SHALL use `color-mix(--divider 62%, --canvas)`; its 56px box, its 2px rule and its centre diamond SHALL otherwise be unchanged. | `new: reading` |

### Key Entities

- **Row** — `.entry__add` (between two blocks) and `.entry__start` (above the first). A 20px slot in
  the flow, plus a 34px bar drawn on top of it.
- **Seam line** — the 1px rule every row paints, full column width, at the slot's vertical centre.
- **Bar** — the four buttons, `width: max-content`, centred on the column and on the line; its hit
  area is exactly its own box.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | Nothing moves | top of every `.tatib__item--acts` before and after hovering each of the first eight: all **0.0px**, page height unchanged |
| SC-002 | The bar floats | a row opened on hover has `position: absolute` on its bar and the row's own height stays 20px |
| SC-003 | The line is a hint at rest | computed `opacity` `.15` at rest, `.6` when open; colour `rgb(141, 165, 147)` |
| SC-004 | Controls stay clickable | `document.elementFromPoint` at an open entry's Edit button returns the button at its top edge and at its middle |
| SC-005 | The keyboard reaches it | Tab into a closed row's first button leaves it with `opacity: 1` and its buttons reachable |
| SC-006 | The rhythm matches | ink gap title → first line **53px**; entry → entry **53px**; block gap **20px**; break margin **8px 0** |

## UI/UX

Measured in headless Chromium at 1440×900 against the real stylesheets, on the live branch server.

- **Layout / position**: `.entry__add` and `.entry__start` are `position: relative`, `height: 20px`,
  margin `0` (the start row `margin-top: -20px`). The bar is `position: absolute; left: 50%;
  top: 50%; transform: translate(-50%, -50%); width: max-content; height: 34px` — measured bar width
  **298.2px** for the four buttons, centred on the column (**760px** in a 1040px preview column).
- **Size / spacing**: buttons keep `padding: 5px 10px`, `font: 500 13px/1.2`, `border-radius: 8px`,
  height **27.6px**; gaps **20px** between blocks, **34px** head margin (→ **53px** of white between
  the title's words and the first line, the same as entry → entry), **8px 0** around the section
  break.
- **Colour**: seam line `color-mix(in srgb, var(--focus) 40%, var(--divider))` = **`rgb(141, 165,
  147)`**, at `.15` rest and `.6` open; section break's rule and diamond `color-mix(--divider 62%,
  --canvas)` = **`rgb(228, 226, 219)`**; button hover fill `color-mix(--ink 8%, --canvas)` =
  **`rgb(230, 228, 224)`** with a `--focus` border.
- **States**: closed (line only, `.15`); open on hover / focus / modal-origin (line `.6` + bar);
  button hover (solid border, opaque fill); touch (rows open at rest).
- **Motion**: one 140ms opacity transition per state, `--ease-timing`, with a 220ms delay on the
  closing direction so a pointer crossing a seam does not blink it.
- **Responsive**: the bar is `max-content` and centres; when the column is narrower than the bar it
  must wrap or shrink inside the column rather than cross its edge.

## Assumptions

- **The bar keeps the shipped button style.** The owner asked for a solid background only on hover;
  the resting dashed style is the product's own.
- **The seam is hinted, not signposted.** `.15` opacity is deliberately near the threshold — a seam
  you find, not a rule you read.
- **The start bar still opens from the first entry's hover.** It was briefly made band-only and the
  owner asked for it back.
- **The eight E2E tests that assert the old mechanism change with this slice**, not before it: the
  old contract (`0px` at rest, `8px` padding when open, the `13.6px` start-bar shift) is what this
  slice replaces.
- **Spec 142's surface change is a dependency, not a part of this slice**: the bar is drawn over bare
  entries, and 142 is already on `develop`.
- **The `poised` guard stays in `entries.js`** even though the cause it patched is gone: removing it
  is a separate risk, and it does no harm.

## Clarifications

### Session 2026-10-28

- Q: Which way should the add-row movement go — float, reserve, or move into the controls column? →
  A: **keep the in-flow look, but the bar floats over the seam** (owner, 2026-10-28).
- Q: Do the rows above and below both open? → A: **yes, both**, and the entry being pointed at must
  stay still (owner, 2026-10-28).
- Q: Should the seam be visible at rest? → A: **yes, but barely** — "just so that you know there will
  be something when you hover there" (owner, 2026-10-28).
- Q: Where should the buttons sit horizontally? → A: **centred on the column** (owner, 2026-10-28).
