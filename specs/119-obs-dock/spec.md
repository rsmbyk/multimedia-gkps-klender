# Spec: OBS dock — one state for the dock, the projector, and the overlay

- **ID:** 119
- **Status:** Accepted (2026-10-20)
- **Item:** ITEM-119
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Preview:** [The interactive mockup (v70)](./preview/dock-preview.html) — approved look, reviewed through v1–v70 during October 2026
- **Bump:** minor

## Intent

An operator runs a Tata Ibadah from inside OBS through one dock, while a fixed-URL
projector page and a caption overlay browser source simply render the same state. The
dock is the only place that picks services and moves screens; the projector and the
overlay never need their URLs changed, never carry controls, and always catch up to
what is on air — including after every surface has been closed.

## Scope

### In scope

- The operator dock at `/obs/dock` (picker + runner).
- The projector page moved from `/obs/service/<id>/` to `/projector`, with
  `?service=<id>` adoption and in-place service switching.
- The caption overlay browser source at `/obs/source/overlay`.
- The shared browser-local display state (extended `static/web/display.js`).
- The public/reading service page's Project / Stop project button.
- Bundled presentation fonts (CMG Sans, Source Sans 3) with licenses, the projector
  stack swap, and `text-wrap: balance` on the projector's screen lines.
- The dock's appearance control and its shared theme storage.

### Out of scope

- The legacy OBS pages `/obs/{bible,songs,tatib,project}/*` (unchanged; the unified
  dock replaces them only for Service Entries in this spec).
- Server-side display state, accounts, or cross-machine control.
- New media behaviour: media entries keep their current preview/projector handling;
  the dock only lists them.
- Overlay output for media screens: the overlay renders text only in this slice; media
  (image, audio, video, PDF, PPTX) shows nothing there until a later slice.
- Reworking the reading pane beyond the project button's behaviour.

## Domain rules

### The display state

- One object per browser in `localStorage['gkps-display']`:
  `{service: number|null, screen: number, on: boolean, translation: 'TB'|'SIM'|null, at: number}`.
  `at` is the write timestamp. `translation: null` means "the entry's own translation".
- One channel per browser: `BroadcastChannel('gkps-service-display')`. Messages:
  - `{type:'show', service, screen}` — an entry screen is on air.
  - `{type:'hide'}` — words off; service and screen stay.
  - `{type:'release'}` — no active service.
  - `{type:'flip', translation}` — TB/SIM changed.
  - `{type:'update'}` — re-read what is on air.
  - `{type:'state'}` — a reader's request to be brought up to date; writers answer with
    `show`/`hide`/`release` as appropriate.
- Writers: the dock (all verbs) and the service page's project button (project/release).
  Readers: the projector, the overlay, and every other tab. Readers never write.
- **Catch-up is mandatory.** Every surface reads the stored state at load and renders
  it; channel and `storage` events keep it live. State survives every surface closing —
  the display ends only by `release` (or `hide` blanking it), never by a window closing.
  Any number of tabs of any surface is safe.

### The two stop verbs

- **Hide** — reversible pause. `on: false`, service/screen kept. The projector and the
  overlay go blank; the dock's display control shows off; showing again resumes in place.
- **Release** — let go. `service: null`, `screen: 0`, `on: false`, `translation: null`.
  Every surface goes idle, the dock has nothing active, and the service page's button
  reads Project again. Release is what the service page's **Stop project** does; the
  dock's display control only ever hides.

### Browse versus run (the dock)

- The dock holds a **cursor** (the service and screen being browsed) and nothing else.
  Opening a service never writes the state.
- Projection acts: clicking an entry row, an inner screen row, or the NEXT band makes
  the run take that service at that screen; the display control pressed while off makes
  the run take the browsed service at its first screen (or resume, when the browsed
  service is the live one and hidden).
- The display control reads ON (filled, "Hide words") only when the browsed service is
  the live service and `on` is true. Otherwise it reads OFF ("Show words" when the live
  service is hidden; "Display this service" when the browsed service is not on air).
- Moving screens, baits, entries, and the TB/SIM flip act on the run only while the
  browsed service is the run. Browsing another service shows no current marker.

### The projector page (`/projector`)

- Renders the state, nothing else: the active service's screen at `state.screen`, blank
  when `on` is false, idle (blank) when `release`d.
- `?service=<id>`: an act of projection. On load, adopt that service at its first screen
  (`show`) — idempotent when it is already the live service. Adoption replaces the
  active service for the whole browser; every other surface follows.
- Service changes are adopted **in place**: no navigation. The page fetches
  `/projector?service=<id>` and swaps the same data islands its `update` path already
  parses (`#projectorEntryData`, `#projectorScreenData`, `#projectorScreens`); media
  elements are released exactly as the existing reuse path does.
- The screen area carries no controls. The spec-091 corner controls (cue, service-entry
  list, Go To) remain as hover-quiet page chrome; their links move under `/projector`
  (`/projector/lookup/`, `/projector/detour/`, and `/projector?service=<id>` for the
  service list).
- Routes: `/projector`, `/projector/lookup/`, `/projector/detour/`. The old
  `/obs/service/<id>/` routes (and their `lookup/` and `detour/`) are **removed without
  redirects** — nothing is published to production yet.

### The overlay (`/obs/source/overlay`)

- A listen-only browser source: no controls, no inputs, no header, transparent
  background. It renders the current screen's text lines as captions; a blank screen,
  `hide`, `release`, or any non-text screen shows no caption.
- Media screens (image, audio, video, PDF, PPTX) render **no caption at all** in this
  slice — media on the overlay is a later slice. Only text-bearing screens reach the
  caption.
- The caption shows the screen's lines, not the reference header. The TB/SIM choice in
  the state is worn (the same lines the projector shows).

### The service page button

- The reading/public service page's project button keeps its two labels
  (`Project` / `Stop projecting`, `data-label-*`) and its icon. Project opens
  `/projector?service=<id>` in the `gkps-projector` window and writes `show`; Stop
  project writes and posts `release`.
- The button is ON when this page's service is the live service and `on` is true.

### Typography

- CMG Sans Bold (free, Church Motion Graphics; OFL/Apache-2.0) and Source Sans 3
  (OFL variable) are bundled under `static/fonts/` with both license texts, loaded via
  `@font-face`.
- The projector stack becomes `"CMG Sans", "Source Sans 3", sans-serif` (CMG at 700,
  Source Sans 3 as its stand-in).
- `.screen__line` gains `text-wrap: balance` so a single authored line that wraps splits
  into near-equal rows. Balance never changes the line count, so the fitting is
  unaffected. `.screen__head` stays as it is.
- The overlay caption uses Source Sans 3 at weight 800.

## UI details

The interactive preview ([preview/dock-preview.html](./preview/dock-preview.html), v70)
is the visual reference for the dock and the overlay; its width and preview panes are
demonstration devices. The dock is designed for a ~400 px OBS dock and stays usable
from 320 px to 560 px without horizontal scrolling.

### Dock — header

- Padding 13 px top, 14 px sides, 12 px bottom; hairline bottom border.
- GKPS mark: 34 × 34 px circular tile (the app's `.rail__logo` treatment: white
  background, 4 px padding, `object-fit: contain`, the repo's `static/assets/gkps.png`).
- Title "Tata Ibadah": 14.5 px / 650.
- Right cluster, 8 px gap: reload (38 px) and appearance (38 px) icon buttons, 1 px
  border, 9 px radius, no fill; hover lifts the icon to full ink.
- No instructional text anywhere in the picker.

### Dock — appearance control

- One button that cycles light → dark → system; the icon, `title`, and `aria-label`
  always state the mode it is in ("Appearance: Dark").
- Icons: the public site's own (sun, moon, monitor; 24 px viewBox, stroke 1.7) — the
  same shapes as `base.html`'s rail theme button.
- Storage `gkps-theme` (shared with the public site); default dark; `system` follows
  `prefers-color-scheme` live.
- On a user switch: a 380 ms colour cross-fade sweep (temporary `html.theme-morph`;
  nothing transitions at rest) and a 280 ms icon pop (scale .4 / −40° → none, ease-out,
  no bounce). Reduced motion skips both. Loading a surface never morphs.

### Dock — picker

- Services grouped by month; 4 px between service rows; the existing Tata Ibadah data
  (name, date); today's row wears the current-entry tint, later rows the inner-row
  tint (as today's calendar highlighting does).
- A tap opens the service in the runner. It never projects.

### Dock — runner

- Head: service name (13 px / 650) over its date (11.5 px, muted); switch-service and
  display-state buttons 38 px on the right.
- Display-state button: filled with the active fill while words are up; muted (75 %
  opacity glyph, no fill) while hidden. `aria-pressed="true"` means hidden.
- Entry list rows: one per service entry, label + right-aligned meta; 4 px between
  entries; kind-appropriate labels (song "NKB 43", passage "Filipi 4:4-9", text title,
  section break "Section break"), numbered like today's list.
- Inner detail: one row per projector screen, flush with the row label (no indent);
  song screens grouped under small uppercase "Bait N" heads; rests as quiet italic
  "Rest" rows; 3 px between inner rows. Only the entry holding the current screen is
  expanded; opening a service starts collapsed.
- Sticky: the current entry's row pins flush at the list top (radius 0 while stuck);
  a "NEXT — <label>" band pins at the bottom while the current entry runs past the
  fold. The current row dissolves passing rows above it only while genuinely stuck.
- Navigation recenters the current row vertically on every move (190 ms ease-out,
  clamped at the ends). Crossing an entry boundary — and the first expansion of a
  service — is one ~230 ms motion: the old inner collapses, the new one grows, and the
  view eases to centre together. No bounce.
- Bait strip: 32 px chips, the current chip centred with the same 190 ms glide, the
  strip scrolls with per-side fades only while overflowing.
- Footer: TB/SIM marker (leftmost; filled when the shown translation differs from the
  entry's own), then the previous/next 40 px chevrons, filled while the window holds
  focus and quiet otherwise.

### Dock — keyboard and focus

- Keys act only in the runner view: arrows/PgUp/PgDn step screens; ⇧ steps baits;
  Ctrl steps entries; Home/End are the unit edges with the same modifier grammar;
  Space hides/shows; T flips TB/SIM; Ctrl/⌘+PgUp/PgDn stay the browser's.
- Nothing on the page takes focus; every control carries `tabindex="-1"` and a pointer
  press hands focus back to the panel, so no focus ring ever appears and the keys never
  dead-end after a click.

### Projector

- The existing dark canvas, safe insets, fitting, and media rendering are unchanged.
- Screen lines: `text-wrap: balance`, weight 700, line-height 1.37, the bundled faces
  above. The head keeps its current treatment.

### Overlay caption

- Container: absolute, left/right 6 %, bottom 6 %, centred, white.
- Type: 800, `clamp(9px, 2.9cqw, 32px)`, line-height 1.4, letter-spacing .01em,
  Source Sans 3.
- Outline: an em-based 4-direction 0.06 em black outline at 0.045 em diagonals plus a
  soft 0.12 em shadow at 45 % black — it scales with the font.
- `text-wrap: balance` on the caption; the screen's lines render as separate blocks.
- Blank/hidden/idle: nothing at all (transparent frame).

## Acceptance scenarios

### Run a service from the dock

- **Given** the dock is open at `/obs/dock` and nothing is on air
- **When** the operator taps a service
- **Then** the runner opens at that service, collapsed, and the projector and overlay
  stay blank.
- **When** the operator taps one of its entry rows
- **Then** the projector and the overlay render that screen, and every other surface
  (including a second tab) shows the same state.

### Step, bait, entry, flip, hide

- **Given** a song is on air from the dock
- **When** the operator steps with arrows, ⇧, Ctrl, Home/End, or the buttons
- **Then** the screens follow one step of that kind at a time and the list recenters.
- **When** T is pressed
- **Then** the projector and the overlay show the other translation of the same screen
  and the TB/SIM marker fills when it differs from the entry's own.
- **When** Space (or the display button) is pressed
- **Then** both screens go blank and nothing else changes; pressing again resumes in
  place.

### Browse versus run

- **Given** service A is on air
- **When** the operator opens service B
- **Then** nothing changes on air, the display button reads "Display this service",
  and B's list shows no current marker.
- **When** the operator presses the display button
- **Then** B takes over at its first screen; A's tabs follow to B.

### Adoption and catch-up

- **Given** every surface is closed and a service was left on air
- **When** `/projector` (no parameter) opens
- **Then** it renders the stored state.
- **Given** a projector is showing service A in OBS
- **When** someone opens `/projector?service=B`
- **Then** that window, the OBS projector, the overlay, and the dock all show B at its
  first screen — without the projector navigating.
- **Given** six tabs across the three surfaces exist
- **When** the dock releases or the state changes
- **Then** every tab agrees; closing tabs never changes the state.

### Hide and release

- **Given** a service is on air
- **When** its service page's button (now reading "Stop projecting") is pressed
- **Then** the state is released: projector and overlay blank, the dock shows nothing
  active, and the page's button reads "Project".
- **When** the dock's display button is used instead
- **Then** that is a hide, not a release — the service stays active and showing resumes
  in place.

### Overlay source

- **Given** the overlay is an OBS browser source at `/obs/source/overlay`
- **When** a text screen is on air
- **Then** it renders the caption lines with the specified typography, no reference
  header, no chrome, and no focusable elements.
- **When** the screen is blank, hidden, released, or a media screen
- **Then** the overlay shows nothing — media entries are deliberately not displayed in
  the overlay in this slice.

### Fonts and wrapping

- **Given** the fonts are bundled
- **When** the projector renders a long single line that wraps
- **Then** the rows are balanced (near-equal) and the block's height is unchanged from
  the greedy wrap — the fitting still fits.
- **When** CMG Sans is missing on the machine
- **Then** the projector falls back to the bundled Source Sans 3, not a system font.

### Unchanged surfaces

- **Given** any media entry (image, audio, video, PDF, PPTX) in a service
- **When** it is projected from the dock or the corner controls
- **Then** its current behaviour and looks are unchanged.
- **Given** the legacy OBS pages
- **When** they are opened
- **Then** they behave exactly as before.

## Traceability

- Domain/app tests: `multimedia/web/test_obs_dock.py` (routes, adoption parameter,
  picker grouping in Indonesian, dated services only, bundled typefaces and the balance
  rule), `multimedia/web/tests.py` (`ServiceProjectorTests`), `multimedia/web/test_media.py`
  (media islands unchanged).
- Browser E2E: `tests/e2e/test_obs_dock.py` (browse vs run, entry click, keyboard units,
  hide/resume, catch-up with every tab closed, `?service` adoption in an open projector),
  `tests/e2e/test_obs_overlay.py` (caption words and type, control-free page, hide empties).
- Implementation: `multimedia/urls.py`, `multimedia/web/reading/views.py`,
  `multimedia/web/templates/reading/{projector,obs_dock,obs_overlay}.html`,
  `static/web/{display,projector,obs-dock,obs-overlay}.js`,
  `static/styles/design/{fonts,projector,obs-overlay,obs-dock}.css`,
  `static/assets/fonts/` (+ licences), `static/assets/gkps.png`.

## Owner review points

- The spec-091 corner controls stay on `/projector` (hover-quiet page chrome; the screen
  itself stays control-free) — confirm, or say they should go.
- Old `/obs/service/*` routes disappear outright (no redirects).
- Media entries appear in the dock list with their normal labels; the dock adds no
  media-specific UI beyond that.
- A closed projector window no longer ends the display (the beat reaper goes); only
  Stop project (release) does.
- The dock shares the public site's `gkps-theme` storage key for the appearance mode.
