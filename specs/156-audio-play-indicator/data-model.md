# Data Model: The audio projector screen shows its play/pause control

**Spec**: `specs/156-audio-play-indicator/spec.md`

Nothing is stored. The screen is painted from the projector's own response and the audio from the local
companion; the slice adds no field, no column and no payload. The model below is the **view model** the
stylesheet and the one script guard have to keep true.

## Entities

### Play/pause control (`.screen__audio-play`)

| Field | Type | Constraints | From |
| --- | --- | --- | --- |
| `box` | 48 × 48, `border-radius: 50%` | fixed; never shrinks in the layout when hidden | FR-001 |
| `mark` | `::before` glyph | 12 × 16 triangle while `data-playing="false"`; 14 × 18 two-bar block while `true` | FR-002 |
| `opacity` | 1 or 0 | 1 whenever the chrome is up, 0 when `.is-idle` | FR-003 |
| `pointer-events` | `auto` / `none` | `auto` when visible, `none` under `.is-idle` | FR-003, FR-005 |
| `aria-label` | text | `Play audio` while paused, `Pause audio` while playing — written by `media-audio.js:update()` | FR-004 |
| `data-playing` | `"true"` / `"false"` | the single source of the mark; written only by `media-audio.js` | FR-002 |

**Relationships**: one control per `.screen__audio-player`; the player is one per audio service entry.
**Validation**: the control paints only when the player is showing — `onReady` unhides the player, and a
failed or missing file leaves it hidden with the missing-file mark instead (edge case, unchanged).
**State transitions**: `paused → playing` on a click or `Space`; `playing → paused` on either again, on
`ended`, or when the screen is left (the player is stopped and torn down).

### Chrome state (`.screen__audio-box.is-idle`)

| Field | Type | Constraints | From |
| --- | --- | --- | --- |
| `is-idle` | class | added by `audioActivity()` 3.5s after playback starts; removed by any pointer move, pointer down or key press | `projector.js:62`, FR-003 |
| `control` | effect | opacity 0, `pointer-events: none` | FR-003 |
| `seek` | effect | opacity `.52` (existing) | FR-003 |
| `times` | effect | opacity `.4` (existing) | FR-003 |

**Relationships**: the idle class belongs to the box, and the control, bar and times all read it.
**State transitions**: `active → idle` 3.5s after playback starts, and only while playing; `idle → active`
on any input; a paused player never enters `idle`.

## Invariants

- The control's box is 48 × 48 in every state, so the seek bar's `y` never changes when the chrome settles
  and returns (FR-003, SC-004).
- The mark reads `data-playing` and nothing else; no second state store is introduced (FR-002).
- Only the control takes pointer events inside the audio box; everything else in the box stays
  transparent to the pointer, so the zones keep working (FR-005).
- The audio box is the only element this slice lifts above the zones, and only while an audio screen is
  the active one — no other screen's stacking changes (FR-006).

## Not modelled

- The audio element itself — its URL, MIME sniffing and playback belong to `media-audio.js`, unchanged.
- The fullscreen gesture — a page-level rule modelled in `research.md` D003, not in this view model.
- The seek bar's own clickability — explicitly out of scope (spec Assumptions): the bar keeps the
  pointer behaviour it has today.
