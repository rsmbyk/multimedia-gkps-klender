# Implementation Plan: Enter accepts a delete confirmation

**Spec**: `specs/256-enter-confirms-delete/spec.md` — Accepted at gate 1, 2026-11-28.
**Branch**: `feat/256-enter-confirms` (cut from `origin/develop` at `1cd9f081`; develop advanced to
`1d8f904e` during Specify — see D008)
**Bump**: `patch` — declared here, shown at gate 2, applied only in the pre-merge delivery commit.
`VERSION` will be re-read at Fold; the base in this worktree is 1.37.11 and develop is 1.37.12, so
sibling slice 254 has since claimed 1.37.13, so this slice takes 1.37.14; re-check again at merge.
**Preview**: `specs/256-enter-confirms-delete/preview/` — live, measured before gate 1; values frozen
in the spec's `## UI/UX`.

## Technical Context

| Field | Value |
| --- | --- |
| Language / version | Python 3.12, Django 4.0.1; ES5-style vanilla JS |
| Change surface | one new script, one script tag, four marker attributes, one E2E module |
| Existing patterns | delegated `keydown` handlers in `preview.js`/`generate.js`; data-attribute hooks throughout `static/web/` |
| Storage | none — no model, migration or session state |
| Testing | `tests.e2e.test_enter_delete_confirm`, Playwright Python via `StaticLiveServerTestCase` |
| Constraints | no dependency, route, schema or endpoint change; no commit before Fold; no push without a separate word |

## Constitution Check (before Phase 0)

No `CONSTITUTION.md` at the repo root — nothing to check. Complexity Tracking: empty.

## Phase 0 — Research

See `research.md`: eight decisions D001–D008 with rationale, alternatives and provenance, zero
unknowns. The retired-surface scope and the focus rule were measured in the live preview before gate
1; no further question was needed.

## Phase 1 — Design

`data-model.md` (one DOM marker, no state), `contracts/none.md`, `quickstart.md` (both helper scripts
and the E2E command are runnable). The preview is the live code path itself; its four before/after
rows are the design's verification surface. No new component is invented.

## Constitution Check (after Phase 1)

Unchanged: still no constitution; no Complexity Tracking entry added.

## Traceability

| Requirement | Component / file | Verified by | Notes |
| --- | --- | --- | --- |
| FR-001 | `static/web/enter-delete.js` | `test` → `tests/e2e/test_enter_delete_confirm.py::test_enter_deletes_an_entry_with_focus_away_from_the_button` | Enters on an open confirm and sends one POST |
| FR-002 | `static/web/enter-delete.js` | `test` → `…::test_enter_deletes_a_sidebar_record_with_focus_away_from_the_button`, `…::test_enter_deletes_a_verse_with_focus_away_from_the_button` | Focus on button and on body both covered |
| FR-003 | `_editor_delete_confirm.html`, `entries.js`, `songs_verse.js`, `media_library.html` | `inspection` — only destructive controls carry `data-enter-delete` | grep marker set |
| FR-004 | `static/web/enter-delete.js` | `inspection` — guards for hidden/closed/disabled/repeat/modifiers/prevented | key-event guards at handler head |
| FR-005 | `static/web/enter-delete.js` | `test` → `…::test_enter_accepts_media_removal_with_focus_away_from_the_button` | click counter is exactly 1; default suppressed |
| FR-006 | the four marked templates/scripts | `test` → all four tests | entry, sidebar, verse, media; old row shares entries.js path |
| FR-007 | `static/web/enter-delete.js` | `inspection` — no Escape/Cancel/scrim handler is replaced | only keydown added |
| SC-001 | `preview/probe.py` + `probe-results-*.jsonl` | `test` — probe rows | 0 → 1 activation on all four surfaces |
| SC-002 | `tests/e2e/test_enter_delete_confirm.py` | `test` — four cases | 4 tests, 0 failures |
| SC-003 | `static/web/enter-delete.js` | `inspection` — guard list and marker set | no negative E2E module added |
| SC-004 | copy/leave/generate/screen-mode templates | `inspection` — no `data-enter-delete` on their controls | attribute survey |
| US1/AC4 | `static/web/enter-delete.js` | `inspection` — focus is never read by the handler | Cancel-focus case follows from focus independence |
| US1/AC1 | `static/web/enter-delete.js` | `test` → `…::test_enter_deletes_an_entry_with_focus_away_from_the_button` | probe row records one POST and a closed dialog |
| US1/AC2 | `static/web/enter-delete.js` | `test` → `…::test_enter_deletes_a_sidebar_record_with_focus_away_from_the_button` | record marked inactive/deleted |
| US1/AC3 | `static/web/songs_verse.js` + handler | `test` → `…::test_enter_deletes_a_verse_with_focus_away_from_the_button` | verse soft-deleted |
| US2/AC1 | `media_library.html` + handler | `test` → `…::test_enter_accepts_media_removal_with_focus_away_from_the_button` | click counter exactly 1 |
| US2/AC2 | `static/web/enter-delete.js` | `inspection` — `usable()` guard | disabled control is skipped |

**Verification split**: 10 test · 7 inspection · 0 manual.

## Complexity Tracking

| Violation | Why needed | Simpler alternative rejected because |
| --- | --- | --- |
| | | |

## Project Structure

### Documentation

```
specs/256-enter-confirms-delete/
  spec.md  plan.md  research.md  data-model.md  quickstart.md  tasks.md
  contracts/  checklists/  preview/
```

### Source

```
static/web/enter-delete.js                         (new)
static/web/entries.js                              (one attribute in the confirm markup)
static/web/songs_verse.js                          (one attribute in the confirm markup)
multimedia/web/templates/reading/base.html         (one script tag)
multimedia/web/templates/reading/_editor_delete_confirm.html  (one attribute)
multimedia/web/templates/reading/media_library.html            (one attribute)
tests/e2e/test_enter_delete_confirm.py             (new)
```

### Structure Decision

The handler lives at `static/web/` beside the other reading-app scripts and is loaded once from the
reading base template, which every live surface in scope extends. Marker attributes stay on the
controls that already own the delete logic, so no surface needs a second listener.
