# Implementation Plan: song entry modal has no scrollbar of its own

**Spec**: `specs/236-song-modal-scrollbar/spec.md`
**Branch**: `fix/236-song-modal-scrollbar`
**Bump**: `patch` — develop is `1.36.20` at Plan; the level is applied pre-merge and re-checked then
**Preview**: `specs/236-song-modal-scrollbar/preview/` (static, self-contained)

## Technical Context

| Field | Value |
| --- | --- |
| Language / version | Python 3.12 + Django 4.0 server; vanilla CSS/HTML, no new JavaScript |
| Primary dependencies | none added; Playwright (Python) already supplies user-visible E2E |
| Storage | PostgreSQL for fixtures only; no model, migration or endpoint change |
| Testing | Django test runner; Playwright E2E through `StaticLiveServerTestCase` with a throwaway database |
| Target platform | The shared editor `<dialog>` in the reading pages, desktop and narrow viewports, light and dark themes |
| Project type | Server-rendered Django templates, one shared editor dialog, stylesheet in `static/styles/design/` |
| Performance goals | none; no new work at runtime |
| Constraints | One CSS declaration on the shared `.editor`; no template, script or endpoint edit; the verse-panel collapse animation stays |
| Scale / scope | Every use of `.editor` is affected in principle; verified behaviour is limited to the song-entry states and tall forms |

## Constitution Check

No `CONSTITUTION.md` exists at the base commit — the constitution is optional and never auto-created
(SDD-01), so the table is empty by absence, not by waiver.

Re-checked after Phase 1: pass — no new component, dependency, interface or runtime behaviour.

## Phase 0 — Research

See `research.md`. **Unknowns remaining: 0.**

## Phase 1 — Design

- `data-model.md` — no persisted entity; documents the CSS boxes the rule relies on.
- `contracts/README.md` — `none`: no HTTP, script, model or event interface changes.
- `quickstart.md` — targeted E2E command, local dev server and preview verifier.

## Traceability

| Requirement | Component / file | Verified by | Notes |
| --- | --- | --- | --- |
| US1/AC1 | `static/styles/design/components.css` → `.editor`; `tests/e2e/test_song_modal_scrollbar.py` | `test` → `test_new_song_dialog_has_no_scrollbar_gutter` | gutter `0px`, `overflow-y: clip` |
| US1/AC2 | same file | `test` → `test_new_song_wheel_does_not_scroll_the_dialog` | wheel + thumb cannot move the dialog |
| US1/AC3 | `static/web/entries.js` → song picker; same module | `test` → `test_new_song_results_menu_still_escapes_the_dialog` | `reading/R48` survives |
| US2/AC1 | same CSS rule; same module | `test` → `test_edit_song_collapsed_verses_has_no_scrollbar` | empty-song fixture |
| US2/AC2 | same CSS rule; same module | `test` → `test_edit_song_with_verses_keeps_its_box` | 410px, 0px gutter |
| US3/AC1 | `.editor__content`; same module | `test` → `test_large_form_scrolls_inside_content` | content scrolls, dialog does not |
| US3/AC2 | `.editor`; same module | `test` → `test_short_viewport_scrolls_inside_content` | `86vh` cap; still an inner scrollport |
| FR-001 | `.editor` in `components.css` | `test` → `test_new_song_dialog_has_no_scrollbar_gutter` | dialog is not a scroll container |
| FR-002 | `.editor` computed overflow | `inspection` — computed `overflow-y` is `clip`, no thumb, no gutter; `scrollHeight` may stay 256px | |
| FR-003 | `.editor__content` | `test` → `test_large_form_scrolls_inside_content` | inner `scrollTop` changes |
| FR-004 | `.editor` box and picker position | `inspection` — one-line CSS diff; 480px width, 14px radius, panel animation, fixed picker menu unchanged | |
| SC-001 | New song test module | `test` → `test_new_song_dialog_has_no_scrollbar_gutter` + `test_new_song_wheel_does_not_scroll_the_dialog` | base fails with 5px gutter |
| SC-002 | Edit song test module | `test` → `test_edit_song_collapsed_verses_has_no_scrollbar` | collapsed and settled states |
| SC-003 | Tall-form tests | `test` → `test_large_form_scrolls_inside_content` + `test_short_viewport_scrolls_inside_content` | |
| SC-004 | `preview/index.html` | `inspection` — readouts before `246/256px, 5px` and after `246/256px, 0px` | edit state `410/410px` |
| US3/AC3 | date popover | `inspection` — top-layer popover unaffected by a CSS-only overflow declaration | |

**Verification split**: 12 test · 4 inspection · 0 manual

## Complexity Tracking

| Violation | Why needed | Simpler alternative rejected because |
| --- | --- | --- |
| | | |

No violations.

## Project Structure

### Documentation

```
specs/236-song-modal-scrollbar/
  spec.md plan.md research.md data-model.md quickstart.md tasks.md analysis.md
  contracts/README.md checklists/requirements.md checklists/checklist.md
  preview/README.md preview/index.html preview/build_preview.py
```

### Source

```
static/styles/design/components.css             # one declaration on .editor
tests/e2e/test_song_modal_scrollbar.py          # new E2E module for both entry modes
docs/spec/reading.md                            # R58 added at Fold
backlog/board.md, backlog/items/ITEM-251-*      # card opened in this PR
VERSION, CHANGELOG.md                           # patch line at delivery
```

### Structure Decision

The fix belongs in the shared `.editor` rule, not in the song-entry template: the fault is the
dialog's own scroll container, and the content wrapper already owns scrolling. The E2E module is
new because the existing picker tests measure menus, not the dialog edge; one module keeps the
new/edit geometry evidence together. The preview is static and self-contained because the change
is CSS-only and no fetch behaviour is involved.
