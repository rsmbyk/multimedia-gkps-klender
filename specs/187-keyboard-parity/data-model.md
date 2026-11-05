# Data Model: one keyboard grammar for the dock and the projector

**Spec**: `specs/187-keyboard-parity/spec.md`

## Entities

### Display state — `gkps-display`

| Field | Type | Constraints | From |
| --- | --- | --- | --- |
| `service` | `int \| null` | `null` means nothing of a service is on air; **may now stand beside a non-null `goto`** | FR-003 |
| `screen` | `int` | the service's own place; untouched while a go to is on air | FR-003, FR-005 |
| `on` | `bool` | words on/off for whatever is on air | FR-003 |
| `translation` | `'TB' \| 'SIM' \| null` | the service's own edition; a go to's edition lives in the go to | FR-005 |
| `at` | `int` | ms, renewed on every write | (spec 119) |
| `session` | `string \| null` | the browser session that wrote it | (spec 184) |
| `goto` | `Goto \| null` | see below | FR-003, FR-004 |

**State transitions**: `idle (service: null, goto: null)` → `service on air` → `go to over a service`
→ `back` → `service on air`; `idle` → `go to alone` (`service: null`, `goto`) → `back` → `idle`.
`show()` ends any go to; `release()` clears everything.

### Goto

| Field | Type | Constraints | From |
| --- | --- | --- | --- |
| `kind` | `'song' \| 'passage'` | discriminator | FR-003 |
| `song_id` | `int` | present iff `kind === 'song'` | FR-003 |
| `index` | `int` | present iff `kind === 'song'`; 0-based screen index in the payload | FR-003 |
| `book_id` | `int` | present iff `kind === 'passage'` | FR-003 |
| `chapter` | `int` | present iff `kind === 'passage'` | FR-003 |
| `verse` | `int` | present iff `kind === 'passage'`; ≥ 1 | FR-003 |
| `translation` | `'TB' \| 'SIM'` | the edition on air for this passage | FR-005 |

**Relationships**: a goto is *over* a service (`service` may be `null`) and *beside* the service's own
`screen`/`translation`, which it never writes.

**Validation**: a stored `goto` that cannot be parsed reads as `null`; a passage with a book or
chapter the index does not hold is dropped at `goTo()`.

**State transitions**: `created (goTo)` → `moved (stepGoto)` → `flipped (flip)` → `ended (back,
show, release)`. A chapter or book step is a `moved` transition that replaces `book_id`/`chapter`
first and then `verse`.

### The dock's shortcut table

| Field | Type | Constraints | From |
| --- | --- | --- | --- |
| `group` | `string` | one of `Pick a service`, `Service`, `Song`, `Passage`, `Display`, `Find` | FR-008 |
| `label` | `string` | the projector's own string, verbatim, except the three dock-only rows | FR-008 |
| `chords` | `string[]` | one chord per alternative; `or` separates them | FR-008 |
| `data-keys` | `'pick' \| null` | only the picker group carries it; it is `hidden` unless the view is the picker | FR-008 |
| `view` | `'pick' \| 'run'` | the sheet's visibility rule reads the dock's `data-view` | FR-008 |

**Invariants**: 32 rows in 5 groups on the runner; 34 in 6 on the picker; one direction per row; no
row mixes a direction with its opposite; every shared label is the projector's own.

### The band's query state (dock-local, not stored)

| Field | Type | Constraints | From |
| --- | --- | --- | --- |
| `open` | `bool` | the band is a layer; while open it owns the keyboard | FR-002, FR-015 |
| `query` | `string` | the field's text | FR-002 |
| `rows` | `Match[]` | answered by `GKPSProjectorLibrary.lookup` over the captured index | FR-002 |
| `choice` | `int` | the highlighted result | FR-002 |
| `loading` / `failed` | `bool` | the index or a payload in flight, or a fetch that failed | FR-009 |
| `busy` | `bool` | the go to's own fetch or a chapter/book step; gates every key and pointer act | FR-009 |

## Invariants

- One write is one state object and one channel message; a reader re-reads rather than trusting the
  payload (spec 185's contract).
- While a go to is on air the service's `screen` and `translation` never change (FR-003, FR-005).
- `back()` from a service-less go to leaves `{service: null, on: false, goto: null}` — idle, not a
  service at screen 0 (FR-003).
- The sheet's picker group is drawn only while `data-view="pick"`; its rows are never shown on the
  runner (FR-008).
- The projector's sheet carries one `Display` group and one `Find` group, in that order, and its
  media groups sit in the left column after `Passage` (FR-013, FR-014).

## Not modelled

- **Focus** — a rule over the DOM (FR-015), not an entity: nothing is stored, and the field's caret is
  the browser's.
- **The sheet's pixels** — widths, heights and the scroll live in `## UI/UX` and the preview, measured
  there; the model carries the rows and their order only.
- **The projector's channels and media hosts** — untouched by this slice beyond the sheet's grouping
  and the service-less paint (FR-011).
