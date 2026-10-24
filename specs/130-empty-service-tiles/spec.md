# Feature Specification: The empty Tata Ibadah is centred, and its five kinds are tiles

**Slice**: `specs/130-empty-service-tiles`
**Branch**: `fix/130-empty-service-stage`
**Created**: 2026-10-25
**Status**: Accepted (owner, gate 1, 2026-10-25; the spec, plan, tasks and analysis pack accepted at
gate 2 the same day)
**Input**: "center the empty tata ibadah view (and the buttons) vertically on the page. also replace the
buttons to be a square icon-only without texts and arranged horizontally" (sent with a screenshot of an
empty `25 OKTOBER 2026` service whose five add actions sit as a full-width column under the heading, near
the top of a page that is otherwise blank below).

## User Scenarios & Testing

### US1 — An empty service sits in the first quarter of the reading area (P1)

**Why this priority**: the screenshot is the defect. The block is the only content on the page and it sat
just under the date, leaving the bottom two thirds of the page blank, so the page read as unfinished rather
than as an invitation. Halfway was the first answer; the owner moved it to the quarter mark.

**Independent Test**: open a Tata Ibadah with no items; the block's centre lies a quarter of the way down the
reading area the header leaves — not half.

**Acceptance scenarios**

1. **Given** a service with no items and editing enabled, **When** its page opens at 1440×900, **Then** the
   empty block (heading, hint, tile row) has its centre on the quarter mark of the area under the header:
   measured 26.2% of that area, its top 132.8px clear of the header.
2. **Given** the same page at 1440×900, **When** the window is resized to 1280×800, 1024×700 or 390×844,
   **Then** the block stays in that first quarter at every size and never overlaps the header.
3. **Given** a service that holds at least one item, **When** its page opens, **Then** nothing moves: the
   stage keeps its header-to-body gap and its top-aligned flow.

### US2 — The five kinds are square, icon-only tiles in one row (P1)

**Why this priority**: five full-width labelled buttons repeat what the operator already knows after the
first service, and they push the block down the page. A row of tiles is the same offer in one line.

**Independent Test**: open the empty page: five square tiles stand in one horizontal row under the hint,
each showing only a glyph; hovering one names it in a tooltip, and a screen reader reads the same name.

**Acceptance scenarios**

1. **Given** an empty service, **When** the page opens, **Then** five buttons are drawn in one horizontal
   row, each 52×52 (square within 1px) with a 10px gap, centred under the hint.
2. **Given** the same row, **When** a tile is inspected, **Then** it contains exactly one glyph and no
   visible text, and its accessible name and `title` are `Add Passage`, `Add Song`, `Add Text`,
   `Add Break`, `Add Media` in that order.
3. **Given** the same row, **When** the media tile is compared with the others, **Then** it shows a glyph
   too — the one action that never had one.
4. **Given** a reading column narrower than 300px, **When** the page opens, **Then** the tiles keep their
   52px size and take two rows of three and two; they never shrink below 44px.
5. **Given** any tile, **When** it is clicked, **Then** the same editor opens as before.

### US3 — The saved copy and the in-place rebuild draw the same row (P2)

**Why this priority**: the empty state is painted from three places (the server template, the saved
renderer and the rebuild that follows deleting the last entry). A row that only one of them knows about
comes back as a labelled column the moment the operator works offline or deletes the last item.

**Independent Test**: delete a service's last entry without reloading, and render the same service from
the saved library: both show the same five tiles, with the same labels and glyphs, as the server page.

**Acceptance scenarios**

1. **Given** a service with one entry, **When** the last entry is deleted in place, **Then** the rebuilt
   empty state is the centred block with the five icon tiles.
2. **Given** a Tata Ibadah page saved in the library, **When** it is rendered from the cache, **Then** its
   five tiles carry the same labels, one glyph each and the same square size as the server route.

### Edge Cases

- **When** the stage is narrow because both sidebars are open **Then** the row falls to three and two but
  stays centred and keeps its 52px tiles.
- **When** the page is printed or the stylesheet's container query does not apply **Then** the row stays
  a horizontal grid of five columns and simply shrinks; nothing overlaps.
- **When** a keyboard user tabs into the row **Then** each tile takes the existing focus ring, unchanged.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | An empty, editable service places its empty block so its centre sits a quarter of the way down the reading area between the header's bottom edge and the bottom of the window — within 12px of that mark, and never overlapping the header. | new: `reading` |
| FR-002 | The empty block's five add actions are one horizontal row of square tiles, 52×52 at a full-width column, 10px apart, centred. | new: `reading` |
| FR-003 | Each tile shows only a glyph; its accessible name and tooltip carry `Add Passage`, `Add Song`, `Add Text`, `Add Break`, `Add Media`, in that order. | new: `reading` |
| FR-004 | `Add Media` shows a glyph in the same 24-unit, 1.6-stroke family as the other four. | new: `reading` |
| FR-005 | In a reading column narrower than 300px the row takes two rows of three and two at 52px; no tile is ever narrower than 44px. | new: `reading` |
| FR-006 | The server template, the saved renderer and the post-delete rebuild paint the same tiles: same order, labels, one glyph each, same size. | `reading/R2` |
| FR-007 | A service that holds items keeps the header-to-body gap and the top-aligned flow it has today. | new: `reading` |

### Key Entities

None. The change is presentational; no model, view signature or stored value changes.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | The block reads as an upper-quarter invitation, not a floating centre | Block centre within 12px of the quarter mark of the reading area at 1440×900, 1280×800, 1024×700 and 390×844; top never above the header's bottom edge |
| SC-002 | The five add actions read as one row | Five tiles, one row above 300px of column, square within 1px |
| SC-003 | No tile drops below a comfortable target | Smallest tile measured at the four sizes ≥ 44px |
| SC-004 | No renderer disagrees | Saved copy and server page give identical label, glyph count and size per tile |

## UI/UX

- **Layout / position**: a flex column article filling the stage's content height (`min-height: 100%`); its
  body takes the remainder (`flex: 1`) and is a grid whose **first row is half of the body**, so the block it
  centres inside that row lands on the body's quarter mark — not its middle. The header's 30px bottom margin
  (22px below tablet width) and the body's 8px top margin are dropped **only** in this state, because both
  would bias the placement downwards; the body gains a 12px top pad as the floor for the case where the half
  row collapses to the block's own height. The block itself measures 142px at 1440×900: title 26px, 10px gap,
  hint 24px, 20px gap, tile row 52px.
- **Size / spacing**: tiles 52×52, `border-radius: 12px`, gap 10px, row width 300px; glyph 22px capped at
  60% of the tile so a shrinking tile shrinks its glyph. Row to hint gap 20px; title to hint 10px.
- **Colour / typography**: unchanged — `--canvas` fill, `--divider` border, `--head-ink` glyph, `--ink` on
  hover with `--focus` border, section-heading title at 20px/600, hint at the body size in `--head-ink`.
- **States**: hover lifts the glyph to `--ink`; focus-visible keeps the existing 2px `--focus` outline at
  3px offset; the row has no disabled or loading state; empty is the state being specified.
- **Motion**: none added; the tile's border/background transition is the existing `--ease` one.
- **Responsive**: above 300px of reading column the row is five tiles that shrink together; at or below
  300px it becomes three and two at full 52px. Measured at 1440×900: tiles 52px × 5 in one row, block centre
  26.2% of the reading area, top 132.8px clear of the header; 1280×800: 52px 3+2, 26.5%, 31.4px clear;
  1024×700: 52px 3+2, 29.9%, 12.0px clear (the half row collapses to the block); 390×844: 52px 3+2, 26.2%,
  80.7px clear.

## Assumptions

- *"First quarter of the height"* means the quarter mark of the reading area the header leaves, not of the
  whole window — the header is furniture at the top of the page, and the same assumption the centring version
  was accepted under. On a 1440×900 window that puts the block's top 253px down (28% of the window) and its
  centre at 36% of the window.
- The tile size is 52px, the same height as a service entry box in this pane, rather than a new number.
- Five tiles at 52px need 300px of reading column; below that, three and two at full size is better than
  five that are too small to hit — hence the container query rather than shrink-only.
- The media glyph is a frame with a play triangle: `Add Media` covers image, audio, video, PDF and slides,
  so the glyph names the family, not a type.
- The saved renderer and the delete-rebuild take the same markup, because a saved page is the same page.

## Clarifications

### Session 2026-10-25

- Q: Centre in the whole window, or in the area under the header? → *Assumed* under the header; the
  numbers in `UI/UX` measure that area, so the other reading is one rule away if the owner prefers it.
- Q: Does `Add Media` get a glyph, having never had one? → *Assumed* yes; an icon-only row cannot leave a
  blank tile.

### Revision 1 — 2026-10-25, after gate 2

The owner accepted the pack and then moved the placement: **from the middle of the reading area to its
quarter mark.** What changed, and only this:

| Artifact | Was | Now |
| --- | --- | --- |
| FR-001 | block centred, gaps above and below equal within 2px | block's centre a quarter of the way down the body, within 12px, never over the header |
| SC-001 | equal gaps at four sizes | centre within 12px of the quarter mark at four sizes; header never overlapped |
| US1 | "centred in the reading area" | "sits in the first quarter of the reading area" |
| `components.css` | body was a flex box centring the block | body is a grid whose first row is half the body (capped at the block's own height), with a 12px top pad |
| `tests/e2e/test_entries.py` | `…_centres_a_row_of_square_icon_buttons`, equal gaps ±2px | `…_places_its_tiles_a_quarter_of_the_way_down`, quarter mark ±12px and clear of the header |
| `docs/spec/reading.md` R6 | "centred vertically … equal space above and below" | "its centre a quarter of the way down that area" |

Unchanged: the five tiles, their size, order, names, the media glyph, the narrow-column 3+2 rule and every
renderer rule.

The requirement is **R6**, not R4: on rebasing onto `develop` the hymn-separator slice (128) had already taken
`reading/R4` and `R5`, so this one moved down the list and every reference moved with it.

The reason the half row is capped at the block's height: at 1024×700 the block is 278px tall
and half the body is 252px, so an uncapped row pushed the block 12.7px back over the header; measured after
the fix, that size clears the header by 12px.
