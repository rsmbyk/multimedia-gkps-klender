# Feature Specification: the rail says what each section is, and its marks are the stage's own

**Slice**: `specs/151-rail-icons`
**Branch**: `feat/151-rail-icons`
**Created**: 2026-10-29
**Status**: Draft — clarified 2026-10-29
**Input**: "can you find a better icons to represent Bible, Songs, and Service Order? … first, the bible
is represented as plain book today. maybe you can find something that can instantly tell people that it
is bible. second, the service order icon looks like a file/document instead and people might think that
it is a file manage or something. third, the icons used to represent medias should not be used for the
main rail to distinguish it (the songs main rail and songs media use the same icons). The icon for main
rail and service entry of type songs should have the same icons. either change the icons for audio files
or find another icon for Kidung main rail and service entry songs." — owner, with the answer "open +
cross, beamed pair, waveform. also use the same icon for passage entry."

## What the page does today

The main rail (`multimedia/web/templates/reading/base.html:64`) is an **80px** strip of **44 × 44px**
buttons, each holding one **24 × 24px** stroke glyph at `stroke-width: 1.7`
(`static/styles/design/components.css:145-166`, `static/styles/design/tokens.css:15-17`). Five
destinations: Search, Alkitab/Bibel, Kidung/Doding, Tata Ibadah/Agenda, Media Library.

| Destination | Mark today | Source |
| --- | --- | --- |
| Alkitab / Bibel | an **open book** — two page halves and a gutter | `base.html:88-92` |
| Kidung / Doding | a **beamed pair of eighth notes** | `base.html:103-108` |
| Tata Ibadah / Agenda | a rounded page with three rule lines — a **document** | `base.html:119-123` |
| Media Library | a folder | `base.html:127` |
| Search | a magnifier | `base.html:75-78` |

Four facts sit behind the report.

1. **The Bible carries no Bible's own sign.** The rail's Alkitab mark is an open book and nothing else.
   The product draws *two different* open books, in four copies: the rail's (`base.html:88-92`), the
   Alkitab panel's empty state (`base.html:256-261`) and the empty stage's Add Passage tile
   (`tatib.html:198-202`, `entries.js:65`) share one drawing (`M12 6.6S10.1 4.2 …`), while a stage
   passage's kind mark uses the other (`_entry_kind_icon.html`, `M12 6.6C10.3 5.2 …`). None of them is
   a Bible.
2. **The service order's mark is a document.** A rounded page with three rule lines is the shape the
   product also uses for a PDF (`media-stage.js:8`), so the rail competes with its own media family —
   and the report reads it as a file manager.
3. **Kidung and an audio file are the same mark.** `media-stage.js:6` draws the audio family as
   `M9 18V5l11-2v13` with two 3px noteheads; the rail's Kidung is `M9 17.4V5.6l10.2-2v11.6` with two
   2.4px noteheads. The same beamed pair, within a unit on every coordinate — told apart by its 42px
   tinted chip, not by its shape. `window.gkpsMediaIcon` draws that glyph in the Media Library list,
   the service-media dialog and the upload preview too.
4. **A song row's mark is not the rail's.** Spec 144 gave a song row a *single flagged note*
   (`_entry_kind_icon.html`; R25: "a single flagged note for a song"), while the rail **and** the Add
   Song tile (`entries.js:66`) draw the beamed pair. One screen shows two note shapes for one thing.

Measured on `/tatib/144/` at 1440×900: rail 80px wide, each button 44 × 44 at `x = 17.5`, each glyph
24 × 24 at `x = 27.5`; a song row's kind mark 20 × 20 at `x = 990` on a row starting at `x = 966`
(+24), its title at `x = 1030` (+64); a media row's chip 42 × 42 at `x = 979` (+13) with a 23 × 23
glyph inside it.

## User Scenarios & Testing

### US1 — A Bible reads as a Bible, in the rail and on the stage (P1)

**Why this priority**: this is the first and third asks. The rail is the only permanent label the
product has, and the owner's answer makes the stage's passage mark part of the same decision: one
Bible mark, drawn wherever scripture is drawn.

**Independent Test**: open any reading page at 1440px, look at the rail's second button without reading
its tooltip; then open a Tata Ibadah stage holding a passage and compare the two marks.

**Acceptance scenarios**

1. **Given** any reading page, **When** the rail draws, **Then** the Alkitab/Bibel button paints an
   open book with a Latin cross above it.
2. **Given** a Tata Ibadah stage holding a passage, **When** its row draws, **Then** the row's 20px
   kind mark is the same path as the rail's mark, and the cross is still legible at 20px.
3. **Given** an empty Tata Ibadah stage, **When** the Add Passage tile draws, **Then** it draws the
   same path again, at its 24px tile size.
4. **Given** the same page in the dark theme, **When** the marks draw, **Then** the cross is legible
   and each mark keeps one ink.

### US2 — A service order is not a file (P1)

**Why this priority**: the report says the mark reads like a file manager; a page-with-lines is also
the product's PDF.

**Independent Test**: at 1440px, compare the rail's Tata Ibadah mark with the PDF chip on a stage; the
two must not share a silhouette.

**Acceptance scenarios**

1. **Given** any reading page, **When** the rail draws, **Then** the Tata Ibadah/Agenda button paints a
   clipboard: a board, a clip above it, three rule lines.
2. **Given** a Tata Ibadah stage holding a PDF, **When** both are on screen, **Then** the rail's
   clipboard and the PDF's page are told apart without reading either.

### US3 — A song is one mark, wherever it is drawn (P1)

**Why this priority**: the report names the contradiction directly — the rail and a song entry must
agree, and a media file must stop borrowing the song's shape.

**Independent Test**: on one screen, find the rail's Kidung mark, a song row's mark and the Add Song
tile; all three draw the same path. Then compare a song row with an audio media row: different shapes.

**Acceptance scenarios**

1. **Given** a Tata Ibadah stage with a song entry, **When** it draws, **Then** the row's 20px mark is
   the rail's Kidung path.
2. **Given** an empty stage, **When** the Add Song tile draws, **Then** it draws the same path.
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
2. **Given** a Tata Ibadah stage, **When** a song or passage row draws, **Then** its mark is 20 × 20 on
   the media chip's centre line and its title still starts at the media title's column.
3. **Given** the rail's hover, focus, current and expanded states, **When** a button is pointed at or
   is current, **Then** the mark paints in the same ink as today's mark on the same element.

### Edge Cases

- **When** the window is narrower than 1272px and the rail is 64px with 40px buttons
  (`tokens.css:116`) **Then** the marks draw at 20px and keep their proportions; the kind mark stays
  20px.
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
- **When** a passage row's mark is drawn at 20px **Then** the cross still resolves — the mark keeps
  its 20px box and its 3.8-unit cross bar, which the preview shows legible at 4×.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | The rail's Alkitab/Bibel destination, and the Alkitab panel's own empty state, SHALL draw an open book with a Latin cross above it. | `new: reading` → R27 |
| FR-002 | A passage entry's kind mark and the empty stage's Add Passage tile SHALL draw the same path as FR-001 — the rail's mark at 20px on the row and 24px on the tile — and no other open book SHALL remain in the product. | `modified: reading` → R25 |
| FR-003 | The rail's Tata Ibadah/Agenda destination, and that panel's own empty state, SHALL draw a clipboard — board, clip above it, three rule lines — and SHALL NOT draw a page, folder or document silhouette. | `new: reading` → R27 |
| FR-004 | The rail's Kidung/Doding destination, a song entry's kind mark and the empty stage's Add Song tile SHALL draw one and the same beamed-pair path. | `modified: reading` → R25 |
| FR-005 | An audio media file's family mark SHALL be a waveform of five rounded bars, in every place that mark is drawn: stage chip, Media Library list, service-media dialog, upload preview. | `new: reading` → R27 |
| FR-006 | The image, video, PDF and PowerPoint family marks, and the `missing` fallback, SHALL NOT change. | `new: reading` → R27 |
| FR-007 | Every mark SHALL keep today's box: a rail glyph 24 × 24 inside its 44 × 44 button; a stage kind mark 20 × 20 at the media chip's centre line with the title on the 64px column; a media chip 42 × 42 with a 23 × 23 glyph; the empty stage's tiles 24px. No row's height, padding or title column SHALL change. | `modified: reading` → R25 |
| FR-008 | Every mark SHALL be inline SVG painted with `currentColor`, carry no new colour token or tint, keep `aria-hidden="true"`, and add no pointer target. | `new: reading` → R27 |
| FR-009 | The rail SHALL keep five destinations and their order; the Search and Media Library marks SHALL NOT change. | `new: reading` → R27 |

### Key Entities

- **Rail mark** — one of five decorative glyphs in the rail template, identified by its destination
  (`Search`, `Alkitab`, `Kidung`, `Tata Ibadah`, `Media Library`). Not data: the same markup on every
  page.
- **Kind mark** — the 20px glyph a stage row draws for `scripture` or `song` (spec 144). This slice
  changes both paths: `scripture` becomes the rail's Bible, `song` becomes the rail's note.
- **Add tile** — one of the empty stage's four square buttons (`tatib.html:198-213` and
  `entries.js` `EMPTY_ADD_ICONS`). Two of them, Passage and Song, take the rail's marks.
- **Media family mark** — the glyph `window.gkpsMediaIcon(family)` returns for `image`, `audio`,
  `video`, `pdf`, `slides`, and the `missing` fallback. This slice changes the `audio` path only.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | The rail's five marks are five distinct path sets, and none of them appears in the media family map. | E2E: read `d` attributes from each rail button and from `window.gkpsMediaIcon` for the five families plus `missing`; assert no intersection. |
| SC-002 | Two pairs are string-identical: the Alkitab rail path = the passage kind mark = the Add Passage tile, and the Kidung rail path = the song kind mark = the Add Song tile. | E2E: compare the three `d` strings in each pair. |
| SC-003 | Rail buttons are 44 × 44 with 24 × 24 glyphs; a stage kind mark is 20 × 20 at row + 24 and the title at row + 64; a media chip is 42 × 42 with a 23 × 23 glyph; row minimum heights stay 56px and 80px. | E2E: `getBoundingClientRect()` on the same nodes as §What the page does today. |
| SC-004 | A song row and an audio media row on one stage draw different silhouettes at 20px and 23px. | manual: the preview's stage column and the live page, at 1:1 |
| SC-005 | Both themes paint every mark with the same computed colour as today's mark on the same element (`--ink`, `--head-ink`, `--focus` — no new token). | E2E: computed `color` on each mark in both themes, compared with `24a6d6d2` |

## UI/UX

**Static preview at `specs/151-rail-icons/preview/preview.html`** (regenerate with `build_preview.py`).
Two 502px columns — an 80px rail beside a 420px stage — built from the live page's own rail and
`<article class="read">` at `/tatib/144/`, with the stylesheets frozen at `24a6d6d2`. **Now** is the
shipped state; **Proposed** is this spec. The bar switches each mark to its alternative, and **Dark**
flips the theme, so every candidate in §Clarifications is reachable by hand.

- **Layout / position**: unchanged. Rail 80px wide, buttons 44 × 44 starting at `x = 17.5` with 10px
  between them, glyph 24 × 24 at `x = 27.5`. A stage kind mark 20 × 20 at `x = row + 24`, the title at
  `x = row + 64`; a media chip 42 × 42 at `x = row + 13`, its glyph 23 × 23 inside it.
- **The marks** (each on the rail's own 24-unit grid, stroke 1.7, round caps and joins):
  - **Alkitab, and a passage** — open book, cross above. Book `12,9.6` at the gutter; covers to
    `x = 4.7 / 19.3`, `y = 7.9 → 20`; cross stem `y = 2.6 → 7.2` at `x = 12`, bar `4.6` wide at
    `y = 4.5`. The stem's lower arm is 2.7 units against a 1.9-unit upper, so it reads as a cross and
    not a plus. Drawn at 24px in the rail, 20px on a row, 24px on the Add Passage tile.
  - **Kidung, and a song** — the beamed pair already in `base.html:103-108` and `entries.js:66`,
    24px in the rail, 20px on a row, 24px on the Add Song tile.
  - **Tata Ibadah** — clipboard. Board `4.6,3.4 → 19.4,20.6` (r 2), clip `8.6,1.9 → 15.4,5.3` (r 1.4),
    rules at `y = 9.6`, `13`, `16.4` (the third 4.8 units shorter). 24px.
  - **Audio media** — waveform. Five bars at `x = 3.6, 7.2, 10.8, 14.4, 18`, `y` extents `10.2–13.8`,
    `7.2–16.8`, `4.4–19.6`, `7.2–16.8`, `10.2–13.8` — the outer bars short, the middle one full height,
    so the mark fills the chip the way the other four families do. 23px in the chip.
- **Size / spacing**: the marks are the only thing that changes; every box in the table above is the
  shipped one. The stage's `Add Text` and `Add Media` tiles keep their own glyphs.
- **Colour / typography**: rail marks `currentColor` (the button's own ink, `--active-ink` when
  current or expanded); a stage kind mark `--head-ink`; the audio chip's glyph `--focus` on the 12%
  tint. No new token, no fill, no second ink.
- **States**: each rail button's rest, hover (`--icon-hover-bg`), focus-visible (2px `--focus` at 3px
  offset) and current/expanded fill must be seen with the new marks — the tooltip is unchanged. A kind
  mark must be seen on a row at rest, under hover, and with a modal open; the audio chip must be seen
  in its available, missing (`--danger`) and unavailable states; the empty stage's four tiles must be
  seen in both themes.
- **Motion**: none. The marks are static markup; the rail's existing transitions are untouched.
- **Responsive**: at ≤1272px the rail is 64px and the buttons 40px (`tokens.css:116`), so the marks
  draw at 20px; below 720px they sit beside the section names in the menu drawer. Both are reachable
  by resizing the preview.

## Assumptions

- **One mark per kind, at two sizes.** The owner's answer — "also use the same icon for passage entry"
  — makes the rail's mark and the stage's kind mark one drawing, as it already is for Kidung. The
  three open books in the product collapse to one, and the Add Passage tile joins it; the Add Song
  tile follows the same rule.
- **The Bible mark is an open book with a cross above it** (owner decision, from the preview's
  alternatives). The closed book with a Latin cross was the other candidate and is rejected because
  the owner wants the passage's own mark to be the Bible's mark, and a closed book cannot also be an
  open one.
- **The cross is a Latin cross, not a plus**: a 3.8-unit bar on a 4.6-unit stem, 1.9 units above the
  bar and 2.7 below. At 20px on a row the cross resolves — the preview's 4× view of the row shows four
  countable arms — so the mark's 20px box is kept rather than enlarged.
- **The song keeps the beamed pair, and the audio file moves** (owner decision). The pair is already
  the rail's mark and the Add Song tile's mark; moving the row to it makes three places agree. A
  waveform is also the more literal mark for a *file* than for a hymn.
- **The clipboard, not the ordered-steps list** (owner left this slot on the proposal). Both stop
  reading as a file; the clipboard is the one that is a *container of lines*, matching what the
  destination holds. The steps alternative stays in the preview.
- **The audio mark changes everywhere it is drawn.** The stage chip, the Media Library list, the
  service-media dialog and the upload preview all call `window.gkpsMediaIcon`; leaving one on the old
  path would put the collision back on that surface.
- **Only paths change.** No template is restructured, no CSS box moves, no JavaScript behaviour
  changes, no API or model changes, and the rail keeps five destinations.
- **The Media Library and Search marks are out of scope**, though the folder mark is the weakest of the
  five at 24px; changing it is a second request.
- **No icon font.** The marks stay inline SVG in the templates (the rail, the kind mark, the tiles) and
  in the JS map (media families), as today.

## Clarifications

### Session 2026-10-29

- **Alkitab** — the owner chose the **open book with a cross above it** over the closed book, and added:
  *"also use the same icon for passage entry."* FR-001 and FR-002 carry that as one drawing in three
  places. The closed book stays in the preview as the rejected alternative, and the passage mark it
  implied (a plain open book, unchanged) with it.
- **Kidung and a song** — the owner chose the **beamed pair everywhere**; the audio family moves to the
  waveform. The single-note alternative stays in the preview.
- **Audio media** — the owner chose the **waveform**; the speaker alternative stays in the preview.
- **Tata Ibadah** — not answered; the proposal stands (clipboard), recorded under Assumptions, and the
  steps alternative stays in the preview.

Zero `[NEEDS CLARIFICATION]` markers remain.
