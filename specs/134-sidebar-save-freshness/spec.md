# Feature Specification: Keep reading views current after sidebar edits

**Slice**: `specs/134-sidebar-save-freshness`
**Branch**: `feat/134-sidebar-save-freshness`
**Created**: 2026-10-26
**Status**: Accepted
**Input**: “when i edit a tataibadah, the changes are not reflected immediately. i need to reopen the sidebar or refresh the page for it to change. can you also check for similar behavior on all pages?”

## User Scenarios & Testing

### US1 — An edited record updates every visible reading view (P1)

**Why this priority**: An operator needs to see that a save took effect before continuing. A current
stage beside a stale sidebar row makes the saved data look inconsistent and invites a second edit.

**Independent Test**: Open a Tata Ibadah, change its name in the first sidebar, and save. Without
reloading, reopening the sidebar, or navigating away, the sidebar row and stage heading show the new
name.

**Acceptance scenarios**

1. **Given** a Tata Ibadah is open, **When** its name is edited from the first sidebar and saved,
   **Then** its first-sidebar row and stage heading show the saved name in the same page session.
2. **Given** a song is open, **When** its title is edited from the second sidebar and saved,
   **Then** its second-sidebar row and stage heading show the saved title, and the document title stays
   the header-derived one `reading` R1 gives every song page.
   *(Superseded 2026-10-26: this scenario originally required the document title to show the saved song
   title. A song page's tab follows its header — the songbook citation — so that clause contradicted
   `reading` R1; the owner kept R1 and amended this scenario.)*
3. **Given** a song is open, **When** its songbook name is edited from the first sidebar and saved,
   **Then** the first-sidebar row, songbook heading, and document title show the saved name.
4. **Given** a Bible chapter is open and the Kidung sidebar is selected, **When** a songbook is edited
   and saved, **Then** the songbook row shows the saved name and the Bible stage stays on the same
   chapter.

### US2 — Search results reflect edits made from an open sidebar (P1)

**Why this priority**: Search results remain visible while operators browse another section. A stale
result can lead the operator back to an outdated title even after the sidebar and server have changed.

**Independent Test**: Search for a song, open its songbook and song sidebars, edit the song while the
matching result remains on screen, and verify the result uses the saved title without a full-page reload.

**Acceptance scenarios**

1. **Given** a search result matches a song, **When** the song title changes and still matches the query,
   **Then** the result shows the saved title and the result count reflects the current data.
2. **Given** a search result matches a song, **When** the song title changes so it no longer matches
   the query, **Then** the result disappears and its group count is updated while the query and current
   search page remain in place.

### Edge Cases

- **When** a sidebar filter matches a row before an edit but not after it, **Then** the updated list
  applies the existing filter to the saved value without clearing the filter.
- **When** a sidebar is open, mini, or closed at save time, **Then** its current state is preserved.
- **When** a save is rejected, **Then** the editor keeps its current validation behavior and no visible
  reading content is changed to an unsaved value.
- **When** an entry inside an open Tata Ibadah is edited, **Then** the current in-place entry refresh
  continues to update the stage and contents list.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | After a successful sidebar edit of a Tata Ibadah, song, or songbook, every currently visible reading-shell representation of that record SHALL show the server-saved values without a page reload, sidebar reopen, or additional navigation. | `new: reading` |
| FR-002 | A successful edit SHALL update the relevant sidebar row and, when the edited record is represented in the current stage, its stage heading and the document title that route renders. An unrelated stage SHALL remain on its current content and route. | `new: reading` |
| FR-003 | When search results are open, a sidebar edit SHALL refresh the current result set using its existing query. A result that still matches SHALL show current values; a result that no longer matches SHALL be removed, and affected group counts SHALL be current. | `new: reading` |
| FR-004 | An in-place save refresh SHALL preserve the current search query, selected record, sidebar open/mini/closed states, filters, scroll positions, and keyboard focus, except when an edited row no longer matches an active filter or search query. | `new: reading` |
| FR-005 | Failed editor submissions SHALL retain the existing validation and error behavior and SHALL NOT publish unsaved values to the reading view. | `new: reading` |
| FR-006 | Existing service-entry save behavior SHALL continue to update its Tata Ibadah stage and contents list in place. | `new: reading` |

### Key Entities

- **Visible reading representation** — a rendered sidebar row, reading-stage heading/content, document
  title, or search result that refers to a saved Tata Ibadah, song, or songbook. It is derived from the
  current server response and is not stored separately.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | Saving any of the three sidebar record types leaves no stale visible representation in the active reading shell. | In the live preview, compare the edited record's visible row, stage heading, and title after the save interaction; no reload or panel reopen occurs. |
| SC-002 | Search results settle on the edited record's current match state. | Run both US2 scenarios and inspect result text, row count, and group count with the original query still present. |
| SC-003 | An unrelated reading stage and the operator's browsing state survive a sidebar save. | Keep a Bible chapter open, edit a Kidung row, and inspect the chapter, panel state, filter, scroll, and focus after save. |

## UI/UX

Behavior-only change. The preview viewport is **1440×900** and uses the existing reading shell, editor
dialogs, typography, tokens, spacing, and transitions. No dimensions, colors, fonts, controls, or motion
change. The affected content changes in place — for example, `Preview Tata Ibadah — Before` becomes
`Preview Tata Ibadah — Updated` in the stage and sidebar; an updated search result keeps its current
query and page. A longer saved name may wrap according to the existing styles.

## Assumptions

- “All pages” means the shared public reading shell at `/`, `/home/`, `/search`, `/bible/`, `/songs/`,
  and `/tatib/`, wherever a Kidung or Tata Ibadah sidebar editor can be opened, plus search results
  shown in that shell. The audit found no matching inline editor on the read-only `/manage/` lists, the
  Django `/admin/` forms, the Media Library file list, projector, or OBS overlay/dock; those use their
  own update paths.
- This slice covers successful online saves of Tata Ibadah, songbook, and song records. Bible content
  has no sidebar edit control; when Bible is the unrelated stage, it stays in place while another
  section's sidebar is refreshed.
- Editor permissions, server validation, error copy, and the local offline snapshot's later sync are
  unchanged.

## Clarifications

None open. Specify records the scope of “all pages” above; no `[NEEDS CLARIFICATION]` markers remain.

**Answered during Implement (2026-10-26)** — US1/AC2 asked for the saved song title in the browser tab,
while `reading` R1 says a song page's tab follows its header (the songbook citation). Asked through the
agent's question tool; the owner kept R1 and amended AC2. FR-002 now says *the document title that route
renders*, so the rewritten page's own title is the standard rather than a title invented for the save.
