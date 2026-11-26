# Feature Specification: Picker popout scrollbars sit at the menu edge

**Slice**: `specs/244-picker-menu-scrollbar-edge`
**Branch**: `fix/244-picker-menu-scrollbar-edge`
**Created**: 2026-11-26
**Status**: Accepted (owner, gate 1 2026-11-26)
**Input**: "the scrollbars inside a dropdown popouts do not touch the edge"

## User Scenarios & Testing

### US1 — The scrollbar is the popout's edge (P1)

**Why this priority**: this is the report. The entry modal's picker menus paint their 5px scrollbar
inside the menu's 8px padding, so the bar reads as floating in the panel rather than belonging to it.
**Independent Test**: open the Book search menu or a Chapter/From verse/To verse popover with more
options than the menu height and look at its bottom-right corner: no canvas between the bar and the
menu's border on either side.

**Acceptance scenarios**

1. **Given** the New passage dialog's Book search menu open on a 1440×900 viewport, **When** its
   scrollport is measured, **Then** its right and bottom edges are each 1px (the menu's own border)
   inside the menu's border box — 9px today.
2. **Given** a Chapter or verse button popover open, **When** its scrollport is measured, **Then**
   the same 1px edge holds for both the 436px-wide chapter menu and the 213px-wide verse menu.
3. **Given** the options list scrolled to its end, **When** the bar's bottom is measured, **Then**
   its lane ends at the menu's inner bottom edge and its last pixels are clipped to the 10px corner
   radius — none paint outside the menu's border.
4. **Given** the light or dark theme, a menu flipped above its trigger, or a menu narrowed by its
   trigger's width, **When** it overflows, **Then** the bar keeps the same edge relationship.

### US2 — Nothing but the bar's lane moves (P2)

**Why this priority**: the report names the bar's position only. Moving the options, their headings,
the in-menu filter or the scroll behaviour would turn a drawing fix into a redesign of the picker.
**Independent Test**: measure the first option's box and the filter input's box before and after on
the same page and compare them pixel for pixel.

**Acceptance scenarios**

1. **Given** the Book menu open, **When** the first option's box is measured, **Then** it is
   unchanged: x 511→929, y 464.1→503.1 at 1440×900.
2. **Given** the Chapter popover open, **When** the filter input is measured, **Then** it is
   unchanged: x 511→929, y 510.1→548.1, 38px high.
3. **Given** a menu whose options fit, **When** it is opened, **Then** no bar is drawn, no lane is
   reserved, and the options keep their original inset.
4. **Given** any picker, **When** typing, arrowing, Enter/Tab commit or scroll-follow is used,
   **Then** the behaviour and the visible option set are unchanged.

### Edge Cases

- **When** a menu flips above its trigger near the viewport bottom **Then** the bar still sits at
  the right and bottom edges of the flipped box.
- **When** the verse menu's 213px width is in use **Then** the scrollport still reaches the border
  without covering the filter.
- **When** the theme changes **Then** the bar keeps spec 087's 5px, `--scroll-thumb` drawing with no
  stepper buttons and a transparent track.
- **When** the dialog closes **Then** nothing of the menu or its bar is painted.
- **When** the option list holds one row **Then** no bar is painted and no scroll lane is reserved.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | An overflowing `.editor__picker-menu` scrollport SHALL end 1px (the menu's border) inside the menu's border box on the right and on the bottom, with no menu padding between it and the border. | `reading/R59` |
| FR-002 | The scrollbar painted by that scrollport SHALL occupy its outer 5px, so the bar's right edge is 0px of menu canvas from the border, and its lane ends at the inner bottom edge. | `reading/R59` |
| FR-003 | The option rows, group headings and in-menu filter SHALL keep their pre-slice boxes: the scrollport's own padding compensates for the negative margin on its right and bottom. | `reading/R59` |
| FR-004 | The menu SHALL clip its contents to its 10px rounded border, so the bar's final pixels follow the corner rather than painting over it; the clipping SHALL NOT make the menu itself a scroll container. | `reading/R59` |
| FR-005 | Filtering, highlight, Enter/Tab commit, Escape and scroll-follow SHALL keep their accepted behaviour; this slice changes CSS only. | `reading/R59` |
| FR-006 | A non-overflowing option list SHALL draw no bar and reserve no lane, and its content SHALL keep the pre-slice inset. | `reading/R59` |
| FR-007 | The bar SHALL keep spec 087's drawing: 5px, `--scroll-thumb` (hover `--scroll-thumb-hover`), rounded, no stepper buttons, transparent track. | `reading/R59` |

### Key Entities

- **Picker menu** — `.editor__picker-menu`, a fixed-position popout anchored to the Book search
  field or a Chapter/verse trigger; it carries 8px padding, a 1px border and a 10px radius.
- **Scrollport** — `.editor__picker-options`, the menu's inner `overflow: auto` box; the engine
  paints its scrollbar against this box, which is why the padding used to inset the bar.
- **Option content** — rows, group labels and the in-menu filter inside the scrollport; their boxes
  are the invariant every measurement checks.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | 0px of menu canvas between the scrollbar's right edge and the menu's border | `menu.right - options.right == 1` (the border's own width), measured on Book, Chapter and verse menus at 1440×900 |
| SC-002 | 0px change in option and filter content boxes | first option `511,464.1 → 929,503.1`; chapter filter `511,510.1 → 929,548.1`, before and after |
| SC-003 | 0px of scroll lane below the last option when the list does not overflow | `scrollHeight <= clientHeight` and no bar painted |
| SC-004 | Accepted interaction behaviour stays green | the spec 238 passage-picker and song-picker browser modules at the push step |

## UI/UX

Live preview at `http://127.0.0.1:8778/` (dev server started from this worktree on port 8778; open
`/` then click the Tata Ibadah rail tile, the first service, hover the start bar and choose
`+ Passage`). Measured at 1440×900, dpr 1, light theme, before (base) → after (slice CSS in the same
live code path):

- **Layout / position**: Book menu border box x 502→938, y 429.9→892. Its scrollport's right/bottom
  go 929/883 → 937/891, i.e. a 9px inset → the 1px border. Chapter menu (436px wide, x 502→938,
  y 501.1→892) and verse menu (213px wide, x 502→715, y 572.4→892) move the same 8px right and
  down. Menu position, width and viewport cap (set by `placeMenu()`) do not change.
- **Size / spacing**: the first book option stays x 511→929, y 464.1→503.1; the chapter filter stays
  x 511→929, y 510.1→548.1 (38px high); the scrollport grows from 418×444.1 to 434×452.1 (Book)
  while its content padding grows from `0` to `0 8px 8px`.
- **Colour / typography**: none changed. The 5px `--scroll-thumb` bar, its hover tone, transparent
  track and the menu's `var(--canvas)` / `var(--divider)` remain spec 087's.
- **States**: open Book menu (66 books, overflowing), Chapter menu (50 options, overflowing), From
  verse menu (31 options, overflowing), filtered chapter menu, a one-option chapter menu (Obaja,
  `scrollHeight == clientHeight == 42`) with no bar and 0px gutter, dark theme, narrow trigger,
  flipped menu. Reachable by clicking through the live dialog; no invented state appears in the
  preview.
- **Motion**: none; the menu opens in one frame before and after.
- **Responsive**: the two measured widths (436px chapter, 213px verse) cover the wide and narrow
  menus; their fixed positioning and viewport cap are untouched, and `overflow: clip` follows the
  menu's own radius at either width.

## Assumptions

- "Dropdown popouts" means the entry-modal picker menus (`.editor__picker-menu`), the only dropdown
  popouts whose scrollbar is inset from its own border. Other surfaces — the OBS dock's find menu,
  the media chooser and the date popover — are out of scope.
- "Touch the edge" means the menu's border box, not the surrounding dialog; the 1px border remains
  visible between bar and outside world. Both the right and bottom lanes extend, matching the
  accepted Transfers-dialog fix (spec 152).
- The CSS edit was made in this worktree first and is served by the live dev server; it is left
  uncommitted until Fold. The before numbers came from the unmodified base at the same path.
- This is a modification of accepted `reading/R59`, not a new capability requirement; the pack
  carries a regression note at Fold rather than claiming a new `R<n>`.
- No owner-visible text, data, focus order or network behaviour changes, so the change is CSS-only.
- `bump: patch` (declared at Plan, applied before merge), following the other user-visible fixes.

## Clarifications

### Session 2026-11-26

- Q: Which dropdown popouts are in scope? → A: the entry-modal Book search and Chapter/verse menus.
- Q: Where should the fix land? → A: a new slice worktree cut from develop (branch
  `fix/244-picker-menu-scrollbar-edge`); do not mix it into the in-flight navigation slice.
