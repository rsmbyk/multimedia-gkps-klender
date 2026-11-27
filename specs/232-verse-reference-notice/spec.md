# Feature Specification: Verse reference notice sits in the action row

**Slice**: `specs/232-verse-reference-notice`
**Branch**: `feat/232-verse-reference-notice`
**Created**: 2026-11-23
**Status**: Accepted (Gate 1 2026-11-23; Gate 2 2026-11-23)
**Input**: "i wanna revamp the warning/notice in edit song verse modal when the verse is being used in a service"
**Demand**: `ITEM-248` (new card)
**Capability**: modifies `reading/R40` (the referenced-verse scenario)
**Preview**: `specs/232-verse-reference-notice/preview/index.html` — owner chose **B · Inline** on 2026-11-23

## User Scenarios & Testing

### US1 — The reason for the disabled delete is read where the button is (P1)

**Why this priority**: the current explanation is a 12px line *below* the action row (`_editor_form.html:81`),
so a reader meets a faded red `Delete verse` before learning why it cannot be pressed. Moving the reason
into the same row, and making the disabled button neutral rather than a faded danger colour, lets the
constraint be understood in one glance without changing the rule behind it.

**Independent Test**: from the app's home URL, open a song whose verse is named by a service, open that
verse's editor and measure the action row: one line of text sits left of the three buttons, the row is
still 38px tall, the note reads `Used in 1 Tata Ibadah — delete unavailable`, and the disabled button's
computed opacity is `1` with `--rail-bg` fill and `--head-ink` text.

**Acceptance scenarios**

1. **Given** a verse named by one service **When** its edit dialog opens **Then** the action row's first
   child is the note `Used in 1 Tata Ibadah — delete unavailable`, left of `Delete verse`, `Save` and
   `Cancel` in that order.
2. **Given** the note **When** it is inspected **Then** the number is the same count the delete guard
   uses, shown as `1 Tata Ibadah` for one and `3 Tata Ibadah` for three, with the numeral in 700 weight.
3. **Given** the referenced verse **When** `Delete verse` is measured **Then** it is disabled with
   computed opacity `1`, `--rail-bg` fill, `--divider` border and `--head-ink` text — never a faded red.
4. **Given** a verse no service names **When** its edit dialog opens **Then** no note is drawn and
   `Delete verse` keeps its base enabled styling and behaviour.
5. **Given** any other editor (songbook, song, Tata Ibadah) or the verse-delete confirmation
   **When** its dialog opens **Then** its action row and disabled buttons are byte-identical to the base.

### US2 — The inline note survives a narrow dialog without squeezing (P2)

**Why this priority**: the note shares the row with three buttons; at phone widths a single line would
be crushed into a 99px, four-line block. The fix must not trade a missed warning for an unreadable one.

**Independent Test**: at 420×900 open a referenced verse's editor and measure the action row: the note
is one 352×18 line on its own row above the buttons, the buttons remain on one right-aligned row, and
nothing overflows horizontally.

**Acceptance scenarios**

1. **Given** a 420px viewport **When** the dialog is measured **Then** the note is 352×18 on a full-width
   line, the action row is 66px tall and has no horizontal overflow.
2. **Given** the note wraps **When** the buttons are measured **Then** `Delete verse`, `Save` and `Cancel`
   keep their 38px height and their right alignment, in the original order.
3. **Given** light or dark theme **When** the note and disabled button are measured **Then** both use
   only existing tokens (`--rail-bg`, `--divider`, `--head-ink`, `--ink`) with no new palette entry.

### Edge Cases

- The modal body is fetched from `/editor/verse/<pk>/` and swapped into `#editorContent`; the note must
  come from the server template, not from a one-off script on the song page, so a reopened dialog shows it.
- The count is verse-level: the view loops song entries and tests `verse.pk in (entry.verses or [])`
  (`views.py:181-184`); the note must use that same context value and must not switch to the page-level,
  song-wide count at `views.py:2452`.
- A verse named by three services is still one note, not three; the numeral changes only.
- The delete endpoint's guard (`verses.py:116-129`) is unchanged: the note explains a refusal, it does not
  replace the refusal.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | For a referenced verse, the editor action row SHALL begin with one note reading `Used in <count> Tata Ibadah — delete unavailable`, with `<count>` from the existing `named_service_count`, before the three buttons in their existing order. | `reading/R40` |
| FR-002 | The note SHALL be a 15px inline lock SVG in `--head-ink` followed by 12px/18px `--head-ink` text, the numeral in 700 weight and `--ink`. | `reading/R40` |
| FR-003 | At widths above 650px the note SHALL sit on the action row's baseline without increasing the row's 38px height; the note box SHALL be 18px tall and vertically centred with the buttons. | `reading/R40` |
| FR-004 | The disabled verse-delete button SHALL be neutral: computed opacity `1`, `--rail-bg` fill, `--divider` border, `--head-ink` text and `cursor: not-allowed`. The rule SHALL be scoped to the verse editor's delete control so no other disabled danger button changes. | `reading/R40` |
| FR-005 | At widths of 650px or less the action row SHALL wrap: the note takes a full-width line above the buttons, and the buttons keep one right-aligned 38px row with no horizontal overflow. | `reading/R40` |
| FR-006 | An unreferenced verse's editor, non-verse editors, the delete confirmation and the loading skeleton SHALL remain unchanged. | `reading/R40` |
| FR-007 | The service-reference count and the server-side delete refusal SHALL remain unchanged; the note is presentation only. | `reading/R40` |
| FR-008 | The note SHALL be associated with the disabled button for assistive technology (`aria-describedby` on the button pointing at the note). | `reading/R40` |

### Key Entities

- **Verse editor fragment** — `reading/_editor_form.html`, fetched into the shared dialog; this slice
  changes only the referenced-verse branch of its action row.
- **Verse reference count** — the number of song-kind service entries whose `verses` list names this
  verse; already computed in `_editor_fragment_context` and reused, not recomputed.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | The reason is visible beside the disabled action instead of below it | a Playwright walk from the home URL to a referenced verse's editor; note is the first child of `.editor__actions` |
| SC-002 | The row keeps its height at desktop width | computed action-row height 38px at 840px viewport, note 18px tall, no overflow |
| SC-003 | The disabled button reads as unavailable, not as a faded danger | computed opacity `1`, background `--rail-bg`, border `--divider`, text `--head-ink` |
| SC-004 | The count matches the guard and reads correctly for one and many | fixture with one service → `1 Tata Ibadah`; fixture with three → `3 Tata Ibadah`; delete still refused |
| SC-005 | The narrow dialog stays readable | 420×900 measurement: note 352×18 on its own line, row 66px, no horizontal overflow |
| SC-006 | Nothing else moves | non-verse editors and the unreferenced verse editor match the base boxes and styles |

## UI/UX

Measured on `preview/index.html` with the product's inlined `tokens.css` and editor CSS at 840×900 and
420×900, light and dark. The preview is the product's own dialog and form markup with the proposed note;
`preview/README.md` names every state.

- **Layout / position** — at 840px the note is 265 × 18 at y712 and the disabled button starts at x530
  in the same 38px row, with the note's right edge at x323: a 207px clear gap before the buttons. At
  420px the note takes a full-width 352 × 18 line at y674 and the buttons sit on the next row at y702.
- **Size / spacing** — the note's glyph is 15 × 15, the text 12px/18px, the numeral 700 weight; the
  desktop row stays 38px tall, the narrow row measures 66px. The note has no background or border of its
  own; only the button's neutral fill changes.
- **Colour / typography** — note text and glyph `--head-ink`, numeral `--ink`; disabled button
  `--rail-bg` fill, `--divider` border, `--head-ink` text at opacity `1`. No new token, no red tint:
  the note is a reason, not an error.
- **States** — referenced verse (note shown, button neutral-disabled) · unreferenced verse (no note,
  button enabled) · count 1 / count 3 · light / dark · 840px / 420px. Hover, focus and loading states
  of the buttons are unchanged.
- **Motion** — none. The note appears with the fetched fragment; no transition.
- **Responsive** — at 650px and below the action row wraps, the note takes the full inset width (352px at
  420px), and the buttons keep their row. Above 650px nothing wraps.

## Assumptions

- The note's copy is the one shown in the approved B · Inline preview; the domain noun stays
  *Tata Ibadah* and the chrome stays English.
- The neutral disabled treatment applies only to the verse editor's `Delete verse`; other dialogs keep
  the shared `.editor__danger:disabled` fade because this slice was asked about one modal.
- Wrapping, not shortening the copy, is the narrow-width answer: the reason stays complete at 420px.
- Card `ITEM-248` is created for this request; the number is checked against `develop` and the other
  worktrees before it is written.

## Clarifications

### Session 2026-11-23

- Q: Which notice presentation? → A: **B · Inline** — one line beside the buttons, no extra height at
  desktop width, neutral Delete (owner's choice in the preview).
- Q: Does `named_service_count` count services naming the song or this verse? → Verified in code: the
  editor context loops entries and tests the verse id (`views.py:181-184`), so the copy is accurate;
  no question put to the owner.
