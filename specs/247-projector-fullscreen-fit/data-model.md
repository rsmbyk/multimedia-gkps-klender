# Data Model: refit the projector words when fullscreen changes the stage

**Spec**: `specs/247-projector-fullscreen-fit/spec.md`

## Entities

### Active screen

| Field | Type | Constraints | From |
| --- | --- | --- | --- |
| `lines` | DOM node `.screen__lines` | carries the fitted inline `font-size` | FR-001 |
| `head` | DOM node `.screen__head` | carries `font-size ÷ golden ratio` | FR-001 |
| `dataset.fitted` | string key | stage box + head + line count + body length | FR-003 |
| `current` | integer | index into `screens()`; unchanged by a fullscreen signal | SC-004 |

**Relationships**: one active screen is on the stage; a Go To detour is the active screen while
`detour` is set, and the service's own screens keep their keys but stay unfitted behind it.
**Validation**: the screen on the stage is the one that gets the new size; neighbours are fitted
in idle time after it.
**State transitions**: `windowed → fullscreen → windowed` — driven by `fullscreenchange`, a
`(display-mode: fullscreen)` change or `resize`; no screen move, cue change or service change.

## Invariants

- The size written by a fullscreen signal equals the size a resize would write for the same stage
  (FR-003, SC-003).
- A signal that leaves the stage unchanged writes no new size (US1/AC4).
- The heading stays at `lines.size ÷ golden ratio`; no typography rule is edited (FR-006).

## Not modelled

- No new persisted entity, client flag or state variable: the signal handlers read the stage and
  write the same inline sizes the existing fit writes. No clock or timer is added; the frame is
  the only sequencing primitive.
