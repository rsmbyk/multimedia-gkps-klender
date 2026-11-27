# Feature Specification: a reordered Tata Ibadah keeps every entry, and both lists agree

**Slice**: `specs/241-tatib-reorder-kept`
**Branch**: `fix/241-tatib-reorder-kept`
**Created**: 2026-11-24
**Status**: Draft
**Input**: "after add/edit/delete and reordering entries, the page appears cut off: the sidebar and pane disagree, sections vanish, and a reorder can be lost even when dragged to the top"
**Demand**: `ITEM-256`
**Capability**: `modified: reading/R57` · `new: reading/R60` (R58/R59 were taken by specs 236/238 while this slice was open)

A Tata Ibadah's contents list and its stage are two views of one order. After any in-place save
— an add, an edit or a delete — the shell reconciles both from the server's answer, then the
operator drags a row. Two client defects break that contract:

1. **The song sorter moves the contents list.** `applySongOrder()` runs after every in-place
   refresh (spec 233) and treats every `.songrow` as a song. A Tata Ibadah contents row is also
   a `.songrow` but carries no song data, so the sorter's comparator is a no-op — yet its
   `appendChild` still moves each row to the end of `#chList`. Rows that are not `.songrow`
   (the break divider, `toc__eos`) stay at the top. The sidebar is left in an order the server
   never sent.
2. **A drop is rewritten by the gesture's own cleanup.** `endDrag()` re-parents the pane while
   `drag` is still set. Re-parenting the captured row fires `pointercancel`/`blur`, `cancelDrag()`
   runs, rewrites the pane a second time from the drag-start order and nulls `drag`; the write
   then posts the old order. `applyPaneOrder()` maps `body.children` one-to-one against a stale
   node cache, so a child with no cached node is dropped — a section disappears from the stage.

Measured on the slice's base commit `c06e8c97`, at 1440×900:

| Moment | Sidebar rows | Stage sections | Server order |
| --- | --- | --- | --- |
| E2E fixture (3 texts + 1 break), after editing the first text | `[4, 1, 2, 3]` | `[1, 2, 3]` | `[1, 2, 3, 4]` |
| then dragging the third text to the top | `[4, 1, 2, 3]` | `[1, 2, 3]` | `[1, 2, 3, 4]` (the drop never landed) |
| E2E fixture, after adding a fourth text, then dragging it to the top | `[4, 5, 1, 2]` | `[5, 3, 1, 2]` | — (entry 3 lost from the stage) |
| scratch service 322 (25 rows), after add | 27 rows | 26 sections | 27 rows |

The target is the order the operator dragged to: every live entry present exactly once in both
lists, the same order in both, and the same order after a reload.

## User Scenarios & Testing

### US1 — A drop after a save is the order that is written (P1)

**Why this priority**: this is the reported loss. The operator rearranges the service after
editing it and the work is silently discarded, while the stage shows a different service order
than the sidebar.
**Independent Test**: edit an entry, drag the last text row above the first, and read both lists;
then reload. Both lists show the dragged order, every entry is present, and the server kept it.

**Acceptance scenarios**

1. **Given** a service with three text entries and a break **When** the first text is edited and
   saved, then the third text is dragged to the top **Then** the sidebar reads `3, 1, 2, 4`, the
   stage reads `3, 1, 2`, and the reorder request carries that order.
2. **Given** the same drop **When** the page is reloaded **Then** both lists still read `3, 1, 2, 4`.
3. **Given** a service with an entry added at the start **When** the new last row is dragged to
   the top **Then** the stage holds every entry once, in the sidebar's order — no section is lost.
4. **Given** a drop that the server accepts **When** the pane is rewritten **Then** the gesture is
   over: no `pointercancel`, `blur` or second write follows the drop.

### US2 — The song sorter leaves the Tata Ibadah contents alone (P1)

**Why this priority**: it is a regression against `R57` and it corrupts the list on every save,
before any drag happens. It also hides the drag defect behind a wrong starting order.
**Independent Test**: open a service whose contents include a break or an end-of-section row,
edit any entry, and read the row order; it equals the server's order.

**Acceptance scenarios**

1. **Given** a Tata Ibadah contents list **When** any in-place refresh completes **Then** the
   sorter leaves every row where the server put it.
2. **Given** a Kidung song list sorted alphabetically **When** a song is created, edited or
   deleted **Then** the chosen sort still survives the refresh (spec 233 behaviour unchanged).
3. **Given** an Alkitab chapter list **When** a chapter is opened **Then** its rows keep their
   server order.

### US3 — An abandoned gesture restores the pre-drag order (P2)

**Why this priority**: a cancelled drag must not leave a half-applied order or a stale node
cache; the next drop would otherwise inherit it.
**Independent Test**: start a drag, press Escape (or move focus out of the window) without
dropping, and read both lists; they show the order from before the gesture.

**Acceptance scenarios**

1. **Given** a drag in progress **When** Escape cancels it **Then** the sidebar and the stage show
   the pre-drag order, and no write is posted.
2. **Given** a cancelled drag **When** a new drag starts **Then** it sees the current rows, not the
   cancelled gesture's cache.

### Edge Cases

- **When** the service has one entry or none **Then** a drop is a no-op and no write is posted.
- **When** a legacy `TataIbadahItem` shares an order slot **Then** it keeps its own row and its
  place; only `ServiceEntry` rows move.
- **When** a choice's options follow the choice **Then** the options keep their order under it.
- **When** the reorder request fails **Then** both lists return to the last written order and the
  existing error line speaks.
- **When** the stage holds no open service **Then** the contents list still sorts nothing.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | A completed drop SHALL be written exactly once, with the order the operator dropped. | `new: reading/R58` |
| FR-002 | After a drop, the contents list and the stage SHALL show the same entries in the same order. | `new: reading/R58` |
| FR-003 | Every live entry SHALL remain on the stage after a drop; no section may be dropped or duplicated. | `new: reading/R58` |
| FR-004 | A cancelled or abandoned drag SHALL restore the pre-drag order in both lists and post nothing. | `new: reading/R58` |
| FR-005 | The song sorter SHALL leave a list whose rows carry no song data untouched, including the Tata Ibadah contents list. | `modified: reading/R57` |
| FR-006 | The Kidung sort choice SHALL keep surviving every in-place refresh, and the Alkitab chapter order SHALL be unchanged. | `modified: reading/R57` |
| FR-007 | A reload SHALL show the order the server kept, matching what the drop wrote. | `new: reading/R58` |
| FR-008 | Legacy rows, break dividers and a choice's options SHALL keep their existing places and relative order. | `new: reading/R58` |

### Key Entities

- **Service entry order** — `ServiceEntry.order_number`, shared with legacy `TataIbadahItem`
  slots; the reorder endpoint accepts a permutation of the live entries' slots.
- **Contents list** — `#chList` in the reading sidebar; one `li` per entry, each movable row
  carrying `data-move-grip="<pk>"`; break rows are `.toc__eos` and carry no `data-entry-pk`.
- **Stage pane** — `#readBody`; one `section[data-entry-pk]` per service entry, plus add bars and
  other shell furniture.
- **Drag gesture** — `static/web/reorder.js`; `drag` holds the captured row, its pk and the
  start order; `endDrag()` settles it and `persist()` posts once.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | The post-edit drop is written and both lists agree | E2E: edit, drag third to top, assert sidebar `3, 1, 2, 4` and stage `3, 1, 2`, then reload and assert again |
| SC-002 | An add-then-drag keeps every entry | E2E: add a text, drag the last row to the top, assert the stage holds every entry once in sidebar order |
| SC-003 | The contents list keeps server order after a save | E2E: after the edit, the sidebar equals the order a fresh fetch returns |
| SC-004 | The song sort and other lists are untouched | the existing `tests/e2e/test_song_sort_retained.py` and `tests/e2e/test_reading.py` sort cases stay green |

## UI/UX

No new visual design. The same rows, grips, break dividers and stage sections keep their boxes,
type and colours; what changes is the order they settle in after a save and a drop.

- **Layout / position**: unchanged. The sidebar keeps its `#chList` column; the stage keeps its
  `#readBody` sections.
- **Size / spacing**: unchanged — no dimension changes. The only measured differences are row
  positions: on the four-entry fixture, the break moves from row 1 to row 4 after the edit, and
  the dragged row moves from row 3 to row 1.
- **Colour / typography**: unchanged.
- **States**: the default, drag-in-progress, dropped, cancelled and failed-write states all end in
  the same painted rows; the existing error line is the only failure surface.
- **Motion**: none added. The drop's rewrite happens in the same frame as today.
- **Responsive**: unchanged; the contents list is not offered at the phone width (`R14`).

## Assumptions

- The write stays at once, with no Save/Discard, as spec 026 established; this slice only makes
  the one write carry the dropped order.
- The reorder endpoint's contract is unchanged: a permutation of the live entries' existing slots,
  options following their choice.
- The fix is client-side. The server already renders every entry and accepts the permutation; the
  observed losses come from the shell's reconciliation and gesture cleanup.
- The song sorter's scope is a list with song rows, identified by the data real song rows carry
  (`data-t`, `data-o`, `data-m`), not by the `.songrow` class alone.
- A drop that the server rejects keeps today's behaviour: both lists return to the last written
  order and the error line speaks.

## Clarifications

None open. The request named the visible failure; the measured reproduction fixed the two causes,
and the assumptions above record the defaults taken where the request was silent.
