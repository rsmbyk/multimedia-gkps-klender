# Implementation Plan: A passage cue carries its current and end verse

**Spec**: `specs/229-cue-verse-counter/spec.md`
**Branch**: `feat/229-cue-verse-counter`
**Bump**: `patch` — 1.36.14 → 1.36.15
**Preview**: `specs/229-cue-verse-counter/preview/`

## Technical Context

| Field | Value |
| --- | --- |
| Language / version | Python 3.12, Django 4.0, vanilla JS |
| Primary dependencies | Django, Django REST Framework, Playwright (Python) for E2E |
| Storage | PostgreSQL; no model or migration change in this slice |
| Testing | Django test runner; Playwright E2E via `StaticLiveServerTestCase` |
| Target platform | Browser projector page, all viewports |
| Project type | Server-rendered projector payload + browser-side cue renderer |
| Performance goals | None; two fields added to an existing payload, one DOM span per cue render |
| Constraints | No new endpoint, state field, CSS rule, token or control; only scripture cues change |
| Scale / scope | `_scripture_screens()`, the scripture entry dict, two cue renderers, three test files |

## Constitution Check

| Principle | Status | Note |
| --- | --- | --- |
| none | pass | No `CONSTITUTION.md` exists at the base commit; there is no project principle to check. |

Re-checked after Phase 1: pass — the payload gains two derived read-only fields and the cue gains
one text span; no dependency, interface or persisted state is added.

## Phase 0 — Research

See `research.md`. **Unknowns remaining: 0.**

## Phase 1 — Design

- `data-model.md` — projector entry/screen fields and the existing Go To detour; no DB changes.
- `contracts/` — `none`; the two new payload fields are additive and no channel message changes.
- `quickstart.md` — throwaway-DB test commands, the E2E lanes and the static preview URL.

## Traceability

| Requirement | Component / file | Verified by | Notes |
| --- | --- | --- | --- |
| FR-001 | `multimedia/web/reading/views.py:1707` `_scripture_screens()`, `:1782` scripture branch | `test` → `multimedia.web.tests.ServiceProjectorTests::test_a_scripture_screen_carries_its_verse_and_the_entry_its_bounds` | payload fields only, no browser |
| FR-002 | `static/web/projector.js:934` `renderCue()` | `test` → `tests.e2e.test_projector.ProjectorE2ETests::test_the_service_passage_cue_counts_the_current_and_end_verse` | `3/5` after the reference, before the flip |
| FR-003 | `static/web/projector.js` `renderCue()` | `test` → the same case, arrow steps 1→2 | current moves, end holds |
| FR-004 | `static/web/projector.js:1694` `renderDetourCue()` | `test` → `tests.e2e.test_goto_shared_state.GotoSharedStateE2ETests::test_the_go_to_cue_counts_the_verse_and_the_chapter_length` | end from `detour.editions` |
| FR-005 | `static/web/projector.js` `renderDetourCue()`, `projector-library.js` (unchanged) | `test` → the Go To case plus `tests.e2e.test_dock_goto` | step and chapter crossing; one shared state |
| FR-006 | both cue renderers | `test` → `tests.e2e.test_projector.ProjectorE2ETests::test_non_scripture_cues_carry_no_verse_counter` and `::test_a_single_verse_passage_counts_one_of_one` | song/text/break/media and `n/n` |
| FR-007 | `static/styles/design/projector.css` (unchanged), `static/web/projector.js` | `inspection` — `git diff` shows no CSS/token change and the flip's handler is untouched | geometry pinned by SC-004 |
| SC-001 | E2E service passage case | `test` | `3/5 → 4/5 → 5/5`, reference unchanged |
| SC-002 | E2E Go To case | `test` | `1/3 → 2/3 → 3/3`, end changes at the crossing |
| SC-003 | E2E non-scripture case | `test` | `.cue-verse` count 0; no `1/0` on an empty chapter |
| SC-004 | existing geometry/flip tests | `test` → `tests.e2e.test_projector.py` cue geometry and flip cases | 24px band and centre alignment unchanged |
| US1/AC1 | service passage at verse 3 | `test` | same as FR-002 |
| US1/AC2 | stepping to verses 4 and 5 | `test` | same as FR-003 |
| US1/AC3 | single-verse passage | `test` | `3/3` |
| US1/AC4 | translation missing on screen | `inspection` — `entry.verse_end` is read from the entry, never from `translations` | no header to parse |
| US1/AC5 | song, text, break, media | `test` | same as FR-006 |
| US2/AC1 | Go To chapter 5 first verse | `test` | same as FR-004 |
| US2/AC2 | Go To verse step | `test` | same as FR-005 |
| US2/AC3 | chapter crossing | `test` | new end number |
| US2/AC4 | edition flip and dock/reading-started Go To | `inspection` — the counter is derived from `detour` at every render; the dock writes the same `goto` field | covered by existing shared-state tests |
| US2/AC5 | song Go To | `test` | same as FR-006 |

**Verification split**: 20 test · 3 inspection · 0 manual

## Complexity Tracking

| Violation | Why needed | Simpler alternative rejected because |
| --- | --- | --- |
| | | |

## Project Structure

### Documentation

```
specs/229-cue-verse-counter/
  spec.md  plan.md  research.md  data-model.md  quickstart.md  tasks.md
  contracts/  checklists/  preview/
```

### Source

```
multimedia/web/reading/views.py     verse on a scripture screen, bounds on its entry
static/web/projector.js             .cue-verse in renderCue() and renderDetourCue()
multimedia/web/tests.py             one payload test
tests/e2e/test_projector.py         service cue cases
tests/e2e/test_goto_shared_state.py Go To cue case
docs/spec/projector.md              R16 folded
```

### Structure Decision

The payload fields are added where the payload is already built, not in the template: the projector
sends JSON to JS for both service and Go To. The tests extend the modules that already own each
fixture; no new JS runner or E2E module is introduced.
