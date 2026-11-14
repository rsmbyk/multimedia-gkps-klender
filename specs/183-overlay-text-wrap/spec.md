# Feature Specification: the overlay's text wraps inside the box that owns it

**Slice**: `specs/183-overlay-text-wrap`
**Branch**: `fix/183-overlay-text-wrap`
**Created**: 2026-11-02
**Status**: Accepted — gate 1 2026-11-02, re-presented after the owner widened the scope
**Input**: the owner's report, with a frame of `/obs/source/overlay` at 63404 — *"a long
word/text are overflowing instead of being wrapped"*. The frame shows a liturgy plate whose body
reads `a very`, then a run of `o`s painted across the whole frame, then `untitled text`. Asked how far
the fix should reach, the owner first answered *"only the plate's body lines"*, then, at gate 2,
widened it: **"do the word-break on the song captions and the panel's header/title as well"**.

## What the surfaces do today

`static/styles/design/obs-overlay.css` declares **no `overflow-wrap`** on `html`, `body`,
`.obs-overlay__stage`, `.obs-overlay__plate`, `.obs-overlay__line`, `.obs-overlay__kicker`,
`.obs-overlay__title`, `.obs-overlay__caption` or any of their children. A run with no space in it is
therefore painted at its full width, whatever box it lives in:

- **the plate** (`:61–89`) is `width: fit-content` between `min-width: 34%` and `max-width: 90%` — so
  a run narrower than the 90 % cap makes the panel grow to hold it, and a run wider than that is
  painted straight out of the panel;
- **the caption** (`:34–58`) sits at `left: 5%; right: 5%` with no width of its own to grow into, so
  any long run leaves it immediately.

Measured on develop (1.26.0), `runserver` from this worktree against the compose Postgres, service
`Ibadah Uji Bungkus 183` at 1920×1080 — the **ink right edge** of a text element against its panel's
right edge:

| state | element | panel box | rows | ink past the panel |
| --- | --- | --- | --- | --- |
| liturgy, body `a very <120-char run> untitled text` | `.obs-overlay__line` | 1728 × 240.72 | 3 | **710.45px** |
| the same, `<140-char URL>` after the mark `L.` | `.obs-overlay__line` (the words column) | 1728 × 251.52 | 3 | **722.08px** |
| song lyric, one 66-char run | `.obs-overlay__caption` | 1728 × 302.39 | 4 | **2,035.20px** |
| passage, verse title one 126-char run | `.obs-overlay__title` | 1728 × 326.22 | 2 | **207.39px** |
| the same passage's body | `.obs-overlay__line` | 1728 × 326.22 | 3 | **694.05px** |
| liturgy, a 64-char entry title (the kicker) | `.obs-overlay__kicker` | 963.44 × 139.94 | 1 | 0px — the plate grows |
| liturgy, short (control) | `.obs-overlay__line` | 823.72 × 201.13 | 1 | 0px |
| liturgy, untitled short (control) | `.obs-overlay__line` | 652.80 × 139.94 | 1 | 0px |

At 1280×720 the overflowing states measure **433.95 · 438.70 · 1,336.81 · 178.59 · 423.36px**; at
960×540 **355.22 · 302.03 · 1,017.61 · 104.69 · 348.02px**.

The reading surfaces got this rule in spec 137 (`overflow-wrap: break-word` on `.read`,
`.search-results`, `.preview`), and that spec's assumptions record that *"the projector and the OBS
dock already break words"*. The overlay was not on that list — and spec 180 then built the plate on
top of it, so the surface that shows the most operator-typed text is the one with no rule at all.

## User Scenarios & Testing

### US1 — Any run with no space in it wraps inside the box that owns it (P1)

**Why this priority**: this is the report. Every word on this surface is operator-typed — a lyric, a
Bible reference, an entry's own title, a liturgy turn — so any of them can arrive as one unbroken run:
a Drive link, a compound word in Simalungun, a name typed with the space missed. Today such a run
leaves its panel and crosses the frame, where the congregation cannot read it against the video.

**Independent Test**: put a 120-character run in a liturgy body, a 140-character URL after a speaker
mark, a 66-character run in a song lyric, and a 126-character run in a passage's verse title; open the
overlay at 1920×1080, 1280×720 and 960×540; every one of them draws inside its box, with no ink past
the box's own edge.

**Acceptance scenarios**

1. **Given** a liturgy body reading `a very <120-char run> untitled text`, **When** the overlay paints
   it at 1920×1080, **Then** the line draws 3 rows inside the 1728px plate and its ink's right edge is
   inside the plate's content edge (710.45px past it today; 32.22px inside after).
2. **Given** the same body with a 140-character URL after the mark `L.`, **When** it is on air at
   1920×1080, **Then** the mark keeps its column, the words wrap to 4 rows, and no ink sits past the
   plate (722.08px today; the plate grows from 251.52 to 301.91px tall to hold the extra row).
3. **Given** a lyric whose run is 66 characters, **When** the caption is on air at 1920×1080,
   **Then** it draws 5 rows inside its 1,728px box and nothing is painted past it (2,035.20px today;
   the caption block grows from 302.39 to 403.19px tall).
4. **Given** a passage whose verse title is one 126-character run, **When** the plate paints at
   1920×1080, **Then** the title takes 3 rows under the reference and the body 3, none past the plate
   (207.39 and 694.05px today; the plate grows from 326.22 to 364.03px).
5. **Given** the body, the caption or the title at 1280×720 or 960×540, **Then** the same holds —
   every one of those spills reaches 0 — with each panel keeping its 90 % width and its bottom-5 %
   anchor.
6. **Given** an entry whose own 64-character title is the plate's kicker, **When** it paints at
   1920×1080, **Then** the plate grows to hold it (963.44 × 139.94) and the title stays 1 row: the
   rule reaches the kicker, and this state needs no break because the kicker is set at `.5em`.

### US2 — Text that already fits is laid out exactly as it is today (P1)

**Why this priority**: the rule is inherited by every text on the surface, so it must be inert where
nothing overflows — otherwise a presentation fix becomes a re-layout of the church's normal week.

**Independent Test**: measure the two control states, a short two-turn liturgy and an untitled one,
before and after at all three frames: the panel's box, the rows and the ink are identical.

**Acceptance scenarios**

1. **Given** a short liturgy, **When** the overlay paints at 1920×1080, **Then** its plate is
   823.72 × 201.13 at the same place and its line still takes 1 row — the same as 1.26.0.
2. **Given** an untitled short text, **When** it paints at 1920×1080, **Then** its plate is
   652.80 × 139.94 and its line 1 row, unchanged.
3. **Given** the same two states at 1280×720 and 960×540, **Then** 548.14 × 135.06 and
   435.19 × 94.28 / 419.34 × 102.02 and 326.39 × 71.44 hold in both builds.

### US3 — The surface keeps every other thing it does (P2)

**Why this priority**: the overlay is a listen-only OBS source whose other behaviour — painting
nothing when nothing is on air, painting nothing for media and rests, leaving the frame transparent —
must not be disturbed by a text-flow property.

**Independent Test**: hide, release and step onto a media screen at 1920×1080; the stage is empty each
time; the page still reports no focusable element and a transparent background.

**Acceptance scenarios**

1. **Given** the display state is off, **When** the overlay is opened, **Then** the stage paints
   nothing and the document body is transparent.
2. **Given** a media or a rest screen, **Then** the stage paints nothing.
3. **Given** the plate's arrival and the caption's arrival, **Then** `overlay-plate-in` and
   `overlay-caption-in` still run at 180ms and the exits at 120ms.

### Edge Cases

- **A run narrower than the panel's cap** — the panel grows to hold it, as today; the rule changes
  nothing, because nothing needs breaking (measured: the 64-character kicker).
- **A speaker's mark** — it keeps its `white-space: nowrap`, its own declaration: marks are labels from
  the mark grammar (`L.`, `P + K:`, `Pengkhotbah:`, at most ~250px at 36px), not prose. The words
  column beside it is what wraps.
- **A row that is *only* a mark** — nothing to break; it renders as it does today.
- **A run longer than the plate's height** — the panel keeps its bottom anchor and grows upward past
  the frame's top; the surface has never clamped its own height and this slice does not start.
- **The caption's own centring** — it is `text-align: center` with `text-wrap: balance`; a wrapped run
  keeps both, so the extra rows are balanced rather than ragged.
- **The stage is transparent** — nothing about the rule paints: no background, no plate for a song.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | A text run wider than the box that owns it SHALL break at that box's edge on the overlay — the plate's body rows, the plate's kicker, the plate's title, and the song caption. No part of any text SHALL be painted past the panel's right edge. | `overlay/R4` |
| FR-002 | The rule SHALL be one declaration inherited from the overlay's root (`.obs-overlay__stage`), so every text element of the plate and the caption is covered without naming each one. | `overlay/R1` |
| FR-003 | The panels' measuring SHALL NOT change: the plate stays `fit-content` between its `min-width: 34%` and `max-width: 90%`, both keep their place at `bottom: 5%`, and a text that fits draws the same rows in the same box. | `overlay/R3` |
| FR-004 | A speaker's mark SHALL keep its own `white-space: nowrap` and its `max-content` column (spec 180). | `overlay/R5` |
| FR-005 | The overlay's other behaviour SHALL be unchanged: nothing painted for blank, hidden, released, media and rest screens, no focusable element, a transparent page. | `overlay/R6` |
| FR-006 | The caption SHALL keep its own type and its centring: weight 800, the eight-way outline, `text-align: center`, `text-wrap: balance` (specs 119 and 180) — only the break opportunity changes. | `overlay/R2` |
| FR-007 | The rule SHALL be size-independent: the same wrap at 1920×1080, 1280×720 and 960×540, because every measure on the surface is already in container units. | `overlay/R4` |

### Key Entities

- **Overlay stage** — `.obs-overlay__stage`, the fixed, transparent root of the surface; the element
  the rule is declared on.
- **Panel** — the thing that owns the text: `.obs-overlay__plate` (a passage or a liturgy text) or
  `.obs-overlay__caption` (a song). Both are absolute, inset 5 % at the sides and the bottom.
- **Text element** — `.obs-overlay__kicker`, `.obs-overlay__title`, `.obs-overlay__line` (with its
  `.obs-overlay__speaker` and `.obs-overlay__words` when it carries a mark), `.obs-overlay__caption`.
  The mark is the one element that does not break, by its own declaration.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | No text on the overlay is painted past its panel | the right edge of every text element's ink rects ≤ its panel's right edge, on seven states at 1920×1080, 1280×720 and 960×540 (0px; from 710.45 / 722.08 / 2,035.20 / 207.39 / 694.05 at 1080p) |
| SC-002 | Text that fits is unchanged | the two control states' panel boxes, row counts and ink are identical to 1.26.0 at all three frames, and the 64-character kicker state is 963.44 × 139.94 in both builds |
| SC-003 | The rule is inherited, not repeated | `getComputedStyle('.obs-overlay__stage').overflowWrap === 'break-word'`, and the same on the plate, the kicker, the row, the words column and the caption, from one declaration in the sheet |
| SC-004 | The surface still paints nothing when nothing is on air | the stage has no child on a blank, hidden or released state, and on media and rest screens |
| SC-005 | The marks still hold their column | the `.obs-overlay__speaker` computed `white-space` is `nowrap`, and its `max-content` column is the widest mark on the screen |
| SC-006 | The caption keeps its own look | weight 800, `text-align: center`, `text-wrap: balance` and its outline intact on the wrapped rows |

## UI/UX

**Static preview**: `specs/183-overlay-text-wrap/preview/index.html` — the DOM captured from the
slice's own `/obs/source/overlay` (the controller's own markup, class for class), the repo's own
`obs-overlay.css` and bundled faces, over a 1920×1080 frame from the church's own worship video. A
sidebar index of seven states, ◀ ▶ / J K / 1–7, a position kept in the URL hash (deep links work), a
**Before / Both / After** switch (`B`), and `Fit` / `1:1`. *Before* is the same subtree with the one
declaration restored to `normal`, so the two frames differ by exactly what the slice changes. Built by
`preview/build_preview.py`; every number below is the live page's own.

- **Layout / position**: unchanged. Both panels keep their 5 % insets, their bottom anchor and the
  plate's `fit-content` measure; the rule adds no box, margin or padding. At 1920×1080 the affected
  panels are 1728px wide before and after (the 90 % cap); only their **height** changes where a run
  wraps to a further row: the pasted-URL plate **1728 × 251.52 → 1728 × 301.91**, the song caption
  **1728 × 302.39 → 1728 × 403.19**, the passage plate **1728 × 326.22 → 1728 × 364.03**. The
  reported liturgy's plate is **1728 × 240.72** in both builds, and the kicker state stays
  **963.44 × 139.94**.
- **Size / spacing**: the type is untouched — the plate's `clamp(5.5px, 1.875cqw, 40px)` resolves to
  **36px** at 1920, **24px** at 1280 and **18px** at 960; the caption's own clamp to **72 / 48 / 36px**;
  the plate's padding `.42em .65em .44em` stays 15.12 / 23.40 / 15.84px and its row gap `.3em`
  10.80px. Only the rows change: **3 → 4** on the pasted-URL body, **3 → 4** on the passage's body,
  **2 → 3** on its title, **4 → 5** on the caption; the reported body stays at **3**.
- **Colour / typography**: unchanged — same face (Source Sans 3), same inks, same plate fill, same
  caption outline, same kicker tracking. The caption's `text-align: center` and `text-wrap: balance`
  are still computed on the wrapped block.
- **States**: seven on the preview page — the report, the pasted link with its mark, the song caption,
  the long verse title, the 64-character kicker, and the two controls. Every state is reachable by
  hand, by key, and by deep link.
- **Motion**: unchanged — the panel's 180ms arrival and 120ms exit animate the box as they do now;
  the rule adds no transition and re-wraps nothing that is already laid out.
- **Responsive**: every affected state stops overflowing at every frame measured — at **1280×720**
  433.95 / 438.70 / 1,336.81 / 178.59 / 423.36 → 0; at **960×540** 355.22 / 302.03 / 1,017.61 /
  104.69 / 348.02 → 0. The controls and the kicker measure the same boxes at all three frames.
- **Unchanged by design**: the speaker mark keeps `nowrap`; neither panel has a maximum height and
  none is added; nothing about the transparency, the count of painted objects, or the page's own
  markup changes.

## Assumptions

- **The whole surface is in scope** — the owner widened it at gate 2 from the plate's body to the
  caption and the plate's heading; the earlier, narrower answer is kept in `## Clarifications` as
  superseded rather than rewritten.
- **`break-word` and not `anywhere`** — measured on the live page, the two produce identical boxes,
  row counts and zero spill on every state; `break-word` matches the projector's own rule and spec
  137's, and leaves intrinsic sizing alone, which `anywhere` changes.
- **No clamp, no scroll, no maximum height** — a text that wraps to more rows makes its panel taller,
  anchored at the bottom; the surface has never limited its own height and the report does not ask
  for one.
- **The mark is not prose** — marks come from the label grammar (`read_mark`), at most `Pengkhotbah:`;
  the rule covers the words beside them and leaves the mark's `nowrap` alone.
- **A kicker cannot outgrow the plate** — it is set at `.5em` and its column holds 64 characters, so
  the plate's `fit-content` measure always absorbs it; the rule is there for a plate that is holding a
  longer row, not for the 64-character state, which is measured as unchanged.
- **CSS only** — no markup, view, model or controller change; the E2E tests read the computed style
  and the geometry from the live page.
- **No new tokens, fonts or icons.**

## Clarifications

### Session 2026-11-02

- Q: How far should the fix reach on the overlay — the whole surface, the body lines, or the body and
  the caption? → A: **only the plate's body lines** (the liturgy text the report shows) — owner,
  2026-11-02.
  - **Superseded at gate 2 the same day**: *"do the word-break on the song captions and the panel's
    header/title as well"* — owner, 2026-11-02. FR-001, FR-002, FR-006 and SC-001, SC-003, SC-006 were
    rewritten for the wider scope; the caption and the heading moved from *unchanged* to *required*,
    and the two states that were out of scope are now acceptance cases (US1.3, US1.4). The earlier
    answer stays here rather than being deleted, so the reversal is visible.
