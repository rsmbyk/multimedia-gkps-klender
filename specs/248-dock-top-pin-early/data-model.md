# Data Model: earlier top pin for the live header

**Spec**: `specs/248-dock-top-pin-early/spec.md`

## Entities

### Live top pin (client-only)

| Field | Type | Constraints | From |
| --- | --- | --- | --- |
| `topBandSlot.hidden` | boolean | true until the live header's natural top crosses the scrollport edge | FR-001 |
| `topBandSrcRow` | DOM node | the header the clone was copied from; re-cloned only when it changes | FR-001 |
| `coveredRow` | DOM node | the real header currently hidden by the clone; cleared on crossing and on yield | FR-001 |
| `.is-covered` | class | `visibility: hidden` on the source row only; never on the clone | FR-001 |

**Relationships**: one live entry → one `.entryli` → one `.entryrow`; at most one clone in the
list-level `.topband-slot` and at most one covered source row at a time.
**Validation**: the source row carries `aria-current="true"`; the clone drops `aria-current` and
`aria-controls` and never becomes a second current row.
**State transitions**: `in flow → covered/pinned → in flow` — driven by `li.top` crossing the edge
in either direction, by a crossing of liveness, or by a list re-render. All transitions are
reconciled in the same `updatePins()` call.

## Invariants

- Exactly one painted header at the top edge: while the clone is shown the source is hidden; when
  the clone is hidden the source is visible (FR-001, FR-004).
- The pin is paint-only: it never changes list flow, scrollTop, the display state or following
  (FR-002, FR-003).
- The clone's top equals the source's sticky top on the takeover frame (0 px measured) — no hop.
- A go to's `.offstrip` has no service pin (FR-004).

## Not modelled

- No server-side entity, migration, endpoint, localStorage key or new client state store: the three
  fields above are local to `obs-dock.js` and live for the life of the rendered list.
- The bottom pin and the NEXT band keep their own slots and state; they are not merged with the top
  pin into a single abstraction.
