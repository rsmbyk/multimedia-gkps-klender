# Convergence: pending state for Search and Media Library rail tiles

**Pass**: 1
**Date**: 2026-11-26
**Spec**: `specs/245-rail-fetch-feedback/spec.md`
**Plan**: `specs/245-rail-fetch-feedback/plan.md`

## What was checked

Every row of the plan's traceability table was re-assessed by the method it declared; no checkbox
was taken as evidence.

| Declared method | Rows | Evidence in this pass |
| --- | --- | --- |
| `test` | 16 | `tests.e2e.test_navigation_pending` — 22 tests (13 original, 9 new) run on `gkps245`; `Ran 22 … OK`. New cases cover both tiles' lock/bar, three placeholder shapes, in-place navigation, settlement, supersede and origin. One case was re-run after adding the rail `aria-current` assertion: `Ran 1 … OK`. |
| `inspection` | 11 | Read `static/web/reading.js` (STAGE_KINDS, sectionsFor, finish/fail, openSearch, announce, history), `static/styles/design/components.css` (scoped override and reduced-motion), and `git diff --stat` (three source files, no backend). |
| `manual` | 0 | none declared |

A first module run was red in five spec-243 tests and one error because the refactor dropped the
old placeholder ids; the ids were restored and the same full module went green. The one failure
among the new cases was a wrong `sessionStorage` key in the test fixture (`gkps-search-last` vs
`gkps-search-last-tab`); corrected and re-run green.

## Findings by requirement

| Requirement | Kind | Outcome |
| --- | --- | --- |
| FR-001 | met | `#railMediaLibrary` now calls `navigate()` with kind `media-library`; E2E proves `timeOrigin` unchanged and URL `/media-library/`. |
| FR-002 | met | Rail tiles carry `aria-disabled="true"` and SVG opacity `0.45` while pending (two E2E cases). |
| FR-003 | met | Stage bar 3px at stage-relative y=0, stage `aria-busy="true"` (E2E). |
| FR-004 | met | Three shapes probed: two `.result-group` with rows and Show more, the 96px home logo/input, and `.media-library` with chips, group headings and three file rows (E2E). The scoped CSS override makes the shell-hidden Search shapes paint. |
| FR-005 | inspection | `sectionsFor()` still returns `['stage']`; only the source tile receives `aria-disabled`. No rail/sidebar container disable in the diff. |
| FR-006 | met / inspection | Settlement test passes; `fail()`'s `noLocationFallback` branch is unchanged, so full-page fallback still keeps pending state until unload. |
| FR-007 | met | Search → Media Library cancels the first fetch and unlocks its tile (E2E). |
| FR-008 | inspection | Search still opens the saved last result set or `/`; Media Library still uses its route. `openSearch()` gained only `source: railSearch` for the lock — recorded as an honest delta from research D003. |
| FR-009 | inspection | `announce()` still fires at start and settlement without moving focus; reduced-motion rule stops the sweep. |
| FR-010 | inspection | `git diff --stat`: `components.css`, `reading.js`, `test_navigation_pending.py` only; no URL, view, model or migration file. Spec pack is documentation. |
| SC-001 | inspection | Preview probe: all three states show lock + bar + placeholder; zero page errors; frame verifier PASS. |
| SC-002 | met | `test_destination_placeholder_origin_matches_the_reading_page` passes: media placeholder starts at the real `.read` box. |
| SC-003 | met | `test_media_library_settlement_clears_state` passes: no `aria-busy`, bar or placeholder residue. |
| SC-004 | met | supersede case passes. |
| US1–US3 scenarios | met / inspection | Each scenario maps to a passed case or an inspected unchanged branch; no scenario left unchecked. |

## Gate-2 findings disposition

- **H1** (Search shapes hidden on home state): resolved by the scoped override in `components.css`;
  the home and results placeholder E2E cases both find a visible placeholder.
- **H2** (`data-home` changes on an in-place library visit): resolved — `applyPage()` syncs rail
  `aria-current` from the fresh document, and the E2E case now asserts the Media Library tile is
  current after arrival.
- **L1** (reduced motion and announcement are inspection-only): accepted at gate 2. Full browser
  suite remains deferred to the push step per the owner; cost is one visual check.

## Pass 2 — post-fold correction (2026-11-26)

- Trigger: owner asked why the placeholder's search input sat at the top. No requirement changed;
  SC-002 already said the placeholder must start at the real page's content offsets.
- Root cause: the scoped unhide override used `display: block !important` for all three destination
  shapes. That killed `.search-home`'s own `display: grid` with `1fr auto 1fr` rows, so the form
  stacked from the top. Search results and Media Library still need `block`.
- Red evidence: `test_search_home_placeholder_matches_the_landing` compared the pending input y
  with the settled real input y — `186` vs `422`, delta 236.
- Fix: split the override so `.search-home` gets `display: grid !important`; rebuilt the previews
  with the same correction and re-ran the probe and frame verifier.
- Green evidence: targeted module `Ran 22 … OK`; live server after `collectstatic` and restart
  measured input y `422` in both placeholder and real home, delta `0`.
- Outcome: no new gaps, no capability delta; the fold's R62 already describes the centred logo and
  input, so `docs/spec/reading.md` needs no edit.

## Pass 3 — Media Library placeholder anatomy (2026-11-26)

- Trigger: owner reported the library placeholder did not match the real page. No requirement
  changed; FR-004 already said the placeholder must use the destination's own markup and offsets.
- Root cause: the library skeleton was a bare `.media-library` appended directly to `.pv-placeholder`,
  while the real page wraps it in `<article class="read" data-kind="media-library">` with a 42px
  header (title + three action buttons) and a `.read__body` offset by 8px. Measured before:
  placeholder `.media-library` x=144, y=40, w=1232; real x=230, y=90, w=1060.
- Fix: seed the same `.read` wrapper, header actions, title, count, sort glyph and unused-line
  height; use the real count class instead of a duplicate id. Preview pages rebuilt with the same
  markup.
- Red evidence: `test_media_library_placeholder_matches_real_rows` first failed with no `.read` in
  the placeholder; an origin test also had to move from `.media-library` to `.read` once the
  wrapper landed.
- Green evidence: targeted module `Ran 22 … OK`. Live measurement after `collectstatic` and
  restart, compared with the unmodified library page on port 63404 at 1440×900:
  `.read`, `.media-library`, intro, filters, sort button, group, first file row, file-main and
  unused line all match at x/y/width/height — e.g. `.read` x=230 y=40 w=1060, first file row
  x=230 y=258 w=1060 h=97. Only total heights differ (3 skeleton rows vs 10 real files).
- Outcome: no new gaps, no capability delta; R62 already names the header and file-row anatomy.

## Pass 4 — skeleton controls and hidden header actions (2026-11-26)

- Trigger: owner asked for the filters, sorter and sub-title to be shown as placeholder, and the
  top buttons hidden while the placeholder is displayed. No requirement changed; FR-004 already
  says bars stand in for content not yet known.
- Fix: scoped CSS paints grey bars over the intro/sub-title, chip labels, result count and sorter
  label while leaving the real elements in place, so geometry is unchanged. The three
  `.media-library__icon-btn` get `visibility: hidden`, reserving their 142×42 header slot.
- Evidence: E2E assertions check the action buttons are hidden, the labels compute to transparent,
  and the chip `::after` bar exists. Targeted module `Ran 22 … OK`. Live probe: intro x=230 y=90
  w=1060 h=22, chips x=230 y=156 w=389 h=30, sort button x=1114 y=153 w=176 h=36 — all unchanged
  from the reference page; header actions `visibility: hidden`, chip bar `rgb(217, 214, 205)`.
  Preview rebuilt; probe and frame verifier pass.
- Outcome: no new gaps, no capability delta; R62's "bars stand in only for content not yet known"
  already covers this.

## Pass 5 — library skeleton data removal (2026-11-26)

- Trigger: owner asked for no date groups, no file names/data, and placeholder bars in place of the
  row buttons. This tightened FR-004 and `reading/R62`; both were edited in this pass before the
  implementation, while the commit is still amendable and nothing is pushed.
- Fix: the media skeleton now emits three identical rows, each with icon/name/meta/unused bars and
  two 36px action bars; the "This week"/"Older" headings and the seeded `gereja.jpg` row are gone.
- Evidence: E2E assertions report 0 groups, 3 rows, 0 row buttons, 6 action bars and an empty
  filename; targeted module `Ran 22 … OK`. Live probe on port 8787: same counts, header actions
  hidden, HTTP 200 after `collectstatic` and restart. Preview rebuilt; frame verifier PASS.
- Outcome: no new gaps; the capability note reflects the tightened requirement.

## Mechanical fixes applied in this pass

- `sessionStorage` key corrected in the results-placeholder test.
- Old placeholder ids (`pvPh-bible`, `pvPh-song`, `pvPh-tatib`) restored after the refactor.
- Task and plan rows now name the actual new test functions; research D003 and the spec Assumptions
  record the added `source: railSearch` option rather than claiming `openSearch()` is byte-identical.
- `analysis.md` artifact SHAs refreshed after those documentation edits.

## Outcome

Converged in one pass: zero `missing`, `partial`, `contradicts` or `unrequested` gaps. Ready for
Fold. Nothing committed or pushed.

## Pass 6 — direct Media Library loading line (2026-11-26)

- Trigger: owner asked what I would change for the delay after arrival, then said proceed.
- Requirement tightened: FR-011 and `reading/R62` now require a loading count/empty line on direct
  loads that bypass the navigation placeholder.
- Fix: `media-library.js:init()` writes `Loading files…` and `Loading files on this computer…`
  before `refresh()`; `render()` still applies the whole state in one pass.
- Local config: companion recreated with 8787 in its allow-list via the checked-in
  `preview/media-override.yml`; no compose file or `.env` edit.
- Evidence: red test showed `0 of 0 files shown` where the loading line belongs; after the fix the
  module ran 23 tests green. Live at 8787: `Loading files…` at ~4.07 s under 800 ms simulated
  latency, then `10 of 10 files shown`, 10 rows, empty slot hidden.
- Outcome: no gaps; no capability renumbering.

## Pass 7 — previous search shell hidden during fetch (2026-11-26)

- Trigger: owner reported that the previous search page's logo and search bar were visible below a
  destination placeholder. FR-012 and `reading/R62` were tightened before the fix.
- Root cause: `.stage[aria-busy="true"] .read { visibility: hidden }` covered the reading article only.
  The search shell sections are sibling elements of the placeholder; the skeleton is shorter than the
  search home, so the old logo/input remained visible underneath.
- Fix: scope `visibility: hidden` to `.stage[aria-busy="true"] > .search-home, > .search-results`; the
  placeholder's own descendant copy is separately forced visible, so Search-to-home still works.
- Evidence: red test failed on `#searchHome`; after the fix the module ran 24 tests green. Live at
  8787 from the search home: `searchHome false, logo false, input false, placeholder true`.
- Outcome: no gaps; no renumbering.

## Pass 8 — spinner on the direct-load line (2026-11-26)

- Trigger: owner asked for a spinner on "Loading files on this computer". FR-011 and `reading/R62`
  were tightened before the code change.
- Fix: `media-library.js` prepends an `aria-hidden` 18px ring to the loading line; CSS uses the
  divider/active tokens, an 800ms linear sweep, and stops under `prefers-reduced-motion`.
  `render()` replaces the textContent, so the ring disappears with the loading state.
- Evidence: red test found no spinner node; after the fix the module ran 24 tests green. Live at
  8787 under 1200ms latency: 18px, `0.8s`, inline-block beside the text; after settlement 0 rings
  and `10 of 10 files shown`.
- Outcome: no gaps; no renumbering.

## Pass 9 — spinner above the loading text (2026-11-26)

- Trigger: owner asked for the spinner above the text. FR-011 and `reading/R62` were tightened.
- Fix: `.media-library__loading-spinner` changed from `inline-block` with a right margin to a
  centred `block` with `margin: 0 auto 10px`; size, 800ms sweep and reduced-motion rule unchanged.
- Evidence: red test failed with `inline-block != block`; after the fix 24 tests green. Live at 8787:
  `display:block`, spinner bottom 296 vs text top 306 (10px gap), duration `0.8s`.
- Outcome: no gaps; no renumbering.

## Pass 10 — search input text as skeleton (2026-11-26)

- Trigger: owner asked to replace the text inside the search bar with a placeholder too.
- Fix: the Search-home skeleton's input uses `placeholder=""` and carries an absolutely centred
  `.pv-ph-bar--input` inside the existing `.search-home__form` positioning context; the real
  input geometry and submit button are unchanged.
- Evidence: red test found no bar node; after the fix 24 tests green. Live at 8787 under 2500ms
  latency: bar 353.8×12 at y=444 inside input y=422–478, placeholder attribute empty.
- Outcome: no gaps; no renumbering.

## Final acceptance (2026-11-26)

The owner accepted the final state after passes 2–10. No further code change was authorized.
Delivery (board card, VERSION, changelog and PR) is not authorized yet; nothing is pushed.

## Pass 11 — push-step verification (2026-11-26)

No CI workflow exists (`git ls-tree origin/develop .github/workflows/` is empty), so these are manual
lanes on the throwaway `gkps245` database:

| Lane | Result |
| --- | --- |
| Slice module `test_navigation_pending` | 24 tests green. |
| Capability batch A (nav freshness, rail marks, targeted reading, home search, filter pill, age buckets) | 45 green after the helper fix below. |
| Capability batch B (`test_media_library`, `test_reading`) | 141 tests, 5 reds — 3 owned by the base, 2 branch-owned and fixed. |
| Whole unit lane `manage.py test multimedia` | 569 tests, 9 failures — the identical 9 on unmodified `origin/develop` `fa452197` under the same command. |
| Full browser matrix | Not run: 962 E2E methods, no pipeline. Named lanes above were run instead. |

### Red attribution

- `test_media_entry_has_roomy_spacing_and_wraps_on_narrow_screen` — ITEM-156.
- `test_the_panel_shows_its_empty_view_when_no_songbook_exists` — ITEM-137.
- `test_hymn_song_order_is_visible_after_browsing_from_home` — reproduced on the base under the same
  command; new card ITEM-262.
- `test_the_scripture_fragment_groups_searchable_books_by_testament` — one of the 9 identical unit
  failures, outside ITEM-217's eight; new card ITEM-261.
- The other eight unit failures are ITEM-217's recorded list, verified by the identical sorted set.

### Branch-owned fixes during the push step

- Age-bucket helper waited on `#mediaEmpty:not([hidden])`, which the new loading line satisfies at
  first paint; it now waits for the count to leave `Loading files…`. The module went 18 green.
- The two focus reds (`test_the_search_rail_opens_a_focused_landing`,
  `test_the_landing_hands_focus_over_when_results_open`) were caused by the FR-012 hiding rule: the
  incoming `#searchQuery` was still hidden while `applyPage()` called `focusLandingSearch()`. The
  hiding rule now keys on `.stage--destination-placeholder`, a class added with the placeholder,
  removed at the start of `applyPage()` and cleared on settlement. Both tests went green with the
  hide test still green (26 tests across the two modules).

Outcome: no branch-owned reds remain; the base-owned reds are carded and unchanged.
