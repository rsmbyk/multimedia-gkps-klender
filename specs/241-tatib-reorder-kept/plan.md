# Implementation Plan: reordered Tata Ibadah keeps every entry

**Spec**: `specs/241-tatib-reorder-kept/spec.md`
**Branch**: `fix/241-tatib-reorder-kept`
**Bump**: `patch`
**Preview**: `specs/241-tatib-reorder-kept/preview/` — live at `http://127.0.0.1:8791/tatib/322/`

## Technical Context

| Field | Value |
| --- | --- |
| Language / version | Python 3.12 + Django 4.0 server; vanilla ES5-style browser JavaScript |
| Primary dependencies | none added — the existing `reading.js` shell and `reorder.js` |
| Storage | no schema change; `ServiceEntry.order_number` slots already exist |
| Testing | Django test runner; Playwright E2E through `StaticLiveServerTestCase` |
| Target platform | the reading pages in a desktop browser (review viewport 1440×900) |
| Project type | server-rendered Django templates with an in-place JS shell |
| Performance goals | one pane re-read per drop; the sorter is a no-op when no song rows exist |
| Constraints | no document reload; the write stays at once; choices keep their options; legacy rows hold their slots |
| Scale / scope | two client files, three new E2E tests, one capability block modified, one added |

## Constitution Check

No `CONSTITUTION.md` at the repository root — optional and never auto-created (SDD-01) — so
there are no principles to check. The table is empty by absence, not by waiver.

Re-checked after Phase 1: n/a — no constitution exists.

## Phase 0 — Research

See `research.md`. **Unknowns remaining: 0.**

## Phase 1 — Design

- `data-model.md` — no persisted entity added; documents the fields and client caches in play.
- `contracts/` — `none` — the endpoint and payload are unchanged.
- `quickstart.md` — preview URL and the exact test commands.

## Traceability

| Requirement | Component / file | Verified by | Notes |
| --- | --- | --- | --- |
| US1/AC1 | `static/web/reorder.js` → `endDrag`, `applyPaneOrder`; `tests/e2e/test_reorder.py` | `test` → `test_a_drop_after_an_edit_is_written_and_the_pane_follows` | sidebar `3,1,2,4`, stage `3,1,2` |
| US1/AC2 | `static/web/reorder.js` → `persist`, `send` | `test` → same test (reload) | server kept the dropped order |
| US1/AC3 | `static/web/reorder.js` → `applyPaneOrder`, `readNodes` | `test` → `test_a_drag_after_an_add_keeps_every_entry_on_the_stage` | no section lost; stage matches sidebar |
| US1/AC4 | `static/web/reorder.js` → `endDrag` clears `drag` before the pane rewrite | `inspection` — no second `applyPaneOrder <- cancelDrag` stack in the captured timeline | one request, one write |
| US2/AC1 | `static/web/reading.js` → `songRowEls`, `applySongOrder` | `test` → `test_an_edit_leaves_the_contents_in_server_order` | rows equal a fresh fetch |
| US2/AC2 | `static/web/reading.js` → `songRowEls` | `test` → `tests/e2e/test_song_sort_retained.py` (six cases) | chosen sort still survives refreshes |
| US2/AC3 | `static/web/reading.js` → `applySongOrder` slot swap | `test` → `tests/e2e/test_reading.py` chapter-order cases | chapter rows keep their order |
| US3/AC1 | `static/web/reorder.js` → `cancelDrag` | `inspection` — `drag` is nulled before rewriting, so a rewrite-raised cancel is inert | no write posted on cancel |
| US3/AC2 | `static/web/reorder.js` → `applyPaneOrder` reads nodes at call time | `inspection` — the next gesture sees fresh `nodes` | no stale cache |
| FR-001 | `static/web/reorder.js` → `endDrag`, `persist` | `test` → `test_a_drop_after_an_edit_is_written_and_the_pane_follows` | one POST, dropped order |
| FR-002 | `static/web/reorder.js` → `applyPaneOrder` | `test` → same test and the add-then-drag test | both lists agree |
| FR-003 | `static/web/reorder.js` → `applyPaneOrder` filters missing nodes | `test` → `test_a_drag_after_an_add_keeps_every_entry_on_the_stage` | every entry once |
| FR-004 | `static/web/reorder.js` → `cancelDrag`, `applyPaneOrder` | `inspection` — a cancelled drag returns `place(current.order)` and never calls `persist()` | |
| FR-005 | `static/web/reading.js` → `songRowEls` requires song data | `test` → `test_an_edit_leaves_the_contents_in_server_order` | contents rows untouched |
| FR-006 | `static/web/reading.js` → `applySongOrder` | `test` → `test_song_sort_retained.py` and the existing sort toggle test | spec 233 kept |
| FR-007 | reorder endpoint + reload | `test` → both new drop tests (reload assertions) | |
| FR-008 | `applyPaneOrder` only moves pks named by `what`; nested option sections stay with their choice | `inspection` — `readNodes()` caches nested sections but `what` lists only top-level rows | service 151 shape |
| SC-001 | three new E2E tests in `tests/e2e/test_reorder.py` | `test` → all three | base red, this branch green |
| SC-002 | `tests/e2e/test_reorder.py` (whole module) | `test` → 32 tests green | no regression |
| SC-003 | `test_an_edit_leaves_the_contents_in_server_order` | `test` → rows equal a fresh fetch | |
| SC-004 | `tests/e2e/test_song_sort_retained.py`, `tests/e2e/test_reading.py` | `test` → six sort tests green; no new reading failures, one prior red now green | known reds recorded |

**Verification split**: 18 test · 4 inspection · 0 manual

## Complexity Tracking

| Violation | Why needed | Simpler alternative rejected because |
| --- | --- | --- |
| | | |

No violations.

## Project Structure

```
specs/241-tatib-reorder-kept/
  spec.md plan.md research.md data-model.md quickstart.md tasks.md
  contracts/README.md checklists/requirements.md analysis.md
  preview/README.md
```

### Source

```
static/web/reading.js                       # scope the sorter to real song rows
static/web/reorder.js                       # end the gesture, re-read nodes, minimal moves
tests/e2e/test_reorder.py                   # three new tests
docs/spec/reading.md                        # R57 modified, R58 added at Fold
backlog/board.md, backlog/items/ITEM-256-*  # card opened and closed in this PR
VERSION, CHANGELOG.md                       # patch line at delivery
```

### Structure Decision

Both faults are client-side and in files already dedicated to these behaviours; no new module,
template or endpoint is introduced. The tests join the existing reorder module so the red/green
evidence sits beside the gesture cases it extends.
