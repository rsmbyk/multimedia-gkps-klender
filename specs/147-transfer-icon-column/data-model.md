# Data Model: a transfer row's icon column

**Spec**: `specs/147-transfer-icon-column/spec.md`

## Entities

### Transfer row (drawn, not stored)

| Field | Type | Constraints | From |
| --- | --- | --- | --- |
| `direction` | string | `upload` or `download`; chooses the glyph | FR-001 |
| `name` | string | one line, ellipsized at the text column's width | FR-002 |
| `status` | string | `active` → percentage, `completed`, `cancelled`, `failed` | FR-003 |

**Relationships**: one Transfers list 1—n rows; nothing else references a row.
**Validation**: none added — the fields arrive as the local companion wrote them and the dialog
renders them as they are.
**State transitions**: none in this slice. A row is redrawn by the page's poll when the companion
reports a new status; the row's geometry is the same in every status.

## Invariants

- The mark column is 32 CSS px wide in every row, whatever the row's content (FR-001).
- Every row's name and status label share one left edge, 12px right of the mark column (FR-003).
- A name wider than the text column is ellipsized; the row's height and width do not change (FR-002,
  FR-005).

## Not modelled

- **The dialog's opening animation.** `[open]` scales the dialog 0.97 → 1 over 190ms; it scales the
  whole row, so it cannot change a spread. The preview disables it so its readout is measured at
  scale 1 (`preview/README.md`).
- **The rail's own transfer list.** Same rows, same classes, same geometry — it is one renderer
  (`media-handoff.js` `renderTransfers`), so a second model would be a second place to disagree.
- **The local companion's API.** No field is added, removed or re-shaped; this slice reads what
  already arrives.
