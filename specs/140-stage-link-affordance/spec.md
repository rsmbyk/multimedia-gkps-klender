# Feature Specification: The stage's entry links read as text until hovered

**Slice**: `specs/140-stage-link-affordance`
**Branch**: `feat/140-stage-link-affordance`
**Created**: 2026-10-27
**Status**: Accepted (owner, gate 1, 2026-10-27). Revised 2026-10-27 at the owner's direction after
Converge found that the entry controls cover the title at narrow stages: the controls move into a
column of their own and collapse to icons on a phone. The requirements are unchanged; the preview and
`## UI/UX` are. Recorded in `research.md` D006.
**Input**: "make the link texts similar to appear in normal color and only get underlined if being hovered"

## What the stage does today

The Tata Ibadah stage prints each entry's title as a link to its song, passage or media page
(`.entry__jump`). Spec 056 gave those links the theme's `--link` colour — forest green `#1C5C3C` in
light, lifted royal blue `#7C9CF0` in dark — with the browser's underline kept, which was right when
the alternative was the browser's default blue. The result is that a service page reads as two
colours: every song and passage title is a green (or blue) line among ink-coloured text, whether or
not the operator is pointing at it.

## User Scenarios & Testing

### US1 — The titles read as the page's text, and answer the pointer (P1)

**Why this priority**: this is the request. The stage is read top to bottom like an order of
service; a link colour on every title turns the reading into a list of links.

**Independent Test**: open a service, look at its entry titles without touching the page — each is
the same colour as the text around it and carries no line — then point at one title and it gains a
line.

**Acceptance scenarios**

1. **Given** a service whose entries have titles, **When** the stage is at rest, **Then** each
   entry title is painted in the heading's own `--ink` and carries no underline, in both themes.
2. **Given** the same stage, **When** the pointer rests on a title, **Then** that title gains an
   underline 3px below its text and its colour does not change.
3. **Given** the same stage, **When** a title is reached with the keyboard, **Then** it gains the
   same underline, so the affordance is not mouse-only.
4. **Given** the pointer leaves the title, **When** it is no longer hovered, **Then** the underline
   is gone and the title is ink again.
5. **Given** a title long enough to wrap, **When** it is hovered, **Then** the underline follows
   every line of it rather than only the last.

### US2 — Nothing else changes (P2)

**Why this priority**: the request is about the stage's titles; touches beyond them would need their
own decision.

**Independent Test**: walk the same frames as before — the search results, the media library's use
links, the sidebar rows, the editor — and find their link treatments exactly as they were.

**Acceptance scenarios**

1. **Given** a search result, **When** it is hovered, **Then** its title underlines as it does today.
2. **Given** the media library, **When** its "used by" links are shown, **Then** they keep the
   `--link` colour they have today.
3. **Given** any other anchor on the stage, **When** it is inspected, **Then** nothing about it has
   changed.

### Edge Cases

- **When** the reading view is a saved copy rather than a freshly served page **Then** the same rule
  applies, because the copy renders the same class.
- **When** the title is a long unbroken run **Then** it still wraps inside the pane (spec 137) and
  the underline follows the wrapped lines.
- **When** the pointer is a touch pointer, which never hovers **Then** the title opens on tap with no
  pre-hover affordance; nothing is drawn at rest.
- **When** the theme is switched while a title is hovered **Then** the title keeps the underline and
  takes the new theme's ink.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | At rest, a stage entry title is painted in `--ink`, with no underline, in both themes. | `new: reading/R16` |
| FR-002 | On pointer hover, a stage entry title gains an underline with a 3px offset; its colour stays `--ink`. | `new: reading/R16` |
| FR-003 | On keyboard focus (`:focus-visible`), a stage entry title gains the same underline; its colour stays `--ink`. | `new: reading/R16` |
| FR-004 | The `--link` token and every other anchor's treatment are unchanged; the media library's links keep their colour. | `new: reading/R16` |

### Key Entities

None. This slice changes one rule's presentation; it adds no field, record or endpoint.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | Every stage entry title is the heading's ink in both themes. | Computed `color` on `.entry__jump` equals the enclosing `.read__sec`'s, `#1F1F1D` light and `#F5F3EE` dark. |
| SC-002 | No stage entry title draws a line at rest. | Computed `text-decoration-line` is `none` on every title before it is pointed at. |
| SC-003 | Hovering draws exactly one line, 3px under the text, and does not recolour it. | Computed `text-decoration-line: underline`, `text-underline-offset: 3px`, colour unchanged. |
| SC-004 | The titles stay AA in both themes. | `--ink` on `--canvas` is 15.16:1 light and 16.76:1 dark. |
| SC-005 | No other anchor's treatment changes. | The link-colour E2E still passes for the media library; the search-result hover underline is unchanged. |

## UI/UX

Live preview at `http://127.0.0.1:8773/tatib/144/` (the slice branch, served from the worktree):

- **Layout / position**: the rule paints, it does not box — the title's own box is unchanged. The
  entry's floating controls now own a column at its right edge (they used to sit over the title): the
  entry reserves 264px once the reading pane is at least 700px wide and 106px below that, so neither a
  title nor a media name is ever drawn under the buttons. The underline sits 3px under the baseline, the same
  offset `.result-row:hover .result-row__title` uses.
- **Size / spacing**: the entry's height, line height and type do not move for the underline. The
  controls' labels collapse to icons while the pane is narrower than 700px: three 27px buttons,
  106px of reserved column; from 700px of pane the labels return — 252px of buttons, 264px reserved.
- **Colour / typography**: rest and hover are `--ink` — `#1F1F1D` on `#F7F5F1` (15.16:1) in light,
  `#F5F3EE` on `#14130F` (16.76:1) in dark. No `--link` on this surface.
- **States**: rest — no line; hover — underline, `text-underline-offset: 3px`; focus-visible — the
  same underline; controls — revealed on the entry's hover or focus exactly as before, labelled on a
  desktop and icon-only on a phone; active, disabled, empty, error, loading — not applicable to a
  link that only navigates.
- **Motion**: none for the link; the controls keep their existing opacity transition.
- **Responsive**: the controls' labels collapse when the reading pane is narrower than 700px — the
  question is the pane's width, not the window's, so the rule is a container query on
  `.read__body`. At a 1440px window with both sidebars open the pane is 400px, so the controls are
  icons there; at 1920px it is 880px, and the labels return. A wrapped title
  underlines every line it occupies; the pane's own wrap rule (spec 137) keeps it inside.

## Assumptions

- **"The link texts" are the stage's entry-title links** — the green underlined song and passage
  titles in the request's screenshot (`.entry__jump`). No other anchor is restyled; the search
  results, the media library's links, the sidebar rows and the editor are deliberately out of scope.
- **The colour is normal in every state, not only at rest.** The request names the underline as the
  only change, so hovering does not bring the link colour back.
- **Keyboard focus gets the same underline.** A rest state with no colour and no line leaves a
  keyboard user nothing to see; `:focus-visible` is the same affordance the pointer gets.
- **The 3px offset is taken from the existing hover cue** on search results rather than invented.
- **`--link` stays.** The media library's "used by" links still wear it, so the token and its
  contrast pair in `tests/test_design_tokens.py` remain true.
- **The controls keep their labels wherever the pane has room, and collapse to icons below 700px of
  pane** (owner's decision, 2026-10-27). The pane is the thing that has to hold the words: at a 1440px
  window with both sidebars open it is 400px, so reserving the labels' 264px there would leave 144px
  for the title and wrap every entry (measured: all four entries on `/tatib/144/` wrapped). Threshold
  and measurement are D006 in `research.md`.
- **The controls' labels stay in the accessibility tree when they collapse.** The label's box is
  visually hidden rather than `display: none`, so a screen reader still hears "Preview", "Edit" and
  "Delete" on a phone.

## Clarifications

None open. The scope question ("the link texts" — these titles or every anchor?) is recorded under
`## Assumptions` with its recommendation rather than asked, because the request's own screenshot
shows the stage's entry titles and spec 056 already rejected a global anchor rule.
