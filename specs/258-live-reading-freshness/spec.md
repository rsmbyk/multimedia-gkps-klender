# Feature Specification: live reading freshness

**Slice**: `specs/258-live-reading-freshness`
**Branch**: `feat/258-live-reading-freshness`
**Created**: 2026-11-28
**Status**: Draft
**Input**: ITEM-272 and ITEM-273 from the owner's nine-point change request — invalidate a stale service or song page, and keep sidebars in step with external edits.

## User Scenarios & Testing

### US1 — An open page notices it is stale (P1)

**Why this priority**: a second operator's write must be visible before the first operator tries another edit, even though the server already refuses the stale write.
**Independent Test**: with a service page open, a write made through another client's session makes the page invalid within 10 s.

**Acceptance scenarios**

1. **Given** a service page loaded at version 5 **When** the server's version becomes 6 **Then** the page marks itself invalid within 10 s.
2. **Given** a song page loaded at version 3 **When** a song or verse change makes it version 4 **Then** the page marks itself invalid within 10 s.
3. **Given** the server version still matches **When** the poll repeats **Then** the page is untouched.

### US2 — An invalid page cannot be edited (P1)

**Why this priority**: disabled controls are the visible half of the server's 409 guard.
**Independent Test**: after invalidation, every add/edit/delete, reorder and Project control on that page is disabled in place and every dialog belonging to the page is closed.

**Acceptance scenarios**

1. **Given** an invalidated service page **When** the operator looks at the stage and sidebars **Then** all edit, delete, add, reorder and project controls are disabled in place, with their layout unchanged.
2. **Given** a dialog or the copy-confirmation layer is open **When** invalidation happens **Then** every dialog on that page closes.
3. **Given** an invalidated page **When** a control would previously open a modal **Then** nothing opens.

### US3 — The badge offers a page-only reload (P1)

**Why this priority**: the operator needs an explicit, low-cost way back to current state.
**Independent Test**: the badge appears at the top centre and its Reload button re-fetches only the current page in place.

**Acceptance scenarios**

1. **Given** an invalidated page **When** the badge renders **Then** it says the page was edited elsewhere and carries a Reload button.
2. **Given** the operator presses Reload **When** the fetch completes **Then** the page content is swapped in place without a browser reload and the badge is gone.
3. **Given** an invalidated page **When** the operator does not press Reload **Then** the badge stays until the page changes.

### US4 — Sidebars follow external list changes (P1)

**Why this priority**: a sidebar showing a stale row is misleading even when the stage is current.
**Independent Test**: with a song sidebar open, an edit made elsewhere updates only that row, in place, without a full page refresh.

**Acceptance scenarios**

1. **Given** a songbook, song or service sidebar **When** its list fingerprint changes **Then** it fetches the fresh list fragment and reconciles rows by id.
2. **Given** a row was edited elsewhere **When** reconciliation runs **Then** only that row's content changes; its neighbours keep their nodes and focus.
3. **Given** a row was deleted elsewhere **When** reconciliation runs **Then** only that row is removed.
4. **Given** a row was added elsewhere **When** reconciliation runs **Then** only that row is inserted, animated, into its position under the current filter and sort.

### US5 — Sidebars keep the operator's view (P1)

**Why this priority**: a fresh list that loses the operator's filter, sort or scroll is worse than a stale one.
**Independent Test**: after reconciliation, filter text, sort choice, scroll offset and panel state match the pre-fetch values.

**Acceptance scenarios**

1. **Given** dated services are shown **When** a template is added elsewhere **Then** the dated list does not gain that template.
2. **Given** songs are sorted alphabetically **When** a new song starting with G is added **Then** it is inserted at its alphabetical position, not at the top of the last-modified order.
3. **Given** a filtered sidebar with a scroll offset **When** rows reconcile **Then** the filter text and scroll offset are unchanged.

## Edge Cases

- **When** a poll request fails **Then** the page and sidebars keep their current state and try again at the next interval; no badge is raised for a network error.
- **When** invalidation happens while a modal is open **Then** unsaved modal content is discarded, since the page is no longer trustworthy.
- **When** a sidebar row is both open on the stage and changed elsewhere **Then** the sidebar updates but the stage is not swapped; page invalidation owns the stage.
- **When** two polls overlap **Then** only one request per endpoint is in flight; the later response wins.
- **When** a template is added while the dated-services panel is shown **Then** the services fingerprint is unchanged for that panel.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | A page-version endpoint SHALL return the current version of a named service or song. | `reading/R72` |
| FR-002 | Three list-version endpoints SHALL return a fingerprint of the ordered `(row id, row version)` pairs for songbooks, songs in the open book, and services in the current mode. | `reading/R73` |
| FR-003 | Service and song pages SHALL poll their page-version endpoint every 10 s while the page is visible. | `reading/R72` |
| FR-004 | When the polled version differs from the loaded version, the page SHALL close its dialogs and disable, in place, all add/edit/delete, reorder and Project controls on that page. | `reading/R72` |
| FR-005 | An invalidated page SHALL show a top-centre badge naming the reason and offering Reload. | `reading/R74` |
| FR-006 | Reload SHALL re-fetch the current URL and swap the page content in place, without a browser reload. | `reading/R74` |
| FR-007 | Each sidebar SHALL poll its list-version endpoint every 10 s while visible. | `reading/R73` |
| FR-008 | On a fingerprint change the sidebar SHALL fetch the fresh list fragment and reconcile by row id: update changed rows, remove deleted rows, insert new rows. | `reading/R73` |
| FR-009 | Reconciliation SHALL preserve filter text, chosen sort, scroll offset and panel state. | `reading/R73` |
| FR-010 | A new row SHALL be inserted at the position dictated by the current filter and sort, with an animation, without rebuilding the list. | `reading/R73` |
| FR-011 | A template added while dated services are shown SHALL NOT appear in that list. | `reading/R73` |
| FR-012 | A poll failure SHALL leave state unchanged; a later successful poll SHALL recover. | `reading/R72` |
| FR-013 | Only one request per endpoint SHALL be in flight at a time. | `reading/R72` |

### Key Entities

- **Page version response** — `{version: <int>}` for one service or song; the value the page loaded is the baseline.
- **List fingerprint** — a deterministic string derived from the ordered `(id, version)` pairs of the rows a sidebar currently shows; changing membership, order or a row's version changes it.
- **Invalidated page state** — a client-side flag that closes dialogs, disables page controls and shows the badge until the in-place reload.
- **Reconciled list** — the fresh fragment applied row by row to the existing sidebar DOM.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | A cross-client change invalidates an open page within 10 s | Playwright observes the badge after a second client writes |
| SC-002 | No edit control remains actionable after invalidation | Every covered control is disabled and every dialog is closed |
| SC-003 | Reload does not perform a browser navigation | The page's document object is unchanged after Reload |
| SC-004 | A sidebar edit updates one row without rebuilding the list | Row node identity is preserved for unchanged rows |
| SC-005 | A new row lands in the current order | Alphabetical and last-modified cases both place it correctly |
| SC-006 | Filter, sort and scroll survive reconciliation | Values before and after a fingerprint change match |

## UI/UX

Static preview: `specs/258-live-reading-freshness/preview/index.html` (states and measurements in `preview/README.md`).

- **Layout / position**: at 1440×900 the badge is 289×48, centred with its Reload button 64×30. In the product the candidate position is `top: 12px`; the preview uses 64px only to clear its state toolbar.
- **Size / spacing**: disabled controls keep their boxes (for example the add control remains 58×28) and move only in opacity, from 1 to 0.45.
- **Colour / typography**: the badge uses the canvas, divider and ink tokens; Reload uses the active button pair. No new palette entry.
- **States**: current · invalidated · sidebar insert, each in light and dark.
- **Motion**: a new row runs `0.18s cubic-bezier(.2,.8,.2,1)` from opacity 0 and `translateY(-6px)` to rest; rAF sampling reaches rest by ~250 ms.
- **Responsive**: below 800px the preview drops the sidebar under the stage; the product's existing reading breakpoints still own the real layout.


## Assumptions

- The 10 s cadence matches the dock and overlay already in the product.
- A fingerprint string is sufficient for list change detection; no new persisted list entity is needed.
- Page invalidation is presentation only — the server's 409 from slice 254 is the actual lost-update guard.
- Reload uses the shell's existing in-place refresh path.
- Both cards land on this one spec: ITEM-272 is the delivery card and ITEM-273 is carried with it.

## Clarifications

### Session 2026-11-28

- Q: Combine the four deferred cards? → A: Two first — ITEM-272 and ITEM-273 — in one spec.
- Q: How should polling be wired? → A: Separate endpoints: one for the open page, one per sidebar list.
- Q: What is a sidebar list version? → A: A fingerprint of the ordered `(row id, row version)` pairs in that list.
