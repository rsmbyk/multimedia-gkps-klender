# Implementation Plan: Verse reference notice sits in the action row

**Spec**: `specs/232-verse-reference-notice/spec.md`
**Branch**: `feat/232-verse-reference-notice`
**Bump**: `patch` — 1.36.17 → 1.36.18 (re-check against `develop` at merge)
**Preview**: `specs/232-verse-reference-notice/preview/`

## Technical Context

| Field | Value |
| --- | --- |
| Language / version | Python 3.12, Django 4.0, vanilla CSS/HTML |
| Primary dependencies | Django, Playwright (Python) for user-visible acceptance |
| Storage | PostgreSQL; no model or data change in this slice |
| Testing | Django test runner; Playwright E2E via `StaticLiveServerTestCase` |
| Target platform | Desktop and narrow browser viewports, light and dark themes |
| Project type | Server-rendered editor fragment fetched into one shared `<dialog>` |
| Performance goals | None; no new work at runtime |
| Constraints | One fragment, one CSS group, one scoped disabled-state rule; endpoints untouched |
| Scale / scope | Referenced verse editors only; other editors and the confirmation dialog stay byte-identical |

## Constitution Check

| Principle | Status | Note |
| --- | --- | --- |
| none | pass | No `CONSTITUTION.md` exists at the base commit; there is no project principle to check. |

Re-checked after Phase 1: pass — no new component, dependency, endpoint or runtime behaviour.

## Phase 0 — Research

See `research.md`. **Unknowns remaining: 0.**

## Phase 1 — Design

- `data-model.md` — reuses `named_service_count`; no entity added.
- `contracts/none.md` — no HTTP, model, script or event interface change.
- `quickstart.md` — targeted E2E command and the preview build command.

## Traceability

| Requirement | Component / file | Verified by | Notes |
| --- | --- | --- | --- |
| FR-001 | `multimedia/web/templates/reading/_editor_form.html:73-82` | `test` → `tests/e2e/test_verse_reference_notice.py::VerseReferenceNoticeE2ETests::test_note_leads_the_action_row` | first child of the row, count text |
| FR-002 | `static/styles/design/components.css` `.editor__refnote` | `test` → `...::test_note_type_and_glyph_use_existing_tokens` | 15px glyph, 12px/18px, 700 numeral |
| FR-003 | `static/styles/design/components.css` `.editor__refnote` | `test` → `...::test_desktop_row_keeps_its_height` | 38px row, 18px note, centred |
| FR-004 | `static/styles/design/components.css` `.editor__delete:disabled` | `test` → `...::test_disabled_delete_is_neutral` | opacity 1, rail-bg, divider, head-ink |
| FR-005 | `static/styles/design/components.css` narrow media query | `test` → `...::test_narrow_row_wraps_the_note_above_the_buttons` | 420px, 352×18, 66px row, no overflow |
| FR-006 | template branch + CSS selector scope | `test` → `...::test_unreferenced_editor_has_no_note` | plus `inspection` of selector scopes |
| FR-007 | `multimedia/web/reading/views.py:176-186`, `verses.py:116-129` | `test` → `...::test_delete_is_still_refused` | count and endpoint unchanged |
| FR-008 | `_editor_form.html` `aria-describedby` | `test` → `...::test_button_is_described_by_the_note` | id/for pair resolves |
| SC-001 | note-leads test | `test` | reason beside the button |
| SC-002 | desktop-row test | `test` | 38px at 840px |
| SC-003 | neutral-button test | `test` | computed styles |
| SC-004 | count tests, one and three services | `test` → `...::test_count_tracks_the_guard` | fixture counts |
| SC-005 | narrow test | `test` | 420×900 |
| SC-006 | unreferenced + non-verse tests | `test` + `inspection` | base boxes unchanged |
| US1/AC1 | note-leads test | `test` | order of row children |
| US1/AC2 | count test | `test` | singular and plural |
| US1/AC3 | neutral-button test | `test` | disabled styling |
| US1/AC4 | unreferenced test | `test` | no note, enabled delete |
| US1/AC5 | other-editors test | `test` + `inspection` | byte-identical rows |
| US2/AC1 | narrow test | `test` | note 352×18, row 66px |
| US2/AC2 | narrow-button test | `test` → `...::test_narrow_buttons_keep_their_row` | right aligned, 38px |
| US2/AC3 | theme test | `test` → `...::test_both_themes_use_existing_tokens` | light and dark computed values |

**Verification split**: 23 test · 3 inspection · 0 manual

## Complexity Tracking

| Violation | Why needed | Simpler alternative rejected because |
| --- | --- | --- |
| | | |

## Project Structure

### Documentation

```
specs/232-verse-reference-notice/
  spec.md  plan.md  research.md  data-model.md  quickstart.md  tasks.md  analysis.md
  contracts/  checklists/  preview/
```

### Source

```
multimedia/web/templates/reading/_editor_form.html   the referenced-verse note
static/styles/design/components.css                  note styles + scoped neutral disabled button + wrap
tests/e2e/test_verse_reference_notice.py             new E2E for both stories
```

### Structure Decision

The note is emitted by the server fragment because `openEditor()` in `songs_verse.js` fetches that
fragment into `#editorContent`; a script-side rewrite would be lost on every reopen. The CSS stays beside
the other `.editor__actions` rules, and the neutral disabled rule is scoped to `.editor__delete` so the
shared `.editor__danger:disabled` used by confirmation dialogs is untouched.
