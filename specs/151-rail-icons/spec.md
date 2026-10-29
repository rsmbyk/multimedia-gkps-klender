# Feature Specification: the rail says what each section is, and a song wears the rail's mark

**Slice**: `specs/151-rail-icons`
**Branch**: `feat/151-rail-icons`
**Created**: 2026-10-29
**Status**: Draft
**Input**: "can you find a better icons to represent Bible, Songs, and Service Order? … first, the bible
is represented as plain book today. maybe you can find something that can instantly tell people that it
is bible. second, the service order icon looks like a file/document instead and people might think that
it is a file manage or something. third, the icons used to represent medias should not be used for the
main rail to distinguish it (the songs main rail and songs media use the same icons). The icon for main
rail and service entry of type songs should have the same icons. either change the icons for audio files
or find another icon for Kidung main rail and service entry songs." — owner

## What the page does today

The main rail (`multimedia/web/templates/reading/base.html:64`) is an **80px** strip of **44 × 44px**
buttons, each holding one **24 × 24px** stroke glyph at `stroke-width: 1.7`
(`static/styles/design/components.css:145-166`, `static/styles/design/tokens.css:15-17`). Five
destinations, in order: Search, Alkitab/Bibel, Kidung/Doding, Tata Ibadah/Agenda, Media Library.

| Destination | Mark today | Source |
| --- | --- | --- |
| Alkitab / Bibel | an **open book** — two page halves and a gutter | `base.html:88-92` |
| Kidung / Doding | a **beamed pair of eighth notes** | `base.html:103-108` |
| Tata Ibadah / Agenda | a rounded page with three rule lines — a **document** | `base.html:119-123` |
| Media Library | a folder | `base.html:127` |
| Search | a magnifier | `base.html:75-78` |

Three collisions follow, and each is a shape, not a taste.

1. **The Bible and a passage are the same mark.** The rail's open book is the same construction the
   stage gives a *passage* (spec 144, `_entry_kind_icon.html`): two page halves, one gutter. The rail
   names the whole Bible; the stage names one passage in it; today nothing but the words tells them
   apart.
2. **Kidung and an audio file are the same mark.** `static/web/media-stage.js:6` draws the audio
   family as `M9 18V5l11-2v13` with two 3px noteheads; the rail's Kidung is `M9 17.4V5.6l10.2-2v11.6`
   with two 2.4px noteheads. That is the same beamed pair, within a unit on every coordinate — it is
   told apart by its 42px tinted chip, not by its shape. The same audio glyph is drawn by
   `window.gkpsMediaIcon` in the Media Library list, the service-media dialog and the upload preview.
3. **A song row's mark is not the rail's.** Spec 144 gave a song row a *single flagged note*
   (`_entry_kind_icon.html`, R25: "a single flagged note for a song"), while the rail **and** the empty
   stage's Add Song tile (`static/web/entries.js:66`) draw the beamed pair. One screen therefore shows
   two different note shapes for the same thing.

Measured on `/tatib/144/` at 1440×900: rail 80px wide, each button 44 × 44 at `x = 17.5`, each glyph
24 × 24 at `x = 27.5`; a song row's kind mark 20 × 20 at `x = 990` on a row starting at `x = 966`
(+24), its title at `x = 1030` (+64); a media row's chip 42 × 42 at `x = 979` (+13) with a 23 × 23
glyph inside it.

## User Scenarios & Testing

### US1 — A Bible reads as a Bible at a glance (P1)

**Why this priority**: this is one of the three marks the report names. The rail is the only permanent
label the product has; an operator glancing at it should not have to read "Alkitab" to know which
section is scripture.

**Independent Test**: open any reading page at 1440px, look at the rail's second button, and name the
section without reading its tooltip; then compare its shape with a passage row's mark on a Tata Ibadah
stage.

**Acceptance scenarios**

1. **Given** any reading page, **When** the rail draws, **Then** the Alkitab/Bibel button paints a
   closed book with a Latin cross on its cover.
2. **Given** a Tata Ibadah stage holding a passage, **When** the rail and the stage are on screen
   together, **Then** the rail's Bible and the passage's open book are different glyphs.
3. **Given** the same page in the dark theme, **When** the rail draws, **Then** the cross is still
   legible and the mark keeps one ink.

### US2 — A service order is not a file (P1)

**Why this priority**: the report says the mark reads like a file manager. A page-with-lines is the
same shape the product already uses for a PDF, so the rail is competing with its own media family.

**Independent Test**: at 1440px, compare the rail's Tata Ibadah mark with the PDF chip on a stage; the
two must not share a silhouette.

**Acceptance scenarios**

1. **Given** any reading page, **When** the rail draws, **Then** the Tata Ibadah/Agenda button paints a
   clipboard: a board, a clip above it, three rule lines.
2. **Given** a Tata Ibadah stage holding a PDF, **When** both are on screen, **Then** the rail's
   clipboard and the PDF's page-with-a-folded-corner are told apart without reading either.

### US3 — A song is one mark, wherever it is drawn (P1)

**Why this priority**: the report names the contradiction directly — the rail and a song entry must
agree, and a media file must stop borrowing the song's shape.

**Independent Test**: on one screen, find the rail's Kidung mark, the stage's Add Song tile and a song
row's mark; all three draw the same path. Then compare a song row with an audio media row: different
shapes.

**Acceptance scenarios**

1. **Given** a Tata Ibadah stage with a song entry, **When** it draws, **Then** the song row's mark and
   the rail's Kidung mark are the same path.
2. **Given** the same stage, **When** the empty state's Add Song tile is present, **Then** it draws the
   same path too.
3. **Given** a stage holding both a song entry and an audio media file, **When** both rows draw,
   **Then** the song's beamed pair and the audio file's waveform are different shapes.
4. **Given** the Media Library, **When** its list draws an audio file, **Then** that row's mark is the
   waveform, and the image, video, PDF and PowerPoint marks are unchanged.

### US4 — Nothing else about the chrome moves (P2)

**Why this priority**: the marks are decorative; the stage's geometry is a contract from specs
055/140/143/144. A new glyph must not resize a button, re-indent a title or change a row's height.

**Independent Test**: measure the five rail buttons and their glyphs, then a song row's mark and title
column, before and after; every value is identical.

**Acceptance scenarios**

1. **Given** any reading page, **When** the rail draws, **Then** each button is 44 × 44 and each glyph
   24 × 24 at the same x.
2. **Given** a Tata Ibadah stage, **When** a song row draws, **Then** its mark is 20 × 20 at the chip's
   centre line and its title still starts at the media title's column.
3. **Given** the rail's hover, focus and active states, **When** a button is pointed at or is current,
   **Then** the mark paints in the same ink as today's mark on the same state.

### Edge Cases

- **When** the window is narrower than 1272px and the rail is 64px with 40px buttons
  (`tokens.css:116`) **Then** the four marks draw at 20px and keep their proportions.
- **When** the rail is a phone's menu drawer **Then** the same marks sit beside the section names; no
  second artwork is introduced.
- **When** an audio file is missing, unavailable, or the local library is disconnected **Then** the
  audio row draws the same waveform; the missing and unavailable states keep their own treatment
  (`media-stage.js` `missing`).
- **When** a media entry's family is unknown **Then** the `missing` fallback is drawn, as today.
- **When** the rail is drawn on the search page, a song page, the Media Library or the OBS dock
  **Then** the marks are identical — there is one rail template.
- **When** the theme switches at runtime **Then** the marks change colour with `currentColor` and no
  repaint of their own is needed.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | The rail's Alkitab/Bibel destination SHALL draw a closed book with a Latin cross on its cover. | `new: reading` → R27 |
| FR-002 | The rail's Tata Ibadah/Agenda destination SHALL draw a clipboard — board, clip above it, three rule lines — and SHALL NOT draw a page, folder or document silhouette. | `new: reading` → R27 |
| FR-003 | The rail's Kidung/Doding destination, a song entry's kind mark and the empty stage's Add Song tile SHALL draw one and the same beamed-pair path. | `modified: reading` → R25 |
| FR-004 | An audio media file's family mark SHALL be a waveform of five rounded bars, in every place that mark is drawn: stage chip, Media Library list, service-media dialog, upload preview. | `new: reading` → R27 |
| FR-005 | The image, video, PDF and PowerPoint family marks, and the `missing` fallback, SHALL NOT change. | `new: reading` → R27 |
| FR-006 | Every mark SHALL keep today's box: a rail glyph 24 × 24 inside its 44 × 44 button; a song entry's mark 20 × 20 at the media chip's centre line with the title on the 64px column; a media chip 42 × 42 with a 23 × 23 glyph. No row's height, padding or title column SHALL change. | `modified: reading` → R25 |
| FR-007 | Every mark SHALL be inline SVG painted with `currentColor`, carry no new colour token or tint, keep `aria-hidden="true"`, and add no pointer target. | `new: reading` → R27 |
| FR-008 | The rail SHALL keep five destinations and their order; the Search and Media Library marks SHALL NOT change. | `new: reading` → R27 |

### Key Entities

- **Rail mark** — one of five decorative glyphs in the rail template, identified by its destination
  (`Search`, `Alkitab`, `Kidung`, `Tata Ibadah`, `Media Library`). Not data: it is the same markup on
  every page.
- **Kind mark** — the 20px glyph a stage row draws for `scripture` or `song` (spec 144). This slice
  changes the `song` path only.
- **Media family mark** — the glyph `window.gkpsMediaIcon(family)` returns for `image`, `audio`,
  `video`, `pdf`, `slides`, and the `missing` fallback. This slice changes the `audio` path only.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | The rail's five marks are five distinct path sets, and none of them appears in the media family map. | E2E: read `d` attributes from each rail button and from `window.gkpsMediaIcon` for the five families plus `missing`, assert no intersection. |
| SC-002 | The Kidung rail path, the song kind mark's path and the Add Song tile's path are string-identical. | E2E: compare the three `d` strings. |
| SC-003 | Rail buttons are 44 × 44 with 24 × 24 glyphs; a song row's mark is 20 × 20 at row + 24 and its title at row + 64; a media chip is 42 × 42 with a 23 × 23 glyph; row minimum heights stay 56px and 80px. | E2E: `getBoundingClientRect()` on the same nodes as §What the page does today. |
| SC-004 | A song row and an audio media row on one stage draw different silhouettes at 20px and 23px. | manual: the preview's stage column, and the live page, at 1:1 |
| SC-005 | Both themes paint every mark with the same computed colour as today's mark on the same element (`--ink`, `--head-ink`, `--focus` — no new token). | E2E: computed `color` on each mark in both themes, compared with `24a6d6d2` |

## UI/UX

**Static preview at `specs/151-rail-icons/preview/preview.html`** (regenerate with `build_preview.py`).
Two 502px columns — an 80px rail beside a 420px stage — built from the live page's own rail and
`<article class="read">` at `/tatib/144/`, with the stylesheets frozen at `24a6d6d2`. **Now** is the
shipped state; **Proposed** swaps the four marks. The bar switches each mark to its alternative, and
**Dark** flips the theme, so every candidate below is reachable by hand.

- **Layout / position**: unchanged. Rail 80px wide, buttons 44 × 44 starting at `x = 17.5` with 10px
  between them, glyph 24 × 24 at `x = 27.5`. A song row's mark 20 × 20 at `x = row + 24`, its title at
  `x = row + 64`; a media chip 42 × 42 at `x = row + 13`, its glyph 23 × 23 inside it.
- **The four proposed marks** (each drawn on the rail's own 24-unit grid, stroke 1.7, round caps and
  joins):
  - **Alkitab — closed book, Latin cross.** Body `5,4.4 → 18.8,20.8` (r 1.8), spine rule at `x = 8`,
    cross bar `11.2 → 15.2` at `y = 9.5`, stem `y = 7.1 → 13.5`. The cross's lower arm is 4 units and
    its upper 2.4, so it reads as a cross and not a plus.
  - **Tata Ibadah — clipboard.** Board `4.6,3.4 → 19.4,20.6` (r 2), clip `8.6,1.9 → 15.4,5.3` (r 1.4),
    rules at `y = 9.6`, `13`, `16.4` (the third 4.8 units shorter).
  - **Kidung and a song entry — the beamed pair** already in `base.html:103-108` and `entries.js:66`,
    drawn at 24px in the rail and 20px on the stage.
  - **Audio media — waveform.** Five bars on the chip's centre line, `y` extents `10–14`, `7.2–16.8`,
    `4.6–19.4`, `7.6–16.9`, `10.2–13.8` at `x = 4.2, 7.6, 11, 14.4, 17.8`.
- **Size / spacing**: the marks are the only thing that changes; every box in the table above is the
  shipped one. The empty stage's four add tiles keep their 24px glyphs.
- **Colour / typography**: rail marks `currentColor` (the button's own ink, `--active-ink` when
  current or expanded); a song's kind mark `--head-ink`; the audio chip's glyph `--focus` on the 12%
  tint. No new token, no fill, no second ink.
- **States**: each rail button's rest, hover (`--icon-hover-bg`), focus-visible (2px `--focus` at 3px
  offset) and current/expanded fill must be seen with the new marks — the tooltip is unchanged. The
  song mark must be seen on a row at rest, under hover, and with a modal open; the audio chip must be
  seen in its available, missing (`--danger`) and unavailable states.
- **Motion**: none. The marks are static markup; the rail's existing transitions are untouched.
- **Responsive**: at ≤1272px the rail is 64px and the buttons 40px (`tokens.css:116`), so the marks
  draw at 20px; below 720px they sit beside the section names in the menu drawer. Both are reachable
  by resizing the preview.

## Assumptions

- **The Bible is a closed book; a passage stays an open one.** The rail names the whole Bible — an
  object — while a stage row names one passage inside it. A closed book with a cross is also the one
  silhouette that cannot be confused with the passage mark sitting a few hundred pixels to its right.
  The preview's second option (an open book with a cross above it) is the alternative if the owner
  prefers the rail to keep the open-book family.
- **A Latin cross, not a plus.** An equal-armed cross reads as "add" at 24px; the stem is 6.4 units
  against a 4-unit bar, and its lower arm is the longer one.
- **The clipboard, not the ordered-steps list.** Both stop reading as a file; the clipboard is the
  only one of the two that is a *container of lines*, matching what the destination holds. The steps
  alternative stays in the preview.
- **The song keeps the beamed pair, and the audio file moves.** The pair is already the rail's mark and
  the Add Song tile's mark; moving the row to it makes three places agree with one file. Changing the
  song's shape instead would leave the rail and the add tile to be rewritten as well — more surfaces
  moved for the same result. A waveform is also the more literal mark for a *file* than for a hymn.
- **The audio mark changes everywhere it is drawn.** The stage chip, the Media Library list, the
  service-media dialog and the upload preview all call `window.gkpsMediaIcon`; leaving one of them on
  the old path would put the collision back on that surface.
- **Only paths change.** No template is restructured, no CSS box moves, no JavaScript behaviour
  changes, no API or model changes, and the rail keeps five destinations.
- **The Media Library and Search marks are out of scope**, though the folder mark is the weakest of the
  five at 24px; changing it is a second request.
- **No icon font.** The marks stay inline SVG in the templates (the rail) and in the JS map (media
  families), as today — the repo bundles no icon sprite for these.

## Clarifications

### Session 2026-10-29

- **The three marks are chosen from the preview, not from prose.** The owner's answer picks, per slot,
  between the proposal and its alternative; the answer is recorded here and the losing option stays in
  the preview.
- `[NEEDS CLARIFICATION: Alkitab — closed book with a Latin cross, or open book with a cross above it?]`
- `[NEEDS CLARIFICATION: Tata Ibadah — clipboard, or the ordered-steps list?]`
- `[NEEDS CLARIFICATION: Kidung and a song entry — the beamed pair everywhere (audio moves to a
  waveform), or the single note everywhere (audio still moves)?]`
