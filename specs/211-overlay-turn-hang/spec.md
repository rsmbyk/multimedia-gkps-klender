# Feature Specification: a speaker's turn hangs under its words

**Slice**: `specs/211-overlay-turn-hang`
**Branch**: `feat/211-overlay-turn-hang`
**Created**: 2026-11-21
**Status**: Accepted — Gate 1 and Gate 2, 2026-11-21
**Input**: the owner's request, 2026-11-21 — "in text entry, when interpreting the speaker lines, the consecutive lines after the lines with speaker tokens should be treated as that speaker lines as well, until a new speaker shows up"; clarified with the OBS overlay screenshot: "the line B should be the Liturgis' line. but it is not hanging on the same line as the one above it".

The voice already continues: `voice_lines` gives every unmarked line the previous speaker's
voice, across blank lines and screen breaks (spec 059). The screenshot shows the other half of the
same turn: in the OBS overlay the marked line owns a words column, and the continuing line is
painted at the plate's leading edge — under the mark. A turn therefore reads as a ragged stack.
This slice makes the continuation share the words column. It does not change the voice.

## Scope

### In scope

- `static/web/obs-overlay.js` — the plate's row builder: a line with no mark and a non-empty voice,
  on a screen that paints at least one mark, is marked as a continuation.
- `static/styles/design/obs-overlay.css` — that continuation row's indent: the same column and gap
  the marked rows use.
- `docs/spec/overlay.md` R5, modified at Fold.
- E2E coverage on the real overlay at 1280×720, plus the existing overlay suites.

### Out of scope

- The projector, the reading stage and the entry preview. None of them paints a speaker column;
  their continuation lines are unchanged.
- Speaker detection, labels and colours (spec 059). The continuation already carries the voice.
- A speaker token alone on its line (`Paragenda:` with the words below). The classifier does not
  read it as a mark today; that separate shape is ITEM-224.
- Blank lines, cue lines (`Nyanyian: …`) and bodies with no speaker. Their voice is empty and their
  layout is unchanged.
- The overlay's enter, leave and resize motion, its type scale and its plate width.

## Domain rules

- **Continuation.** A line with no mark and a non-empty voice is the previous speaker's turn
  continuing. `voice_lines` sets exactly that pair: a mark sets the voice, an unmarked non-blank
  line inherits it, and a cue resets it to `''`.
- **One column per screen.** The marked lines of a screen share one column sized by the widest mark
  (R5). The continuation is indented by that column and its gap; it paints no mark.
- **No mark, no column.** A screen that begins mid-turn and paints no mark has nothing to align to;
  its lines stay flush at the plate's content edge.
- **Empty voice, ordinary line.** A line with an empty voice — ordinary text, a cue, a body with no
  speaker — stays flush at the plate's content edge.
- **Voice is preserved.** The continuation keeps its `is-leader` / `is-join` treatment (and
  `assembly`'s ordinary ink). Only its x changes.
- **Wrapping.** A continuation that wraps keeps every visual row at the words column and its ink
  inside the plate's content box.

## User Scenarios & Testing

### US1 — A leader's turn reads as one block (P1)

**Why this priority**: the words are on screen but the turn's second line begins under the mark,
so the congregation reads it as a new, unrelated line and the speaker cue breaks. The fix is the
owner's report, and it is the only user-visible outcome of the slice.
**Independent Test**: project a text with `L. Aku percaya kepada Allah` followed by
`Bapa yang mahakuasa, Khalik langit dan bumi.`; read the overlay at 1280×720: the second line
begins at the same x as `Aku`, carries `is-leader`, and no ink passes the plate.

**Acceptance scenarios**

1. **Given** a liturgy screen with a marked leader line and an unmarked line after it **When** the
   screen is on air in the OBS overlay at 1280×720 **Then** the unmarked line's first glyph begins
   at the marked line's words x, within 1 px.
2. **Given** the same screen **When** it is on air **Then** the unmarked line carries `is-leader`
   and its colour matches the marked line's words.
3. **Given** a marked line, a continuation and a new `J.` line **When** the screen is on air
   **Then** the continuation and the `J.` line's words begin at the same x, the column sized by the
   widest mark.

### US2 — The rule stays inside a real turn (P2)

**Why this priority**: the overlay paints ordinary text, cues and mid-turn screens too. Indenting
those would move text the owner did not report and would make a cue look like a speaker's line.
**Independent Test**: project a cue line, a body with no speaker, and a screen whose lines all
continue a turn but which carries no mark; all stay at the plate's content edge.

**Acceptance scenarios**

1. **Given** a screen whose only lines continue a turn begun on the previous screen and carry no
   mark **When** it is on air **Then** its lines stay flush at the plate's content edge.
2. **Given** a cue line (`Nyanyian: …`) followed by ordinary lines **When** the screen is on air
   **Then** the cue and the lines stay flush at the plate's content edge and keep their ink.
3. **Given** an unmarked body with no speaker at all **When** it is on air **Then** nothing moves.

### Edge Cases

- **When** a continuation is long enough to wrap **Then** every visual row begins at the words
  column and no ink passes the plate's content edge.
- **When** the mark is `P + K:` and another is `L.` **Then** the column is the widest of them and
  the continuation follows the same column.
- **When** a blank line separates the continuation from its mark **Then** the voice still carries
  onto the next screen; that screen hangs only if it paints a mark, and stays flush otherwise
  (FR-003).
- **When** the continuation comes before the screen's first mark **Then** it still hangs, because
  the column is a fact about the screen, not about the line's order.
- **When** the speaker is an ordinary group (`J.`, `Bapa:`) **Then** the continuation hangs at the
  column although it has no colour of its own; the alignment is independent of the colour.
- **When** the screen has no mark at all **Then** no indent is added, even if the voice is
  non-empty.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | An overlay liturgy line with no mark and a non-empty voice SHALL be laid out at the screen's words column when the screen paints at least one mark. | `overlay/R5` modified |
| FR-002 | The continuation SHALL be indented by the marked row's column and gap, so its first glyph lands on the words x; it paints no mark. | `overlay/R5` modified |
| FR-003 | When the screen paints no mark, a continuation SHALL stay flush at the plate's content edge. | `overlay/R5` modified |
| FR-004 | A line with an empty voice SHALL stay flush at the plate's content edge. | `overlay/R5` modified |
| FR-005 | The continuation SHALL keep the voice class it already carries; no colour, weight or motion changes. | `overlay/R5` |
| FR-006 | A wrapped continuation SHALL keep every visual row at the words column and inside the plate's content box. | `overlay/R5` modified |

### Key Entities

- **Overlay line** — what `modelOf` hands the plate: `text`, `voice` (`leader`, `join`,
  `assembly` or `''`), `mark` (`''` when the line has none) and `words`. The continuation is
  `mark === '' && voice !== ''`.
- **Speaker column** — the single `--speaker-col` width the plate sets on its body from the widest
  `.obs-overlay__speaker`; the marked rows' words and the continuation share it.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | At 1280×720 the continuation's first glyph x equals the marked line's words x within 1 px. | E2E `tests/e2e/test_obs_overlay.py` |
| SC-002 | The continuation's wrapped rows all share that x within 1 px, and its right ink edge stays within the plate's content edge. | same |
| SC-003 | A no-mark screen's lines stay at the plate's content edge (no added indent). | same |
| SC-004 | The marked lines, the voices and the existing overlay suites are unchanged. | the existing suite |

## UI/UX

- **Layout / position**: the continuation row is indented by exactly the marked row's column and
  gap — `padding-left: calc(var(--speaker-col, 0px) + .45em)`, the same pair the `has-mark` grid
  uses. At 1280×720 the plate's font is 24 px (`1.875cqw`); `L:` measures about 18 px and the words
  x sits about 29 px (28.8 px measured) from the plate's content edge. At 1920×1080 those are
  36 px and about 43 px. The values scale with the stage; no fixed px.
- **Size / spacing**: the words column is the one R5 already sets; the continuation adds no margin
  of its own. The plate hugs its widest row and is centred, so when the continuation is that row
  the panel grows by the indent (measured 28.8 px at 1280×720) and re-centres; it stays inside the
  90 % cap and both the marked words and the continuation keep one x. The row itself may also grow
  taller because its line is narrower than the full content width.
- **Colour / typography**: unchanged. A leader continuation is `rgba(255,255,255,.381)`, a joined
  one `rgba(255,255,255,.8)`; an assembly continuation keeps the body ink.
- **States**: a leader turn, a joined turn, an assembly turn, a no-mark screen, a cue, a wrapped
  continuation.
- **Motion**: none added. The panel's enter/leave/resize is untouched.
- **Responsive**: 960×540, 1280×720 and 1920×1080 — the column is measured from the mark each
  paint and the gap is em-based, so the relationship holds at every size.
- **Preview**: `specs/211-overlay-turn-hang/preview/index.html` — a static page built from the real
  `obs-overlay.css` and the plate's real classes; before/after at 1280×720, plus the no-mark
  control.

## Assumptions

- A line with a non-empty voice and no mark is a continuation; this is the spec 059 data contract,
  not a heuristic added by this slice.
- The screen's one column is the correct anchor. A screen with no mark has no anchor, so flush left
  is the intended "nothing to align to" case.
- The owner's screenshot is the OBS overlay (its liturgy plate has the mark column); the projector
  and reading page are out of scope.
- A token alone on its line is not in scope; it is not a mark today and is captured as ITEM-224.
- The existing `--speaker-col` measurement is reused; no second measurement pass and no fixed
  column width are introduced.
- The plate may grow by the indent when the continuation is its widest row. The plate already hugs
  its content between 34 % and 90 %, so this is its existing behaviour meeting a wider row, not a
  new sizing rule; the alternative — narrowing the words to keep the old panel width — would add
  wraps the owner did not ask for.

## Clarifications

### Session 2026-11-21

- Q: Which surface shows the defect? → A: the OBS overlay — the screenshot's liturgy plate with
  the `L:` column.
- Q: Does the continuation's voice need to change? → A: no. `voice_lines` already gives it the
  leader's voice; the line is in the leader's colour but at the wrong x.
- Q: Is a speaker token alone on its line in scope? → SKIPPED, assumed out of scope; recorded as
  ITEM-224 with the 23-line evidence from the local snapshot.
