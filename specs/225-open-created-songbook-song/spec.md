# Feature Specification: a newly created songbook or song opens as its row would

**Slice**: `specs/225-open-created-songbook-song`
**Branch**: `feat/225-open-created-songbook-song`
**Created**: 2026-11-23
**Status**: Accepted — Gate 1 and Gate 2, 2026-11-23
**Input**: "when you add a new songbook or song, it should be opened after created"
**Demand**: `ITEM-240`
**Capability**: `new: reading/R53`

Today a successful sidebar create only refreshes the lists: the new row appears, but nothing is
selected and the stage stays where it was. Live reproduction from this worktree's base commit
`e83e7154` (dev server `127.0.0.1:8768`, 1440×900) with an in-page marker set before the save:

- Before create: `path=/songs/`, `currentBook=null`, `currentSong=null`, `data-ch=closed`,
  `data-read=off`, marker `alive`.
- After creating a songbook: `path=/songs/`, `currentBook=null`, `data-ch=closed`,
  `data-read=off`, marker `alive`; the new row `/songs/book/38/` is in the panel but not current.
- After opening that row by hand: `currentBook="38"`, `data-ch=open` — the path stays `/songs/`,
  as the shell's in-place `lists` navigation keeps the book URL in history state.
- After creating a song in the open book: `path=/songs/book/38/`, `currentSong=null`,
  `data-read=off`, `#readName=""`; the new song row is in the child list but not opened.
- After opening that song row by hand: `path=/songs/1908/`, `#readName="Probe Song 396886"`,
  `currentSong` is the row, `data-read=on`, `data-ch=open`, marker `alive`.

The target state after each save is exactly the measured click-through state, reached without a
second click and without reloading the document.

## User Scenarios & Testing

### US1 — Creating a songbook opens it in the sidebar (P1)

**Why this priority**: a songbook exists to hold songs. After the save the row is in the panel but
no book is selected and the song list is still closed, so the operator has to find and click the
new row before they can add the first song.
**Independent Test**: on `/songs/`, create a songbook named `Ibadah Baru`; after the save resolves
the new row carries `aria-current="true"` and `data-ch=open`, with the empty song list visible, and
the in-page marker is still present. On the base commit no row is current and `data-ch=closed`.

**Acceptance scenarios**

1. **Given** the Kidung panel with no songbook open **When** a songbook is created from the panel
   Add button **Then** the new row is current in the panel, the child pane is open on that
   songbook's song list, and its empty state is shown when it has no songs.
2. **Given** another songbook is already open **When** a new songbook is created **Then** the new
   one becomes current, the previous row no longer is, and the child pane shows the new book's
   songs.
3. **Given** a successful create **When** the stage has settled **Then** the state matches a click
   on that songbook's row (URL kept in history state as `/songs/book/<id>/`, row current, child
   pane open), with no full document load.

### US2 — Creating a song opens it on the reading stage (P1)

**Why this priority**: the song list's Add action exists to get a song onto the stage. Today the
save only adds a row to the list; the heading stays blank and the reader cannot see or project the
song they just wrote.
**Independent Test**: with a songbook open, create a song titled `Kidung Baru`; after the save
resolves `location.pathname` is `/songs/<new id>/`, `#readName` is `Kidung Baru`, the new row is
current, `data-read=on`, and the marker survives.

**Acceptance scenarios**

1. **Given** an open songbook with its song list **When** a song is created from the list's Add
   button **Then** the song opens on the reading stage: its URL is `/songs/<id>/`, the heading is
   the entered title, its row is current, and `data-read=on`.
2. **Given** a song is already on stage **When** another song is created **Then** the new song
   replaces it on the stage in place; the previous song is no longer current.
3. **Given** a successful create **When** the stage settles **Then** the state matches a click on
   that song row, including the child pane remaining open on the parent songbook's list.

### US3 — Edits, refusals and other kinds keep their behaviour (P2)

**Why this priority**: the same save event carries edits, verse saves, Tata Ibadah saves and
already-navigating flows. Widening the new rule to those would move stages that have nothing to do
with a new songbook or song.
**Independent Test**: edit an existing songbook or song, create a Template, save a verse and submit
an invalid songbook form; each keeps today's list refresh and stage, and the refused form stays
open with its error.

**Acceptance scenarios**

1. **Given** an existing songbook or song **When** its name or title is edited **Then** no new
   selection or stage navigation happens; the current refresh path is unchanged.
2. **Given** a Template create, a verse save or a Tata Ibadah save **When** it succeeds **Then**
   the record follows its existing rules, including the created Normal service still opening on
   the stage (spec 209).
3. **Given** an invalid create form **When** the server answers with validation errors **Then**
   no navigation happens, the dialog stays open and the existing error rendering is unchanged.
4. **Given** a failed or refused save **When** no created record is returned **Then** the stage
   and the panel selection stay where they were.

### Edge Cases

- **When** the created songbook is the first in the list **Then** its empty song invitation is
  shown; no song is created by this slice.
- **When** the created song has no verses **Then** the song page's own verse state (spec 224 / R40)
  applies unchanged.
- **When** the first panel is collapsed or mini **Then** its `data-nav` state is not widened by the
  save; the new record is still current in its list.
- **When** a song is created from a hymn songbook **Then** no Add control is rendered there, so this
  slice changes nothing; hymn records stay uneditable.
- **When** the create response is slow **Then** no selection or stage change appears before the
  server confirms the record.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | A successful create of a non-hymn songbook SHALL open it the way its panel row does: the new row carries `aria-current="true"` and the child pane is open on that songbook's song list. | `new: reading/R53` |
| FR-002 | A successful create of a song SHALL open it the way its song row does: the URL becomes `/songs/<id>/`, the heading names the saved title, the row is current, and `data-read=on`. | `reading/R53` |
| FR-003 | Both opens SHALL use the reading shell's existing in-place navigation and SHALL NOT reload the document or change `data-nav`; the songbook open SHALL keep the stage as it is, and the song open SHALL keep the parent songbook selected. | `reading/R53` |
| FR-004 | Edits, verse and Tata Ibadah saves (including the created Normal service of spec 209), Template creates and hymn records SHALL keep their present behaviour. | `reading/R46`, `reading/R40` |
| FR-005 | A refused create SHALL NOT open a record and SHALL keep today's error handling. | `reading/R53` |

### Key Entities

- **Created record** — the `Book` or `Song` row whose id and kind arrive in the sidebar save
  response. No new field: the response already carries `id`, `kind` and `created`.
- **Reading shell** — the existing `/songs/book/<id>/` list selection (`lists` navigation) and
  `/songs/<id>/` song page (`song` navigation), reached through the shell's own navigation.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | After one songbook create the new row is current and the child pane is open, without a second click. | Playwright E2E reads `#panelBody .book[aria-current="true"][data-name]` and `document.documentElement.dataset.ch`. |
| SC-002 | After one song create the URL, heading, current row and `data-read` match the song just created. | Playwright E2E reads `location.pathname`, `#readName`, `.songrow[aria-current="true"]` and `data-read`. |
| SC-003 | Both opens are in place: no reload, no `data-nav` change. | E2E reads an in-page marker, `performance.timeOrigin` and `data-nav` before and after. |
| SC-004 | Edits, other kinds and refused creates behave as on the base commit. | Focused E2E assertions plus the existing editor/module suites. |

## UI/UX

`n/a — no new look. Both destinations are existing pages reached by the same in-place navigation a
row click uses; no control, style, spacing or motion is added.`

Gate-1 material is the measured reproduction above, taken on the base commit with
`reproduce.py` in this folder (dev server on `127.0.0.1:8768`). The target states are the measured
click-through states from `probe_click.py`.

## Assumptions

- "Opened" means the same result as clicking the new row, as the owner chose on 2026-11-23: the
  songbook is selected with its songs listed; the song is on the reading stage.
- "After created" means on the successful save response, before any further click, but not before
  the server has confirmed the record.
- Only the sidebar create paths are involved; verse creation and the Tata Ibadah paths keep their
  own navigation rules.
- No new model, field or endpoint: the save response already distinguishes a create (`created`)
  from an edit and names the kind and id.

## Clarifications

### Session 2026-11-23

- Q: What should "opened" mean for a new songbook or song? → A: Like clicking the new row — the
  songbook is selected with its songs listed, the song is on the reading stage (owner decision).
- No other open questions remain.
