# Research: focus only the empty search landing

**Spec**: `specs/220-initial-search-focus/spec.md` (Accepted, Gate 1 2026-11-22)
**Measured against**: the served shell at `http://127.0.0.1:63404/` (develop), Chromium, 1440×900 and 390×844.

## Unknowns remaining: 0

## D001 — Focus is applied by the shell, on load and on in-page arrival

**Decision**: `static/web/reading.js` gains one predicate, `onLanding()`, and one
`focusLandingSearch()`. The latter is called at init (bottom IIFE block, after `syncState()`) and at
the end of `applyPage()` after the stage swap, so both entry paths converge.

**Rationale**: the public site is one page. `/` arrives as a full document load, but every rail
destination, the home logo and the Search rail arrive through `applyPage()` after a `fetch`. An
`autofocus` attribute or a template script would cover only the first path.

**Alternatives rejected**: (a) `autofocus` on `#searchQuery` — fires once per document, never on the
in-page path, and a second `autofocus` after a swap does nothing; (b) an inline script in
`reading/base.html` — the shell owns stage state, and a template script would re-run against a stage
the shell replaces.

**Provenance**: `static/web/reading.js` init block (`applyTheme`, `syncState`, … line 2129) and
`applyPage()` (`syncState()` at line 1813); measured on develop.

## D002 — Focus never scrolls the page

**Decision**: `focus({preventScroll: true})`, the same call the shell already uses for
`bootFocusTarget` and the drawer rows.

**Rationale**: `reading/R15` holds the landing to exactly one window tall with no scrollbar, and the
field is already centred, so any scroll caused by focus would be a regression. Measured: `scrollY` 0
and `scrollHeight == innerHeight` at 1440×900, 720×900, 390×844 and 320×568 before and after focus.

**Alternatives rejected**: relying on the browser not to scroll — Chrome scrolls a focused element
into view when it is partly outside the scrollport, which is reachable at 320×568 with an open
on-screen keyboard.

**Provenance**: `reading.js` lines 1795, 808, 1022 (existing `preventScroll` uses); preview probe.

## D003 — Focus is keyed on the landing being painted, not on the route

**Decision**: `onLanding()` is `root.dataset.home === 'landing' && root.dataset.read !== 'on'`.

**Rationale**: measured on develop, `/bible/`, `/songs/` and `/tatib/` are the same landing as `/` —
`data-home="landing"`, `data-read="off"`, `#searchHome` visible with its field at top 422 — and only
`data-section` on the root differs, which drives the sidebar. Reading routes are
`data-home="reading"`, `data-read="on"`, `#searchHome` at `display: none`.

**Alternatives rejected**: an allow-list of the five paths — it duplicates a decision the server
already made, and the next index route added would silently lose focus.

**Provenance**: measured `#searchHome.outerHTML` on all five routes: 1299 bytes,
`sha1 c19937db7f2f73c709c84e95fffd3bf0229a81e7` on every one; `data-section` values `alkitab`,
`alkitab`, `alkitab`, `kidung`, `tatib`.

## D004 — The blur on submit is explicit, because the input survives the swap

**Decision**: `applyPage()` captures `previousHome` before it touches the stage, and at the end blurs
`#searchQuery` only when `previousHome === 'landing'` and the arriving state is `results` and the field
is the active element.

**Rationale**: measured on develop — focus the landing field, submit `garam`: after the results render,
`document.activeElement === #searchQuery` and the node is the *same* node (`sameNode: true`,
`reconcileChildren` reused it). Nothing removes the focus, so the requirement needs an explicit blur.

**Alternatives rejected**: (a) rely on the stage swap replacing the input — it does not; the same
`#globalSearch` form serves both states, which is why the compact bar looks unchanged; (b) blur on
every arrival at results — that would change a re-submit typed into the compact bar, which the spec
does not ask for.

**Provenance**: probe on develop: landing `activeElement` BODY → submit → results
`activeElement` `searchQuery`, `sameNode: true`; direct `/search/?q=garam` load `activeElement` BODY.

## D005 — No CSS and no template change

**Decision**: the focus ring is the product's existing `:focus-visible` treatment; this slice adds no
rule, token or class.

**Rationale**: measured on the live page, the field with `:focus-visible` paints
`outline: rgb(28, 92, 60) solid 2px` with the existing 2px offset. Programmatic focus on load does
paint it — `q.matches(':focus-visible')` was true immediately after the call, because no pointer
interaction had happened.

**Alternatives rejected**: an explicit `:focus` ring — it would repaint on pointer focus too, changing
states the spec keeps unchanged.

**Provenance**: probe on the served page; preview probe (`focusVisible: true`, `outline 2px`).

## D006 — Five E2E tests, one per success criterion

**Decision**: `tests/e2e/test_reading.py` gains five tests: landing focus on `/` and the four other
landing routes, the Search-rail in-place arrival, results never auto-focused, submit moves focus out,
and reading routes untouched.

**Rationale**: the repository's user-visible acceptance runs on Playwright against a live server
(`StaticLiveServerTestCase`), and every claim in the spec is an observable browser fact
(`document.activeElement`, `scrollY`, typed text). A unit test would have to mock the DOM the shell
builds at runtime.

**Alternatives rejected**: asserting the source text of `reading.js` — it would pass on a call that
never runs.

**Provenance**: `tests/e2e/test_reading.py` (2574 lines, `ReadingE2ETests`), existing
`page.evaluate("document.activeElement...")` assertions at lines 765-783, 1672, 1687.

## D007 — Bump: `patch`

**Decision**: `bump: patch` under the repository's semver scheme.

**Rationale**: a user-visible behaviour change with no API, route or data change, and no compatibility
question; `VERSION` moves `1.36.4 → 1.36.5` at delivery.

**Alternatives rejected**: `none` — the change is observable in the product, not a refactor.

**Provenance**: `VERSION` `1.36.4` on develop; `CHANGELOG.md` `## [Unreleased]`.