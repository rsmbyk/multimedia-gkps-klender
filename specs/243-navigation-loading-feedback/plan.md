# Implementation Plan: visible pending state for rail and sidebar fetches

**Spec**: `specs/243-navigation-loading-feedback/spec.md`
**Branch**: `fix/243-navigation-loading-feedback`
**Bump**: `patch` — neighbouring slices 240–242 all take patch; VERSION is `1.37.0` at this base
**Preview**: `specs/243-navigation-loading-feedback/preview/index.html` (static, opened as a file; v14 is the accepted state)

## Technical Context

| Field | Value |
| --- | --- |
| Language / version | Python 3.12 + Django 4.0 server; vanilla ES5-style browser JavaScript |
| Primary dependencies | none added — existing `reading.js`, `components.css` and inlined inline SVG/CSS tokens |
| Storage | no schema change; no endpoint change; no new persisted state |
| Testing | Playwright E2E through `StaticLiveServerTestCase`, plus targeted inspection of the client state machine |
| Target platform | desktop browser at 1440×900, plus 900px and 390px for the bar/placeholder offsets |
| Project type | server-rendered Django templates with an in-place JS shell |
| Performance goals | one fetch per activation, no queued second fetch, no extra layout shift beyond the accepted placeholder |
| Constraints | the stage keeps its content on list-only fetches; only the clicked item and (for writes) the stage lock; the rail and both sidebars stay interactive |
| Scale / scope | two client files, one new E2E module, one capability block added, one card and one patch line at delivery |

## Constitution Check

No `CONSTITUTION.md` at the repository root — optional and never auto-created (SDD-01) — so
there are no principles to check. The table is empty by absence, not by waiver.

Re-checked after Phase 1: n/a — no constitution exists.

## Phase 0 — Research

See `research.md` (the `preview/loading-patterns-research.md` note) and the accepted
`preview/rules-v5-draft.md`. **Unknowns remaining: 0.**

Resolved before this plan:

- Pending style: dim only; the spinner, label, edge fill and ring alternatives were shown and
  rejected in favour of the dim-only lock.
- Write classification: song, verse/passage and service write to the stage; rail, chapter-number
  list and songbook do not. The owner confirmed the chapter/verse boundary.
- Bar placement: very top edge of each section the fetch will update.
- Placeholder anatomy: real `read__head` / `read__body` shapes for Bible, song and Tata Ibadah,
  starting at the same stage padding as real content.
- Supersede rule: cancel by default; keep the first fetch only when it writes and the new click
  does not.

Assumptions carried forward: search and history traversal use the same `navigate()` mechanism and
the same write-vs-list classification; no separate visual treatment is introduced for them.

## Phase 1 — Design

- `data-model.md` — no persisted entity added; documents the client state objects and DOM anchors.
- `contracts/` — `none` — no route, payload or storage contract changes.
- `quickstart.md` — preview file path and the exact targeted verification commands.

## Traceability

| Requirement | Component / file | Verified by | Notes |
| --- | --- | --- | --- |
| US1/AC1 | `static/web/reading.js` → `railBtnClick`, `navigate`; `static/styles/design/components.css` → item lock, section bar | `test` → `tests/e2e/test_navigation_pending.py::test_a_rail_click_locks_the_item_and_bars_both_lists` | rail item opacity 0.45, bars at 0px top offset |
| US1/AC2–AC4 | same handlers; `kind` decides list-only | `test` → list-only cases in the same module | stage `aria-busy` absent, no bar, no placeholder |
| US2/AC1–AC3 | `static/web/reading.js` → stage-write branch and placeholder builder | `test` → song / verse / service cases | 3 / 5 / 3 anatomy rows |
| US2/AC4 | `static/styles/design/components.css` → placeholder padding | `inspection` — placeholder `.read` origin equals real `.read` (x=520, y=218 at 1440×900) | 18px at ≤720px |
| US2/AC5 | `navigate()` → finish path | `test` → settlement case | busy, bar and placeholder all clear |
| US3/AC1–AC3 | `navigate()` → supersede decision by stage-write class | `test` → three cancellation cases | queued `pendingNavigation` replaced by cancel/coexist |
| US3/AC4 | `releaseNavigation` / unlock path | `test` → re-activation case | cancelled item clickable again |
| US3/AC5 | `navigate()` → `fail()` full-page fallback | `inspection` — pending state is not cleared before `window.location.href` | stays until unload |
| FR-001, FR-002 | item lock state | `test` → lock cases; `inspection` — no spinner/label/edge/ring marker in the locked item | dim only |
| FR-003 | section bars | `test` → bar cases; `inspection` — bar-to-parent top offset 0px | first, second, stage |
| FR-004, FR-005 | stage-write classification | `test` → list-only and write cases | `aria-busy` only for writes |
| FR-006 | placeholder builder | `inspection` — class anatomy matches real page markup | no generic skeleton |
| FR-007 | supersede rule | `test` → cancellation cases | |
| FR-008 | all settlement paths | `test` + `inspection` | success, failure, supersede, fallback |
| FR-009 | rail/sidebar disabled state | `inspection` — only clicked item and stage carry disabled/busy state | |
| FR-010 | `navigate()` choke point | `inspection` — no per-click pending state outside `navigate()` | |

**Verification split**: 11 test · 8 inspection · 0 manual across 16 traceability rows. Targeted only; the full browser matrix is deferred to the push step.

## Complexity Tracking

| Violation | Why needed | Simpler alternative rejected because |
| --- | --- | --- |
| Disabling the clicked item during a fetch | The operator must not re-trigger the same rail/sidebar item while its request is live | Leaving it clickable was rejected by the owner; first-party guidance (Primer, Wix) is overridden deliberately and recorded in the spec |

No other violations.

## Project Structure

```
specs/243-navigation-loading-feedback/
  spec.md plan.md research.md data-model.md quickstart.md
  contracts/README.md
  preview/index.html, rules-v5-draft.md, loading-patterns-research.md
  preview/build*.py, probe*.py, grid*.png, source.html
  checklists/requirements.md, tasks.md, analysis.md  # later stages, not written by Plan
```

### Source

```
static/web/reading.js                      # pending state at navigate(), click sources, supersede
static/styles/design/components.css        # dim lock, section bars, layout-matched placeholder
tests/e2e/test_navigation_pending.py       # new targeted E2E module
docs/spec/reading.md                       # reading/R61 added at Fold
backlog/board.md, backlog/items/ITEM-258-* # card opened and closed with the slice
VERSION, CHANGELOG.md                      # patch bump at delivery
```

### Structure Decision

All behaviour lives in the shell script that already owns in-page navigation and in the
stylesheet that already owns the shell's state machine. No new module, endpoint, template
or storage is introduced; the placeholder is built client-side from the clicked item's
data using the product's existing `read__*`, `v` and `tatib__item` classes. The new E2E
module sits beside `test_navigation_freshness.py`, whose rail-to-page path it extends.
