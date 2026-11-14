# Feature Specification: The Break kind retires, and the breaks already written stay

**Slice**: `specs/131-retire-break-entry`
**Branch**: `feat/131-retire-break-entry`
**Created**: 2026-10-25
**Status**: Accepted (owner, gate 1, 2026-10-25)
**Input**: "i want you to retire service entry of kind Break. cant add/edit anymore, but can still view/delete the old/already created ones"

## User Scenarios & Testing

### US1 — No surface offers a new Break (P1)

**Why this priority**: the kind is retired, so the first thing that must be true is that it cannot be
created. Every place that offers it is a place that would create one.

**Independent Test**: open a Tata Ibadah with items and one with none; the add rows and the empty service's
action menu offer Passage, Song, Text and Media, and no Break; a POST that asks for one creates nothing.

**Acceptance scenarios**

1. **Given** a service with at least one item, **When** an add row (the start bar or a row under an item) is
   revealed, **Then** it holds four buttons — `+ Passage`, `+ Song`, `+ Text`, `+ Media` — and no `+ Break`.
2. **Given** an empty service, **When** it opens, **Then** its action menu holds four actions and none of them
   is `Add Break`.
3. **Given** any of those surfaces, **When** the last entry is deleted in place, **Then** the rebuilt empty
   state offers the same four actions and no Break.
4. **Given** a page whose Break control was rendered before this change, **When** it is clicked, **Then** no
   entry is created and the entry is refused by the server, with the existing failure feedback.
5. **Given** a POST to the entry-save endpoint naming the Break kind, **When** it is sent directly (no page
   involved), **Then** no `ServiceEntry` row is created and the response is `404`.

### US2 — The breaks already written still read as dividers (P1)

**Why this priority**: the operator's past services must keep projecting and reading exactly as they do
today. Retiring the kind may not delete, hide or reshape what it already produced.

**Independent Test**: open a service that holds a Break entry: the stage and the sidebar show one full-width
divider, the projector carries its blank screen, and the saved render agrees.

**Acceptance scenarios**

1. **Given** a service holding a Break entry, **When** the stage opens, **Then** the entry draws the same
   full-width rule in the same 56px box, with no label and no note, as before the retirement.
2. **Given** the same service, **When** the sidebar is read, **Then** the Break keeps its row and its number
   among the other entries.
3. **Given** the same service, **When** it is projected, **Then** the Break still contributes its blank
   projector screen with entry type `break`.
4. **Given** the same service rendered from the saved library, **When** it is read, **Then** the divider, its
   place in the order and its sidebar row are the same as the server page's.

### US3 — An existing Break stays deletable, and never editable (P1)

**Why this priority**: the request names deletion explicitly. A retired kind that cannot be cleared would
leave old rows stuck in every service that used them.

**Independent Test**: delete a Break entry from the stage; the row disappears, the order closes up, and the
same page offers no way to edit it.

**Acceptance scenarios**

1. **Given** a Break entry, **When** the divider is hovered or focused, **Then** its controls offer Delete and
   no Edit.
2. **Given** the Delete control, **When** it is confirmed, **Then** the row leaves the stage and the sidebar,
   the remaining entries close up their order, and the deletion is recorded on the server.
3. **Given** a Break entry's id, **When** the edit form or the save endpoint is asked for it directly,
   **Then** the response is `404` and the stored row is unchanged.
4. **Given** a Break entry, **When** it is dragged, **Then** it reorders exactly as today.

### Edge Cases

- **When** a legacy `END_OF_SECTION` row (`TataIbadahItem`) is on the page **Then** nothing changes for it: it
  is a different table, still viewable, editable and deletable, and it keeps its note.
- **When** a service holds only Break entries **Then** they all render, and deleting the last one lands on the
  empty state, which offers the four remaining kinds.
- **When** the kind is read from stored data **Then** its display name stays `Section break` in the sidebar,
  the projector and any export — the stored kind and its label are not removed.
- **When** the browser runs an older cached `entries.js` or `offline-render.js` **Then** a stale `+ Break`
  click is refused by the endpoint rather than silently creating a row.
- **When** a Break entry carries a legacy title **Then** it still renders with no label (spec 038), unchanged.
- **When** the empty service is narrower than 300px of reading column **Then** spec 130's three-column fallback
  applies to the four remaining tiles — three and one — and nothing shrinks below 44px.
- **When** the empty state's grid is not narrowed with the kind **Then** the four tiles would sit left of
  centre in a five-track row, so the grid's track count is part of the change, not a follow-up.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | The server-rendered stage offers no Break add control in the start bar, in an item's add row, or in the empty service's action menu, whose tile row draws four tracks rather than five. | `new: reading` |
| FR-002 | The in-place rebuild that follows deleting an entry's row offers the same four actions, with no Break. | `new: reading` |
| FR-003 | The saved-page renderer offers the same four actions in both its add rows and its empty menu. | `new: reading` |
| FR-004 | The new-entry form endpoint refuses the Break kind (`404`), and the entry-save endpoint refuses to create one, whatever `kind` or `after` the request carries. | `new: reading` |
| FR-005 | The edit-form endpoint and the entry-save endpoint refuse an existing Break entry (`404`) and change nothing. | `new: reading` |
| FR-006 | A Break entry still renders as the one full-width divider, in the same box, with no label, on the stage and in the sidebar, and still contributes its blank projector screen. | `new: reading` |
| FR-007 | A Break entry's Delete control stays, and deleting it removes the row and compacts the service order as before. | `new: reading` |
| FR-008 | A Break entry stays reorderable by the existing drag path. | `new: reading` |
| FR-009 | The saved-page renderer draws an existing Break entry exactly as the server page does. | `reading/R2` (spec 122), `R5` (spec 128) |
| FR-010 | The stored kind, its value, its display name and its rows are not removed, renamed or migrated. | `new: reading` |
| FR-011 | The legacy `END_OF_SECTION` row is untouched in every respect. | `new: reading` |

### Key Entities

- **ServiceEntry (kind 3, Section break)** — retained in the model and in existing rows; no longer creatable
  or editable through any endpoint; still renderable, reorderable and deletable. No field changes, no
  migration.
- **The add row / empty action menu** — the three surfaces that offer creation: `tatib.html` (server),
  `entries.js` (rebuild after a delete), `offline-render.js` (saved page). Each offers the four remaining
  kinds.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | No surface offers a Break action | one server page, one rebuilt empty state and one saved render each show exactly four `data-entry-open` values, none `section_break` |
| SC-002 | A direct save request cannot create one | three POSTs naming the kind (with a title, with `after`, bare) all answer `404` and leave `service_entries` unchanged |
| SC-003 | An existing Break still reads, projects and deletes | one divider on the stage and in the sidebar, one `break` projector screen, one Delete that removes the row and closes the order |
| SC-004 | Nothing else on the page moves | the four remaining add buttons keep their 28px height and 6px gaps; the empty menu keeps its 320px width, 10px gaps and row heights; the divider keeps its 56px box and centred rule |
| SC-005 | The four remaining kinds are untouched | the existing entry suites (`multimedia.web`, `tests.e2e.test_entries`, `test_reorder`, `test_tatib_section_break`) pass |

## UI/UX

Measured on the branch at 1440×900, from the running page with the Break control removed from the live DOM
(`preview/probe_break_controls.py`, frames in `preview/`):

- **Layout / position**: the add row keeps its 400px block, left-aligned; the four remaining buttons stand in
  one line, 28px tall, 6px apart — `+ Passage` 84px, `+ Song` 64px, `+ Text` 58px, `+ Media` 71px. The row's
  right edge moves 75px left (Break was 69px + one 6px gap). The empty service's action row (spec 130's tiles)
  keeps its centred 52px squares and 10px gaps: five tiles span 300px, four span 238px, centre unmoved.
- **Size / spacing**: nothing is resized, re-padded or re-gapped; only the Break control's width leaves the row,
  and the empty menu's grid drops from five tracks to four (`repeat(5, minmax(0, 52px))` →
  `repeat(4, minmax(0, 52px))`), which is what keeps the row centred instead of leaving an empty slot.
- **Colour / typography**: unchanged — the same dashed `--divider` buttons, `--head-ink` labels, 13px/1.2; the
  tiles keep their 12px radius, `--divider` border and 22px glyph.
- **States**: hover, focus and disabled on the four remaining buttons are unchanged; there is no disabled
  Break state to draw, because the control does not exist. The divider's hover (Delete only), modal-origin
  and focus-restore states are unchanged.
- **Motion**: none added or removed.
- **Responsive**: the add row still wraps when the column is narrow (now one button earlier); the empty menu
  keeps its full width under 320px of column.

## Assumptions

- **The endpoint is closed, not just the button.** "Can't add" is enforced where rows are made, so a stale
  page or a direct request cannot create one — a UI-only removal would leave the kind creatable.
- **Deletion is not being repaired; it is being kept.** The owner reported being unable to delete a Break,
  and the cause was a network fault on the operator's side, not the app: this slice proves the path still
  works after the retirement (US3), and changes nothing in it.
- **The break's hover movement is pre-existing and untouched.** Hovering a break reveals its neighbouring add
  rows, which pushes the divider down 64px before its own controls settle in; that is spec 036/037/052
  behaviour, applies to every entry, and is out of this slice's scope.
- **The kind and its rows stay.** Retiring creation and editing is not a data migration: existing rows keep
  kind 3 and their display name, so no projection, export or search behaviour has to change with them.
- **Editing was already absent in the UI.** Break rows have offered Delete only since spec 057; this slice
  makes the endpoint agree with the control, so no visible edit control is removed.
- **The empty state's Break action is included.** It is a creation surface like any add row; leaving it would
  keep the kind reachable.
- **The legacy `END_OF_SECTION` row is not the retired kind.** It predates `ServiceEntry` and belongs to
  `TataIbadahItem`; the request names the service entry kind, so the legacy row's controls are untouched.
- **One action fewer is the whole visual change.** Spec 130's tiles are the empty state's layout on `develop`;
  this slice drops one tile and one grid track from it, and touches no other part of that design.

## Clarifications

### Session 2026-10-25

- Q: Should a Break entry also be deletable, since the owner could not delete one? → A: Yes, and the report
  was a network fault on the operator's side. The delete path was exercised on the branch (dialog, `POST 200`,
  row removed, order compacted) and US3 proves it still works after the retirement. No repair is in scope.
- Q: Should the break's hover movement — the divider being pushed down when its add rows reveal — be changed
  in this slice? → A: No. It is pre-existing behaviour of every entry (spec 036/037/052) and is recorded as an
  edge case, not touched.
