# Feature Specification: a newly created Template opens on the reading stage

**Slice**: `specs/234-open-created-template`
**Branch**: `feat/234-open-created-template`
**Created**: 2026-11-23
**Status**: Accepted — gate 1, 2026-11-23
**Input**: "when you create a template tata ibadah, it does not open it immediatelly in reading page. only dated services have this behavior"
**Demand**: `ITEM-249` (opened at Specify)
**Capability**: `reading/R46` — *modified*, not added (the existing requirement says the opposite today)

Today a successful create of a Normal (dated) Tata Ibadah opens it in place on the reading stage
(`static/web/reading.js`, the `editor:saved` handler). The server returns `record_kind: 0` for a
service and `record_kind: 1` for a template (`multimedia/web/reading/views.py:212-214`); the handler
navigates only for `0`. A template create therefore falls through to the ordinary list refresh:
the sidebar lists the new template but the URL and stage stay where they were. This is currently
**intentional**: `docs/spec/reading.md` R46 says creating a Template "SHALL NOT open a stage", and
`tests/e2e/test_editor.py::test_a_template_create_keeps_the_stage` asserts the URL stays `/tatib/`.
The owner has now asked for templates to behave like dated services on create, so R46 is modified
and that test is superseded.

Live reproduction on the real pages, 1440×900, base `be9863d2` versus this slice's worktree,
both against the same dedicated preview database (probe: `preview/probe.py`):

| Start | Case | Base — after save | Slice — after save |
| --- | --- | --- | --- |
| `/tatib/` | Template | `/tatib/`, no stage, no current row | `/tatib/<id>/?mode=template`, stage names the template, row current |
| `/tatib/?mode=template` | Template | `/tatib/?mode=template`, no stage | `/tatib/<id>/?mode=template`, stage names the template, row current |
| `/tatib/` | Dated service | `/tatib/<id>/` | `/tatib/<id>/` (unchanged) |

## User Scenarios & Testing

### US1 — Creating a Template opens it immediately (P1)

**Why this priority**: it is the reported case. The operator saves a template and expects to
land on it ready to add entries, exactly as saving a dated service does; today a second click
on the new sidebar row is needed.
**Independent Test**: from `/tatib/`, create a template through the sidebar's Add button; after
the save the URL is `/tatib/<id>/?mode=template`, the stage heading names the saved template,
its sidebar row carries `aria-current="true"`, and the child pane is open.

**Acceptance scenarios**

1. **Given** the Tata Ibadah list **When** a new record is saved with the **Template** type
   **Then** the stage opens that template at `/tatib/<id>/?mode=template` with no second click.
2. **Given** the same create from `/tatib/?mode=template` **When** the save succeeds
   **Then** the same stage opens and the template mode stays pressed.
3. **Given** a template with no entries **When** it opens **Then** its own empty-service
   invitation and add actions are shown, as they are after clicking the row by hand.

### US2 — The open keeps the dated-create guarantees (P1)

**Why this priority**: spec 209 already fixed the no-reload, panel-state and focus behaviour for
a created service. A template create must travel the same path, or the fix introduces a second,
noticeably different create flow.
**Independent Test**: set a page marker, create a template, and read the page back: the marker
and `performance.timeOrigin` are unchanged, `data-nav` keeps its value, `data-ch` is `open`, and
quiet focus is restored to the saved row.

**Acceptance scenarios**

1. **Given** a saved create response for a template **When** the stage opens **Then** no document
   reload occurs: an in-page marker survives, `performance.timeOrigin` is unchanged and the
   `data-nav` choice is preserved.
2. **Given** the new template's sidebar row **When** the stage settles **Then** that row carries
   `aria-current="true"` and quiet focus with the `row-flash` cue is restored to it.
3. **Given** the operator's panel state **When** the template opens **Then** the child pane opens
   on the template's contents as it does for a dated service.

### US3 — Every other create path stays as it is (P2)

**Why this priority**: the same `editor:saved` handler also serves dated services, edits, the
template generator and copy-as-template. Widening the condition must not change those paths.
**Independent Test**: create a dated service, edit an existing record, refuse a create, generate
a service from a template and copy a service as a template; each lands exactly where it does today.

**Acceptance scenarios**

1. **Given** a Normal service with a date **When** it is created **Then** it opens at
   `/tatib/<id>/` (no `mode` query), as before.
2. **Given** an existing service or template **When** it is edited and saved **Then** the stage
   and URL stay where they were and the list refreshes as before.
3. **Given** a refused create **When** validation or the request fails **Then** no stage opens and
   the dialog and its error handling stay in place.
4. **Given** the template-generate and copy-as-template flows **When** they create a record
   **Then** they continue to land on the record they create, as R46 already requires.

### Edge Cases

- **When** the create is from the template list **Then** the opened stage shows the template list
  in its sidebar, not the dated buckets.
- **When** the template has no date **Then** no date is invented; the stage eyebrow stays
  `Tata Ibadah`, as on a hand-opened template.
- **When** the create response has no `record_kind` **Then** no stage-opening branch runs and the
  original list-refresh behaviour remains.
- **When** the new template's row lies outside the visible part of the sidebar **Then** the
  existing focus-restore reveal scrolls it into view.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | A successful create of a Template SHALL open the saved template on the reading stage at `/tatib/<id>/?mode=template`, replacing the R46 clause that said a Template SHALL NOT open a stage. | `reading/R46` |
| FR-002 | The opened stage SHALL name the new template, mark its sidebar row `aria-current="true"`, show its empty/add actions, and open the child pane. | `reading/R46` |
| FR-003 | The open SHALL use the existing in-place navigation: no document reload, `data-nav` unchanged, quiet focus restored to the new row. | `reading/R46` |
| FR-004 | A dated service create, an edit, a refused create, the template-generate flow and copy-as-template SHALL keep their present destinations and error handling. | `reading/R46` |
| FR-005 | Creating from `/tatib/?mode=template` SHALL open the same stage with the template mode still pressed. | `reading/R46` |

### Superseded wording (kept visible, not deleted)

R46 previously read: *"Creating a Template, editing a service, and saving any other record kind
SHALL keep their present list-refresh behaviour and SHALL NOT open a stage."* and its scenario
*"WHEN a Template is created or an existing service is edited THEN the stage and URL stay where
they were and the list refreshes as before."* Only the Template half is superseded by FR-001;
the edit and other-record halves stand. The test
`tests/e2e/test_editor.py::test_a_template_create_keeps_the_stage` is superseded accordingly at
Implement; until then it is expected to fail against the preview change.

### Key Entities

- **Tata Ibadah record kind** — `record_kind` in the editor save response: `0` Normal (dated),
  `1` Template. Unchanged by this slice; the create handler already receives it.
- **Created-record destination** — URL chosen in the `editor:saved` handler: bare `/tatib/<id>/`
  for a dated service, `/tatib/<id>/?mode=template` for a template.
- **Reading stage** — the `#read` panel and `#panelBody` sidebar row, swapped in place by
  `navigate(..., {kind: 'service', forceServer: true})`.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | A template create lands on its stage | probe E2E: URL `/tatib/<id>/?mode=template`, `#readName` equals the saved name, row `aria-current="true"`, `data-ch="open"` |
| SC-002 | The open is in place | probe E2E: in-page marker `alive`, `performance.timeOrigin` identical before/after, `data-nav` unchanged |
| SC-003 | The template-list start behaves the same | probe E2E from `/tatib/?mode=template`: same destination and `#tatibMode` `aria-pressed="true"` |
| SC-004 | Other flows do not move | probe E2E: dated create still `/tatib/<id>/`; the existing editor tests for edit, refused/failed create, generate and copy stay green |

## UI/UX

No new visual design: the stage, sidebar row and modal are the project's existing components.
The change is which page is on screen after a save, so the numbers are navigation and state
readings at 1440×900, dark scheme, from `preview/probe.py`:

- **Layout / position**: created template stage measured at 1440×900 — `#readName` at x976, y73,
  362×94; template eyebrow at x976, y43, 127×27; empty-service invitation at x1049, y257,
  253×26; current sidebar row at x90, y164, 395×38. No box is added, removed or resized.
- **Size / spacing**: unchanged. The stage uses the same `.read` and `.tatib__item` rules as a
  hand-opened template.
- **Colour / typography**: unchanged.
- **States**: after a template create — URL `/tatib/<id>/?mode=template`, `#tatibMode`
  `aria-pressed="true"`, `data-nav="open"`, `data-ch="open"`, focused row classes
  `book row-flash focus-restore-quiet` with `data-name=<id>`. Before the change the same save left
  URL `/tatib/` (or `/tatib/?mode=template`), empty `#readName`, `data-ch="closed"`, no current row.
  Refused/failed create keeps the dialog open with its existing error state.
- **Motion**: none added. The `service` navigation's existing smooth scroll-to-top still applies;
  no new animation or delay was measured.
- **Responsive**: unchanged — the same stage the row click already opens at every width.

## Assumptions

- The owner approved this change through the question tool on 2026-11-23 before Specify. The live
  preview change was applied to the worktree before this spec was written; it is uncommitted and
  stays that way until Fold (commits start there).
- The template destination carries an explicit `?mode=template`, matching the copy-as-template
  flow's URL, although `TatibView` also derives template mode from the record's kind. This keeps
  the sidebar list and mode button in template mode on arrival.
- The server's `record_kind` contract is unchanged; no endpoint or model is touched.
- Quiet focus for a template row uses the existing `focusKind: 'tatib'` path: template rows carry
  the same `data-editor-open="tatib"` button as dated rows.
- The next free numbers were checked against `develop`, `origin/develop` and all localrefs before
  the worktree was cut: spec `234`, card `ITEM-249`.
- No constitution file exists at the repo root, so SDD-01 is skipped silently.

## Clarifications

### Session 2026-11-23

- Q: should a newly created Template open on the reading stage like a dated service? → A: yes;
  change R46 and take it through the spec gates.
- Q: which URL for the template? → assumed from the approved question: `/tatib/<id>/?mode=template`,
  the same destination copy-as-template already uses. No separate question was needed.
