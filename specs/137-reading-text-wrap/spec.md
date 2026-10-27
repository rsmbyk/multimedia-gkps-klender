# Feature Specification: A reading page's text wraps at its pane instead of running past it

**Slice**: `specs/137-reading-text-wrap`
**Branch**: `feat/137-reading-text-wrap`
**Created**: 2026-10-27
**Status**: Accepted (owner, gate 1, 2026-10-27 — accepted after the scope question was reopened and
answered: every text run on the reading surfaces, not only the page title)
**Input**: "long title in pages overflows instead of wrapped (the sample i give you in those two images are tata ibadah and songs. but make sure it is fixed in other kind of pages)"

## User Scenarios & Testing

### US1 — A page title wraps inside the reading pane (P1)

**Why this priority**: this is the report. A title is one unbroken run — a pasted link, a
script-created record, a name with no spaces — and today it is painted straight out of the reading
pane. At 1440×900 the Tata Ibadah title alone pushes the document 1,033px past the viewport, so the
whole page scrolls sideways and the title cannot be read past the pane's edge. Every reading page
draws its title from the same element, so the same fault is one copy on each of them.

**Independent Test**: open a Tata Ibadah service and a song whose titles are unbroken runs; each
title occupies as many lines as it needs inside the pane, the document does not scroll sideways,
and the title's box keeps the width it has today.

**Acceptance scenarios**

1. **Given** a service whose title is one unbroken run of 64 characters — the column's own limit — **When** the service page
   opens at 1440×900, **Then** the title is drawn in 4 lines inside its 400px box, no part of it sits
   past the pane, and the document's `scrollWidth` equals its `clientWidth`.
2. **Given** a song whose title is a long unbroken run followed by a space and a name, **When** the
   song page opens, **Then** it wraps at the space as it does today and the unbroken part breaks at
   the pane's edge — 3 lines at 1440×900 in a 520px box, no horizontal scroll.
3. **Given** a title that fits, **When** the page opens, **Then** it is one line and exactly the
   height it is today.
4. **Given** the same page at 390×844, **When** it opens, **Then** the title still wraps inside the
   pane, and the document does not scroll sideways.

### US2 — Every other text run on the reading surfaces wraps the same way (P1)

**Why this priority**: the report asks for the other page kinds, and the defect is one property, not
one element. The same fault measured on the same pages: a Bible pericope heading (143px past its
pane at 1280×800), a verse line, a Tata Ibadah body paragraph holding a pasted Drive link (215px at
1440×900, 375px at 1280×800), and a search result's title (614px). A fix that reaches only the title
would leave each of them overflowing.

**Independent Test**: on a page of each kind, put one unbroken run in a section heading, a verse
line, a body paragraph, a search row and a preview line; none of them is painted past its pane and
none of them widens the document.

**Acceptance scenarios**

1. **Given** a Bible chapter whose pericope heading is one unbroken run, **When** the chapter page
   opens at 1280×800, **Then** the heading wraps inside the reading pane and the document has no
   horizontal overflow (143px before).
2. **Given** a Tata Ibadah text entry whose body is a pasted URL, **When** the service page opens at
   1440×900, **Then** the URL wraps onto 2 lines inside its 400px box instead of running 215px past
   it.
3. **Given** a search result whose title is one unbroken run, **When** the results page opens,
   **Then** the title wraps inside the result row and the document has no horizontal overflow
   (614px before).
4. **Given** a preview of that same text entry, **When** the Preview modal opens, **Then** its lines
   wrap inside the dialog exactly as they do in the pane.

### US3 — A surface that deliberately truncates keeps truncating (P2)

**Why this priority**: the fault is "text escapes its box", and the cure must not arrive where
truncation is the design. A service or songbook row in the sidebar is one line ending `…`; a media
library filename is one line ending `…`; a contents row is three lines ending `…` (spec 135). A
blanket wrap would silently unclip all three, which is a different change from this one.

**Independent Test**: open a service list, a media library and a service's contents list; the rows
that hid text before still hide it, in the same number of lines, with the same `…`.

**Acceptance scenarios**

1. **Given** a service whose name is a 60-character unbroken run, **When** the Tata Ibadah list is
   drawn, **Then** its row is still one line ending `…`, not a wrapped block.
2. **Given** a media file whose name is longer than its row, **When** the media library is drawn,
   **Then** its filename is still one line ending `…`.
3. **Given** a contents row that needs more than three lines, **When** the service page is drawn,
   **Then** it is still three lines ending `…`.

### Edge Cases

- **When** a run is a single character wide **Then** nothing changes: the text is already inside its
  box.
- **When** a title is long but has spaces **Then** it wraps at the spaces exactly as today, and only
  a part that cannot fit breaks.
- **When** the language toggle (TB / SIM) shares the title's row **Then** it keeps the line it takes
  today at every width — the title's own measuring must not change.
- **When** the text is inside a `nowrap` element **Then** it keeps not wrapping; that is the
  truncation surfaces' own declaration and is untouched.
- **When** a page is opened with no long text at all **Then** it renders byte-for-byte the same
  layout as before the slice.
- **When** the reading pane is hidden — the search page's results, the index — **Then** the rule
  still applies where those surfaces draw text, and nothing appears or disappears.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | A reading page's title SHALL wrap a run wider than its box at the box's edge; no part of the title SHALL be painted past the pane or widen the document. | `new: reading` |
| FR-002 | A section or item heading, a verse or lyric line, and a Tata Ibadah body paragraph SHALL wrap a run wider than the box that owns it, on every reading page. | `new: reading` |
| FR-003 | A search result's title, meta line and excerpt SHALL wrap a run wider than the result row. | `new: reading` |
| FR-004 | The Preview modal's rendered lines and references SHALL wrap a run wider than the dialog's content box. | `new: reading` |
| FR-005 | No reading route SHALL scroll horizontally because of text: the document's `scrollWidth` SHALL equal its `clientWidth` at 1440×900, 1280×800, 820×900 and 390×844. | `new: reading` |
| FR-006 | A surface that deliberately truncates SHALL keep its truncation: the sidebar's service and songbook rows and the media library's filenames stay one line ending `…`, and a contents row keeps its three-line clamp (spec 135). | `reading/R12` |
| FR-007 | Wrapping SHALL NOT change the layout's own measuring: a title's box keeps the width it has today at every width, and the language toggle keeps the position it takes today. | `new: reading` |
| FR-008 | Text that already fits SHALL render as it does today — same line count, same box height, same position. | `new: reading` |
| FR-009 | The rule SHALL reach a surface by inheritance from the surface's own root, so a text run inside it is covered without naming each element. | `new: reading` |

### Key Entities

- **Reading surface** — the elements that carry the reading document's text: the reading pane
  (`.read`, its head and body), the search results list (`.search-results`) and the Preview modal
  (`.preview`). The rule is declared on these three roots and inherited.
- **Truncating surface** — an element that declares its own one- or three-line cut: `.book__n` and
  the media filenames (`nowrap` + `…`), `.songrow__t` (`anywhere` + three-line clamp). Read, never
  changed by this slice.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | No reading route scrolls sideways | `document.scrollWidth - clientWidth == 0` at 1440×900, 1280×800, 820×900 and 390×844 on `/tatib/<id>/`, `/songs/<id>/`, `/bible/<book>/<ch>/`, `/search?q=…`, `/media-library/`, `/tatib/`, `/songs/`, `/` |
| SC-002 | A 64-character title is wholly inside the pane | the title's range rectangles all end at or before its box's right edge (0px spill, from 1,082px) |
| SC-003 | Titles that fit are unchanged | the same line count and box height before and after on a short-title service, song and Bible chapter |
| SC-004 | Truncating surfaces still truncate | `.book__n` and the media filename report one line and `text-overflow: ellipsis`; `.songrow__t` keeps `-webkit-line-clamp: 3` |
| SC-005 | The layout's measuring is unchanged | the title's box width is identical before and after at every measured width (400px at 1440×900 on `/tatib/149/`, 240px at 1280×800, 290px at 390×844) |
| SC-006 | The body paragraph wraps | the Drive-link body's spill goes from 215px to 0 at 1440×900 and it draws 2 lines instead of 1 |
| SC-007 | The Bible heading and search row wrap | `.read__sec` 143px → 0 at 1280×800; `.result-row__title` 614px → 0 |

## UI/UX

Measured on the preview (`preview/after-*.html`, built from the worktree's own server) against
`preview/before-*.html`, which is the same page with the rule's one declaration restored to
`overflow-wrap: normal`.

- **Layout / position**: unchanged. The rule adds no box, no margin and no padding; every element
  keeps the width it has today. On `/tatib/149/` the title's box is **400px** at 1440×900, **240px**
  at 1280×800 and **290px** at 390×844 — the same before and after; on `/songs/1817/` it is **520px**,
  **360px** and **290px**.
- **Size / spacing**: the type is untouched. The title is **43.2px/46.66px** at 1440×900 and
  1280×800, and **25.35px/27.38px** at 390×844. The 64-character Tata Ibadah title goes from **1
  line, 47px** (painted 1,082px past the pane) to **4 lines, 187px**; the song's title from **2
  lines, 93px** to **3 lines, 140px**; the Drive-link body from **1 line** to **2 lines**.
- **Colour / typography**: unchanged — same serif, same weight 620, same tracking; nothing new.
- **States**: no hover, focus, active, selected or empty state is touched; the rule is a property of
  the text flow, so every state that draws text inherits it.
- **Motion**: none added.
- **Responsive**: at **1280×800** the title runs to 7 lines (327px) inside 240px and the Bible
  pericope heading stops overflowing (143px → 0); at **390×844** the title runs to 4 lines (109px)
  inside 290px and the Bible heading stops overflowing at 394px. Document overflow at each width:
  1,033 → 0 (Tata Ibadah, 1440), 1,193 → 0 (1280), 571 → 0 (390); songs 380 → 0, 540 → 0, 257 → 0;
  Bible 79 → 0 (1280), 376 → 0 (390); search 467 → 0 (1440), 547 → 0 (1280), 996 → 0 (390).
- **Unchanged by design**: the sidebar's service row still clips (281px of text hidden inside a
  293px row, one line, `…`), the media filename still clips, and the contents rows keep their
  three-line clamp.

## Assumptions

- **The truncating surfaces stay as they are** — the sidebar list rows, the media filenames and the
  contents rows are index shapes with a deliberate cut; this slice does not unclip them.
- **The widest storable values are the fixtures** — `TataIbadah.name` and `Song.title` are 64
  characters, a `BookTranslation`'s translation 32, a `Verse`'s title 128, and a text entry's body a
  `TextField`. No column limit changes here; the tests use the widest value the product can hold,
  which is exactly the case the owner met.
- **`/manage/` and the Django admin are outside** — they are the content editors, not reading
  surfaces, and they render their own pages.
- **The projector and the OBS dock already break words** (`overflow-wrap: break-word` /
  `anywhere`) and are untouched.
- **CSS only** — no markup, no view, no model, no test-fixture change is required by the rule
  itself; the browser tests in `plan.md` read the computed style and the geometry.
- **No new tokens, fonts or icons.**

## Clarifications

### Session 2026-10-27

- Q: Which text should break at its box's edge — only the page title, or every text run on the
  reading surfaces? → A: **every text run on the reading surfaces** — the page title, section
  headings, verse and lyric lines, body paragraphs, search result rows and the Preview modal's
  lines (owner, 2026-10-27).
- The question was reopened after going unanswered on the first pass. The answer matches FR-002 to
  FR-004 as written, so no requirement, scenario or success criterion changed to accept it; the
  assumption that had stood in its place is removed from `## Assumptions`.
