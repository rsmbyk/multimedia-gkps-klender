# Feature Specification: Use template progress persists for seven days

**Slice**: `specs/255-use-template-progress-persist`
**Branch**: `feat/255-use-template-progress-persist`
**Created**: 2026-11-28
**Status**: Accepted (Gate 1, 2026-11-28 — the owner saw all three indicators, chose A, then answered "accept")
**Input**: "can you make the progress save to survive the browser session and persist for 7 days instead? also add some indicator/modifier on the Use template button when a template has a progress saved"

## User Scenarios & Testing

### US1 — Progress outlives the browser session, for seven days (P1)

**Why this priority**: Spec 253 keeps progress for one browser session, so closing the browser loses
several slot resolutions. The owner wants the work to survive that, on a seven-day clock measured
from the last change.

**Independent Test**: Settle a slot, close the whole browser, open a new one within seven days and
reopen the template: the slot is settled. Age the record past seven days and it is gone.

**Acceptance scenarios**

1. **Given** progress saved in one browser session, **When** the browser is closed and reopened
   within seven days, **Then** the template's slots, step, name and date come back.
2. **Given** a record last written seven days and one second ago, **When** the template is opened,
   **Then** it starts empty and the record is removed.
3. **Given** a record written six days ago, **When** a slot is settled, **Then** the clock restarts
   at that moment and the record survives another seven days.
4. **Given** two templates, **When** each is settled, **Then** each keeps its own clock and its own
   record.

### US2 — The Use template button shows a saved draft (P2)

**Why this priority**: Once progress survives sessions, the operator cannot tell from the stage
whether a template has unfinished work. The button must say so before the modal opens.

**Independent Test**: With a live record, the template page's Use template button carries the saved
mark on load; without one, it does not.

**Acceptance scenarios**

1. **Given** a template with a live saved record, **When** its page paints, **Then** the Use template
   button carries the saved mark without opening the modal.
2. **Given** a template with no record, or a record older than seven days, **When** the page paints,
   **Then** the button carries no mark.
3. **Given** an open modal with no saved work, **When** the first slot is settled, **Then** the mark
   is present when the modal closes.
4. **Given** a saved draft, **When** a service is created from it, **Then** the next visit paints no
   mark.

### Edge Cases

- **When** storage is unavailable or full, **Then** the modal still opens and works; persistence and
  the mark are best-effort.
- **When** a saved slot id no longer exists, **Then** it is ignored on restore (as today).
- **When** the record is malformed or has an unknown `v`, **Then** it is treated as absent.
- **When** the page is a dated service, **Then** there is no Use template button and no mark.
- **When** the record expires while the page is open, **Then** the mark may remain until the next
  load; reopening the template then starts empty and removes the record.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | Progress SHALL be stored in `localStorage` under `gkps:generate:<templateId>` as a `v: 2` record holding the settled slots, step, name, date and a `savedAt` timestamp. | `reading/R67` |
| FR-002 | Every settled slot, choice pick, name change, date change and step change SHALL rewrite `savedAt`, so the seven-day clock runs from the last change. | `reading/R67` |
| FR-003 | A record whose `savedAt` is more than seven days (168 hours) old SHALL be treated as absent and removed. | `reading/R67` |
| FR-004 | Opening Use template SHALL restore a live record exactly as spec 253 did, still dropping slot ids that no longer exist. | `reading/R67` |
| FR-005 | A successful Create SHALL clear that template's record; a failed one SHALL keep it. | `reading/R67` |
| FR-006 | A template page whose template has a live record SHALL mark its Use template button before the modal opens with a 7 × 7 px corner dot inset 4px from the button's top-right border box (3px inside its 1px border), the label and button width unchanged. | `reading/R67` |
| FR-007 | The mark SHALL NOT be colour-only: the button's accessible name SHALL state that a draft is saved. | `reading/R67` |
| FR-008 | The mark SHALL appear when the first change saves and SHALL be gone after a successful Create. | `reading/R67` |
| FR-009 | Saving, restoring, expiring and abandoning SHALL leave the template byte-identical, preserving `reading/R36`. | `reading/R67` |
| FR-010 | A browser that refuses storage SHALL still open and operate the modal; no error SHALL be surfaced. | `reading/R67` |
| FR-011 | The leave confirmation SHALL say the progress is saved on this browser for seven days, not in this browser session. | `reading/R67` |

### Key Entities

- **Template progress** — a browser-local record per template, now persisted in `localStorage` with a
  `savedAt` timestamp. Still no model, endpoint or migration.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | A new browser session restores progress | E2E: new browser context, same origin, reopen the template |
| SC-002 | Older than seven days is gone | E2E: write a `savedAt` 168h+1s old, open, assert empty and the key removed |
| SC-003 | Six days plus an edit keeps it | E2E: write a six-day-old record, settle a slot, assert `savedAt` is now |
| SC-004 | The mark tracks the record | E2E: with and without a live record, assert the button's mark and accessible name |
| SC-005 | Create clears the mark | E2E: create, return to the template, assert no mark |
| SC-006 | The mark is accessible | E2E: assert the button's accessible name names the saved draft |

## UI/UX

The chosen indicator is **variant A — corner dot**, previewed at
`specs/255-use-template-progress-persist/preview/index.html` on the real `read__project` button:

- The button keeps its 34px height, 9px radius and filled `--active-bg` style, and its width does
  not change: **135.8 px** with and without the mark.
- The mark is a **7 × 7 px** dot, `border-radius: 50%`, filled `--active-ink`, positioned 3px
  inside the button's 1px border — **4px from its border box** (measured at +124.8, +4 inside a
  135.8 × 34 box).
- The button carries `data-draft="true"` while the mark shows; the dot is `aria-hidden`, and the
  button's accessible name becomes **"Use template, draft saved"**. The visible label is unchanged.
- Variants B (label suffix, +81.8px) and C (inline dot, +12px) were rendered in the same preview and
  not chosen; the preview keeps all three for comparison.

The 7-day period is 168 hours from `savedAt`; no calendar rounding.

## Assumptions

- `localStorage`, not a server record: the owner asked for persistence across browser sessions, and
  the app still has no account-scoped draft.
- Seven days is 168 hours from the last change, sliding on every save (owner choice, Clarify).
- Existing `sessionStorage` records from spec 253 are not migrated; they die with that session.
  The feature reached `develop` today and production does not carry it.
- The mark lives only on the stage's Use template button; sidebar rows are unchanged.

## Clarifications

### Session 2026-11-28

- Q: What does the 7-day lifetime count from? → A: Seven days since the last change — every edit
  resets the clock. (Owner answer.)
- Q: Which indicator shape? → A: **A — corner dot**, a 7 × 7 px dot inset 4px from the button's
  border box, label and width unchanged. The owner saw all three in the preview and chose A.
  Recorded in FR-006 and UI/UX.

No `[NEEDS CLARIFICATION]` markers remain.