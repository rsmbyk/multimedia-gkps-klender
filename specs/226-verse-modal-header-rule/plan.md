# Implementation Plan: Verse modal header draws one rule

**Spec**: `specs/226-verse-modal-header-rule/spec.md`
**Branch**: `fix/226-verse-modal-header-rule`
**Bump**: `patch` — 1.36.11 → 1.36.12
**Preview**: `specs/226-verse-modal-header-rule/preview/`

## Technical Context

| Field | Value |
| --- | --- |
| Language / version | Python 3.12, Django 4.0, vanilla CSS/JS |
| Primary dependencies | Django, Django REST Framework, Playwright (Python) for E2E |
| Storage | PostgreSQL; no data changes in this slice |
| Testing | Django test runner; Playwright E2E via `StaticLiveServerTestCase` |
| Target platform | Desktop and narrow browser viewports, light and dark themes |
| Project type | Server-rendered templates with a fetched editor dialog |
| Performance goals | None; no new work at runtime |
| Constraints | One CSS rule group; no template, script, endpoint or model change |
| Scale / scope | One shared dialog's large form marker; songbook/song/Tata Ibadah editors untouched |

## Constitution Check

| Principle | Status | Note |
| --- | --- | --- |
| none | pass | No `CONSTITUTION.md` exists at the base commit; there is no project principle to check. |

Re-checked after Phase 1: pass — the design introduces no new component, dependency or runtime behaviour.

## Phase 0 — Research

See `research.md`. **Unknowns remaining: 0.**

## Phase 1 — Design

- `data-model.md` — `n/a — no entities; the change is one CSS state rule.`
- `contracts/` — `none` — no HTTP, model, script or event interface changes.
- `quickstart.md` — how to run the targeted E2E and the live probe.

## Traceability

| Requirement | Component / file | Verified by | Notes |
| --- | --- | --- | --- |
| FR-001 | `static/styles/design/components.css:541` | `test` → `tests/e2e/test_verse_modal_header.py::VerseModalHeaderE2ETests::test_new_verse_header_has_one_rule` | title `borderBottomWidth === '0px'` |
| FR-002 | `static/styles/design/components.css:541` | `test` → `...::test_edit_verse_header_has_one_rule` | head only ruled descendant, both dialogs |
| FR-003 | `static/styles/design/components.css:541`, `:539` | `test` → `...::test_header_gap_matches_the_other_editors` | 21px top, 16–17px below text, x=289, 21px/640 |
| FR-004 | `static/styles/design/components.css:541` | `inspection` — the changed selectors both require `[data-editor-size="large"]`; no other file changes | loading skeleton has no such marker |
| FR-005 | `static/styles/design/components.css:541` | `test` → `...::test_single_rule_follows_a_narrow_dialog` | 390×844, head width `100vw - 32px` |
| FR-006 | `static/styles/design/components.css:539`, `:545` | `test` → `...::test_header_gap_matches_the_other_editors` | divider-to-label stays 30px |
| SC-001 | E2E new/edit tests | `test` | one ruled descendant in the header |
| SC-002 | E2E narrow test | `test` | head rule width tracks the dialog |
| SC-003 | E2E gap test + inspection of non-verse editors | `test` + `inspection` | typography and field boxes unchanged |
| US1/AC1 | `static/styles/design/components.css:541` | `test` → `...::test_new_verse_header_has_one_rule` | new verse, no ruled descendants |
| US1/AC2 | `static/styles/design/components.css:541` | `test` → `...::test_edit_verse_header_has_one_rule` | edit verse, no ruled descendants |
| US1/AC3 | `static/styles/design/components.css:541` | `test` → `...::test_new_verse_header_has_one_rule` | title 0px, head 1px |
| US1/AC4 | `static/styles/design/components.css:541` | `test` → `...::test_header_gap_matches_the_other_editors` | inset, type and gaps |
| US1/AC5 | `static/styles/design/components.css:539`, `:545` | `test` → `...::test_header_gap_matches_the_other_editors` | fields and actions unchanged |
| US1/AC6 | `static/styles/design/components.css:541` | `test` → `...::test_non_verse_editor_header_is_unchanged` | non-verse dialog byte-identical |
| US1/AC7 | `static/styles/design/components.css:541` | `test` → `...::test_single_rule_follows_a_narrow_dialog` | both themes, three viewports |

**Verification split**: 15 test · 3 inspection · 0 manual

## Complexity Tracking

| Violation | Why needed | Simpler alternative rejected because |
| --- | --- | --- |
| | | |

## Project Structure

### Documentation

```
specs/226-verse-modal-header-rule/
  spec.md  plan.md  research.md  data-model.md  quickstart.md  tasks.md
  contracts/  checklists/  preview/
```

### Source

```
static/styles/design/components.css       one large-editor rule group + large head padding
tests/e2e/test_verse_modal_header.py      new E2E for both dialog states and the gap
```

### Structure Decision

The CSS change stays beside the other large-editor rules at `components.css:539–545`, where the
spec 189 size marker's rules already live. The E2E is its own file because the song page's dialog
has a different fetch path from the sidebar editors in `test_editor.py`.
