# Implementation Plan: center the service-entry kind mark

**Spec**: `specs/237-sidebar-mark-centering/spec.md`
**Branch**: `fix/237-sidebar-mark-centering`
**Bump**: `patch` — origin/develop is `1.36.22` at Plan; the level is applied pre-merge and re-checked then
**Preview**: `specs/237-sidebar-mark-centering/preview/README.md` (live worktree page)

## Technical Context

| Field | Value |
| --- | --- |
| Language / version | Python 3.12 + Django 4.0 server; vanilla CSS/HTML, no JavaScript change |
| Primary dependencies | none added; Playwright (Python) already supplies user-visible E2E |
| Storage | PostgreSQL for fixtures only; no model, migration or endpoint change |
| Testing | Django test runner; Playwright E2E through `StaticLiveServerTestCase` with a throwaway database |
| Target platform | The Tata Ibadah contents list and its drag copy, desktop and narrow viewports, light and dark themes |
| Project type | Server-rendered Django templates; mark span from `_toc_mark.html`, stylesheet in `static/styles/design/` |
| Performance goals | none; no new work at runtime |
| Constraints | Two selectors beside spec 063's number rule; no template, script or endpoint edit |
| Scale / scope | Every marked row in `#chList` is affected; verified behaviour is limited to the live list and its drag copy |

## Constitution Check

No `CONSTITUTION.md` exists at the base commit — the constitution is optional and never
auto-created (SDD-01), so the table is empty by absence, not by waiver.

Re-checked after Phase 1: pass — no new component, dependency, interface or runtime behaviour.

## Phase 0 — Research

See `research.md`. **Unknowns remaining: 0.**

## Phase 1 — Design

- `data-model.md` — no persisted entity; documents the flex boxes and the slot badge's positioning context.
- `contracts/README.md` — `none`: no HTTP, script, model or event interface changes.
- `quickstart.md` — live preview, probe and targeted E2E command.

## Traceability

| Requirement | Component / file | Verified by | Notes |
| --- | --- | --- | --- |
| US1/AC1 | `#chList a.songrow` in `static/styles/design/components.css`; `tests/e2e/test_sidebar_mark_centring.py` | `test` → `test_mark_centre_matches_number_on_every_row` | 0px centre offset on all 12 rows |
| US1/AC2 | existing `.songrow__mark` colour rules; same module | `inspection` — computed `color` follows `--head-ink` / `--ink` in both themes; hover and selected rules are untouched | no new token or transition |
| US2/AC1 | `.songrow__mark`, `.songrow__c`, `.songrow__t`; same module | `test` → `test_columns_heights_and_clamp_are_unchanged` | x 42/66px, heights 38/53px, three-line clamp |
| US2/AC2 | same rules; same module | `test` → `test_wrapped_song_row_keeps_centred_mark` | 390px window, 74px row, centre 0px |
| US3/AC1 | `.songrow__mark .slot__badge`; same module | `test` → `test_slot_badge_follows_the_mark` | badge bottom 9px above row, x 50px |
| US3/AC2 | `.reorder__ghost .songrow__mark`; `static/web/reorder.js:268` | `inspection` — ghost is stamped from `drag.row.innerHTML`, so the mark span is present; the CSS selector applies the same declaration as the number's | drag-copy rule mirrors spec 063 |
| FR-001 | `#chList .songrow__mark` in `components.css` | `test` → `test_mark_centre_matches_number_on_every_row` | every marked row centred |
| FR-002 | mark box and label rules | `test` → `test_columns_heights_and_clamp_are_unchanged` | 16px mark, 42px/66px columns, clamp unchanged |
| FR-003 | `.reorder__ghost .songrow__mark` | `inspection` — selector beside `.reorder__ghost .songrow__c`; the ghost copies the row markup | no script change |
| FR-004 | one CSS diff; `tests/e2e/test_sidebar_kind_marks.py` | `inspection` — no dock, projector or songbook row gains a mark; the diff touches only the two selectors | existing `test_dock_and_projector_keep_their_own_rows` still passes at push |
| SC-001 | new E2E module | `test` → `test_mark_centre_matches_number_on_every_row` | base fails at −4px / −11.5px |
| SC-002 | new E2E module | `test` → `test_columns_heights_and_clamp_are_unchanged` + `test_slot_badge_follows_the_mark` | geometry and badge numbers |
| SC-003 | `.reorder__ghost` rule | `inspection` — CSS readout on a ghost clone mirrors the number's computed `align-self: center` | no drag-gesture dependency |
| SC-004 | `preview/probe.py` | `inspection` — readouts in both themes at 1440/1024/390px; light and dark colours unchanged | numbers frozen from gate 1 |

**Verification split**: 8 test · 6 inspection · 0 manual

## Complexity Tracking

| Violation | Why needed | Simpler alternative rejected because |
| --- | --- | --- |
| | | |

No violations.

## Project Structure

### Documentation

```
specs/237-sidebar-mark-centering/
  spec.md plan.md research.md data-model.md quickstart.md tasks.md analysis.md
  contracts/README.md checklists/requirements.md checklists/checklist.md
  preview/README.md preview/probe.py
```

### Source

```
static/styles/design/components.css              # two selectors beside spec 063's number rule
tests/e2e/test_sidebar_mark_centring.py          # new E2E module for the row and badge boxes
docs/spec/reading.md                             # R49 modified at Fold
backlog/board.md, backlog/items/ITEM-252-*       # card opened in this PR
VERSION, CHANGELOG.md                            # patch line at delivery
```

### Structure Decision

The declaration belongs beside spec 063's number rule: both columns of the same flex
line need the same alignment, and the ghost copy is covered by the same selector pair.
A new E2E module keeps the row geometry and badge evidence together; the existing
`test_sidebar_kind_marks.py` covers which marks render, not where they sit. The preview
stays live because the measurement needs the real service rows and the shared Postgres
fixture; `probe.py` supplies the frozen before/after numbers without changing the page.
