# Feature Specification: A Tata Ibadah sidebar row is three lines, ellipsized

**Slice**: `specs/135-tatib-sidebar-row-clamp`
**Branch**: `feat/135-tatib-sidebar-row-clamp`
**Created**: 2026-10-26
**Status**: Accepted (owner, gate 1, 2026-10-26 — accepted after the preview gained the unbroken-run
case in every kind and the song row's heading was capped at two lines so its `Bait …` line always
shows)
**Input**: "alright. here is how i want it to change: — remove the 60-char cap — it is now capped at 3 visual lines for texts (title and first 3 body lines), medias, passages, songs (including bait row, which means two lines for heading/title), section break, and legacy tataibadahitem. — it is now ellipsized at the end"

## User Scenarios & Testing

### US1 — A row is as tall as three lines of its own text, and says when it holds more (P1)

**Why this priority**: this is the whole request. Today a row's height is a side effect of what the
server chose to send — two body lines for an untitled text, one title otherwise — and the label is
then cut at 60 characters with nothing at the cut. A 64-character song title wraps to a second line
and is mistaken for a three-line row; a 61-character title loses its last character silently. Moving
the cap to the row's height makes every kind obey one rule and makes the cut visible.

**Independent Test**: a service holding a long text entry, a long passage reference, a long media
title and a long section-break-free service order shows every row at three lines or fewer, each
clamped row ending in `…`.

**Acceptance scenarios**

1. **Given** a row whose label word-wraps past three lines, **When** the row is drawn, **Then** it
   occupies three lines and its last line ends `…`.
2. **Given** a row whose label fits in one, two or three lines, **When** it is drawn, **Then** no
   `…` appears and the row is exactly as tall as its own lines.
3. **Given** a title of 61–64 characters, **When** it fits in three lines, **Then** all of it is
   shown — no silent cut at 60.
4. **Given** an untitled text entry whose body has more than three lines, **When** the row is drawn,
   **Then** the row shows the body's first three lines and ends `…`.
5. **Given** a legacy row whose whole body is one unbroken link of 81 characters, **When** the row
   is drawn, **Then** it wraps inside the pane across the lines it needs — no part of it, and no
   `…`, sits past the row's right edge.

### US2 — A song row spends at most two lines on its heading, and keeps its `Bait …` line third (P1)

**Why this priority**: the `Bait …` line is the operator's check that the right verses are in the
order; it is the one part of a song row that must not be pushed out by a long title. Counting it
inside the three-line budget is what the request asks for.

**Independent Test**: a song whose `PKJ 4 <title>` heading needs more than two lines shows its
heading on two lines ending `…`, with `Bait …` on the third; a song with a short heading shows
heading, `Bait …`, and a blank third line's worth of nothing.

**Acceptance scenarios**

1. **Given** a song entry with a `Bait …` line and a heading that needs one line, **When** it is
   drawn, **Then** the heading is line 1 and `Bait …` is line 2.
2. **Given** the same row with a heading that needs two lines, **When** it is drawn, **Then** the
   heading takes lines 1–2 and `Bait …` is line 3 — the row is exactly three lines.
3. **Given** a heading that needs three lines or more, **When** it is drawn, **Then** the heading is
   capped at two lines ending `…`, and `Bait …` is line 3.
4. **Given** a song entry with no verse line — its target deleted, or no verses stored — **When** it
   is drawn, **Then** the whole three-line budget belongs to the heading.

### US3 — The saved copy of the page draws the same rows (P2)

**Why this priority**: a saved Tata Ibadah page is rendered from the library by
`static/web/offline-render.js`, and its sidebar is read before the online page replaces it. A row
that changes shape when the online page arrives is the regression spec 122 and the capability's
saved-copy requirements exist to prevent.

**Independent Test**: render a saved Tata Ibadah page holding the same rows; each row is the same
three-line box, with the same ellipsis, as the server page's.

**Acceptance scenarios**

1. **Given** a saved service whose rows are clamped on the server, **When** the saved page is drawn,
   **Then** every row's line count, wrapping and trailing `…` equal the server page's.

### Edge Cases

- **When** a body line is blank **Then** it still occupies its line (a blank second line leaves a gap
  in the row, as it does today), and the three-line count includes it.
- **When** one line is a single unbroken run wider than the pane **Then** the row wraps it at the
  pane's edge rather than overflowing horizontally.
- **When** a row is the section break **Then** its label is the kind's own name and the row is one
  line, unaffected by the cap.
- **When** the panel filter is used **Then** it still matches the entry's whole text, not only the
  three lines on screen.
- **When** an entry carries a title longer than the budget allows **Then** the row ends `…` — no
  name, tooltip or queue index is truncated in the same act (the controls' own labels are unaffected).
- **When** the row is selected, hovered or focused **Then** its height does not change.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | A service-order row in the reading sidebar SHALL be capped at three visual lines of its own text; a row that does not show all of its text SHALL end in `…`. | `new: reading` |
| FR-002 | The 60-character cut on a row's label SHALL be removed for every kind, so a title that fits in three lines is shown whole. | `new: reading` |
| FR-003 | An untitled text entry's row SHALL carry the first three lines of its body. | `new: reading` |
| FR-004 | A titled text entry's row SHALL carry its title alone, wrapping within the three lines; its body SHALL NOT be drawn in the row. | `new: reading` |
| FR-005 | A song entry's row SHALL carry its heading and its `Bait …` line, with the `Bait …` line counted as one of the three: the heading SHALL occupy at most two lines and the `Bait …` line SHALL always be drawn, with the heading ending `…` when it does not fit two lines. | `new: reading` |
| FR-006 | A passage, media or section-break row SHALL obey the same three-line cap over its label as rendered. | `new: reading` |
| FR-007 | A legacy `TataIbadahItem` row SHALL follow the Text entry's shape: without a title it carries the first three body lines, and with one it carries the title alone — under the same cap and ellipsis. | `new: reading` |
| FR-008 | A row's label SHALL wrap at the pane's edge instead of overflowing it, in every kind — text, media, passage, song, section break and the legacy rows — so no line, and no `…`, sits past the row's right edge. | `new: reading` |
| FR-009 | A page rendered from the saved library SHALL draw the same rows — the same lines, wrapping and trailing `…` — as the server route it mirrors. | `reading/R2` |
| FR-010 | The panel filter SHALL keep matching the entry's whole text, independent of how much of it the row shows. | `new: reading` |

### Key Entities

- **Service-order row (`toc_items` entry)** — one line of the reading sidebar's contents list: an
  anchor, its index number and its label. The label is what this slice constrains; the anchor,
  index, drag handle and edit control are untouched.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | No row in the reading sidebar is taller than three text lines | every row in a service holding all six kinds measures ≤ 3 line boxes at 1440×900, 1280×800 and 390×844 |
| SC-002 | Every row that hides text ends in `…` | a body of five lines and a 64-character title both read `…`; a one-line label reads none |
| SC-003 | No label is cut at 60 characters any more | a 64-character title is fully present in the row's text |
| SC-004 | The saved copy matches | the saved page's rows equal the server page's in line count and ellipsis |
| SC-005 | No row's label overflows its pane | at 1440×900, 1280×800 and 390×844 every row's label reports `scrollWidth == clientWidth`, and the row's `…` sits inside the row |

## UI/UX

Measured on the preview (`preview/after.html`, built from the real `/tatib/144/` page) at
**1440×900**, panel `#chList` **415px** wide — its `26rem` cap.

- **Layout / position**: unchanged. The row keeps its 7px/10px padding, its number gutter
  (`min-width: 3.4rem`) and its 30px of right padding that makes room for the drag grip. Only the
  label's box changes: a text row is one clamped block with its lines separated by a line break, and
  a song row keeps its heading and its `Bait …` line as two blocks inside that box — the heading
  clamped to two lines, the `Bait …` line always the third.
- **Size / spacing**: the label's box is **21.75px** for one line, **43.5px** for two, **65.25px**
  for three (14.5px type, 21.75px line). A song row is **39px** with a one-line heading plus its
  `Bait …` line, and **60px** with a two-line heading plus `Bait …` — its heading never takes a third
  line, and a song with no `Bait …` line uses the full three lines (65.25px). With the row's padding
  the whole row measures **38px** (one line), **57.5px** (two), **79.3px** (three), **53px** (a song's
  heading and `Bait …`) and **74px** (a two-line heading and `Bait …`).
- **Colour / typography**: unchanged — the label stays 14.5px, a song's reference 12px/600, its
  `Bait …` line 12px/400 in `--head-ink`, an untitled text's label in the italic `--head-ink` of
  `.songrow--cont`.
- **States**: hover, selected (`aria-current`), focus and drag all keep the row's height; the clamp
  does not change with them. A row that hides text ends `…`; a row that shows all of it does not.
- **Motion**: none added. The row's existing transitions are untouched.
- **Responsive**: at **390×844** the panel is **313px** wide and a 64-character title takes three
  lines (65.3px) instead of two; the cap still holds at three, a song's heading is capped at two
  lines ending `…`, and its `Bait …` line stays as the third.

## Assumptions

- **Scope is the reading sidebar** (`#chList` on a Tata Ibadah page) — the first-level list of
  services, the operator dock's own rows and the stage's text pane are outside it. The stage keeps
  its existing three-line clamp, which this slice does not touch.
- **The saved copy is in scope**, because it draws the same rows from the same data.
- **A `…` is required where text is hidden, not where it fits** — a row that shows everything has no
  ellipsis.
- **The row's index number, drag grip and edit control do not count** towards the three lines and do
  not move.
- **The 64-character column limits are unchanged** — this slice changes presentation, not storage.
- **No new tokens, fonts or icons.**

## Clarifications

### Session 2026-10-26

- Q: Titled Text entries — does the body join the title under the three-line cap? → A: the title
  alone, wrapping across up to three lines (owner).
- Q: Legacy `TataIbadahItem` rows — three lines of what? → A: untitled, the first three body lines;
  titled, the title alone — the same shape as a Text entry (owner).
- Q: Song row whose heading needs more than two lines — cap it or let it take all three? → A: cap the
  heading at two lines; the `Bait …` line always shows (owner).

