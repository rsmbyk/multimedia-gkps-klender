# Implementation Plan: Project button on the song and Bible pages

**Spec**: `specs/193-reading-project-button/spec.md` (Accepted, Gate 1 2026-11-14)
**Branch**: `feat/193-reading-project-button`
**Bump**: `minor` — a new user-facing capability (a new control on two reading pages and a guard on the projector's Go To)
**Preview**: `specs/193-reading-project-button/preview/index.html` (static)

## Technical Context

| Field | Value |
| --- | --- |
| Language / version | Python 3.12, Django 4.0; vanilla JS (no framework) |
| Primary dependencies | none added |
| Storage | none touched |
| Testing | Django `manage.py test` (targeted), Playwright (Python) E2E via `LiveServerTestCase` |
| Target platform | Server-rendered reading pages; the projector window (spec 141's named `gkps-projector`) |
| Project type | Django templates + vanilla JS slices |
| Performance goals | none — one click writes state and opens a window |
| Constraints | display.js's shell-swap rule (no held nodes); `reading/R14`'s narrow-width rule; `dock/R1`'s Go To contracts untouched |
| Scale / scope | 2 templates, 1 new block in base.html, 2 JS modules touched, 1 CSS selector, 1 new E2E module |

## Constitution Check

No `CONSTITUTION.md` exists in this repo — check skipped (SDD-01: the constitution is optional and never auto-created).

## Phase 0 — Research

See `research.md`. **Unknowns remaining: 0.**

## Phase 1 — Design

- `data-model.md` — no model changes; the pointer shapes restated
- `contracts/` — none (no new external interface)
- `quickstart.md` — worktree server + targeted test commands

## Design Notes

1. **Song page** (`song.html`): a new `{% block read_actions %}` draws the `.read__project` group
   with one `data-project-goto` button carrying `data-goto-song="{{ song.pk }}"`, gated
   `{% if verse_rows %}` (FR-007). Anatomy and icon copied from `tatib.html`.
2. **Bible page** (`bible.html` + `base.html`): `base.html`'s `read__row` gains an empty
   `{% block read_row_actions %}` after the `.read__lang` conditional; `bible.html` fills it with
   the group gated `{% if read_state == 'on' %}`, the button carrying
   `data-goto-book="{{ book_id }}" data-goto-chapter="{{ read_no }}"
   data-goto-edition="{% if read_lang == 'sim' %}SIM{% else %}TB{% endif %}"` (FR-002's placement).
3. **`display.js`** (FR-003/004/005, A8): a delegated `click` branch for `[data-project-goto]` —
   build the pointer from the data attributes; if `state.goto` already opens that content
   (research D4) and `on` is true, leave the pointer untouched; if it is open but hidden, call
   `resume()`; otherwise `goTo(pointer)`. Then `openProjector(dataset.projectorUrl || '/projector')`
   in every case (the window act is unconditional, FR-005). No new verbs, no new state fields.
4. **`projector.js`** (FR-008): a module-level `appliedGoto`; `applyGoto()` returns before fetching
   when the incoming pointer deep-equals `appliedGoto`; `appliedGoto` is set when a detour is
   applied and cleared when the pointer ends (`leaveDetour`/Back, `goto: null`), so Back re-arms
   the fetch. Boot paints normally (`appliedGoto` starts empty).
5. **`components.css`**: the ≤720px rule at `:3202` gains `[data-project-goto]` (FR-007).
6. **Offline renderer unchanged** (`offline-render.js` draws no project controls today — A4).
7. **Tests**: `ReadingViewTests` render pins (button present with the right data attributes on hymn
   and ordinary songs and on a chapter page; absent on a verse-less song and a book landing page;
   `offline-render` parity untouched); new `tests/e2e/test_reading_project.py` — pointer write,
   projector paints the detour, window opened once and reused, repeat click inert (route count),
   in-page navigation keeps the control alive, Back returns to the service.

## Traceability

| Requirement | Component / file | Verified by | Notes |
| --- | --- | --- | --- |
| FR-001 (song page control) | `song.html`, `tatib.html` (anatomy source) | `test` → `multimedia/web/tests.py::ReadingViewTests::test_song_page_draws_project_control` | hymn and ordinary |
| FR-002 (chapter page control, placement) | `bible.html`, `base.html` | `test` → `multimedia/web/tests.py::ReadingViewTests::test_bible_chapter_draws_project_control_beside_the_switch` + `inspection` (right of the switch in the title row) | `read_row_actions` block |
| FR-003 (song pointer, no reset) | `display.js` | `test` → `tests/e2e/test_reading_project.py::test_clicking_project_writes_the_song_pointer` / `::test_repeat_click_keeps_the_detours_place` | |
| FR-004 (chapter pointer, verse 1, edition) | `display.js`, `bible.html` | `test` → `tests/e2e/test_reading_project.py::test_clicking_project_writes_the_chapter_pointer` / `::test_sim_page_projects_sim` | verse 1 per Clarify |
| FR-005 (window act, never Stop) | `display.js`, both templates | `test` → `tests/e2e/test_reading_project.py::test_one_click_opens_the_projector_window_once` | popup-blocked → `inspection` |
| FR-006 (composes with dock/R1) | `display.js` | `test` → `tests/e2e/test_reading_project.py::test_back_returns_to_the_service` + `inspection` against `dock/R1` | service preserved underneath |
| FR-007 (not drawn: landing, verse-less, saved, ≤720px) | `bible.html`, `song.html`, `components.css:3202`, `offline-render.js` (unchanged) | `test` → `ReadingViewTests::test_project_control_is_absent_where_it_has_nothing_to_say` + saved-parity suite; `inspection` (≤720px) | |
| FR-008 (projector fetches only a different Go To) | `projector.js` | `test` → `tests/e2e/test_reading_project.py::test_repeat_click_makes_no_second_fetch` (route count) | `projector/R1` modified |
| SC-001–SC-006 | the rows above | mixed | SC-005 by inspection |
| US1/AC5, US2/AC4 (survives the stage swap; layout) | `display.js` delegation, `bible.html` | `test` → `tests/e2e/test_reading_project.py::test_the_control_survives_in_page_navigation` + `inspection` | |
| Owner's live review | worktree server | `manual` — click through song and chapter pages with the projector window | per the owner's review habit |

**Verification split**: 7 test · 6 inspection · 1 manual

## Complexity Tracking

| Violation | Why needed | Simpler alternative rejected because |
| --- | --- | --- |
| | | |

## Project Structure (changes)

```
multimedia/web/templates/reading/base.html        (+ read_row_actions block)
multimedia/web/templates/reading/song.html        (+ read_actions block)
multimedia/web/templates/reading/bible.html       (+ read_row_actions block)
static/web/display.js                             (+ data-project-goto branch)
static/web/projector.js                           (+ appliedGoto guard)
static/styles/design/components.css               (:3202 selector gains [data-project-goto])
multimedia/web/tests.py                           (+ render pins)
tests/e2e/test_reading_project.py                 (new)
specs/193-reading-project-button/                 (spec pack)
backlog/board.md, backlog/items/ITEM-197-…md      (card moves)
```
