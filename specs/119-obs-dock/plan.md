# Plan 119: OBS dock — one state for the dock, the projector, and the overlay

- **Status:** Accepted
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-119
- **Bump:** minor

## Why

The owner is revamping the OBS side the same way the public site was revamped: **one
dock and one source** instead of today's per-module OBS pages with different layouts.
For Service Entries this means an operator dock that runs a Tata Ibadah from inside
OBS, a projector page that simply renders what the dock says, and a caption overlay
browser source that renders the same state as subtitles over the video.

Today the projector is one page per service (`/obs/service/<id>/`), opened as a window
by the reading page's Project button; every window carries its own corner controls, a
closing window silently ends the display (beat reaper), and a second Tata Ibadah
"steps aside". None of that survives a fixed-URL OBS browser source operated from a
separate dock.

The approved preview is the interactive mockup (v70) the owner has been reviewing:
picker ⇄ runner through one panel, browse-vs-run, hide vs release, the caption look,
the font choices, and the appearance control.

## Scope / edges

**In:**

- The dock at `/obs/dock`: service picker + runner, transport and keyboard, TB/SIM,
  sticky current/NEXT list behaviour, appearance control, logo header.
- The projector moved to `/projector` (the old `/obs/service/<id>/`, `/lookup/`, and
  `/detour/` routes are dropped without redirects — nothing is in production), with
  `?service=<id>` adoption, in-place service adoption, bundled CMG Sans / Source Sans 3,
  and balanced wrapping on the screen lines.
- The caption overlay at `/obs/source/overlay`: listen-only, state-driven, caption
  typography.
- One browser-local display state shared by all three surfaces (extended `display.js`):
  catch-up on open, safe with every surface closed, safe with many tabs.
- The public/reading service page's Project button: opens `/projector?service=<id>`;
  Stop project becomes a release.

**Out:**

- The legacy per-module OBS pages (`/obs/{bible,songs,tatib,project}/*`) — untouched.
- Any server-side display state; any cross-machine control (state stays within one
  browser, as today).
- New media behaviour; media entries only need to appear in the dock's entry list.
  Overlay output for media screens is a later slice — the overlay is text-only here.
- Other modules' future undocking; this spec covers Service Entries.

## Approach

**One state object, three readers and one writer.** `static/web/display.js` becomes the
shared state module for all surfaces. Storage key `gkps-display` keeps
`{service, screen, on, at}` and gains `translation`; channel `gkps-service-display`
keeps `show` / `update` / `state` and splits today's `stop` into `hide` (blank, keep
place) and `release` (clear the active service). The dock is the writer; the projector
and the overlay render; the reading page's project button writes project/release.

**Drop the liveness reaper and the step-aside.** The current "window closed → stop"
beat logic and the "another service takes the screen over, this window steps aside"
rule both contradict the new contract (closing/opening any surface catches up to the
state; the projector follows any service). The state becomes authoritative, not a
window.

**The projector follows the state.** `/projector` renders `state.service`/`screen`/
`on`/`translation`. When the named service is not its own, it fetches
`/projector?service=<id>`, parses the same data islands its `update` path already reads
(`projectorEntryData`, `projectorScreenData`, `projectorScreens`), swaps in place, and
never navigates. `?service=<id>` on load is an act of projection (idempotent adoption).
The spec-091 corner controls stay (hover-quiet page chrome; OBS never sees them).

**The dock is server-rendered + one fetch per service.** The dock gets its service
list from the view; opening a service fetches `/projector?service=<id>` and reads the
islands — the single data contract the projector and offline shell already use, no new
endpoint.

**Typography ships with the code.** `static/fonts/` gains CMG Sans Bold (free, OFL /
Apache-2.0, bundled with licenses) and Source Sans 3 (OFL variable); `@font-face`
rules live beside their users; `projector.css:29` becomes
`"CMG Sans", "Source Sans 3", sans-serif`; `.screen__line` gains
`text-wrap: balance` (line count unchanged, so fitting is unaffected); the overlay's
caption uses Source Sans 3 with the measured broadcast proportions.

**One appearance control.** A single cycling button (light → dark → system, the public
site's own icons and storage key `gkps-theme`), with a 380 ms colour-morph sweep and a
280 ms icon pop on user switches; reduced motion wins.

## TDD

- Domain/app tests: routes and template contexts (`/projector` with and without
  `?service`, `/obs/dock`, `/obs/source/overlay`, removed `/obs/service/*`), the dock's
  service list, the overlay's state-less first paint, and the projector's data islands
  unchanged for every media kind (existing media suites stay green).
- Browser E2E: a dock class (pick, browse vs project, step, bait, TB/SIM, hide, release,
  keyboard, appearance cycle + persistence), a state class (catch-up with all tabs
  closed, multiple tabs of each surface, service adoption mid-run, release from the
  service page), an overlay class (caption content, blank on hide/release, no controls,
  fonts loaded), and a projector class (adoption without navigation, balance on a long
  line, bundled faces).

## Risks

- **Two writers.** The dock and the reading page's project button both write. The state
  carries `at`; the last write wins and every surface re-renders from storage, so
  divergence heals on the next write.
- **Adoption vs. media.** Fetching another service swaps the whole stage; a live
  image/audio/video/PDF/PPT element must be released exactly as the current reuse path
  does. The spec keeps adoption on the same code path as `update` to inherit the
  existing cleanup.
- **Removing the reaper is a behaviour change.** A closed projector window no longer
  stops the display; the dock (and the service page button) must therefore make the
  display state always visible, which the browse-vs-run model already does.
- **Offline shell routing.** The service worker's projector shell and the saved
  `gkps-display` reads keyed on the old path must move to `/projector`; a missed
  pattern would silently drop offline projector support.
- **Spec 091 links.** The corner's service list and Go To point at
  `/obs/service/<id>/…`; those links move with the route or they 404.
