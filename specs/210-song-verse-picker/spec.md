# Feature Specification: the song entry's pickers

**Slice**: `specs/210-song-verse-picker`
**Branch**: `feat/210-song-verse-picker`
**Created**: 2026-11-21
**Status**: Draft
**Input**: the owner's request — "i wanna revamp the song entry picker modal" — and the
decisions made over the preview review: the verse picker was the first pain point; the song
picker belongs in the same slice; search must be ready as the modal opens; the results list
must be able to run past the modal's bottom edge; five tiles per row; range extension is a
held press-and-drag that previews until release; the monologue line ("Bait 1", "Bait 1–2",
"This song has no verses") lives inside the Verses section with a separator below it.
**Preview**: static preview at `specs/210-song-verse-picker/preview/index.html`, portable
single file at `preview/song-verse-picker-preview.html`, accepted at gate 1 on 2026-11-21.
**Capability**: modifies `reading/R30` and `reading/R43`; adds `reading/R48`.

The song entry currently opens with a closed Song dropdown whose search box is only reachable
after a second click, and a Verses dropdown holding one native checkbox per verse, all ticked
by default. The owner's problem is concrete: finding a song means opening a menu before
typing, and picking verses means ticking small boxes one at a time. This slice makes the
search live from the first frame and rebuilds the verse control as a five-across tile grid
with press-and-drag ranges, while keeping the existing song data, query semantics, verse
IDs and save refusals exactly as they are.

## User Scenarios & Testing

### US1 — Song search is ready when the modal opens (P1)

**Why this priority**: it removes the extra click between deciding to add a song and typing
the song's name, which is the first thing the owner asked to change.

**Independent Test**: from the home page, click through to a service and use "+ Song"; the
search input already has focus, and typing `kj 12` narrows the grouped list to KJ 12, KJ 12a
and KJ 123 before any other click.

**Acceptance scenarios**

1. **Given** the Add song form has just opened **When** the operator types without clicking
   **Then** the Song search input receives the text and the result list narrows as it is typed.
2. **Given** a query that matches a hymn-book reference **When** results are listed **Then**
   they keep the product's existing book-first order, short-reference labels and 200-result
   cap, grouped under the book name.
3. **Given** a highlighted result **When** the operator presses Enter or taps the row
   **Then** the field becomes that song's label, the hidden song input holds its ID, and the
   verse section reveals for that song.
4. **Given** the result list is open **When** the operator presses Escape **Then** the list
   closes and the typed text stays in the input.
5. **Given** a query with no match **When** results render **Then** the list says "No songs
   match." and the modal's height is unchanged.

### US2 — Verses are ticked and ranged by one continuous gesture (P1)

**Why this priority**: the verse checklist was the first thing the owner called a hassle;
tapping large tiles plus one drag covers both a single verse and a stretch.

**Independent Test**: with a 12-verse song picked, click tile 4 → only verse 4 toggles; press
tile 2, drag to tile 5 and release → verses 2–5 are selected and the readout says so, with no
mark left on the tiles.

**Acceptance scenarios**

1. **Given** a fresh pick **When** the verse section appears **Then** only verse 1 is ticked.
2. **Given** any tile **When** it is clicked without dragging **Then** that one verse is
   ticked or unticked and no other verse changes.
3. **Given** a tile is held **When** the pointer is dragged across other tiles **Then** the
   whole stretch is tinted and the summary reads `Preview: Bait a–b · release to keep`,
   while the hidden verse values still hold their pre-drag set.
4. **Given** a drag is released **When** the form is read **Then** the stretch is committed as
   verse IDs, the tint becomes the normal ticked state, and no anchor ring or Esc hint remains.
5. **Given** every verse is ticked, or none is **When** the state settles **Then** All, or
   Clear respectively, is disabled.
6. **Given** an existing entry is edited **When** its form opens **Then** its saved verses
   stay ticked rather than resetting to verse 1.

### US3 — The verse section follows the chosen song (P1)

**Why this priority**: an empty or single-verse song should not offer a control that cannot
do anything, and the owner explicitly asked that the section be hidden in that state.

**Independent Test**: with no song, the Verses section measures 0px; picking a 12-verse song
reveals it with verse 1 ticked; picking a song with no verses collapses it to 0px again; a
one-verse song leaves one inert tile.

**Acceptance scenarios**

1. **Given** no song is picked **When** the form renders **Then** the whole Verses section is
   hidden, not merely disabled.
2. **Given** a song with no live verses **When** it is picked **Then** the section is hidden in
   the server-rendered fragment before any script runs, and Save still refuses with the
   existing named-song error.
3. **Given** a song with exactly one verse **When** it is picked **Then** one tile is drawn,
   the section is muted, and no range gesture is offered.
4. **Given** a song is picked or changed **When** the section appears **Then** it reveals in
   one 200 ms motion on the product's existing ease curve, with no second phase.
5. **Given** `prefers-reduced-motion: reduce` **When** the section appears **Then** it is
   painted in its final state without a transition.

### US4 — The Verses control reads as part of the form (P2)

**Why this priority**: the owner asked to keep the dropdown component but stop it looking
like one. A flat summary inside the section gives the name line a home without the old
boxed trigger and chevron.

**Independent Test**: in the approved preview's tab 6, the summary line is a child of the
Verses panel, has a 1px rule beneath it, and clicking it collapses only the tile block.

**Acceptance scenarios**

1. **Given** the Verses panel **When** it renders **Then** the summary line sits inside it,
   with a 1px separator between that line and the controls below.
2. **Given** the soft-trigger treatment **When** the summary is tapped **Then** only the tile
   block collapses; the summary stays visible.
3. **Given** the visible-panel treatment **When** it renders **Then** the tiles sit inside a
   bordered panel using the rail surface, with no dropdown chevron or floating menu.

### Edge Cases

- **When** the verses request fails **Then** the failure notice is shown and the section keeps
  the line it had; no partial tile state is committed.
- **When** a stored entry names verse numbers the song no longer carries **Then** those
  numbers stay choices and the entry stays saveable, as required by `reading/R30`.
- **When** the drag starts and ends on the same tile **Then** it is treated as a click.
- **When** a query matches no song **Then** the fixed results list shows the empty line and
  never changes the modal's height.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | The Song search input SHALL hold focus when the Add song form first renders, without a preceding trigger click; the Edit form SHALL NOT take focus into the Song field. Whenever the field gains focus its whole text SHALL be selected, so typing starts a new query. | `new: reading/R48` |
| FR-002 | Song results SHALL render in a fixed overlay anchored under the search input, capped only by the window edge, and SHALL be allowed to extend past the dialog's bottom edge. | `reading/R48` |
| FR-003 | The query grammar, hymn-first ordering, short-reference labels and 200-result cap SHALL stay as they are; no backend endpoint or schema changes in this slice. | `reading/R48` |
| FR-004 | Arrow keys SHALL move the result highlight, Enter SHALL pick it, Escape SHALL close the list and keep the text, and a tap SHALL pick on touch. | `reading/R48` |
| FR-005 | Picking a song SHALL write its ID to the hidden song input and show its reference-and-title label in the field. | `reading/R48` |
| FR-006 | The Verses section SHALL be part of the form's flow inside a 1px-bordered, 10px-padded panel on the rail surface, with its summary line inside the section as display text — not a control — and a 1px rule beneath both that line and the helper/All-Clear row, each with 8px to what follows; no dropdown chevron or floating verse menu SHALL be drawn. | `reading/R48` |
| FR-007 | The verse control SHALL draw five equal tiles per row, each 40px high and filling its column (81px at the 480px dialog), with 7px gaps and the helper/All/Clear row above the grid. | `reading/R48` |
| FR-008 | A fresh song pick SHALL start with verse 1 ticked; editing a stored entry SHALL preserve its saved verse set. | `reading/R48` |
| FR-009 | A click without drag SHALL tick or untick exactly one verse, and SHALL leave no ring behind (the ring is keyboard-only). | `reading/R48` |
| FR-010 | A held press-and-drag SHALL preview the whole stretch in the summary line until release (with an sr-only live region), write no form values during the preview, commit on release, and leave no persistent mark. | `reading/R48` |
| FR-011 | The hidden checkboxes SHALL keep submitting verse IDs, and the fetch SHALL keep returning `{id, number}` pairs. A server-rendered checklist — the Edit form, or an Add form returned by a refused save — SHALL already be the same five-across tile grid, without Django's own wrapper around it. | `reading/R43` (unchanged) |
| FR-012 | The summary SHALL state the chosen verses as `Bait` plus collapsed ranges (`Bait 1–3, 5, 8–10`), collapsing a pair too (`1–2`), and SHALL state the whole set rather than an `All verses` line when every verse is ticked. | `reading/R43` (modified) |
| FR-013 | All SHALL be disabled when every verse is ticked; Clear SHALL be disabled when none is ticked. | `reading/R48` |
| FR-014 | With no song, or a song with no live verses, the whole Verses section — its label included — SHALL be hidden, server-side for the first paint, while the existing save refusals stay in force. | `reading/R30` (modified) |
| FR-015 | A one-verse song SHALL show one inert tile in a muted section. | `reading/R48` |
| FR-016 | The section reveal SHALL last 200 ms on the product's existing ease curve, SHALL drop its clip and return to block layout once settled so no tile is ever cut, and SHALL be instant under reduced motion. | `reading/R48` |

### Key Entities

- **Song** — existing record; its ID, label and query semantics are unchanged.
- **Verse** — existing record; `{id, number}` remains the picker contract and IDs remain the
  submitted values.
- **ServiceEntry** — existing record; its stored verse-ID list and save guards are unchanged.
- **VersePickerState** — ephemeral: selected IDs, last tile, and the in-progress drag preview;
  it exists only in the form and is discarded when the dialog closes.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | Typing in the Song field needs zero prior clicks. | The input has DOM focus on the first frame after open. |
| SC-002 | A stretch of verses takes one drag instead of one click per verse. | One press-and-drag selects 2–5 with four IDs submitted. |
| SC-003 | The preview never writes a value the operator has not released. | Hidden verse values are unchanged while the drag is held. |
| SC-004 | Result count does not resize the dialog. | Dialog height is identical with 11, 3 and 0 results (516 px in the approved preview at 960×900). |
| SC-005 | No verse is offered for a song that cannot project one. | The section measures 0 px for no song and for a no-verses song. |

## UI/UX

Approved preview: `preview/index.html` (portable: `preview/song-verse-picker-preview.html`).
Tab 5 is the combined flow; tabs 1 and 6 are the two Verses treatments under comparison;
tabs 2–4 are earlier comparison models and are not part of this slice's design.

- **Layout / position**: 480px (30rem) dialog; five tiles per row under the summary; Song
  results in a fixed overlay anchored 6px below the input, with an 8px window edge and flip-up
  when the space below is under 150px. At 960×900 with all 11 sample results the overlay ends
  at y=892 while the dialog ends at y=885; the dialog stays 516px tall.
- **Size / spacing**: tiles 40px high and 81px wide (five equal columns of the 431px content row),
  7px gaps; quick actions 28px high and placed above the grid; summary 13px/1.3 with a 1px rule
  beneath it and 8px to the controls; soft-trigger variant has no box and no visible readout line.
- **Colour / typography**: product tokens only — `--ink`, `--head-ink`, `--rail-bg`,
  `--divider`, `--active-bg` (`#1C5C3C` light, `#7C9CF0` dark), `--active-ink`, `--danger`,
  `--focus`; tile ticks use the active pair, muted sections sit at 0.45 opacity.
- **States**: rest · hover (focus-colour border) · focus (2px focus ring) · ticked · range
  preview (30% focus tint) · soft-trigger collapsed (tiles hidden, summary visible) · disabled
  All/Clear · muted one-verse section · hidden no-song/no-verses section · invalid (none
  ticked) · song results empty · verse request failed · dark and light themes.
- **Motion**: one 200ms `cubic-bezier(.32,.72,.28,1)` reveal for the Verses section; no
  staged phases; no motion under `prefers-reduced-motion`. The preview's `Slow`/`S` control
  (900ms) is a review aid only and is not shipped.
- **Responsive**: dialog `min(30rem, 100vw - 32px)`; the five-column grid keeps 40px tiles by
  narrowing them at the 560px breakpoint; the results overlay follows the input on scroll and
  resize.

## Assumptions

- The song endpoint's text-matching, reference parsing, ordering, labels and 200-result cap
  are already accepted (`reading/R1`, `reading/R4`, specs 042/050/051) and are not changed.
- The board card for this demand is attached at delivery; no card ID is claimed in this Draft.
- The preview's sample songs are illustrative only; no song data is added to the product.

## Clarifications

### Session 2026-11-21

- Q: Verse picker or whole song entry? → A: the verse picker first, then the song picker;
  both in one slice.
- Q: Which picking gesture? → A: tiles with a plain click ticking one and a held press-and-drag
  extending.
- Q: Should the drag commit while the button is held? → A: no; preview it while held, commit
  on release, and leave no mark.
- Q: How many tiles per row? → A: five.
- Q: What should a song with no verses show? → A: hide the whole Verses section.
- Q: Should a one-verse song be muted? → A: yes, with its single tile visible but inert.
- Q: Should editing preserve saved verses? → A: yes; only a fresh pick defaults to verse 1.
- Q: What should the Verses control look like? → A: keep the component but make it read as a
  section: the summary line inside the section with a separator below it, no chevron or boxed
  dropdown menu.
- Q: Song search behavior? → A: the search field is focused and usable as the modal opens, and
  the result list may extend past the modal's bottom edge.
