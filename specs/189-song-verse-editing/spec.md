# Feature Specification: an ordinary song's verses are added, edited, removed and reordered on its page

**Slice**: `specs/189-song-verse-editing`
**Branch**: `feat/189-song-verse-editing`
**Created**: 2026-11-05
**Status**: Accepted (Gate 1, 2026-11-09)
**Input**: *"i wanna add the features to add, edit, and remove non-hymn song verses. also the ability to reorder the verses. i want these to be doable in song page"* — with two rulings from the owner in Clarify: *"the service store the references (IDs) and display the current (order of) verse number of the verse. when the verse is reordered, the displayed verse number changes, but the references stays. a verse referenced in a service cant be deleted."*

## What the song page does today

`/songs/<song_id>/` renders a song's live verses in `number` order, one `<p class="v">` per verse —
the position in `.v__n` (`forloop.counter`), the lyric `linebreaksbr`-joined beside it
(`multimedia/web/templates/reading/song.html`). The page has no verse control of any kind.

A **lyric verse** (`songs.Verse`) carries a song, a number and a lyric. The only live writer is the
REST resource `/api/songs/verses/`; its own page, `/manage/songs/songs/<id>/`, still loads
`static/web/songs/verses/index.js`, a file this repo does not contain — the management screen is dead.
The sidebar editors (spec 005) add and rename songbooks and songs, never verses, and they refuse a
hymn songbook outright. A hymn song's verses are therefore read-only by decision, and an ordinary
song's verses have no live editor at all.

Every ordinary song's live verses are numbered `1…n` with no gap (281 songs; 7 have none), so today the
position the page prints and the number a service entry stores are the same fact.

## What a Tata Ibadah stores today, and what changes

A **song entry** names the verses it will project by *number*: `ServiceEntry.verses` is a JSON list of
integers (`multimedia/tatib/models.py:193`), the entry form offers the song's numbers as checkboxes
(`multimedia/web/reading/entries.py:125–143`), and everything downstream filters `number__in=entry.verses`
— the stage's `Bait …` line, the entry's body, the projector's screens. A number is therefore an ordinal
used as an identity, and the two agree only while nothing reorders the song.

This slice separates them, as the owner ruled:

| Before | After |
| --- | --- |
| `ServiceEntry.verses` holds verse **numbers** | holds verse **IDs** |
| the entry's label is the stored numbers | the label is the **current** number of each stored verse |
| `number__in=…` resolves the entry | `pk__in=…` resolves the entry, ordered by the verse's current number |
| a reorder would silently repoint a prepared service | a reorder changes the displayed numbers; the reference does not move |

Measured on the local library: 448 entries name a verse of an ordinary song (433 exactly one, 12 two,
3 three), and a migration mapping each stored number to that song's live verse with the same number
covers all of them — no stored number names a deleted verse (0 rows).

The legacy **setlist** rows (`SongBookmarkItem.verse`, comma-separated numbers, 829 items naming an
ordinary song) deliberately stay number-based: the owner's ruling is that they may show a different
stanza after a reorder. They are outside this slice's writes and reads.

## User Scenarios & Testing

### US1 — a verse is added on the song page (P1)

**Why this priority**: it is the request's first verb, and the only way to give the seven verse-less
ordinary songs a lyric without a dead screen or the raw API.

**Independent Test**: open an ordinary song, press `Add verse`, type a lyric, save — the verse appears
last with the next number, and the page is still the song's page.

**Acceptance scenarios**

1. **Given** an ordinary song with three verses, **When** the reader presses `Add verse`, **Then** the
   editor modal opens titled `New verse` with an empty `Lyrics` field and the focus in it.
2. **Given** the modal is filled with a three-line lyric, **When** Save is pressed, **Then** the verse is
   written, the page re-reads, and a fourth verse numbered `4` holds those three lines — no reload.
3. **Given** a song with no verses, **When** its page opens, **Then** the stage offers its empty
   invitation and `Add verse`, and the first save numbers the verse `1`.

### US2 — a verse's lyric is edited on the song page (P1)

**Why this priority**: the same screen has to carry the correction, or every typo means the dead
management page.

**Independent Test**: hover a verse, press its edit control, change a line, save — the row shows the new
text with the same number and nothing else moves.

**Acceptance scenarios**

1. **Given** an ordinary song, **When** the pointer is over a verse (or focus is inside it), **Then**
   its grip and edit control are visible and reachable; at rest neither is painted.
2. **Given** verse `2` and the edit control pressed, **When** the modal opens, **Then** it is titled
   `Edit verse` and the field holds that verse's lyric, with the caret at the end.
3. **Given** a changed lyric, **When** Save is pressed, **Then** the same verse keeps its number and
   shows the new text, and the song's title, songbook and other verses are untouched.

### US3 — the verses are reordered on the song page (P1)

**Why this priority**: it is the second half of the request, and it is what makes the hand-entered
order correctable at all.

**Independent Test**: grab verse 3's grip and drag it above verse 1, release — the list collapses for
the gesture and expands again, the page reads `1, 2, 3` top to bottom with their lyrics moved, and a
service entry that named the old verse 1 still projects that same lyric, now labelled with its new
number.

**Acceptance scenarios**

1. **Given** an ordinary song with four verses, **When** a verse's grip is grabbed, **Then** the list
   collapses to one-line rows for the length of the gesture — number, one line of lyric, the grip — the
   row in hand lifted on a fill and a shadow, and the rows it passes sliding one slot each.
2. **Given** the verse has been dropped, **Then** the list expands again to the full stanzas, the order
   is written at once (no Save, no mode, no confirmation), and the numbers read `1…4`.
2. **Given** a service entry naming two verses of that song, **When** the song is reordered, **Then** the
   entry still projects the same two lyrics, and its `Bait …` line now reads their current numbers.
4. **Given** a drag that ends where it started, **When** the pointer is released, **Then** nothing is
   written and no toast appears.
5. **Given** the song's page at rest, **Then** there is no mode control, no arrow button and no key
   handler for reordering — the grip is a pointer gesture only (owner decision).
6. **Given** a row the carried verse passes, **Then** it travels exactly one slot, once: it is never
   thrown further and never slides back.

### US4 — a verse is removed, and only when nothing projects it (P2)

**Why this priority**: deletion is the destructive verb; it must exist, but it must never leave a
prepared service naming a lyric that is gone.

**Independent Test**: open a verse named by a service entry — the dialog offers no delete; open an
unreferenced verse — `Delete verse` asks once and removes it.

**Acceptance scenarios**

1. **Given** the edit modal for a verse that no service entry names, **When** `Delete verse` is pressed,
   **Then** one confirmation names the verse and the song, and accepting removes it, renumbers the rest
   `1…n`, and re-reads the page.
2. **Given** the edit modal for a verse that a service entry names, **Then** the delete action is
   disabled and the modal states how many Tata Ibadah name a verse of this song, so the person knows
   where to go first.
3. **Given** the confirmation, **When** Cancel is pressed, **Then** the verse is unchanged and the modal
   stays open.

### US5 — a prepared service keeps its lyrics across the four verbs (P1)

**Why this priority**: it is the ruling that makes the other four safe; without it a reorder silently
rewrites a service that is already prepared.

**Independent Test**: with a service entry naming verses 1 and 3, add, edit and reorder the song; the
entry's resolved body is unchanged, and its label follows the new numbers.

**Acceptance scenarios**

1. **Given** an entry naming two verses, **When** a third verse is added before them, **Then** the entry
   still projects its two lyrics and its label reads their new numbers.
2. **Given** an entry naming a verse, **When** that verse's lyric is edited, **Then** the entry projects
   the corrected lyric — the reference is to the verse, not to a copy of its text.
3. **Given** an entry naming a verse, **When** the verse's row is dragged elsewhere, **Then** the entry's
   reference is untouched and its displayed number changes with the verse.
4. **Given** any entry, **When** the migration runs, **Then** every stored number becomes that song's
   live verse with the same number, and a number naming no live verse is dropped.

## Edge Cases

- **When** the page is a hymn song's **Then** no verse control is drawn and every endpoint refuses it —
  the rule spec 005 set, enforced on the server as well as in the template.
- **When** editing is restricted (`SIDEBAR_EDITORS_REQUIRE_LOGIN` on, anonymous reader) **Then** no
  verse control is drawn; the endpoints answer 403 without writing.
- **When** a lyric is blank or whitespace only **Then** the save is refused with the field's own error,
  the modal stays open, and nothing is written.
- **When** two pages edit the same verse and the later save names a verse that is no longer live
  **Then** the save is refused as stale, the page re-reads, and the person sees the current lyric.
- **When** a reorder's list does not match the song's live verses (a verse was added or removed
  elsewhere) **Then** the write is refused whole, nothing is renumbered, and the page re-reads.
- **When** the song or its songbook is deleted while the page is open **Then** the endpoints answer 404
  and the page's next read leaves the stage.
- **When** a verse's lyric is one very long unbroken run **Then** the row wraps inside the stage's text
  column, as the reading text already does.
- **When** a verse is a single short line **Then** its tools still stand in the gutter: the 42px stack
  overhangs the 36.8px row by 2.6px top and bottom, into the neighbouring gutter's blank, and the
  lyric column still does not move.
- **When** a drag ends outside the list, on a link, or the page navigates mid-drag **Then** the drag is
  cancelled, the list expands again, and nothing is written.
- **When** a song's verses are longer than the stage **Then** the collapsed list is shorter than the
  full one — eight stanzas of 271.9px collapse to a 392px list — and the stage scrolls under the
  pointer when it comes within 72px of the top or bottom.
- **When** a grip is grabbed and the pointer is held still **Then** the order is unchanged — the
  collapse alone never reorders — and the verse is written where it stands when the pointer is
  released.
- **When** a service entry is open in the editor while its song's verses are reordered elsewhere
  **Then** the form's checkboxes are the song's current verses on its next load, and a save from a stale
  form is refused by the form's own choice validation.
- **When** a verse's lyric is edited while its service is on air **Then** the display keeps what it
  loaded; it re-reads on its next display write, as it already does after any entry save (research:
  `static/web/projector.js` `reflow()`).

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | The song page SHALL render verse controls only when the song belongs to an ordinary songbook and editing is allowed; a hymn song's page SHALL render none. | `reading/R40` |
| FR-002 | The page SHALL offer one add control after the last verse; pressing it SHALL open the shared editor modal titled `New verse` with an empty `Lyrics` field. | `reading/R40` |
| FR-002a | The add control SHALL start on the lyric column, not the verse gutter, and SHALL be drawn as a dashed row — dashed because it is still to be added, the rule the Tata Ibadah slots follow. | `reading/R40` |
| FR-003 | Saving a new verse SHALL append it to the song, numbered one past the last live number, and the stage SHALL show it without a reload. | `reading/R40` |
| FR-004 | Each verse row SHALL offer an edit control and a reorder grip, painted only while the row is hovered or focus is inside it; the edit control SHALL open the same modal titled `Edit verse <number>`, prefilled with that verse's lyric. | `reading/R40` |
| FR-004a | The tools SHALL stand at the top of the verse's own number gutter and the number SHALL yield it to them while they are up, so the lyric column keeps its exact width and position in every state. | `reading/R40` |
| FR-005 | Saving an edit SHALL replace only that verse's lyric; the verse keeps its number and every other record is untouched. | `reading/R40` |
| FR-006 | The grip SHALL reorder by pointer drag only — no mode control, no arrow button, no key handler. Grabbing a grip SHALL collapse the verses to one-line rows for the length of the gesture and restore them when it ends; a completed drop SHALL write the order at once, with no Save and no confirmation. | `reading/R40` |
| FR-006a | A collapsed row SHALL be 44px: the verse's number kept, its lyric cut to one line with an ellipsis, a hairline between rows, and the grip at the row's right. | `reading/R40` |
| FR-006b | The row in hand SHALL ride the hand as a ghost copy following the pointer one to one (service sidebar's shape, `static/web/reorder.js`), carried by a fill on `--rail-bg` and a shadow under it — never a 1px ring. The real row SHALL stay in flow as a tinted placeholder with its contents hidden. | `reading/R40` |
| FR-006c | The numbers SHALL renumber as the row crosses, not on release, so the order being made is the order being read (spec 081's rule for the Tata Ibadah order). | `reading/R40` |
| FR-006d | The reorder SHALL move one row per crossing — the rows it passes travelling exactly one slot, once, with no rebound — and SHALL scroll the stage when the pointer nears its edge. | `reading/R40` |
| FR-006e | The list SHALL stay at its normal place for the whole gesture — no shifting. The other rows' midpoints SHALL freeze at the grab (Sidebar's frozen rule); the slot the dragged row holds SHALL be the first frozen middle the **current** cursor height has not yet passed, evaluated each move. The slot SHALL NOT be derived from the origin slot or from travel since the grab: if the cursor is below the frozen midpoint of verse 4 the target is after verse 4, wherever the grip was first taken. | `reading/R40` |
| FR-006f | The grip SHALL be hittable at rest: the tools may be painted only on hover, but the press that starts a drag SHALL NOT need one first. When a song has only one verse the grip SHALL render disabled — one verse has nowhere to move. | `reading/R40` |
| FR-006h | The hairlines SHALL belong to the list, not to the row in hand: while a verse is being carried the card SHALL draw no line of its own, the slot it was lifted from SHALL keep a seam above it and below it, and the lines on screen SHALL be exactly the seams of the order being shown — one per row boundary, none following the card. | `reading/R40` |
| FR-006g | The row in hand SHALL read `from→now` in its own number column — the number the verse was taken from and the number it holds at that moment — so the order as it stood before the grab stays on screen for as long as the gesture lasts. | `reading/R40` |
| FR-007 | On any reorder the live verses SHALL be renumbered `1…n` in their new order, and the page SHALL show the new numbers without a reload. | `reading/R40` |
| FR-008 | A service entry SHALL name its verses by **ID**: `ServiceEntry.verses` SHALL store verse IDs, and the entry's label, body and projected screens SHALL use each referenced verse's **current** number, in that number's order. | `reading/R40` |
| FR-009 | The migration SHALL convert every stored verse number to the ID of that song's live verse with the same number; a stored number naming no live verse SHALL be dropped. | `reading/R40` |
| FR-010 | A verse that any service entry references SHALL NOT be deletable; the edit modal SHALL disable the delete action — drawn neutral rather than as a faded danger — and state how many Tata Ibadah name a verse of this song. | `reading/R40` |
| FR-011 | Deleting an unreferenced verse SHALL soft-delete it, renumber the remaining verses `1…n`, and re-read the page. | `reading/R40` |
| FR-012 | After any add, edit, delete or reorder, the song's live verses SHALL be numbered `1…n` with no gap and no duplicate. | `reading/R40` |
| FR-013 | Every endpoint SHALL enforce its own rules — ordinary songbook only, live song only, POST with the CSRF token, a permutation of the song's live verses, verse IDs that belong to the named song — whatever the modal sends. | `reading/R40` |
| FR-014 | A write SHALL leave every field outside its own subject unchanged: the song's title, songbook and number, and the lyrics of verses it did not name. | `reading/R40` |
| FR-015 | The legacy setlist rows (`SongBookmarkItem.verse`) SHALL NOT be migrated or written by this slice, and their API shape SHALL NOT change. | `reading/R40` |
| FR-016 | The service entry's verse picker SHALL carry each verse's **ID** as its value and that verse's **current number** as its label, and its summary line (`Verses 1, 3`, `All verses`) SHALL read the same numbers — one reading of `verses`, not three. | `reading/R40` |

### Key Entities

- **Song** — `songs.Song`; the page's subject. This slice reads its songbook's `is_hymn_book` and never
  changes the song's own fields.
- **Lyric verse** — `songs.Verse`: song, number, lyric, and the soft-delete triple. Its number is its
  position in the song; after this slice the two are the same fact on every write.
- **Service entry (kind song)** — `ServiceEntry.verses` becomes a list of verse IDs. A reference names a
  lyric verse; the number it is called by is read from that verse.
- **Setlist item** — `SongBookmarkItem.verse`, comma-separated numbers. Unchanged, and allowed to drift
  from the song's numbering after a reorder (owner decision).
- **The verse row** — `.v`, the grid of number and text the stage already draws; the unit the controls
  attach to. Collapsed for a reorder gesture it becomes a one-line row, and it is restored from the
  page's own markup, byte for byte, when the gesture ends.
- **The editor modal** — the one `<dialog>` every sidebar editor opens (spec 005); this slice adds a
  fourth kind to it.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | An ordinary song's verse can be added, edited, removed and reordered from its own page, and the page never reloads for any of them | a Playwright walk of the four verbs on one song page |
| SC-002 | A reorder leaves the page reading `1…n` in the new lyric order | the row numbers and the lyric text compared before and after |
| SC-003 | A service entry that named a verse projects the same lyric after the song is reordered, and its label shows the new number | the entry's resolved body and `Bait …` line before and after, on a fixture song |
| SC-004 | A hymn song's page draws zero verse controls, and its endpoints refuse a write | a rendered-page assertion and four refused requests |
| SC-005 | A verse named by a service entry cannot be deleted, and the modal says how many services name the song | the disabled action and its line, against a fixture count |
| SC-006 | No write can leave an ordinary song's live verse numbers out of `1…n` | the database after each verb in the walk |
| SC-007 | Every pre-existing service entry resolves to the same lyric text after the migration | a fixture of ten entries compared before and after the migration |

## UI/UX

Measured on `preview/index.html` with `preview/probe.py` at 1440×900 and 420×900, dark and light. The
preview is the product's own page — its shell, verse text, stylesheets and editor dialog — with this
slice's controls drawn over it; `preview/README.md` lists what is simulated.

**Layout / position**

- **At rest the page is unchanged**: the read article is 520px at x = 856 inside a 648px stage, a
  four-line verse is 520 × 137.6, the number column is 41.6px, the lyric column starts at x = 900 and
  is 476px wide. The one new thing is `Add verse`, 111.8 × 38, starting on the lyric column (x = 900),
  not the gutter.
- **The tools live at the top of the number's gutter**: two 20 × 20 buttons, 2px apart, stacked, 2px below the
  top of the verse so the stack aligns with the first line (a 42px stack at x = 866.8). While they are up the number yields the gutter; at rest they are at
  opacity 0 and cannot take a click.
- **The add row is the Tata Ibadah platform's dashed row**: 1px dashed
  `color-mix(--focus 42%, --divider)`, 9px radius, `+` glyph and `Add verse` at 13px/600.
- **The editor dialog is the shared one**: 480 × 352.3 at (480, 273.9) — title 436 × 42, the `Lyrics`
  textarea 436 × 150, the actions row 436 × 55, `Save` 66.6 × 38, `Cancel` 81.6 × 38. Focus lands in
  the textarea with the caret at the end.
- **The confirmation replaces the dialog's body**, as `entries.js` already deletes: a 436-wide block
  holding the question, one line of consequence, and `Cancel` / `Delete` 38px tall, right-aligned.
- **The empty song** draws the app's own `.entry__empty` invitation — a 365.5 × 128 block centred in
  the stage, title 20px/600, hint in `--head-ink`, one `Add verse` — and nothing else.

**Size / spacing** — every number above is measured; the controls add no box to the page at rest, so
the lyrics' own rhythm (1.6px row padding, 33.6px line height) is untouched. A one-line verse is a
36.8px row and the 42px tool stack overhangs it by 2.6px top and bottom — into the neighbouring
gutter's blank, with no visible collision (measured, the `short` state).

**Colour / typography** — nothing new is introduced. The number and the tool glyphs are `--head-ink`
(`rgb(156,154,145)` dark, `rgb(100,99,87)` light); a tool's own hover is `--icon-hover-bg` with `--ink`
glyphs; the add row's ink is `--head-ink` turning `--ink`, its dash `color-mix(--focus 42%,
--divider)`; the disabled `Delete verse` is `--divider` + `--head-ink` (neutral, never a faded danger),
its reason a 12px/18px help line. The lyric keeps its 18.88px/33.6px `ui-serif` face, the number its
11px/590 sans.

**States** — rest · hover (the number yields the gutter, 120ms fade in after 90ms) · focus-visible (a
2px `--focus` ring on each tool) · grabbing (the list collapses; the row in hand on `--rail-bg` and a
shadow, the rows it passes sliding one slot) · dropping (expanded again 170ms later, renumbered at
once) · saving (the shared toast and
dialog-busy state) · `New verse` · `Edit verse n` · `Edit verse n` with `Delete verse` disabled and
its count · `Delete verse n?` · empty song · hymn song and restricted reader (no control at all) ·
stale write (refused, the page re-reads).

**The reorder, measured** — a collapsed row is **44px**: the number in the same 2.6rem gutter, its
line-height raised to fill the row; the lyric cut to one line (`white-space: nowrap`, ellipsis) at
14px serif; the grip at the row's right with the pencil hidden; a 1px `--divider` hairline between
rows. The row in hand is `--rail-bg` with `0 14px 30px -16px var(--backdrop)` — **no ring**. Eight
stanzas of 271.9px collapse to a **392px** list, all in view, against 2200.3px expanded and ~3.3 rows
in view at 1440×900. The row in hand reads `2→2` the moment it is grabbed and `2→8` five slots later,
inside the same 41.6px number column (the readout ends 2.4px short of the lyric column, so the text
never moves). Traced through a slow drag (`Drag trace`, 14 independent checks per run) that walks the live cursor down the compact list: every
check compares the live cursor height against the frozen grab midpoints of the
other verses (`indexFollowsTravel:
true` — the slot the hand is over is the slot the verse holds, 14/14); every row it
passed travelled **exactly one slot — −43.5 / −44 of 44px — once**; the row it never reached travelled
0; **reversals: 0**. The lines are checked the same way (`seamsOk: true` — the drawn hairlines must
equal the seams of the order on screen: 271/315/359/403/447/491/535 for eight 44px rows, none missing,
none doubled). Both checks are known to fail on the versions they guard: `indexFollowsTravel: false`
when the slot is read from live-reflowed goalposts instead of the frozen grab lines, `seamsOk: false` when the carried
row keeps its own `border-top` (measured: a stray line 2px below the slot's own seam, which then
vanishes from the slot). The ghost rides the hand 1:1 throughout (`cardInSlot: true` — top plus grab offset equals the live pointer), matching the service sidebar's `reorder__ghost`.

The seam above the slot is marked by the engine on the row directly before it, not by a
`:has(+ .is-dragging)` sibling rule: a sibling rule holds for a verse dropped in the middle of the
list but silently stops matching when it is dropped at the **end**, where the row above is no longer
the card's previous sibling — measured as a missing seam (`seamsOk: false`, drawn 6 lines against 7
expected). Auto-scroll begins within 72px of the stage's top or
bottom edge.

**Motion** — the tools fade in over 120ms with a 90ms delay and out at once; the list collapses at the
start of a gesture and is restored 170ms after the drop; the rows a crossing moves slide on a 150ms
curve; the carried row settles on a 160ms one. No other transition is added.

**Responsive** — at 420×900 the read column is 384 wide, the gutter 27.2, the lyric column 354.4 at
x = 47.6, `Add verse` at x = 47.6, the tools still 20px wide centred in the narrower gutter, and the
dialog 382 wide with a 338-wide field (Chrome caps a `<dialog>` at `calc(100vw - 6px - 2em)`).

Two states are **not** reachable by hand in the static preview, and are this slice's E2E instead:
`saving` (the shared toast and dialog-busy frame) and a stale write's refusal. A static page cannot
show either — they are requests.

## Assumptions

- **The four verbs live on the stage itself**, not behind a second list or a separate screen: the row
  that shows a lyric is the row that edits it. — the request's own words, and the owner's choice in
  Clarify.
- **`Add verse` is one control after the last verse**, not one between every pair: verses are appended
  and then moved, and a seam control on every gap would double the count of controls on the page.
- **The number is the position.** A reorder renumbers, a delete compacts, an add appends. — every
  ordinary song's live verses are already `1…n`, and the page has always printed the position.
- **A reference names a verse, not an ordinal**, so it survives a reorder and always displays the
  current number. — the owner's ruling; it is also what makes a prepared service safe.
- **The reorder is pointer-only**, by the owner's decision: no arrow buttons and no key handler. This
  departs from the grip-with-arrows grammar the Tata Ibadah order uses (`static/web/reorder.js`), and
  the deviation is deliberate.
- **Grabbing a grip collapses the list for the gesture** — the alternative, a `Reorder verses` mode
  with its own button and hint line, was built and rejected by the owner. The mode asks the reader to
  leave the page to change it; a gesture that begins where the verses are and ends by itself does not.
  The rejected design's cost is recorded: the reading view changes under the pointer mid-gesture.
- **The list stays put and the hand decides.** The gesture does not shift the list to meet the pointer and does not remember the origin slot: the slot is read from the live cursor height against the live other-verse midpoints each frame, so after the collapse a pointer that is still where it grabbed a middle stanza (well below the 44px rows) reads as past the last verse. — owner decision 2026-11-09: *current cursor, not original verse position*; consequence recorded rather than hidden.
- **The FLIP snapshot is keyed by the row element, never by an attribute.** Two rows sharing a key
  collapse the snapshot and throw every row the list's whole height and back — a shake on every
  crossing, measured at 13 reversals per row before this was fixed.
- **A referenced verse's delete is disabled rather than refused after the press**, with the count on
  screen: the modal should say why before the person tries. It is drawn neutral, because a red
  outline at half opacity still reads as an action.
- **The verse's number yields its gutter to the tools while they are up.** The gutter is 41.6px, two
  24px targets do not fit across it, and a second column would shorten every ordinary song's lyric
  line. The number is repeated in the dialog's title (`Edit verse 3`), so nothing is lost.
- **The legacy setlists stay number-based and may drift.** — the owner's ruling; they are the retired
  surface, and their API shape does not change.
- **The editor modal is the one spec 005 built**, with `verse` added as a fourth kind: one dialog, one
  fetch-and-revalidate path, one toast, one focus restore. — a second modal would be a second set of
  those behaviours.
- **Hymn songs keep their read-only rule.** — spec 005's decision, unchanged by this slice.
- **The verse picker's "This song has no verses" line (spec 162) is left as it is.** This slice gives
  that state a way out — the page's `Add verse` — but does not change the entry form's words.
- **The dead management screen is not revived or repaired.** — it points at a script the repo does not
  contain; this slice gives the verbs a live home instead.
- **A verse edit does not write the display state**; a display already showing the service re-reads on
  its next display write, as it does after any entry save. — researched in `static/web/projector.js`
  (`reflow()`), not assumed.

## Clarifications

### Session 2026-11-05

- Q: what should happen to the verse numbers a service entry or setlist stores when the song is
  reordered? → A: service entries store verse **IDs** and display the verse's current number; the
  reference never moves. A verse referenced in a service cannot be deleted. (owner decision)
- Q: do the legacy setlist rows follow the same rule? → A: no — they stay number-based, and a reorder
  may change what they show. (owner decision)
- Q: where do the verse controls live? → A: on the verses themselves on the song page — a grip and an
  edit control per row, one `Add verse` row after the last verse, delete inside the edit dialog.
  (owner decision)
- Q: how is reordering operated? → A: drag only, no keyboard control. (owner decision)
- Q: with long verses, which reorder — a `Reorder verses` mode that collapses the list until Done,
  or grabbing a grip, which collapses it for the gesture? → A: **the grab** — B in the preview. The
  mode was built, measured and rejected: it asks the reader to leave the page to change it. What B
  costs, recorded rather than hidden: the reading view changes under the pointer until the drop.
  (owner decision, 2026-11-06)
