# Data Model: the Media Library list holds still while it refreshes

**Spec**: `specs/148-media-library-refresh-flicker/spec.md`

No stored entity, table, column or API payload changes. The model below is the **in-memory state the
page draws from** — the thing this slice re-orders — so the invariants that make the jolt impossible
are written down where Converge can check them.

## Entities

### Library state

The four values `refresh()` reads and `render()` consumes, held in the module closure today.

| Field | Type | Constraints | From |
| --- | --- | --- | --- |
| `files` | `Array<FileRow>` | replaced only by a complete read; never emptied to signal loading | FR-001, FR-003 |
| `uses` | `Object<sha256, Array<Reference>> \| null` | `null` means "not known", and only a failed read may set it | FR-001, FR-003 |
| `protected` | `Set<sha256>` | replaced with `uses`, never apart from it | FR-005 |
| `status` | `Object \| null` | applied with the state it arrived with (`setStatus`) | FR-005 |

**Relationships**: one library state → n `FileRow`; one `FileRow` → 0..n `Reference`.
**Validation**: a state is *applicable* only when `files` and `uses` come from the same refresh — except
that a `uses = null` state is applicable when and only when its references read failed.
**State transitions**: `unknown → complete` (first successful refresh) · `complete → complete`
(any later refresh) · `complete → degraded` (references read failed; `uses = null`) ·
`degraded → complete` (a later refresh succeeds).

### File row

Drawn from one entry of `files`; not modelled as data, modelled as what decides its geometry.

| Field | Type | Constraints | From |
| --- | --- | --- | --- |
| `name`, `family`, `uploaded_at`, `size` | companion fields | rendered unchanged | FR-005 |
| `references` | 0..n entries of `uses[sha256]` | draws `.media-library__uses` (18px per line, `margin-top: 8px`, `gap: 4px`) when non-empty | FR-001, FR-002 |
| `unused label` | string | draws `.media-library__unused` (one 18px line, `margin-top: 4px`) when `uses` is known and the list is empty | FR-005 |
| `placeholder` | the literal `Service uses unavailable` | draws only when `uses === null` | FR-001, FR-003 |
| cloud state | available / uploading / share | draws in the 66px column; does not affect height | FR-005 |

**Measured heights** (1920×1100, the owner's library): 97px with no `used by` block, 101px with one
18px reference line, 119px with a two-line 36px block, 123px with a 40px block. The row's height is a
function of its `used by` block and of nothing else — which is why an intermediate state with `uses =
null` cannot keep the list still.

## Invariants

- **One draw per applied state.** Every change to `files`, `uses`, `protected` or `status` is followed by
  exactly one `render()` (FR-001, SC-003).
- **No partial state is ever drawn.** `files` and `uses` move together; a poll landing mid-refresh
  redraws the previous complete state (FR-001, D002 in `research.md`).
- **Degraded is a state, not a pass.** `uses = null` is drawn once, and only when its read failed
  (FR-003).
- **A row's top is stable across a refresh.** For every row, `top` before the refresh equals `top` after
  it, in every frame (FR-002, SC-001).
- **The list's height never grows after it first appears** (SC-004).

## Not modelled

- **The 2s poll's own rebuild.** It replaces the list's children with identical content; measured inert
  (no row's top changes) and kept by FR-004. Modelling it would mean modelling a renderer this slice
  does not change.
- **The references view and the companion's endpoints.** Untouched; their payloads are already the
  shape `uses` and `files` take.
- **`delete_at` / retention copy.** Drawn from the state, not re-shaped here.
