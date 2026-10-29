# Feature Specification: Audio and video name their play/pause key

**Slice**: `specs/160-shortcuts-audio-video-groups`
**Branch**: `feat/160-shortcuts-audio-video-groups`
**Created**: 2026-10-29
**Status**: Accepted (owner, gate 1, 2026-10-29)
**Input**: "add play/pause to keyboard shortcuts modal for audio and video" — then, asked which sheet:
"projector sheet. move it to their own groups of 'Audio' and 'Video'"

## What the sheet does today

The projector's shortcuts sheet is `#key-list` in
`multimedia/web/templates/reading/projector_controls.html` — a static block of nine `.group`
sections laid out as three `.stack` columns. The third column opens with `Display`, whose four rows
are `Show or Hide Words` (Space), `Audio/Video Play/Pause` (Space), `Show or Hide Corner` (C) and
`Keyboard Shortcuts` (K). Everything else in the sheet is grouped by the thing the keys act on:
`Service`, `Song`, `Passage`, `Library passage`, `Library Detour`, `Find`, `While Finding`,
`Fullscreen`.

So the one row that acts on a single entry's media sits inside a group about the screen, beside the
other behaviour the same key has — and a group heading is the only thing telling an operator which
Space applies when.

Measured on the running develop page (`/projector`, compose `web` at `127.0.0.1:63404`) at
1920×1080 and again at 1280×720, sheet open: the sheet's box is 676.5 × 1124px, its columns'
natural heights are 634.5 / 380 / 609px, a row's pitch is 34px (3px padding either side of a 28px
key), a group heading is 21.5px, the gap between groups is 24px and between columns 32px, and the
sheet's padding is 20px 24px. The tallest column therefore sets the sheet's height, and the middle
column is 254.5px shorter than it. The preview reads the same sheet 0.4px shorter (676.1 × 1123.4),
its own sub-pixel rounding; either number sits under the 688px a 1280×720 window allows.

## User Scenarios & Testing

### US1 — The sheet names audio and video as the subjects of their row (P1)

**Why this priority**: this is the request. A group heading is how the sheet says what a key acts
on, and the two media kinds are the only subjects in it that share a heading with the screen rather
than owning one.

**Independent Test**: press K on the projector, read the middle column: a heading `Audio` above one
`Play/Pause` row and a heading `Video` above another, and no play/pause row left in `Display`.

**Acceptance scenarios**

1. **Given** the projector page, **When** the shortcuts sheet is opened with K, **Then** the middle
   column holds a group headed `Audio` whose single row reads `Play/Pause` and whose combo is the
   Space chord, and directly below it a group headed `Video` whose single row is the same.
2. **Given** the same sheet, **When** the `Display` group is read, **Then** it holds exactly
   `Show or Hide Words`, `Show or Hide Corner` and `Keyboard Shortcuts`, and the string
   `Audio/Video Play/Pause` appears nowhere in the sheet.
3. **Given** a 1280×720 window, **When** the sheet is opened, **Then** the sheet's box is 676.5px
   tall — the same box as before this slice — and nothing inside it scrolls.
4. **Given** a 1920×1080 window, **When** the sheet is opened, **Then** the sheet is 676.5px tall and
   1095px wide, and every row keeps its 34px pitch and every heading its 21.5px box.

### US2 — The keys the sheet names are unchanged (P1)

**Why this priority**: the sheet is a description. If regrouping it changed what Space does, the
description would be of a different product.

**Independent Test**: on a service whose entry is audio, Space plays and pauses it; on a text entry
Space hides and shows the words; with the sheet open Space does nothing.

**Acceptance scenarios**

1. **Given** a showing entry whose media is audio **When** Space is pressed **Then** that audio
   toggles play/pause once per press and the words do not change.
2. **Given** a showing entry whose media is video **When** Space is pressed **Then** that video
   toggles play/pause once per press and the words do not change.
3. **Given** a showing entry with no audio or video **When** Space is pressed **Then** the words hide
   or show, as before.
4. **Given** the sheet is open **When** Space is pressed **Then** nothing toggles, and **When** K or
   Escape is pressed **Then** the sheet closes.

### Edge Cases

- **When** the window is shorter than the sheet's box **Then** the sheet keeps `max-height:
  calc(100vh - 32px)` and scrolls inside itself, exactly as today.
- **When** the middle column is read on a narrow window **Then** no group wraps or clips: the column
  keeps its 379px width and the sheet keeps its 1095px width.
- **When** the operator's pointer is over a row **Then** nothing is added: the sheet's rows have no
  hover state and this slice adds none.
- **When** `prefers-reduced-motion: reduce` is set **Then** the sheet still opens without the
  animation, as today.
- **When** the reader counts headings **Then** the sheet holds eleven: the nine it has today, minus
  none, plus `Audio` and `Video`.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | The shortcuts sheet SHALL draw a group headed `Audio` holding one row, `Play/Pause`, whose combo is the Space chord. | `new: projector` |
| FR-002 | The shortcuts sheet SHALL draw a group headed `Video` holding one row, `Play/Pause`, whose combo is the Space chord. | `new: projector` |
| FR-003 | The `Display` group SHALL hold `Show or Hide Words`, `Show or Hide Corner` and `Keyboard Shortcuts` only; the combined `Audio/Video Play/Pause` row SHALL be removed. | `new: projector` |
| FR-004 | The two groups SHALL sit in the middle column, after `Library Detour`, so the sheet's box keeps its current height. | `new: projector` |
| FR-005 | The sheet's box, its columns' widths, its row pitch, its heading box and its group gaps SHALL otherwise be unchanged. | `new: projector` |
| FR-006 | Space SHALL keep toggling the showing audio or video, and toggling the words when neither is showing; an open sheet SHALL keep swallowing the key. | `new: projector` |

This slice adds `projector/R3` — the projector's existing file carries `R1` (the Go To index) and
`R2` (the page renders from its own response), and neither states what the shortcuts sheet says.

### Key Entities

- **Group** — a `.group` section: one `h3` heading and the `.row` paragraphs under it. Its heading is
  the subject a set of keys acts on; its height is the heading box plus its rows' pitch plus the 24px
  gap to the next group.
- **Row** — one `.row`: a `.fn` label at the left and a `.combo` of `.chord`s at the right. A chord
  draws one or more `.k` key caps; the Space cap is `.k.sp.glyph` with the `␣` mark.
- **Column** — a `.stack`: a flex column of groups. The sheet holds three, and its height is the
  tallest column's natural height.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | Audio and video each own a heading, and no combined row survives | the sheet's headings and rows, read from the rendered page: `Audio` → `Play/Pause`, `Video` → `Play/Pause`, `Display` → three rows, `Audio/Video Play/Pause` absent |
| SC-002 | The sheet is no taller than it is today | the sheet's box: 676.1px on the preview and 676.5px on the running page before → the same after, at 1920×1080 and at 1280×720 |
| SC-003 | Nothing else in the sheet moves | row pitch 34px, heading 21.5px, group gap 24px, column gap 32px, sheet padding 20px 24px — unchanged; the middle column grows 159px (380 → 539.3), still 95px shorter than the tallest |
| SC-004 | The keys themselves are unchanged | the projector's own media and words behaviour, exercised by the module's existing cases plus one new case |

## UI/UX

`static preview at specs/160-shortcuts-audio-video-groups/preview/preview.html` — the real
`tokens.css` and `projector.css` with the real sheet markup, in the projector's own dark canvas, at
1:1. The preview toggles between the sheet as it stands today and the sheet after this slice.

- **Layout / position**: the sheet keeps `left: 50%; top: 50%` centred, `gap: 32px` between its three
  columns, `padding: 20px 24px`, `border: 1px solid #3a372f`, `border-radius: 10px`. `Audio` and
  `Video` are the third and fourth groups of the middle column: `Library passage` (300.3px),
  `Library Detour` (55.5px), `Audio` (55.5px), `Video` (55.5px), with 24px between groups — the
  column's natural height 380 → 539.3px.
- **Size / spacing**: a group is its heading (14px at 1.25 line-height = 17.5px, `margin: 0 0 4px`)
  plus its rows at a 34px pitch (3px padding, 28px key cap, 3px padding; the separator between rows is
  a 1px `#ffffff08` border, so a two-row group is 90.5px and a one-row group 55.5px). The Space cap is
  84px wide (`.k.sp` = 3 × 28px), 28px tall, radius 5px.
- **Colour / typography**: unchanged — headings `--quiet` (`#8E8A80`), row labels `--on` (`#E8E4DC`)
  at 14px, keys `#2a2722` on `#4a463f` with the sheet's own shadow; no token is added.
- **States**: the sheet open (the only state a group has) and closed; today's sheet and the sheet
  after, both reachable in the preview; a 1280×720 window, where the sheet still fits at 676.5px
  under its 688px limit; a window shorter than that, where the sheet scrolls as today. No hover,
  focus, active, disabled, empty, error or loading state exists on this surface.
- **Motion**: unchanged — `projectorSheetIn` / `projectorSheetOut`, 180ms, `--display-ease`, and the
  `prefers-reduced-motion` exemption.
- **Responsive**: unchanged — no breakpoint; the sheet keeps `max-width: calc(100vw - 32px)` and
  `max-height: calc(100vh - 32px)`. The sheet's width falls from 1124px to 1095px because the removed
  row was the widest text in the third column.

## Assumptions

- **The column is the middle one.** The owner named the groups, not their place. The middle column is
  the shortest by 254.5px, so the two groups fit there without growing the sheet; beside `Display`
  the sheet would be 775px tall and scroll at 720p. — measured, both window sizes.
- **After `Library Detour`, not before `Library passage`.** Appending keeps every existing group where
  it is; the sheet's reading order changes only by gaining two groups at the end of the middle column.
- **One row per group, labelled `Play/Pause`.** The heading is the context, so no qualifier is added;
  the label keeps the wording the removed row used. — follows the owner's "their own groups".
- **The groups are always drawn.** The sheet is static markup and no group is conditional today; a
  group that appeared only while media was showing would be a different behaviour, not this request.
- **The Space chord is reused verbatim** — the same `.k.sp.glyph` cap, its `␣` mark, its title and
  `aria-label="Space"`.
- **No new CSS, token, script or endpoint.** The change is markup in one template.
- **The `Display` group is not otherwise touched**, and `Show or Hide Words` keeps its wording.

## Clarifications

### Session 2026-10-29

- Q: which sheet? → A: "projector sheet".
- Q: how should the pair be grouped? → A: "move it to their own groups of 'Audio' and 'Video'".
- Q: where in the sheet? → not asked; recorded as the first two assumptions above and vetoable at
  gate 1.
