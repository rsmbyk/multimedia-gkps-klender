# Feature Specification: the dock centres its live entry only when asked

**Slice**: `specs/200-dock-centre-triggers`
**Branch**: `feat/200-dock-centre-triggers`
**Created**: 2026-11-18
**Status**: Draft
**Input**: the owner's request, 2026-11-18 — *"i want to remove that auto-center behavior, and,
instead, add a button in between the previous and next to do that."* Revised in the same session to
*"maybe not actually removing it. i want to add some conditions for the behavior to trigger"*, with
the triggers named:

- the newly introduced button to center the live-entry
- clicking on the items inside the entries
- after being idle (no mouse activities, no modals open) for 15 seconds, no other entry headers
  open, the live-entry item is currently completely off the screen, the display state is currently
  on, and the service is currently being opened in the dock.

Revised again in the same session: that condition's *"no mouse activities"* means **scrolls and
clicks only** — a press held down (a drag) included — and never plain pointer movement.

## What the runner does today

Every display-state notice reaches `sync()` (`static/web/obs-dock.js`). With a service live and no
crossing morph it calls `scheduleCenter()` (`:1317`), which on the next frame runs `centerRow()` on
the live row — the current screen row, or the entry's label row when the screen has no row of its
own (`liveNode()`, `:612`). The target puts the row's centre on the scrollport's centre
(`:603–607`), reached by a 190 ms ease-out glide clamped to the list's real ends (`glideScroll()`,
`:560`), instant under `prefers-reduced-motion`. When the live **entry** changes, `startMorph()`
(`:640`) animates both inner block heights by hand over 230 ms and derives `scrollTop` from the
arriving row's live layout position on the same curve, so expand, collapse and scroll are one
motion; `finishMorph()` re-centres when it lands (`:707`). A wheel or pointerdown on the list
cancels any pending centring or glide (`cancelPendingCenter`, `:774–782`).

So today the list re-parks the live row on **every** state notice — a screen step, an entry step,
a display toggle, a go to, a saved-change re-read (R13), a session refresh, a load.

This slice keeps the centring mechanism and gives the dock **two modes**:

- **Following** — the normal state, inherited from today. Every advance of the service — forward or
  backward, within an entry or across one — keeps the live row centred, so the screen follows the
  service as it runs. This holds even with other entries open and even with the words hidden; the
  one condition is that the dock is showing the service that is actually on the projector and
  overlay. A follow-mode advance runs the existing 230 ms crossing morph when the entry changes.
- **Browsing (not following)** — entered the moment the operator **scrolls the list** or **expands
  another entry**. In this state the list stays where the operator put it: advancing changes what
  is on air but does not move the list.

Three things put the dock back into following: pressing the new centre button, clicking an item
inside an entry — which includes the sticky **Next** band at the foot of the live entry — and a
successful 15 s idle re-centre. The transport's **Next** and **Back** buttons are ordinary advances:
they centre when following and leave the list alone when browsing, but never change the mode.
Follow mode is a mode, not a per-event flag: after a re-entry, the *next* advance follows again
without another press.

## User Scenarios & Testing

### US1 — A control in the transport centres the live entry (P1)

**Why this priority**: the owner is replacing an automatic behaviour with an explicit one. Without
this control the other two triggers leave the operator no way to ask for the centring on demand.

**Independent Test**: open a service with the display on, scroll the list so the live entry is out
of view, press the new control between Previous and Next — the list glides until the live row's
centre is on the scrollport's centre.

**Acceptance scenarios**

1. **Given** a service on air and the runner showing **When** the transport is looked at **Then**
   one new control sits between Previous and Next, in that row, with the same 40 px height and
   the same `navbtn` face as the two arrows.
2. **Given** the live row is off the middle **When** the control is pressed **Then** the list
   glides the live row to the scrollport's centre over 190 ms and nothing else changes — no
   display write, no selection change.
3. **Given** `prefers-reduced-motion: reduce` **When** the control is pressed **Then** the list
   jumps to the target with no glide.
4. **Given** nothing is on air from this dock (no live row) **When** the control is looked at
   **Then** it is disabled and pressing it does nothing.
5. **Given** a go to is on air **When** the control is pressed **Then** it centres the go to's
   live row, the same as a service's (`dock.stops`-style target: the marked row of the block).
6. **Given** the dock is browsing — the operator has scrolled or opened another entry, so advances
   no longer centre **When** the control is pressed **Then** the dock is following again, and the
   **next** advance centres without another press.
7. **Given** the dock is following **When** the control is looked at **Then** it is filled in
   `--active-bg`/`--active-ink` with `aria-pressed="true"`; after a scroll or an expanded entry puts
   the dock in browsing mode **Then** the same control shows the plain `navbtn` outline with
   `aria-pressed="false"`.

### US2 — Clicking an item inside an entry centres the live row (P1)

**Why this priority**: the item is the dock's only projection path from the list (spec 198 R14),
and the owner keeps centring on it: the row the operator just asked for is the one they should be
looking at.

**Independent Test**: expand an entry, click one of its screen rows — the list centres the row
that just went on air.

**Acceptance scenarios**

1. **Given** a screen row inside an open block **When** it is clicked **Then** that screen goes on
   air (unchanged) and the list centres the live row it produced.
2. **Given** a screen row in the **same** entry as the live one **When** it is clicked **Then**
   the live entry is unchanged and the list glides the new live screen row to the middle.
3. **Given** a screen row in a **different** entry **When** it is clicked **Then** the live entry
   changes and the crossing runs as one motion, the arriving row ending centred.
4. **Given** the sticky Next band of the live entry **When** it is clicked **Then** its screen goes
   on air — the **next entry becomes the live entry**, its first row carries the live mark, that row
   is centred, and the dock is following again, as an item click does.
5. **Given** an entry's header **When** it is clicked **Then** only its block toggles — no
   projection and no centring (spec 198 R14 stands); because this opens *another* entry, the dock
   also leaves following mode.
6. **Given** the dock is browsing **When** an item inside an entry is clicked **Then** the dock is
   following again from that click onward — and the sticky **Next** band is such an item, so
   clicking it re-enters following.

### US3 — The idle return brings a lost live entry back (P2)

**Why this priority**: it is the owner's stated courtesy case — an operator who has scrolled away
and then stopped touching anything should find the live entry again without asking, but only when
nothing else on the dock is competing for attention.

**Independent Test**: with the display on and the dock showing that service, scroll the live entry
completely out of view and stop touching the dock; after 15 s the list brings the live row back to
the middle.

**Acceptance scenarios**

1. **Given** the runner showing the service that is on air, the display on, no layer open, no
   other entry's block open, and the live row entirely outside the scrollport **When** 15 s pass
   with no scroll, press, held press or key **Then** the list glides the live row to the middle.
2. **Given** the same state but an entry header was opened by hand **When** the 15 s pass **Then**
   nothing moves, and the timer keeps running.
3. **Given** the same state but a layer is open (the find band or the shortcut sheet) **When** the
   15 s pass **Then** nothing moves.
4. **Given** the same state but the words are hidden, or a go to is on air **When** the 15 s pass
   **Then** nothing moves.
5. **Given** the same state but the live row is at least partly on screen **When** the 15 s pass
   **Then** nothing moves.
6. **Given** the same state but the picker is the view, or the browsed service is not the one on air
   **When** the 15 s pass **Then** nothing moves.
7. **Given** the timer is part-way through **When** the wheel turns, a button is pressed or
   released, or a key is pressed **Then** the count restarts from 0.
8. **Given** the timer is part-way through with the live row out of view **When** the pointer is
   moved across the dock without pressing anything **Then** the count does **not** restart and the
   elapse still centres the list.
9. **Given** a button is held down — a press that has not been released, a drag on the list
   included **When** the 15 s pass with it still held **Then** the count is suspended and nothing
   moves until the release.
10. **Given** the page is hidden **When** the timer elapses **Then** nothing moves (the page is not
    being looked at), and the count restarts when the page is shown again.
11. **Given** the dock is browsing **When** the idle elapse centres the live row **Then** the dock
    is following again, and the next advance centres without another press.

### US4 — Advancing follows in following mode, and not while browsing (P1)

**Why this priority**: this is the behaviour the owner is protecting. A service left alone keeps its
live entry in view the way it does today, even when nobody presses the new control; the moment the
operator takes the list over by scrolling or opening an entry, advancing stops fighting them.

**Independent Test**: leave a service running and press Next a few times — the live row stays
centred. Scroll away and press Next or Back — the list stays where it was. Press the centre button
or click the sticky **Next** band — it follows again.

**Acceptance scenarios**

1. **Given** the dock is following and the service it shows is the one on air **When** the service
   advances with the arrow buttons, the keys, `PgUp`/`PgDn`, `Home`/`End`, a bait chip or
   `Ctrl`/`⌘` + arrow **Then** the live row is centred on each step, and a step that crosses into
   another entry runs the 230 ms crossing morph.
2. **Given** that state but other entries are open by hand, or the words are hidden **When** the
   service advances **Then** the list still follows the live row — neither condition breaks
   following.
3. **Given** the dock is browsing after a scroll **When** the service advances by any path,
   including the transport's Next and Back buttons **Then** the live row changes but the list does
   not move, and the mode stays browsing.
4. **Given** the dock is browsing after the operator expanded another entry **When** the service
   advances **Then** the list does not move.
5. **Given** the dock is browsing **When** the operator clicks the sticky **Next** band **Then** the
   dock is following again and that projection centres, because the band is an item inside the
   live entry.
6. **Given** the dock is following but it is not showing the service on air — the picker is the
   view, a different service is open, or a go to has taken the screens **When** the service advances
   **Then** nothing centres.
7. **Given** any mode **When** the display is switched on or off, a saved change is re-read (R13),
   the dock reloads onto what is on air (R11), a service is opened, the runner is entered from the
   picker, or a go to's own row is stepped **Then** the list does not move and no glide is scheduled.
8. **Given** the dock is following **When** the operator scrolls the list or expands another entry
   **Then** the dock leaves following mode, and that scroll or expansion itself does not centre.

### Edge Cases

- **When** the live row has no row of its own (a blank-only entry) **Then** the fallback label row
  is the target, as today.
- **When** the live entry changes because of an item click **Then** the crossing motion is the one
  that carries the arriving row to the middle; the idle timer's own glide never runs on top of it.
- **When** the operator presses the centre control while a crossing is in flight **Then** the
  crossing is left to finish; the control is a glide, not a second motion.
- **When** the list is already centred **Then** pressing the control is a no-op (no visible move).
- **When** the live row is less than half a scrollport from the top or bottom **Then** the centring
  clamps at the list's end and the row lands where the geometry allows, as today.
- **When** the operator's pointer rests still over the dock, or moves across it, unsigned **Then**
  that is idle: only a scroll, a press (a click, or a press held down) or a key restarts the count.
- **When** a press is held through the whole 15 s — a drag on the list **Then** the count is
  suspended while it is held and restarts from the release.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | The runner's transport SHALL render exactly one new control, placed between Previous and Next in the same row, carrying the same `navbtn` height and face as those two. | `dock` (R15 new) |
| FR-002 | Pressing the control SHALL centre the live row (the current screen row, or the entry's label row when the screen has no row of its own) on the scrollport's centre: a 190 ms ease-out glide, clamped to the list's ends, and an instant jump under `prefers-reduced-motion: reduce`. It SHALL write no display state and change no selection, and SHALL put the dock into following mode. The control SHALL carry `aria-pressed="true"` with the filled `--active-bg`/`--active-ink` face while following, and `aria-pressed="false"` with the plain `navbtn` outline while browsing. | `dock` (R15 new) |
| FR-003 | The control SHALL be disabled while the dock has no live row (nothing on air from this dock, or the picker is the view). | `dock` (R15 new) |
| FR-004 | Clicking a screen row inside an entry's block, or the live entry's Next band, SHALL centre the live row that results from that projection — a glide when the live entry is unchanged, the crossing motion when it changed — and SHALL put the dock into following mode. The Next band's screen belongs to the **next** entry: clicking it SHALL move the live pointer to that entry and mark its first row. | `dock` (R15 new) |
| FR-005 | An entry header's click SHALL NOT centre the list (spec 198 R14's "no scroll" holds). Opening another entry's block by hand SHALL put the dock into browsing mode. | `dock` (R14 unaffected, R15 new) |
| FR-006 | **Following mode:** when the service advances — forward or backward, within an entry or across one, by the arrow buttons, the keys, `PgUp`/`PgDn`, `Home`/`End`, a bait chip or `Ctrl`/`⌘` + arrow — the dock SHALL centre the live row on each step, using the crossing morph when the entry changes. This SHALL hold with other entries open and with the words hidden. **Browsing mode:** the same advances SHALL change what is on air but SHALL NOT move the list. The transport's **Next** and **Back** buttons SHALL NOT change the mode in either state. | `dock` (R15 new) |
| FR-007 | The dock SHALL run a 15 s idle timer, restarted by a **scroll** (the wheel), a **press** (a pointerdown, a click, or a press held down — a drag included) or a **key** press in the dock, and **NOT** by plain pointer movement. When it elapses it SHALL centre the live row **only if every one** of these holds: the runner is the view; the browsed service is the service on air; the display is on and no go to is on air; no layer is open (the find band, the shortcut sheet); no entry's block is open except the live entry's; and the live row's box lies entirely outside the scrollport. A successful idle centring SHALL put the dock into following mode. | `dock` (R15 new) |
| FR-008 | When the idle timer elapses and any condition in FR-007 fails, the list SHALL NOT move and the timer SHALL keep running; the conditions SHALL be read at the moment it fires, not when it was armed. | `dock` (R15 new) |
| FR-009 | The idle timer SHALL not fire while the page is hidden, and SHALL restart its count when the page becomes visible again. | `dock` (R15 new) |
| FR-010 | A centring in flight SHALL remain cancellable by the operator's own hand: a wheel or pointerdown on the list SHALL still cancel a pending centring or glide, and the idle timer SHALL NOT fight it. | `dock` (unchanged, R14/119) |
| FR-011 | The dock SHALL begin in following mode (the behaviour it has today). | `dock` (R15 new) |
| FR-012 | A scroll of the list, or the expansion of another entry's block by hand, SHALL put the dock into browsing mode; neither act SHALL centre the list itself. Browsing mode SHALL last until one of FR-002, FR-004 (which includes the sticky Next band) or FR-007's successful elapse. | `dock` (R15 new) |
| FR-013 | Following SHALL apply only while the runner is showing the service that is on air on the projector and overlay. With the picker as the view, a different service open, or a go to on air, no advance SHALL centre. | `dock` (R15 new) |
| FR-014 | In either mode the following SHALL NOT centre the list: a display switch, a saved-change re-read, a session refresh, a load, opening a service, entering the runner from the picker, a go to's own rows, and a layer closing. | `dock` (R15 new) |

### Key Entities

- **Live row** — the current screen row (`.screenerow[aria-current="true"]`) or, when the screen has
  none, the live entry's label row (`.entryrow[aria-current="true"]`); the centring target.
- **Following mode** — the dock's normal state: advances centre the live row. It is entered by the
  control, an item click (including the sticky Next band), a successful idle elapse, and initially
  on load; it is left by a scroll or by opening another entry's block. The transport's Next and
  Back buttons are advances only and never change the mode. It applies only while the dock shows
  the service on air.
- **Trigger** — the control, an item click (including the sticky Next band), the idle elapse that
  satisfies FR-007, and an advance while following. All but a plain advance also (re)enter
  following.
- **Idle clock** — the 15 s count, restarted by a scroll, a press (a click, or a press held down —
  a drag included) or a key press; plain pointer movement never restarts it, and a press still held
  suspends it.
- **Layer** — the find band (`#findBand` + `#findScrim`) and the shortcut sheet (`#keysheet`); either
  open suppresses the idle centring.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | The named triggers centre the live row on the scrollport's centre, within 1 px of the target, after the move settles; the Next band also moves the live mark to the next entry's first row. | Live probe: press the control / click an item / let 15 s pass / advance while following, then read the live row's centre against the scrollport's centre; click the Next band and read the live `data-index` before and after. |
| SC-002 | In browsing mode no advance moves the list. | Live probe: scroll the live row out of view or open another entry, then step with keys, buttons and chips; `scrollTop` reads the same before and after each. |
| SC-003 | The idle centring happens only with all of FR-007's conditions true, and never with any one of them false. | Live probe: set each condition false in turn and let the 15 s pass; `scrollTop` reads the same each time; with all true it moves. |
| SC-004 | A centring always reads as one motion (no bounce, no second phase). | Frame sampling of `scrollTop` per move; no direction reversal before the settle. |
| SC-005 | Under `prefers-reduced-motion: reduce` every centring is an instant jump with no glide. | Live probe with the media emulated. |
| SC-006 | The clock's own events are exactly scrolls, presses and keys: a moving pointer leaves it counting, and a press held down suspends it. | Live probe: move the pointer through a whole interval and watch it still centre; hold a button and watch nothing move until the release; a wheel turn and a click each restart the count. |
| SC-007 | Following ends only on a scroll or another entry's expansion; it returns on the control, an item click (including the sticky Next band) or a successful idle elapse. The transport's Next and Back buttons never change the mode. | Live probe: advance three times (centres each time); scroll, press Next and Back (no move, still browsing); click the sticky Next band (centres, following again); expand another entry, press Next (no move); let the idle elapse fire, advance (centres). |

## UI/UX

`static preview at specs/200-dock-centre-triggers/preview/index.html` — the runner's transport and
list assembled from the real template's markup, class names and `styles/design/obs-dock.css`
(inlined by `preview/build.py`, so the page cannot drift from the stylesheet silently). Measured in
a 420 × 780 px pane by `preview/probe.py`:

- **Layout / position**: the control is the middle child of `.navpair` — `#prevBtn` at x 287,
  `#centreBtn` at x 337, `#nextBtn` at x 387, all on the same line at y 747;
- **Size / spacing**: 40 × 40 px, `border-radius` 10px, `.navpair` gap 10px — identical to the two
  arrows; the glyph is a 17 × 17 px box inside it;
- **Colour / typography**: `navbtn` face — 1px `--divider` border (rgb(58, 54, 47) at rest in dark),
  `currentColor` ink, stroke-width 1.8, round caps; no text;
- **States**: at rest · hover (`--focus` border + `--icon-hover-bg`) · the window-focus fill
  (`html.win-focus .navbtn:not(:disabled)`) · disabled at `opacity: .45` with no live row;
  **following** — crosshair filled `--active-bg` (#7C9CF0 in dark, #1C5C3C in light) with
  `--active-ink`, `aria-pressed="true"`; **browsing** — transparent face, `--divider` border,
  `aria-pressed="false"`.
- **Motion**: the control only starts the list's own 190 ms quadratic ease-out glide — measured on
  the live dock at 60 fps: per-frame steps `63, 56, 51, 45, 40, 33, 28, 23, 16, 11, 5, 1` px
  (first third 215 px, last third 33 px), 0 direction reversals, landing 0.0 px off the scrollport's
  centre;
- **Responsive**: `flex: none`, so it takes its width from `.baits`, which already shrinks; the
  fixture's pane is 623 px tall over 1715 px of list.

## Assumptions

- The control is an icon button like its two neighbours, not a text pill — the transport row is
  icon-only today and a labelled control would change its rhythm. Its `title`/`aria-label` name the
  act.
- "clicking on the items inside the entries" means a screen row inside an open block, and the live
  entry's Next band (both project from the list). An entry header never centres. Go to rows and the
  transport's bait chips are not "items inside an entry", so they do not centre.
- 15 s is measured from the last **scroll, press or key** in the dock: a wheel turn, a pointerdown,
  a click, or a press held down — a drag on the list included — and a key press. Plain pointer
  **movement** is not activity, so a pointer travelling across the dock is idle. Keys still count:
  the owner narrowed "mouse activities", and the dock's own navigation is keyboard-driven.
- "no modals open" means the dock's own layers: the find band and the shortcut sheet (the picker is
  a view, not a layer, and is excluded by "the service is currently being opened in the dock").
- "no other entry headers open" means no block is open except the live entry's — a block the
  operator opened by hand suppresses the idle centring.
- "the display state is currently on" means the words are up (`on: true`) with no go to on air.
- The idle centring is a glide, not a morph: it moves the list only, and never expands a block.
- The dock starts in **following** mode, as it does today. A go to on air suspends following because
  the projector and overlay are showing the go to, not the service; the dock's service is not "the
  one currently on overlay and projector".
- "was auto-centered" (the third re-entry the owner named) is read as the successful 15 s idle
  elapse, not as a passive state: after the idle centring the dock follows again.
- The owner's "next panel" is the sticky **Next** band at the foot of the live entry — already an
  item click and therefore a re-entry, and it also jumps the live pointer to the next entry (FR-004).
  "Pointer" means the live-entry marker (`data-live` / the row's `aria-current`), not the picker's
  marked row. The earlier reading (the transport's Next control) was
  corrected the same day and is kept as a retraction in Clarifications. The transport's **Next** and
  **Back** buttons are plain advances: they keep whatever mode is current.
- The display being off does **not** break following — the owner explicitly named open entries and
  a dark display as conditions that an advance ignores. A scroll or opening another entry is what
  ends following.
- The control's glyph is a stroked crosshair, drawn to `navbtn`'s own metrics (viewBox 20 × 20,
  stroke 1.8); the product ships no centring glyph, and a text label would break the row's rhythm.
- No `[NEEDS CLARIFICATION]` marker remains: every question the slice raised is recorded below.

## Clarifications

### Session 2026-11-18

- Q: Which condition should gate the dock's auto-centre? → SKIPPED (the owner chose to write the
  triggers himself), and answered instead by the three bullets quoted under **Input**.
- Q: When a crossing is caused by something **outside** the three triggers — a keyboard or button
  step into the next entry — does the list still travel with the blocks' expand/collapse morph?
  → SKIPPED, assumed the list stays put — **superseded later the same day** by the owner's follow-mode
  decision below: while following, an advance across an entry *does* centre (FR-006); while
  browsing it does not. The assumption is kept here as a retraction, not silently rewritten.
- Q: Does advancing still follow the live entry when the service is left alone? → **Yes**, the owner
  confirmed: in a normal, undisturbed service the screen follows the live entry as it does today;
  the named actions are ways to *return* to that state after a deviation, not the only times
  the list may move; pressing Next is one of those returns.
- Q: What ends following? → **"scrolling and expanding another entries exits the following mode"**
  (owner, 2026-11-18). An advance does not end it, and neither an open block nor a dark display
  blocks an advance while following.
- Q: What returns the dock to following? → the three the owner named: the centre button, an item
  click, and "was auto-centered" — the last read as the successful idle elapse (Assumptions).
- Q: Which control is "the next panel"? → first timed out, assumed the transport's Next control —
  **superseded by the owner's correction**: *"no, i mean the sticky next band. the 'Next' (and
  'Back') navigation buttons keeps whatever the current following mode."* So the sticky band is the
  re-entry (it already is, as an item click) and the transport buttons never change the mode. The
  wrong reading is kept here as a retraction, not silently rewritten.
