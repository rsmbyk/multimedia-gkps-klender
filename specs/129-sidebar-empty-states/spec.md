# Feature Specification: The sidebars say which nothing they show

**Slice**: `specs/129-sidebar-empty-states`
**Branch**: `fix/129-sidebar-empty-states`
**Created**: 2026-10-25
**Status**: Accepted (owner, gate 1, 2026-10-25; the spec, plan, tasks and analysis pack accepted at
gate 2 the same day)
**Input**: "fix the "No matching sections." (image 1), "No matching songs.", "No matching Tata
Ibadah." (image 2) position (also any other similar texts/views in the sidebars). center vertically and
horizontally in the sidebar and add an icon above it. also differentiate between empty (no data) and not
found (match nothing in the search filter)." (sent with three screenshots of `localhost:63404`: an empty
Tata Ibadah whose section list says `No matching sections.` at the pane's bottom-left, the Kidung sidebar
saying `No matching songs.` the same way, and the Tata Ibadah panel saying `No matching Tata Ibadah.`
after a query `qq`.)

*Sequencing note*: the owner asked for the fix in a working session, so the branch already carries the
implementation and the reference preview is the running branch. Gate 1 still decides whether the copy and
the numbers below are the ones to keep; the plan, tasks and convergence record are written against this
spec.

## User Scenarios & Testing

### US1 — A list with nothing in it is centred and says what it is (P1)

**Why this priority**: this is the defect in the screenshots. Both columns render their "empty" line as the
last flex child of the pane, so it sits at the bottom-left, unreadable as a state and easy to mistake for a
footer.

**Independent Test**: open a Tata Ibadah with no sections and a songbook with no songs; in each the second
column shows one block — glyph, title, hint — on the centre of the list pane, above nothing else.

**Acceptance scenarios**

1. **Given** a Tata Ibadah with no sections, **When** its page opens, **Then** the sections pane shows a
   glyph, `No sections yet.` and `Add the first item to start preparing the service.`, centred in the pane.
2. **Given** a songbook with no songs, **When** its page opens, **Then** the songs pane shows a glyph,
   `No songs yet.` and `Add the first song to this songbook.`, centred in the pane.
3. **Given** any first column (books, songbooks, Tata Ibadah services) with no rows, **When** the page
   opens, **Then** that column's block is centred and names its own list.

### US2 — A filter that matched nothing says so, differently (P1)

**Why this priority**: today both cases print the same sentence, so a genuinely empty list reads as a
failed search and an operator keeps retyping a filter that was never the problem.

**Independent Test**: on a page whose list has rows, type a query that matches nothing: the block keeps its
place and switches its glyph, its title and its hint to the search miss; clear the field and the block
disappears.

**Acceptance scenarios**

1. **Given** a Tata Ibadah with sections, **When** the sections filter matches nothing, **Then** the block
   reads `No matching sections.` / `Try a different search.` under the miss glyph.
2. **Given** the same list, **When** the filter is cleared, **Then** the block is not shown at all.
3. **Given** a section whose list is empty and a filter typed anyway, **When** the filter matches nothing,
   **Then** the block still reads the empty copy: the emptiness was never the filter's doing.
4. **Given** the first column filtered to nothing, **When** the section is Kidung or Tata Ibadah, **Then**
   the title names that column's list (`No matching songbooks.` / `No matching Tata Ibadah.`).

### US3 — The saved copy types the same two lists (P2)

**Why this priority**: a saved page is rebuilt from the cached home shell, whose blocks are the Bible's; if
the renderer does not re-label them, an offline Kidung or Tata Ibadah page shows the Bible's copy under the
wrong glyph.

**Independent Test**: render a Kidung and a Tata Ibadah route from the saved library and read the two
blocks' copies and glyphs: they match the server route's.

**Acceptance scenarios**

1. **Given** a synced library, **When** a Kidung or Tata Ibadah route is rendered from it, **Then** both
   blocks carry that section's empty title, empty hint, filter title and empty glyph.
2. **Given** the same library, **When** the rendered page's list holds rows, **Then** no block is shown.
3. **Given** a section whose list has no rows, **When** the saved page is the final page offline, **Then**
   it shows the empty copy, not the filter's.

### Edge Cases

- **When** the panel is collapsed to its mini rail **Then** no block is shown: an 80px column cannot hold a
  two-line state, and the rail's filter is not offered there.
- **When** the Bible's chapter list is open **Then** the block stays hidden: chapters are never filtered, and
  a book with no text at all is a property of the edition, not of a search.
- **When** the operator deletes the last entry of a Tata Ibadah **Then** the sections block reads the empty
  copy without a reload.
- **When** the page is read by a screen reader **Then** the block announces itself as a status and is not
  focusable.
- **When** the pointer is over the block **Then** the wheel still scrolls the list beneath it.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | Each of the two sidebar lists renders one empty-state block, absolutely positioned over that list's scroll pane, its visible content centred horizontally and vertically on the pane. | `reading/R7` |
| FR-002 | The block shows a glyph above a title above a hint; the title and the hint are separate elements. | `reading/R7` |
| FR-003 | The block is typed: with no rows in the list it shows the empty copy, with rows present but none matching it shows the filtered copy, and with at least one matching row it is not shown. | `reading/R7` |
| FR-004 | Each section's copy names its own list, in both columns: books, songbooks, Tata Ibadah; songs, sections. | `reading/R7` |
| FR-005 | The empty copy carries the section's own list glyph; the filtered copy carries a magnifier with a cross inside it. | `reading/R7` |
| FR-006 | A page that arrives with an empty list shows the empty copy before the first keystroke. | `reading/R7` |
| FR-007 | Matching rows, an in-page navigation or a cleared filter hide the block; an arriving page's copy and glyph replace the live ones before the arriving filters are applied. | `reading/R7` |
| FR-008 | The saved renderer writes the section's copy and glyph into both blocks, whichever route it is rebuilding. | `reading/R2` |
| FR-009 | Deleting a Tata Ibadah entry that was the list's last row shows the empty copy. | `reading/R7` |
| FR-010 | The block is hidden in the collapsed mini panel and in the Bible's chapter list. | `reading/R7` |
| FR-011 | The old bottom-left paragraphs (`.panel__empty`, `.ch__empty`) and their rules are gone; no page renders either. | `reading/R7` |

### Key Entities

- **Empty-state block** — one per list; identity `#panelEmpty` (first column) and `#chEmpty` (second
  column); carries `data-empty-title`, `data-empty-hint`, `data-filter-title`, `data-filter-hint`, two glyph
  spans keyed `data-when="empty"` / `data-when="filter"`, and a live `data-state` (`empty` or `filter`).
  Never persisted; composed at render time and typed in the browser.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | The block's ink is centred on its list pane | measured in Chromium at 1440×900 on four states: vertical and horizontal offsets ≤ 1px |
| SC-002 | Empty and filtered read differently | four readings (`No sections yet.` / `No matching sections.`, `No songs yet.` / `No matching songs.`) in the browser and in the rendered markup |
| SC-003 | One sentence per list, per column | the four section resolutions for both columns, read from the served HTML |
| SC-004 | The saved render writes the same copy | saved renderer output compared with the server route's copy and glyph for Kidung and Tata Ibadah |
| SC-005 | Nothing else moves | the reading-page suite and the sidebar fixture tests stay green |

## UI/UX

- **Layout / position**: the block spans its list pane — `inset: 0` on `#panelEmpty` inside
  `.panel__scrollwrap`, on `#chEmpty` inside `.ch__wrap` — so it is centred on the rows' area, not on the
  column (the ~63px filter strip above never pushes it off-centre). `pointer-events: none`.
- **Size / spacing**: glyph 38×38 at stroke 1.5; 8px grid gap; title margin-top 2px; hint `max-width: 26ch`
  with `text-wrap: balance`; block padding 0 20px.
- **Colour / typography**: glyph and hint `--head-ink` (#646357 light, #9C9A91 dark), glyph at `opacity:
  .85`; title 14px/600 `--ink`; hint 13px/1.4.
- **States**: empty (section glyph) · filtered (magnifier with a cross) · hidden (any match). Focus, hover,
  active, disabled and error do not apply: the block is not a control.
- **Motion**: none — the block appears and disappears with the list it belongs to.
- **Responsive**: hidden at the collapsed mini panel (`[data-nav="mini"] .panel .listempty`); in the narrow
  phone drawer the block keeps the same centring inside the drawer.

## Assumptions

- **One filter hint for every list** — `Try a different search.` — because the miss always has the same
  remedy; the empty hint is per list because the invitation differs.
- **The empty copy is an invitation, not a repeat of the stage** — `No sections yet.` rather than the stage's
  `This Tata Ibadah is empty.`, so the sidebar names its own list.
- **The glyphs are the rail's own iconography** for the three sections, and a new magnifier-with-cross for
  the miss — no new icon set, no illustration.
- **The block is not a control**: no button, no link, nothing to click; the remedy is the filter field above
  it and the add controls in the same toolbar.
- **A list that is both empty and filtered keeps the empty copy**: the filter did not empty it.

## Clarifications

### Session 2026-10-25

- Q: (not asked) whether the empty state should offer an add action → SKIPPED, assumed: no, the toolbar's
  add control is one row above and a second one would duplicate it.
- Q: (not asked) whether the sections list should repeat the stage's `This Tata Ibadah is empty.` → SKIPPED,
  assumed: no; the sidebar names its own list, `No sections yet.`
