# Feature Specification: a newly created service opens on the reading stage

**Slice**: `specs/209-open-created-service`
**Branch**: `feat/209-open-created-service`
**Created**: 2026-11-21
**Status**: Accepted — Gate 1 and Gate 2, 2026-11-21
**Input**: the owner's request, 2026-11-21 — "when you create a service, it should be open immediately"

Today a successful sidebar create only re-renders the lists: the new row appears under Tata Ibadah
but the reading stage stays where it was and the URL stays `/tatib/`. The operator has to click the
new row to open it. Live reproduction on `develop` (compose web at `127.0.0.1:63404`, base
`989347f2`): before save `url=/tatib/`, `#readName=""`, no `aria-current` row, `data-nav=open`,
`data-ch=closed`; after save `url=/tatib/`, `#readName=""`, no `aria-current` row, `data-nav=open`,
`data-ch=closed`, new row `/tatib/317/`, and the in-page marker `set-before-save` still present (so
the save itself does not reload). Clicking that row gives the state this slice wants immediately:
`url=/tatib/317/`, `#readName="Gate1 Probe 209B"`, `data-name="317"` carries `aria-current="true"`,
`data-nav=open`, `data-ch=open`, marker still present.

## User Scenarios & Testing

### US1 — Creating a service opens it on the stage (P1)

**Why this priority**: the whole point of creating a service is to start preparing its order. The
save succeeds and the new row is visible, yet the stage still shows the previous page (or nothing),
so the operator must find and click the row before doing any work. The request is about that missing
step, not about a new control or a new look.
**Independent Test**: on `/tatib/`, create a dated Normal service named `Ibadah Baru`; after the
save resolves, read the stage: URL `/tatib/<new id>/`, heading `Ibadah Baru`, the new row carries
`aria-current="true"`, and the service's entry controls are on screen — all without a second click.
On `develop` the URL and heading are unchanged and no row is current.

**Acceptance scenarios**

1. **Given** the Tata Ibadah list is open with any stage state **When** a Normal service is created
   from the sidebar and the save succeeds **Then** the stage shows the new service: its URL is
   `/tatib/<id>/`, the heading is the entered name, the new row is current, and its empty-service
   add actions are present.
2. **Given** the stage already shows another service **When** a Normal service is created
   **Then** the new service replaces it on the stage without a full page load; the previous service
   is no longer current.
3. **Given** a successful create **When** the stage has settled **Then** the child pane is open on
   the new service's contents exactly as it is after clicking that service's row.
4. **Given** a successful create **When** the save response is processed **Then** an in-page marker
   set before the save is still present and `performance.timeOrigin` is unchanged — no navigation
   by document reload.

### US2 — Only creates of a Normal service change the stage (P2)

**Why this priority**: the sidebar form creates both a dated service and a Template, and the same
save event is used for edits, entries and other record kinds. Widening the rule would pull a template
(or a song) onto the stage and break the behaviour those paths already have.
**Independent Test**: create a Template from the sidebar and edit an existing service; both keep
today's list refresh and current stage. The template-generate and copy-as-template flows still land
on their new service as they do today.

**Acceptance scenarios**

1. **Given** the sidebar create form **When** a Template is saved **Then** the stage and URL are
   left as they were and the list refreshes as today.
2. **Given** an existing service **When** its name or date is edited **Then** the stage is not
   switched to it; editing keeps its current in-place refresh.
3. **Given** a fill-in-and-choice generate flow or a Copy-as-template action **When** it finishes
   **Then** the browser still lands on the created record's URL, as it does on `develop`.
4. **Given** a song, songbook or verse save **When** it succeeds **Then** nothing about this slice's
   service navigation runs.

### US3 — A refused create changes nothing (P2)

**Why this priority**: navigating on every save response would be easy to get wrong when the server
answers with validation errors instead of a created record; the stage must never claim a service
that was not written.
**Independent Test**: submit the create form with a missing date; the form re-renders with its
error, the dialog stays open, and the stage and URL are untouched.

**Acceptance scenarios**

1. **Given** the create form with an invalid date **When** the save is refused (HTTP 400)
   **Then** no stage navigation happens and the existing error handling is unchanged.
2. **Given** a refused permission or a failed request **When** the save does not return a created
   service **Then** the stage stays put and the existing failure message is shown.

### Edge Cases

- **When** the newly created service is the first in the list **Then** the empty-service invitation
  is the stage content; no entry is created by this slice.
- **When** the operator created the service from the home page instead of `/tatib/` **Then** the
  same in-place open applies — the create path, not the page it started from, decides.
- **When** the first panel is collapsed or mini **Then** its state is not widened by the save; the
  new service is current in the list whether or not the row is visible.
- **When** the operator is in template mode (`?mode=template`) **Then** creating a Normal service
  still opens it on the dated service route, not under the template list.
- **When** the create response is slow **Then** no preview of the new stage appears before the
  server confirms the record; the stage changes once, on success.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | A successful create of a Normal (dated) Tata Ibadah SHALL open that service on the reading stage in place: the URL becomes `/tatib/<id>/`, the stage heading names the saved service, its row carries `aria-current="true"`, and its order view (including the empty-service state) is shown. | `new: reading/R46` |
| FR-002 | The in-place open SHALL use the reading shell's existing navigation path and SHALL NOT reload the document; the child pane SHALL end open on the new service's contents, matching a click on that service's row. | `reading/R46` |
| FR-003 | The open SHALL NOT change the main panel's `data-nav` state, and SHALL NOT change which record is current in any other list. | `reading/R46` |
| FR-004 | Creating a Template, editing an existing service, and saving any other record kind SHALL keep their present list-refresh behaviour and SHALL NOT open a stage. | `reading/R46` |
| FR-005 | A refused create (validation, permission or request failure) SHALL NOT open a stage, and SHALL keep today's error handling. | `reading/R46` |
| FR-006 | The template-generate and copy-as-template flows SHALL continue to land on the URL of the record they create. | `reading/R36`, `reading/R37` |

### Key Entities

- **Created service** — the `TataIbadah` row returned by the sidebar save: its `id`, `kind` (Normal
  or Template) and `name` decide whether and where the stage opens. No new record or field is added.
- **Reading stage** — the existing `/tatib/<id>/` view: `#readName`, the current `.book` row in the
  first sidebar, and the child pane's service contents, all reached through the shell's in-place
  navigation rather than a document request.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | After one create save the stage URL, heading, current row and empty-service actions match the service just created, with no second click. | Playwright E2E reads `location.pathname`, `#readName`, `.book[aria-current="true"][data-name]`, `.entry__empty-title`. |
| SC-002 | The open is in place: no document reload and no change to `data-nav`. | E2E reads an in-page marker, `performance.timeOrigin` and `document.documentElement.dataset.nav` before and after. |
| SC-003 | Template create, service edit, generate and copy-as-template behave exactly as on the base commit. | E2E assertions in the existing template/editor modules, plus focused new assertions for the two already-navigating flows. |
| SC-004 | A refused create leaves the stage and URL unchanged. | E2E submits an invalid form and compares URL, heading and marker. |

## UI/UX

`n/a — no new look. The stage after the save is the existing `/tatib/<id>/` service page, reached by
the same in-place navigation a row click uses; no control, style, spacing or motion is added.`

The gate-1 material is the measured defect above from the live base commit: after save the URL stays
`/tatib/`, `#readName` is empty, no row is current, `data-ch=closed`; the target state is exactly the
measured click-through state (`/tatib/<id>/`, name filled, row current, `data-nav=open`,
`data-ch=open`, marker preserved). Re-run the measurement with `reproduce.py` in this folder (it
needs the compose web service on `127.0.0.1:63404`).

## Assumptions

- "Service" means a dated Normal Tata Ibadah. A Template is undated and is not a service the
  operator prepares on the stage, so creating one keeps today's list refresh.
- "Open" means the reading stage, as the owner chose on 2026-11-21; the OBS dock and projector are
  untouched by this slice.
- "Immediately" means on the successful save response, before any further click, but not before the
  server has confirmed the record.
- The opening navigation is in place (no full reload), per the owner's choice; it reuses the shell's
  navigation path rather than adding a second mechanism.
- The sidebar form is the only create path that needs changing: template-generate and copy-as-template
  already navigate to the created record (measured in `generate.js:463` and `editors.js:509`).

## Clarifications

### Session 2026-11-21

- Q: Which surface should show the new service right after Create? → A: the reading stage shows the
  new service, in place with no full reload (owner decision).
- No other open questions remain.
