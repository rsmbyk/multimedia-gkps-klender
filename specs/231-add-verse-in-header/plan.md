# Plan: Add verse sits beside Project in the song header

**Spec**: `specs/231-add-verse-in-header/spec.md`
**Branch**: `fix/231-add-verse-top`
**Bump**: `patch` — 1.36.16 → 1.36.17, applied in the pre-merge delivery commit
**Preview**: `specs/231-add-verse-in-header/preview/README.md`

## Technical Context

| Field | Value |
| --- | --- |
| Language / version | Python 3.12; Django templates; CSS with `color-mix()` |
| Primary dependencies | Django 4.0; Playwright (Python) for E2E; no new dependency |
| Storage | PostgreSQL via the compose DB; no schema change |
| Testing | Django template tests beside the app; Playwright E2E in `tests/e2e/` |
| Target platform | Browsers served by the public reading shell |
| Project type | Server-rendered templates plus vanilla JS |
| Performance goals | No new request; one fewer positioned element on a song page |
| Constraints | `songs_verse.js` reads the first `[data-add-verse]`; each state must carry one |
| Scale / scope | One template block moved, one scoped CSS rule, one E2E module, one capability requirement |

## Constitution Check

| Principle | Status | Note |
| --- | --- | --- |
| `CONSTITUTION.md` exists | pass | Not present in this repo (SDD-01) |
| Dependency-free implementation | pass | Template and CSS only |
| Self-hosted assets | pass | No asset added |
| Visible change needs a preview | pass | Live preview on 8772 with measured before/after boxes |
| Repo process is binding | pass | Slice, card, gates and Fold followed |

Re-checked after Phase 1: **pass** — no violations, no Complexity Tracking entries.

## Phase 0 — Research

See `research.md`. **Unknowns remaining: 0.**

## Phase 1 — Design

- `data-model.md` — no entities; the placement derives from `verse_rows` and `can_edit_verses`
- `contracts/` — `none`, recorded in `contracts/none.md`
- `quickstart.md` — live preview, focused test command and browser probe

## Traceability

| Requirement | Component / file | Verified by | Notes |
| --- | --- | --- | --- |
| US1/AC1 | `tests/e2e/test_add_verse_header.py` | `test` → `test_add_verse_sits_left_of_project_in_header` | 111×34 then 96×34, 8px gap |
| US1/AC2 | same | `test` → `test_header_add_verse_opens_editor` | `#editorModal` title `New verse` |
| US1/AC3 | `multimedia/web/reading/test_verse_add_gate.py` | `test` → `test_song_with_verses_keeps_single_header_add_control` | no `.verse-add` row |
| US1/AC4 | live preview at 560px | `manual` — resize `/songs/1880/`, read the header | Add verse stays, Project hidden |
| US1/AC5 | `multimedia/web/reading/test_verse_add_gate.py` | `test` → `test_hymn_song_draws_no_add_verse_but_keeps_project` | read-only path unchanged |
| US2/AC1 | same module | `test` → `test_empty_song_has_no_header_actions` | header holds only the eyebrow |
| US2/AC2 | same module | `test` → `test_empty_song_has_one_add_verse_button` | existing spec-224 pin |
| US2/AC3 | same module | `test` → `test_empty_song_has_no_after_verse_row` | deleted-only verse |
| FR-001 | `reading/song.html` | `inspection` — control inside `.read__project`, before Project, gated on both flags | |
| FR-002 | `reading/song.html` | `test` → `test_song_with_verses_keeps_single_header_add_control` | |
| FR-003 | `reading/song.html` | `test` → `test_empty_song_has_no_header_actions` | |
| FR-004 | `static/web/songs_verse.js` | `test` → `test_header_add_verse_opens_editor` | one node, song id intact |
| FR-005 | `static/styles/design/components.css` | `inspection` — scoped 34px height rule beside `.verse-add__btn` | |
| FR-006 | whole tree | `inspection` — diff touches only `song.html` and `components.css` | |
| FR-007 | `docs/spec/reading.md` | `inspection` — `R56` block at Fold | |
| SC-001 | `preview/README.md` + E2E | `inspection` — probe boxes x=1157 / x=1276 | |
| SC-002 | E2E | `inspection` — `.verse-add` resolves to null | |
| SC-003 | template tests | `test` → both count assertions | |
| SC-004 | template test | `test` → `test_empty_song_has_one_add_verse_button` | |
| SC-005 | E2E | `test` → `test_header_add_verse_opens_editor` | |
| SC-006 | template test | `test` → `test_hymn_song_draws_no_add_verse_but_keeps_project` | |

**Verification split**: 14 test · 6 inspection · 1 manual

## Complexity Tracking

| Violation | Why needed | Simpler alternative rejected because |
| --- | --- | --- |
| — | — | — |

## Project Structure

### Documentation

```
specs/231-add-verse-in-header/
  spec.md  plan.md  research.md  data-model.md  quickstart.md  tasks.md
  contracts/none.md  checklists/requirements.md  preview/README.md
  analysis.md (here)  converge.md / fold.md (written by those stages)
```

### Source

```
multimedia/web/templates/reading/song.html   control moved into read_actions
static/styles/design/components.css          one scoped height rule
multimedia/web/reading/test_verse_add_gate.py placement pins updated
tests/e2e/test_add_verse_header.py           new (Playwright acceptance)
docs/spec/reading.md                         +R56 at Fold
backlog/board.md + backlog/items/ITEM-246    card and row
```

### Structure Decision

The header action group already owns page-level controls, so the add control joins it rather than
getting a second zone. Browser E2E is used where the observable behaviour is a box or a dialog;
the fast template tests cover the render gates because that is where the repo's TDD custom puts
application rules.
