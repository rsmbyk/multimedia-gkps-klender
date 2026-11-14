# Research: the empty notice leaves the stage

**Spec**: `specs/161-projector-empty-notice/spec.md`
**Unknowns remaining**: 0

## D001 — Where the notice's visibility is decided

- **Decision**: one function, `syncEmptyNotice()`, sets the paragraph's `hidden` attribute from the
  page's two facts — `screens().length` and `detour !== null` — and is called at the end of `render()`
  and `renderDetour()`. `adoptService()`'s own two-line hide becomes a call to it.
- **Rationale**: every state the spec names ends in one of those two functions: `reflow()` and
  `adoptService()` both finish with `render(true)`; `openDetour()` and every step inside a detour end
  in `renderDetour()`; `leaveDetour()` calls `render()`. Writing the rule once from the state, rather
  than patching each path, is what makes the report's case and the re-read case the same fix. Measured
  that the two functions are the only terminal paths: `grep -n "render(" static/web/projector.js`
  lists `leaveDetour`, `reflow`, `render`'s callers in the channel handler and `settle`.
- **Alternatives considered**: (a) hiding it inside `openDetour()` only — fixes the report and leaves
  the re-read defect; (b) a CSS rule keyed on `body.detour-open` — adds a second source of truth for
  a state the script already holds, and would need its own removal on every path; (c) hiding it from
  `renderDetour()` alone — misses `render()`'s re-read path.
- **Provenance**: research — code reading plus live probes on the worktree's dev server.

## D002 — Hiding means out of the layout

- **Decision**: the paragraph carries `hidden` (the UA's `display: none`), not `visibility` or
  `opacity`.
- **Rationale**: it is the stage's next sibling in a flex column, so an invisible-but-present notice
  keeps its 38.4px band and leaves a phantom gap under every projected passage. The product already
  uses `hidden` on its own placeholder glyphs (`projector.css:78`), and the page's `render()` toggles
  `aria-hidden` for screens — one mechanism for "not painted".
- **Alternatives considered**: reserving the band so the words never move — rejected: the band is the
  empty state's own furniture, and keeping it under content reads as a layout error; the words' 23.8px
  move is the honest consequence of the space.
- **Provenance**: research — measured both states on the live page (945.6 → 984 stage height at
  1920×1080).

## D003 — The re-read case is the same rule, not a second fix

- **Decision**: `reflow()` is covered by the helper through its existing `render(true)`; no change to
  `reflow()` beyond that.
- **Rationale**: `reflow()` swaps `#projectorScreens`' children and calls `render(true)`; the notice
  lives outside the swapped box, so its state must be re-derived after the swap — exactly what the
  helper does. Verified by building the case on the live page: adding a `ServiceEntry` to the empty
  service and posting `{type: 'update'}` paints the screen with the notice still below it before the
  fix.
- **Alternatives considered**: re-reading the notice from the reflowed HTML — the paragraph cannot
  appear that way: the server renders it only when the response has no screens, and the re-read
  carries screens. Recorded instead as an out-of-scope limitation (a service emptied while open).
- **Provenance**: research.

## D004 — How the suite proves it

- **Decision**: four E2E cases in `ProjectorE2ETests`, driven through the real page: open the empty
  service, press `g`, choose `Mat 5`, read the notice and the stage; close with `Escape`; and a
  re-read pair driven by another tab's `{type: 'update'}` broadcast, as
  `test_update_finds_a_song_added_after_the_page_loaded` already does.
- **Rationale**: the notice is painted state, not a payload, so the browser is the only honest
  observer; `StaticLiveServerTestCase` plus Playwright is the repo's declared E2E stack. The "leaves"
  case asserts the relationship the spec promises: the notice has no box, and the stage's height
  gains exactly the notice's former height — not a magic pixel value.
- **Alternatives considered**: a unit test of the helper — it would test a DOM assignment through a
  double and prove nothing about the page; the defect existed precisely because the paths were
  untested.
- **Provenance**: research.

## D005 — The released display keeps today's behaviour

- **Decision**: when the display is released while a detour is painted, the notice stays hidden with
  the detour.
- **Rationale**: the notice is decided from the stage's content, not from the display's on/off state;
  tying it to `showing` would paint the empty-service sentence over a released display and would be a
  second, unrequested rule. `body[data-showing="false"]` already hides the detour screen itself.
- **Alternatives considered**: showing the notice whenever `showing` is false — that is a different
  behaviour (the empty state of a stopped display) and the spec does not ask for it.
- **Provenance**: research; recorded as an edge case in the spec.

## Open

<!-- empty: Phase 0 finished with zero unknowns -->
