# Feature Specification: Sidebar Delete Buttons

**Slice**: `specs/190-sidebar-delete`
**Branch**: `feat/190-sidebar-delete`
**Created**: 2026-11-13
**Status**: Accepted (Gate 1, 2026-11-13)
**Input**: "i want you to add delete buttons on the sidebar items for songs (non-hymn), songbooks (non-hymn), and services sidebars"

## User Scenarios & Testing

### US1 — Delete a non-hymn songbook (P1)

**Why this priority**: Removing an unused songbook keeps the sidebar list accurate; the action must be explicit and reversible-in-intent (confirmed) before it takes effect.

**Independent Test**: With `editor_enabled` and a non-hymn songbook visible, hover the row, click the trash control, confirm deletion in the modal, and verify the row is removed and the server records the delete.

**Acceptance scenarios**

1. **Given** a non-hymn songbook row **When** the user hovers it **Then** the row reveals the delete control alongside the existing edit control.
2. **Given** the delete control is clicked **When** the confirm modal opens **Then** it shows `Delete songbook` context for that record with Cancel and Delete actions.
3. **Given** the user confirms **When** the request succeeds **Then** the row is removed from the sidebar; if that songbook was on stage, navigation returns to the parent list with history replaced (not appended).

### US2 — Delete a non-hymn song (P2)

**Why this priority**: Songs are managed frequently inside a songbook; deletion must follow the same safe, confirmed pattern.

**Independent Test**: With `editor_enabled` and a non-hymn song visible in a songbook, hover the row, delete via confirm, and verify removal.

**Acceptance scenarios**

1. **Given** a non-hymn song row in a songbook **When** hovered **Then** the delete control is revealed beside the edit control.
2. **Given** delete is confirmed **When** successful **Then** the song row is removed from `#chList`; if it was on stage, history is replaced appropriately.

### US3 — Delete a service (Tata Ibadah) row (P3)

**Why this priority**: Services/templates in the Tata Ibadah sidebar must be removable with the same affordance and confirmation.

**Independent Test**: With `editor_enabled`, delete a dated service and a template service; verify correct noun/labeling and removal.

**Acceptance scenarios**

1. **Given** a service row **When** hovered **Then** the delete control is revealed alongside the existing edit control.
2. **Given** a dated Tata Ibadah service row that displays a date **When** hovered **Then** the row’s date text is hidden while hovered so the revealed row actions are not obscured.
3. **Given** a template row (Templates group) **When** delete is confirmed **Then** the confirm/modal context uses the template noun (`Delete template`), not "Tata Ibadah".
4. **Given** a dated service row **When** delete is confirmed **Then** the confirm/modal context uses "Tata Ibadah".

### Edge Cases

- **When** the row is a hymn songbook or a song inside a hymn songbook **Then** no edit/delete controls are rendered (existing restriction preserved).
- **When** the viewer is not an editor (`editor_enabled` false) **Then** no delete controls are rendered.
- **When** the deleted record was currently shown on stage **Then** the UI navigates back to the parent list and replaces the history entry (FR/UX parity with preview behavior).
- **When** delete is cancelled **Then** no request is made and the row remains.
- **When** a dated Tata Ibadah service row is hovered **Then** its date is hidden only for the hover/focus-reveal interaction and remains present in the row’s accessible label/markup; template rows without a date are unchanged.
- **When** running on touch/coarse pointers **Then** controls remain accessible per existing phone/touch drawer behavior (no gesture model regression).

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | Add a delete control to each eligible sidebar row for songs (non-hymn), songbooks (non-hymn), and Tata Ibadah services/templates. | `sidebar/delete-controls` |
| FR-002 | Render delete only where `editor_enabled` is true and the row is not restricted (non-hymn songbooks; songs not in a hymn book). | `sidebar/delete-controls` |
| FR-003 | Place the delete control in the row actions area alongside the existing edit control, hidden at rest and revealed on hover/focus (matching edit UX). | `sidebar/delete-controls` |
| FR-004 | In the Tata Ibadah sidebar, hide a dated service row’s displayed date while the row is hovered/focused for action reveal, so row controls do not overlap or obscure the date text. | `sidebar/delete-controls` |
| FR-005 | Clicking delete opens a confirmation in the shared editor modal before any destructive request. | `sidebar/delete-confirm` |
| FR-006 | Confirm modal copy must reflect the record kind: `song`, `songbook`, `Tata Ibadah` (service), or `template` (template panel rows). | `sidebar/delete-confirm` |
| FR-007 | Template rows must be distinguishable in markup (`data-editor-kind="template"` on template panel rows) so `nounFor` returns `template`, not "Tata Ibadah". | `sidebar/delete-confirm` |
| FR-008 | Deletion is performed via `POST` to a dedicated delete endpoint (not GET), with CSRF protection. | `sidebar/delete-endpoint` |
| FR-009 | Provide server endpoints for delete confirmation context (GET) and delete action (POST) for kinds `songbook`, `song`, `tatib`, and `template` (as applicable). | `sidebar/delete-endpoint` |
| FR-010 | On successful delete, remove the corresponding `<li>` from the correct panel (`#chList` for songs, `#panelBody` for others). | `sidebar/delete-apply` |
| FR-011 | If the deleted record was on stage, replace history/navigation to the parent list (no appended history entry for the removed item). | `sidebar/delete-apply` |
| FR-012 | Reuse existing modal classes/styles (`editor__cancel`, `editor__danger`, shared editor modal structure) and preserve existing edit controls/behavior. | `sidebar/delete-ui` |
| FR-013 | Preserve responsive/phone drawer behavior and touch-first interaction model (media query nesting and existing rules intact). | `sidebar/delete-ui` |

### Key Entities

- **Songbook (Book)** — sidebar row in songbooks panel; deletable when non-hymn and editor enabled.
- **Song** — sidebar row in song list; deletable when not in hymn book and editor enabled.
- **Tata Ibadah service/template** — sidebar row in tatib panel; deletable when editor enabled; template distinguished by kind/label.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | Eligible rows show a delete affordance on hover/focus without breaking existing edit affordance. | Manual/preview inspection across songbooks, songs, tatib, template states. |
| SC-002 | Delete always requires explicit confirmation before POST. | Network/interaction check: no delete POST without confirm action. |
| SC-003 | Correct noun/label shown for service vs template deletes. | Preview states `confirmtatib` vs `confirmtemplate`; DOM/modal text check. |
| SC-004 | Hymn/restricted rows and non-editor view show no delete controls. | Preview states `hymn`, `restricted`; template conditions. |
| SC-005 | Successful delete removes row and handles on-stage case per spec. | Behavior test in running app (targeted). |

## UI/UX

- **Layout / position**: Delete icon control sits in the row actions area adjacent to the existing edit (pencil) control; aligned to the row’s trailing edge consistent with current `.row-edit` placement.
- **Size / spacing**: Match existing row action control sizing and icon stroke/visual weight (per preview).
- **Colour / typography**: Use existing editor/modal and control tokens/classes; destructive action uses `editor__danger`.
- **States**: hover · focus · active (button press) · disabled/loading during confirm fetch/submit (as applicable) · error feedback via existing feedback/toast patterns if request fails.
- **Tata Ibadah date on hover**: For dated service rows that show a date, the date text is hidden while the row is hovered/focused for action reveal so the delete/edit controls remain unobscured. Template rows without a displayed date are unaffected.
- **Motion**: No new motion beyond existing hover reveal/modal transitions already in the product.
- **Responsive**: Works in narrow/phone drawer contexts; touch/coarse interactions preserved (controls accessible without breaking drawer gestures).

Preview reference: `specs/190-sidebar-delete/preview/index.html` (static, self-contained states). The preview must include a state demonstrating a hovered dated Tata Ibadah service row with its date hidden while row actions are visible.

## Assumptions

- Delete is a server-side removal consistent with existing editor patterns (soft-delete/active flag behavior as used elsewhere in this codebase for sidebar-managed records) — exact mechanism confirmed during Plan against current models/views.
- CSRF token is available via existing editor/form mechanisms in the shared modal flow.
- Template vs service distinction is available from panel grouping/context (`Templates` group / kind) and must be reflected in row attributes for client-side noun selection.

## Clarifications

### Session 2026-11-13

- Q: “hide the hovered service’s date” (owner request, 2026-11-13) → A: Added to spec 190. For dated Tata Ibadah service rows, hide the displayed date while hovered/focused so revealed row actions are unobscured (FR-004, US3 scenario 2, UI/UX). Template rows without a displayed date are unaffected. Preview must demonstrate this state. Gate 1 still pending.
