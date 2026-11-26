# Tasks: pending state for Search and Media Library rail tiles

**Spec**: `specs/245-rail-fetch-feedback/spec.md`
**Plan**: `specs/245-rail-fetch-feedback/plan.md`
**Verification split**: 16 test · 11 inspection · 0 manual

`[P]` means order-independent, not concurrent; one thread runs them in the order written.
Every new `test` row has a red and a green task. Inspection rows produce no test task. The static
preview was built before gate 1; no application code has been changed yet.

## Phase 1 — Setup

- [X] T001 Extend `tests/e2e/test_navigation_pending.py` with helpers that open `/` at
      1440×900, click a named rail tile under `slow_network()` latency, and return the tile,
      stage, bar and placeholder locators. No assertions yet; no production code touched.

## Phase 2 — Foundational

- [X] T002 Register `media-library` as a stage-writing kind in `static/web/reading.js`:
      `STAGE_KINDS`, `applyPage()`'s `swapsStage` test and the history `pushes` list; add the
      `#railMediaLibrary` click handler that calls `navigate(href, {kind:'media-library',
      source: tile})` while keeping the anchor's `href`. This makes FR-001 reachable.

## Phase 3 — US1 (P1) 🎯 MVP

**Goal**: a slow Search or Media Library rail click locks the tile, bars the reading stage and
shows the destination's real layout before the page arrives.
**Independent test**: delay the fetch, click Search, read the lock, bar and result-group anatomy.

- [X] T003 [P] [US1] Red test for FR-002 / US1-AC1 in `test_navigation_pending.py`:
      `test_search_rail_locks_the_tile` — SVG opacity `0.45`, `aria-disabled="true"`, no spinner
      or label added. Confirm it fails on the unmodified base.
- [X] T004 [P] [US1] Red test for FR-003 / US1-AC2:
      `test_search_rail_shows_the_stage_bar` — `.stage > .pv-stagebar` visible, 3px high at the
      stage's top edge, `aria-busy="true"`, sidebars still enabled. Confirm red on base.
- [X] T005 [P] [US1] Red test for FR-004 / US1-AC3:
      `test_search_results_placeholder_matches_real_groups` — `.result-group__head`, count,
      result rows with title/meta/excerpt and `.result-more` inside `.pv-placeholder`.
- [X] T006 [P] [US1] Red test for FR-004 (home shape):
      `test_search_home_placeholder_matches_the_landing` — 96px logo placeholder, real
      `.search-home__form`, `.search-home__input` and `.search-home__submit`.
- [X] T007 [P] [US1] Red test for FR-001 / FR-004 / US1-AC3:
      `test_media_library_placeholder_matches_real_rows` — the rail click stays in-page
      (`timeOrigin` unchanged), intro, chips, count, sort, `.media-library__group` headings and
      three `.media-library__file` rows with icon, filename, meta, unused, cloud and remove.
- [X] T008 [US1] Implement `placeholderFor()` shapes `results`, `search-home` and
      `media-library` plus their seeds (`q=` from `lastSearchSnapshot()`, `Media Library` name),
      and add the scoped `.stage[aria-busy="true"] > .pv-placeholder` CSS override in
      `components.css`. Make T003–T007 green without touching rail/sidebar containers.

## Phase 4 — US2 (P1)

**Goal**: the pending state always clears, and a second write retargets it.
**Independent test**: replay a slow click, wait for settlement, then start a second click.

- [X] T009 [P] [US2] Red test for FR-006 / US2-AC1 / SC-003:
      `test_media_library_settlement_clears_state` — after the page paints the tile is enabled,
      `aria-busy` absent, bar hidden and placeholder gone.
- [X] T010 [US2] Reuse `finish()`/`fail()`/`clearStageFor()` for the new kind; make T009 green.
      Confirm the `noLocationFallback` branch still leaves the state until unload (inspection).
- [X] T011 [P] [US2] Red test for FR-007 / SC-004 / US2-AC3: extend
      `test_search_then_media_library_cancels_the_first` so a Search write followed by a Media
      Library write cancels the first, unlocks its tile and retargets the bar and placeholder.
- [X] T012 [US2] Extend the `activeFetches` cancel rule to the new kind; make T011 green.

## Phase 5 — US3 (P2)

**Goal**: destinations, reduced motion and announcements are unchanged.
**Independent test**: click Search after a saved query and compare the arriving URL with the base.

- [X] T013 [P] [US3] Red test for SC-002:
      `test_destination_placeholder_origin_matches_the_reading_page` — the new placeholder's content box
      starts at the real `.read` origin (stage +64px/+40px at 1440px).
- [X] T014 [US3] Set the placeholder wrapper's padding to the real `.read` offsets; make T013 green.
      Confirm by inspection that the reduced-motion rule stops the sweep without hiding text and
      `announce()` fires once at start and once at settlement.
- [X] T015 [US3] Inspect `openSearch()`, `lastSearchSnapshot()` and both rail hrefs against the
      base: the saved last-results destination and `/media-library/` are unchanged. The only edit
      to `openSearch()` is the added `source: railSearch` option so the clicked tile can lock.

## Phase 6 — Polish

- [X] T016 Run the named new cases as a targeted module with the throwaway `gkps245` database:
      `GKPS_DB=gkps245 python3 preview/run_local.py -- <venv-python> manage.py test
      tests.e2e.test_navigation_pending --keepdb --noinput`. Report failures by name; if a failure
      also occurs on unmodified base, say so. Full browser suite waits for the push step.
- [X] T017 Run `preview/probe.py` and the chat-frame verifier; record the three measured pending
      states in `converge.md` and check the diff contains only `static/web/reading.js`,
      `static/styles/design/components.css` and the E2E module (FR-010).

## Phase 7 — Convergence

<!-- written by Converge only; absent until it runs -->

- [X] T019 After the owner reported the Media Library placeholder did not match the real layout:
      red test comparing the placeholder's `.read` box with the settled one, then wrap the library
      skeleton in the real `.read[data-kind="media-library"]` header/body anatomy, seed the real
      count and sort shapes, match the unused-line height, rebuild previews and restart the
      server. Live boxes at 1440×900 now match the reference at every measured point.

## Phase 8 — Post-fold correction

- [X] T018 After the owner asked why the placeholder's search input sat at the top: red test
      (`test_search_home_placeholder_matches_the_landing` now compares pending and real input y —
      measured 186 vs 422), change the scoped override to keep `display: grid` for `.search-home`
      while leaving results and media at `block`, rebuild the previews, re-run the module and
      collectstatic/restart the dev server. Green: both at y=422, delta 0.
- [X] T020 After the owner asked for skeleton filters/sorter/sub-title and hidden header buttons:
      CSS-only change that keeps the real controls' geometry while painting grey bars over their
      text, and hides the three `.media-library__icon-btn` with `visibility: hidden` so their
      space stays reserved. Mirrored in the preview; E2E assertions check hidden buttons,
      transparent labels and the pseudo bars; targeted module and live geometry stay green.

## Phase 9 — Library skeleton data removal

- [X] T021 After the owner asked for no date groups, no file names/data and placeholder row buttons:
      FR-004 and `reading/R62` were tightened, then the library skeleton was reduced to three
      identical rows with name/meta/unused bars and two 36px action bars, dropping both group
      headings and the seeded `gereja.jpg` row. E2E assertions cover zero groups, zero row buttons,
      six action bars and an empty filename. Preview rebuilt, server restarted, full module green.

## Phase 10 — direct-load loading line

- [X] T022 After the owner asked what I would change for the post-arrival gap: red test for a direct
      `/media-library/` load under delayed network, then set `Loading files…` and the matching empty
      line in `media-library.js:init()` before `refresh()`. Companion allow-list for port 8787 was
      added by recreating only the media container with `preview/media-override.yml`; compose files
      and `.env` untouched. Targeted module `Ran 23 … OK`; live load showed the loading line first,
      then `10 of 10 files shown` with 10 rows.

## Phase 11 — hide the previous search shell while pending

- [X] T023 After the owner saw the old logo/search bar below a shorter destination placeholder: red
      test asserting `#searchHome`, `#homeLogo` and `#searchQuery` are hidden while the Media Library
      skeleton is up, then a scoped CSS rule hiding direct-child search sections under
      `stage[aria-busy="true"]`. The copy inside the placeholder stays visible. Preview mirrored,
      module ran 24 tests green, live probe showed all three old nodes hidden.

## Phase 12 — spinner on the loading line

- [X] T025 After the owner asked for a spinner: red test for `.media-library__loading-spinner` beside the loading text, then an 18px ring using the app's 2px divider/active colours and 800ms sweep with reduced-motion stillness; `render()` clears it. Module ran 24 tests green; live spinner measured 18px, 0.8s, removed after settlement.

## Phase 13 — spinner above the loading text

- [X] T026 After the owner said "above the text, i think": red test asserting `display:block` and the ring's bottom above the text node, then changed the spinner from inline-before to a centred block with a 10px gap. Module ran 24 tests green; live ring measured at x centre, spinner bottom 296 vs text top 306.

## Phase 14 — search input text as skeleton

- [X] T027 After the owner asked to replace the text inside the search bar too: red test for a
      `.pv-ph-bar--input` inside the home placeholder and an empty `placeholder` attribute, then
      a centred 12px bar in the form. Preview mirrored; module ran 24 tests green; live bar measured
      353.8×12 at the input's vertical centre (y 444 inside input y 422–478).

## Phase 15 — push-step verification

- [X] T028 Manual lanes (no CI): 24 slice tests, 45 capability A, 141 capability B, 569 unit tests. Attributed all reds against the same commands on unmodified develop; fixed the age-bucket settle helper and the focus/hide interaction; carded the two uncarded base reds.
