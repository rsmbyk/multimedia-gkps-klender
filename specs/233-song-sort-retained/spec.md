# Feature Specification: the song list keeps its chosen order across in-place refreshes

**Slice**: `specs/233-song-sort-retained`
**Branch**: `fix/233-song-sort-retained`
**Created**: 2026-11-23
**Status**: Accepted — gate 1, 2026-11-23
**Input**: "when you create a new song, the sidebar should retain whatever order it is being sorted with"
**Demand**: `ITEM-247` (to be opened at Specify)
**Capability**: `new: reading/R57`

Today the second sidebar's song list offers a sort control (`#songSort`) that toggles between last
modified (the server's own order) and alphabetical. The choice lives only in a client-side
variable and is applied to the DOM once, on the button click. Every in-place refresh — a create,
an edit, a delete, or a row click — reconciles the list back into the server's last-modified order,
but never re-applies the chosen sort. The button still advertises `data-order="title"`, so the
control lies about the rows it governs.

Live reproduction from the slice's base commit `b46f7efe` (probe E2E against a dedicated database,
1440×900; two songs in one ordinary songbook, `Zebra` modified 2020-01-02 and `Alpha` modified
2020-01-01):

| Moment | Row order | `#songSort` |
| --- | --- | --- |
| page opens | `['Zebra', 'Alpha']` | `m` |
| after the sort is toggled | `['Alpha', 'Zebra']` | `title` |
| after a song `Beta` is created (newest stamp) — base | `['Beta', 'Zebra', 'Alpha']` | `title` |
| after the same create — with the slice's change | `['Alpha', 'Beta', 'Zebra']` | `title` |

The target state after a refresh is the row order the chosen sort would produce, with the sort
button still agreeing, in the same document (no reload).

## User Scenarios & Testing

### US1 — Creating a song keeps the alphabetical order (P1)

**Why this priority**: the create action is the reported case. A newly created song carries the
newest modification stamp, so a lost sort puts it at the head of the list instead of in its
alphabetical place — the exact moment the operator is looking for it.
**Independent Test**: with two songs in one book, toggle to alphabetical, create a third song;
the rows stay alphabetical and the sort button still reads `title`, with no document reload.

**Acceptance scenarios**

1. **Given** an ordinary songbook with `Zebra` (newer) and `Alpha` (older) **When** the operator
   toggles the sort to alphabetical and creates `Beta` **Then** the rows read `Alpha`, `Beta`,
   `Zebra` and `#songSort` still carries `data-order="title"`.
2. **Given** the same book in the default last-modified order **When** a song is created **Then**
   it leads the list as it does today, and `#songSort` still carries `data-order="m"`.
3. **Given** a successful create **When** the list settles **Then** `performance.timeOrigin` is
   unchanged and no page marker is lost — the refresh is in place (spec 225 behaviour survives).

### US2 — Every in-place refresh keeps the chosen order (P1)

**Why this priority**: the fault is in the shared list-reconciliation path, not in the create
handler. Fixing only create would leave the same wrong order after an edit, a delete or a row
click, and would need a second fix later. The owner chose this root-cause scope.
**Independent Test**: with the sort set to alphabetical, edit a song's title, delete a song and
open a different song row; after each operation the remaining rows stay alphabetical.

**Acceptance scenarios**

1. **Given** an alphabetical song list **When** an existing song is edited and the lists refresh
   **Then** the rows stay in alphabetical order.
2. **Given** an alphabetical song list **When** a song is deleted **Then** the remaining rows stay
   in alphabetical order.
3. **Given** an alphabetical song list **When** a different song row is opened on the stage
   **Then** the child list stays alphabetical while the stage follows the click.
4. **Given** a hymn songbook, which offers no sort control **When** any of these refreshes happen
   **Then** its number order is unchanged.

### US3 — Other lists and the default order are untouched (P2)

**Why this priority**: the reconciliation helper is shared with the Alkitab chapter list and the
Tata Ibadah contents; widening the re-sort to those lists would reorder content that has no song
rows and no sort control.
**Independent Test**: with the sort toggled to alphabetical, browse Alkitab and Tata Ibadah and
return to Kidung; chapter rows and service contents keep their own order.

**Acceptance scenarios**

1. **Given** the sort set to alphabetical **When** the operator moves to a section whose second
   column has no song rows **Then** nothing in that column is reordered by the song sorter.
2. **Given** a freshly loaded page **When** no sort click has happened **Then** the list is in the
   server's last-modified order, as it is today.

### Edge Cases

- **When** the list is empty or has one song **Then** re-applying the order is a no-op.
- **When** two songs share a modification stamp **Then** the existing tiebreak (source order on
  last-modified, title then source order on alphabetical) is unchanged.
- **When** the song list is in another section's collapsed pane **Then** the re-sort touches no
  rows.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | After any in-place refresh of the song list, the rows SHALL be ordered by the sort currently chosen by the operator, not by the server's default. | `new: reading/R57` |
| FR-002 | The sort control's indicated order SHALL agree with the rendered row order after every such refresh. | `new: reading/R57` |
| FR-003 | The last-modified order SHALL remain the default on a freshly loaded page and after a create when that order is chosen. | `new: reading/R57` |
| FR-004 | Lists with no song rows, the number order of hymn songbooks, and a full document reload SHALL be unaffected. | `new: reading/R57` |

### Key Entities

- **Song sort choice** — client state in `static/web/reading.js`, one of last modified (`m`) or
  alphabetical (`title`), changed only by `#songSort` and stable for the life of the document.
- **Song list** — the `#chList` element in the second sidebar; its `.songrow` children carry the
  modification stamp, title and source-order data the sorter uses.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | A created song lands in its alphabetical position | the probe E2E: toggle, create `Beta`, rows read `Alpha, Beta, Zebra` and `data-order` is `title` |
| SC-002 | The order survives edits, deletes and row clicks | an E2E pass that performs each operation with the sort on `title` and reads the row titles after each |
| SC-003 | Nothing else changes | the default-order create path, hymn-book order and other sections keep their current orders in the same suite |

## UI/UX

No new visual design: the change keeps the same rows, sort button and stage as the pages already
shipped. What changes is that the promised order matches the painted order after a refresh.

- **Layout / position**: unchanged. `#songSort` stays in `.ch__search` beside the song filter;
  each `.songrow` keeps its own box.
- **Size / spacing**: unchanged — no dimension changes; the only measured differences are row
  positions as listed in the reproduction table (three rows, 1440×900).
- **Colour / typography**: unchanged.
- **States**: both sort states are affected — `m` (default) stays as today, `title` now survives a
  refresh. Hover and focus on the sort button and on song rows are unchanged.
- **Motion**: none added. No new animation; the re-order happens in the same frame as the list
  refresh.
- **Responsive**: unchanged.

## Assumptions

- The sort choice is per document, not persisted to storage. The owner chose "every in-place
  refresh" and did not choose the browser-persistence option; a full reload still starts in last
  modified order, as it does today.
- The re-sort is applied to every in-place list reconciliation, including navigations and other
  sections; where there are no song rows it is a no-op. This is the shared root cause of the
  reported create case.
- Hymn songbooks never offer the control and keep their number order (spec 011, spec 125).
- Server order is last modified first with title as the tiebreak; the client's `m` sort uses the
  same stamps and source order, so re-applying it on refresh cannot diverge from the server.

## Clarifications

### Session 2026-11-23

- Q: should the sort be retained only after a create, or after every in-place refresh? → A: after
  every in-place refresh (create, edit, delete, row click) — the root-cause fix.
