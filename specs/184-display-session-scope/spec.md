# Feature Specification: the active Tata Ibadah lasts only the browser session

**Slice**: `specs/184-display-session-scope`
**Branch**: `fix/184-display-session-scope`
**Created**: 2026-11-03
**Status**: Accepted
**Input**: *"the projector / obs source overlay active tata ibadah should only last for the current
browser session. when the browser reopens, there should be nothing to display until operators
choose to"*

## What the surfaces do today

One object in `localStorage['gkps-display']` decides what is on air in a browser:
`{service, screen, on, translation, at}`. The dock (`static/web/display.js`) and the projector
(`static/web/projector.js`) write it; the caption overlay (`static/web/obs-overlay.js`) and every
reading page read it; the `gkps-service-display` channel carries each change to the other surfaces.

Nothing bounds its life to the browser. `localStorage` outlives the process that wrote it, so the
next time the browser — or OBS, which runs the dock and the overlay in its own CEF browser — starts,
the overlay finds a state it did not write this run and paints it, and the dock's picker still marks
a service as "On screen" before anything has been chosen.

Measured on develop (1.26.0), in a browser profile reopened on the same storage (each measurement is
one Playwright context; a throwaway probe, removed at Fold):

| after every surface closed and a page opened again | today |
| --- | --- |
| overlay children on its stage | **1** (the liturgy plate paints) |
| dock picker rows wearing "On screen" | **1** |
| `localStorage['gkps-display']` | `{"service":1,"screen":0,"on":true,"translation":null,"at":…}` |

Spec 119 made that survival deliberate: *"Catch-up is mandatory… State survives every surface
closing — the display ends only by `release` (or `hide` blanking it), never by a window closing."*
This slice revises the outer boundary only: the display may not outlive the browser session.

## The display state, after this slice

- The state keeps its shape and gains one field: `{service, screen, on, translation, at, session}`.
- `session` is an opaque id — a random string, never a service, screen, translation or operator —
  kept in a **session cookie** `gkps-session` (`Path=/`, `SameSite=Lax`, no expiry). A cookie with
  no expiry is the browser's own definition of a session: it is gone when the browser process exits.
- The cookie is minted by the first **write** of a display state in a browser session. Reading never
  mints one.
- A stored state is a display state **only while `stored.session` equals the cookie's value**. With
  no cookie, or a different value, every surface reads `{service: null, screen: 0, on: false}` and
  paints that — never the stored object, not even for a frame.
- Within the session nothing changes: `localStorage` still carries the state between surfaces, the
  channel still pushes each change, and closing any or every surface still changes nothing.
- The writers stay the dock, the projector and the reading page's Project/Stop control; the readers
  stay the overlay and every surface's renderer. The slice changes what they store, not who may
  write.
- The cookie carries no display data, and no display state reaches the server.

## User Scenarios & Testing

### US1 — A browser that starts again starts idle (P1)

**Why this priority**: this is the report, and the moment it matters is the start of a service: the
overlay, the projector and the dock must be dark until an operator puts something on air, otherwise
last week's words are painted over this week's stream.

**Independent Test**: put a service on air, then open the overlay, the projector and the dock in a
browser session with no marker but with the stored state left behind; all three are idle, and the
first act that puts words up is the operator's own.

**Acceptance scenarios**

1. **Given** a service on air and every surface closed **When** the browser exits and starts again
   **Then** the overlay paints nothing, the projector paints no screen, and the dock's picker shows
   no "On screen" pill with its control reading "Display this service".
2. **Given** a state left by a previous browser session **When** any surface opens **Then** that
   surface never paints it, not even for a frame.
3. **Given** a clean session **When** the operator presses the dock's display control **Then** the
   service goes on air exactly as it does today and the state is stamped with the new session.

### US2 — Inside one browser session nothing changes (P1)

**Why this priority**: the surfaces must keep their present behaviour while the browser lives — the
operator opens the projector window after the dock, refreshes the overlay, closes every surface and
brings one back, and each of them catches up to what is on air. A containment that broke catch-up
would trade one hazard for a worse one.

**Independent Test**: with the dock and the overlay open and a service on air, open the projector,
reload the dock, close every surface and open the dock again, hide and show, then release; every
surface follows at each step.

**Acceptance scenarios**

1. **Given** a service on air in one surface **When** another surface opens in the same browser
   session **Then** it paints the live screen.
2. **Given** a service on air **When** the dock is reloaded **Then** the overlay never blanks and the
   dock comes back knowing the service is on air.
3. **Given** a service on air and every surface closed **When** a surface is opened again in the same
   session **Then** it still shows the service on air (spec 119, kept by this slice).
4. **Given** a service on air **When** the operator hides, shows, flips the edition, steps screens,
   or releases **Then** every surface follows, and a release leaves every surface idle.

### Edge cases

- **When** the browser was killed rather than closed **Then** the next start is still idle: the
  boundary must not depend on an unload handler running.
- **When** the browser is configured to restore its previous session and restores the cookie with it
  **Then** the display returns as part of that restored session — the browser kept its session; the
  slice does not try to outguess it.
- **When** cookies are unavailable but `localStorage` is (private mode, cookies disabled) **Then** the
  session id lives in page memory: the display works for the life of the page, a reload starts idle,
  and no error reaches the operator. In that configuration the surfaces cannot agree on one id, so
  the page is its own session; this is the recorded cost of a browser that cannot hold a session.
- **When** the stored state is unreadable, corrupt, or has no `session` **Then** it is no state.
- **When** two browsers on one machine run at once **Then** each mints its own id and keeps its own
  state, as today.
- **When** the reading page is reloaded with its service on air **Then** the state it shows follows
  the same rule as the projection surfaces — no third answer.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | The display state SHALL be valid only inside the browser session that wrote it; a state left by an earlier session SHALL be treated as no state by every reader. | `new: display-state` |
| FR-002 | No surface SHALL paint a state from an earlier session, at any point of its load, including the first paint. | `new: display-state` |
| FR-003 | Every write of the display state SHALL stamp the current session, and a write in a session that has no marker SHALL mint one first. | `new: display-state` |
| FR-004 | Within one browser session, catch-up and live updates SHALL be unchanged: a surface that opens or reloads adopts what is on air, and every hide, show, flip, step and release reaches every open surface. Closing every surface SHALL NOT end the display while the session lives. | `new: display-state` |
| FR-005 | The session marker SHALL carry no service, screen, translation or operator identity, and no display state SHALL be sent to the server. | `new: display-state` |
| FR-006 | A browser whose cookie storage is unavailable SHALL keep working from an in-page session id, without an error reaching the operator; a reload then starts idle rather than showing a foreign state. | `new: display-state` |
| FR-007 | Hide and release SHALL keep their present meanings: hide blanks the words and keeps the service and screen; release lets everything go. | `new: display-state` |
| FR-008 | The boundary SHALL be enforced on the state as a property — the stamp it carries against the session's own marker — not on the act that usually produces it: a state written by a reload, a restored tab, or a hand-set value SHALL be judged by its own stamp. | `new: display-state` |
| FR-009 | A state written before this slice (no `session`) SHALL read as no state: the upgrade starts idle, with no migration. | `new: display-state` |
| FR-010 | Two surfaces that mint a marker at the same moment SHALL end up on one id: a mint SHALL take the value the cookie holds after writing, so the state a surface then writes can never carry an id the session has already replaced. | `new: display-state` |

### Key Entities

- **Display state** — `{service, screen, on, translation, at, session}` in
  `localStorage['gkps-display']`: one object per browser, valid only for the session in its `session`
  field.
- **Session marker** — `gkps-session`, a session cookie holding an opaque id. Lifetime is the
  browser session; it is minted by the first display write and read by every surface to judge the
  state.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | After the browser session ends and the browser starts again, the overlay stage has 0 children, the projector has no active screen, and the dock's picker has 0 visible "On screen" pills. | E2E: project, take the stored state without its marker, open each surface, assert all three. |
| SC-002 | No surface paints a prior-session state: the overlay's stage is empty at its first settled frame and the dock's picker shows no pill. | E2E, with the storage injected before navigation. |
| SC-003 | Inside one session, closing every surface and reopening one keeps the display; the existing overlay, projector, dock and reading suites pass unchanged in their intent. | E2E: project, close all pages, open a new page in the same context; plus the existing suites. |
| SC-004 | The marker carries no display data. | Read of the cookie: one opaque value; the stored state's service/screen never appear in it. |
| SC-005 | A state without a matching session reads as `{service: null, screen: 0, on: false}` in every reader. | E2E read through the dock's `gkpsDisplay.read()` and the overlay's painted stage. |

## UI/UX

`n/a — no appearance changes.` Every state this slice produces already exists and is designed: the
dock's picker without an "On screen" pill, its display control reading "Display this service", the
projector's blank stage, and the overlay's empty stage. The slice changes only whether a stored
state is valid when a browser session begins. The gate-1 walkthrough is the live app after a
restart: `runserver` from this worktree at `127.0.0.1:8765`, project a service, close the browser,
reopen it, and the three surfaces are idle.

## Assumptions

- The browser session is the browser process's life, which is what a session cookie measures. OBS
  hosts the dock and the overlay in its own CEF browser and does not persist session cookies by
  default, so an OBS restart is a browser restart for those surfaces.
- The state keeps its present storage key, shape (plus the stamp) and channel; only its lifetime and
  its readers' validation change.
- A freshly started surface looks exactly as it does today with nothing on air; no new empty state is
  designed.
- Two browsers open at once keep separate states; the marker is per browser session, not per machine.
- A state left by an earlier session is not deleted on read — the next write replaces it — so a
  read can never race a write from another surface.

## Clarifications

### Session 2026-11-03

- Q: Which event ends the browser session — the browser closing, or the last surface closing?
  → A: **the browser closing (or OBS closing)**. The service stays on air even if the dock,
  projector and overlay are all closed and one is reopened; it is gone only after the browser
  restarts. The state therefore needs a session marker; today's in-session behaviour (spec 119) is
  kept.
