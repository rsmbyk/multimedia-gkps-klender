# Feature Specification: a surface re-reads the session it is showing

**Slice**: `specs/186-display-session-refresh`
**Branch**: `fix/186-display-session-refresh` (stacked on `feat/185-dock-goto`)
**Created**: 2026-11-04
**Status**: Accepted — gate 1 2026-11-04 · gate 2 2026-11-04 (checklist 8/8 ticked)
**Input**: *"the dock is still marking a service as on screen while the browser considers that display expired"* — the
owner's answer to a live out-of-sync report, after the overlay's diagnostic showed `session REFUSED` beside a dock that
still showed the service on air.

## What the surfaces do today

Spec 184 bounded the display state's life to the browser session: `read()` refuses a stored state whose `session` does
not match the browser's marker, and every surface reads through it. That refusal happens **when a surface reads** — and
a surface that is already open only reads again when something writes: on a channel message, on a `storage` event, or
on its own verbs.

A tab that outlives the browser session therefore keeps painting what it painted: the marker is a session cookie, the
cookie goes when the browser closes (or when the jar is cleared), `localStorage` survives, and the tab's own read has
not been asked again. The painter and the store disagree until the next write.

Measured on the worktree server (`/obs/dock`, 2026-11-04):

| Step | `gkpsDisplay.read()` | what the dock painted |
| --- | --- | --- |
| service 142 projected, screen 2 | `{service: 142, on: true}` | 1 live row, eye reads `Hide words` |
| the session marker cleared | `{service: null, on: false}` | **still** 1 live row, eye still `Hide words` |
| a freshly loaded dock page, same storage | `{service: null, on: false}` | 0 live rows, eye reads `Display this service` |
| the overlay, same storage | refused (`session REFUSED`) | paints nothing |

The overlay already re-reads on `visibilitychange` and `focus` (`obs-overlay.js:305-308`); the dock reads only after a
write, and the projector only on a channel message or a `storage` event. So two of the three surfaces carry the hole,
and the third proves the fix's shape.

## The surfaces, after this slice

- The **dock** and the **projector** re-read the state when their document becomes visible again and when their window
  takes focus, and repaint from what they read. A state whose stamp no longer matches leaves them idle in that same
  turn: no live row, no block, no detour, the eye reading `Display this service`, the transport disabled as it is with
  nothing on air.
- The **shared module** (`static/web/display.js`) does this once for its subscribers: on a re-read it compares, and
  notifies only when the state actually changed, so a surface that renders on notification follows without a timer of
  its own — and focusing a surface that is in step repaints nothing.
- Nothing new is stored, posted or keyed: the re-read is the existing `read()`, the notification the existing
  subscribers. No new message type, no new verb, no change to the stored shape.
- The overlay keeps its own `visibilitychange`/`focus` re-reads; they become the same rule seen twice, not a second
  mechanism.

## User Scenarios & Testing

### US1 — A tab that outlived its session stops claiming something is on air (P1)

**Why this priority**: it is the contradiction the owner saw — the dock saying "on air" while every new surface refuses
the state, so the operator drives a display nobody else can see.

**Independent Test**: put a service on air in a dock tab, clear the browser's session marker, focus the tab: the dock
paints idle without a reload, and the overlay opened afterwards agrees.

**Acceptance scenarios**

1. **Given** a service on air and a dock tab painting it **When** the session marker is cleared and the tab is focused
   **Then** the dock marks no entry, no screen row, draws no block, and its eye reads `Display this service`.
2. **Given** the same **When** the tab becomes visible again without being focused **Then** the same idle paint happens.
3. **Given** a state whose stamp still matches **When** a surface is focused **Then** nothing repaints.
4. **Given** a projector painting a service or a go to **When** its session marker is cleared and it is focused
   **Then** it paints no screen.

### US2 — The rule is one read, not a second mechanism (P1)

**Why this priority**: two re-read paths would drift; the point is that every surface gets its truth from the same place.

**Independent Test**: with the module's subscriber list empty, a focus event on a dock page changes nothing observable;
with a subscriber, a changed re-read notifies it once.

**Acceptance scenarios**

1. **Given** a re-read that returns the same state **When** it finishes **Then** no subscriber is notified.
2. **Given** a re-read that returns a different state **When** it finishes **Then** every subscriber is notified once.
3. **Given** the overlay's own re-reads **When** the module's rule is exercised **Then** they remain, and neither
   double-paints.

### Edge Cases

- **When** the browser cannot hold a cookie at all (spec 184's own edge) **Then** a re-read reads the same empty state
  the first paint did, and a surface stays idle without an error.
- **When** a surface is hidden while a write lands **Then** the channel/storage path still paints as it does today; the
  re-read adds nothing when nothing changed.
- **When** the document is focused repeatedly in a burst **Then** the state is compared, not repainted, each time.
- **When** the stored state is corrupt **Then** the re-read reads it as no state, as `read()` already does.
- **When** the tab is in the back/forward cache and restored **Then** the restore fires `pageshow`; the same re-read
  covers it.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | The dock and the projector SHALL re-read the display state when their document becomes visible and when their window gains focus, and SHALL repaint from that read in the same turn. | `display-state/R3` (new) |
| FR-002 | `static/web/display.js` SHALL expose the re-read as the module's own act — comparing the read with what it holds and notifying its subscribers only when they differ — so a surface that renders on notification needs no timer. | `display-state/R3` (new) |
| FR-003 | With no display on air, or a state whose session stamp no longer matches, a re-read SHALL leave every surface painting nothing: no live row, no go to block, no detour, no overlay plate, and the dock's eye reading `Display this service`. | `display-state/R1` (kept), `display-state/R3` (new) |
| FR-004 | A re-read SHALL NOT introduce storage, a channel message, a verb or a shape change: it reads what `read()` already reads and notifies the subscribers that already exist. | `display-state/R3` (new) |
| FR-005 | A re-read that finds the state unchanged SHALL notify nobody and repaint nothing. | `display-state/R3` (new) |
| FR-006 | The overlay's existing `visibilitychange` and `focus` re-reads SHALL keep working as they are; the slice adds no second path to them. | `overlay/R1` (kept) |

### Key Entities

- **Session marker** — the cookie spec 184 mints; its presence and value decide whether a stored state is a state.
- **Re-read** — one call to `read()`, compared with the state the module holds, notifying only on change.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | After the marker is cleared, one focus or visibility change leaves the dock painting nothing, without a reload. | E2E: project, clear the cookie, focus, count live marks and read the eye's label. |
| SC-002 | The same for the projector: no `.screen.is-active`, `data-showing="false"`. | E2E: project, clear the cookie, focus, read the body's state. |
| SC-003 | A focus with the state unchanged repaints nothing. | E2E: a `MutationObserver` over the list counts 0 mutations across a focus. |
| SC-004 | No new key, message or verb: the stored JSON's keys and the channel's message types are the ones spec 185 left. | Read of the stored JSON and of the module's exports. |

## UI/UX

`n/a — nothing visible changes.` The defect is a stale paint that only exists after the browser session ends; no new
surface, state, colour or motion is introduced, and the fix's evidence is the E2E readouts above (SC-001 to SC-003),
not a preview. The dock and the projector keep the look they have.

## Assumptions

- The re-read's triggers are `visibilitychange` (when becoming visible), window `focus`, and `pageshow`; a `storage`
  event and a channel message keep their present meaning and are not replaced.
- "In the same turn" means the repaint starts inside the event handler — no timeout, no polling interval.
- The session marker stays a session cookie with no expiry (spec 184's own shape); this slice does not change how it is
  minted, only when the surfaces look again.
- A frame-rate timer is not the answer: it would repaint surfaces that have nothing to change and burn an OBS dock's
  budget for a condition that changes once per browser session.

## Clarifications

None yet — nothing was asked before drafting.
