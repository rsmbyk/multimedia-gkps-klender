# Feature Specification: passage entry's Book uses the song search field, Chapter and verse popovers gain in-menu filters

**Slice**: `specs/238-passage-search-pickers`
**Branch**: `feat/238-passage-search-pickers`
**Created**: 2026-11-24
**Status**: Draft → accepted at Gate 1; scope revised in review
**Input**: "can you make the book, chapter and from verse dropdowns in passage entry modal to use the same dropdown as the song picker dropdown in song entry modal" — revised in review to: "turn the chapter and from/to verse dropdown back to their previous version, but add a search filter inside the popout dropdown (just like the previous songbook dropdown)"
**Demand**: `ITEM-253` (new card)
**Capability**: `reading/R59` (new)
**Preview**: live preview at `http://127.0.0.1:8792/tatib/151/` — from `/`, click the Tata Ibadah rail, then the service `111ojo`; run `python specs/238-passage-search-pickers/preview/run.py runserver 0.0.0.0:8792 --noreload` from the slice worktree if the server is down.

The song entry's picker is a search field: its trigger is an `<input type="search">`, typing
replaces the query and filters results, Arrow Up/Down moves the active option, Enter chooses it
and Escape closes the menu. The passage entry's book, chapter and verse pickers were buttons with
a chevron; only the book had a filter, and that filter sat inside its popout menu.

**Scope as finally delivered**: Book became the search field (the song picker's combobox).
Chapter, From verse and To verse kept their original button triggers and popout menus; each of
those three menus gained a `type="search"` filter field above its options, matching the book
picker's original in-menu filter. The book → chapter → verse cascade, the translation toggle,
the hidden form values and the verse checklist are unchanged.

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
   books whose TB or SIM name or code contains "mat", and the empty hint appears when none match.
3. **Given** a visible book option **When** Enter is pressed or the option is clicked **Then** the
   field shows that book's name in the active translation, the menu closes, and the hidden
   translation-aware id is set.

### US2 — Chapter and verse popovers filter inside the menu (P1)

**Why this priority**: the owner's revised decision — keep the button popovers for the numeric
controls, but make their long lists searchable without converting their triggers.

**Independent Test**: choose a book, open Chapter's popover, type a number and check the visible
options; repeat for From verse and To verse; choose one and check the hidden select and cascade.

**Acceptance scenarios**

1. **Given** a book with 28 chapters **When** Chapter's popover is opened and `12` is typed into
   its filter **Then** only chapter 12 is visible and choosing it sets `chapter=12` and reloads
   that chapter's verses.
2. **Given** a chapter's verses **When** `1` is typed into From verse's filter **Then** only
   verses whose number contains 1 are visible, and choosing one sets `verse_start` and refreshes
   the To verse list.
3. **Given** a start verse with verses after it **When** To verse's filter is typed into **Then**
   only later verse numbers containing the query remain and choosing one sets `verse_end`.
4. **Given** an empty filter **When** it is cleared **Then** every option in that popover returns
   and its empty hint is hidden.
5. **Given** a numeric popover is opened **When** its options arrive **Then** the stored option —
   or the first one when nothing is stored — carries the active tint; ArrowDown/ArrowUp moves that
   highlight and scrolls the option list to keep it visible.

### US3 — The cascade, translation toggle and sibling controls are untouched (P1)

**Independent Test**: create and edit a passage in TB and SIM, switching translation and chapter,
and compare the POSTed payload and rendered stage reference with a baseline.

**Acceptance scenarios**

1. **Given** a stored SIM passage **When** its Edit modal opens **Then** Book's field shows the
   stored name and Chapter/From verse's button labels show the stored numbers, with the hidden
   selects holding the same ids as before this slice.
2. **Given** a chosen book **When** the TB/SIM toggle is used **Then** Book's label and options
   re-render in the new translation and the cascade reloads exactly as before.
3. **Given** any state **When** the chapter or verse popover is opened **Then** it keeps the
   original button geometry, chevron, disabled state and hover note.

### US4 — Keyboard, dismissal and single-menu rule (P2)

**Acceptance scenarios**

1. **Given** Book's menu is open **When** ArrowDown/ArrowUp are pressed **Then** exactly one
   visible option carries the active tint and Enter chooses it.
2. **Given** an open menu **When** Escape is pressed **Then** only that menu closes and the dialog
   stays open; a click outside the picker also closes it. Escape in Book does not clear the
   chosen label.
3. **Given** one picker's menu is open **When** any other picker in the modal is opened **Then**
   the first menu closes and only the newly opened one is visible.
4. **Given** a search dropdown with a highlighted option — or visible matches with none highlighted
   — **When** Tab is pressed **Then** that option is chosen and focus moves to the next field.
   This applies to Book, Song, the three in-menu filters, the OBS dock find and the projector
   find and entry-list comboboxes.
5. **Given** a long option list **When** ArrowDown/ArrowUp moves the highlight past the visible
   rows **Then** the menu scrolls just enough to keep the highlighted option inside its own
   scroll box, without scrolling the dialog underneath.

### Edge Cases

- A book with no translation in the active edition is disabled and cannot be chosen.
- A filter with no matches leaves the popover open with a "No matching chapters/verses" hint.
- A chapter with no verses, or a start verse that is the chapter's last, keeps From verse / To
  verse disabled as today.
- Editing keeps the stored values; focus does not reset the cascade to chapter 1.
- The menu stays anchored to its trigger while the dialog scrolls and flips up near the viewport
  bottom, as every picker does today.
- Filtered-out options must actually be hidden: the author `display` rule on
  `.editor__picker-option` needs an explicit `[hidden]` rule, or they stay painted but unclickable.
- Opening the numeric popovers via a button click focuses their in-menu filter, so typing filters
  immediately.
- With no visible match, Tab leaves the typed text alone and still moves focus to the next field.
- The next focus target is read *after* the choice, because a field such as Chapter only becomes
  enabled by choosing Book; option buttons inside a closing menu are never the next target.
- Scrolling is limited to `.editor__picker-options`; the dialog content must not move with it.
- The numeric popovers share the active-option helper: the highlight starts on the stored value,
  follows Arrow keys over visible options, and is what Tab commits.
- Enter in a numeric popover filter commits the highlight and closes only the menu: the filter sits
  inside the entry form, so without `preventDefault` the dialog would submit and close.

## UI/UX

Measured on the live preview at 1440×900, light theme (numbers frozen from the Gate 1 probe,
revised for the button popovers in review):

| Measurement | Song / Book search field | Chapter / From / To button trigger |
| --- | --- | --- |
| Trigger | `INPUT[type=search]` | `BUTTON.editor__picker-trigger` with chevron |
| Field height | 38px | 38px |
| Corner radius | 9px | 9px |
| Font | `500 14px/18.9px ui-sans-serif, system-ui, sans-serif` | same chrome family |
| Border / background at rest | `--divider` / `--rail-bg` | unchanged from before the slice |
| Menu width / radius / surface | 436px / 10px / `--canvas` on `--divider` | unchanged |
| Menu gap / cap | 6px below anchor, viewport-capped, flips up | unchanged |
| Filter location | in the trigger (Book and Song) | inside the popout menu, above the options |

The Book menu held 66 book buttons in two Testament groups at 462.13px tall in this window;
the Song menu held its fetched results at 419.88px. Both are capped to the room below the
anchor rather than to the dialog. Filtering "mat" left 2 books (Imamat, Matius). Book focus
selected the whole stored label (6 of 6 characters). After the review revision, typing `12` in
Chapter's in-menu filter left 1 visible option and chose hidden chapter `12` on the live page.

*(Numbers came from `preview/probe.py`, `preview/parity.py` and the live page.)*

## Requirements

### Functional Requirements

- **FR-001** Book SHALL be an `<input type="search">` using the song picker's `.editor__songsearch`
  chrome, with no filter input inside its menu.
- **FR-002** Typing in Book SHALL filter its options locally after a 140ms debounce by TB/SIM name
  or code; the Chapter, From verse and To verse menus SHALL each carry a `type="search"` filter
  that hides options whose `data-value` does not contain the query.
- **FR-003** Book's focus SHALL select the field's text; ArrowDown/ArrowUp SHALL move an active
  option and Enter SHALL choose it; Escape SHALL close only that menu without clearing the label.
  Tab SHALL choose the highlighted option, or the first visible match when none is highlighted,
  and then move focus to the next field, in every search dropdown the app offers.
- **FR-004** Choosing a book SHALL keep the translation-aware id lookup, group labels, chapter fill
  and verse load.
- **FR-005** Choosing a numeric option SHALL keep the existing hidden `<select>` values, verse
  reload and To verse refresh.
- **FR-006** The hidden selects SHALL remain the form's value carriers, so the POSTed payload and
  server validation are unchanged.
- **FR-007** Chapter, From verse and To verse SHALL keep their original button triggers, popout
  menus, disabled states and hover notes; only the in-menu filter is added.
- **FR-008** Menus SHALL remain viewport-capped and anchored to their trigger, and only one SHALL
  be open in the modal at a time.

### Success Criteria

- **SC-001** Book behaves like `#entry-song-search`; the three numeric popovers offer an in-menu
  filter over the same options they always showed.
- **SC-002** Create and edit of a passage in either translation post the same values as before.
- **SC-003** No new endpoint is added; filtering uses option data already in the modal.
- **SC-004** The song entry's picker and its verse checklist remain unchanged in behaviour.

## Assumptions

- "Same dropdown" was first confirmed as the full search-combobox interaction, then revised in
  review: only Book keeps that interaction; Chapter/From/To return to button popovers with an
  in-menu filter. Both decisions are recorded in this spec's Input line.
- "Previous songbook dropdown" means the filter-inside-the-popout pattern the book picker used
  before this slice — a search field above the options, no new keyboard contract.
- Filtering is client-side because the book list and generated chapter/verse lists are already in
  the modal; no server search endpoint is introduced.
- A typed Book query that is not chosen is left in the field on blur, matching the song picker;
  the hidden select remains the saved value.
- The keyboard highlight needs an `.is-active` tint; one shared rule now serves Book and Song.
- Escape in Book calls `preventDefault()` so it closes the menu without the native search-field
  clearing of a chosen label. The song picker's own handler is untouched.
- The song picker's own code is not refactored: it is green and pinned by spec 210.

## Known impact

`tests/e2e/test_entry_pickers.py` had its Book selectors migrated to the search field; the
Chapter and From verse selectors stay on their button triggers, with a shared
`[data-menu-anchor], [data-picker-trigger]` locator where a picker could be either. The module is
already red on develop (`ITEM-174` backdrop race), so its pass rate is not a regression signal;
the spec-210 song module is the green regression check.

## Open items

None. Both scope decisions (initial "same dropdown" answer and the review revision) are recorded;
the remaining choices are assumptions above.
