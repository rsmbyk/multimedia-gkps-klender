# Feature Specification: Use template progress survives a close

**Slice**: `specs/253-use-template-progress`
**Branch**: `feat/253-use-template-progress`
**Created**: 2026-11-28
**Status**: Accepted (Gate 1, 2026-11-28 — the owner read the spec, the preview and the assumptions, then answered "accept")
**Input**: "when you try to close a dirty use template modal, it should confirm the user that leaving will save the progress and can be resumed later. each template can save their own progress"

## User Scenarios & Testing

### US1 — A template's unsettled work survives closing the modal (P1)

**Why this priority**: Preparing a service from a template takes several slot resolutions. Today every
close path — Cancel, the backdrop and Esc — throws that work away, so an accidental dismissal means
starting over. The fix has to keep the work without writing to the template: R36 already promises the
template is byte-identical after generating or abandoning.

**Independent Test**: Settle a slot in template A, close the modal, reopen template A and the row is
settled again; open template B and its rows are all unset.

**Acceptance scenarios**

1. **Given** a template's Use template modal, **When** a fill-in or choice is settled, **Then** that
   state is written to this browser session's storage immediately.
2. **Given** saved progress for a template, **When** that template's Use template modal is opened
   again, **Then** the settled rows, the step, the name and the date come back as they were.
3. **Given** progress saved for template A, **When** template B's modal is opened, **Then** B starts
   from its own defaults with no slot settled.
4. **Given** the browser session is closed and a new one opened, **When** the template is reopened,
   **Then** no progress is restored — session storage does not outlive the session.

### US2 — Closing a dirty modal says the work is kept (P2)

**Why this priority**: Without a word at the point of leaving, the operator cannot tell the difference
between "discarded" and "saved for later" — the existing Cancel button reads as discard. The modal
must say plainly what happens.

**Independent Test**: A dirty modal shows the confirmation on Cancel; a modal with nothing settled
closes without one.

**Acceptance scenarios**

1. **Given** a modal with settled progress, **When** Cancel, the backdrop or Esc is used, **Then** a
   confirmation states that the progress is saved in this browser session and can be resumed later.
2. **Given** that confirmation, **When** **Stay** is pressed, **Then** the modal stays open with every
   settled row unchanged.
3. **Given** that confirmation, **When** **Leave** is pressed, **Then** the modal closes and the saved
   progress is still there on the next open.
4. **Given** a modal with nothing settled, **When** it is closed, **Then** no confirmation appears.

### Edge Cases

- **When** a template's slots changed since the progress was saved, **Then** a saved slot id that is no
  longer in the modal is ignored on restore; the rest still come back.
- **When** the modal is swapped in place by the reading shell, **Then** progress is read from storage by
  template id on every open, never cached on the old dialog node.
- **When** a chooser is open and Esc is pressed, **Then** the chooser still closes first and the modal
  stays open, as it does today.
- **When** Create fails validation, **Then** the saved progress is kept so the operator can retry.
- **When** storage is unavailable or disabled, **Then** the modal still opens and works; persistence is
  a best-effort enhancement, not a gate.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | The generate modal SHALL persist its progress in `sessionStorage` under a key derived from the template id in `data-generate-tatib`, so two templates never share progress. | `reading/R65` |
| FR-002 | Progress SHALL be written after every settled slot, choice pick, name change and date change, so a reload or an unconfirmed close cannot lose it. | `reading/R65` |
| FR-003 | Saved progress SHALL hold the settled slots, the current step, the name and the date. | `reading/R65` |
| FR-004 | Opening Use template for a template with saved progress SHALL restore those slots, step, name and date instead of starting empty. | `reading/R65` |
| FR-005 | A saved slot whose id is no longer present in the current template SHALL be ignored on restore. | `reading/R65` |
| FR-006 | Closing a dirty modal by Cancel, backdrop or Esc SHALL open a confirmation stating that the progress is saved in this browser session and can be resumed later, with **Stay** and **Leave** actions. | `reading/R65` |
| FR-007 | **Stay** SHALL keep the modal open with its state intact; **Leave** SHALL close it without discarding the saved progress. | `reading/R65` |
| FR-008 | A successful Create SHALL clear the saved progress for that template. | `reading/R65` |
| FR-009 | Saving, restoring and abandoning progress SHALL leave the template byte-identical, preserving `reading/R36`. | `reading/R65` |

### Key Entities

- **Template progress** — a browser-session record keyed by template id: settled slots (slot id →
  resolution), step, name, date. It is client state; there is no model, endpoint or migration.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | Two templates keep separate progress | E2E: settle in A, close, open B (all unset), reopen A (restored) |
| SC-002 | A reload does not lose progress | E2E: settle, `page.reload()`, reopen the modal and read the settled row |
| SC-003 | The confirmation is tied to dirty state | E2E: dirty close shows the layer; a clean close leaves no layer |
| SC-004 | Every close path keeps the work | E2E over Cancel, backdrop and Esc separately |
| SC-005 | A created service consumes its progress | E2E after a successful Create, once FR-008 is answered |

## UI/UX

Static preview at `specs/253-use-template-progress/preview/index.html`, assembled from the project's
own `_generate_modal.html` markup and `generate.css` / `components.css` tokens.

The confirmation reuses the existing `generate__confirm-layer` / `editor__confirm` component, so its
measured geometry is unchanged: layer `inset: 0`, `padding: 24px`, `z-index: 6`; card
`width: min(440px, 100%)`, `padding: 20px 22px 18px`, `border-radius: 12px`; title
`650 17px/1.3 ui-sans-serif`; body `400 13px/1.5 ui-sans-serif`; action row `gap: 8px`,
`margin-top: 8px`. Only the words and the two actions are new.

Measured in the preview at 1440×1000, dark, 1×: the rendered confirm card is **347.5 × 184.6 px** at
x 49, y 321.7 inside the 840 × 760 sheet. Ten Playwright assertions pass with zero console errors
(`preview/probe.py`).

States reachable by hand in the preview: clean close (no layer), dirty close (layer), **Stay** (rows
still settled), **Leave** (modal closed, reopen restores), template B (independent empty state), and
the browser-session boundary (storage cleared).

## Assumptions

- The owner chose **session storage**: progress survives reloads and in-page navigation but is lost
  when the browser session closes. No server or API work is involved.
- The owner chose **continuous save**: progress is written on every change, so even an unconfirmed
  close or a reload keeps it; the confirmation is informational, not the save trigger.
- Restoration is automatic on open — there is no separate "Resume?" prompt — because the owner asked
  that progress "can be resumed later" and the modal already opens on demand.
- Slot ids are stable across a template's lifetime; stale ids from an edited template are dropped.
- A successful Create consumes the work: the saved progress for that template is cleared, so the next
  Use template starts empty. A failed Create keeps it.

## Clarifications

### Session 2026-11-28

- Q: Where should a template's in-progress state be saved? → A: Session only — the progress is lost
  when the browser session is closed. (Owner answer; research was not needed.)
- Q: When should progress be written? → A: Continuously — after every slot/name/date change, so a
  reload or any close keeps it; the close confirm just tells the user it is safe to leave. (Owner
  answer.)
- Q: After a successful Create, what happens to that template's saved progress? → A: Clear it — the
  service was created, so the next Use template starts empty. (Owner answer; FR-008.)

No `[NEEDS CLARIFICATION]` markers remain.
