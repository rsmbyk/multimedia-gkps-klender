# Feature Specification: Enter accepts a delete confirmation

**Slice**: `specs/256-enter-confirms-delete`
**Branch**: `feat/256-enter-confirms` (cut from `origin/develop` at `1cd9f081`)
**Created**: 2026-11-28
**Status**: Accepted — gate 1, 2026-11-28 (permission to plan only)
**Capability read before writing**: `docs/spec/reading.md` (delete confirmation rules R31/R44/R58 and
Media Library's removal dialog; none says what Enter does once a destructive confirmation is open,
so this slice adds one rule rather than rewriting them)
**Input**: the request as written — *"pressing enter key when a confirmation dialog/modal such as
delete, should be treated as confirming/delete"*. Two clarifications settled the boundary: *"Only
delete confirmations, on every surface"* and *"Yes — include it as a destructive delete
confirmation"* for the Media Library's Remove file dialog.

## User Scenarios & Testing

### US1 — Enter deletes on any open delete confirmation (P1)

**Why this priority**: This is the reported gap. On the live worktree before the change, pressing
Enter with focus away from the destructive control produced **zero** delete requests on the stage,
sidebar and verse confirmations; the dialog stayed open. The control exists, but a keyboard user has
to Tab onto it first.

**Independent Test**: On the live preview, open a stage entry's Delete confirmation, move focus to
the body, press Enter once, and watch the request log: before 0 POSTs, after 1 POST to
`/editor/entry/<pk>/delete/` and the dialog closes.

**Acceptance scenarios**

1. **Given** an open stage-entry confirmation with focus outside its Delete button,
   **When** Enter is pressed once,
   **Then** exactly one `POST /editor/entry/<pk>/delete/` is sent, the dialog closes, and the entry is
   gone on the next render.
2. **Given** an open sidebar-record confirmation with focus outside its Delete button,
   **When** Enter is pressed once,
   **Then** exactly one `POST /editor/<kind>/<pk>/delete/` is sent, the dialog closes, and the record
   is marked inactive/deleted.
3. **Given** an open verse confirmation with focus outside its Delete button,
   **When** Enter is pressed once,
   **Then** exactly one `POST /editor/verse/<pk>/delete/` is sent and the verse is removed.
4. **Given** focus is on the confirmation's Cancel button,
   **When** Enter is pressed,
   **Then** the destructive action still runs (the key belongs to the open confirmation, not to the
   focused control).

### US2 — Enter accepts the Media Library removal (P2)

**Why this priority**: The owner explicitly included this destructive confirmation. It is a separate
`<dialog>` outside the editor, so a handler scoped only to the editor modal would miss it.

**Independent Test**: Open `#mediaRemoveDialog`, press Enter with focus away from Remove file, and
read a click counter attached to `#mediaConfirmRemove`: before 0, after 1.

**Acceptance scenarios**

1. **Given** the Media Library removal dialog is open,
   **When** Enter is pressed once,
   **Then** `#mediaConfirmRemove` is activated exactly once.
2. **Given** a removal dialog whose destructive control is disabled,
   **When** Enter is pressed,
   **Then** nothing is activated.

### Edge Cases

- **When** Enter is repeated or combined with Shift, Ctrl, Alt or Meta — **Then** no activation;
  one physical press is one confirmation.
- **When** a confirmation layer is hidden or its `<dialog>` is closed — **Then** Enter keeps its
  normal meaning elsewhere on the page.
- **When** a non-destructive confirmation (copy as template, Use template create, leave-with-changes,
  screen-mode switch) is open — **Then** Enter is untouched: none of these carries the marker.
- **When** Escape is pressed — **Then** it still cancels the confirmation, as before.
- **When** a retired Fomantic delete modal from spec 194 is present in the source tree but its route
  now redirects — **Then** it is out of scope; there is no live page on which to press Enter.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | On an open destructive confirmation, Enter activates that confirmation's destructive control. | `reading/R67` |
| FR-002 | The activation does not depend on which element has focus inside the open confirmation. | `reading/R67` |
| FR-003 | The destructive control is marked in markup (`data-enter-delete`) so non-destructive confirmations are not caught. | `reading/R67` |
| FR-004 | A hidden layer, a closed `<dialog>`, a disabled control, a repeated keydown and a modified chord (Shift/Ctrl/Alt/Meta) never activate the control. | `reading/R67` |
| FR-005 | One Enter press triggers exactly one activation; the default key action is suppressed so a focused control cannot fire twice. | `reading/R67` |
| FR-006 | The covered surfaces are the sidebar record, stage entry, stage old row, verse and Media Library removal confirmations. | `reading/R67` |
| FR-007 | Escape, Cancel clicks and scrim dismissal keep their existing behaviour. | `reading/R67` |

### Key Entities

- **Destructive control** — a visible, enabled element carrying `data-enter-delete` inside an open
  confirmation; it is the single target of the handler and owns the existing delete logic.
- **Confirmation** — the existing `<dialog>` / editor content layer; no new dialog, state or route is
  introduced.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | All four probed surfaces go from 0 to exactly 1 activation on one Enter press. | `preview/probe.py` before/after JSONL: entry, sidebar and verse POST counts; media click counter. |
| SC-002 | Four targeted E2E tests pass. | `tests.e2e.test_enter_delete_confirm` — 4 tests, 0 failures. |
| SC-003 | No activation occurs when the confirmation is hidden, the control is disabled, or the chord is modified. | Inspected in the handler guards; covered by FR-004. |
| SC-004 | No non-destructive confirmation changes its Enter behaviour. | Inspection: no marker on copy, leave, generate or screen-mode buttons. |

## UI/UX

Shape: **live preview** from the slice worktree at `http://127.0.0.1:8768/`, dark mode at 1×,
1440×900. No box, colour, type or motion changes; the frozen observable is the key-to-action result.

| State | Before (base commit) | After (worktree) |
| --- | --- | --- |
| Stage entry confirm, focus away | 0 POST; dialog open; confirm visible | 1 POST `/editor/entry/9/delete/`; dialog closed; confirm gone |
| Sidebar record confirm, focus away | 0 POST; dialog open; confirm visible | 1 POST `/editor/tatib/9/delete/`; dialog closed; confirm gone |
| Verse confirm, focus away | 0 POST (probe reached the confirm; the pre-change click used a pointer) | 1 POST `/editor/verse/19/delete/`; dialog closed; confirm gone |
| Media removal, focus away | 0 Remove-file clicks; dialog open | 1 Remove-file click; dialog open (no pending file in the probe) |
| Focus before Enter | `BUTTON#` on stage/sidebar/media, `BODY#` on verse | same; the action no longer depends on it |

- **Layout / position / size / colour / typography / motion / responsive**: unchanged — the slice adds
  one script tag and four data attributes, no CSS.
- **States**: covered — open confirmations (four), hidden/closed confirmation, disabled control,
  repeated/modified Enter, non-destructive confirmations.
- **Responsive**: identical at any width; no geometry is read by the handler.

## Assumptions

- "Every surface" means every live destructive confirmation in the reading application; the
  Fomantic/OBS manager modals named by the owner's first answer are retired by spec 194 and their
  routes now redirect, so there is no live page to change — measured, not presumed.
- "Delete confirmation" includes the Media Library's Remove file dialog — owner answer.
- Enter accepts even when Cancel has focus, because the owner described the key as belonging to the
  confirmation, not to the focused control.
- Shift/Ctrl/Alt/Meta+Enter and repeat are ignored so one press is one destructive action.
- No new state, route, schema or endpoint: the handler clicks the existing control and its existing
  handler performs the write.
- Preview-first chronology: the live change was applied to the worktree before gate 1 so the
  before/after numbers above come from the real code path; it stays uncommitted until Fold.

## Clarifications

### Session 2026-11-28

- Q: Which confirmation surfaces should pressing Enter accept? → A: Only delete confirmations, on
  every surface.
- Q: Does that include the Media Library's "Remove file from this computer?" confirmation? → A: Yes
  — include it as a destructive delete confirmation.
