# Data Model: a speaker's turn hangs under its words

**Spec**: `specs/211-overlay-turn-hang/spec.md`

## Entities

No model, field, route or payload is added. The slice reads two existing values the projector
already hands the overlay for each line (`_screen_lines` → `modelOf` → `plate`):

| Field | Type | Meaning here | Source |
| --- | --- | --- | --- |
| `mark` | str | the speaker token lifted out of the line; `''` when the line has none | `voices.read_mark` |
| `words` | str | the text after the mark on a marked line; the whole line otherwise | `voices.read_mark` |
| `voice` | str | `leader`, `join`, `assembly`, or `''` for ordinary text | `voices.voice_lines` |
| `text` | str | the full line as written; this is what an unmarked row paints | `voices.voice_lines` |

### Derived values (this slice)

| Value | Type | Definition |
| --- | --- | --- |
| `hasPaintMark` | bool | `model.lines.some(function (line) { return line.mark && line.words; })` — a property of the screen, computed once in `plate()` |
| `is-continuation` | CSS class | added to a row when `!line.mark && line.voice && hasPaintMark`; no new data field |

**Relationships**: `is-continuation` and `.has-mark` are mutually exclusive. Both read the
`--speaker-col` custom property that `applySpeakerColumn` sets on `.obs-overlay__body`.
**Validation**: none — the rule cannot produce an invalid state; an empty voice or a mark without
words simply fails one of the two conditions.
**State transitions**: none. A class is recomputed on every paint from the incoming model.

## Rendering invariants

- A marked row paints `mark | words` in the shared grid (R5, unchanged).
- A continuation paints its `text` only, at the words column, with its voice class and colour.
- A screen with no painted mark sets no `--speaker-col`; the continuation rule is not applied, so
  every line stays at the plate's content edge (FR-003, FR-004).
- Wrapping a continuation keeps all its visual rows at that indent and its ink inside the plate
  (FR-006); `fit-content` sizing may widen and re-centre the plate (accepted in the spec).

## Not modelled

- No `continuation` flag in the projector payload: it would duplicate the spec 059 voice contract
  at a second seam (D001).
- No second column measurement and no fixed width: `--speaker-col` is the single source (D002).
- A token alone on its line (`Paragenda:`) is still ordinary text to the classifier (ITEM-224).
  At this seam it is indistinguishable from any other line with a carried voice: on a screen that
  also paints a real mark it will receive `is-continuation`, which changes only its x, not its
  speaker, colour or words. Fixing that shape stays ITEM-224.
