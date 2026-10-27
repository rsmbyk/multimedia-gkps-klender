# Research: reopening the projector window

**Slice**: `specs/141-projector-window-reopen`
**Spec**: `spec.md` (Accepted, gate 1, 2026-10-27)

## D1 — The control is a third button in the existing group, and `display.js` owns the click

**Decision**: the markup joins `.read__project` in `multimedia/web/templates/reading/tatib.html`
(the group that already carries `data-project-group`); the visibility rule is CSS on the group's
existing `data-displaying`; the click is one more branch in `static/web/display.js`'s delegated
listener, beside the Project / Stop projecting branch.

**Rationale**: that file is the display state's writer and already resolves the group's nodes from
the document on every use, because the shell swaps the reading pane in place (its header comment
records the dead-handler bug that came from holding nodes). A new script would re-derive the same
state and the same guards.

**Alternatives**: a second script file — rejected, two readers of one state and a second
`shell:page` hook; an inline `onclick` in the template — rejected, it cannot see `state` and would
duplicate the guard.

**Provenance**: `static/web/display.js:142-191` (nodes, `syncButton`, the delegated handler);
`specs/119-obs-dock/spec.md` §"The service page button"; spec 137's note on the `shell:page` hook.

## D2 — Reopening opens `/projector` with no `?service`

**Decision**: the control opens `/projector` bare. That page follows the stored state — service and
screen — and paints the screen that is on air.

**Rationale**: `?service=<id>` is an act of adoption: `projector.js` writes `show(service, 0)` for it,
even when the service is already live (`service_projector` renders `adopt_service` only from the
query string, and the page's load path calls `write({service, screen: 0, on: true})`). Reopening with
it would silently restart the service at its first screen — the exact defect this slice removes.

**Alternatives**: `?service=<id>&screen=<n>` — rejected: a URL contract the projector does not read,
and it would need a new write path; asking the projector to adopt without writing — rejected: the
adoption path is spec 119's and is not this slice's to change.

**Provenance**: `static/web/projector.js:1437-1470` (the load path: `adoptId` → write, otherwise
follow `stored`), `multimedia/web/reading/views.py:1321-1351`; spec 119 §"The projector page", and
its scenario "every surface is closed … `/projector` renders the stored state".

## D3 — An open window is focused, not navigated

**Decision**: `window.open('', 'gkps-projector', 'width=1280,height=800')`; if the returned window is
on `about:blank` (a fresh popup) set its location to `/projector`, otherwise only `focus()`. Reads of
`win.location` are wrapped: a named window the operator pointed elsewhere is left alone.

**Rationale**: `window.open('<url>', 'gkps-projector')` navigates a live window, which reloads the
projector page — a flash, media restarted, and any adopted detour lost. An empty URL reuses the named
window without navigating it; a fresh one is ours to fill.

**Alternatives**: holding the `window.open` reference only — rejected: it is lost when the reading
page itself reloads or the operator arrives through the shell's in-place navigation, and the fallback
then reloads a live projector; a `focus` message on the display channel — rejected: the projector
would need a new command and a listener, for one act.

**Provenance**: `static/web/display.js:186-188` (the named window today), the projector's
`pagehide` cleanup of media (`projector.js`, the last lines) which a reload would trigger.

## D4 — Icon-only, 34 × 34

**Decision**: an icon-only control (the group's "pop out" glyph), with the words in `aria-label` and
`title`.

**Rationale, measured** (preview, real `components.css`, at a 13 px/600 label): the live group with
Media files measures 238.4 px in the 240 px pane of a 1280 window; the 400 px pane of a 1440 window is
the common case. A worded control measures **118 px** ("Open projector") or **80.2 px**
("Projector"); with Stop projecting (139.7) and the 8 px gap the group becomes **265.7 px** or
**227.9 px**, and even the shorter word pushes the 1440 header's own row to two lines
(227.9 + 12 + 171.3 = 411.2 px against 400) — the height the common case has today is lost. The icon
adds **42 px**, keeping the group at 181.7 px without media (one 34 px row) and 280.4 px with it.

**Alternatives**: a worded button — rejected on those numbers; an icon inside the Stop button —
rejected, one control cannot carry two acts; hiding Media files at narrow widths — rejected, a second
behaviour change the spec does not ask for.

**Provenance**: `preview/preview.html` measured in headless Chromium; `components.css:837-866` (the
group's own type and box), `2676-2683` (the Tata Ibadah padding).

## D5 — Visibility comes from CSS on `data-displaying`

**Decision**: `.read__project-btn[data-project-window]` is `display: none` by default and drawn by
`.read__project[data-displaying="true"] …` — the attribute `display.js`'s `syncButton` already keeps
for the label swap.

**Rationale**: one source of truth for "is this service on air"; the rule survives a DOM swapped in
place, and it needs no second JS branch to show or hide.

**Alternatives**: toggling the `hidden` attribute in JS — rejected: a second place that must agree
with `syncButton`, and a stale node would keep the wrong state.

**Provenance**: `display.js:159-172` (`syncButton` writes `data-displaying`), `components.css:851-866`
(colour rules keyed on the same attribute).

## D6 — The phone rule is a `min-width: 721px` gate

**Decision**: the show rule lives inside `@media (min-width: 721px)`; the existing `≤720 px` block
needs no new selector.

**Rationale**: the hide rule at `components.css:2900` is a bare `[data-project-open]` (0,1,0); a new
hide rule for this control would lose to the show rule's (0,3,0) and would need `!important`. Gating
the show rule means it never applies on a phone, and the control's default `display: none` stands.

**Alternatives**: `!important` in the phone block — rejected, the file has none for layout and this
would be the first; hiding the whole group — rejected, Media files is drawn on a phone today.

**Provenance**: `components.css:2896-2900`; spec 138/R14; E2E
`tests/e2e/test_drawer_shell.py::test_the_project_control_is_hidden_on_a_phone`.

## D7 — The group wraps inside the pane

**Decision**: `.read[data-kind="tatib"] .read__project` keeps `flex-wrap: wrap` and gains
`max-width: 100%` at ≥721 px, instead of the `nowrap` it declares at `components.css:2676`.

**Rationale**: measured at the 1280 window, the live group with Media files becomes 280.4 px in a
240 px pane — a **40.4 px spill** past the pane's right edge. `flex: none` sizes the group to its
content, so wrapping needs the width cap as well as `wrap`. With both, the group becomes
`[Media files][icon]` over `[Stop projecting]` and the header is 111 px.

**Alternatives**: accept the spill — rejected, it paints over the stage's padding; reorder the
buttons so the icon and Stop share the first line — rejected, Media files would move to the end of
the group while live.

**Provenance**: preview measurement; `components.css:2676-2683`.

## D8 — Verification is six browser tests

**Decision**: extend `tests/e2e/test_projector.py` (`ProjectorE2ETests`) with six Playwright tests;
no JS unit tests, because the repo declares user-visible acceptance as Playwright E2E and has no JS
runner.

**Rationale**: the behaviour is browser state and window management — the only honest harness is a
real browser with two pages in one context.

**Alternatives**: a unit test of the handler with jsdom — rejected, no runner and no jsdom in the
repo; a server test — rejected, nothing reaches the server.

**Provenance**: `tests/e2e/test_projector.py:1-60` (runner, static-files override, contexts docs),
`docs/PROCESS.md` TDD repo block.

## Unknowns remaining: 0
