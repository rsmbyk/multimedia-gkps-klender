# Implementation Plan: the empty search landing is ready for typing

**Spec**: `specs/220-initial-search-focus/spec.md` (Accepted, Gate 1 2026-11-22)
**Branch**: `fix/220-initial-search-focus`
**Bump**: `patch` (D007; shown at Gate 2) — `VERSION` `1.36.4 → 1.36.5` at delivery
**Preview**: `static preview at specs/220-initial-search-focus/preview/index.html`

## Technical Context

| Field | Value |
| --- | --- |
| Language / version | vanilla JS in `static/web/reading.js`, ES5-style IIFE, no build step |
| Primary dependencies | none new; `HTMLElement.focus({preventScroll})` is already used in this file |
| Existing patterns | the shell owns stage state on `document.documentElement.dataset` (`home`, `read`, `section`); `applyPage()` swaps the stage for both full loads and in-page arrivals; `reconcileChildren()` reuses the search form's nodes across states |
| Storage | none; the tab-local search snapshot is read as today and never written by this behaviour |
| Testing | `tests/e2e/test_reading.py` — five new Playwright tests in `ReadingE2ETests`; no existing test changes |
| Target platform | the public reading shell in Chromium at 1440×900 and 390×844; desktop and phone layouts |
| Performance goals | none measurable; one `focus()` call per arrival |
| Constraints | `reading/R15` geometry and the one-window-tall rule unchanged; no scroll, no transition, no new control; results and reading routes stay unfocused |
| Scale / scope | 1 source file (~15 lines net), 1 test module (+5 tests); no template, CSS, view or model change |

## Constitution Check

No `CONSTITUTION.md` in this repository — nothing to check (SDD-01). Re-checked after Phase 1:
unchanged.

## Phase 0 — Research

See `research.md`. **Unknowns remaining: 0.** Seven decisions: where focus is applied (D001),
`preventScroll` (D002), the landing predicate (D003), the explicit blur (D004), no CSS change (D005),
the test set (D006), the bump (D007).

## Phase 1 — Design

- `data-model.md` — explicitly none.
- `contracts/none.md` — explicitly none: no route, payload or header changes.
- `quickstart.md` — the commands that reproduce every number and run every test.

### Design notes

- **One predicate, one call.** `onLanding()` is `root.dataset.home === 'landing' &&
  root.dataset.read !== 'on'`; `focusLandingSearch()` returns early unless it is true, then focuses
  `#searchQuery` with `preventScroll: true`. Nothing else in the file learns about focus.
- **Two call sites, both after the state is settled.** At init, after `syncState()` and
  `revealCurrent()`; in `applyPage()`, after `syncState()` so `root.dataset.home` already names the
  arriving state. Both run after the stage markup is in place, which is what FR-001's "visible before
  focus is assigned" asks for.
- **The blur is keyed on the transition, not the destination.** `applyPage()` reads
  `previousHome = root.dataset.home` before it swaps the stage, and blurs only when
  `previousHome === 'landing'` and the arriving `home` is `results` and `document.activeElement` is the
  field. A re-submit typed into the compact bar therefore behaves exactly as it does today.
- **Nothing is added to the template or the stylesheet.** The ring is the existing
  `:focus-visible` rule (measured `rgb(28, 92, 60) solid 2px`, 2px offset).
- **The `bootFocusId` restore is left alone.** It serves background refreshes after a save and runs
  before the new focus call; where both apply, they agree (a landing refresh focuses the landing
  field).

## Traceability

| Requirement | Component / file | Verified by | Notes |
| --- | --- | --- | --- |
| FR-001 (the landing focuses on load, on every route that paints it) | `static/web/reading.js` — `onLanding()`, `focusLandingSearch()`, the init block | `test` → `tests/e2e/test_reading.py::ReadingE2ETests::test_the_empty_search_landing_takes_focus` (all five routes, typed without clicking) | |
| FR-001 (in-page arrival focuses too) | `applyPage()` | `test` → `test_the_search_rail_opens_a_focused_landing` | |
| FR-002 (focus changes neither value, selection nor scroll) | `focusLandingSearch()` — `preventScroll: true` | `test` → `test_focusing_the_landing_keeps_the_page_still` (`scrollY` 0, `selectionStart`/`selectionEnd` 0, value untouched, document one viewport tall) | |
| FR-003 (submit moves focus out; results never take it) | `applyPage()` blur, keyed on `previousHome` | `test` → `test_submitting_from_the_landing_moves_focus_out`, `test_results_never_take_focus` (direct load and Search-rail restoration) | |
| FR-004 (reading routes stay unfocused) | `onLanding()` read guard | `test` → `test_reading_routes_never_take_search_focus` (`/bible/1/1/`, `/songs/1/`, `/tatib/1/`) | |
| FR-005 (nothing else changes: no CSS, template, view or route) | the diff | `inspection` — the slice touches `static/web/reading.js` and `tests/e2e/test_reading.py` only; no rule, token, template or view in the diff | |
| FR-006 (only Spec 139's no-focus clause is superseded) | `specs/220-initial-search-focus/spec.md` §Clarifications; Fold's `modified` block for `reading/R15` | `inspection` — the superseded clause is recorded, and R15's geometry, no-scroll and no-transition text survives the fold | |
| UI/UX numbers (field box, centres, results offsets, no overflow) | `specs/220-initial-search-focus/preview/` | `manual` — the preview probe: 610×56 at top 422 (centre 450) at 1440×900, 354×56 at top 394 (centre 422) at 390×844, results bar 46/82, results section 128/164, `scrollY` 0, no overflow at 320/390/720/1440 | identical on the preview and the served page |

**Verification split**: `5 test · 2 inspection · 1 manual`.

## Complexity Tracking

| Violation | Why needed | Simpler alternative rejected because |
| --- | --- | --- |
| — | — | — |

## Project Structure

### Documentation

```
specs/220-initial-search-focus/
  spec.md  plan.md  research.md  data-model.md  quickstart.md  tasks.md  analysis.md
  converge.md  fold.md
  contracts/none.md  checklists/requirements.md
  preview/index.html          (the landing and results states, from served markup)
  preview/README.md           (how to reach each state by hand)
```

### Source

```
static/web/reading.js        (onLanding(), focusLandingSearch(), two call sites, the blur)
tests/e2e/test_reading.py    (five new tests in ReadingE2ETests)
docs/spec/reading.md         (Fold: R15 modified, R50 added)
backlog/board.md, backlog/items/ITEM-235-search-landing-focus.md
CHANGELOG.md, VERSION        (delivery commit)
```

### Structure Decision

No new module and no new directory in the source: the behaviour belongs to the shell that already owns
stage state, and it is fifteen lines inside it. The preview and its probe live in the slice folder
because they are evidence for this spec, not product code.