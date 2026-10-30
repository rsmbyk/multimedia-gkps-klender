# Feature Specification: the overlay reads by kind — a song stays a caption, a passage and a text wear a plate

**Slice**: `specs/180-overlay-text-styles`
**Branch**: `feat/180-overlay-text-styles`
**Created**: 2026-10-30
**Status**: Accepted
**Input**: "i want you to add different styles for passage and texts in obs source overlay page. as you can see,
currently obs source overlay use a subtitle/captions style to display all the texts. that suits the songs as it is
actually displaying lyrics of the songs. but for passage and liturgies, that does not suitable. maybe add some
background to it to also incorporate some headings for the bible references or title"

## What the overlay paints today

Measured on the live page from this worktree at 1920×1080, service 144 (25 Oct 2026):

- **One style for everything.** Every text-bearing screen paints `.obs-overlay__caption`: 1728×202 px at (96, 824),
  Source Sans 3 **800 at 72 px** (`clamp(11px, 3.75cqw, 80px)` resolved at this width), line-height 1.4, white with
  the eight-way black outline, 5 % insets, no plate (`static/styles/design/obs-overlay.css`).
- **The heading is thrown away.** `linesOf()` (`static/web/obs-overlay.js`) returns `screen.lines` only, so a
  passage screen's `header` — `"Kisah Para Rasul 1:1\nRoh Kudus dijanjikan"` — and a text screen's `header` (the
  entry's title) never reach the stream. A lyric and a scripture reading are painted identically.
- **What a screen already carries.** `header` (the reference plus the verse's own title for a passage, the entry's
  title for a text), `lines[].voice` (`leader` · `assembly` · `join`, which the current renderer drops), and
  `entry_index` into the projector's entry island (`type`: `song` · `passage` · `text` · `media` · `break`). The
  overlay already fetches that island's page; it simply does not read the entry list.

Measured on the content, 30 Oct 2026: **1320 of 2714** legacy text items carry a title, and both new-kind `TEXT`
entries carry none; one of those two keeps its section heading as its first body line
(`"VOTUM, INTROITUS, DOA"`). A plate therefore cannot assume a heading exists.

## User Scenarios & Testing

### US1 — A passage is a quotation: a centred card names the reference and the verse's title (P1)

**Why this priority**: a scripture reading is the screen where the current caption style fails hardest — the stream
shows a verse with no idea what is being read, and the reference the operator sees on the projector is lost.

**Independent Test**: project a `passage` entry on the live overlay and read its DOM: a plate with the reference as
its heading, the verse's own title under it, and the words beneath a hairline.

**Acceptance scenarios**

1. **Given** a passage screen for Matius 5:3 whose header is `"Matius 5:3\nKesembuhan pada hari Sabat"`, **When** it
   is on air, **Then** the stage paints `.obs-overlay__plate` with `.obs-overlay__kicker` `Matius 5:3`,
   `.obs-overlay__title` `Kesembuhan pada hari Sabat`, and the verse in `.obs-overlay__line`.
2. **Given** the same screen, **When** it is painted, **Then** no `.obs-overlay__caption` exists and the plate's
   background is the dark fill, not transparent.
3. **Given** a passage whose edition carries no verse title, **When** it is painted, **Then** the kicker stands
   alone and no empty title element or extra rule is emitted.

### US2 — A liturgy is a script: a left-aligned panel with its title and its speaker turns (P1)

**Why this priority**: the second half of the request. A liturgy is spoken, not sung or quoted — a leader's cue and
the congregation's answer are read aloud together, and a centred quotation card flattens that structure.

**Independent Test**: project a `TEXT` entry titled `Salam` with a leader line and an assembly line; the panel is
left-aligned with a bar on its leading edge, carries `Salam`, and the leader line is quieter than the assembly line.

**Acceptance scenarios**

1. **Given** a text screen whose header is `Salam`, **When** it is on air, **Then** the plate's kicker is `Salam`
   and each body line is `.obs-overlay__line` with `is-leader` · `is-assembly` · `is-join` carried from the screen.
2. **Given** a liturgy plate and a passage plate, **When** both are measured, **Then** the liturgy is left-aligned
   with a 3 px bar on its leading edge and an almost square corner, while the passage is centred with a rounded
   12.4 px corner and no bar.
3. **Given** a text screen with no header (the stored case today), **When** it is on air, **Then** the plate paints
   with no kicker, no title and no hairline — a fixed-width panel holding the turns only.
4. **Given** a text screen holding one short answer, **When** it is on air, **Then** the panel keeps its width
   instead of collapsing to a chip — the panel is the object, only the words change.
5. **Given** a leader line and an assembly line on one plate, **When** the inks are compared, **Then** the leader's
   composited ink is darker than the assembly's.
6. **Given** a speaker line long enough to wrap, **When** it is on air, **Then** its second row starts at the same x
   as the first row's words — under `Di dalam`, not under `L.` or the panel's edge.

### US3 — A song screen is untouched (P1)

**Why this priority**: the caption is the accepted style for lyrics, and this slice must not respecify it.

**Independent Test**: project a `song` entry; the caption paints at its current size and weight with no plate, no
heading, and no title line.

**Acceptance scenarios**

1. **Given** a song screen, **When** it is on air, **Then** the stage paints `.obs-overlay__caption` with two spans,
   weight 800, transparent background, its outline, and **no** `.obs-overlay__plate` or `.obs-overlay__kicker`.
2. **Given** a song entry titled `Ada Kuasa`, **When** it is on air, **Then** the stage does not contain that title.

### US4 — The translation flip rewrites the heading with the words (P2)

**Why this priority**: the flip is the one state where the heading and the words change together; a plate that only
re-reads the lines would keep a TB reference over SIM text.

**Independent Test**: with a passage live, flip the edition from the dock; the kicker changes to the other edition's
reference and the body to its verse.

**Acceptance scenarios**

1. **Given** a passage live in TB, **When** `T` flips the state to SIM, **Then** the kicker reads the SIM edition's
   reference and the body reads its verse text, with no stale element left from TB.

### US3 — A panel arrives and leaves instead of popping (P2)

**Why this priority**: the plate is a large, near-opaque object landing in a live video frame; appearing between two
frames reads on the stream as a fault, not as a caption.

**Independent Test**: blank the overlay, project a passage, and read the plate's animation: a 200 ms fade with a
10 px rise; blank again and read the exit: a 140 ms fade with a 6 px sink, after which the stage is empty.

**Acceptance scenarios**

1. **Given** an empty stage, **When** a passage or text screen goes on air, **Then** the plate enters over 180 ms —
   opacity 0 → 1 while rising `.5em` (18 px) and growing from 97.5 % into its place, on
   `cubic-bezier(.4, 0, .2, 1)`.
2. **Given** a plate on air, **When** the display blanks, hides or is released, **Then** the plate leaves over
   120 ms — opacity 1 → 0 while sinking `.22em` (7.92 px) and shrinking to 98.5 % — and the stage is empty
   afterwards.
3. **Given** a plate on air, **When** the next screen of the same entry arrives, **Then** the panel does not
   re-enter: only its words change, as a cut.
4. **Given** a machine asking for reduced motion, **When** a panel or a caption comes or goes, **Then** it paints
   and clears with no animation at all.
5. **Given** an empty stage, **When** a song screen goes on air, **Then** the caption enters the same way over
   180 ms — a shorter travel of its own, `.2em` (14.4 px at 72 px) — and leaves over 120 ms as it sinks `.12em`
   (8.6 px); stepping to the next lyric swaps the words without re-entering it.

### Edge Cases

- **When** the screen is blank, a section break, or a media payload **Then** the stage paints nothing (unchanged).
- **When** the dock hides or releases **Then** the stage is emptied (unchanged).
- **When** a text screen has no header **Then** the plate paints without a heading, not with an empty heading shell.
- **When** the entry island is missing or the screen's `entry_index` has no entry **Then** the screen keeps the
  caption, exactly as every screen painted before this slice.
- **When** a verse is long enough to wrap **Then** the plate grows upward and keeps its 5 % bottom inset; nothing is
  clipped or scrolled.
- **When** a screen holds one short line **Then** both panels keep a minimum width of 34 % of the frame rather
  than collapsing to a chip.
- **When** a verse or a liturgy turn is long **Then** the panel takes the frame's full 90 % measure before it
  grows taller — a 467-character verse is five rows (373 px) rather than six (423 px) at 78 %.
- **When** the translation variant exists but its `line` is empty **Then** the plate falls back to the screen's own
  lines.
- **When** the speaker mark is long (`Pelayan :`, `L+J :`) **Then** the wrapped rows still hang under the words: the
  mark's column is sized by the mark itself, not by a fixed indent.
- **When** a line carries no mark **Then** it paints as one plain paragraph, as it did before this slice.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | The overlay SHALL choose its text style from the kind of the entry holding the screen on air: `song` → the caption; `passage` and `text` → the plate; `media`, `break` and blank → nothing; an unknown or missing entry → the caption. | `new: overlay` |
| FR-002 | A song screen SHALL paint exactly the caption it paints today: 800 weight, the eight-way outline, transparent fill, 5 % insets, no plate and no heading. | `new: overlay` |
| FR-003 | A passage plate SHALL carry the screen's header as its heading: the first line as the kicker, any following line as the title, with a hairline between the heading and the words — and no heading shell at all when the header is empty. | `new: overlay` |
| FR-004 | A liturgy plate SHALL carry the entry's title as its kicker when the screen has one, and each body line SHALL carry the screen's voice — a leader line quieter than the assembly's, a joined line between the two. | `new: overlay` |
| FR-004a | A liturgy plate SHALL be its own object on the screen: left-aligned text, a bar on its leading edge and an almost square corner — not the passage's centred, rounded card. | `new: overlay` |
| FR-005 | The plate SHALL be a near-opaque dark card (fill `rgba(10, 12, 16, .88)`, 1 px `rgba(255,255,255,.12)` border) so white body text reads over a bright frame without the caption's outline. | `new: overlay` |
| FR-006 | The plate SHALL sit at the caption's 5 % left, right and bottom inset, hug its content between a 34 % minimum and a 90 % maximum of the frame width, and scale every size in container units of the stage. | `new: overlay` |
| FR-007 | When a passage carries a shown edition, the plate SHALL paint that edition's header as its heading and its line as the body. | `new: overlay` |
| FR-008 | Blank, media and section-break screens SHALL paint nothing, and `hide`/`release` SHALL empty the stage. | `new: overlay` |
| FR-009 | The overlay SHALL remain listen-only: the painted surface SHALL carry no control and no focusable element. | `new: overlay` |
| FR-011 | A plate SHALL enter over 180 ms (opacity 0 → 1, `translateY(.5em) scale(.975)` → none, `cubic-bezier(.4, 0, .2, 1)`) and leave over 120 ms (opacity 1 → 0, `translateY(0) scale(1)` → `.22em` / `98.5%`), and the stage SHALL be empty once the exit ends. A screen step within one entry SHALL NOT re-enter the panel, and a machine asking for reduced motion SHALL get a cut. | `new: overlay` |
| FR-013 | When consecutive screens of one entry are both panels, the panel SHALL keep its place and morph its box from the old measure to the new one over 180 ms — width and height on the shared curve, the words resolving inside it 110 ms in — rather than re-entering. Reduced motion SHALL snap. | `new: overlay` |
| FR-012 | A song caption SHALL enter over 180 ms (opacity 0 → 1, `translateY(.2em)` → 0) and leave over 120 ms (opacity 1 → 0, `translateY(0)` → `.12em`) on the same curve as the plate; a screen step within one song SHALL NOT re-enter it, and reduced motion SHALL get a cut. | `new: overlay` |
| FR-010 | A liturgy line that carries a speaker mark SHALL lay the mark in a column and the words beside it, so every wrapped row starts under the words — whatever the mark's width, `L.` or `Pelayan :` — and the marks on one screen SHALL share one column, sized by the widest of them, so every line's words begin on the same x. The screen data SHALL carry the mark and the words beside the full line the projector paints. | `new: overlay` |

### Key Entities

- **Screen** — what the projector shows for one step: `blank`, `header`, `lines[{text, voice}]`, `entry_index`,
  optional `translations{edition: {header, line}}`, and the song markers (`bait`, `split`, `split_total`).
- **Entry** — the service entry the screen belongs to: `type` (`song` · `passage` · `text` · `media` · `break`),
  `label`, `start`/`end`. The overlay reads it from the projector page's `projectorEntryData` island.
- **Display state** — `{service, screen, on, translation}` in `gkps-display`, unchanged.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | A song screen is pixel-for-pixel the caption it is today | live page at 1920×1080: 1728×202 at (96, 824), 72 px, weight 800, transparent fill |
| SC-002 | A passage's card is the one the preview shows | live page at 1920×1080: 1728×238 at (96, 788), body 36 px / 50.40 px line-height, 11.52 px radius |
| SC-002a | A liturgy's panel is the one the preview shows | at 1920×1080: 1555×201 at (182, 825) with a title, 1553×145 without; left-aligned, 3 px leading bar painted from `.105em`, 2.88 px radius |
| SC-003 | The heading reaches the stream | the plate's kicker and title text equal the screen header's lines, in order |
| SC-004 | The liturgy hierarchy survives | the leader line's ink composited over the plate is darker than the assembly line's |
| SC-005 | Nothing else changed on the surface | zero focusable elements; hide and release empty the stage; media and break screens paint nothing |
| SC-006 | The flip rewrites heading and words together | after `T`, the kicker names the other edition and the body is its verse |
| SC-007 | Text arrives and leaves without a pop | `animationstart` on the live page: `overlay-plate-in` / `overlay-caption-in` at 180 ms, `overlay-plate-out` / `overlay-caption-out` at 120 ms, stage empty after the exit; sampled at 60 fps the opacity ramps 0 → 1 over ~150 ms |

## UI/UX

**Motion, live**: `specs/180-overlay-text-styles/preview/overlay-motion.html` — the same markup and stylesheet as the
source, with the controller's own classes; press a state to watch the panel arrive or leave, at 1× (the product's
timing) or at ¼× / ⅛× for review, with a live readout of the opacity and offset per frame.

**Static preview**: `specs/180-overlay-text-styles/preview/overlay-preview.html` — the real classes and the repo's
own `obs-overlay.css` + bundled faces over a 1920×1080 frame from the church's own worship video. It is a navigable
viewer of **fifteen states** — a sidebar index grouped by kind, one frame on stage, ◀ ▶ / J K / Home / End / 1–9,
the position kept in the URL hash. Moving between states plays the panel's own motion: it leaves (120 ms) and the
next arrives (180 ms) when the object changes, and only the words swap when the kind does not. Each frame is labelled
with its measured rows, characters and heading: a titled short verse, a titled long verse, a reference-only passage, the longest verse in the database, a titled liturgy turn, an
untitled one (the stored case), a single answer, a joined line, a long leader turn, **two speakers and a joined line
on one screen**, **two speakers with long turns**, **a long joined line**, a two-line lyric, a one-line lyric, and
the nothing case. Every frame is laid out at 1920×1080 and only the paint is scaled, so container units
resolve at the real size.

**Sequence**: `specs/180-overlay-text-styles/preview/overlay-sequence.html` — twelve captures of the **real** page at
1920×1080, driven through service 144 by the dock's own verbs, in the order the panels come and go: the passage panel
(`screen 0`), the rest that clears it (`1`), media (`2`), a song caption (`4`), the song's rest (`18`), media (`19`),
the text panel (`20`), its answer (`21`), the text's rest (`84`), a song (`86`), and the two ways the words leave the
air — the dock's hide and the release. Its companion `preview/overlay-walkthrough.mp4` is that whole walk recorded at 1920×1080 — every
stop labelled, each panel's arrival and departure at the product's own pace — for the motion a still cannot show.

**Live preview**: `http://127.0.0.1:8816/obs/source/overlay` — `runserver` from this worktree against the compose
Postgres, driven from `/obs/dock`. The page is transparent (an OBS browser source), so it is judged over video in
OBS or over the injected frame the preview shows.

Numbers are from the live page at 1920×1080, service 144; the preview agrees to the pixel.

- **Layout / position**: both panels are absolute at `left/right/bottom: 5%` — 96 px sides at 1920, the caption's
  own inset — and centred by `margin-inline: auto`. They hug their content between `min-width: 34%` and
  `max-width: 90%`: the **passage card** is 1728×238 at (96, 788); the **liturgy panel** is 1555×201 at
  (182, 825) with a title, 1553×145 without one, and 653×83 at (634, 943) for a single answer. Both bottom out
  54 px above the frame.
- **Size / spacing**: the plate's own scale is `font-size: clamp(5.5px, 1.875cqw, 40px)` — **36 px** at 1920,
  exactly half the caption's 72 px — with line-height 1.4 (**50.40 px**). Passage padding `.42em .65em .44em` =
  15.12 / 23.40 / 15.84 px, radius `.32em` = **11.52 px**; liturgy padding `.42em .65em .44em 1.05em` = 15.12 /
  23.40 / 15.84 / 37.80 px, radius `.08em` = **2.88 px**, leading bar `.105em` = **3.78 px** (paints 3 px on a
  1080p device grid). Kicker `.5em` = **18 px**, weight 350 (the quietest layer), tracking `.12em`; title
  `.808em` = **29.09 px**, italic 400; body 1em = 36 px at 500; hairline 1 px, `.38em` = **13.68 px** above (the
  heading's breath) and `.54em` = **19.44 px** below; body line gap `.3em` = **10.80 px**. A line with a speaker
  mark is a two-column grid — the marks of that screen share one `max-content` column sized by the widest of them
  (`L.` = 29 px, `P + K:` = 94 px, `Pelayan :` = 155 px), the words take the rest, `.45em` = **16.20 px** apart —
  so every wrapped row, and every line, starts at the same words x.
- **Colour / typography**: fill `rgba(10, 12, 16, .88)` with a white sheen to 5 % at the top and 0 % by 42 %;
  border 1 px `rgba(255,255,255,.12)`; shadow `0 .62em 1.65em rgba(0,0,0,.42)`; body ink `#F6F7F5`; kicker
  `rgba(255,255,255,.76)`; title `rgba(255,255,255,.92)`; hairline `rgba(255,255,255,.22)`; liturgy leading bar
  `rgba(255,255,255,.78)`; a leader line `rgba(255,255,255,.381)`, a joined line `.8`. Face unchanged: Source Sans 3.
- **States**, all fifteen on the preview page: a passage with reference and verse title (1 row at 1048×188), a
  titled long verse (3 rows at 1728×288), a reference-only passage (2 rows at 1728×190), the database's longest
  verse (5 rows at 1728×342), a titled liturgy turn (2 rows at 1555×201), an untitled one (2 rows at 1553×145), a
  single answer (1 row at 653×83), a joined line (2 rows at 1728×134), a long leader turn (2 rows at 1728×190),
  two speakers and a joined line on one screen (3 rows at 1053×206), two speakers with long turns (5 rows at
  1728×296), a long joined line (4 rows at 1728×235), a two-line lyric (1728×202), a one-line lyric (1728×101),
  and nothing painted (blank, break, media, hidden, released). Hover, focus, active, disabled, loading: `n/a — the
  surface has no controls and paints from state alone`.
- **Motion**: the words are a cut; the objects are not. A **panel** appears when a passage or text screen with words
  goes on air — entering over **180 ms**, opacity 0 → 1 while rising `.5em` (18 px) and growing from 97.5 %,
  `cubic-bezier(.4, 0, .2, 1)` — and disappears on the rest that closes every entry, on a section break, on a media
  payload, and on `hide`/`release`, leaving over **120 ms** as it sinks `.22em` (7.92 px) and shrinks to 98.5 %.
  A **lyric caption** is an object too: it enters over **180 ms** with a shorter travel of its own — `.2em` (14.4 px at
  72 px) — and leaves over **120 ms** (`.12em`, 8.6 px) on the same clock and curve. Sampled at 60 fps either entrance
  is ~10 frames of interpolation, not a pop. No bounce, no overshoot, nothing at rest. A screen step inside one entry
  does not re-enter the object: a panel keeps its place and **morphs its box** from the old measure to the new one over
  180 ms — width and height on the same curve, the words resolving inside it after 110 ms, so nothing re-wraps while
  the card moves — and a caption simply swaps its words. `prefers-reduced-motion` gets the cut.
- **Responsive**: every size is a container unit of the stage, so a 1280×720 frame paints the same proportions
  (body 24 px, kicker 12 px, title 19.39 px, passage card ≤ 1152 px, bar 2 px); each panel's type scale hangs off
  one number.


## Assumptions

- **Two treatments, not one plate reskinned.** A passage is a quotation: a centred, rounded card that hugs its
  verse. A liturgy is a script: a fixed-width, left-aligned panel with a bar on its leading edge. The inks, face and
  type scale are shared so the surface still reads as one product. — owner decision, Clarify 2026-10-30, over the
  shared-plate recommendation.
- **The heading is the screen's `header`, never guessed from the body.** No title is promoted out of a body line
  (1320 of 2714 legacy text items carry one; the stored entries that don't show a plate without a heading). — a body
  line is content; stripping it into a heading would change what is read aloud.
- **Kickers are uppercased by the stylesheet** (`text-transform`), the DOM keeps the source string. — an uppercase
  reference is the convention; the markup stays copyable.
- **Voices are monochrome**, dimming the leader, rather than the projector's coloured voices. — a plate over video
  should not introduce a second colour language; the room's screen already carries the colours.
- **Songs are not touched**, not even to add the song number or bait. — the caption is the accepted lyric style.
- **Media screens still paint nothing** on the overlay. — spec 119's deliberate scope; this slice changes text only.
- **The plate hugs its content** between 34 % and 90 % width rather than taking a fixed width. — a fixed width either
  empties on a one-line answer or shrinks the type on a long verse; 90 % lets a long verse take the frame's measure
  before it grows taller.

## Clarifications

### Session 2026-10-30

- Q: Should a liturgy text and a passage share one plate treatment, or should each kind get its own distinct style?
  → A: each kind gets its own distinct style — the passage stays a centred quotation card, the liturgy becomes a
  left-aligned script panel with a leading bar.
_Open items:_ 0.
