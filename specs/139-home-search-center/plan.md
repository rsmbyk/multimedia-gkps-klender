# Implementation Plan: The landing search field sits on the window's middle

**Slice**: `specs/139-home-search-center` · **Branch**: `feat/139-home-search-center`
**Date**: 2026-10-27 · **Status**: Draft (gate 1 accepted the spec on 2026-10-27)
**bump**: `patch` — a presentation fix to an existing surface; no stored value, endpoint or capability
is added or removed. One `CHANGELOG.md` line under `## [Unreleased]` → `### Changed`: *"The landing
page's search field is centred on the window's middle at every width, with the logo above it — it sat
49px low on a desktop and 85px low on a phone."*

## Technical Context

| | |
| --- | --- |
| Language | CSS only — no Python, no template, no JavaScript |
| Front end | server-rendered templates, vanilla JS, hand-written CSS; no framework, no build step |
| Files | `static/styles/design/components.css` (the fix); `tests/e2e/test_home_search_center.py` (new) |
| Data | no migration, no payload change — the landing markup is untouched |
| Tests | Playwright E2E through `StaticLiveServerTestCase` (`tests/e2e/`), the repository's user-visible acceptance layer |
| Constraints | no new tokens, fonts, icons or dependencies; the results and reading views keep their geometry; no script reads the moved boxes |

## Constitution Check

`CONSTITUTION.md` does not exist and is never auto-created (SDD-01). No principle to check against;
nothing to justify in a Complexity Tracking table.

- Before Phase 0: n/a — no constitution.
- After Phase 1: n/a — no constitution.

## Phase 0 — Research

`research.md` records five decisions, all with provenance, and exits at zero unknowns:

1. Three grid rows rather than a compensating padding — the middle row lands on the container's middle
   whatever the logo measures; no second copy of the logo's height.
2. The section measures the stage's real paddings through two tokens — today it subtracts `--pad-top`
   while the phone stage pads 76px, which is 36px of the phone's error.
3. A signed margin on the stretched inner cancels the stage's asymmetry — the only box property that
   takes the negative value the phone layout needs.
4. The margin is qualified by `[data-home="landing"]` — the results bar is auto-height and would grow
   24px.
5. Verification is geometry at eleven widths straddling both breakpoints.

## Phase 1 — Design artifacts

- `data-model.md` — no entity; the five boxes with their before/after values at 1440×900.
- `contracts/none.md` — no interface; states the class names the stylesheet addresses and that none is
  renamed or read by a script.
- `quickstart.md` — how to open the preview, rebuild it, run the module and run the branch's server.

## Design

### Stylesheet (`static/styles/design/components.css`)

**(a) The stage states its two vertical paddings once** — the base rule at line 1694 and the phone
block at line 2897:

```css
.stage {
  --stage-pad-top: var(--pad-top);
  --stage-pad-bottom: 64px;
  padding: var(--stage-pad-top) clamp(24px, 5vw, 64px) var(--stage-pad-bottom);
}

@media (max-width: 720px) {
  :root .stage { --stage-pad-top: calc(var(--topbar-h) + 18px); padding-top: var(--stage-pad-top); }
}
```

**(b) The section fills that box, and the form is its middle row** — replacing the flex centring at
line 956:

```css
.search-home {
  min-height: calc(100svh - var(--stage-pad-top) - var(--stage-pad-bottom));
  display: grid;
  align-items: stretch;
  justify-items: center;
}
.search-home__inner {
  width: min(100%, 610px);
  text-align: center;
  display: grid;
  grid-template-rows: 1fr auto 1fr;
  justify-items: center;
}
[data-home="landing"] .search-home__inner {
  margin-top: calc(var(--stage-pad-bottom) - var(--stage-pad-top));
}
.search-home__logo { grid-row: 1; align-self: end; }
.search-home__form { grid-row: 2; width: 100%; }
```

That is the whole change. Measured on the rendered page (Chromium): field centre 549 → **500** at
1920×1000, 499 → **450** at 1440×900, 449 → **400** at 1280×800, 433 → **384** at 1024×768, 535 →
**450** at 720×900, 507 → **422** at 390×844, 369 → **284** at 320×568; the logo keeps its 26px gap and
stays inside the window down to 320×568 (top 134); the document's height is unchanged at every width;
the results bar keeps field top 46 (≥721px) / 82 (≤720px) and results top 128 / 164; the reading page
never paints the section.

Why the phone needed (a) as well as (b): `min-height` used to subtract `--pad-top` (40) while the stage
pads 76 for the toolbar, so the section was 36px taller than its space and its middle 18px low on top of
the block's 61px — the measured +85.

### Tests (`tests/e2e/test_home_search_center.py`, new)

One class, `HomeSearchCenterE2ETests`, on `StaticLiveServerTestCase`, no fixtures beyond a song for the
reading-view check. A `CENTRE` helper returns the field's, the logo's and the section's rects plus the
document's `scrollHeight`/`scrollWidth`, and a `at(width, height)` helper resizes the page. Seven tests:

1. `test_the_field_is_on_the_window_middle` — eleven widths, `|centre − h/2| ≤ 1`.
2. `test_the_logo_stays_whole_above_the_field` — logo top ≥ 0 and the gap is 26px at each width.
3. `test_the_landing_page_is_one_window_tall` — `scrollHeight === innerHeight`, no horizontal overflow.
4. `test_the_phone_layout_centres_too` — 720, 600, 390, 320; the section is exactly the stage's content
   box and the field is on the middle.
5. `test_the_results_bar_keeps_its_place` — a query submitted; field top 46 at 1440×900, 82 at 390×844;
   results top 128 / 164, bar height 88.
6. `test_the_reading_page_is_unchanged` — a song page: `.search-home` is not painted, and `.read` sits
   at the stage's content box (same left, top, width).
7. `test_the_field_does_not_travel` — no transition on the section's height, `scrollY === 0` on load,
   and the field's centre is unchanged 400ms after paint.

## Traceability

| ID | Requirement / scenario | Component | Verified by |
| --- | --- | --- | --- |
| FR-001 | the field's box is on the window's middle, within 1px, 320–1920px | `.search-home__inner` grid rows | `test` — `test_the_field_is_on_the_window_middle` |
| FR-002 | the logo sits above the field, whole, with its 26px gap | row 1 + `align-self: end`, logo rule untouched | `test` — `test_the_logo_stays_whole_above_the_field` |
| FR-003 | the landing page stays one window tall | `min-height` from the stage's tokens | `test` — `test_the_landing_page_is_one_window_tall` |
| FR-004 | the phone layout centres too, from the stage's real paddings | `--stage-pad-top` in the phone block | `test` — `test_the_phone_layout_centres_too` |
| FR-005 | the results bar and the reading view do not move | `[data-home="landing"]` guard; untouched reading rules | `test` — `test_the_results_bar_keeps_its_place`, `test_the_reading_page_is_unchanged` |
| FR-006 | no motion, no scroll, no focus change on load | no transition declared | `test` — `test_the_field_does_not_travel` |
| SC-001 | 1px tolerance at eleven widths | the grid rows | `test` — `test_the_field_is_on_the_window_middle` |
| SC-002 | no scrollbars | the `min-height` calculation | `test` — `test_the_landing_page_is_one_window_tall` |
| SC-003 | logo whole, 26px gap | row 1 | `test` — `test_the_logo_stays_whole_above_the_field` |
| SC-004 | results/reading unchanged | the state guard | `test` — the two US2 tests |
| US1.1 | 1440×900: field 422–478, centre 450 | the grid rows | `test` — `test_the_field_is_on_the_window_middle` |
| US1.2 | 390×844: field centre 422, logo top 272 | the tokens + the grid rows | `test` — `test_the_phone_layout_centres_too` |
| US1.3 | 1024×768: centre 384 | the grid rows | `test` — `test_the_field_is_on_the_window_middle` |
| US1.4 | resizing 1920→320 keeps the field on the middle | the grid rows | `test` — `test_the_field_is_on_the_window_middle` |
| US2.1 | results: field top 46, list top 128 | `[data-home="landing"]` guard | `test` — `test_the_results_bar_keeps_its_place` |
| US2.2 | reading: no search section; the article keeps its box | untouched `.read` rules | `test` — `test_the_reading_page_is_unchanged` |
| Edge | a 320×568 window clips nothing above | `1fr auto 1fr` with a 96px logo | `test` — `test_the_logo_stays_whole_above_the_field` (320×568) |
| Edge | ≤720px the section measures the toolbar's padding | `--stage-pad-top` | `test` — `test_the_phone_layout_centres_too` |
| Edge | the results bar never recentres on resize | `[data-home="landing"]` guard | `test` — `test_the_results_bar_keeps_its_place` (resize after submit) |

**Verification split: 19 test · 0 inspection · 0 manual.** Untested is allowed; unverifiable is not.
The `inspection` rows of spec 137 needed a look because a rule there was inherited; here every claim is
a rect, and a rect is a measurement.

## Risks

- **A future logo size.** Row 1 is `1fr` and the logo is aligned to its end, so a taller logo keeps the
  form on the middle and moves only its own top edge; `test_the_logo_stays_whole_above_the_field` reads
  the gap from the rects, not a constant, and fails first if a change squeezes the logo out of the top.
- **`--stage-pad-top` becomes load-bearing.** Anything that sets the stage's top padding without the
  token would leave the section measuring the old value. The token is set in the two places the padding
  is set; `test_the_phone_layout_centres_too` fails if a third appears.
- **The 1px tolerance is tight.** Chromium reports fractional rects; the tolerance is the spec's, and
  the measurement is a difference of two rects on the same page, so sub-pixel rounding cannot accumulate.
