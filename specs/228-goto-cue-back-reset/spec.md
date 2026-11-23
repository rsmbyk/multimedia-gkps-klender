# Feature Specification: Back clears the Go To from the cue over an empty stage

**Slice**: `specs/228-goto-cue-back-reset`
**Branch**: `fix/228-goto-cue-back-reset`
**Created**: 2026-11-23
**Status**: Accepted (Gate 1 2026-11-23)
**Input**: "when you detour goto from those situations (no service, no entries), the cue stays in the goto information"
**Demand**: `ITEM-243`
**Capability**: modifies `projector/R2`

## User Scenarios & Testing

### US1 — Leaving a Go To returns the cue to the empty stage (P1)

**Why this priority**: spec 227 made the cue name the Go To over zero screens, but the empty-stage
early return in `renderCue()` leaves that DOM untouched on the way out. Back removes the detour and
clears the shared state while the cue still names the passage or song, shows its baits and offers
`back to service` — a control for a Go To that no longer exists. The operator reads stale
information and may press a dead control. This is the only behaviour the finding asks to change.

**Independent Test**: open a projector with no service (or on a service with no entries), start a
Go To, press the cue's Back (or the dock's Back), and read the cue. It carries no passage or song
label, no flip, no baits, no progress and no Back control — the same empty cue as before any Go To.

**Acceptance scenarios**

1. **Given** a projector with no service and a passage Go To on air **When** its cue's Back is
   pressed **Then** the cue is empty: no passage label, no translation flip, no Back control.
2. **Given** a projector on a service with no entries and a song Go To on air **When** its cue's
   Back is pressed **Then** no song label and no bait buttons remain.
3. **Given** a Go To started from the dock with no service under it **When** Back is pressed on the
   dock **Then** the projector's cue clears through the shared state.
4. **Given** a projector with no service that has never shown a Go To **When** it renders **Then**
   its cue is in the same empty state as after Back.
5. **Given** a service with entries **When** a Go To starts and ends **Then** the populated cue path
   is untouched: it returns to the entry's label, baits and next control.

### US2 — An idle empty projector has no phantom mouse controls (P2)

**Why this priority**: once the stage is empty there is nothing to step, hide or show, yet the
edge and centre mouse zones still draw their arrows and hide/show icons, the pointer still hides
itself after two seconds, and the cue keeps a bare `·` separator. Those affordances promise
actions that do nothing. The operator keeps the fullscreen gesture and the cue's own buttons.

**Independent Test**: open a projector with no service (or on a service with no entries) and idle
it. The cue's visible text is empty; the separator is not displayed; the mouse zones take no
pointer events; after 2.4s the pointer is still visible with the normal cursor; a click still
fullscreens the window; the service list, keys and find still open.

**Acceptance scenarios**

1. **Given** an idle projector with no service **When** the cue is read **Then** it shows no
   separator, no next control and no text.
2. **Given** the same projector **When** an edge or centre zone is clicked **Then** nothing steps,
   hides or shows; the zones take no pointer events.
3. **Given** the same projector **When** the pointer is left still for over two seconds **Then** it
   is not hidden and its cursor is the normal one.
4. **Given** the same projector **When** the screen is clicked **Then** it still fullscreens; the
   service list, keys sheet and find band still open.
5. **Given** a Go To detour over the same empty stage **When** it is up **Then** the Go To cue,
   its baits and Back are unchanged from spec 227 — the idle rules apply only when it is gone.

### Edge Cases

- `paintIdle()` calls `renderCue()` but paints no screens, so the clear must live in `renderCue()`
  itself, not in one particular caller.
- The `.cue-separator` is part of the template; it is hidden by CSS only while the idle empty
  state holds, so a populated service keeps its separator and the Go To detour keeps its label.
- A running untitled-text label cannot exist with no entries; the existing
  `clearRunningCueLabels()` at the top of `renderCue()` already handles it.
- The entry-list sheet is not populated on an empty service, so no separate clear is needed there.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | When the stage holds no screens and no Go To is up, `renderCue()` SHALL clear the cue's Go To label, translation flip, baits and progress. | `modified: projector/R2` |
| FR-002 | In that state the Back control SHALL be hidden, not displayed at all, unpressed, unnamed and labelled `No next entry`; its lone right-arrow icon SHALL NOT paint. | `modified: projector/R2` |
| FR-003 | The clear SHALL run on every path that ends a Go To over an empty stage — the projector's Back, the dock's Back and an idle re-read — because all three reach `renderCue()`. | `modified: projector/R2` |
| FR-004 | The detour cue SHALL still paint its label and controls while the Go To is up (spec 227); only its removal changes. | `modified: projector/R2` |
| FR-005 | The populated service's cue path SHALL be unchanged; no state, message or template is added and only `projector.js` and `projector.css` change. | `modified: projector/R2` |
| FR-006 | While the stage holds no screens and no Go To is up, the cue's `.cue-separator` SHALL NOT be displayed, leaving the cue with no visible text. | `modified: projector/R2` |
| FR-007 | In that state the mouse zones SHALL take no pointer events, so edge and centre clicks cannot step, hide or show; the fullscreen click on the screen SHALL still work. | `modified: projector/R2` |
| FR-008 | In that state the pointer SHALL NOT auto-hide: no `cursor-hidden` class, and the normal cursor remains. | `modified: projector/R2` |
| FR-009 | The cue's service-list button, the keys sheet and the find band SHALL remain usable, and a Go To detour over the empty stage SHALL keep its spec 227 cue. | `modified: projector/R2` |

### Key Entities

None. The change is the empty branch of an existing render function plus a body-state class used by
two CSS rules.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | After Back with no service, the cue prefix is empty and no flip or Back control remains. | Playwright read-back of `#cue-prefix`, `.cue-translation` and `#cue-next`. |
| SC-002 | After Back over a service with no entries, no bait buttons remain. | Playwright count of `#cue-baits .cue-bait`. |
| SC-003 | Both projector- and dock-initiated Back clear the cue, and the populated-service path is unchanged. | The 31 tests in `test_goto_shared_state` + `test_dock_goto` stay green. |
| SC-004 | The idle empty cue shows no separator and no next, and the mouse zones take no pointer events in both empty situations. | Playwright computed styles and `innerText` in `test_an_idle_empty_cue_has_no_separator_and_no_next`. |
| SC-005 | The pointer stays visible, fullscreen still works, and the service list, keys and find still open. | Playwright class/computed-style readback and a real fullscreen click. |

## UI/UX

`live preview at http://127.0.0.1:8765/projector` — the slice worktree's own server, hard-reloaded
after the JS edit. Start a Go To with `g`, press the cue's Back, and compare with a page that never
had one. The read-back harness is `specs/228-goto-cue-back-reset/preview/probe.py`.

- **Before (measured, 1280×800, unfixed code)**: with `goto: null`, `detour: false` and zero screens,
  the cue still reads `· HAL 1 Jahowa Sihol Pujionku ·12345671/2 back to service`; prefix
  `HAL 1 Jahowa Sihol Pujionku ·`, seven baits, `back to service`, `#cue-next.hidden === false`.
- **After (measured, same route)**: with the same state, the cue reads `·` before the revision and
  nothing visible after it — prefix empty, zero baits, no flip, Back empty and
  `#cue-next.hidden === true`. During the Go To it still reads
  `HAL 1 Jahowa Sihol Pujionku ·` with seven baits and `back to service`.
- **Idle HUD (measured, 1280×800, after the revision)**: cue `innerText` is `''`,
  `.cue-separator` computed `display: none`, `.mouse-zone--next` computed `pointerEvents: none`,
  `#cue-next.hidden === true`; after 2.4s `body.cursor-hidden === false` and body cursor `auto`;
  `.keys` and `#cue-service` keep `pointerEvents: auto`; a click at (100, 100) still enters
  fullscreen (`document.fullscreenElement !== null`).
- **The lone arrow (measured)**: before the second revision `#cue-next` computed `display: flex`
  despite `hidden === true`, and `#cue-arrow` painted 12.8 × 12.8; after the `.cue-next[hidden]`
  rule its display is `none` and the arrow box is 0 × 0, with no visible cue text.
- **Typography and colour**: unchanged; no new token, face or size. The separator keeps its own
  rule when a service holds entries.
- **States**: passage with no service; song with no entries; Back from the cue; Back from the dock;
  idle re-read; idle empty HUD; Go To detour over the empty stage; populated service.
- **Motion**: none added or removed.
- **Responsive**: no new box or viewport rule; the same two CSS switches apply at every size.

## Assumptions

- The cause is the empty-stage early return in `renderCue()`: spec 227 moved the detour check above
  it but left the return itself with no DOM work, so the detour's cue survives its own state.
- The clear belongs in `renderCue()`, not in `leaveDetour()` or `paintIdle()`, because every exit
  path already calls it; a caller-specific clear would miss the idle re-read.
- Hiding `#cue-next` in the empty state matches the populated path's own `cueNext.hidden = !next`
  when there is no next entry.
- `syncEmptyNotice()` already knows the idle state (notice visible, no detour, no screens), so it is
  the single source for the `empty-stage` body class; the fullscreen capture handler stays on the
  screen, which is still hit-testable when the zones are disabled.
- The cue's own buttons stay out of the disabled set: the owner asked to keep the service list,
  keys and find usable; only the phantom edge/centre zones and cursor auto-hide go away.
- The bump is `patch`, applied at delivery rather than in implementation commits.

## Clarifications

No open questions. Zero clarification markers remain.
