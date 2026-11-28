# Data Model: refit the Go To detour on a stage resize

**Spec**: `specs/249-goto-fullscreen-fit/spec.md`

## Entities

### Go To detour

| Field | Type | Constraints | From |
| --- | --- | --- | --- |
| `is-active` | class | detour is the stage's screen | FR-001 |
| `lines` | DOM node `.screen__lines` | carries the fitted inline `font-size` | FR-001 |
| `dataset.fitted` | string key | stage box + head + line count + body length | FR-003 |
| `detour` | client flag | set while the detour is on the stage | FR-001 |

**Relationships**: while `detour` is set, the service screens keep their own keys but are not
fitted; `fitNeighbours()` returns early. On an `is-active` detour the stage-screen choice is
`detourNode`, not `screens()[current]`.
**Validation**: the detour's key follows the stage in both directions; a repeated resize at the
same stage writes no new size.
**State transitions**: `service screen → detour → service screen` — unchanged; a resize neither
opens nor closes a detour.

## Invariants

- The detour's size after a resize equals the size the fitter gives for that stage (FR-001).
- A resize with no detour leaves the service-screen fit exactly as before (FR-004).
- No new persisted entity, client flag or endpoint is introduced.

## Not modelled

- The fonts-ready path still clears the detour key without fitting it; recorded as a known gap,
  not modelled by this slice.
