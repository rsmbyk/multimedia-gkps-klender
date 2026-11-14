# Spec 026: Keep editing while projecting, and keep the display in step

- **ID:** 026
- **Status:** Accepted (owner, 2026-10-08)
- **Item:** ITEM-028
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** minor

## Intent

The projector is a working surface, not a lock. While a Tata Ibadah is on screen the operator
should still be able to add, edit, delete and reorder its entries, have a reorder take effect the
moment it is dropped, and see the display follow every change — without pressing Update.

Today the shell refuses those actions while this browser is projecting, holds a reorder until an
explicit Save, and only re-reads the display when the operator asks. This slice removes all three
frictions while keeping the display's own state exactly where it is (in the browser that started
it, never on the server).

## Scope

### In scope

- Entry add / edit / delete (new entries and legacy old rows) and reorder are **never** refused
  because a Tata Ibadah is being displayed.
- A reorder is written as soon as it is made — on a pointer drop, and on a keyboard grip move.
  There is no saved/unsaved distinction, nothing to discard, and no "leave without saving" question.
- After every successful entry add / edit / delete / reorder, the running projector re-reads and
  follows, keeping its place.
- The projector keeps its place across a re-read. *(Spec 028 removed the manual **Update the current
  state** control; the automatic follow is now the only re-read.)*

### Out of scope

- OBS browser sources and second-laptop fan-out: those need a server push, which this slice does not
  add. The display stays a same-browser popup over the existing channel.
- Server-side projection state, new endpoints, or any change to the `web-entry-reorder` contract.
- Any OBS dock / source / settings page, and the legacy DRF API payloads.
- Any UI or accessibility change beyond removing the reorder mode's chrome.

## Domain rules

- **Projection never blocks an entry action.** Being on screen may not stop, decline, or delay an
  add, edit, delete, or reorder. *(Amends spec 006: "The entry lock belongs to the browser that is
  displaying" and its "Display mode blocks entry edits across that browser's tabs" scenario;
  supersedes spec 021, which kept the lock and only hid its explanation.)*
- **A reorder is written when it is made.** A completed drop, or a keyboard grip move, persists the
  order at once; the page keeps no pending order to Save or Discard, and leaving it never asks.
  *(Amends spec 006 slice 3: "Reorder is transactional in the UI" and its "Reorder holds until
  saved" scenario.)*
- **One running order, unchanged.** Entries are still ordered by `order_number`, contiguous from 1;
  the sidebar previews the new order immediately and the pane follows it, as before.
- **Bursts settle on the last order.** Several reorders in quick succession end at the newest order;
  one write is in flight at a time and only the latest is sent next.
- **Every change reaches the display.** A successful add, edit, delete, or reorder tells the display
  on this browser to re-read; the display keeps its place by position, so a change around it is seen
  without the operator pressing anything.
- **The display state is unchanged.** It still lives only in the browser that started it, shared by
  its tabs over the channel; no server record is added.
- **A failed reorder write is visible.** It announces on the status line and the page re-reads the
  true order, so the list cannot keep a change the server did not take.

## Acceptance scenarios

### Scenario: Adding, editing and deleting stay available while projecting

- **Given** this browser is projecting a Tata Ibadah
- **When** I add an entry, edit an entry, or delete an entry (new entries and legacy old rows alike)
- **Then** the action is allowed, and no refusal is shown

### Scenario: Reordering stays available while projecting

- **Given** this browser is projecting a Tata Ibadah
- **When** I drag an entry's grip, or move it with the arrow keys
- **Then** the reorder is allowed

### Scenario: A drop persists at once

- **Given** a service order with several entries
- **When** I drag one to a new position and release it
- **Then** the new order is written immediately, the sidebar and the pane show it, and no Save
  control appears
- **When** I reload the Tata Ibadah
- **Then** the order I dropped is the order that came back

### Scenario: A keyboard move persists

- **Given** an entry's grip has keyboard focus
- **When** I move the entry with the arrow keys
- **Then** the new order is written, with the writes coalesced to the final order

### Scenario: Leaving a reordered page never asks

- **Given** I have just reordered an entry in place
- **When** I open another Tata Ibadah, run a search, or close the tab
- **Then** no confirmation appears, because there is nothing unsaved to lose

### Scenario: The display follows an add

- **Given** the projector is open and showing a Tata Ibadah
- **When** I add an entry in the shell
- **Then** the projector reflects the new entry without my pressing Update the current state

### Scenario: The display follows an edit

- **Given** the projector is open and showing a Tata Ibadah
- **When** I edit an entry that is part of it
- **Then** the projector reflects the edit without my pressing Update the current state

### Scenario: The display follows a delete

- **Given** the projector is open and showing a Tata Ibadah
- **When** I delete an entry
- **Then** the projector no longer shows the deleted entry, keeping its place

### Scenario: The display follows a reorder

- **Given** the projector is open and showing a Tata Ibadah
- **When** I drop an entry into a new position
- **Then** the projector re-reads and shows the new order without my pressing Update the current state

### Scenario: A re-read keeps the place (manual control superseded by spec 028)

- **Given** the projector is open and showing a Tata Ibadah, and a saved change makes it re-read
- **Then** the projector re-reads the page and keeps its place, as before

### Scenario: A failed reorder write is surfaced

- **Given** a reorder whose write fails
- **When** the failure returns
- **Then** the page announces it and shows the true order again

## Traceability

- Domain/app tests: `multimedia/web/tests.py`.
- E2E: `tests/e2e/test_projector.py`, `tests/e2e/test_reorder.py`.
- Amended by: spec 028 (the manual Update control is removed; the automatic follow remains).
- Implementation: `static/web/display.js`, `static/web/projector.js`, `static/web/reorder.js`,
  `static/web/entries.js`, `static/web/reading.js`,
  `multimedia/web/templates/reading/{base,tatib}.html`.
