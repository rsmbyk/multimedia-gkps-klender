# Implementation Plan: Keep a chapter's verse text when the reading page updates in place

**Spec**: `specs/124-bible-edition-block-identity/spec.md`
**Branch**: `fix/124-bible-edition-block-identity`
**Bump**: `patch`
**Preview**: `n/a — the spec declares no visible change (UI/UX: n/a), so there is nothing to preview`

## Technical Context

| Field | Value |
| --- | --- |
| Language / version | vanilla browser JavaScript (ES5 style, no build step) in `static/web/reading.js`; Python 3.12 / Django 4.0 unchanged |
| Primary dependencies | none added — one identity function in an existing script |
| Storage | none — no model, migration, or saved payload |
| Testing | Playwright (Python) E2E via `StaticLiveServerTestCase`, Django test runner |
| Target platform | browsers served by the reading shell (`/bible/<book>/<chapter>/`), desktop viewport |
| Project type | server-rendered Django templates with vanilla JS; the reading shell swaps the stage in place |
| Performance goals | none — the identity lookup is unchanged in cost; no extra request |
| Constraints | the stage markup is emitted by two renderers (`multimedia/web/templates/reading/bible.html` and `static/web/offline-render.js`); the reconciler's other keyed nodes (book rows, chapter rows, entries, songs) must keep their identity |
| Scale / scope | one attribute order in one function, plus one browser test |

## Constitution Check

| Principle | Status | Note |
| --- | --- | --- |
| n/a | n/a | no `CONSTITUTION.md` exists in this repo (checked 2026-10-24) — nothing to check against |

Re-checked after Phase 1: n/a — still no constitution file.

## Phase 0 — Research

See `research.md`. **Unknowns remaining: 0.**

## Phase 1 — Design

- `data-model.md` — `n/a — no entity, field, relationship, migration or payload changes`
- `contracts/` — `none — the change is inside a browser script; it exposes no request, response, event or function contract`
- `quickstart.md` — how to serve the branch and what to verify by hand

## Traceability

| Requirement | Component / file | Verified by | Notes |
| --- | --- | --- | --- |
| FR-001 | `static/web/reading.js` (`nodeIdentity`, the key the in-place reconciler matches nodes by) | `test` → `tests/e2e/test_reading.py::ReadingE2ETests::test_same_name_edition_blocks_keep_the_verse_text` | after the move: two `#readBody .read__ed` blocks, TB visible, SIM hidden |
| FR-002 | same function | `test` → the same test's chapter-move leg | chapter 2's verses visible; both blocks still mounted |
| FR-003 | same function | `test` → the same test's switch leg | SIM text, then TB text, each visible in turn |
| FR-004 | `multimedia/web/templates/reading/bible.html`, `static/web/offline-render.js` (both emit `data-ed`; untouched) | `test` → the existing edition, navigation, targeted-update and saved-parity classes, re-run unchanged | the fix relies on `data-ed` being present in both renderers |
| SC-001 | `static/web/reading.js` | `test` → the new test's opening leg | visible stage text is non-empty after home → Alkitab → Rut → chapter 1 |
| SC-002 | `static/web/reading.js` | `test` → the new test's move and switch legs | keeps text and the selected translation |
| SC-003 | untouched files | `test` → `test_shell_navigates_in_place`, `test_bible_sidebar_labels_follow_edition_and_reset_on_refresh`, `test_sim_codes_titles_labels_and_fallback_follow_selected_edition`, `test_bible_edition_survives_menu_switches_and_history`, `test_the_translation_switch_fills_the_hovered_option`, `tests.e2e.test_targeted_reading_updates`, `tests.e2e.test_navigation_freshness`, `tests.e2e.test_saved_render_parity` | all re-run unchanged |
| US1/AC1–AC3 | `static/web/reading.js` | `test` → the new test | one test covers opening, moving, switching |
| US2/AC1–AC2 | untouched files | `test` → the existing classes above | distinct-name books and direct loads |
| US2/AC3 | `static/web/offline-render.js` (`edition()`) | `inspection` — the saved renderer emits `class="read__ed" data-ed="tb|sim"`, so the corrected identity reaches it; the saved-parity class is re-run as the guard | no code change expected; no same-name offline fixture |

**Verification split**: 9 test · 1 inspection · 0 manual

## Complexity Tracking

| Violation | Why needed | Simpler alternative rejected because |
| --- | --- | --- |
| none | — | — |

## Project Structure

### Documentation

```
specs/124-bible-edition-block-identity/
  spec.md  plan.md  research.md  data-model.md  quickstart.md  tasks.md  analysis.md
  contracts/  checklists/
```

### Source

```
static/web/reading.js          # nodeIdentity: edition before label
tests/e2e/test_reading.py      # one new browser test with a same-name book fixture
backlog/items/ITEM-125-bible-edition-block-identity.md
backlog/board.md               # the card's row
VERSION  CHANGELOG.md          # patch bump
```

### Structure Decision

Everything stays inside the reading shell: the script that already owns the in-place update, the E2E
module that already owns the Bible edition pins (`tests/e2e/test_reading.py`), and the board's existing
card format. No new module, template, asset, or CSS.
