# Implementation Plan: The sidebars say which nothing they show

**Spec**: `specs/129-sidebar-empty-states/spec.md`
**Branch**: `fix/129-sidebar-empty-states`
**Bump**: `patch`
**Preview**: `specs/129-sidebar-empty-states/preview/` — the running branch plus the probe that measured it

## Technical Context

| Field | Value |
| --- | --- |
| Language / version | Python 3.12, Django 4.0 templates; ES5-style browser JavaScript (no build step) |
| Primary dependencies | Django template engine; `static/styles/design/tokens.css` + `components.css`; no new library |
| Storage | none — the block is composed per render and typed in the browser |
| Testing | Django `TestCase` for the rendered markup; Playwright (Python) E2E for the states and the centring |
| Target platform | the reading shell at any width, light and dark themes |
| Project type | server-rendered pages + in-page navigation that swaps shell fragments |
| Performance goals | none measurable: no new request, no new script file, no layout read in a loop |
| Constraints | the offline saved render must keep parity with the server route (spec 122) |
| Scale / scope | 2 blocks, 6 panes' worth of copy, 3 JS files, 1 stylesheet, 2 templates-of-context |

## Constitution Check

`n/a — no CONSTITUTION.md in this repository` (SDD-01: optional, never auto-created).

Re-checked after Phase 1: nothing to check against; the repo's `docs/PROCESS.md` rules were applied instead
(one slice, one branch, tests before the claim, no commit before Fold).

## Phase 0 — Research

See `research.md`. **Unknowns remaining: 0.**

## Phase 1 — Design

- `data-model.md` — the block's data attributes and the six copies; no persisted entity
- `contracts/` — `none`; the only interfaces are the existing DOM ids and the `window.shellListEmpty` helper
- `quickstart.md` — serve the worktree, read the four states, measure the centring

## Traceability

| Requirement | Component / file | Verified by | Notes |
| --- | --- | --- | --- |
| FR-001 | `multimedia/web/templates/reading/base.html` (block markup), `static/styles/design/components.css` (`.listempty`) | `test` → `tests/e2e/test_reading.py::ReadingE2ETests::test_sidebar_empty_states_are_centred_and_typed` | offsets ≤ 1.5px asserted on two panes |
| FR-002 | `base.html`, `components.css` | `test` → same E2E; `inspection` — glyph is a sibling of the two paragraphs | |
| FR-003 | `static/web/reading.js` (`paintListEmpty`) | `test` → the same E2E (all four states, plus clearing the filter) | |
| FR-004 | `multimedia/web/reading/views.py` (`PANEL_META`, `CH_META`) | `test` → `multimedia/web/tests.py::ReadingViewTests::test_each_section_names_its_own_first_list`, `…::test_a_songbook_with_no_songs_says_no_songs_yet`, `…::test_a_service_with_no_sections_says_no_sections_yet` | |
| FR-005 | `base.html` (two glyph spans), `components.css` (`[data-when]` rules) | `inspection` — the miss glyph is a magnifier with a cross in the lens | |
| FR-006 | `static/web/reading.js` (boot paint) | `test` → the E2E opens both empty pages without typing | |
| FR-007 | `static/web/reading.js` (`reconcileNode` on both blocks, filters re-applied after a swap) | `test` → `tests/e2e/test_targeted_reading_updates.py` (the existing in-page navigation suite) + the new E2E's clear step | |
| FR-008 | `static/web/offline-render.js` (`LIST_EMPTY`, `labelListEmpty`, `paintListEmptyStates`) | `test` → `tests/e2e/test_saved_render_parity.py` | generic by construction: it re-labels for the section it builds |
| FR-009 | `static/web/entries.js` | `inspection` — the delete handler calls `window.shellListEmpty(node, false, 0)` | the E2E delete suites cover the row disappearing |
| FR-010 | `components.css` (`[data-nav="mini"] .panel .listempty`), `static/web/reading.js` (alkitab early return) | `inspection` — the probe reports `display: none` in mini | |
| FR-011 | `base.html`, `components.css` | `grep -rn "panel__empty\|ch__empty"` → no hits | |
| SC-001 | the running branch | `test` → the E2E's measured offsets; the probe prints `dvCenter`/`dhCenter` = 0.0 | |
| SC-002 | the running branch | `test` → the E2E's copy assertions | |
| SC-003 | `views.py` | `test` → the three `ReadingViewTests` copy tests | |
| SC-004 | `offline-render.js` | `test` → the saved-render parity suite (push step) | accepted gap until then: the browser suite is deferred |
| SC-005 | whole app | `test` → `multimedia.web` suite | |

**Verification split**: 12 test · 4 inspection · 0 manual

## Complexity Tracking

| Violation | Why needed | Simpler alternative rejected because |
| --- | --- | --- |
| The copy is duplicated in `offline-render.js` (six strings per section) | the saved renderer rebuilds a page from the cached **home** shell, so its blocks belong to the Bible; it has no server context to ask | fetching the destination page's markup for its labels would put a network round-trip on the offline path |
| `window.shellListEmpty` is a global | `entries.js` and `offline-render.js` load around `reading.js` and must type the same block | a third script file would add a fetch to every reading page for eight lines |

## Project Structure

### Documentation

```
specs/129-sidebar-empty-states/
  spec.md  plan.md  research.md  data-model.md  quickstart.md  tasks.md
  contracts/  checklists/  preview/
```

### Source

```
multimedia/web/templates/reading/base.html      the two blocks (markup + glyphs + copy attributes)
multimedia/web/reading/views.py                 PANEL_META / CH_META copy, and _shell's context keys
static/styles/design/components.css             .listempty; position: relative on both panes
static/web/reading.js                           paintListEmpty, boot paint, filter typing, swap sync
static/web/entries.js                           the deleted-last-row case
static/web/offline-render.js                    LIST_EMPTY, labelListEmpty, paintListEmptyStates
multimedia/web/tests.py                         four markup tests
tests/e2e/test_reading.py                       one E2E test with the centring measurement
specs/129-sidebar-empty-states/preview/probe_empty_states.py   the measurement probe
```

### Structure Decision

No new file on the reading pages: the block is markup in the shell they already render, its styles are in
the shared component sheet, and its behaviour is in `reading.js`, which owns both lists. The probe is a
slice artefact under `preview/`, not app code.
