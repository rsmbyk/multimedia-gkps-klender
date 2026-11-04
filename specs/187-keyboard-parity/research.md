# Research: one keyboard grammar for the dock and the projector

**Spec**: `specs/187-keyboard-parity/spec.md`
**Unknowns remaining**: 0

## D001 — The band keeps the keyboard, keyed on the band

- **Decision**: `openFind()` focuses the field; a `window` `focus` listener and a
  `document` `visibilitychange` → `visible` listener re-focus it while `find.open`; the panel's
  `pointerdown` park and the outside-`focusin` park choose the field while the band is open and the
  panel otherwise; the field is only focused when it is enabled, and the existing
  `projector-library:ready` handler covers the case where the index arrives after the band opens.
- **Rationale**: measured on the living dock — `G` leaves `document.activeElement` on `#dockPanel`
  and typing reaches `<body>`; the field is `disabled` until the index arrives, so `openFind`'s
  synchronous `focus()` is a no-op on first open; the window regaining focus has no listener at all
  (`window.addEventListener('focus', markFocus)` only toggles a class). OBS's CEF does not reliably
  restore the field's focus after the window loses it, so the dock must ask for it.
- **Alternatives considered**: routing the next keystroke into the field on the first `keydown`
  (loses the caret and breaks IME composition); re-focusing on `visibilitychange` only (misses a
  window that keeps visibility but loses focus, e.g. clicking the projector); a persistent hidden
  input (worse focus semantics, and the field already exists).
- **Provenance**: research — code read and measured on `/obs/dock` at 63404.

## D002 — Go To stepping is the library's own move, not a copy

- **Decision**: the dock calls `window.GKPSProjectorLibrary.movePassage(detour, action, level)` and
  `fetchChapter(...)` exactly as the projector's `requestPassage` does, then writes the result through
  `gkpsDisplay.stepGoto()` / `goTo()`.
- **Rationale**: the library is already loaded on the dock for the band's lookup (`ensureLibrary`),
  already owns the chapter and book neighbours, and already fetches a chapter with the right edition.
  The projector's `requestPassage` is twenty lines around those two calls
  (`projector.js:1418-1435`).
- **Alternatives considered**: a dock-local chapter map built from the index (duplicates the
  neighbour logic and drifts from the library); having the projector compute the step (couples two
  windows over the channel, and the dock can be open alone).
- **Provenance**: research — `static/web/projector-library.js` and `projector.js`.

## D003 — Plain `Home`/`End` mirrors `unitBoundary` in the dock

- **Decision**: the dock's `edgeOf`/`stepUnit` implement the projector's plain, `Shift` and
  `Ctrl`/`⌘` rules against its own model (`dock.entries`, `dock.stops`, the cached go to payload's
  `baits`); no shared module is extracted in this slice.
- **Rationale**: the two scripts are separate closures with different screen models — the dock knows
  `stops` and `entries`, the projector knows `screens` and `entries` — and the FR pins the arithmetic
  to `unitBoundary` so agreement is testable (SC-004, SC-010) without a refactor the slice does not
  need.
- **Alternatives considered**: extracting `unitBoundary` into `projector-library.js` (a change to the
  projector's tested core beyond this slice's ask); routing the dock's keys through the projector's
  page (impossible across windows).
- **Provenance**: research.

## D004 — The in-flight guard is a dock-local `gotoBusy`

- **Decision**: `gotoBusy` is raised when the dock's goto payload fetch or a chapter/book step begins
  and lowered when it paints or fails; while it is raised every dock key and every pointer act that
  would change what is on air is refused, and the block's header reads `Loading…`.
- **Rationale**: the projector has exactly this flag (`projector.js:1177-1198`) and the dock has none;
  a step during a fetch would write a position into a payload that has not arrived.
- **Alternatives considered**: disabling the transport controls (a visual change beyond the ask, and
  the guard must cover keys anyway); queueing the input (surprising, and the fetch may fail).
- **Provenance**: research — `projector.js` `gotoBusy`, `beginGotoLoad`.

## D005 — A go to may stand with no service

- **Decision**: `display.js`'s `gotoOf()` accepts a goto when `service === null`; `goTo()` writes
  `{service: null, screen: 0, on: true, translation: null, goto}`; `stepGoto`, `hide`, `resume` and
  `flip` act on it; `back()` writes `{service: null, screen: 0, on: false, goto: null}`; `show()`
  ends it; the session stamp applies as it does to any write.
- **Rationale**: the owner's ruling — a go to chosen on the picker stands alone. `service: null` is
  already the state's idle marker, and a non-null goto beside it is the one thing the state needs to
  say "this is on air".
- **Alternatives considered**: adopting a service under the picker's go to (the owner rejected it);
  a second storage key for a service-less goto (breaks one-state, one-channel).
- **Provenance**: owner decision, recorded in the spec's `Input` and US2.

## D006 — The dock's sheet is a static panel inside the dock, toggled by `K`

- **Decision**: the five groups live in `obs_dock.html` as one `<section class="keysheet">` inside
  `#dockPanel`, with `data-keys="pick"` on the picker group and every control `tabindex="-1"`; `K`
  toggles `is-on`; `Esc`, the close control and a click on the 8 px frame close it; the picker group's
  `hidden` follows `data-view`.
- **Rationale**: no route and no round trip; the dock's table, until now a comment
  (`obs-dock.js:14-25`), becomes inspectable markup, and the E2E can read its rows. Every control
  staying `tabindex="-1"` keeps the keyboard on the panel, which the dock's shortcuts depend on.
- **Alternatives considered**: building the sheet in JS from a table (harder to inspect, and the
  labels would drift from the template); a separate sheet page (breaks the single-panel dock).
- **Provenance**: research.

## D007 — The projector's sheet changes are template plus one height rule

- **Decision**: `projector_controls.html` merges Display + Find + Fullscreen into `Display`, renames
  *While Finding* to `Find` and orders it Prev · Next · Open · Close When Empty · Close, merges Audio
  and Video into one group and moves it and Image and PDF into the first `.stack`; `.sheet`
  (`projector.css:488`) stops holding a fixed height and follows its tallest column — 835.5 px at
  1080p, measured on the living page — with its existing `overflow: auto` covering 720p.
- **Rationale**: the sheet's box is already content-driven (676.5 px at 1080p today, its tallest
  column plus the head); the media move makes the left column the tallest one, and the owner asked for
  the move. The measured 835.5 px fits 1080p with its frame; at 720p the sheet scrolls instead of
  clipping.
- **Alternatives considered**: keeping 677 px and letting the sixth group fall below the fold
  (contradicts the no-clip rule); equal-height columns with an internal scroll (worse than one scroll
  on the sheet); shrinking the rows or headings (changes the type scale the owner approved).
- **Provenance**: owner decision plus measurement — `projector-sheet/before.png` / `after.png`.

## D008 — The dock's sheet keycaps copy the projector's design, not its stylesheet

- **Decision**: the cap rules stay the projector's design at the dock's scale — `--u` 22 px, word /
  `bk` / `ww` caps 2 u, the space bar 3 u with the `␣` mark at 14 px and `scaleX(1.3)`, the dark
  palette `#2A2722` / `#4A463F` — written into the dock's own stylesheet; `projector.css` is not
  loaded on the dock page.
- **Rationale**: the dock page carries `tokens.css` and `obs-dock.css`; loading `projector.css` would
  bring the projector's whole sheet layout and collide with the dock's classes. The measured cap is
  44 × 22 with an 11 × 11 glyph, which is the projector's cap at the dock's `--u`.
- **Alternatives considered**: loading `projector.css` for the sheet (collides, and drags the display
  surface's rules in); reproducing the projector's sheet markup wholesale (a three-column sheet cannot
  fit a 384 px dock).
- **Provenance**: research — measured in the preview.

## D009 — `⌘` parity on the projector is one guard

- **Decision**: the projector's keydown stops returning on `metaKey`; `ctrl = event.ctrlKey ||
  event.metaKey` gates the arrow and `Home`/`End` chords only; any other `⌘` chord returns before an
  action fires.
- **Rationale**: the projector's own sheet already draws `⌘` for the entry chords, and the code
  returns on meta before any of them (`projector.js:1629`); the dock has treated the two as one
  modifier since it shipped.
- **Alternatives considered**: treating `⌘` as an alias everywhere (`⌘+T` would flip the edition and
  take a browser shortcut); fixing only the sheet's symbol (a lie).
- **Provenance**: research.

## D010 — Verification through the repo's own E2E harness

- **Decision**: two new modules, `tests/e2e/test_dock_keys.py` and
  `tests/e2e/test_projector_keys.py`, plus extensions to `test_dock_goto.py`,
  `test_goto_shared_state.py`, `test_obs_dock.py` and `test_projector.py`; the preview's `probe.py`
  stays the static check of the sheet.
- **Rationale**: every behaviour in the spec is browser state and DOM — focus, keys, localStorage,
  the channel — which is exactly what `StaticLiveServerTestCase` + Playwright covers here; the repo has
  no JS unit harness and this slice does not need one.
- **Alternatives considered**: Jest/jsdom (a new toolchain for behaviour the E2E already reaches);
  manual checks only (unverifiable, and the process forbids an un-verifiable requirement).
- **Provenance**: research — `tests/e2e/` conventions.

## D011 — The picker narrows to `↑` / `↓`, and the band keeps its keys

- **Decision**: on the picker only `↑`/`↓` move the mark, `Enter` opens the service, `G` opens the
  band; `←`, `→`, `PgUp`, `PgDn`, `Home`, `End` do nothing there. The band's own field keeps the keys
  it has (arrows, `Enter`, `Esc`, `Backspace` on empty).
- **Rationale**: the owner asked for the narrower set; the band is a text field, so its arrows are
  text navigation, not dock navigation.
- **Alternatives considered**: keeping the four arrows and the page keys (the owner's ask is the
  opposite); narrowing the band too (would break typing).
- **Provenance**: owner decision.

## Open

<!-- empty when Phase 0 is finished; anything here blocks Phase 1 -->
