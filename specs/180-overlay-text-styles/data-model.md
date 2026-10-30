# Data Model: the overlay reads by kind

**Spec**: `specs/180-overlay-text-styles/spec.md`

The overlay stores nothing: every object below already exists on the page or in the projector response. This file
records what the paint path reads, what it derives, and the invariants a reviewer can check against the code.

## Entities

### Screen — one step of the projector's own response

| Field | Type | Constraints | From |
| --- | --- | --- | --- |
| `blank` | bool | true for the built-in rest and section breaks | FR-008 |
| `header` | string | `""`, or one line (reference / title), or two lines separated by `\n` | FR-003, FR-004 |
| `lines[]` | array | each `{text, voice, mark, words}` | FR-004, FR-010 |
| `entry_index` | int | index into `projectorEntryData`; absent on an older payload | FR-001 |
| `translations` | map | `{edition: {header, line}}`, only when the entry carries a second edition | FR-007 |
| `bait`, `split`, `split_total` | string · int · int | song markers; not painted by the plate | — |

**Relationships**: Entry 1—n Screen — a screen belongs to exactly one entry.
**Validation**: a screen is paintable only when it is not blank *and* its entry is known; otherwise the caption is the
fallback, which is the surface's behaviour before this slice.
**State transitions**: none — a screen is derived per request and never stored.

### Entry — what the service holds at that position

| Field | Type | Constraints | From |
| --- | --- | --- | --- |
| `type` | enum | `song` · `passage` · `text` · `media` · `break` | FR-001 |
| `label` | string | operator-facing citation, never painted on the plate | FR-002 |
| `start`, `end` | int | half-open range of screen indices | FR-001 |

**Relationships**: Entry 1—n Screen.
**Validation**: an unknown or missing entry keeps the caption (the pre-slice behaviour).
**State transitions**: none.

### Display state — what is on air, browser-local

| Field | Type | Constraints | From |
| --- | --- | --- | --- |
| `service` | int | the active service id | FR-008 |
| `screen` | int | index into the service's screens | FR-001 |
| `on` | bool | false after hide, true after show | FR-008 |
| `translation` | string | `""` or an edition abbreviation | FR-007 |

**Relationships**: Display state 1—1 Screen (by index) at any moment.
**Validation**: read from `localStorage['gkps-display']`, pushed over `BroadcastChannel('gkps-service-display')`; the
overlay is listen-only and never writes it (FR-009).
**State transitions**: `hidden → showing → hidden` on the dock's verbs; `release` clears the service and paints nothing.

### Plate — the derived painting object

| Field | Type | Constraints | From |
| --- | --- | --- | --- |
| `kind` | `passage` · `liturgy` | from `entry.type` | FR-001, FR-004a |
| `kicker` | string | first line of `header`; empty when the header is empty | FR-003 |
| `title` | string | the remaining header lines; empty when there are none | FR-003 |
| `rule` | element | present only when kicker or title exists | FR-003 |
| `lines[]` | array | `is-leader` · `is-assembly` · `is-join`; `has-mark` when `mark` is set | FR-004, FR-010 |
| `width`, `height` | px | between `min-width: 34%` and `max-width: 90%` of the stage | FR-006, FR-013 |

**Relationships**: Plate 1—1 Screen when the screen's entry is `passage` or `text`; absent otherwise.
**Validation**: a plate exists only for a passage or a liturgy screen carrying words; a caption exists only for a
song screen; media, break, blank, hidden and released screens paint nothing.
**State transitions**: `entering → settled → (morphing → settled)* → leaving → removed`; `entering` and `leaving` are
the two motion classes, `morphing` (`is-resizing`) runs only between two panels of one entry.

## Invariants

- A screen paints exactly one object — a caption, a plate, or nothing (FR-001, FR-008).
- The plate's words are the screen's own lines; the heading is the screen header's own lines, in order (FR-003, SC-003).
- Every screen shows the same number of words the projector shows: `mark + words` reassembles `text` (FR-010).
- The surface carries no control and no focusable element (FR-009).
- Nothing survives a rest: every entry closes with a blank, and a blank clears the stage (FR-008).

## Not modelled

- **The panel's own geometry as data** — width, height, radius and paddings are CSS, measured in `## UI/UX`; the script
  reads them from layout when a morph starts, and never stores them.
- **The dock's verbs** — `show`, `screen`, `hide`, `release`, `flip` belong to the display channel, owned by the dock
  (spec 119); this slice only reads their outcome.
- **Motion state** — an animation is a class plus a timer, not a field; a reload repaints from the display state alone.
- **The projector page** — it renders the same screens for the wall; the overlay shares the data, not the layout.
