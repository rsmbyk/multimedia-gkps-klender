# Data Model: opening a service starts its entry blocks shut

**Spec**: `specs/204-dock-entry-open-reset/spec.md`

No Django model, serializer, endpoint or storage key changes. The only state this slice touches is
the dock page's own memory.

## Entities

### Entry block override (existing, its lifetime modified)

| Field | Type | Constraints | From |
| --- | --- | --- | --- |
| key | entry index (integer, 0-based) | unique within the open service; a section break or an empty block never records one | FR-001, spec 198 FR-006 |
| value | boolean | `true` open, `false` closed; absent = unset = the base rule (shut) | FR-001 |
| lifetime | page memory | ends at an explicit open of a service (new) and at a reload (existing); never persisted | FR-001, FR-003, FR-006 |

**Relationships**: one map per dock page, scoped to the service currently open — the scope is
enforced by emptying the map on an open, not by a second key.
**Validation**: `toggleBlock()` (`obs-dock.js:856`) refuses the live entry and any entry with no
inner, so no override is ever recorded for a block that cannot act.
**State transitions**: `unset → open|closed` on a header click; `open|closed → unset` on an
explicit open of a service (FR-001) or a reload; inert while the entry is live (spec 198 FR-006).

### Effective open state (existing, unchanged)

| Field | Type | Constraints | From |
| --- | --- | --- | --- |
| live | boolean | `gkps-display.service === dock.service` and the screen falls in the entry's range | FR-002 |
| open | boolean | `live ? true : (override ?? false)` — the single input to every painter | FR-002, spec 198 FR-006 |

**Relationships**: read by `sync()`'s per-`li` repaint, the crossing's settle paint and the hand
toggle's finish paint — one question, three painters, no second source.
**State transitions**: recomputed at every paint; never stored.

### Explicit open (existing path, named here as the reset's trigger)

| Field | Type | Constraints | From |
| --- | --- | --- | --- |
| service id | integer | the picker row's `data-service`, or the display state's service on load | FR-003 |
| path | one of three | picker click (`:1435`), picker `Enter` (`:392`), on-load resume (`:2032`) | FR-003 |

**Not an open**: `refreshService()` (`:472`), the `update` channel message, the 10 s timer
(`:2013`) — all call `loadServiceData()` directly and keep every override.

## Invariants

- After an explicit open, no non-live entry block in the drawn list is open (FR-001, SC-001…003).
- The live entry's block is open whenever its service is the one drawn and on air, regardless of
  the map's contents (FR-002, SC-004).
- An open writes nothing: the stored display state is byte-identical and no channel message is
  sent (FR-005, SC-006).
- A crossing or a re-read never empties the map (FR-003, FR-004, SC-005).
- Nothing about an override reaches `localStorage`, `sessionStorage`, a cookie or the server
  (FR-006).

## Not modelled

- The go to's block (`offBlock`): drawn from the display state, not from an entry index, so no
  override applies to it (spec A5).
- The crossing and toggle morph state (`morphState`, `toggleMorphs`): keyed by element, discarded
  with the list, untouched by this slice (research D004/D008).
- The per-service data cache (`cache`, keyed by service id): already correctly scoped.
