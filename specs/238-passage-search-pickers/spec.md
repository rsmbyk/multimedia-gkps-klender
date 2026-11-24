# Feature Specification: passage entry's book, chapter and from-verse use the song search dropdown

**Slice**: `specs/238-passage-search-pickers`
**Branch**: `feat/238-passage-search-pickers`
**Created**: 2026-11-24
**Status**: Draft — Gate 1 pending
**Input**: "can you make the book, chapter and from verse dropdowns in passage entry modal to use the same dropdown as the song picker dropdown in song entry modal"
**Demand**: `ITEM-253` (new card)
**Capability**: `reading/R59` (new)
**Preview**: live preview at `http://127.0.0.1:8792/tatib/<service>/` — from `/`, click the Tata Ibadah rail, then `Add Passage`; run `python <worktree>/run.py runserver 0.0.0.0:8792 --noreload` from the slice worktree if the server is down.

The song entry's picker is a search field: its trigger is an `<input type="search">`, typing
replaces the query and filters results, Arrow Up/Down moves the active option, Enter chooses it,
Escape closes the menu, and the menu is anchored to the field and capped to the viewport. The
passage entry's book, chapter and from-verse pickers are buttons with a chevron; the book hides
its filter *inside* the menu and chapter/verse have no filter at all. The three controls therefore
read, behave and are driven differently from the song picker in the same family of dialogs.

This slice makes book, chapter and from-verse **the same search combobox as the song picker** —
same field chrome, type-to-filter, keyboard selection and viewport-capped menu — while keeping
the existing book → chapter → verse cascade, the translation toggle, the hidden form values, and
the optional "To verse" control exactly as they are.

## User Scenarios & Testing

### US1 — Book is searched by typing (P1)

**Why this priority**: it is the reported surface. The book list runs to a couple of hundred
names across two translations and two Testament headings; a chevron button with a filter buried
in its menu makes the first field feel different from the Song field beside it in the same UI.

**Independent Test**: open Add Passage, focus the Book field, type a name or code in either
translation, and check that only matching options remain and choosing one fills the field.

**Acceptance scenarios**

1. **Given** an open passage modal **When** Book is focused **Then** the field's text is selected
   and its menu is open with the full book list, grouped by Testament.
2. **Given** "mat" is typed **When** the debounce settles **Then** the visible options are the
   books whose TB or SIM name or code contains "mat", in both translations where present, and
   the empty hint appears when none match.
3. **Given** a visible book option **When** Enter is pressed or the option is clicked **Then** the
   field shows that book's name in the active translation, the menu closes, and the hidden
   `book_translation` value is the id for that translation.

### US2 — Chapter and from verse take the same combobox (P1)

**Why this priority**: these are the other two controls named in the request, and the chapter
and verse lists are generated locally rather than supplied by the server, so they must filter
over those same lists without changing the cascade that produces them.

**Independent Test**: pick a book, type into Chapter and From verse, and check the filtered
options, keyboard selection and resulting form values.

**Acceptance scenarios**

1. **Given** a book with 28 chapters **When** "12" is typed into Chapter **Then** only chapter 12
   remains and choosing it sets `chapter=12`, keeps the book, and reloads that chapter's verses.
2. **Given** a chapter's verses **When** "7" is typed into From verse **Then** only verses whose
   number contains 7 remain and choosing one sets `verse_start` and refreshes the To verse list.
3. **Given** an empty query **When** either field gains focus **Then** every option appears again.

### US3 — The cascade, translation toggle and sibling controls are untouched (P1)

**Why this priority**: these pickers are the front end of a value cascade; changing their trigger
must not change what is saved or what happens when a book, chapter or translation changes.

**Independent Test**: create and edit a passage in TB and SIM, switching translation and chapter,
and compare the POSTed payload and rendered stage reference with a baseline.

**Acceptance scenarios**

1. **Given** a stored SIM passage **When** its Edit modal opens **Then** all three fields show the
   stored values in SIM, and the hidden selects hold the same ids as before this slice.
2. **Given** a chosen book **When** the TB/SIM toggle is used **Then** the Book field's label and
   the book list re-render in the new translation and the cascade reloads exactly as before.
3. **Given** any state **When** the pointer is away **Then** To verse remains a button picker with
   its "No ending verse" state and hover note, unchanged.

### US4 — Keyboard and dismissal match the song picker (P2)

**Why this priority**: the shared dropdown's promise includes its keyboard contract; a field that
looks right but does not answer Arrow/Enter/Escape is not the same dropdown.

**Independent Test**: drive a field with ArrowDown, ArrowUp, Enter and Escape and check the active
option, the chosen value and the menu's visibility.

**Acceptance scenarios**

1. **Given** an open menu **When** ArrowDown/ArrowUp are pressed **Then** exactly one visible
   option carries the active tint and Enter chooses it.
2. **Given** an open menu **When** Escape is pressed **Then** only that menu closes and the dialog
   stays open; a click outside the picker also closes it.
3. **Given** one picker's menu is open **When** any other picker in the modal is focused or its
   button is clicked **Then** the first menu closes and only the newly opened one is visible.
4. **Given** a chosen value **When** the field is focused again **Then** its text is selected so
   typing starts a new query instead of appending to the chosen label.

### Edge Cases

- A book with no translation in the active edition is disabled and cannot be chosen.
- No matching options leaves the menu open with the same hint the book filter already used;
  chapter/verse state their own "No matching chapters." / "No matching verses." hint.
- A chapter with no verses, or a start verse that is the chapter's last, keeps From verse / To
  verse disabled as today.
- Editing keeps the stored values; focus does not reset the cascade to chapter 1.
- The menu stays anchored to the field while the dialog scrolls and flips up near the viewport
  bottom, as every picker does today.
- Only one menu may be open in the modal: opening a search combo closes any other picker's menu,
  and opening the To verse button picker closes a search combo.

## UI/UX

Measured on the live preview at 1440×900, light theme, with the passage modal open.
`parity.py` measures the same properties on `#entry-song-search` in the song modal:

| Measurement | Song picker | Book / Chapter / From verse |
| --- | --- | --- |
| Trigger element | `INPUT[type=search]` | `INPUT[type=search]` (all three) |
| Field height | 38px | 38px |
| Field width in a single-field row | 436px | 436px (Book, Chapter); 213px (From verse, half of a two-field row, as before) |
| Corner radius | 9px | 9px |
| Font | `500 14px/18.9px ui-sans-serif, system-ui, sans-serif` | identical |
| Border / background at rest | `--divider` (`rgb(217,214,205)`) / `--rail-bg` (`rgb(237,234,227)`) | identical |
| Border on focus | `--focus` (`rgb(28,92,60)`) | identical |
| Menu width / radius / surface | 436px / 10px / `--canvas` on `--divider` | identical |
| Menu gap below anchor | 6px | 6px |
| Menu cap | viewport-capped, flips up near the bottom | identical |
| Chevron glyph | none (search field) | none — the down-chevron is gone from all three |

The Book menu held 66 book buttons in two Testament groups at 462.13px tall in this window;
the Song menu held its fetched results at 419.88px. Both are capped to the room below the
field rather than to the dialog. Filtering "mat" left 2 books (Imamat, Matius); filtering
"1" in Imamat left 12 chapters and 11 verses. One option at a time carried the active tint
after ArrowDown, and focus selected the whole stored label (6 of 6 characters).

*(Numbers came from `preview/probe.py` and `preview/parity.py` against the live slice.)*

## Requirements

### Functional Requirements

- **FR-001** The Book control SHALL be an `<input type="search">` using the song picker's
  `.editor__songsearch` chrome, with no filter input inside its menu.
- **FR-002** Typing in any of the three fields SHALL filter its options locally after a 140ms
  debounce, by TB/SIM name or code for Book and by number substring for Chapter/From verse.
- **FR-003** Focus SHALL select the field's existing text; ArrowDown/ArrowUp SHALL move an active
  option, Enter SHALL choose it, Escape SHALL close only that menu.
- **FR-004** Choosing a book SHALL keep the existing translation-aware id lookup, group labels,
  chapter fill and verse load.
- **FR-005** Choosing a chapter or from verse SHALL keep the existing hidden `<select>` values,
  verse reload and To verse refresh.
- **FR-006** The hidden selects SHALL remain the form's value carriers, so the POSTed payload and
  all server validation are unchanged.
- **FR-007** To verse, the translation toggle and every other modal control SHALL be unchanged.
- **FR-008** The menu SHALL remain viewport-capped and anchored to the field, and stay attached
  while the dialog scrolls.

### Success Criteria

- **SC-001** All three fields answer focus, type-to-filter, keyboard selection and Escape the way
  `#entry-song-search` does.
- **SC-002** Create and edit of a passage in either translation post the same values as before.
- **SC-003** No new endpoint is added; filtering uses option data already in the modal.
- **SC-004** The song entry's picker and its verse checklist remain byte-identical in behaviour.

## Assumptions

- "Same dropdown" means the full search-combobox interaction and field styling, confirmed by the
  owner at the start of the slice.
- "To verse" is deliberately out of scope: the request named exactly Book, Chapter and From verse,
  and To verse keeps its button picker, optional state and hover note.
- Filtering is client-side because the book list and generated chapter/verse lists are already in
  the modal; no server search endpoint is introduced.
- A typed query that is not chosen is left in the field on blur, matching the song picker's
  behaviour; the hidden select remains the saved value.
- The keyboard highlight needs an `.is-active` tint; the class was already applied by the song
  picker but had no rule, so one shared rule is added and both pickers gain the visible cue.
- Escape calls `preventDefault()` in the new combos so it closes the menu without the native
  search-field clearing of the chosen label. The song picker's own Escape handler is untouched.
- The passage modal does not grab focus for Book on open, unlike the song modal's spec-220
  behaviour; auto-focusing a field before the translation toggle is a separate change.
- The song picker's own code is not refactored: it is green and pinned by spec 210, so the shared
  interaction is mirrored in a helper for the passage fields rather than rewiring a passing path.

## Known impact

`tests/e2e/test_entry_pickers.py` still clicks `#entry-book-trigger`, `#entry-chapter-trigger`
and `#entry-verse_start-trigger`, which no longer exist, and uses `[data-picker-trigger]` on
those three pickers. Those selectors must be migrated to the new search fields. That module is
already pinned on the board as red on develop (`ITEM-174` backdrop race), so its pass rate is
not a regression signal on its own; the spec-210 song module is the green regression check.

## Open items

None. The one ambiguity (what "same dropdown" means) was answered before this spec was written;
the scope choices above are recorded as assumptions.
