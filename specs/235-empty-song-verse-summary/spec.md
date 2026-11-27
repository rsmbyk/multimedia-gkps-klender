# Feature Specification: An empty song names itself in the Verses section

**Slice**: `specs/235-empty-song-verse-summary`
**Branch**: `fix/235-empty-song-verse-summary`
**Created**: 2026-11-24
**Status**: Accepted (Gate 1 2026-11-24; Gate 2 2026-11-24)
**Input**: "when picking an empty song (no verses) in new/edit song entry modal, display the verse picker section, but only the summary row part that states that the song has no verses"
**Demand**: `ITEM-250` (new card)
**Capability**: modifies `reading/R30` and `reading/R48`
**Preview**: `specs/235-empty-song-verse-summary/preview/index.html`

## What the product does today

Spec 210 chose to hide the whole Verses section for a song with no live verses
(`reading/R30`, `reading/R48`; FR-014, SC-005). The server renders the panel with
`hidden` and the summary line `This song has no verses` *inside* it, so the sentence is in
the markup but never painted. `verseSummary()` in `static/web/entries.js` re-hides the
panel whenever the checklist has no boxes (`shouldHide = !songPicked || !boxes.length`) and
the CSS hides the section's label alongside the hidden panel. The save refusal still names
the song, so the only thing missing is the visible statement.

This slice **reverses spec 210's answer to "what should a song with no verses show?"** —
from *hide the whole Verses section* to *show the section, collapsed to its summary row*.
Nothing else about the picker, the other states, or the save rules changes.

## User Scenarios & Testing

### US1 — A verse-less song is named where the verse picker was (P1)

**Why this priority**: the operator picks an empty song and the field silently disappears;
the only wording that explains why is in the server response and a Save error. Showing the
section's own summary line in place answers "why is there nothing to tick?" before Save is
ever pressed.

**Independent Test**: from the app's home URL, open a service, choose Add Song, search for a
song with no verses and pick it: the Verses label and a small bordered section appear, the
section's only line reads `This song has no verses`, and there are no tiles, helper text or
All/Clear buttons. Open the Edit modal of an existing song entry whose song has no verses and
read the same state before any script runs.

**Acceptance scenarios**

1. **Given** the Add song modal with no song picked **When** it opens **Then** the whole
   Verses section, its label included, is hidden and measures 0 px — unchanged.
2. **Given** a song with no live verses **When** it is picked **Then** the Verses label and
   the verse panel are shown, and the panel's only visible content is the summary line
   `This song has no verses`.
3. **Given** that state **When** the panel is inspected **Then** it has no checkbox, no tile,
   no helper line, no All/Clear buttons and no bottom rule under the summary.
4. **Given** an Edit modal for a song entry whose song has no verses, or an Add form returned
   by a refused save **When** the fragment arrives **Then** the same visible state is already
   in the markup, with no script run.
5. **Given** the state **When** Save is pressed **Then** the refusal is still
   `This song has no verses: pick another song.` and the dialog stays open.

### US2 — The full picker still works for songs that have verses (P2)

**Why this priority**: the change is scoped to one state; the 200 ms reveal, five-across
tiles, drag range, muted one-verse song and the two save refusals must not drift with it.

**Independent Test**: pick a song with verses after a verse-less one and measure the panel:
the helper row, All/Clear and the tile grid appear, verse 1 is ticked, and the summary reads
`Bait 1`; clearing every box still reads `No verses: keep at least one`.

**Acceptance scenarios**

1. **Given** a verse-less pick **When** a song with verses is picked **Then** the section
   shows the full picker with verse 1 ticked, without leaving an empty-state mark behind.
2. **Given** a song with many verses **When** tiles are picked **Then** the summary, All/Clear
   enablement, drag preview and submit values are byte-identical to today.
3. **Given** a song with exactly one verse **When** picked **Then** the section is muted with
   one inert tile, as today.
4. **Given** no song is picked after a verse-less song **When** the field is cleared **Then**
   the section returns to 0 px.

### Edge Cases

- **When** the verse-list request fails while a verse-less song is already picked **Then**
  the existing failure notice is used and the empty-state line is not mistaken for a
  successful empty result.
- **When** a song's verses were deleted after an entry was saved **Then** the empty-state
  summary shows on Edit, and the saved verse IDs are not silently rewritten.
- **When** reduced motion is on **Then** the new state has no reveal animation, as today.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | With a picked song that has no live verses, the Verses section SHALL be visible in both Add and Edit song entry modals: its label and its 1px-bordered, 10px-padded rail-surface panel are drawn, and the panel's only visible content SHALL be the summary line reading exactly `This song has no verses`. | `reading/R30` (modified) |
| FR-002 | In that state the helper/All–Clear row, the tile grid and the readout SHALL NOT be visible, and the summary SHALL NOT draw a bottom rule or bottom spacing, because no content follows it. | `reading/R30` (modified) |
| FR-003 | The state SHALL be present in the server-rendered fragment before any script runs, including the Add form returned by a refused save, and SHALL be re-derived on every later pick. | `reading/R30` (modified) |
| FR-004 | With no song picked the whole Verses section and its label SHALL stay hidden at 0 px. With a song that has verses, the section, reveal motion, tiles, summary and All/Clear rules SHALL be unchanged. Switching directly between the two song states SHALL leave no mark or stale value from the previous one. | `reading/R30`, `reading/R48` (modified) |
| FR-005 | The save refusals SHALL stay `This song has no verses: pick another song.` for a verse-less pick and `Keep at least one verse in the service.` for a cleared checklist. | `reading/R30` (unchanged) |
| FR-006 | No other surface SHALL change: the song page's empty invitation, the service row, the projector and the OBS dock keep their current no-verses behavior. | `reading/R30` (unchanged) |

### Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | An empty song is named without pressing Save | The visible panel contains only the line `This song has no verses` in Add and Edit. |
| SC-002 | No unusable control is offered for an empty song | Zero visible checkboxes, tiles, helper text or All/Clear buttons in that state. |
| SC-003 | The no-song and full-picker states do not regress | 0 px with no song; the full tile grid, first verse ticked and 200 ms reveal with a song that has verses. |

## UI/UX

- **Current**: the whole `Verses` field (label + `.editor__verse-panel`) is `hidden`, measuring
  0 px; the sentence exists only inside the hidden panel.
- **Proposed**: the `Verses` label renders as it does for a song with verses; under it the
  panel keeps its rail surface, 1px `--divider` border and 10px padding, and holds one line —
  `This song has no verses` — in `600 13px/1.3` `--ink`, its bottom rule and 8px bottom
  spacing dropped because nothing follows. The panel's height is that one line plus its
  10px padding top and bottom.
- **States**: no song (hidden, 0 px, label hidden) · verse-less song (label + summary-only
  panel) · full picker (unchanged) · one verse (unchanged, muted) · failed verse fetch
  (unchanged failure notice) · dark and light themes.
- **Motion**: the existing 200 ms `cubic-bezier(.32,.72,.28,1)` reveal still carries the
  no-song → song transition. The empty ↔ populated swap has no separate staged animation;
  the body rows appear or disappear in the same frame the pick lands. Reduced motion keeps
  every transition instant.

## Assumptions

- "Verse picker section" means the field's label plus the bordered `.editor__verse-panel`;
  "only the summary row part" means its `.editor__verse-summary` line, not a bare sentence
  floating in the form.
- The summary's bottom rule is a separator between it and the rows below; with those rows
  hidden, it is dropped rather than left dangling.
- No reveal animation is added for the empty ↔ populated swap; one frame, no phases.
- The song page's `This song has no verses yet.` invitation (spec 189) is a different surface
  and is untouched.
- The capability tree records this as a modification of `reading/R30` and `reading/R48`,
  with spec 210's superseded note updated rather than deleted.
