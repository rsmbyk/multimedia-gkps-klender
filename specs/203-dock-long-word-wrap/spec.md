# Feature Specification: A long word wraps in the dock runner

**Slice**: `specs/203-dock-long-word-wrap`
**Branch**: `fix/203-dock-long-word-wrap`
**Created**: 2026-11-19
**Status**: Accepted
**Input**: "a really long words do not get wrapped in service title and entry headers" — with a
screenshot of the operator dock's runner: a service named with a run of `h`, a pasted Google Drive
URL as the first entry, three image filenames under it, and a horizontal scrollbar across the body.

## User Scenarios & Testing

### US1 — An unbroken run wraps inside the box that owns it (P1)

**Why this priority**: This is the reported defect. Today the runner paints a long word past its own
box, under the head's buttons and past the panel's right edge, and the body grows a horizontal
scrollbar — the operator cannot read the name of the service they are running or the entry they are
about to project.
**Independent Test**: Open the dock on a service whose name is 64 unbroken characters and whose first
entry is a pasted URL, at a narrow panel. No painted text sits past its own box and the body has no
horizontal scrollbar.

**Acceptance scenarios**

1. **Given** a service named `h`×64 **When** the dock opens its runner at a 456px panel **Then** the
   title wraps inside its own column (3 lines), no part of it is painted past that column, and the
   three head buttons keep their place beside it.
2. **Given** an untitled Text entry whose body is a 69-character URL **When** its header is drawn
   **Then** the quiet line wraps inside the header's text box (2 lines) instead of running 178px past it.
3. **Given** the same URL rendered as a screen row inside the open block **When** the block is open
   **Then** the line wraps inside the row instead of running past it.
4. **Given** any of the above **When** the runner body is measured **Then** `scrollWidth` equals
   `clientWidth` — the body scrolls vertically only.

### US2 — What already fits is untouched (P2)

**Why this priority**: A wrapping rule that changes the layout of text which already fit is a
regression, not a fix. The dock's rows are measured controls (spec 198's chevron geometry, spec 119's
38px row); the rule must reach only the run that overflows.
**Independent Test**: The same service read twice — with the rule and with its value restored to
`normal` — gives identical boxes for every row whose text already fits.

**Acceptance scenarios**

1. **Given** entries named `random.jpg` and `images (1).jpeg` **When** the rule applies **Then** each
   keeps its line count (1), its height (19.6px header, 38.0px row) and its width.
2. **Given** a 137-character hyphenated filename that already wraps at its hyphens **When** the rule
   applies **Then** it keeps the same 3 lines and the same 58.7px header height.
3. **Given** any entry header **When** the rule applies **Then** the number column keeps its width
   (33.6px) and left edge (18px), and the chevron keeps its trailing offset (10px from the row's right
   edge) and its vertical centre (0px off the row's centre).
4. **Given** a panel wide enough that the whole name fits (900px) **When** the rule applies **Then**
   the title stays on one line at the same height and width, and every box whose text already fits is
   unchanged; a run wider than the panel itself still wraps.

### US3 — What declares its own cut keeps truncating (P3)

**Why this priority**: Two runner labels are deliberately one line ending `…`. Wrapping them would
break the transport's own geometry, so the rule must not reach them.
**Independent Test**: With a long next-entry name, the next band's label and the off-strip's label
stay one line, clipped with an ellipsis.

**Acceptance scenarios**

1. **Given** a next entry whose name is wider than the band **When** the band is drawn **Then** its
   label stays one line ending `…` (`white-space: nowrap`, `text-overflow: ellipsis`).
2. **Given** the picker's service list **When** the same 64-character name is drawn there **Then** it
   wraps exactly as it does today — the picker's own rule is unchanged.

### Edge Cases

- **When** the panel is 320px wide **Then** the title wraps to 5 lines inside its 148px column and the
  body still has no horizontal scrollbar (today: 464px and 271px of overflow).
- **When** a media filename is 255 characters with no break opportunity **Then** it wraps inside the
  header's text box; the header grows taller and the chevron stays centred on the whole row.
- **When** the entry is a section break **Then** nothing changes — a hairline carries no text.
- **When** the live entry's header is pinned (sticky) and wraps to several lines **Then** it pins as
  it does today, at its own taller height.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | The runner's service title SHALL wrap a run wider than its own box at that box's edge, and SHALL NOT paint any part of it past the box, at every panel width. | `new: dock/R16` |
| FR-002 | An entry header's text — a media filename, an untitled entry's quiet lines, a song's reference and title — SHALL wrap inside the header's text box rather than run past it. | `new: dock/R16` |
| FR-003 | A screen row inside an open block SHALL wrap its line inside the row rather than run past it. | `new: dock/R16` |
| FR-004 | The runner body SHALL NOT scroll horizontally because of text: its `scrollWidth` SHALL equal its `clientWidth`. | `new: dock/R16` |
| FR-005 | Text that already fits its box SHALL render unchanged — the same line count, height and width — and the row's own geometry (number column, chevron offset and centre) SHALL be unchanged. | `new: dock/R16` |
| FR-006 | A label that declares its own cut SHALL keep truncating: the next band's label and the off-strip's label stay one line ending `…`. | `new: dock/R16` |
| FR-007 | The picker's service name SHALL keep wrapping as it does today; this slice changes no picker rule. | `dock/R6` (unchanged, pinned) |

### Key Entities

No model, field or endpoint changes. The values the fixtures use are the widest the columns already
accept: `TataIbadah.name` and `ServiceEntry.title` are 64 characters, `ServiceEntry.media_filename`
is 255, and a Text entry's `text` is unbounded — the same fixtures spec 137 used for the reading page.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | No painted text past its own box in the runner's title, entry headers or screen rows | Range-rect spill ≤ 1px on each, at 320, 456 and 900px panels |
| SC-002 | The runner body scrolls vertically only | `#runBody.scrollWidth - clientWidth == 0` at the same three widths |
| SC-003 | A run that fits is unchanged | With-rule vs rule-restored boxes equal for every fitting row: height, width, line count |
| SC-004 | The row's geometry is unchanged | Number column 33.6px at left 18; chevron 10px off the row's right edge, 0px off its centre |
| SC-005 | The truncators keep truncating | `white-space: nowrap`, `text-overflow: ellipsis`, one line, `scrollWidth > clientWidth` |

## UI/UX

Live preview at `http://127.0.0.1:8767/obs/dock` (worktree `~/Projects/multimedia-gkps-klender-203`,
service 149). The runner is built by `obs-dock.js` from a fetched library, so a static page cannot
show it. `preview/probe.py` reads the same page twice — as it ships, and with the one candidate rule
injected — and writes both sets of numbers. See `preview/README.md`.

The candidate rule, and the whole of the proposed change:

```css
.serviceline, .entryrow__t, .screenerow { overflow-wrap: anywhere; }
```

- **Layout / position**: the title keeps its 284px column at a 456px panel (148px at 320px, 728px at
  900px); the head's three buttons keep their 38px boxes and their place. The number column keeps
  33.6px at left 18px; every chevron keeps 10px off its row's right edge and 0px off its centre.
- **Size / spacing**: measured before → after at 456×1087, dark, 1×.
  | box | before | after |
  | --- | --- | --- |
  | `.serviceline` spill | 328px, 1 line, 20.3px tall | 0px, 3 lines, 60.8px tall |
  | `.dock__head` scroll − client | 170px | 0px |
  | `#runBody` scroll − client | 135px | 0px |
  | URL entry header spill | 178px, 1 line, 19.6px | 0px, 2 lines, 39.1px |
  | URL screen row spill | 97px, 28.8px tall | 0px, 47.7px tall |
  | `random.jpg` header | 19.6px, 1 line | 19.6px, 1 line (unchanged) |
  | hyphenated filename header | 58.7px, 3 lines | 58.7px, 3 lines (unchanged) |
  | `.servicedate` | 16.9px tall, left 14 | 16.9px tall, left 14 (unchanged) |
  At 320px: title spill 464 → 0 (1 → 5 lines), body 271 → 0, screen row 243 → 0.
  At 900px the 64-character name fits its 728px column and is unchanged (1 line, same height and
  width, before and after). A run wider than the panel itself — the 200-character filename the
  fixture uses, out of the 255 the column allows — still wraps there, so the rule is
  width-independent rather than a narrow-panel case.
- **Colour / typography**: unchanged. `.serviceline` stays 15px/650, the entry header 14.5px/1.35
  (`.entryrow__title` 14px), the screen row 13px/1.45. No token, face or colour is touched.
- **States**: the live row keeps its selected fill and its sticky pin at its own taller height; the
  hover face still tints the whole line including the chevron; the open/closed chevron states are
  unchanged (spec 198). Empty and error states carry no long run.
- **Motion**: none added. The block's 230ms morph and the view's 200ms slide are untouched; a taller
  header simply gives the morph a taller end value.
- **Responsive**: measured at 320, 456 and 900px. The rule is width-independent — it breaks a run
  only where it would otherwise overflow, so a wide panel renders as today wherever the text fits.

## Assumptions

- **The slice covers the runner's three text surfaces, not only the two named.** The request names
  the service title and the entry headers; the open block's screen rows overflow by the same
  mechanism (97px on the same URL) and are half of what gives the body its horizontal scrollbar.
  Fixing only the two named boxes would leave the scrollbar. — measured, not guessed.
- **`overflow-wrap: anywhere`, not `break-word`.** The dock's own picker already uses `anywhere`
  (`.servicerow__n`), and every box here is either a block in a `min-width: 0` column or a flex item
  with `min-width: 0`, so the min-content collapse spec 137 guarded against on the reading page
  cannot move a control here — verified: the chevron and number geometry are identical before and
  after. — the reading page's `break-word` choice stays as it is; this is the dock's own convention.
- **No line clamp.** A hyphenated filename already wraps to 3–4 lines in this same list and the owner
  reads it that way today; an unbroken run gets the same treatment rather than a new cut. — the
  request asks for wrapping, not truncation.
- **The reading page, projector and overlay are out of scope.** All three measured clean on the same
  service at 456px (zero spill, zero document overflow); `reading/R13` already holds the rule.
- **The two truncating labels keep their cut.** `.nextband__label` and `.offstrip__label` declare
  `nowrap` + ellipsis by design (spec 119); the rule inherits into them but cannot wrap a `nowrap`
  line. Pinned by FR-006 rather than left to chance.

## Clarifications

### Session 2026-11-19

- No open markers: every ambiguity above was settled by measurement against the owner's own service
  149, and each decision is recorded as an assumption with its evidence.
