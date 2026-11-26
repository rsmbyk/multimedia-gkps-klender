# Data Model: pending state for Search and Media Library rail tiles

**Spec**: `specs/245-rail-fetch-feedback/spec.md`

## Entities

All three are client-side state in `static/web/reading.js`; none is persisted.

### RailTile

| Field | Type | Constraints | From |
| --- | --- | --- | --- |
| `id` | string | `railSearch` or `railMediaLibrary`; identity is the anchor id | FR-001, FR-008 |
| `destination` | URL string | `/` or a saved `/search/?q=…` for Search; `/media-library/` for the library | FR-008 |
| `locked` | boolean | true from activation until settlement; mirrors `aria-disabled` | FR-002 |
| `appearance` | computed style | SVG opacity `0.45`; no spinner/label/edge/ring | FR-002 |

**Relationships**: one RailTile starts at most one PendingFetch at a time.
**Validation**: a tile with `aria-disabled="true"` cannot start another fetch (`navigate()` guard).
**State transitions**: `idle → locked → idle`, on fetch start and settlement/cancel/fallback.

### PendingFetch

| Field | Type | Constraints | From |
| --- | --- | --- | --- |
| `kind` | enum | `results` (Search) or `media-library`; both are stage writes | FR-001 |
| `sections` | list | `['stage']` for both kinds | FR-003 |
| `controller` | AbortController | cancels the in-flight request on supersede | FR-007 |
| `record` | object | existing `activeFetches` entry: source, writes, bars, done, cancelled | FR-006, FR-007 |

**Relationships**: a PendingFetch owns one Placeholder and one stage bar while live.
**Validation**: a later stage-writing click cancels it; a later list-only click does not.
**State transitions**: `pending → settled | cancelled | full-page fallback`.

### Placeholder

| Field | Type | Constraints | From |
| --- | --- | --- | --- |
| `kind` | enum | `results`, `search-home`, `media-library` | FR-004 |
| `seed` | object | query for Search results, `null` for home, `Media Library` name for the library | FR-004 |
| `origin` | box | stage box +64px horizontal, +40px vertical at 1440px | FR-004, SC-002 |
| `anatomy` | DOM fragment | destination's own classes with `.pv-ph-bar` bars for unknown content | FR-004 |

**Relationships**: appended to `.stage`, removed by `clearStageFor()`.
**Validation**: visible only while `stage[aria-busy="true"]`.
**State transitions**: `absent → shown → replaced by the real page`.

## Invariants

- Only the clicked tile and the stage are locked; the rail and both sidebars stay interactive (FR-005).
- Every pending state clears on success, failure, supersede and settlement; on full-page fallback it
  stays until unload (FR-006).
- No placeholder or bar appears for a fetch that does not write to the stage (inherited from R61).

## Not modelled

- No database tables, migrations, serialisers or API contracts: the slice changes only client state
  and reads pages the existing views already render (FR-010).
- No stored history of fetches or locks; `activeFetches` is in-memory for the life of the page.
