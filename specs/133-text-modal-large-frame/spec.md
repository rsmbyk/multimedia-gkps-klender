# Feature Specification: A text entry is written and edited in the media modal's large frame

**Slice**: `specs/133-text-modal-large-frame`
**Branch**: `feat/133-text-modal-large-frame`
**Created**: 2026-10-25
**Status**: Accepted (owner, gate 1, 2026-10-25 — accepted with the branch updated onto `develop`
`ffa5c340` first; the geometry was re-measured on that base before this line was written. Gate 2 the
same day: plan, the eight checklist items, tasks and analysis accepted, every item ticked.)
**Input**: "make the new text modal to be the same large modal as new media modal" — sent with a
screenshot of the New text dialog: a 480×495 panel carrying the Multi-line/Single-screen switch, a
Title (optional) field and a 131px Text box, opened over an otherwise empty `25 OKTOBER 2026`
service whose `+ Media` action opens a dialog of a different size altogether.

## User Scenarios & Testing

### US1 — A new text entry is written in the same large frame as a new media entry (P1)

**Why this priority**: `+ Text` and `+ Media` sit side by side on the same stage and open the same
`<dialog>`; one of them draws 480×495 and the other 840×760. The small one leaves a 131px box for the
field the operator actually fills — the text that goes on the projector — while the media dialog spends
its height on a drop zone. Matching the frames is what the request asks for, and it is the story that
can ship alone.

**Independent Test**: open a service, click `+ Text`, measure the dialog: 840×760 with the media
dialog's title band, gutters and action row, and a Text box that fills what is left.

**Acceptance scenarios**

1. **Given** a Tata Ibadah service and editing enabled, **When** `+ Text` is clicked at 1440×900,
   **Then** the dialog measures 840×760 at (300, 70) — the same box, at the same place, as `+ Media`.
2. **Given** the same dialog, **When** its chrome is compared with `+ Media`'s, **Then** all of these
   are equal: content padding 0, a 72.5px title band padded 20px/26px with a 1px bottom divider at
   21px type, top-level fields 788 wide at x=326 (26px gutters, 14px apart), and an action row at
   y=772 that is 38px tall with no top divider and 14px/20px of margin.
3. **Given** the same dialog, **When** the Text box is measured, **Then** it is 419px tall — the height
   the switch, the title field and the action row leave — instead of the 131.3px six-row box, and its
   bottom edge meets the action row's 14px margin.
4. **Given** the modal is open and empty, **When** the operator types, **Then** Save enables; **When**
   the field is cleared, **Then** Save disables again — unchanged from today.
5. **Given** the modal is open, **When** `Single-screen` is picked, **Then** the hidden
   `default_screen_mode` input reads `single_screen`, the switch shows that option selected and the help
   line reads "One fitted screen by default" — and the frame does not resize.

### US2 — An existing text entry is edited in that same frame (P1)

**Why this priority**: the Edit form is the same template with the same two fields; a 480px edit form
for a text entry that is created in 840px would make the size depend on which step the operator is on.
The owner chose "every text form" at Clarify.

**Independent Test**: open an existing text entry's Edit and measure the same box.

**Acceptance scenarios**

1. **Given** a service holding a text entry, **When** its Edit control is clicked at 1440×900,
   **Then** the dialog measures 840×760 at (300, 70), with the title band reading `Edit text`.
2. **Given** that dialog, **When** the Text box is measured, **Then** it fills the leftover height
   (507px for a one-field form) and the existing text is shown in it.
3. **Given** any other kind's Edit — passage, song, media — **When** it is opened, **Then** it keeps
   the compact frame it has today (480 wide, content padded 22px).

### US3 — The frame is placed against the viewport, not the document (P1)

**Why this priority**: a 760px frame opened from a long service's entry was measured starting at
y = −4 with the page scrolled 74px: the dialog is `position: relative`, so the document's scroll offset
moved it up and clipped the title band. The small dialogs had the same fault (the passage dialog on a
page scrolled 400px would have opened at y = −161); it only became visible at this size. US2 cannot be
satisfied without it, because an entry's Edit is always below the fold of a filled stage.

**Independent Test**: scroll a filled service to the bottom, open an entry's Edit: the dialog is
centred on the window and both its edges are inside it.

**Acceptance scenarios**

1. **Given** `/tatib/144/` scrolled to the bottom (scrollY 556) at 1440×900, **When** the text entry's
   Edit is opened, **Then** the dialog's top is at y=70 and its bottom at 830 — centred, nothing clipped.
2. **Given** the list page scrolled 250px, **When** a service's edit form is opened, **Then** it is
   centred (measured 285.8 for a 328.5px form) and the date popover still opens 8px under its trigger
   (measured 504.3 against a 496.25px trigger bottom) and inside the window.
3. **Given** the stage scrolled 400px, **When** `+ Passage` is opened, **Then** its compact dialog is
   centred on the window (measured 238.6 for a 422.8px form).

### Edge Cases

- **When** the window is 1280×800 **Then** the frame is 840×760 at (220, 20) and nothing scrolls.
- **When** the window is 1280×600 **Then** the frame is 840×568 at (220, 16), the Text box 227px, the
  action row at y=526 — the dialog fits the window and the page behind does not gain a scrollbar.
- **When** the window is 390×844 **Then** the frame is 352×760 at (19, 42), the title band 64.5px
  padded 16px/18px, fields 316 wide at x=37, the Text box 427px.
- **When** the text is longer than the box **Then** the Text box scrolls internally; the dialog keeps
  its size and the action row stays where it is.
- **When** the save is rejected with a 400 **Then** the re-rendered form is the same large frame (the
  marker is server-rendered per kind, not added by script).
- **When** a keyboard user opens the dialog **Then** focus lands in the Title field as it does today;
  `Save` keeps its existing disabled treatment and the existing focus rings are unchanged.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | A text entry's form — create and edit — opens in the dialog box the media create form uses: width `min(840px, 100vw − 32px)`, height `min(760px, 100dvh − 32px)`. | `reading/R10` |
| FR-002 | The large frame's chrome is shared, not copied: content padding 0; title band padded `20px 26px` with a 1px bottom divider at 21px; top-level fields and the mode switch inset `26px` from the sides with `14px` between them; the action row inset `26px`, `14px` above and `20px` below, with no top divider. | `reading/R10` |
| FR-003 | Inside the large frame the Text box takes the leftover height, from a `flex: 1` field down to a `flex: 1` textarea, and never pushes the action row out of the dialog. | `reading/R10` |
| FR-004 | Every other form keeps its current frame: passage, song and media create, passage/song/media edit, and the old-item forms stay 480 wide with 22px content padding. | `reading/R10` |
| FR-005 | Below 650px the large frame's gutters fall to 18px and its title band to `16px 18px`, exactly as the media create form already does. | `reading/R10` |
| FR-006 | The text form's behaviour is unchanged: the Multi-line/Single-screen switch and its help line, the Save guard, the hidden `default_screen_mode` field, and the 400 re-render path. | `reading/R10` |
| FR-007 | The editor dialog is placed against the viewport rather than the document, so its position does not depend on the page's scroll offset, while absolutely positioned children (the date popover) keep resolving inside it. | `reading/R10` |

### Key Entities

`none — the slice changes a dialog's frame and two template attributes; no model, field, relationship or
stored value changes.`

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | The two create dialogs are the same box, indistinguishable in chrome | The six measured values of US1/2 (box, title band, field gutter, field width, action row, button x) are equal between `+ Text` and `+ Media` at 1440×900 |
| SC-002 | The frame never clips and never makes the page scroll | At 1440×900, 1280×800, 1280×600 and 390×844 the dialog's top is ≥ 0, its bottom ≤ the window height, and `documentElement.scrollHeight` does not exceed the window |
| SC-003 | The dialog is centred whatever the page's scroll position | At scrollY 0 and scrollY 556 the same 760px dialog sits at y=70 |
| SC-004 | No other form changes size | The passage form measures 422.8 tall and 480 wide with the page scrolled; the media create form still measures 840×760 at (300, 70) |

## UI/UX

Measured on the running worktree (`probe_modal_frame.py`), 1440×900, light theme; the dark theme draws
the same geometry with the same tokens.

| | New text — before | New text — after | New media (unchanged) |
| --- | --- | --- | --- |
| Dialog box | 480 × 494.8 at (480, 202.6) | 840 × 760 at (300, 70) | 840 × 760 at (300, 70) |
| Content padding | 22px | 0 | 0 |
| Title band | 42px tall inside the padding, 18px type, no full-bleed divider | 72.5px tall, padding `20px 26px`, 21px type, 1px bottom divider | 72.5px, `20px 26px`, 21px, 1px divider |
| Field gutter / width | 22px / 436px at x=502 | 26px / 788px at x=326 | 26px / 788px at x=326 |
| First field under the title | 16px | 14px | 14px |
| Text box | 131.3px (`rows="6"`) | 419px — fills what is left | — |
| Action row | `18px 0 0`, 1px top divider, 16px padding, y=620.4, 55px tall | `14px 26px 20px`, no divider, y=772, 38px tall | same as after |
| Save button x | 781.8 | 957.8 | 957.8 |

- **Layout / position**: unchanged order — title band, the Multi-line/Single-screen switch centred at
  `min(308px, 100%)`, its help line, Title, Text, actions at the bottom right.
- **Size / spacing**: the numbers above. Edit text measures 840×760 with a 507px Text box.
- **Colour / typography**: nothing new; the frame reuses `--canvas`, `--ink`, `--divider`, `--head-ink`,
  `--active-bg`/`--active-ink`, `--focus` and `--shadow-dialog`.
- **States**: hover · focus · active of Save/Cancel and the switch are the existing components, unchanged;
  disabled Save (empty text) unchanged; empty title unchanged. New states: none.
- **Motion**: none added. The 190ms `media-library-in` scale stays media-only (assumption A-4).
- **Responsive**: 1280×800 → 840×760 at (220, 20); 1280×600 → 840×568 at (220, 16), Text 227px, actions
  at y=526; 390×844 → 352×760 at (19, 42), title band 64.5px padded `16px 18px`, fields 316px at x=37,
  Text 427px.

## Assumptions

- **A-1** "The same large modal" means the same finished box and chrome as New media's — 840×760 clamped
  to the window, 26px gutters, a full-bleed title band at 21px, actions at the bottom with no divider —
  rather than a second, differently proportioned large size.
- **A-2** The Text box grows into the height the frame leaves; a 760px frame around a fixed 131px box
  would be a hole, and the text is the form's subject.
- **A-3** The wide Text box (788px) is accepted as drawn: these entries are short projection lines, and
  the frame is chosen for parity with the media dialog, not for line-length comfort.
- **A-4** No motion is added to the text dialog; it still appears without the media dialog's 190ms
  scale-in. Veto at gate 1 if the two should move alike.
- **A-5** No copy changes: the title, the field labels, the help line and the media modal's own strings
  keep their wording.

## Clarifications

### Session 2026-10-25

- Q: Does the large frame go to New text only, mirroring New media where only the create dialog is
  large? → A: **Both** — every text form takes the large frame (create and edit).
