# Feature Specification: A song with no verses is named, not mistaken for no song

**Slice**: `specs/162-song-verse-empty-state`
**Branch**: `fix/162-song-verse-empty-state`
**Created**: 2026-10-29
**Status**: Accepted (owner, gate 1, 2026-10-29)
**Input**: "when a song does not have any verse, state it clearly" — with a screenshot of the New song
modal, `lagu kosong` picked, the Verses field reading `Pick a song first`, and the red line
`Keep at least one verse in the service.`

## What the form does today

The New song modal's Verses field is a picker whose trigger carries one summary line. The template
renders that line as a constant (`multimedia/web/templates/reading/_entry_form.html:208` —
`Pick a song first`), and `verseSummary` (`static/web/entries.js:663`) rewrites it from the only thing
it inspects, the checkboxes in `#entry-verses`:

```js
var boxes = box ? [].slice.call(box.querySelectorAll('input[type=checkbox]')) : [];
…
if (!boxes.length) {
  summary.textContent = 'Pick a song first';   // ← also the state of a song that has no verses
  trigger.disabled = true;
} else if (checked.length === boxes.length) {  // 'All verses'
```

A song whose live verses are empty answers the verses endpoint with an empty list —
`entry_song_verses` (`multimedia/web/reading/views.py:719`) returns `{"verses": [], "title": …}`, and
`loadVerses` (`static/web/entries.js:733`) draws no checkboxes. Zero boxes is therefore two different
worlds at once: **no song picked** and **a song picked that has no verses**. The form says the first
one in both, and the second is the one a person is actually in.

Measured on the live page (worktree 162, `/tatib/149/`, New song modal, 1440×900):

| state | Verses field | trigger | checkboxes | Save | after Save |
| --- | --- | --- | --- | --- | --- |
| nothing picked | `Pick a song first` | disabled | 0 | enabled | — |
| `lagu kosong` picked (pk 1906, no live verses) | `Pick a song first` | disabled | 0 | enabled | `Keep at least one verse in the service.` |
| `KJ 152` picked (three verses) | `All verses` | enabled | 3 | enabled | saves |

Both of the second row's lines misname the cause: the field says no song is picked when one is, and
the refusal says verses were removed when no verse ever existed. Seven songs in the local library
carry no live verses (`pk` 1774, 1852, 1886, 1905, 1906, 1879, 1731), so the state is reached by
picking a song in the normal way.

## User Scenarios & Testing

### US1 — the Verses field names a song that has no verses (P1)

**Why this priority**: it is the reported defect. The field's single line is the only thing that says
why the form cannot be finished, and today it says the opposite of what is true.

**Independent Test**: open New song, pick a song with no verses, and read the Verses field — it names
the song as the reason and the field is not offered for opening.

**Acceptance scenarios**

1. **Given** the New song modal and a song with no live verses picked, **When** the verses answer
   arrives, **Then** the Verses trigger reads `This song has no verses` and stays disabled.
2. **Given** the same modal and no song picked, **When** it opens, **Then** the trigger still reads
   `Pick a song first` — the line that is true there.
3. **Given** a song with verses, **When** it is picked, **Then** the field behaves exactly as today
   (`All verses`, one checked verse disabled, `Verses 1, 3`, `No verses: keep at least one`).
4. **Given** an entry being edited whose stored song has no live verses, **When** the modal fragment
   is rendered, **Then** the field carries the statement before any script runs — first paint is not
   `Pick a song first`.

### US2 — a save refusal names the song, not a removal (P2)

**Why this priority**: the person reaches Save after reading the corrected line, and the refusal is
the last place that can still tell them which song to change. It is a second line in the same story,
not a new behaviour.

**Independent Test**: with a verse-less song picked, press Save; the field's error names the song's
lack of verses. With a song that has verses and none checked, the existing error stands.

**Acceptance scenarios**

1. **Given** a song with no live verses picked, **When** Save is pressed, **Then** the Verses field's
   error says the song has no verses, and the dialog stays open with the entry unsaved.
2. **Given** a song with verses and every box cleared, **When** Save is pressed, **Then** the error
   is still `Keep at least one verse in the service.`

### Edge Cases

- **When** the song pick itself fails (the verses request errors) **Then** the existing failure toast
  stands and the field keeps its previous line; the statement is never shown for a failed load.
- **When** the entry stores verses that the song no longer has (an old entry, verses since deleted)
  **Then** those stored numbers are still choices, the field is in its normal state, and the
  statement does not appear — the entry can still be saved.
- **When** the song has exactly one verse **Then** the field reads `All verses` and is disabled, as
  today; the new statement is only for zero verses.
- **When** the picked song's verses are fetched again after a soft delete elsewhere **Then** the
  field states the new truth on that answer, with no stale `All verses` left behind.
- **When** the dialog is narrow (420px viewport) **Then** the statement stays on one line; it is
  shorter than the trigger's own width.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | The Verses trigger SHALL distinguish "no song picked" from "the picked song has no verses": the second state reads exactly `This song has no verses` | `new: reading` |
| FR-002 | The statement SHALL be present at first paint when editing an entry whose song has no live verses — rendered by the server, not only written by the script afterwards | `new: reading` |
| FR-003 | With a picked song that has no verses the trigger SHALL stay disabled, so an empty verse menu cannot be opened | `new: reading` |
| FR-004 | A save refusal caused by a picked song having no verses SHALL name the song; a refusal caused by clearing every box of a song that has verses SHALL keep `Keep at least one verse in the service.` | `new: reading` |
| FR-005 | Every other Verses-field line, state and geometry SHALL be unchanged: `Pick a song first`, `All verses`, `Verses n, …`, `No verses: keep at least one`, and the enabled/disabled rules that carry them | `new: reading` |

### Key Entities

- **Song** — the picked song; its verse numbers are the only source of the form's choices, and a song
  with none is the state this slice names.
- **Service entry (kind: song)** — stores the chosen verse numbers; it needs at least one, so a
  verse-less song can never complete one. Unchanged by this slice.
- **The Verses field** — one trigger, one summary line, one checkbox list; the state this slice adds
  is a sixth line for the picker's summary.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | In the New song modal, a picked song with no verses is identifiable from the Verses field alone, without pressing Save | the trigger's text differs from `Pick a song first` and names verses |
| SC-002 | The no-song state is not lost to the new one | the trigger reads exactly `Pick a song first` with no song picked, in the modal and on an edit form |
| SC-003 | The new line does not move the field | on the live page at 1440×900 the trigger reports 436×38 and at a 420 viewport 338×38, before and after; the summary measures 158.52×18.89 — one line |
| SC-004 | A person who presses Save anyway is told which song to change | the error names verses and the song, and the entry is not written |

## UI/UX

**Layout / position** — unchanged: the summary is the trigger's own first child
(`.editor__picker-trigger` > `[data-verses-summary]`), left-aligned inside a 436px-wide field in the
480px dialog (desktop) and 338px in the 382px dialog a 420px viewport gives.

**Size / spacing** — the trigger is 38px tall in every state, before and after. The approved line
measures 158.52×18.89 in the summary box — one line at 14px/18.9px, inside a 338px field on a phone,
so no wrap and no height change.

**Colour / typography** — the line keeps the disabled trigger's ink, `rgb(100, 99, 87)`, against the
enabled `rgb(31, 31, 29)`; font 14px, line-height 18.9px. No new colour is introduced and no weight
changes: the statement is quiet, because it explains a field rather than raising an error.

**States** — no song (`Pick a song first`, disabled) · song with verses (`All verses` or
`Verses n, …`, enabled; one verse: `All verses`, disabled) · every box cleared (`No verses: keep at
least one`, enabled) · song with no verses (the new line, disabled) · loading (the previous line
stands until the verses answer arrives) · fetch failure (toast, previous line kept) · error (the save
refusal names the song).

**Motion** — none. The line is replaced in place; there is no reveal, no animation and no layout
shift (the trigger's box is fixed at 38px).

## Assumptions

- The save refusal's words are `This song has no verses: pick another song.` — the field's own line
  first, so the two read as one statement, then the remedy that is one field away. —
- `Pick a song first` keeps its exact words and its disabled trigger; it is the true line for the
  no-song state and reads as the field's neutral opening. —
- The song list is not marked up: a verse-less song stays selectable and unannotated in the picker's
  options, because marking it would change a second surface and the field already states it once the
  song is picked. —
- `entry_song_verses` keeps returning `{"verses": [], "title": …}` — an empty list is the honest
  answer, and the fix is in how the form reads it. —
- The single-verse state (`All verses`, disabled) is not merged with the new one: one verse is a
  choice already made, zero verses is no choice at all. —
- Only the song form's Verses line is fixed — the modal's other kinds (passage, text, media) and the
  editor's other fields are untouched.

## Clarifications

### Session 2026-10-29

- Q: which line states a picked song that has no verses — *This song has no verses* / *No verses in
  this song* / *No verses to choose from*? A: `This song has no verses` (owner decision).
