# Data Model: The Transfers scrollbar sits at the dialog's edges

**Spec**: `specs/152-transfer-scrollbar-edge/spec.md` (revision 2)

Nothing is stored: the dialog is painted from the companion's `/v1/transfers` response on every poll
and holds no schema, migration or server state. The model below is the **view model** the stylesheet
has to keep true — the three boxes the slice moves relative to one another.

## Entities

### Dialog (`.media-library__dialog.media-transfers__dialog`)

| Field | Value | Constraint |
| --- | --- | --- |
| `width` | `min(580px, calc(100vw - 32px))` | unchanged |
| `padding` | `22px` | unchanged — the number the list's negative margins and padding are tied to |
| `border` | `1px solid var(--divider)` | unchanged — the edge the bar comes to rest against |
| `border-radius` | `12px` | unchanged — what the clip follows at the bottom-right corner |
| `max-height` | `min(86vh, 46rem)` | unchanged |
| `display` | `flex; flex-direction: column` while open | unchanged (spec 149) |
| `overflow` | `visible` | **`clip`** — clips the bar to the rounded corner (FR-007) |

### Transfer list (`#mediaTransfersList.media-transfers__list`)

| Field | Today | After | From |
| --- | --- | --- | --- |
| box, inline | content box of the dialog: `x 453 → 987` at 580px | the dialog's padding box: `x 431 → 1009` | FR-001 |
| box, bottom | `y 683.8` — 23px above the dialog's border | `y 705.8` — 1px above it | FR-001 |
| box, top | `y 117.2`, 14px under the title | unchanged | FR-004 |
| `margin` | `0` | `0 -22px -22px` | D001 |
| `padding` | `0` | `0 22px 22px` | D001, D006 |
| `overflow-y` | `auto` | `auto` | unchanged (spec 149) |
| scrollbar lane | the outermost 5px of the box — `x 982 → 986`, ending 23px above the bottom border | the outermost 5px of the box — `x 1004 → 1008`, ending 1px above it | FR-002 |

**Relationships**: the list is the dialog's only scroll container and the bar's box. Its content box
is what every row is laid out in.
**Validation**: the box's right and bottom edges are exactly the dialog's border width inside the
dialog's border box (FR-001); the lane, when the engine takes one, is the box's last `5px` (FR-002).
**State transitions**: none — the list is re-drawn by `renderTransfers()` on every poll; this slice
changes no drawing code.

### Row content (`.media-transfers__row`)

| Field | Value | Constraint |
| --- | --- | --- |
| content box, inline | `x 453 → 982` at 580px with the bar, `→ 987` without it | unchanged by this slice (FR-003) |
| padding | `13px 4px` | unchanged |
| pitch | 72px | unchanged |
| glyph column | 32px, at `x 457` | unchanged (spec 147) |
| separator | `border-bottom: 1px solid var(--divider)`, ending at the content box's right edge | unchanged (spec 149) |
| at the end of the scroll | 22.6px above the dialog's bottom border | unchanged, now carried by the list's `padding-bottom` (D006) |

## Invariants

- **The box reaches the border.** `dialog.border-box right − list.right == 1px` **and**
  `dialog.border-box bottom − list.bottom == 1px`, with `list.left − dialog.left == 1px`, at every
  viewport the dialog draws at. — FR-001, SC-002
- **The lane is outermost.** Where the engine paints a bar, the bar is the list box's last 5px, so the
  gap between the bar and the dialog's right border is 0px, and the lane ends at the bottom border. —
  FR-002, SC-001
- **The content does not move.** `row.left − dialog.left == 23px`; `dialog.right − row.right ==
  23px + the bar's width` (`28px` with the classic 5px bar, `23px` without it). — FR-003, SC-003
- **The top does not move.** `list.top − title.bottom == 14px`; the title and the first age heading
  sit 23px from the dialog's left. — FR-004, SC-004
- **The scroll's end does not move.** At the end of the scroll the last row's border sits 22px above
  the dialog's bottom border — the list's own `padding-bottom`. — FR-004, SC-004
- **A short list gains nothing.** No bar, no reserved lane; the rows keep today's 23px right inset. —
  FR-005
- **Nothing leaves the rounded box.** No pixel of the bar paints outside the 12px corner at any scroll
  position. — FR-007, SC-006

## Not modelled

- **The companion's transfer records** — ids, hashes, byte counts, timings. Unchanged; the contract
  is `none` (see `contracts/none.md`).
- **The Media Library page's own list** and the **service-media dialog** — different surfaces, out of
  scope (spec §Assumptions).
