# Data Model: picker popout scrollbar edge

**Spec**: `specs/244-picker-menu-scrollbar-edge/spec.md`

## Entities

### Picker menu (`.editor__picker-menu`)

| Field | Type | Constraints | From |
| --- | --- | --- | --- |
| `position` | CSS | `fixed`, anchored by `placeMenu()` | FR-001 |
| `padding` | CSS length | `8px`, unchanged | FR-003 |
| `border` | CSS length | `1px` `var(--divider)`, unchanged | FR-001 |
| `border-radius` | CSS length | `10px`, unchanged | FR-004 |
| `overflow` | CSS keyword | `clip` (new) | FR-004 |

### Scrollport (`.editor__picker-options`)

| Field | Type | Constraints | From |
| --- | --- | --- | --- |
| `overflow` | CSS | `auto`, unchanged | FR-005 |
| `margin` | CSS shorthand | `0 -8px -8px` (new) | FR-001 |
| `padding` | CSS shorthand | `0 8px 8px` (new), compensates the margin | FR-003 |
| `min-height` | CSS length | `0`, unchanged | FR-005 |

### Option content

Rows, group headings and the in-menu filter. Their rendered boxes are the invariant: first book
option x 511→929, y 464.1→503.1; chapter filter x 511→929, y 510.1→548.1 at 1440×900. (FR-003)

**Relationships**: menu 1—1 scrollport 1—n option rows. No server model, migration or API row.
**Validation**: every box claim is read from `getBoundingClientRect()` on the live page.
**State transitions**: hidden → open (trigger click) → hidden (choice/Escape); the slice changes none.

## Invariants

- The scrollport's right and bottom edges stay 1px inside the menu's border box whenever the menu
  is open, whether the list overflows or not (FR-001, FR-006).
- Option and filter content boxes stay where they were before the slice (FR-003).
- The menu never becomes a scroll container; only the options list does (FR-004, FR-005).

## Not modelled

- The scrollbar itself: it has no DOM node, so the model constrains the scrollport's box and the
  engine paints the bar against it.
- A separate short-menu state: a list that fits still has the same scrollport box; it simply draws
  no bar (FR-006).
