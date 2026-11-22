# Implementation Plan: Keep Add song when the songbooks sidebar is closed

**Spec**: `specs/222-add-song-parent-closed/spec.md`
**Branch**: `fix/222-add-song-parent-closed`
**Bump**: `patch`
**Preview**: `specs/222-add-song-parent-closed/preview/`

## Technical Context

| Field | Value |
| --- | --- |
| Language / version | Python 3.12, vanilla JS, CSS |
| Primary dependencies | Django 4.0, DRF, Playwright (Python E2E) |
| Storage | PostgreSQL; no schema change in this slice |
| Testing | Django test runner; Playwright `StaticLiveServerTestCase` for user-visible acceptance |
| Target platform | Desktop and phone browsers, 320px–1920px viewport |
| Project type | Server-rendered Django app with vanilla JS reading shell |
| Performance goals | No extra layout, fetch or JS work; one CSS selector changes scope |
| Constraints | Preserve the first sidebar's hide states, hymn read-only and editor behaviour |
| Scale / scope | One CSS rule and one E2E regression test |

## Constitution Check

No `CONSTITUTION.md` exists in this repo; SDD-01 makes it optional. No principles to check.

Re-checked after Phase 1: pass — no constitution file was introduced.

## Phase 0 — Research

See `research.md`. **Unknowns remaining: 0.**

## Phase 1 — Design

- `data-model.md` — no entities; the change is a selector boundary over existing controls.
- `contracts/` — `none.md`: no interface is exposed or changed.
- `quickstart.md` — exact test and preview commands.

## Traceability

| Requirement | Component / file | Verified by | Notes |
| --- | --- | --- | --- |
| FR-001 | `static/styles/design/components.css` | `test` → `tests/e2e/test_editor.py::EditorE2ETests::test_add_song_stays_when_the_songbooks_sidebar_is_closed` | scoped hide rule |
| FR-002 | `static/styles/design/components.css` | `test` → same E2E, display + 38px box | closed parent |
| FR-003 | `static/styles/design/components.css` | `test` → same E2E, `#panelAdd` display none | first-sidebar control still hidden |
| FR-004 | `static/styles/design/components.css` | `test` → same E2E, songs list closed | no control visible |
| FR-005 | editor templates/JS | `inspection` — no editor, form or hymn-book file is touched by this slice | unchanged behaviour |
| SC-001 | E2E | `test` → same E2E | flex, 38px |
| SC-002 | E2E | `test` → same E2E, dialog title | New song |
| SC-003 | E2E | `test` → same E2E | panel add hidden |
| SC-004 | E2E | `test` → same E2E | no visible add control |
| SC-005 | E2E | `test` → same E2E at 1440×900, 1000×800, 390×844 | responsive states |
| US1/AC1 | E2E | `test` → same E2E | real collapse control |
| US1/AC2 | E2E | `test` → same E2E | dialog opens |
| US1/AC3 | CSS state | `test` → same E2E, `data-nav="mini"` set directly | unreachable via Kidung UI |
| US1/AC4 | E2E | `test` → same E2E | songs list closed |
| US1/AC5 | E2E | `test` → same E2E | first sidebar control |
| US1/AC6 | hymn book | `inspection` — no control is rendered for a hymn book; template condition unchanged | read-only preserved |

**Verification split**: 14 test · 2 inspection · 0 manual

## Complexity Tracking

| Violation | Why needed | Simpler alternative rejected because |
| --- | --- | --- |
| none | — | — |

## Project Structure

### Documentation

```
specs/222-add-song-parent-closed/
  spec.md  plan.md  research.md  data-model.md  quickstart.md  tasks.md
  analysis.md  contracts/none.md  checklists/requirements.md  preview/
backlog/items/ITEM-237-add-song-parent-closed.md
```

### Source

```
static/styles/design/components.css   (one rule's selector)
tests/e2e/test_editor.py              (one regression test)
```
