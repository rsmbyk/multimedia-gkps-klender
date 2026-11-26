# Research: pending state for Search and Media Library rail tiles

**Spec**: `specs/245-rail-fetch-feedback/spec.md`
**Unknowns remaining**: 0

## D001 — Both rail tiles become stage-writing fetches through `navigate()`

- **Decision**: keep `openSearch()` → `navigate(url, {kind: 'results'})` for Search; add a click
  handler on `#railMediaLibrary` calling `navigate(href, {kind: 'media-library', source: tile})`.
  Add `media-library` to `STAGE_KINDS`, `applyPage()`'s `swapsStage` test and its history `pushes`
  list. The anchor keeps its `href`, so a no-script click still loads the page.
- **Rationale**: `navigate()` (`static/web/reading.js:1681`) already owns fetch, lock, bars,
  cancellation, status and settlement. `sectionsFor()` and `writesStage()` at :1493–1497 classify
  by kind; `applyPage()` at :1839 swaps the stage only for kinds in `swapsStage`; :2084 pushes
  history only for listed kinds. A new kind avoids giving Media Library Search's snapshot and
  focus behaviour.
- **Alternatives considered**: reuse `kind: 'results'` — rejected because `fresh.home === 'results'`
  branches (railSearch href, `SEARCH_LAST`, focus handback) would treat a library visit as a search.
  Keep a full document load with a viewport bar — rejected by the owner, who wants the bar on the
  reading page.
- **Provenance**: research — `static/web/reading.js:1493,1681,1839,2084,2288`.

## D002 — Placeholder anatomy comes from the destination's real classes

- **Decision**: extend `placeholderFor(kind, seed)` with three shapes — `results`, `search-home`
  and `media-library` — using the same classes as `reading/search.html` and
  `reading/media_library.html`: `.search-results__intro`, `.result-group__head`, `.result-list`,
  `.result-row__title/__meta/__excerpt`, `.result-more`; `.search-home__inner`,
  `.search-home__logo`, `.search-home__form`, `.search-home__input`, `.search-home__submit`;
  `.media-library__intro`, `.media-library__filters`, `.media-library__chips`,
  `.media-library__file` with icon/main/filename/meta/unused and two action bars; the final shape has no group headings and no seeded file data (owner revision, pass 5).
  Add a scoped CSS override so the shell's home-state gates do not hide those classes inside
  `.stage[aria-busy="true"] > .pv-placeholder`.
- **Rationale**: the accepted spec-243 placeholders in `preview/index.html` already use this
  technique (real `.read` anatomy plus `.pv-ph-bar` bars). The preview's own override proved
  necessary: the shell hides `.search-results`/`.search-home` on the reading home state, so a
  placeholder painted without it measured blank (computed `display: none`).
- **Alternatives considered**: the one-line/two-bar sketch of the first draft — superseded by the
  owner's "match the real layout". A generic spinner — rejected as not layout-matched.
- **Provenance**: research — `static/web/reading.js:1570` (`placeholderFor`),
  `specs/243-navigation-loading-feedback/preview/index.html`, `preview/probe.py`.

## D003 — Search's destination and seed are unchanged

- **Decision**: derive the Search placeholder seed from `lastSearchSnapshot()`'s URL `q=` value;
  with no saved snapshot use the home shape. Do not alter the destination logic of `openSearch()`, `SEARCH_LAST`,
  `saveSearchSnapshot()` or the `/search` response; passing `source: railSearch` is required for the lock.
- **Rationale**: `openSearch()` at :2288 already chooses the last result set or `/`, and
  `lastSearchSnapshot()` at :2274 reads it from `sessionStorage`. The placeholder should describe
  that same destination, not a new one.
- **Alternatives considered**: always seed a result list — wrong when the saved destination is
  home; reading the current input value — wrong when the stage is a different page.
- **Provenance**: research — `static/web/reading.js:2268–2290`; implementation added only the `source` option.

## D004 — Media Library page re-initialises after the in-place swap

- **Decision**: rely on the existing `shell:page` event dispatched at the end of `applyPage()`
  (`reading.js:2112`). `static/web/media-library.js:188` listens for it and its `init()` guard uses
  `data-mediaInitialized` on the incoming `#mediaLibrary` node, so the new page binds its own
  filters, status and companion fetch. No extra dispatch or media JS change.
- **Rationale**: the event is already the repo's contract for scripts that own stage content;
  duplicating it would double-bind the library.
- **Alternatives considered**: rebind from `bindStageExtras()` — rejected because that function
  owns stage click/submit delegation for search results, not the library's own state.
- **Provenance**: research — `static/web/reading.js:2112`, `static/web/media-library.js:3,188`.

## D005 — No server-side interface changes

- **Decision**: `navigate()` sends the same `X-Requested-With: fetch` request the shell already
  uses; the existing `web-media-library` and `web-search`/index views keep rendering the full
  page, which `applyPage()` parses. No view, URL, model, migration or permission changes.
- **Rationale**: the route map (`multimedia/web/urls.py:17,34`) and views already return the page
  shell the stage reconciliation expects.
- **Alternatives considered**: a JSON endpoint returning fragments — larger scope, contradicts
  FR-010 and adds an interface the slice does not need.
- **Provenance**: research — `static/web/reading.js:1751–1766`, `multimedia/web/urls.py`.

## D006 — Targeted E2E cases live with the spec-243 suite

- **Decision**: add new cases to `tests/e2e/test_navigation_pending.py`, reusing its
  `slow_network()` CDP latency helper and `StaticLiveServerTestCase` fixture. A targeted run of the
  named test functions is the in-between evidence; the full browser suite waits for the push step.
- **Rationale**: the existing module already delays fetches and asserts the same lock/bar/
  placeholder state, so the new cases differ only in which rail tile starts the fetch.
- **Alternatives considered**: a new test module — rejected because it would duplicate the
  fixture and the CDP helper for the same behaviour family.
- **Provenance**: research — `tests/e2e/test_navigation_pending.py:1–47`.

## D007 — Direct loads need their own loading line

- **Decision**: set `Loading files…` into `#mediaResultCount` and `Loading files on this computer…` into `#mediaEmpty` at the top of `media-library.js:init()`, before `refresh()`. `render()` replaces both when the single state is applied.
- **Rationale**: the server renders both slots empty; a direct URL or hard reload has no navigation placeholder, so the companion chain otherwise paints a blank gap. Measured before: count text appeared after ~215 ms on a disallowed origin and ~310 ms on the allowed one; after: `Loading files…` paints first, then `10 of 10 files shown`.
- **Alternatives considered**: collapsing the `/status` → `/files` → references → POST `/references` chain — rejected because the single render is deliberate.
- **Provenance**: research — `static/web/media-library.js:178–182`, `multimedia/web/templates/reading/media_library.html:16`.
