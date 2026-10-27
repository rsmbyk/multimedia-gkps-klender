# Feature Specification: A closed projector window can be reopened at the screen that is on air

**Slice**: `specs/141-projector-window-reopen`
**Branch**: `feat/141-projector-window-reopen`
**Created**: 2026-10-27
**Status**: Accepted (owner, gate 1, 2026-10-27)
**Input**: "when you close the projector window, you cant reopen it without stop projecting in service page"

## What the page does today

The reading page's project button has two acts (spec 119). While this service is on air it is
**Stop projecting** and a click releases the display (`static/web/display.js`, the click handler:
`release()`); otherwise it is **Project** and a click opens `/projector?service=<id>` in the
`gkps-projector` window and writes `show(service, 0)`.

Closing that window deliberately does not end the display — spec 119 removed the beat reaper, so the
state survives every surface going away. What is missing is the way back: with the window closed and
the service still on air, the only control on the page releases the display, and the next **Project**
starts the service over at its first screen. An operator who closes the window on screen 12 has no
control that brings it back on screen 12.

The bare `/projector` page already renders the stored state at the stored screen (spec 119: "a service
left on air, every surface closed, `/projector` renders it"). This slice gives the reading page the
control that opens exactly that page while the service is live.

## User Scenarios & Testing

### US1 — The window can be reopened without releasing the display (P1)

**Why this priority**: this is the report. Closing the window while a service runs is an ordinary act
— the window is moved, closed by mistake, or the browser restarts — and today the only route back
releases the service and restarts it at screen 0, so a mid-service place is lost and the overlay and
dock go idle in between.

**Independent Test**: start a service, step it to a screen of its own (screen 4), close the projector
window, and press the new control on the service page: the window returns showing screen 4, the page
still reads Stop projecting, and the stored state is untouched.

**Acceptance scenarios**

1. **Given** this browser has the page's service on air and no projector window open, **When** the
   service page draws, **Then** the project group shows a second control immediately before Stop
   projecting, 34×34 px, named "Open projector window".
2. **Given** the state is at screen 4 and the projector window is closed, **When** the control is
   pressed, **Then** the `gkps-projector` window opens on `/projector` (no `?service`) and shows
   screen 4 — not screen 0 — and the display state is unchanged.
3. **Given** the projector window is already open, **When** the control is pressed, **Then** that
   window comes forward without loading the projector page again: the screen it shows, the state and
   any media playing in it are untouched.
4. **Given** the state is released, or hidden, or names another service, **When** the page draws,
   **Then** the control is not drawn and Project (or Stop projecting) is the only projection control,
   as today.
5. **Given** another tab of this browser starts this service, **When** this tab hears the change,
   **Then** this tab draws the control too — the group's displaying state is shared, not local.

### US2 — The control fits the pane at every desktop width (P2)

**Why this priority**: the group sits in the reading pane, and the pane is narrow exactly where the
sidebars push (240 px at a 1280 window). A third control that spills past the pane would be a new
defect traded for the old one.

**Independent Test**: draw the page at 1440×900 and 1280×800, with and without a Media files button;
the group's right edge stays inside the pane and the header's height is the one measured below.

**Acceptance scenarios**

1. **Given** a 1440×900 window with no media on the service, **When** the service is on air, **Then**
   the header stays one row (34 px) and the group measures 181.7 px inside a 400 px pane.
2. **Given** a 1440×900 window with Media files, **When** the service is on air, **Then** the header
   keeps the 69 px it has today and the group measures 280.4 px inside the pane.
3. **Given** a 1280×800 window with Media files, **When** the service is on air, **Then** the group
   wraps inside the 240 px pane as [Media files][control] over [Stop projecting], the header grows
   from 69 px to 111 px, and no part of the group crosses the pane's right edge.
4. **Given** a 425×900 window, **When** the service is on air, **Then** neither the Project control
   nor the new control is drawn (spec 138/R14).

### Edge Cases

- **When** the browser blocks the window (no user gesture, a policy) **Then** nothing opens and the
  state is unchanged — the control never falls back to releasing.
- **When** the projector page is open as an ordinary tab rather than the named window **Then** the
  control still opens the named window; both surfaces follow the same state.
- **When** the control is pressed twice quickly, the second press landing while the new window is
  still blank **Then** the same window is brought forward; a second window is never opened.
- **When** the display is hidden (`on: false`) **Then** the page reads Project, the control is not
  drawn, and Project starts the service at its first screen — spec 119's rule, unchanged.
- **When** the service has no items **Then** the reopened window shows the projector's own empty
  state.
- **When** the page is a deep link, or reached through the shell's in-place navigation, **Then** the
  control is equally present: the group's displaying state is re-synced on `shell:page` as today.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | While this page's Tata Ibadah is the browser's live service and the display is on, the project group SHALL draw a second control immediately before Stop projecting; in every other state the control SHALL NOT be drawn. | `new: reading` |
| FR-002 | Activating it SHALL open `/projector` in the browser's `gkps-projector` window at the screen that is on air, never at the service's first screen, and SHALL NOT write the display state. | `new: reading` |
| FR-003 | When that window is already open, activating it SHALL bring the window forward without loading the projector page again. | `new: reading` |
| FR-004 | The control SHALL NOT end or pause projection: Stop projecting keeps releasing (spec 119), and closing the projector window keeps leaving the state untouched. | `new: reading` |
| FR-005 | The control SHALL be a 34×34 px icon-only button whose accessible name and tooltip read "Open projector window"; it SHALL be drawn on the desktop widths the Project control is drawn on, and never at the phone width. | `reading/R14` |
| FR-006 | When the pane is narrower than the group, the group SHALL wrap inside the pane rather than cross its right edge, at every width from 721 px up. | `new: reading` |

### Key Entities

- **Display state** — the browser-local `gkps-display` object (service, screen, on, translation, at)
  defined by spec 119. Read, never written, by this control.
- **Projector window** — the named `gkps-projector` popup. Its page is `/projector`, which renders
  the stored state; a `?service=<id>` URL is an act of adoption (spec 119) and is deliberately not
  used here.
- **Project group** — `.read__project` inside the reading page's head, the only group carrying
  `data-project-group`, right-aligned beside the date.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | Reopening returns to the on-air screen | set the state to screen 4, close the window, press the control: the projector's active screen index is 4 |
| SC-002 | Reopening changes no state | `gkps-display` is identical before and after the press, `at` included |
| SC-003 | An open window is not reloaded | a token written on the projector's window object before the press is still there after it, and the window has focus |
| SC-004 | The control wears the group's treatment | 34×34 box, 15×15 glyph, 9 px radius, hover `#1F1F1D`/`#1C5C3C`/`rgba(31,31,29,.08)`, dark `#F5F3EE`/`#7C9CF0`/`rgba(255,255,255,.09)`, focus-visible 2 px `#1C5C3C` at 2 px offset |
| SC-005 | No spill at any desktop width | group right edge ≤ pane right edge at 1440×900 and 1280×800, with and without Media files |
| SC-006 | The phone is unchanged | at 425×900 the control and the Project control both measure 0×0 |

## UI/UX

Measured on the preview (`preview/preview.html`) in headless Chromium against the real
`tokens.css` and `components.css`, at the stage column's real widths.

- **Layout / position**: the last-but-one button in `.read__project` — after Media files when the
  service has media, immediately before Stop projecting; right-aligned with the group, 8 px gap.
  Measured group widths while on air: **181.7 px** without media and **280.4 px** with it.
- **Size / spacing**: **34 × 34 px**, no padding, **15 × 15 px** glyph at stroke **1.6**, radius
  **9 px**, border **1 px** `--divider` (`#D9D6CD` light, `#3A362F` dark), no fill.
- **Colour / typography**: glyph `--head-ink` (`#646357` light, `#9C9A91` dark). No text on the
  face; the words live in `aria-label` and `title` ("Open projector window"). Hover: glyph `--ink`
  (`#1F1F1D` / `#F5F3EE`), border `--focus` (`#1C5C3C` / `#7C9CF0`), fill `--icon-hover-bg`
  (`rgba(31,31,29,.08)` / `rgba(255,255,255,.09)`). Focus-visible: the group's existing 2 px
  `--focus` outline at 2 px offset. No disabled state exists in this group.
- **States**: off air, released, hidden, or another service live → **not drawn**; on air → drawn;
  hover, focus-visible and active as above; nothing else changes on the other two controls.
- **Motion**: none added. The control appears and disappears with the state, like the Project /
  Stop projecting label swap; its colour transition is the group's existing `--ease` (200 ms).
- **Responsive**: never drawn at ≤720 px (the Project control's own rule, extended); drawn from
  721 px. At 1440×900 the header stays **34 px** without media and **69 px** with it — the heights it
  has today. At 1280×800 the header is **69 px** without media, unchanged, and grows **69 → 111 px**
  with media because the group wraps inside the 240 px pane; group spill goes **+40.4 px → 0**. The
  phone frame (425×900, pane 389 px) draws only the Media files button.
- **Unchanged by design**: the Project and Stop projecting buttons keep their labels, icons and
  primary/danger treatments (spec 018); the Media files button keeps its place at the group's start.

## Assumptions

- **"On air" means `on === true`.** A hidden display is not on air; the page reads Project and the new
  control is not drawn (today's rule).
- **Icon-only, because of the width budget.** The pane is 240 px at a 1280 window, where the live
  group with Media files already measures 238.4 px; a worded control would spill in that case by more
  than 100 px. The accessible name carries the words.
- **The window is the existing named popup.** No new route, no tab type, no second window name.
- **Reopening writes nothing.** It is a reader act; the state, the overlay and the dock are untouched.
- **The dock is out of scope.** Its display control stays hide/show; release stays the service page's
  Stop projecting (spec 119).
- **Only the service page carries the control**, because only it carries the project group.
- **The phone breakpoint stays at 720 px** where spec 138 put it, and the wrap rule is scoped to the
  Tata Ibadah group so other reading pages are untouched.
- **The popup keeps its 1280×800 default size**, as today.

## Clarifications

### Session 2026-10-27

- Q: While a service is on air, how should the closed projector window be reopened? → A: **a second
  control appears beside Stop projecting while this service is on air; it opens the projector window
  at the screen that is currently on air, and focuses the window if it is already open** (owner,
  2026-10-27).
