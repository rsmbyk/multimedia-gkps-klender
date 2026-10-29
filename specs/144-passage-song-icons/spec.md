# Feature Specification: a passage and a song carry their own kind mark

**Slice**: `specs/144-passage-song-icons`
**Branch**: `feat/144-passage-song-icons`
**Created**: 2026-10-28
**Status**: Draft
**Input**: "i want you to add some kind of icons for passage and songs just like the media entries, but make it kind of different so that you can distinguish between media and passage/songs entries." — owner, with a screenshot of `/tatib/144/`

## What the page does today

On the Tata Ibadah stage only a media row is marked. It draws a **42 × 42px** chip at its left edge —
`--focus` at 12% over the canvas, a 23px stroke glyph inside — and its row is **80px** tall because
the chip sits inside the flow, with the title pushed to `x = 1030` (item `x = 966`, `padding-left:
64px`).

A passage row and a song row have no mark at all. They are **56px** boxes with `padding-left: 12px`,
so the title's first line starts at `x = 978` — 52px to the left of where a media title starts, and
nothing at the row's left edge but the palette. Their only kind signals are words: the reference
("Kisah Para Rasul 1:1"), the hymn number ("HAL 1 — …"), and a song's "Bait 1-7" second line.

| measured on `/tatib/144/` at 1440×900 (pane 400px) | value |
| --- | --- |
| a passage / song row | **420 × 56px**, title at `x = 978`, first line `23.8px` tall |
| a media row | **420 × 80px**, chip at `x = 979` `42 × 42px`, title at `x = 1030` |
| room left of a passage/song title inside the row | **12px** (the row's own padding) |
| the entry's own left margin | `-10px` — there is no gutter to hang a mark in |

## User Scenarios & Testing

### US1 — A passage and a song are recognisable without reading (P1)

**Why this priority**: this is the request. The stage is read at a glance while a service runs; the
kind of a row should be known before its words are.

**Independent Test**: with the change applied, the passage row and the song row each paint a glyph
at their left edge, and the glyph differs between the two kinds.

**Acceptance scenarios**

1. **Given** a service with a passage entry, **When** the stage is drawn, **Then** the row paints a
   passage glyph at its left edge.
2. **Given** a service with a song entry, **When** the stage is drawn, **Then** the row paints a song
   glyph — a different mark from the passage's.
3. **Given** a passage and a song beside each other, **When** the stage is scanned, **Then** the two
   marks are told apart without reading either title.

### US2 — A media file is never mistaken for a passage or a song (P1)

**Why this priority**: the request names it — the mark has to be *different* from the media chip,
not a smaller copy of it.

**Independent Test**: a media row, a passage row and a song row side by side in one service; the
media row's mark and the passage/song mark differ in at least size and one other property (fill,
colour or container) at the 400px pane.

**Acceptance scenarios**

1. **Given** a media row and a passage row adjacent, **When** the stage is scanned, **Then** the
   media chip reads as the heavier, tinted mark and the passage mark as the quieter one.
2. **Given** a song row, **When** its mark is compared with an audio media chip, **Then** the two are
   distinguishable by more than the glyph's outline.

### US3 — The stage keeps its rhythm and its text column (P2)

**Why this priority**: specs 055/140/143 fixed the stage's geometry as a contract — 56px boxes,
words centred, controls in their own column. A mark that changes the row's height or moves the title
off its line breaks those contracts.

**Independent Test**: measure a passage row's height and its title's first-line position before and
after the change, and the same for a media row, the add rows and the service head.

**Acceptance scenarios**

1. **Given** a passage row, **When** the mark is drawn, **Then** the row's box stays 56px and its
   title's first line stays on the row's centre line.
2. **Given** a song row with a `Bait` line, **When** the mark is drawn, **Then** the row grows only by
   whatever the reduced title column wraps — and this slice declares exactly which titles wrap at the
   400px pane, with the pixel count, rather than claiming nothing moves.
3. **Given** the mark, **When** the row is hovered or focused, **Then** the mark stays legible on the
   hover fill.
4. **Given** `prefers-reduced-motion`, **When** the row is drawn, **Then** nothing is animated.

### Edge Cases

- **When** the reading pane is 400px — a 1440px window with both sidebars open — **Then** the mark
  and the title both fit, and the title's column still shows its words without running under the
  controls' column.
- **When** a song's title is a long unbroken run, **Then** the mark does not narrow the title's wrap
  box below what `test_text_wrap` requires.
- **When** an entry's target was deleted (`is-deleted-target`), **Then** the row still paints its
  kind mark; the mark states the kind, not the availability.
- **When** the mark's kind is a text entry, **Then** see FR-004 — the request names passage and song
  only.
- **When** a text entry sits between two marked rows, **Then** its own text stays on the row's 12px
  edge — the stage shows two text columns by design (FR-004).

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | A passage row on the stage SHALL paint a passage mark at its left edge. | `new: reading` |
| FR-002 | A song row on the stage SHALL paint a song mark at its left edge, different from the passage mark. | `new: reading` |
| FR-003 | The passage/song mark SHALL be distinguishable from the media chip by at least its size and one of fill, colour or container shape. | `new: reading` |
| FR-004 | A text entry SHALL NOT be marked: the request names passage and song, and a text entry's own body stays on the row's 12px edge. *(Recorded assumption — reopen if a text row should carry a mark too.)* | `new: reading` |
| FR-005 | The marking SHALL NOT add height of its own: a passage row's box stays 56px and no other block moves. A song row MAY grow only where the narrower title column wraps its title, and that set is declared with its measured cost. | `new: reading` |
| FR-006 | The mark SHALL be `aria-hidden`, because the row already states its kind in words and its title is its link. | `new: reading` |
| FR-007 | The mark SHALL remain legible on the hover fill, in both themes, at the contrast the stage's other meta text holds. | `new: reading` |
| FR-008 | The mark SHALL NOT be painted on the sidebar's service list or on the OBS dock's entry list — those surfaces keep their own anatomy. | `new: reading` |

### Key Entities

- **Kind mark** — an inline, decorative glyph at a passage or song row's left edge; server-rendered
  from the entry's kind, so it is present without JavaScript.
- **Media chip** — the existing `.entry__media-icon`: 42px, `--focus` at 12%, injected glyph.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | Passage and song rows are marked | on `/tatib/144/`: the passage row and the three song rows each carry the mark element; a text row and the section break do not |
| SC-002 | The marks differ from the media chip | computed size, background and colour of the mark vs `.entry__media-icon` on the same page |
| SC-003 | Nothing moves | every `.tatib__item`'s top and the page's scroll height, before and after |
| SC-004 | The row keeps its box | a passage row measures **56px**; a song row measures its title's lines × 23.8 + the `Bait` block, unchanged by the mark itself; a media row **80px** |
| SC-005 | The glyph is reachable-free | the mark is `aria-hidden="true"` and the row's accessible name is unchanged |

## UI/UX

Measured in headless Chromium against the real stylesheets, on the static preview
(`specs/144-passage-song-icons/preview/preview.html`) at the 400px reading pane a 1440px window
produces, and on the live slice server.

**Adopted: A, with the mark and the title on the media row's own columns.** A passage or song row
puts its 20px glyph where the media chip sits — centre **34px** from the row's left edge, i.e.
`left: calc(13px + (42px - 20px) / 2)` — and its title on the media title's column, **64px**, so a
media row, a passage row and a song row all share one left rail: mark centred on x = 34, words from
x = 64.

| | mark | mark centre | title starts at | title column | passage row | song row (`Bait 1-7`) | song row (`HAL 7`) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Now** | none | — | **32px** | **302px** | 56px | 62.5px | 62.5px |
| **A · adopted** | **20 × 20** at x = 44, centred on the row | 54px | **84px** | **250px** | 56px | 86.3px | 86.3px |
| *(B · glyph on the title)* | 20 × 20 at x = 32, first line, 30px hanging indent | 42px | 62px | 272px | 56px | 62.5px | 86.3px |
| *(C · outline chip)* | 30 × 30 at x = 33, 1px ring, no fill | 48px | 75px | 259px | 56px | 86.3px | 86.3px |
| *(D · tinted chip)* | 30 × 30 at x = 33, `--head-ink` at 9% | 48px | 75px | 259px | 56px | 86.3px | 86.3px |

Coordinates are the preview page's own (a 420px row), where **the media chip runs x = 33…75, its
centre 54, and a media title starts at x = 84** — the same 64px column A gives a passage or song.

- **Size**: the mark is **20 × 20px**, the media chip **42 × 42px**, so the chip is 2.1× the mark's
  box at the same seat. The glyph is drawn in the media chip's own stroke language: 24 viewBox,
  1.8 stroke, round caps.
- **Vertical**: centred on the row, like the chip. On a row with a `Bait` line the mark therefore
  sits between the title and the verse line — measured **11px below** the title's first line.
- **The cost, stated plainly:** the title column drops from **302px to 250px** — the media title's
  own column. `HAL 7 — Porini Dong Marribu Hali` measures **295.6px** on one line and
  `HAL 1 — Jahowa Sihol Pujionku` **270.9px**, so **all four songs in `/tatib/144/` wrap onto a
  second title line at this pane: +23.8px each, +95.2px of stage.** At a 1920px window the pane is
  880px and no title wraps. A text row is untouched: its body keeps the 12px edge (FR-004).
- **Colour**: `--head-ink` — **5.57:1** on `--canvas` light, **6.59:1** dark, **4.77:1** / **5.23:1**
  on the hover fill. The media chip's `--focus` glyph is **6.08:1** / **5.89:1** on its own tint, so
  the media chip stays the heavier mark of the two.
- **States**: at rest; `--icon-hover-bg`; `is-modal-origin`; both themes; keyboard focus on the
  title's own link (the mark is not focusable and takes no pointer).
- **Motion**: none.
- **Coupling to avoid:** the mark must not become the section's first child — `.tatib__item--acts >
  :first-child { margin-top: 0 }` is what flattens the title's 30px pericope margin, and a mark in
  that seat gave it back (measured: the row grew 56px → 69.8px). The mark rides inside the heading.

## Assumptions

- **The stage is the surface.** The ask came from a screenshot of the stage; the sidebar's service
  list and the OBS dock's entry list keep their own row anatomy (FR-008).
- **A mark states the kind, not the availability.** A deleted-target song still shows its song mark.
- **Server-rendered, not script-injected.** The media chip's glyph script exists because the media
  family is a client-side fact; a passage or song's kind is known when the page is drawn.
- **No new asset.** The marks are inline SVGs in the existing stroke language (24 viewBox, 1.8
  stroke, round caps) — the language `.entry__media-icon svg` and the entry controls already use.
- **One left rail, not two.** The mark sits on the media chip's centre line and the title on the
  media title's column, so a file, a passage and a song share the stage's left edge. The cost is the
  title's width (302px → 250px) and the wraps listed under UI/UX.
- **A text row keeps its own edge.** Only passage and song are marked, so a text row's body still
  starts at 12px. The stage therefore shows two text columns; that is the request read literally,
  not an oversight.

## Clarifications

### Session 2026-10-28

- Q: Which mark should a passage and a song carry? → A: **the bare 20px glyph (candidate A), but the
  glyph horizontally centred on the media icons and the title aligned with the media entries'
  title/filename column** (owner, 2026-10-28). Candidates B/C/D were shown and not taken.
- Q: Should a text entry carry a mark too? → **not asked; recorded as FR-004's assumption** (the
  request names passage and song). Reopening it is a revision at Specify, not a defect.
- **Retracted, 2026-10-28:** this slice first wrote FR-005 as "the marking SHALL NOT change a row's
  height". Measuring killed it: `HAL 7 — Porini Dong Marribu Hali` is **295.6px** on one line and the
  media column is **250px**, so every song in `/tatib/144/` gains a line. The requirement now claims only
  that the mark adds no height of its own, and the wraps are declared with their cost.
