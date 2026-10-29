# Data Model: The Transfers list draws each boundary once

**Spec**: `specs/149-transfer-separator-seam/spec.md`

Nothing is stored: the dialog is painted from the companion's `/v1/transfers` response on every poll
and holds no schema, migration or server state. The model below is the **view model** the stylesheet
has to keep true — the two things the list renders and the distances between them.

## Entities

### Transfer row (`.media-transfers__row`)

| Field | Type | Constraints | From |
| --- | --- | --- | --- |
| `name` | text | one line, ellipsized at the row's width | `media-handoff.js:61` |
| `status` | text | `Completed` · `n%` while active · `Cancelled` · `Failed` | `media-handoff.js:62` |
| `direction` | glyph | upload / download / both, from the job's `direction` | `media-handoff.js:59` |
| `border` | 1px `--divider` | bottom only; removed on the row immediately above the seam | FR-003, FR-001 |
| `pitch` | 72px | 13px padding + content + 13px padding + 1px border | SC-004 |

**Relationships**: a row 1—n boundaries — its own bottom border, plus the seam divider when it is the
last row of the newer group.
**Validation**: the border is `1px` unless the row's next sibling is `.media-transfers__divider`
(FR-001), and a row never paints outside the dialog (FR-005).
**State transitions**: none — a row is redrawn from the next poll; nothing in this slice changes what
a row contains.

### Session seam (`.media-transfers__divider`)

| Field | Type | Constraints | From |
| --- | --- | --- | --- |
| `element` | `<hr>` | inserted before the first transfer that ended before this session started | `media-handoff.js:55` |
| `line` | 2px `--divider` | `border-top` only; `border: 0` clears the UA box | FR-001 |
| `space` | 9px above, 9px below | `margin: 9px 0`; no second line within 20px | FR-002 |

**Relationships**: the seam 1—1 the row above it — that row drops its bottom border so the seam is the
only line.
**Validation**: exactly one painted boundary within 20px of the seam (SC-001).
**State transitions**: present only in a rail-opened dialog with no active transfer and at least one
unseen completed transfer; absent otherwise (US1/AC4). This slice does not change that rule.

## Invariants

- **One line per boundary.** No two painted horizontal lines sit closer than 20px anywhere in the
  dialog; the seam's own two would be 10.5px apart. — FR-001, SC-001
- **Nothing leaves the dialog.** The list's painted box is within the dialog's inner bottom edge at
  every scroll position. — FR-004, FR-005, SC-003
- **The dialog's padding survives.** The list ends 22px above the dialog's bottom border, so no
  boundary can sit closer than 22px to it. — FR-005, SC-002
- **Rows are unchanged.** 72px pitch, 13px padding, 1px `--divider` border, unchanged text. — FR-003,
  SC-004

## Not modelled

- **The companion's transfer records** — ids, hashes, byte counts, timings. The dialog reads them but
  this slice changes none of them; the contract is `none` (see `contracts/none.md`).
- **The session** (`started` / `seen` / `viewed`) — client state in `media-handoff.js` that decides
  *whether* the seam exists. Recorded as out of scope (D006); the model only states that a seam, when
  present, is one line.
