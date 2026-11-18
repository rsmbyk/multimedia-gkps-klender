# Data model — spec 198 (the 2026-11-18 revision)

No model changes. No migration. Nothing reaches the database, the channel, or `gkps-display`.

## Entities

### ServiceEntry, TataIbadah, screens — unchanged

| Field | Type | Constraints | From |
| --- | --- | --- | --- |
| `entry.start` / `entry.end` | int | computed server-side today; the range `buildInner` reads | — (untouched) |

No column, no property, no serializer changes. The slice is browser-side only.

### `.entryinner` DOM shape — one attribute added

| Attribute | Type | Constraints | From |
| --- | --- | --- | --- |
| `id` | string | `entryinner-<index>` — set in `buildInner` so the header's `aria-controls` has a referent | FR-008 |

Class churn: none. `.is-open` / `.is-morph` keep their names and their meanings
(open = effective state; morph = a hand animation owns the height).

### `gkps-display` (localStorage) — unchanged

`service, screen, on, translation, at, session, goto`. No field is added; the toggle never writes.
The inter-surface channel (`OBS-*` postMessage) is never sent by the toggle path. Verified by the
toggle tests asserting the stored shape is byte-identical after a header click.

## Invariants

- **Effective open state** — `live ? open : (override ?? closed)`; the single input to the inner's
  `is-open`, `aria-hidden`, `inert`, the header's `aria-expanded`, and the chevron's presence.
  (FR-006, Key Entities.)
- **`entryOverrides`** (new, page memory only) — `Map<index, boolean>` inside `obs-dock.js`.
  - Absent index ⇒ no override ⇒ closed (a non-live row's default).
  - `true` ⇒ operator opened it; `false` ⇒ operator closed it.
  - Inert while the entry is live (effective state is `open` regardless); re-applies the moment it
    departs.
  - Never serialized, never persisted, never broadcast; dies with the page (A2/A10).
- **Headers write nothing** — a header click issues no `gkps-display` write and no `OBS-*`
  message (FR-002/FR-004). The only writes in the slice's path are the pre-existing
  `projectScreen()` calls from screen rows, the Next band, bait chips and the transport.

## State transitions

```
block:  closed --header click--> open (override := true)
        open   --header click--> closed (override := false)
        any    --entry goes live--> open (override kept, inert)
        live   --header click--> no transition (locked, FR-002)
        any    --page reload--> closed unless live (overrides gone, A2)
        any    --toggle during crossing morph--> recorded; lands at settle (FR-009)
```

## Not modelled

- **Persistence of overrides** — deliberately page-memory; a reload repaints with the live-block
  rule (US3 scenario 6, A2).
- **A "selected screen" per open block** — opening a block selects nothing (FR-007); `aria-current`
  on screen rows keeps its existing, projection-driven meaning.
- **The chevron's rotation** — not state, a paint of the effective state; no attribute beyond
  `aria-expanded` carries it.
