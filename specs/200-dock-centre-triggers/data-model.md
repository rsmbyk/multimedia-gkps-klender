# Data Model: the dock follows the live entry only when following

**Spec**: `specs/200-dock-centre-triggers/spec.md`

No database model, migration or API changes. The three entities below are page-memory state in
`static/web/obs-dock.js`; the display record (`gkps-display`) is read, never extended (D001).

## Entities

### Following mode

| Field | Type | Constraints | From |
| --- | --- | --- | --- |
| `following` | boolean | `true` on load; never persisted or broadcast | FR-011, FR-012 |

**State transitions**: `following → browsing` on a `wheel` over `runBody` or on `toggleBlock()`
opening a non-live entry (FR-012); `browsing → following` on the centre button, any item click
(including the sticky Next band), or a successful idle elapse (FR-002, FR-004, FR-007). An advance
in either state leaves the mode unchanged (FR-006).

### Previous display notice

| Field | Type | Constraints | From |
| --- | --- | --- | --- |
| `service` | number \| null | as read from `gkps-display` | D002 |
| `screen` | number | as read | D002 |
| `goto` | object \| null | as read | D002 |

**Relationships**: one snapshot per `sync()` call, replaced after the call. **Validation**: an
advance is `service` equal, `goto` equal and null, `screen` changed; the first notice after load has
no snapshot and is never an advance.

### Idle clock

| Field | Type | Constraints | From |
| --- | --- | --- | --- |
| `lastActivity` | timestamp | set on wheel, pointerdown, pointerup, pointercancel, keydown | FR-007 |
| `holding` | boolean | true between pointerdown and pointerup/cancel; refreshes `lastActivity` each tick | FR-007, US3/AC9 |
| `IDLE_MS` | number | 15000 | FR-007 |

**State transitions**: threshold crossing with every FR-007 condition true → centre, set
`following = true`, restart the count (FR-007). Page hidden → no fire; on show, restart (FR-009).

## Invariants

- Following never writes the display record and never changes what is on air (FR-002).
- No centring occurs on the first notice after load, or when `service`, `goto` changed or `screen`
  did not (D002, FR-011, FR-014).
- A crossing morph in browsing animates block heights only; `centerRow()` cannot be reached from
  that path (FR-006, D003).
- A wheel or pointerdown cancels a pending glide but does not itself centre (FR-010).
- The centre button is disabled iff there is no live row, including the go-to fallback (FR-003,
  D009).

## Not modelled

- The project's picker cursor (`dock.pickIndex`) — the owner's "pointer" is the live entry marker
  (`data-live` / `aria-current`), not the picker mark.
- The idle clock's remaining seconds — the real dock has no readout; the one in the preview is
  preview-only.
- Persistence of the mode — FR-011 requires a fresh following state on every load.
