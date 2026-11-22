# Implementation Plan: an empty reading stage after deleting the open record

**Spec**: `specs/221-empty-reading-stage/spec.md` (Accepted, Gate 1 2026-11-22)
**Branch**: `fix/221-empty-reading-stage` · **Bump**: `patch` (declared here, applied pre-merge:
`VERSION` `1.36.6 → 1.36.8`).
**Preview**: `specs/221-empty-reading-stage/preview/index.html` (static, accepted at Gate 1)

## Technical Context

| Field | Value |
| --- | --- |
| Language / version | Python 3.12, Django 4.0 templates and class-based views; vanilla ES5-style JS in `static/web/editors.js` and `reading.js`, no build step |
| Primary dependencies | none new; Playwright (Python) for E2E, already a dev dependency |
| Existing patterns | `_shell()` supplies `data-read`/`data-home`; `applyPage()` reconciles the whole `.stage`; the delete flow already branches on `wasOnStage()`; `/tatib/?mode=template` is the existing query-flag precedent |
| Storage | none; the empty stage is a URL flag plus existing shell nodes, no model or migration |
| Testing | new `tests/e2e/test_deleted_stage.py` under Django's runner; `StaticLiveServerTestCase` with `STATICFILES_STORAGE` override and Playwright skip |
| Target platform | public reading shell in Chromium at 1440×900 and 390×844, both themes |
| Performance goals | none measurable; one query-flag append and one small template branch |
| Constraints | the preview's approved copy and geometry; R41's row removal, neighbour focus and history replacement stand; no new CSS token, endpoint or route |
| Scale / scope | 3 view methods, 1 shared template branch, 2 lines in `editors.js` plus its comment, 1 icon rule + 1 centring rule in `components.css`, 1 new E2E module |

## Constitution Check

No `CONSTITUTION.md` in this repository — nothing to check (SDD-01). Re-checked after Phase 1:
unchanged.

## Phase 0 — Research

See `research.md`. **Unknowns remaining: 0.** Eight decisions: the URL flag (D001), the view helper
(D002), the template copy (D003), the client branch (D004), stage reconciliation (D005), the empty
stage's identity (D006), verification (D007), the bump (D008).

## Phase 1 — Design

- `data-model.md` — explicitly none.
- `contracts/none.md` — explicitly none: no external interface changes.
- `quickstart.md` — reproduce the defect, the targeted test command, the slice's own dev server and
  the static preview; links to the two design notes rather than duplicating them.

### Design notes

- **One predicate, three views.** `_empty_stage(request)` reads `stage=empty`. `BookIndexView`,
  `BookDetailView` and `TatibView` pass it as `read_on` to `_shell()`, choose `home_state` `'reading'`
  when set and add `read_name='Nothing open.'` plus the hint to the context. Their `nav` and `ch`
  values are untouched, so the side panels stay exactly where the delete flow puts them.
- **The copy comes from the base template.** The reading header is suppressed when `read_hint` is
  set, and `#readBody` renders the empty song view's `.entry__empty` block: a 38px empty-screen glyph
  (a blank monitor with a dash, selected by the owner from two option sets), `.entry__empty-title`
  "Nothing open." and `.entry__empty-hint` with the subtitle. Only one new CSS rule sizes the glyph;
  no list template is edited and a service's own items are unaffected.
- **The client change is one URL.** `wasOnStage()` is already computed before the navigation; when it
  is true, `parentListUrl(kind)` gains `?stage=empty` (or `&stage=empty` when `mode=template` is
  present) and the existing `gkpsNavigate(url, {kind:'refresh', replaceUrl:true})` does the rest.
  Off-stage deletes never see the flag.
- **No JS paints the stage.** `applyPage()` copies `data-read`, `data-home` and the entire `.stage`
  subtree from the fetched page, then refreshes its refs; the approved state is therefore server
  truth on both a fresh load and an in-page delete.
- **Nothing is on stage.** With no `read_kind`, `stageSection()` is `null`, so `gkpsStage()` reports no
  record and the idle-collapse and next-delete branches behave correctly.
- **The preview is the pixel contract.** Its after state toggles only `data-read`/`data-home` on the
  real shell; the measured `.read` boxes (520×148 at 856,48 and 354×148 at 18,84), icon 38px and the
  title/subtitle offsets and the block's exact centre (x=1116,y=450 / x=195,y=422) are what the
  E2E geometry test asserts. `preview/icons.html` and
  `icons2.html` record the owner's icon selection.

## Traceability

| Requirement | Component / file | Verified by | Notes |
| --- | --- | --- | --- |
| US1/AC1 (song delete leaves a nothing-open stage) | `editors.js`, `views.py`, `base.html` | `test` | `tests/e2e/test_deleted_stage.py::DeletedStageE2ETests::test_deleting_the_open_song_leaves_a_nothing_open_stage` |
| US1/AC2 (no search surface; songbook list beside it) | `views.py`, `applyPage()` | `test` | same test: datasets, `#searchHome` hidden, `#chList` rows present |
| US1/AC3 (reload keeps the state) | `views.py` | `test` | `test_reloading_the_empty_stage_keeps_the_reading_view` |
| US1/AC4 (Back does not revisit the deleted song) | `editors.js` | `test` | same test: history length and Back target |
| US1/AC5 (refused delete leaves the stage alone) | existing delete endpoints | `inspection` | 403/404 guard and failure message unchanged; no stage branch on failure |
| US2/AC6 (service delete) | `TatibView` | `test` | `test_deleting_the_open_service_keeps_the_reading_stage` |
| US2/AC7 (template delete keeps `mode=template`) | `TatibView`, `parentListUrl()` | `test` | `test_deleting_the_open_template_keeps_its_mode_and_the_stage` |
| US2/AC8 (songbook delete) | `BookIndexView` | `test` | `test_deleting_the_open_songbook_keeps_the_reading_stage` |
| US3/AC9 (off-stage delete is unchanged) | `editors.js` | `test` | `test_deleting_another_row_keeps_the_open_song_on_stage` |
| US3/AC10 (chrome, filters and focus unchanged) | shell state and `applyPage()` | `inspection` | diff review plus the preview's Before/After/dark/narrow toggles |
| FR-001 (reading stage with title and hint, no search) | `views.py`, `base.html` | `inspection` | context and template branch; pixels from the accepted preview |
| FR-002 (parent lists and modes stay) | `parentListUrl()`, all three views | `inspection` | URL builder unchanged; view `nav`/`ch` values unchanged |
| FR-003 (flag in the URL, reload and history) | `editors.js`, views | `test` | covered by the reload/history test |
| FR-004 (off-stage delete unchanged) | `editors.js` | `inspection` | the flag is inside the `onStage` branch only |
| FR-005 (only the approved copy, existing styles) | `base.html` | `inspection` | no CSS diff; only `.read__title` and `.listempty__hint` used |
| FR-006 (refused/restricted records excluded) | delete endpoints | `inspection` | no new path to the empty stage on failure |
| FR-007 (only R41's landing clause superseded) | `spec.md`, `docs/spec/reading.md` at Fold | `inspection` | row removal, neighbour focus and history replacement survive |
| SC-001 | E2E song test | `test` | dataset, title, hint, no search input in stage |
| SC-002 | E2E reload/history test | `test` | reload assertions and history length |
| SC-003 | E2E service/template/songbook tests | `test` | shell assertions plus the right list/mode |
| SC-004 | E2E off-stage test | `test` | stage text, URL and datasets byte-identical |
| SC-005 | E2E geometry test | `test` | `test_the_nothing_open_stage_keeps_the_shell_geometry` |
| UI/UX numbers (preview states and dark/narrow) | `specs/221-empty-reading-stage/preview/` | `manual` | click Before/After, dark and 390px; compare with the README table |

**Verification split**: `14 test · 8 inspection · 1 manual`.

## Complexity Tracking

| Violation | Why needed | Simpler alternative rejected because |
| --- | --- | --- |
| — | — | — |

## Project Structure (changes)

```
static/web/editors.js                       # append stage=empty on on-stage delete
multimedia/web/reading/views.py             # _empty_stage() + three view contexts
multimedia/web/templates/reading/base.html  # nothing-open block instead of the header
static/styles/design/components.css           # icon sizing + stage-centred empty block
tests/e2e/test_deleted_stage.py             # new E2E module (7 tests)
specs/221-empty-reading-stage/*             # accepted spec pack, preview, plan, tasks, analysis
docs/spec/reading.md                        # Fold: modify R41
VERSION, CHANGELOG.md                       # pre-merge patch bump
backlog/items/ITEM-236-*.md, backlog/board.md
```
