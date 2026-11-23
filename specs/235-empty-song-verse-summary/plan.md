# Implementation Plan: An empty song names itself in the Verses section

**Spec**: `specs/235-empty-song-verse-summary/spec.md`
**Branch**: `fix/235-empty-song-verse-summary`
**Bump**: `patch` (1.36.19 → 1.36.21; spec 234 took 1.36.20 on develop while this slice was open)
**Preview**: `specs/235-empty-song-verse-summary/preview/` — accepted at Gate 1 2026-11-24

## Technical Context

| Field | Value |
| --- | --- |
| Language / version | Python 3.12, Django 4.0; vanilla ES5-style JS, CSS with `:has()` and `fr` tracks |
| Primary dependencies | Django forms/templates, Playwright E2E, no new package |
| Storage | PostgreSQL; no schema change, no migration |
| Testing | Django `TestCase` for the server fragment; Playwright `StaticLiveServerTestCase` for the modal |
| Target platform | The product's reading/Tata Ibadah shell, dark and light themes |
| Project type | Server-rendered Django app with progressive vanilla JS |
| Performance goals | No new request, no new animation phase; one frame for the empty ↔ populated swap |
| Constraints | Spec 210's reveal, tile grid, mute and save refusals stay byte-identical in behaviour; repo rules in `docs/PROCESS.md` |
| Scale / scope | Three product files, two test files, capability delta in `reading/R30` and `reading/R48` |

## Constitution Check

| Principle | Status | Note |
| --- | --- | --- |
| — | `n/a` | No `CONSTITUTION.md` in the repo; SDD-01 makes it optional and never auto-created. |

Re-checked after Phase 1: `n/a` — still no constitution; no violation to justify.

## Phase 0 — Research

See `research.md`. **Unknowns remaining: 0.** Five decisions, all with provenance in the
accepted preview or the repo's own code; no owner question needed after Gate 1.

## Phase 1 — Design

- `data-model.md` — no entities change; one new DOM state (`data-empty`) with a four-row matrix.
- `contracts/` — `none`; the `data-empty` attribute is an internal DOM contract, documented in the data model.
- `quickstart.md` — targeted test commands and the six-step manual walk.

## Traceability

| Requirement | Component / file | Verified by | Notes |
| --- | --- | --- | --- |
| US1/AC1, FR-001 | `_entry_form.html`, `entries.js`, `components.css` | `test` → `tests/e2e/test_entries.py::EntryModalE2ETests::test_an_empty_song_shows_only_the_verse_summary` | Add: pick empty song, label + panel visible, only the summary line |
| US1/AC2, FR-002 | `components.css` | `test` → same E2E test | body rows `display:none`, summary bottom rule `0px` |
| US1/AC3, FR-002 | `components.css` | `test` → same E2E test | zero visible checkboxes, tiles, helper, All/Clear |
| US1/AC4, FR-003 | `_entry_form.html`, `entries.py` | `test` → `multimedia/web/tests.py::ServiceEntryViewTests::test_an_edit_form_for_a_verse_less_song_states_it_in_the_markup` | extend to assert not hidden and `data-empty="true"` |
| US1/AC5, FR-005 | `reading/entries.py` (unchanged) | `test` → updated E2E + `multimedia/tatib/tests.py::test_a_song_entry_with_no_verses_names_the_song` | refusal wording byte-identical |
| US2/AC1, FR-004 | `entries.js` | `test` → new E2E test (swap empty → populated) | no stale `data-empty`, verse 1 ticked |
| US2/AC2–3, FR-004 | `entries.js`, `components.css` (unchanged behaviour) | `test` → existing `test_the_song_pick_searches_and_the_verses_start_all_checked`, `test_single_verse_song_keeps_checked_verse_and_disables_picker` | full picker and one-verse mute stay green |
| FR-006 | all other surfaces | `inspection` — only the three listed product files change | song stage, service row, projector, OBS dock untouched |
| SC-001 | E2E new test | `test` — summary-only state in Add and Edit | |
| SC-002 | E2E new test | `test` — zero visible controls | |
| SC-003 | existing E2E tests | `test` — no song still 0 px; full picker still visible | |
| FR-004 motion | `entries.js` reveal branch | `inspection` — the 200 ms `data-settled` path is byte-identical | no new phase added |

**Verification split**: 9 test · 2 inspection · 0 manual.

## Complexity Tracking

| Violation | Why needed | Simpler alternative rejected because |
| --- | --- | --- |
| — | — | — |

## Project Structure

### Documentation (this slice)

```
specs/235-empty-song-verse-summary/
├── spec.md, research.md, data-model.md, plan.md, quickstart.md
├── checklists/requirements.md
├── contracts/none.md
├── preview/{template.html,build.py,index.html,README.md}
├── tasks.md, analysis.md, converge.md, fold.md   (later stages)
```

### Product files to change

```
multimedia/web/templates/reading/_entry_form.html   (panel hidden only with no song; data-empty)
static/web/entries.js                               (verseSummary hides only for no song; sets data-empty)
static/styles/design/components.css                 (empty-state rules)
tests/e2e/test_entries.py                           (updated + new E2E pins)
multimedia/web/tests.py                             (server fragment pin)
docs/spec/reading.md, VERSION, CHANGELOG.md, backlog/board.md, backlog/items/ITEM-250-*.md
```

## Plan exit gate

- Requirement coverage: FR-001…006 and SC-001…003 each appear above — **pass**.
- Entity coverage: no new entity; the DOM state matrix is in `data-model.md` — **pass**.
- Interface coverage: `contracts/none.md` states none with the reason — **pass**.
- Decision provenance: D001–D005 each carry a rationale and a source — **pass**.
- Constitution conformance: `n/a`, no constitution — **pass**.
- Zero unknowns: `research.md` ends at none — **pass**.
- Verification declared: 9 test · 2 inspection · 0 manual — **pass**.
- `quickstart.md` commands are runnable — **pass** (targeted suites, no new setup).
