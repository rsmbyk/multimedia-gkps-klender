# Data Model: the empty notice leaves the stage

**Spec**: `specs/161-projector-empty-notice/spec.md`

No server data is added, read or changed. The model this slice decides is the **page state** the
notice is painted from, because that is what the requirements name.

## Entities

### Empty notice

| Field | Type | Constraints | From |
| --- | --- | --- | --- |
| `element` | `HTMLParagraphElement` `p.projector__empty` | server-rendered only when the response carries no screens; at most one per page | FR-001 |
| `hidden` | boolean attribute | `true` when the stage holds a screen or a detour; `false` otherwise | FR-001, FR-002, FR-004 |
| `copy` | text | `Nothing to show yet: this Tata Ibadah has no items.` — unchanged by this slice | FR-007 |

**Relationships**: the notice is a **sibling** of `#projectorScreens` inside `.projector__screen`
(a flex column), so its own box decides how much room the stage gets.
**Validation**: there is never more than one notice (the template renders it once); the script must
not create one.
**State transitions**:

| From | Event | To |
| --- | --- | --- |
| — | response with no screens, nothing else showing | `visible` |
| `visible` | a Go To detour paints (`openDetour`, or any `renderDetour()`) | `hidden` |
| `hidden` | the detour closes (`leaveDetour` → `render()`) and the service still has no screens | `visible` |
| either | a re-read (`reflow()`) ends in `render()` with `screens().length > 0` | `hidden` |
| either | a re-read ends in `render()` with no screens and no detour | `visible` |
| either | another Tata Ibadah is adopted (`adoptService()` → `done` → `render()`) | by the adopted service's screens |

### Stage

| Field | Type | Constraints | From |
| --- | --- | --- | --- |
| `screens` | `NodeList` of `section.screen[data-screen]` | the response's screens; empty for an empty service | FR-001, FR-004 |
| `detour` | `section.screen.projector-detour` or absent | the script's own node, appended once; `is-active` while a passage or a song is painted | FR-002, FR-003 |
| `height` | layout value | flex child of `.projector__screen`: whatever the notice does not take | FR-002 |

## Invariants

- **One decision point.** `hidden` is written in `syncEmptyNotice()` only, and that function reads
  only `screens().length` and `detour` (FR-005).
- **The notice never coexists with painted content.** A stage with a screen or a detour has the
  notice `hidden`; a stage with neither has it visible (FR-001, FR-002, FR-004).
- **Nothing is created.** The script never inserts a notice, so a page that arrived with screens
  cannot gain one (spec edge case, Assumptions).
- **The copy is untouched.** The sentence, its 28px size, colour and centred position are the
  server's (FR-007).

## Not modelled

- **The display's on/off state.** `data-showing` hides the active screen through CSS; it is not part
  of the notice's rule (research D005).
- **A service emptied while its page is open.** The notice cannot appear without the server's own
  markup, and this slice does not add one; recorded in the spec's edge cases.
- **Saved or persisted state for the notice.** None exists or is added.
